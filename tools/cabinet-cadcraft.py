"""Profili 2D esplorativi con CADCraft, DXF riletto e aree confrontate."""
import argparse
import csv
import json
import math
from pathlib import Path
import subprocess

ROOT=Path(__file__).resolve().parents[1]


def run(app,args):
    result=subprocess.run([str(app),*args],capture_output=True,text=True,encoding='utf-8',timeout=30)
    if result.returncode: raise RuntimeError(result.stderr+result.stdout)
    return [json.loads(line) for line in result.stdout.splitlines() if line.strip()]


def verify_shapes(data,dimensions):
    reports=[x for x in data if isinstance(x,dict) and 'shapes' in x]
    if len(reports)!=1: raise RuntimeError('Rapporto CADCraft shapes assente o ambiguo')
    report=reports[0]
    if report['count']!=3 or report['truncated']: raise RuntimeError('Attesi tre profili chiusi completi')
    actual=sorted((s['area'],s['perimeter']) for s in report['shapes'])
    expected=sorted((w*h,2*(w+h)) for w,h in dimensions)
    for found,wanted in zip(actual,expected):
        if not all(math.isclose(a,b,rel_tol=1e-9,abs_tol=1e-4) for a,b in zip(found,wanted)):
            raise RuntimeError(f'Profilo differente: area/perimetro {found}, attesi {wanted}')
    return report


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--app',type=Path,default=Path('C:/Program Files/CADCraft/cadcraft-cli.exe'))
    parser.add_argument('--config',type=Path,default=ROOT/'config/cabinet/studio-st120.json')
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--font',type=Path,default=Path('D:/design-systems/intrawelt-design/assets/fonts/Altro-Grotesk-Book.ttf'))
    parser.add_argument('--errore-scala-per-prova',action='store_true')
    args=parser.parse_args()
    args.out.mkdir(parents=True,exist_ok=False)
    config=json.loads(args.config.read_text(encoding='utf-8'))
    report={'status':'running','variants':[],'not_for_manufacturing':True}
    try:
        for variant in config['variants']:
            name=variant['id'];folder=args.out/name;folder.mkdir()
            w,d,h,t=(variant[k] for k in ['width','depth','height','thickness'])
            dimensions=[(w,h),(d-2*t,h),(w-2*t,d-2*t)]
            names=['Frontale e posteriore','Fianchi','Cielo e fondo']
            command=['run','--metric','--cmd','units '+json.dumps({'insunits':4})]
            if not args.font.is_file(): raise FileNotFoundError('Font di account mancante: indicarlo con --font')
            command+=['--cmd','style '+json.dumps({'name':'Intrawelt','font':args.font.name,'current':True})]
            cursor=0
            for i,((pw,ph),label) in enumerate(zip(dimensions,names)):
                scale=1.05 if args.errore_scala_per_prova and i==0 else 1
                command+=['--cmd','rectang '+json.dumps({'p1':[cursor,0],'p2':[cursor+pw*scale,ph]})]
                for y,text in [(-12,f'{name}: {label}'),(-24,f'{pw} x {ph} mm'),(-36,f'4 pannelli da {t} mm per coppia')]:
                    command+=['--cmd','text '+json.dumps({'at':[cursor,y],'height':5,'text':text})]
                cursor+=pw+40
            dxf=folder/'profili-studio.dxf'
            command+=['--save',str(dxf)]
            creation=run(args.app,command)
            (folder/'creazione.json').write_text(json.dumps(creation,indent=2),encoding='utf-8')
            styles=[s for item in creation if isinstance(item,dict) for s in item.get('styles',[]) if s.get('name')=='Intrawelt']
            if len(styles)!=1 or not styles[0].get('trueType'): raise RuntimeError('CADCraft non ha risolto il font TrueType di account')
            readings=run(args.app,['run',str(dxf),'--cmd','shapes {}'])
            (folder/'rilettura.json').write_text(json.dumps(readings,indent=2),encoding='utf-8')
            shapes=verify_shapes(readings,dimensions)
            lines=dxf.read_text(encoding='utf-8').splitlines()
            markers=[i for i,line in enumerate(lines) if line.strip()=='$INSUNITS']
            if len(markers)!=1 or int(lines[markers[0]+2].strip())!=4: raise RuntimeError('DXF privo di unità millimetri esplicite')
            svg=folder/'profili-studio.svg';png=folder/'profili-studio.png'
            run(args.app,['convert',str(dxf),str(svg)])
            run(args.app,['convert',str(dxf),str(png)])
            with (folder/'distinta-esplorativa.csv').open('w',encoding='utf-8',newline='') as stream:
                writer=csv.writer(stream);writer.writerow(['parte','larghezza_mm','altezza_mm','spessore_mm','quantita_coppia','stato'])
                for label,(pw,ph) in zip(names,dimensions): writer.writerow([label,pw,ph,t,4,'IPOTESI, NON ORDINARE'])
            report['variants'].append({'id':name,'closed_profiles':shapes['count'],'areas_mm2':sorted(s['area'] for s in shapes['shapes']),
                                       'units_insunits':4,'wood_area_pair_m2':4*sum(pw*ph for pw,ph in dimensions)/1e6})
        report['status']='success'
    except Exception as exc:
        report.update(status='failed',error=str(exc));raise
    finally:
        (args.out/'esito.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
        print(args.out/'esito.json')


if __name__=='__main__':main()
