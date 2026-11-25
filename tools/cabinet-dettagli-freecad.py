"""Assieme nominale FreeCAD a sette pannelli, fori/incassi e rinforzo.

Eseguire con freecadcmd; DIY_DETAIL_OUT deve indicare una cartella nuova.
Il rapporto esito.json prevale sul codice del launcher FreeCAD.
"""
import copy
import hashlib
import json
import math
import os
from pathlib import Path
import sys
import FreeCAD as App
import Part

sys.path.insert(0,str(Path(__file__).resolve().parent))
from progetto_cabinet import ROOT, load_project, analyse_variant

out=Path(os.environ['DIY_DETAIL_OUT'])
out.mkdir(parents=True,exist_ok=False)
report={'status':'running','version':App.Version()[:3], 'variants':[],
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'input_sha256':{name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in
            ('tools/progetto_cabinet.py','tools/studia_ingombri.py','data/driver-geometria.json',
             'config/cabinet/progetto-candidato.json','config/cabinet/studio-st120.json')},
        'manufacturing_release':False}


def near(actual,expected,label):
    if not math.isclose(actual,expected,rel_tol=1e-9,abs_tol=1e-3):
        raise RuntimeError(f'{label}: {actual} != {expected}')


def validate(wood,geo):
    if any(not o.Shape.isValid() or len(o.Shape.Solids)!=1 for o in wood):
        raise RuntimeError('Pannello non valido o non connesso')
    near(sum(o.Shape.Volume for o in wood),geo['wood_volume_per_cabinet_l']*1e6,'Volume sette pannelli')
    near(wood[0].Shape.Volume,geo['front_volume_mm3'],'Volume frontale forato')
    near(wood[-1].Shape.Volume,geo['brace']['volume_mm3'],'Volume rinforzo')
    for i,left in enumerate(wood):
        for right in wood[i+1:]:
            near(left.Shape.common(right.Shape).Volume,0,'Interferenza fra pannelli')
    compound=Part.makeCompound([o.Shape for o in wood])
    for actual,expected in zip((compound.BoundBox.XLength,compound.BoundBox.YLength,compound.BoundBox.ZLength),geo['external_dimensions_mm']):
        near(actual,expected,'Dimensione assieme')
    return compound


