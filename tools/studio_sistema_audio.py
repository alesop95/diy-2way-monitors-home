"""Modello preliminare dei driver in cassa chiusa e profili solo su file.

Non misura altoparlanti, non apre periferiche e non modifica CamillaDSP installato.
"""
from pathlib import Path
import argparse
import hashlib
import json
import math
import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def closed_box(frequency, fs, qts, vas, vb):
    scale = math.sqrt(1 + vas/vb)
    z = 1j * np.asarray(frequency) / (fs*scale)
    return z*z / (z*z + z/(qts*scale) + 1)


def sealed_f3(fc, qtc):
    coefficient = 2 - 1/qtc**2
    return fc * math.sqrt((-coefficient + math.sqrt(coefficient**2 + 4))/2)


def excursion_spl(frequency, sd_cm2, xmax_mm, distance):
    # RMS pressure of a sinusoidal monopole in 4pi; Xmax is one-way PEAK.
    pressure = 1.204 * (2*math.pi*frequency)**2 * sd_cm2*1e-4 * xmax_mm*1e-3 / (4*math.pi*distance*math.sqrt(2))
    return 20*math.log10(pressure/20e-6)


def profiles(rate, channels, source_pair, mode):
    settings = json.loads((ROOT/'data/driver-candidati.json').read_text(encoding='utf-8'))['design_assumptions']
    cfg = json.loads((ROOT/'config/camilladsp/offline-lr4.json').read_text(encoding='utf-8'))
    cfg['title'] = f"LABORATORIO SU FILE - progetto {settings['crossover_electrical_hz']} Hz NON CALIBRATO"
    cfg['description'] = 'Profilo elettrico dimostrativo: parametri dal file driver-candidati, nessuna taratura acustica.'
    cfg['devices']['samplerate'] = rate
    cfg['devices']['capture']['channels'] = channels
    cfg['filters']['basso']['parameters']['freq'] = settings['crossover_electrical_hz']
    cfg['filters']['alto']['parameters']['freq'] = settings['crossover_electrical_hz']
    mix = cfg['mixers']['stereo_quattro_vie']
    mix['channels']['in'] = channels
    for dest, source in zip(mix['mapping'], [source_pair[0], source_pair[0], source_pair[1], source_pair[1]]):
        dest['sources'][0]['channel'] = source
    cfg['filters'].update({
        'margine': {'type': 'Gain', 'parameters': {'gain': settings['pre_gain_db'], 'inverted': False}},
        'subsonico': {'type': 'BiquadCombo', 'parameters': {'type': 'LinkwitzRileyHighpass', 'freq': settings['highpass_hz'], 'order': 4}},
        'trim_tweeter': {'type': 'Gain', 'parameters': {'gain': settings['tweeter_trim_db'], 'inverted': False}},
    })
    # CamillaDSP 4.1.3 applica Main implicitamente; Volume serve ai fader Aux.
    cfg['pipeline'].insert(1, {'type': 'Filter', 'channels': [0,1,2,3], 'names': ['margine', 'subsonico']})
    cfg['pipeline'].append({'type': 'Filter', 'channels': [1,3], 'names': ['trim_tweeter']})
    if mode == 'ascolto':
        cfg['filters']['preferenza'] = {'type': 'Biquad', 'parameters': {'type': 'Lowshelf', 'freq': settings['profile_listening_low_shelf_hz'], 'slope': 1, 'gain': settings['profile_listening_low_shelf_db']}}
        cfg['pipeline'].insert(2, {'type': 'Filter', 'channels': [0,1,2,3], 'names': ['preferenza']})
    return cfg


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--dest', required=True, type=Path)
    a = p.parse_args()
    a.dest.mkdir(parents=True, exist_ok=False)
    data = json.loads((ROOT/'data/driver-candidati.json').read_text(encoding='utf-8'))
    cabinets = json.loads((ROOT/'config/cabinet/studio-st120.json').read_text(encoding='utf-8'))
    frequency = np.geomspace(20, 500, 1000)
    rows = []
    curves = []
    for driver in data['woofers']:
        for box in cabinets['variants']:
            gross = math.prod(box[k]-2*box['thickness'] for k in ['width', 'depth', 'height'])/1e6
            net = gross-data['assumed_displacement_l']
            scale = math.sqrt(1+driver['vas_l']/net)
            fc, qtc = driver['fs_hz']*scale, driver['qts']*scale
            h = closed_box(frequency, driver['fs_hz'], driver['qts'], driver['vas_l'], net)
            at60 = 20*math.log10(abs(closed_box(60, driver['fs_hz'], driver['qts'], driver['vas_l'], net)))
            rows.append({'driver': driver['id'], 'box': box['id'], 'gross_l': gross, 'net_assumed_l': net,
                         'fc_hz': fc, 'qtc': qtc, 'f3_hz': sealed_f3(fc,qtc), 'relative_db_at_60hz': at60,
                         'excursion_ceiling_60hz_1m_fullspace_sine_rms_db': excursion_spl(60,driver['sd_cm2'],driver['xmax_oneway_mm'],1)})
            curves.append((driver['id']+' / '+box['id'], 20*np.log10(abs(h))))
    generated = []
    for rate in (44100, 48000):
        for mode in ('mix', 'ascolto'):
            for capture, channels, pair in [('pc',2,(0,1)),('pi-digitale',18,(8,9)),('pi-analogico',18,(0,1))]:
                name = f'{capture}-{rate}-{mode}.json'
                (a.dest/name).write_text(json.dumps(profiles(rate,channels,pair,mode),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
                generated.append(name)
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib import font_manager
    fontdir = ROOT/'build/consegna-cabinet-20261119/assets'
    for font in fontdir.glob('*.ttf'):
        font_manager.fontManager.addfont(str(font))
    plt.rcParams.update({'font.family':'Altro Grotesk Book','axes.edgecolor':'#D0D4E3','grid.color':'#D0D4E3','legend.fancybox':False})
    fig, ax = plt.subplots(figsize=(9,5),layout='constrained')
    for n, (name, values) in enumerate(curves):
        ax.semilogx(frequency,values,label=name,color=['#4D11A7','#0A0A0A'][n//3],ls=['-','--',':'][n%3])
    ax.set(xlabel='Frequenza [Hz]',ylabel='Risposta normalizzata [dB]',ylim=(-25,3),xlim=(20,500))
    ax.set_title('Cassa chiusa: modello, volumi netti ipotizzati',fontfamily='Altro Serif Light')
    ax.grid(True,which='both'); ax.legend(fontsize=9)
    for suffix in ('pdf','png','svg'):
        fig.savefig(a.dest/f'confronto-driver.{suffix}',dpi=150)
    np.savetxt(a.dest/'curve-driver.csv',np.column_stack([frequency]+[v for _,v in curves]),delimiter=',',header='frequency_hz,'+','.join(name for name,_ in curves),comments='')
    result = {'status':'MODELLO IDEALE, non misure o cabinet esecutivi','source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'assumptions':data,'results':rows,'offline_configs':generated}
    (a.dest/'studio.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(rows,indent=2))


if __name__ == '__main__':
    main()
