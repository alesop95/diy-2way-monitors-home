"""Confronto nominale riproducibile di reflex, direttivita, geometria e livelli.

Non apre periferiche, non cambia profili, non qualifica hardware o tagli.
"""
import argparse
from datetime import datetime
import hashlib
import itertools
import json
import math
from pathlib import Path
import sys
import numpy as np
import acustica_cabinet as ac
from fattibilita_basso import lr4_hp, target_frequency, transform
from progetto_cabinet import load_project, analyse_variant
from studio_sistema_audio import closed_box

ROOT = Path(__file__).resolve().parents[1]
INPUTS = ('tools/studio_completamento.py','tools/acustica_cabinet.py','tools/progetto_cabinet.py',
          'tools/studia_ingombri.py','tools/studio_sistema_audio.py','tools/fattibilita_basso.py',
          'data/driver-candidati.json','data/driver-geometria.json',
          'config/cabinet/progetto-candidato.json','config/cabinet/studio-st120.json')


def radiation_requirements(frequency, cone_response, port_response, sd_cm2, area_m2, level_db):
    """Picchi per eccitazione con passabanda ideale level_db in 4pi a 1 m.

    Cono e condotto devono già includere l'eventuale HP comune. Il livello
    e' RMS di una sinusoide, non una misura dell'ascolto o del guadagno reale.
    """
    f=np.asarray(frequency,dtype=float)
    if np.any(~np.isfinite(f)) or np.any(f<=0) or sd_cm2<=0 or area_m2<=0 or not math.isfinite(level_db):
        raise ValueError('Parametri di radiazione non fisici')
    w=2*math.pi*f
    pressure=20e-6*10**(level_db/20)
    flow_peak=4*math.pi*pressure*math.sqrt(2)/(ac.AIR_DENSITY*w)
    return {'excursion_peak_mm':flow_peak*abs(np.asarray(cone_response))/(w*sd_cm2*1e-4)*1000,
            'port_velocity_peak_m_s':flow_peak*abs(np.asarray(port_response))/area_m2}


def _db(value):
    return float(20*np.log10(max(abs(value),1e-15)))


