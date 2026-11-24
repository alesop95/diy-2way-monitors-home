"""Fattibilità del basso: ipotesi chiuse, sensibilità e collaudo DSP su file.

Non installa profili e non apre ALSA/USB. Un solo rapporto, temporanei eliminati.
"""
from pathlib import Path
import argparse
import copy
import hashlib
import itertools
import json
import math
import subprocess
import tempfile
import numpy as np
from studio_sistema_audio import closed_box, excursion_spl, profiles

ROOT = Path(__file__).resolve().parents[1]


def highpass(frequency, fc, q):
    s = 1j*np.asarray(frequency,dtype=float)/fc
    return s*s/(s*s+s/q+1)


def lr4_hp(frequency, fc):
    return 1/(1+(fc/np.asarray(frequency,dtype=float))**4)


def transform(frequency, fc, q, target_fc, target_q):
    s = 2j*math.pi*np.asarray(frequency,dtype=float)
    w, wt = 2*math.pi*fc,2*math.pi*target_fc
    return (s*s+s*w/q+w*w)/(s*s+s*wt/target_q+wt*wt)


def target_frequency(edge, target_db, protection_hz):
    desired = 10**(target_db/20)/float(lr4_hp(edge,protection_hz))
    if not 0 < desired < 1:
        raise ValueError('Target impossibile con questo passa alto e un target Butterworth passivo')
    return edge*(1/desired**2-1)**.25


def required_excursion(level_db, ceiling_db, xmax):
    return xmax*10**((level_db-ceiling_db)/20)


def model():
    drivers = json.loads((ROOT/'data/driver-candidati.json').read_text(encoding='utf-8'))
    cabinets = json.loads((ROOT/'config/cabinet/studio-st120.json').read_text(encoding='utf-8'))['variants']
    protection = drivers['design_assumptions']['highpass_hz']
    target = target_frequency(60,-2,protection)
    rows = []
    for driver,box in itertools.product(drivers['woofers'],cabinets):
        gross = math.prod(box[k]-2*box['thickness'] for k in ('width','depth','height'))/1e6
        net = gross-drivers['assumed_displacement_l']
        scale = math.sqrt(1+driver['vas_l']/net)
        fc,q = driver['fs_hz']*scale,driver['qts']*scale
        base60 = 20*math.log10(abs(highpass(60,fc,q)))
        hp60 = 20*math.log10(float(lr4_hp(60,protection)))
        f = np.geomspace(1,20000,8192)
        eq = transform(f,fc,q,target,1/math.sqrt(2))
        eq_peak = float(np.max(20*np.log10(abs(eq))))
        combined_peak = float(np.max(20*np.log10(abs(eq)*lr4_hp(f,protection))))
        scenarios = []
        for occupancy,fs_factor,q_factor,vas_factor in itertools.product((.8,1.5,2.2),(.9,1,1.1),(.9,1,1.1),(.9,1,1.1)):
            vb = gross-occupancy
            s = math.sqrt(1+driver['vas_l']*vas_factor/vb)
            response = highpass(60,driver['fs_hz']*fs_factor*s,driver['qts']*q_factor*s)
            # EQ fissa nominale, non ricalcolata per nascondere la sensibilità.
            corrected = response*transform(60,fc,q,target,1/math.sqrt(2))*lr4_hp(60,protection)
            scenarios.append(20*math.log10(abs(corrected)))
        ceiling = excursion_spl(60,driver['sd_cm2'],driver['xmax_oneway_mm'],1)
        rows.append({'driver':driver['id'],'box':box['id'],'net_l':net,'fc_hz':fc,'qtc':q,
                     'raw_60_db':base60,'hp35_60_db':hp60,'protected_60_db':base60+hp60,
                     'boost_60_for_minus2_db':-2-base60-hp60,'eq_dc_db':40*math.log10(fc/target),
                     'eq_peak_db':eq_peak,'eq_plus_hp_peak_db':combined_peak,
                     'relative_power_multiplier_60':10**((-2-base60-hp60)/10),
                     'fixed_eq_scenario_60_db_range':[min(scenarios),max(scenarios)],'scenarios':len(scenarios),
                     'ideal_fullspace_sine_rms_60hz_1m_db':ceiling,
                     'x_peak_mm_for_85db_at_60hz_1m':required_excursion(85,ceiling,driver['xmax_oneway_mm']),
                     'xmax_oneway_mm':driver['xmax_oneway_mm']})
    return {'status':'MODELLO IDEALE, non taratura o prestazione misurata','target_edge_hz':60,'target_edge_db':-2,
            'target_fc_hz':target,'target_q':1/math.sqrt(2),'protection_hz':protection,'rows':rows,
            'assumptions':['Singolo woofer in 4pi, sinusoide RMS a 1 m; nessun guadagno della stanza o somma stereo.',
                           'Scenari Fs/Qts/Vas +/-10% e occupazione 0,8/1,5/2,2 L: ipotesi di sensibilità, non tolleranze del produttore.',
                           'EQ nominale invariata nei 81 scenari per combinazione: non è robustezza provata su esemplari.',
                           'Nessuna stima di rumore, tenuta termica, potenza reale del finale o direttività.'],
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'input_sha256':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in ('data/driver-candidati.json','config/cabinet/studio-st120.json','tools/studio_sistema_audio.py')}}


