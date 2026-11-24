"""Geometria dei cabinet esplorativi: nessuna simulazione acustica implicita."""
import argparse
import csv
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def finite_positive(*values):
    if any(not math.isfinite(v) or v<=0 for v in values): raise ValueError('Dimensioni finite positive richieste')


def footprint(width,depth,yaw_deg):
    finite_positive(width,depth)
    if not math.isfinite(yaw_deg) or not 0<=yaw_deg<=90: raise ValueError('Angolo richiesto fra 0 e 90 gradi')
    a=math.radians(yaw_deg)
    return width*math.cos(a)+depth*math.sin(a),width*math.sin(a)+depth*math.cos(a)


def panel_specs(width,depth,height,thickness):
    finite_positive(width,depth,height,thickness)
    if min(width,depth,height)<=2*thickness: raise ValueError('Cavita interna non positiva')
    t=thickness;w=width;d=depth;h=height
    return [
        {'name':'Frontale','size':[w,t,h],'position':[0,0,0]},
        {'name':'Posteriore','size':[w,t,h],'position':[0,d-t,0]},
        {'name':'FiancoSinistro','size':[t,d-2*t,h],'position':[0,t,0]},
        {'name':'FiancoDestro','size':[t,d-2*t,h],'position':[w-t,t,0]},
        {'name':'Fondo','size':[w-2*t,d-2*t,t],'position':[t,t,0]},
        {'name':'Cielo','size':[w-2*t,d-2*t,t],'position':[t,t,h-t]},
    ]


def box_contact_area(a,b,tolerance=1e-5):
    """Area di contatto fra parallelepipedi con facce parallele agli assi."""
    overlaps=[min(a[i+1],b[i+1])-max(a[i],b[i]) for i in (0,2,4)]
    if any(v < -tolerance for v in overlaps): return 0
    zero=[v for v in overlaps if abs(v)<=tolerance]
    if len(zero)!=1: return 0
    return math.prod(v for v in overlaps if v>tolerance)


def layout(box,shelf,screen_width):
    w,d,h,t=(box[k] for k in ['width','depth','height','thickness'])
    panels=panel_specs(w,d,h,t)
    finite_positive(shelf['width'],shelf['depth'],screen_width)
    if any(not math.isfinite(shelf[k]) or shelf[k]<0 for k in ['outer_margin','depth_margin','screen_gap']):
        raise ValueError('Margini finiti non negativi richiesti')
    a=math.radians(box['yaw_deg'])
    bx,by=footprint(w,d,box['yaw_deg'])
    max_screen=shelf['width']-2*bx-2*shelf['outer_margin']-2*shelf['screen_gap']
    cy=shelf['depth']/2
    left_x=shelf['outer_margin']+bx/2
    right_x=shelf['width']-shelf['outer_margin']-bx/2
    front_y=cy-d/2*math.cos(a)
    left_front=left_x+d/2*math.sin(a)
    right_front=right_x-d/2*math.sin(a)
    separation=right_front-left_front
    eye=[shelf['width']/2,front_y-separation/(2*math.tan(a))] if box['yaw_deg']>0 and separation>0 else None
    inner=(w-2*t)*(d-2*t)*(h-2*t)/1e6
    return {'footprint':[bx,by],'screen_width_assumed':screen_width,'max_screen_width':max_screen,
            'fits_nominal_rectangle':screen_width<=max_screen+1e-8 and by<=shelf['depth']-2*shelf['depth_margin']+1e-8,
            'depth_slack':shelf['depth']-2*shelf['depth_margin']-by,
            'screen_width_slack':max_screen-screen_width,
            'box_centers':[[left_x,cy],[right_x,cy]],'front_centers':[[left_front,front_y],[right_front,front_y]],
            'front_center_separation':separation,'axis_intersection':eye,
            'internal_gross_l':inner,'wood_volume_l':sum(math.prod(p['size']) for p in panels)/1e6,
            'panels':panels,'actual_support_verified':False,'acoustic_design_approved':False}


def analyse(config):
    rows=[]
    for variant in config['variants']+[config['reference_rejected']]:
        row={'id':variant['id'],'box':variant,'scenarios':[]}
        for screen in config['assumed_screen_widths']:
            result=layout(variant,config['shelf'],screen)
            result['net_volume_sensitivity_l']={str(v):result['internal_gross_l']-v for v in config['assumed_displacements_l']}
            row['scenarios'].append(result)
        rows.append(row)
    return {'status':config['status'],'units':'mm','assumptions':config,'variants':rows}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config',type=Path,default=ROOT/'config/cabinet/studio-st120.json')
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    config=json.loads(args.config.read_text(encoding='utf-8'))
    source=json.loads((ROOT/config['shelf_source']).read_text(encoding='utf-8'))
    official=source['tavolo']['ripiano_superiore']
    for key,actual in [('width',official['larghezza']),('depth',official['profondita']),('height',official['quota_superficie_da_pavimento'])]:
        if config['shelf'][key]!=actual: raise ValueError('Quote config divergenti dalla base del tavolo')
    result=analyse(config)
    args.out.mkdir(parents=True,exist_ok=False)
    (args.out/'ingombri.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    with (args.out/'ingombri.csv').open('w',encoding='utf-8',newline='') as out:
        writer=csv.writer(out)
        writer.writerow(['variante','schermo_ipotizzato_mm','base_X_mm','base_Y_mm','schermo_max_mm','margine_profondita_mm','entra_rettangolo_nominale','volume_lordo_l'])
        for row in result['variants']:
            for s in row['scenarios']:
                writer.writerow([row['id'],s['screen_width_assumed'],*s['footprint'],s['max_screen_width'],s['depth_slack'],s['fits_nominal_rectangle'],s['internal_gross_l']])
    lines=['# Confronto esplorativo, non ordinare pannelli','','| Variante | W × D × H mm | Angolo | Base X × Y mm | Schermo massimo mm | Volume lordo L |','|---|---|---|---|---|---|']
    for row in result['variants']:
        b=row['box'];s=row['scenarios'][0]
        lines.append(f"| {row['id']} | {b['width']} × {b['depth']} × {b['height']} | {b['yaw_deg']}° | {s['footprint'][0]:.2f} × {s['footprint'][1]:.2f} | {s['max_screen_width']:.2f} | {s['internal_gross_l']:.3f} |")
    (args.out/'confronto.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print('\n'.join(lines))


if __name__=='__main__':main()