def build_report():
    config,geometry=load_project()
    assumptions=config['acoustic_assumptions']
    driver_data=json.loads((ROOT/'data/driver-candidati.json').read_text(encoding='utf-8'))
    woofers={v['id']:v for v in driver_data['woofers']}
    f=np.geomspace(20,500,801)
    hp=lr4_hp(f,driver_data['design_assumptions']['highpass_hz'])
    target=target_frequency(60,-2,driver_data['design_assumptions']['highpass_hz'])
    angles=np.array([-60.,-45.,-30.,-20.,-10.,0.,10.,20.,30.,45.,60.])
    reflex,sealed,directivity,electrical,details=[],[],[],[],[]
    for variant in config['variants']:
        geo=analyse_variant(variant,geometry);details.append(geo)
        driver=woofers[variant['woofer']]
        b=variant['cabinet'];w,d,h,t=(b[k] for k in ('width','depth','height','thickness'))
        gross=(w-2*t)*(d-2*t)*(h-2*t)/1e6
        available=gross-assumptions['component_displacement_before_port_l']
        if available<=0: raise ValueError('Volume utile prima del tubo non positivo')
        scale=math.sqrt(1+driver['vas_l']/available)
        fc,qtc=driver['fs_hz']*scale,driver['qts']*scale
        raw=closed_box(f,driver['fs_hz'],driver['qts'],driver['vas_l'],available)
        eq=transform(f,fc,qtc,target,1/math.sqrt(2))
        boost=float(np.max(20*np.log10(abs(eq)*hp)))
        sealed.append({'id':variant['id'],'driver':driver['id'],'net_assumed_l':available,
                       'raw_60_db':_db(closed_box(60,driver['fs_hz'],driver['qts'],driver['vas_l'],available)),
                       'lt_hp35_peak_gain_db':boost,'fc_hz':fc,'qtc':qtc})
        for fb,diameter,quality in itertools.product(assumptions['tuning_hz'],
                assumptions['port_diameter_mm'],assumptions['port_q']):
            port=ac.port_geometry(available,fb,diameter,assumptions['port_wall_mm'],
                                 assumptions['port_end_factor'],panel_thickness_mm=t)
            response=ac.vented_box(f,driver['fs_hz'],driver['qts'],driver['vas_l'],port['net_volume_l'],fb,quality)
            motion=radiation_requirements(f,response['cone']*hp,response['port']*hp,driver['sd_cm2'],
                                         port['area_m2'],assumptions['reference_level_db_spl_1m_fullspace'])
            peak_x=float(np.max(motion['excursion_peak_mm']))
            peak_speed=float(np.max(motion['port_velocity_peak_m_s']))
            fit=(port['internal_length_mm']+diameter*assumptions['rear_port_clearance_diameters']<=d-2*t)
            h60=ac.vented_box(60,driver['fs_hz'],driver['qts'],driver['vas_l'],port['net_volume_l'],fb,quality)
            reflex.append({'id':variant['id'],'driver':driver['id'],'fb_hz':fb,'diameter_mm':diameter,
                'port_q_hypothetical':quality,**port,'straight_geometry_fits':fit,
                'raw_60_db':_db(h60['total']),'protected_60_db':_db(h60['total']*lr4_hp(60,35)),
                'excursion_peak_max_mm':peak_x,'xmax_oneway_mm':driver['xmax_oneway_mm'],
                'within_xmax':peak_x<=driver['xmax_oneway_mm'],
                'port_velocity_peak_max_m_s':peak_speed,'port_mach_peak_max':peak_speed/ac.SOUND_SPEED})
        for crossover,offset in itertools.product(assumptions['crossover_hz'],assumptions['depth_offsets_mm']):
            args=(driver['sd_cm2'],geometry[variant['tweeter']]['sd_cm2'],geo['driver_spacing_mm'],crossover,offset)
            vertical=ac.two_way_response(crossover,angles,*args)
            horizontal=ac.two_way_response(crossover,angles,*args,plane='horizontal')
            cap=ac.two_way_response(crossover,0,*args,capacitor_uf=assumptions['series_capacitor_uf'],
                                    tweeter_re_ohm=assumptions['tweeter_resistance_ohm'])
            directivity.append({'id':variant['id'],'crossover_hz':crossover,'depth_offset_mm':offset,
                'vertical_at_crossover_db':[_db(v) for v in vertical],
                'horizontal_at_crossover_db':[_db(v) for v in horizontal],
                'on_axis_without_capacitor_db':_db(ac.two_way_response(crossover,0,*args)),
                'on_axis_with_capacitor_db':_db(cap)})
        for gain,mode in itertools.product(assumptions['hypothetical_amplifier_gain_db'],('mix','ascolto')):
            shelf=2 if mode=='ascolto' else 0
            pre=driver_data['design_assumptions']['pre_gain_db']
            dac=ac.dbu_to_vrms(assumptions['interface_fullscale_dbu'])
            voltage=dac*10**((pre-6+boost+shelf+gain)/20)
            tweet=dac*10**((pre-6+driver_data['design_assumptions']['tweeter_trim_db']+gain)/20)
            electrical.append({'id':variant['id'],'mode':mode,'amplifier_gain_hypothetical_db':gain,
                'main_development_ceiling_db':-6,'dac_fullscale_vrms':dac,
                'woofer_voltage_demand_upper_bound_vrms':voltage,'woofer_equivalent_resistor_8ohm_w':voltage**2/8,
                'tweeter_voltage_demand_upper_bound_vrms':tweet,'tweeter_equivalent_resistor_4ohm_w':tweet**2/4,
                'ideal_32v_rail_ceiling_vrms':32/math.sqrt(2),'woofer_demand_exceeds_ideal_rail':voltage>32/math.sqrt(2)})
    cap=ac.series_capacitor_response(2600,assumptions['tweeter_resistance_ohm'],assumptions['series_capacitor_uf'])
    return {'schema':1,'status':'PROGETTO NOMINALE, non rilascio costruttivo o qualifica acustica',
        'hardware_qualified':False,'manufacturing_release':False,
        'input_sha256':{name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in INPUTS},
        'assumptions':assumptions,'frequency_range_for_motion_hz':[20,500],
        'motion_excitation':'Passabanda ipotetico a 90 dB SPL RMS sinusoidali, singolo diffusore 4pi a 1 m, HP35 attivo, nessuna EQ reflex',
        'angle_deg':angles.tolist(),'sealed':sealed,'reflex':reflex,'directivity':directivity,
        'electrical_hypotheses':electrical,'cabinet_details':details,
        'capacitor_resistive_model':{'capacitance_uf':47,'resistance_ohm':3.2,
            'pole_hz':1/(2*math.pi*3.2*47e-6),'at_2600hz_db':_db(cap),'phase_deg':float(np.angle(cap,deg=True))},
        'limits':['Circuito reflex senza perdite della cassa, Le, turbolenza o compressione.',
            'Mach e Xmax sono segnali di margine nel modello, non limiti di qualifica completi.',
            'Pistoni e fase LR4 ideali: nessuna diffrazione del baffle o risposta complessa misurata.',
            'Guadagni 20/26/32 dB ipotetici; nessuna potenza continua Fosi o taratura UMC misurata.',
            'Il limite ideale di rail non include cadute, distorsione o capacita di corrente.',
            'Gioco di taglio, montaggio e rinforzo nominali da verificare sul prototipo.']}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,default=ROOT/'research-vault/completamento-20261125/risultati.json')
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    report=build_report()
    if args.check:
        if not args.out.is_file():
            print('Rapporto assente');return 1
        saved=json.loads(args.out.read_text(encoding='utf-8'))
        saved.pop('generated_at',None)
        valid=saved==report
        print('Completamento: '+('rapporto e input coerenti' if valid else 'rapporto alterato o da rigenerare'))
        return 0 if valid else 1
    if args.out.is_file():
        saved=json.loads(args.out.read_text(encoding='utf-8'))
        saved.pop('generated_at',None)
        if saved==report:
            print('Completamento: rapporto invariato, data originale conservata')
            return 0
    report['generated_at']=datetime.now().astimezone().isoformat(timespec='seconds')
    sys.path.insert(0,str(ROOT/'.claude/templates/tools'))
    from rigenera_sicuro import scrivi
    if scrivi(str(args.out),json.dumps(report,ensure_ascii=False,indent=2,allow_nan=False)+'\n',silenzioso=True):
        raise RuntimeError('Rigenerazione fermata: contenuto autorato da conservare')
    print(json.dumps({'reflex_cases':len(report['reflex']),'angular_cases':len(report['directivity']),
                      'straight_ports_fitting':sum(r['straight_geometry_fits'] for r in report['reflex'])}))
    return 0


if __name__=='__main__':
    raise SystemExit(main())
