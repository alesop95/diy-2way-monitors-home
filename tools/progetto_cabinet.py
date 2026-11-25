"""Geometria nominale dei frontali e del rinforzo: non autorizza la fabbricazione."""
import copy
import json
import math
from pathlib import Path
from studia_ingombri import panel_specs

ROOT = Path(__file__).resolve().parents[1]


def load_project():
    config = json.loads((ROOT/'config/cabinet/progetto-candidato.json').read_text(encoding='utf-8'))
    boxes = json.loads((ROOT/config['boxes_source']).read_text(encoding='utf-8'))
    drivers = json.loads((ROOT/config['drivers_source']).read_text(encoding='utf-8'))['drivers']
    canonical = {b['id']: b for b in boxes['variants']}
    config = copy.deepcopy(config)
    config['variants'] = [{**config['geometry_assumptions'], **v,
                           'cabinet': canonical[v['id']]} for v in config['variants']]
    return config, drivers


def analyse_variant(variant, drivers):
    box = variant['cabinet']
    w, d, h, t = (float(box[k]) for k in ('width','depth','height','thickness'))
    panels = panel_specs(w,d,h,t)
    gap, web = (variant[k] for k in ('diameter_clearance_mm','minimum_web_mm'))
    border, front_gap, bz = (variant[k] for k in ('brace_border_mm','brace_front_gap_mm','brace_z_mm'))
    for value in (gap, web, border, front_gap, bz):
        if not math.isfinite(value) or value < 0:
            raise ValueError('Giochi e rinforzo finiti e non negativi richiesti')
    iw, bd = w-2*t, d-2*t-front_gap
    if border <= 0 or 2*border >= min(iw,bd) or not t <= bz < h-2*t:
        raise ValueError('Rinforzo privo di finestra o fuori dalla cavita')
    brace = {'size_mm':[iw,bd,t], 'position_mm':[t,t+front_gap,bz],
             'window_size_mm':[iw-2*border,bd-2*border],
             'window_position_mm':[t+border,t+front_gap+border,bz],
             'volume_mm3':(iw*bd-(iw-2*border)*(bd-2*border))*t,
             'side_contact_area_mm2':2*bd*t, 'rear_contact_area_mm2':iw*t}
    openings, mounts, removed, free_depth = [], [], 0., math.inf
    for role in ('woofer','tweeter'):
        driver = drivers[variant[role]]
        cx, cz = w/2, float(variant[role+'_z_mm'])
        cut = driver['rear_diameter_mm'] + gap
        rebate = driver['outer_diameter_mm'] + gap
        depth = driver['flange_thickness_mm']
        if not all(math.isfinite(v) and v > 0 for v in (cut,rebate,depth,driver['overall_depth_mm'])):
            raise ValueError('Quote driver non fisiche')
        if cut >= rebate or depth >= t or not math.isfinite(cz):
            raise ValueError('Taglio/incasso non fisico nel frontale')
        if min(cx, w-cx, cz, h-cz) - rebate/2 < web:
            raise ValueError('Incasso fuori dal frontale o bordo insufficiente')
        remaining = d-t-driver['overall_depth_mm']
        if remaining < web:
            raise ValueError('Driver contro il posteriore')
        free_depth = min(free_depth,remaining)
        # Inviluppo conservativo: il cestello e' un cilindro pieno del diametro posteriore.
        radius = driver['rear_diameter_mm']/2
        overlap_z = min(cz+radius,bz+t)-max(cz-radius,bz)
        overlap_y = min(driver['overall_depth_mm'],d-t)-max(depth,t+front_gap)
        if overlap_z > 0 and overlap_y > 0:
            raise ValueError('Inviluppo driver in interferenza col rinforzo')
        removed += math.pi*((cut/2)**2*t + ((rebate/2)**2-(cut/2)**2)*depth)
        opening = {'role':role, 'driver':variant[role], 'x_mm':cx, 'z_mm':cz,
                   'cut_diameter_mm':cut, 'rebate_diameter_mm':rebate,
                   'rebate_depth_mm':depth,'driver_depth_envelope_mm':driver['overall_depth_mm'],
                   'minimum_edge_web_mm':min(cx,w-cx,cz,h-cz)-rebate/2}
        openings.append(opening)
        for n in range(driver['mount_count']):
            a=math.radians(driver['mount_angle_deg'] + 360*n/driver['mount_count'])
            mounts.append({'role':role, 'x_mm':cx+driver['mount_pcd_mm']/2*math.cos(a),
                           'z_mm':cz+driver['mount_pcd_mm']/2*math.sin(a),
                           'status':'CENTRO NOMINALE; diametro pilota da fissaggio, non definito'})
    spacing = math.dist([openings[0]['x_mm'],openings[0]['z_mm']],
                        [openings[1]['x_mm'],openings[1]['z_mm']])
    between = spacing - sum(o['rebate_diameter_mm']/2 for o in openings)
    if between < web:
        raise ValueError('Driver in interferenza o ponte fra incassi insufficiente')
    front_volume = w*h*t-removed
    total_wood = sum(math.prod(p['size']) for p in panels)-removed+brace['volume_mm3']
    return {'id':variant['id'], 'external_dimensions_mm':[w,d,h], 'thickness_mm':t,
            'panels':panels,'openings':openings,'mount_centres':mounts,'brace':brace,
            'driver_spacing_mm':spacing, 'between_rebates_web_mm':between,
            'front_volume_mm3':front_volume,'wood_volume_per_cabinet_l':total_wood/1e6,
            'wood_area_pair_before_holes_m2':2*sum(p['size'][0]*p['size'][2] if p['name'] in ('Frontale','Posteriore')
                else p['size'][1]*p['size'][2] if p['name'].startswith('Fianco')
                else p['size'][0]*p['size'][1] for p in panels)/1e6 + 2*iw*bd/1e6,
            'cavity_after_brace_l':(iw*(d-2*t)*(h-2*t)-brace['volume_mm3'])/1e6,
            'nominal_internal_free_depth_mm':free_depth,
            'acoustic_design_approved':False,'actual_support_verified':False,
            'manufacturing_release':False}
