"""Confronta profili logici PC e Pi con CamillaDSP su soli file PCM.

Richiede binario verificato, profili generati e destinazione nuova. Nessun ALSA/USB.
"""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import numpy as np

root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--bin', required=True, type=Path)
parser.add_argument('--profiles', required=True, type=Path)
parser.add_argument('--dest', required=True, type=Path)
args = parser.parse_args()
binary, source, dest = args.bin.resolve(), args.profiles.resolve(), args.dest.resolve()
dest.mkdir(exist_ok=False)
results = []
for rate in (44100,48000):
    # 2 secondi: L/R distinti a 100 Hz e 1 kHz; gli ingressi inutilizzati sono disturbati.
    n = rate*2
    time = np.arange(n)/rate
    signals = np.column_stack([0.07*np.sin(2*np.pi*100*time), 0.07*np.sin(2*np.pi*1000*time)])
    by_mode = {}
    for mode in ('mix','ascolto'):
        reference = None
        for kind, channels, pair in [('pc',2,(0,1)),('pi-digitale',18,(8,9)),('pi-analogico',18,(0,1))]:
            folder = dest/f'{kind}-{rate}-{mode}'
            folder.mkdir()
            config_name = f'{kind}-{rate}-{mode}.json'
            config = json.loads((source/config_name).read_text(encoding='utf-8'))
            devices = config.get('devices', {})
            capture, playback = devices.get('capture', {}), devices.get('playback', {})
            if (capture.get('type') != 'RawFile' or playback.get('type') != 'File'
                    or capture.get('filename') != 'input.pcm' or playback.get('filename') != 'output.pcm'
                    or capture.get('channels') != channels or playback.get('channels') != 4
                    or capture.get('format') != 'S16_LE' or playback.get('format') != 'F32_LE'
                    or devices.get('samplerate') != rate
                    or any(f.get('type') not in {'BiquadCombo','Biquad','Gain'} for f in config.get('filters',{}).values())):
                raise ValueError('Profilo non limitato ai file di prova previsti')
            frames = np.tile((0.03*np.sin(2*np.pi*333*time))[:,None],(1,channels))
            frames[:,pair] = signals
            (folder/'input.pcm').write_bytes(np.rint(frames*32767).astype('<i2').tobytes())
            (folder/'config.json').write_text(json.dumps(config,indent=2),encoding='utf-8')
            outputs = []
            for args in [('--check','config.json'),('config.json',)]:
                p = subprocess.run([str(binary),*args],cwd=folder,capture_output=True,timeout=25)
                outputs.append((p.stdout+p.stderr).decode('utf-8',errors='replace'))
                if p.returncode:
                    raise RuntimeError(outputs[-1])
            (folder/'motore.log').write_text('\n'.join(outputs),encoding='utf-8')
            audio = np.fromfile(folder/'output.pcm',dtype='<f4').reshape(-1,4)
            if len(audio) < rate*3//2 or not np.isfinite(audio).all():
                raise AssertionError('Campioni mancanti o non finiti')
            stable = audio[rate//2:rate*3//2]
            if reference is None:
                reference = stable
                difference = 0
                # RMS globale includerebbe le armoniche di quantizzazione sul ramo quasi nullo.
                phase_time = np.arange(len(stable))/rate
                by_mode[mode] = np.array([abs(np.mean(stable[:,ch]*np.exp(-2j*np.pi*f*phase_time)))
                                         for ch,f in enumerate((100,100,1000,1000))])
            else:
                difference = float(np.max(abs(stable-reference)))
                if difference > 1e-7:
                    raise AssertionError((kind,rate,mode,difference))
            results.append({'kind':kind,'rate':rate,'mode':mode,'frames':len(audio),
                            'max_difference_from_pc':difference,'max_abs':float(np.max(abs(audio)))})
        ratio = by_mode[mode]/by_mode.get('mix',by_mode[mode])
        if mode == 'ascolto':
            profile_db = 20*np.log10(ratio)
            # Una modifica comune conserva il rapporto fra le due vie di ciascun lato.
            if max(abs(profile_db[0]-profile_db[1]),abs(profile_db[2]-profile_db[3])) > 1e-2:
                raise AssertionError(profile_db)
            if not (0 < profile_db[0] < 2.1):
                raise AssertionError('Profilo ascolto non modifica il basso come atteso')
negative = dest/'sorgente-errata'
negative.mkdir()
good = dest/'pi-digitale-48000-mix'
bad_config = json.loads((good/'config.json').read_text(encoding='utf-8'))
for index, mapping in enumerate(bad_config['mixers']['stereo_quattro_vie']['mapping']):
    mapping['sources'][0]['channel'] = index//2
(negative/'input.pcm').write_bytes((good/'input.pcm').read_bytes())
(negative/'config.json').write_text(json.dumps(bad_config),encoding='utf-8')
bad_run = subprocess.run([str(binary),'config.json'],cwd=negative,capture_output=True,timeout=25)
if bad_run.returncode:
    raise RuntimeError('Il controllo negativo deve produrre audio, non fallire per errore di processo')
bad_audio = np.fromfile(negative/'output.pcm',dtype='<f4').reshape(-1,4)
expected_audio = np.fromfile(dest/'pc-48000-mix/output.pcm',dtype='<f4').reshape(-1,4)
mutation_difference = float(np.max(abs(bad_audio[24000:72000]-expected_audio[24000:72000])))
if mutation_difference < 1e-5:
    raise AssertionError('La misura non vede la selezione di sorgente errata')
report = {'passed':True,'hardware_test':False,'binary_sha256':hashlib.sha256(binary.read_bytes()).hexdigest(),
          'runner_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
          'negative_source_selection_max_difference':mutation_difference,
          'results':results,'limitations':'Solo RawFile/File su Windows; nessun ALSA/ARM/USB o trasduttore qualificato'}
(dest/'risultati.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
