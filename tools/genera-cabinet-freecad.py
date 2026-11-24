"""Scatole esplorative parametriche, senza fori driver e senza ordine di taglio.

freecadcmd; variabili DIY_CABINET_CONFIG e DIY_CABINET_OUT, cartella nuova.
Il rapporto JSON deve essere letto: il codice del solo launcher non basta.
"""
import json
import math
import os
from pathlib import Path
import sys

import FreeCAD as App
import Part

sys.path.insert(0,str(Path(__file__).resolve().parent))
from studia_ingombri import panel_specs,layout,box_contact_area

out=Path(os.environ['DIY_CABINET_OUT'])
out.mkdir(parents=True,exist_ok=False)
config=json.loads(Path(os.environ['DIY_CABINET_CONFIG']).read_text(encoding='utf-8'))
report={'status':'running','version':App.Version()[:3],'variants':[]}


def require(condition,message):
    if not condition: raise RuntimeError(message)


def near(actual,expected,label,tolerance=1e-4):
    require(abs(actual-expected)<=tolerance,f'{label}: {actual} != {expected}')


def local_compound(panels): return Part.makeCompound([p.Shape for p in panels])


def global_compound(group,panels):
    shapes=[]
    for panel in panels:
        shape=panel.Shape.copy()
        shape.Placement=group.Placement.multiply(panel.Placement)
        shapes.append(shape)
    return Part.makeCompound(shapes)


def verify_panels(panels,w,d,h,t):
    for panel in panels:
        require(panel.Shape.isValid() and len(panel.Shape.Solids)==1,'Pannello non valido')
    shape=local_compound(panels)
    expected=w*d*h-(w-2*t)*(d-2*t)*(h-2*t)
    near(shape.Volume,expected,'Volume dei sei pannelli')
    near(shape.BoundBox.XLength,w,'Larghezza locale')
    near(shape.BoundBox.YLength,d,'Profondità locale')
    near(shape.BoundBox.ZLength,h,'Altezza locale')
    adjacency={i:set() for i in range(6)}
    for i in range(6):
        for j in range(i+1,6):
            common=panels[i].Shape.common(panels[j].Shape)
            near(common.Volume,0,'Sovrapposizione fra pannelli')
            bounds=[]
            for panel in [panels[i],panels[j]]:
                b=panel.Shape.BoundBox;bounds.append([b.XMin,b.XMax,b.YMin,b.YMax,b.ZMin,b.ZMax])
            if box_contact_area(*bounds)>1e-4:
                near(panels[i].Shape.distToShape(panels[j].Shape)[0],0,'Distanza delle facce a contatto')
                adjacency[i].add(j);adjacency[j].add(i)
    seen={0};pending=[0]
    while pending:
        for n in adjacency[pending.pop()]-seen: seen.add(n);pending.append(n)
    require(len(seen)==6,'Grafo dei contatti scollegato')
    return expected


def make_panels(doc,group,prefix):
    definitions=[
        ('Frontale',['Larghezza','Spessore','Altezza'],['0 mm','0 mm','0 mm']),
        ('Posteriore',['Larghezza','Spessore','Altezza'],['0 mm','Profondita-Spessore','0 mm']),
        ('FiancoSinistro',['Spessore','Profondita-2*Spessore','Altezza'],['0 mm','Spessore','0 mm']),
        ('FiancoDestro',['Spessore','Profondita-2*Spessore','Altezza'],['Larghezza-Spessore','Spessore','0 mm']),
        ('Fondo',['Larghezza-2*Spessore','Profondita-2*Spessore','Spessore'],['Spessore','Spessore','0 mm']),
        ('Cielo',['Larghezza-2*Spessore','Profondita-2*Spessore','Spessore'],['Spessore','Spessore','Altezza-Spessore']),
    ]
    panels=[]
    def expr(text):
        for key in ['Larghezza','Profondita','Altezza','Spessore']: text=text.replace(key,'Parametri.'+key)
        return text
    for name,sizes,position in definitions:
        panel=doc.addObject('Part::Box',prefix+name)
        group.addObject(panel)
        for axis,formula in zip(['Length','Width','Height'],sizes): panel.setExpression(axis,expr(formula))
        for axis,formula in zip(['x','y','z'],position): panel.setExpression('Placement.Base.'+axis,expr(formula))
        panels.append(panel)
    return panels