def make_document(variant,drivers):
    geo=analyse_variant(variant,drivers)
    doc=App.newDocument('Cabinet_'+variant['id'])
    sheet=doc.addObject('Spreadsheet::Sheet','Quote')
    w,d,h=geo['external_dimensions_mm'];t=geo['thickness_mm']
    params={'W':w,'D':d,'H':h,'T':t,'BraceZ':variant['brace_z_mm'],
            'FrontGap':variant['brace_front_gap_mm'],'Border':variant['brace_border_mm']}
    for opening,suffix in zip(geo['openings'],('W','T')):
        params.update({'Cut'+suffix:opening['cut_diameter_mm'],'Rebate'+suffix:opening['rebate_diameter_mm'],
                       'Depth'+suffix:opening['rebate_depth_mm'],'Centre'+suffix:opening['z_mm']})
    cells={}
    for row,(name,value) in enumerate(params.items(),1):
        sheet.set('A'+str(row),name);sheet.set('B'+str(row),str(value)+' mm')
        sheet.setAlias('B'+str(row),'Dim'+name);cells[name]='B'+str(row)
    def box(name,dims,position):
        obj=doc.addObject('Part::Box',name)
        for prop,expr in zip(('Length','Width','Height'),dims): obj.setExpression(prop,expr)
        for axis,expr in zip(('x','y','z'),position): obj.setExpression('Placement.Base.'+axis,expr)
        return obj
    q='Quote.Dim'
    front=box('FrontalePieno',(q+'W',q+'T',q+'H'),('0 mm','0 mm','0 mm'))
    for suffix in ('W','T'):
        for cut in (True,False):
            cylinder=doc.addObject('Part::Cylinder',('Taglio' if cut else 'Incasso')+suffix)
            factor='0.51' if cut and os.environ.get('DIY_DETAIL_NEGATIVE_RADIUS')=='1' else '0.5'
            cylinder.setExpression('Radius',q+('Cut' if cut else 'Rebate')+suffix+'*'+factor)
            cylinder.setExpression('Height',q+'T+2 mm' if cut else q+'Depth'+suffix+'+1 mm')
            cylinder.Placement.Rotation=App.Rotation(App.Vector(1,0,0),-90)
            cylinder.setExpression('Placement.Base.x',q+'W/2')
            cylinder.Placement.Base.y=-1
            cylinder.setExpression('Placement.Base.z',q+'Centre'+suffix)
            result=doc.addObject('Part::Cut','Frontale_'+cylinder.Name)
            result.Base=front;result.Tool=cylinder;front=result
    front.Label='Frontale con tagli e incassi nominali'
    back=box('Posteriore',(q+'W',q+'T',q+'H'),('0 mm',q+'D-'+q+'T','0 mm'))
    left=box('FiancoSinistro',(q+'T',q+'D-2*'+q+'T',q+'H'),('0 mm',q+'T','0 mm'))
    right=box('FiancoDestro',(q+'T',q+'D-2*'+q+'T',q+'H'),(q+'W-'+q+'T',q+'T','0 mm'))
    bottom=box('Fondo',(q+'W-2*'+q+'T',q+'D-2*'+q+'T',q+'T'),(q+'T',q+'T','0 mm'))
    top=box('Cielo',(q+'W-2*'+q+'T',q+'D-2*'+q+'T',q+'T'),(q+'T',q+'T',q+'H-'+q+'T'))
    brace_outer=box('RinforzoPieno',(q+'W-2*'+q+'T',q+'D-2*'+q+'T-'+q+'FrontGap',q+'T'),
                    (q+'T',q+'T+'+q+'FrontGap',q+'BraceZ'))
    window=box('FinestraRinforzo',(q+'W-2*'+q+'T-2*'+q+'Border',
               q+'D-2*'+q+'T-'+q+'FrontGap-2*'+q+'Border',q+'T+2 mm'),
               (q+'T+'+q+'Border',q+'T+'+q+'FrontGap+'+q+'Border',q+'BraceZ-1 mm'))
    brace=doc.addObject('Part::Cut','Rinforzo');brace.Base=brace_outer;brace.Tool=window
    doc.recompute()
    return doc,sheet,cells,[front,back,left,right,bottom,top,brace],geo


try:
    config,drivers=load_project()
    for variant in config['variants']:
        folder=out/variant['id'];folder.mkdir()
        doc,sheet,cells,wood,geo=make_document(variant,drivers)
        validate(wood,geo)
        altered=copy.deepcopy(variant);altered['cabinet']['width']+=10
        sheet.set(cells['W'],str(altered['cabinet']['width'])+' mm');doc.recompute()
        validate(wood,analyse_variant(altered,drivers))
        sheet.set(cells['W'],str(variant['cabinet']['width'])+' mm');doc.recompute()
        compound=validate(wood,geo)
        for obj in doc.Objects:
            if obj.ViewObject: obj.ViewObject.Visibility=obj in wood
        native=folder/'cabinet-nominale.FCStd'
        step=folder/'cabinet-nominale.step'
        names=[obj.Name for obj in wood]
        doc.saveAs(str(native));App.closeDocument(doc.Name)
        reopened=App.openDocument(str(native));reopened.recompute()
        restored=[reopened.getObject(name) for name in names]
        validate(restored,geo)
        Part.export(restored,str(step))
        imported=Part.read(str(step))
        if not imported.isValid() or len(imported.Solids)!=7:
            raise RuntimeError('STEP non conserva sette solidi validi')
        near(imported.Volume,compound.Volume,'Volume STEP reimportato')
        for actual,expected in zip((imported.BoundBox.XLength,imported.BoundBox.YLength,imported.BoundBox.ZLength),geo['external_dimensions_mm']):
            near(actual,expected,'Ingombro STEP reimportato')
        report['variants'].append({'id':variant['id'],'solids':7,'native_reopened':True,
            'width_mutation_mm':10,'step_reimported':True,'wood_volume_mm3':compound.Volume,
            'front_volume_mm3':geo['front_volume_mm3'],'brace_volume_mm3':geo['brace']['volume_mm3'],
            'native_sha256':hashlib.sha256(native.read_bytes()).hexdigest(),
            'step_sha256':hashlib.sha256(step.read_bytes()).hexdigest()})
        App.closeDocument(reopened.Name)
    report['status']='success'
except Exception as exc:
    report.update(status='failed',error=str(exc))
    raise
finally:
    (out/'esito.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
