"""Tavole nominali dei sette pannelli con CADCraft, DXF riletto prima della consegna."""
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import subprocess
from progetto_cabinet import ROOT, load_project, analyse_variant
from font_intrawelt import resolve_fonts, font_hashes


def run(app,args):
    result=subprocess.run([str(app),*args],capture_output=True,text=True,encoding='utf-8',timeout=60)
    if result.returncode: raise RuntimeError(result.stderr+result.stdout)
    return [json.loads(line) for line in result.stdout.splitlines() if line.strip()]


def verify_shapes(readings,expected):
    reports=[r for r in readings if isinstance(r,dict) and 'shapes' in r]
    if len(reports)!=1 or reports[0]['truncated'] or reports[0]['count']!=len(expected):
        raise RuntimeError('Profilatura CADCraft assente, troncata o con forme inattese')
    key=lambda shape:(round(shape['centroid'][0],6),round(shape['centroid'][1],6),round(shape['area'],6))
    for actual,wanted in zip(sorted(reports[0]['shapes'],key=key),sorted(expected,key=key)):
        values=[actual['area'],actual['perimeter'],*actual['centroid']]
        targets=[wanted['area'],wanted['perimeter'],*wanted['centroid']]
        if not all(math.isclose(a,b,rel_tol=1e-9,abs_tol=1e-5) for a,b in zip(values,targets)):
            raise RuntimeError('Raggio o profilo CADCraft differente dalle quote nominali')
    return reports[0]['count']


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--app',type=Path,default=Path('C:/Program Files/CADCraft/cadcraft-cli.exe'))
    parser.add_argument('--font',type=Path,help='File Altro Grotesk Book; altrimenti usa i font di account')
    parser.add_argument('--solo-verifica',action='store_true')
    parser.add_argument('--errore-raggio-per-prova',action='store_true')
    args=parser.parse_args()
    args.out.mkdir(parents=True,exist_ok=False)
    report={'status':'running','application':'CADCraft 0.20.1','variants':[],
            'manufacturing_release':False,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    try:
        if args.font is None:
            args.font=resolve_fonts(required=('Altro-Grotesk-Book.ttf',))/'Altro-Grotesk-Book.ttf'
        if not args.font.is_file(): raise FileNotFoundError('Font Intrawelt assente: correggere --font')
        report['font_sha256']=font_hashes(args.font.parent,required=(args.font.name,))
        report['dependency_sha256']={'tools/font_intrawelt.py':hashlib.sha256((ROOT/'tools/font_intrawelt.py').read_bytes()).hexdigest()}
        config,drivers=load_project()
        for variant in config['variants']:
            geo=analyse_variant(variant,drivers);w,d,h=geo['external_dimensions_mm']
            folder=args.out/geo['id'];folder.mkdir()
            commands=['run','--metric','--cmd','units '+json.dumps({'insunits':4}),
                '--cmd','style '+json.dumps({'name':'Intrawelt','font':args.font.name,'current':True})]
            expected=[];bom=[]
            def command(name,data): commands.extend(['--cmd',name+' '+json.dumps(data)])
            def rect(x,y,width,height):
                command('rectang',{'p1':[x,y],'p2':[x+width,y+height]})
                expected.append({'area':width*height,'perimeter':2*(width+height),
                                 'centroid':[x+width/2,y+height/2]})
            def text(x,y,value): command('text',{'at':[x,y],'height':6,'text':value})
            for n,panel in enumerate(geo['panels']):
                if n<2: pw,ph=panel['size'][0],panel['size'][2]
                elif n<4: pw,ph=panel['size'][1],panel['size'][2]
                else: pw,ph=panel['size'][0],panel['size'][1]
                x=(n%4)*(w+60);y=(n//4)*(h+120)
                rect(x,y,pw,ph)
                text(x,y-16,f"{geo['id']} {panel['name']} - {pw:g} x {ph:g} mm")
                text(x,y-29,f"MDF {geo['thickness_mm']:g} mm - quantita coppia: 2")
                bom.append([panel['name'],pw,ph,geo['thickness_mm'],2])
            for opening in geo['openings']:
                cx,cy=opening['x_mm'],opening['z_mm']
                for kind in ('cut','rebate'):
                    radius=opening[kind+'_diameter_mm']/2
                    used=radius*1.02 if args.errore_raggio_per_prova and kind=='cut' else radius
                    command('circle',{'center':[cx,cy],'radius':used})
                    expected.append({'area':math.pi*radius**2,'perimeter':2*math.pi*radius,'centroid':[cx,cy]})
            for n,opening in enumerate(geo['openings']):
                text(0,-43-13*n,f"{opening['role']}: foro {opening['cut_diameter_mm']:g}; incasso {opening['rebate_diameter_mm']:g} x {opening['rebate_depth_mm']:g}")
            for centre in geo['mount_centres']:
                x,y=centre['x_mm'],centre['z_mm']
                command('line',{'points':[[x-2,y],[x+2,y]]})
                command('line',{'points':[[x,y-2],[x,y+2]]})
            text(0,-82,'Croci: centri fissaggio nominali, non fori pilota.')
            x=2*(w+60);y=h+120
            bw,bd,bt=geo['brace']['size_mm']
            border=variant['brace_border_mm']
            rect(x,y,bw,bd);rect(x+border,y+border,bw-2*border,bd-2*border)
            text(x,y-16,f"Rinforzo {bw:g} x {bd:g} x {bt:g} mm - quantita coppia: 2")
            text(x,y-29,f"Bordo finestra {border:g} mm; quota inferiore {variant['brace_z_mm']:g} mm")
            bom.append(['Rinforzo',bw,bd,bt,2])
            text(0,h+120+max(d,bd)+40,'STUDIO NOMINALE - NON ORDINARE PANNELLI DA QUESTA TAVOLA')
            dxf=folder/'pannelli-e-frontale.dxf'
            commands.extend(['--save',str(dxf)])
            creation=run(args.app,commands)
            styles=[s for item in creation if isinstance(item,dict) for s in item.get('styles',[]) if s.get('name')=='Intrawelt']
            if len(styles)!=1 or not styles[0].get('trueType'): raise RuntimeError('Font di account non risolto da CADCraft')
            readings=run(args.app,['run',str(dxf),'--cmd','shapes {}'])
            count=verify_shapes(readings,expected)
            lines=dxf.read_text(encoding='utf-8').splitlines()
            unit=[i for i,line in enumerate(lines) if line.strip()=='$INSUNITS']
            if len(unit)!=1 or lines[unit[0]+2].strip()!='4': raise RuntimeError('DXF non dichiarato in mm')
            with (folder/'distinta-coppia.csv').open('w',encoding='utf-8',newline='') as stream:
                writer=csv.writer(stream);writer.writerow(['parte','larghezza_mm','altezza_mm','spessore_mm','quantita_coppia']);writer.writerows(bom)
            (folder/'rilettura.json').write_text(json.dumps(readings,indent=2),encoding='utf-8')
            if not args.solo_verifica:
                for suffix in ('svg','pdf','png'):
                    run(args.app,['convert',str(dxf),str(folder/('pannelli-e-frontale.'+suffix))])
            report['variants'].append({'id':geo['id'],'shapes_verified':count,'units_mm':True,
                                       'dxf_sha256':hashlib.sha256(dxf.read_bytes()).hexdigest(),
                                       'files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in folder.iterdir()
                                                if p.is_file() and p.suffix in ('.dxf','.pdf','.svg','.csv')}})
        report['status']='success'
    except Exception as exc:
        report.update(status='failed',error=str(exc));raise
    finally:
        (args.out/'esito.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False))


if __name__=='__main__':
    main()
