"""Prova CamillaDSP su file PCM, senza aprire dispositivi audio.

Usa soltanto la libreria standard. Il binario si scarica dal rilascio ufficiale,
si verifica per SHA-256 e si indica con --bin. Le prove e le mutazioni restano
nella cartella indicata da --dest, creata nuova a ogni esecuzione.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import struct
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
RATE = 48000
FREQUENCIES = (100, 2000, 8000)


def rms(values):
    return math.sqrt(sum(v * v for v in values) / len(values))


def db(value):
    return 20 * math.log10(max(value, 1e-15))


def generate_input(path):
    frames = []
    windows = []
    for side in (0, 1):
        for frequency in FREQUENCIES:
            start = len(frames)
            for i in range(RATE // 4):
                sample = round(32767 * 0.1 * math.sin(2 * math.pi * frequency * i / RATE))
                frames.append((sample, 0) if side == 0 else (0, sample))
            lo, hi = start + RATE // 10, start + RATE // 5
            reference = rms([frame[side] / 32768 for frame in frames[lo:hi]])
            windows.append((side, frequency, lo, hi, reference))
            frames.extend([(0, 0)] * (RATE // 20))
    path.write_bytes(b''.join(struct.pack('<hh', *frame) for frame in frames))
    return windows


def validate_offline(config):
    devices = config['devices']
    assert devices['capture']['type'] == 'RawFile', 'Ingresso ammesso: solo RawFile'
    assert devices['playback']['type'] == 'File', 'Uscita ammessa: solo File'
    assert devices['capture']['filename'] == 'input.pcm'
    assert devices['playback']['filename'] == 'output.pcm'
    assert devices['samplerate'] == RATE
    assert devices['capture']['channels'] == 2
    assert devices['capture']['format'] == 'S16_LE'
    assert devices['playback']['channels'] == 4
    assert devices['playback']['format'] == 'F32_LE'


def run_case(binary, config, folder, windows, gain=0, mute=False):
    folder.mkdir()
    (folder / 'input.pcm').write_bytes((folder.parent / 'input.pcm').read_bytes())
    config_path = folder / 'config.json'
    config_path.write_text(json.dumps(config, indent=2), encoding='utf-8')
    validate_offline(config)
    command = [str(binary), '--check', str(config_path)]
    check = subprocess.run(command, cwd=folder, capture_output=True, text=True, timeout=15)
    assert check.returncode == 0, check.stderr + check.stdout
    command = [str(binary), f'--gain={gain}']
    if mute:
        command.append('--mute')
    command.append(str(config_path))
    result = subprocess.run(command, cwd=folder, capture_output=True, text=True, timeout=30)
    (folder / 'motore.txt').write_text(result.stdout + result.stderr, encoding='utf-8')
    assert result.returncode == 0, result.stderr + result.stdout
    raw = (folder / 'output.pcm').read_bytes()
    assert len(raw) > 0 and len(raw) % 16 == 0, 'PCM a quattro canali non valido'
    frames = list(struct.iter_unpack('<ffff', raw))
    assert len(frames) >= max(w[3] for w in windows), 'Uscita troncata'
    assert all(math.isfinite(v) for frame in frames for v in frame), 'NaN o infinito'
    if mute:
        peak = max(abs(v) for frame in frames for v in frame)
        assert peak < 1e-8, f'Mute non silenzioso: {peak}'
        return {'mute_peak': peak, 'frames': len(frames)}
    measurements = []
    for side, frequency, lo, hi, reference in windows:
        levels = [rms([frame[c] for frame in frames[lo:hi]]) / reference for c in range(4)]
        low, high = side * 2, side * 2 + 1
        other = (1 - side) * 2
        assert max(db(levels[other]), db(levels[other + 1])) < -70, 'Canali L/R errati'
        summed = rms([frame[low] + frame[high] for frame in frames[lo:hi]]) / reference
        assert abs(db(summed) - gain) < 0.12, f'Somma non unitaria: {frequency} Hz'
        if frequency == 2000:
            assert abs(db(levels[low]) - gain + 6.0206) < 0.12, 'Incrocio passa basso'
            assert abs(db(levels[high]) - gain + 6.0206) < 0.12, 'Incrocio passa alto'
        elif frequency == 100:
            assert db(levels[high]) - gain < -40, 'Bassi nella via tweeter'
        else:
            assert db(levels[low]) - gain < -40, 'Alti nella via woofer'
        measurements.append({'lato': side, 'frequenza_hz': frequency,
                             'guadagni_db': [round(db(v), 5) for v in levels],
                             'somma_db': round(db(summed), 5)})
    return {'gain_db': gain, 'frames': len(frames), 'misure': measurements}


def main():
    if not __debug__:
        raise RuntimeError('Eseguire senza -O: i controlli del collaudo devono restare attivi')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bin', required=True, type=Path)
    parser.add_argument('--config', type=Path, default=ROOT / 'config/camilladsp/offline-lr4.json')
    parser.add_argument('--dest', type=Path, default=ROOT / '_notes/collaudi-camilladsp')
    parser.add_argument('--mutazioni', action='store_true')
    args = parser.parse_args()
    config = json.loads(args.config.read_text(encoding='utf-8'))
    validate_offline(config)
    binary = args.bin.resolve(strict=True)
    args.dest.mkdir(parents=True, exist_ok=True)
    folder = Path(tempfile.mkdtemp(prefix='collaudo-', dir=args.dest)).resolve()
    windows = generate_input(folder / 'input.pcm')
    report = {'binario': str(binary), 'cartella': str(folder), 'esiti': {}}
    for name, gain, mute in [('normale', 0, False), ('volume', -6, False), ('mute', 0, True)]:
        report['esiti'][name] = run_case(binary, config, folder / name, windows, gain, mute)
    if args.mutazioni:
        for name in ('lati_scambiati', 'passaalto_errato'):
            mutated = json.loads(json.dumps(config))
            if name == 'lati_scambiati':
                for item in mutated['mixers']['stereo_quattro_vie']['mapping']:
                    item['sources'][0]['channel'] = 1 - item['sources'][0]['channel']
            else:
                mutated['filters']['alto']['parameters']['type'] = 'LinkwitzRileyLowpass'
            try:
                run_case(binary, mutated, folder / name, windows)
            except AssertionError as error:
                report['esiti'][name] = {'mutazione_rilevata': str(error)}
            else:
                raise AssertionError(f'Prova vacua: mutazione non rilevata: {name}')
    (folder / 'esito.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'Collaudo riuscito: {folder / "esito.json"}')
    print('Tre corse: normale, volume -6 dB e mute; ordine, bande e somma verificati.')
    if args.mutazioni:
        print('Entrambe le mutazioni hanno fatto fallire il controllo del segnale.')


if __name__ == '__main__':
    main()