def laboratory_config(row,report,rate):
    cfg = profiles(rate,2,(0,1),'mix')
    cfg['title'] = 'LABORATORIO SU FILE - LT nominale NON CALIBRATA'
    cfg['filters']['lt_nominale'] = {'type':'Biquad','parameters':{'type':'LinkwitzTransform',
        'freq_act':row['fc_hz'],'q_act':row['qtc'],'freq_target':report['target_fc_hz'],'q_target':report['target_q']}}
    cfg['pipeline'].insert(2,{'type':'Filter','channels':[0,2],'names':['lt_nominale']})
    return cfg


def verify_engine(binary,report):
    version = subprocess.run([str(binary),'--version'],capture_output=True,check=True).stdout.decode()
    if '4.1.3' not in version:
        raise ValueError('Richiesto CamillaDSP 4.1.3')
    results = []
    def run_case(cfg,rate):
        devices = cfg['devices']
        if (devices['capture']['type'] != 'RawFile' or devices['playback']['type'] != 'File'
                or devices['capture']['filename'] != 'input.pcm' or devices['playback']['filename'] != 'output.pcm'):
            raise ValueError('Il banco deve restare su file fissi')
        with tempfile.TemporaryDirectory(prefix='basso-',dir=ROOT/'build') as tmp:
            folder = Path(tmp)
            t = np.arange(rate*3)/rate
            signal = np.column_stack([.03*np.sin(2*math.pi*60*t),.03*np.sin(2*math.pi*120*t)])
            quantized = np.rint(signal*32767).astype('<i2')
            (folder/'input.pcm').write_bytes(quantized.tobytes())
            (folder/'config.json').write_text(json.dumps(cfg,allow_nan=False),encoding='utf-8')
            for command in (['--check','config.json'],['config.json']):
                subprocess.run([str(binary),*command],cwd=folder,capture_output=True,check=True,timeout=20)
            output = np.fromfile(folder/'output.pcm',dtype='<f4').reshape(-1,4)
            if not np.isfinite(output).all() or len(output) < 2*rate:
                raise AssertionError('Campioni non validi')
            f = 60
            phase = np.exp(-2j*math.pi*f*np.arange(rate)/rate)
            in_amp = abs(np.mean(quantized[rate:2*rate,0]/32768*phase))
            out_amp = abs(np.mean(output[rate:2*rate,0]*phase))
            return 20*math.log10(out_amp/in_amp),float(np.max(abs(output)))
    for row,rate in itertools.product(report['rows'],(44100,48000)):
        cfg = laboratory_config(row,report,rate)
        actual,peak = run_case(cfg,rate)
        lt60 = 20*math.log10(abs(transform(60,row['fc_hz'],row['qtc'],report['target_fc_hz'],report['target_q'])))
        cutoff = cfg['filters']['basso']['parameters']['freq']
        lp = -20*math.log10(1+(60/cutoff)**4)
        expected = cfg['filters']['margine']['parameters']['gain']+row['hp35_60_db']+lt60+lp
        error = actual-expected
        if abs(error) > .02 or peak >= 1:
            raise AssertionError((row['driver'],row['box'],rate,actual,expected,peak))
        results.append({'driver':row['driver'],'box':row['box'],'rate':rate,'measured_gain_60_db':actual,
                        'expected_gain_60_db':expected,'error_db':error,'peak':peak})
    bad = laboratory_config(report['rows'][0],report,48000)
    bad['filters']['lt_nominale']['parameters']['freq_target'] *= 1.2
    actual,_ = run_case(bad,48000)
    difference = actual-results[1]['measured_gain_60_db']
    if abs(difference) < .2:
        raise AssertionError('Il controllo non rileva il target alterato')
    return {'passed':True,'hardware_test':False,'binary_sha256':hashlib.sha256(binary.read_bytes()).hexdigest(),
            'cases':results,'negative_target_difference_db':difference,'temporary_pcm_retained':False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--binary',type=Path)
    parser.add_argument('--check',action='store_true')
    parser.add_argument('--out',type=Path,default=ROOT/'research-vault/sistema-autonomo-20261120/fattibilita-basso.json')
    args = parser.parse_args()
    report = model()
    if args.check:
        saved = json.loads(args.out.read_text(encoding='utf-8'))
        valid = (saved.get('source_sha256')==report['source_sha256']
                 and saved.get('input_sha256')==report['input_sha256']
                 and saved.get('engine',{}).get('passed') is True
                 and len(saved['engine'].get('cases',[]))==12
                 and abs(saved['engine'].get('negative_target_difference_db',0))>.2)
        print('Fattibilità basso: '+('rapporto e collaudo coerenti' if valid else 'rapporto da rigenerare'))
        raise SystemExit(0 if valid else 1)
    report['engine'] = verify_engine(args.binary.resolve(),report) if args.binary else {'passed':False,'reason':'Non eseguito'}
    args.out.write_text(json.dumps(report,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    print(json.dumps({'target_fc_hz':report['target_fc_hz'],'rows':report['rows'],
                      'engine_passed':report['engine']['passed']},ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()