try:
    for box in config['variants']:
        w,d,h,t=(box[k] for k in ['width','depth','height','thickness'])
        folder=out/box['id'];folder.mkdir()
        screen=540 if box['id']!='B27' else 620
        expected=layout(box,config['shelf'],screen)
        require(expected['fits_nominal_rectangle'],'Variante fuori dal rettangolo con margini')
        doc=App.newDocument('Studio'+box['id'])
        params=doc.addObject('App::FeaturePython','Parametri')
        for key,value in [('Larghezza',w),('Profondita',d),('Altezza',h),('Spessore',t)]:
            params.addProperty('App::PropertyLength',key,'Dimensioni esplorative');setattr(params,key,value)
        params.addProperty('App::PropertyString','Stato','Avvertenze').Stato=config['status']
        params.addProperty('App::PropertyString','Materiale','Avvertenze').Materiale='MDF 18 mm ipotizzato; nessuna verifica strutturale'
        params.addProperty('App::PropertyString','Rotazione','Avvertenze').Rotazione=f'{box["yaw_deg"]} gradi, input JSON; rigenerare per cambiare angolo'
        left=doc.addObject('App::Part','Sinistra');right=doc.addObject('App::Part','Destra')
        left_panels=make_panels(doc,left,'S_');right_panels=make_panels(doc,right,'D_')
        a=math.radians(box['yaw_deg']);si=math.sin(a);co=math.cos(a)
        shelf=config['shelf'];cx=shelf['width'];cy=shelf['depth']/2;edge=shelf['outer_margin']
        left.Placement=App.Placement(App.Vector(),App.Rotation(App.Vector(0,0,1),box['yaw_deg']))
        right.Placement=App.Placement(App.Vector(),App.Rotation(App.Vector(0,0,1),-box['yaw_deg']))
        test_shift=float(os.environ.get('DIY_CABINET_TEST_SHIFT_X','0'))
        left.setExpression('Placement.Base.x',f'{edge+test_shift} mm + {si}*Parametri.Profondita')
        left.setExpression('Placement.Base.y',f'{cy} mm - ({si}*Parametri.Larghezza + {co}*Parametri.Profondita)/2')
        right.setExpression('Placement.Base.x',f'{cx-edge} mm - ({co}*Parametri.Larghezza + {si}*Parametri.Profondita)')
        right.setExpression('Placement.Base.y',f'{cy} mm + {si}*Parametri.Larghezza/2 - {co}*Parametri.Profondita/2')
        left.Placement.Base.z=right.Placement.Base.z=shelf['height']
        shelf_obj=doc.addObject('Part::Box','RipianoProxy')
        shelf_obj.Label='Ripiano nominale, spessore grafico 18 mm, rientranze non modellate'
        shelf_obj.Length=shelf['width'];shelf_obj.Width=shelf['depth'];shelf_obj.Height=18
        shelf_obj.Placement.Base.z=shelf['height']-18
        interval=doc.addObject('Part::Feature','LarghezzaSchermo')
        interval.Label=f'Sola larghezza schermo ipotizzata {screen} mm, nessun piedistallo'
        interval.Shape=Part.makeLine(App.Vector((cx-screen)/2,cy,shelf['height']+1),App.Vector((cx+screen)/2,cy,shelf['height']+1))
        doc.recompute()
        volume=verify_panels(left_panels,w,d,h,t)
        verify_panels(right_panels,w,d,h,t)
        params.Larghezza=w+10;doc.recompute()
        changed=verify_panels(left_panels,w+10,d,h,t)
        near(changed-volume,10*(d*h-(d-2*t)*(h-2*t)),'Ricomputazione volume indipendente')
        params.Larghezza=w;doc.recompute()
        global_left=global_compound(left,left_panels);global_right=global_compound(right,right_panels)
        for axis,wanted in [('XLength',expected['footprint'][0]),('YLength',expected['footprint'][1]),('ZLength',h)]:
            near(getattr(global_left.BoundBox,axis),wanted,'Ingombro trasformato '+axis)
        near(global_left.BoundBox.ZMin,shelf['height'],'Quota appoggio')
        near(global_left.BoundBox.XMin,edge,'Posizione nominale sinistra')
        near(global_right.BoundBox.XMax,shelf['width']-edge,'Posizione nominale destra')
        for shape in [global_left,global_right]:
            near(shape.BoundBox.YMin,(shelf['depth']-expected['footprint'][1])/2,'Posizione profondità minima')
            near(shape.BoundBox.YMax,(shelf['depth']+expected['footprint'][1])/2,'Posizione profondità massima')
        near(global_left.common(global_right).Volume,0,'Interferenza fra cabinet')
        export=doc.addObject('Part::Feature','EsportazioneTemporanea');export.Shape=global_left
        step=folder/'cabinet-sinistro.step';Part.export([export],str(step))
        restored=Part.read(str(step))
        require(restored.isValid() and len(restored.Solids)==6,'STEP non contiene sei solidi validi')
        near(restored.Volume,volume,'Volume STEP')
        for axis in ['XLength','YLength','ZLength','XMin','YMin','ZMin']:
            near(getattr(restored.BoundBox,axis),getattr(global_left.BoundBox,axis),'STEP '+axis)
        doc.removeObject(export.Name)
        native=folder/'studio.FCStd';doc.recompute();doc.saveAs(str(native));App.closeDocument(doc.Name)
        doc=App.openDocument(str(native));doc.recompute()
        verify_panels([doc.getObject('S_'+p['name']) for p in panel_specs(w,d,h,t)],w,d,h,t)
        near(doc.getObject('Parametri').Larghezza.Value,w,'Parametro riaperto')
        App.closeDocument(doc.Name)
        item={'id':box['id'],'status':'success','volume_wood_one_mm3':volume,'gross_internal_l':expected['internal_gross_l'],
              'footprint_mm':expected['footprint'],'panels_one_box':panel_specs(w,d,h,t),'native':str(native),'step':str(step),
              'actual_support_verified':False,'driver_holes_defined':False}
        (folder/'esito.json').write_text(json.dumps(item,indent=2),encoding='utf-8')
        report['variants'].append(item)
    report['status']='success'
except Exception as exc:
    report.update(status='failed',error=str(exc))
    raise
finally:
    (out/'esito.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(out/'esito.json')
