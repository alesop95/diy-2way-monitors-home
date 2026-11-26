"""Somma complessa di due driver su file; nessuna acquisizione o qualifica hardware."""
import argparse
import csv
import io
import json
from pathlib import Path, PurePosixPath
import sys
import numpy as np
import caratterizzazione as source
from caratterizzazione import Curve, analyse_curve, json_bytes, sha


def sos_response(frequency, samplerate, sos):
    """H(z) con righe [b0,b1,b2,a0,a1,a2], z^-1=exp(-j*omega)."""
    f = np.asarray(frequency, dtype=float)
    if (f.ndim != 1 or not len(f) or not np.all(np.isfinite(f))
            or not np.isfinite(samplerate) or samplerate <= 0
            or np.any(f <= 0) or np.any(f >= samplerate/2)):
        raise ValueError('Frequenze positive sotto Nyquist e frequenza di campionamento valida richieste')
    if not isinstance(sos, list):
        raise ValueError('SOS deve essere una lista di sezioni')
    z = np.exp(-2j*np.pi*f/samplerate)
    response = np.ones(len(f), dtype=complex)
    for row in sos:
        coefficients = np.asarray(row, dtype=float)
        if coefficients.shape != (6,) or not np.all(np.isfinite(coefficients)) or coefficients[3] == 0:
            raise ValueError('Servono sei coefficienti finiti con a0 diverso da zero')
        with np.errstate(over='raise', invalid='raise', divide='raise'):
            b = coefficients[:3]/coefficients[3]
            a = coefficients[3:]/coefficients[3]
            if np.any(np.abs(np.roots(a)) >= 1):
                raise ValueError('Sezione non strettamente stabile')
            response *= (b[0]+b[1]*z+b[2]*z*z)/(a[0]+a[1]*z+a[2]*z*z)
    if not np.all(np.isfinite(response)):
        raise ValueError('Risposta del filtro non finita')
    return response


def _filtered(curve, samplerate, settings):
    if not isinstance(settings, dict) or set(settings) != {'sos', 'gain_db', 'polarity', 'delay_ms'}:
        raise ValueError('Filtro incompleto o con parametri sconosciuti')
    gain, polarity, delay = (float(settings[key]) for key in ('gain_db', 'polarity', 'delay_ms'))
    if not np.all(np.isfinite([gain, polarity, delay])) or polarity not in (-1, 1) or delay < 0:
        raise ValueError('Guadagno e ritardo finiti, ritardo non negativo, polarità +1/-1 richiesti')
    with np.errstate(over='raise', invalid='raise'):
        response = (curve.complex_response()*sos_response(curve.frequency_hz, samplerate, settings['sos'])
                    * np.power(10., gain/20)*polarity
                    * np.exp(-2j*np.pi*curve.frequency_hz*delay/1000))
    if not np.all(np.isfinite(response)):
        raise ValueError('Risposta filtrata non finita')
    return response


def sum_branches(woofer, tweeter, samplerate, woofer_filter, tweeter_filter):
    """Richiede lo stesso riferimento fisico, che i soli numeri non verificano."""
    if not np.array_equal(woofer.frequency_hz, tweeter.frequency_hz):
        raise ValueError('Griglie diverse: non viene interpolata la fase')
    low = _filtered(woofer, samplerate, woofer_filter)
    high = _filtered(tweeter, samplerate, tweeter_filter)
    with np.errstate(over='raise', invalid='raise'):
        total = low + high
    return {'frequency_hz': woofer.frequency_hz.copy(), 'woofer': low, 'tweeter': high, 'sum': total}


REFERENCES = {'level': 'same_excitation_voltage', 'time': 'common_time_origin',
              'observation': 'same_direction_and_distance', 'drivers': 'without_applied_crossover'}


def _analyse_manifest(manifest_path):
    path = Path(manifest_path).resolve(strict=True)
    raw = path.read_bytes()
    data = json.loads(raw.decode('utf-8-sig'))
    if not isinstance(data, dict) or data.get('schema') != 'speaker-complex-sum-1':
        raise ValueError('Schema manifesto non supportato')
    if data.get('data_kind') not in ('synthetic', 'simulated', 'measured'):
        raise ValueError('Provenienza degli input obbligatoria')
    if data.get('level_unit') not in ('dB_relative', 'dB_SPL') or data.get('references') != REFERENCES:
        raise ValueError('Unità e dichiarazioni sui riferimenti comuni obbligatorie')
    target = source._target(data.get('target'))
    plane, angle = source._direction(data.get('direction'))
    rows = data.get('branches')
    if not isinstance(rows, dict) or set(rows) != {'woofer', 'tweeter'}:
        raise ValueError('Servono soltanto i due rami woofer e tweeter')
    rate = float(data['samplerate_hz'])
    curves, quality = {}, {}
    files = {'inputs/'+path.name: raw}
    inputs = {path.name: sha(raw)}
    for name, row in rows.items():
        if not isinstance(row, dict) or set(row) != {'path', 'format', 'valid_range_hz', 'filter'}:
            raise ValueError('Ramo incompleto o con parametri sconosciuti')
        if row['valid_range_hz'] is None:
            raise ValueError('Dichiarare la banda valida di ciascun driver')
        filename = PurePosixPath(row['path']).as_posix()
        if filename == path.name:
            raise ValueError('Una curva non può sostituire il manifesto')
        if 'inputs/'+filename not in files:
            files['inputs/'+filename] = source._inside(path.parent, row['path']).read_bytes()
        blob = files['inputs/'+filename]
        curves[name] = source._parse_curve(blob, row['format'])
        files['inputs/'+filename] = blob
        inputs[filename] = sha(blob)
        quality[name] = analyse_curve(curves[name], target, row['valid_range_hz'])
    result = sum_branches(curves['woofer'], curves['tweeter'], rate,
                          rows['woofer']['filter'], rows['tweeter']['filter'])
    total = result['sum']
    floor_db, cancellation_ratio = -300., 1e-12
    with np.errstate(over='raise', invalid='raise'):
        magnitude = np.abs(total)
        reference = np.abs(result['woofer'])+np.abs(result['tweeter'])
        phase_defined = magnitude > cancellation_ratio*reference
        db = 20*np.log10(np.maximum(magnitude, 10**(floor_db/20)))
    phase = np.rad2deg(np.angle(total))
    all_phases = phase if np.all(phase_defined) else None
    curve = Curve(result['frequency_hz'], db, all_phases)
    valid = [max(quality[n]['declared_valid_band_hz'][0] for n in rows),
             min(quality[n]['declared_valid_band_hz'][1] for n in rows)]
    bad_quality = any(q['coverage_issues'] or q['status'] == 'low_coherence' for q in quality.values())
    analysis = analyse_curve(curve, target, valid if valid[0] < valid[1] else None)
    status = 'input_quality_insufficient' if bad_quality else analysis['status']
    stream = io.StringIO(newline='')
    writer = csv.writer(stream, lineterminator='\n')
    writer.writerow(['frequency_hz', 'woofer_real', 'woofer_imag', 'tweeter_real', 'tweeter_imag',
                     'sum_real', 'sum_imag', 'magnitude_db', 'phase_deg'])
    fmt = lambda value: format(float(value), '.12g')
    for i, f in enumerate(result['frequency_hz']):
        values = [f]
        for branch in ('woofer', 'tweeter', 'sum'):
            values += [result[branch][i].real, result[branch][i].imag]
        values += [db[i]]
        writer.writerow([fmt(v) for v in values]+[fmt(phase[i]) if phase_defined[i] else ''])
    files['system.csv'] = stream.getvalue().encode('utf-8')
    if not bad_quality:
        columns = [curve.frequency_hz, curve.magnitude_db]
        if all_phases is not None:
            columns.append(all_phases)
        files['system.frd'] = ''.join('\t'.join(fmt(v) for v in row)+'\n' for row in zip(*columns)).encode('utf-8')
        dataset = {'schema': 'speaker-response-dataset-1', 'data_kind': 'simulated',
                   'level_unit': data['level_unit'], 'target': target,
                   'required_directions': [{'plane': plane, 'angle_deg': angle}],
                   'curves': [{'id': 'system', 'path': 'system.frd', 'format': 'frd',
                               'plane': plane, 'angle_deg': angle, 'valid_range_hz': valid}],
                   'derivation': {'schema': 'speaker-complex-sum-1', 'references': REFERENCES,
                                  'references_status': 'declared_not_independently_verified',
                                  'input_sha256': inputs, 'magnitude_floor_db': floor_db,
                                  'phase_cancellation_ratio_threshold': cancellation_ratio}}
        files['dataset.json'] = json_bytes(dataset)
    report = {'schema': 'speaker-complex-sum-report-1', 'data_kind': 'simulated',
              'input_data_kind': data['data_kind'], 'level_unit': data['level_unit'],
              'samplerate_hz': rate, 'direction': {'plane': plane, 'angle_deg': angle},
              'references': REFERENCES, 'references_status': 'declared_not_independently_verified',
              'filters': {n: rows[n]['filter'] for n in rows}, 'target': target,
              'status': status, 'input_quality': quality, 'analysis': analysis,
              'magnitude_floor_db': floor_db, 'phase_cancellation_ratio_threshold': cancellation_ratio,
              'magnitude_floored_bins': int(np.count_nonzero(magnitude < 10**(floor_db/20))),
              'undefined_phase_bins': int(np.count_nonzero(~phase_defined)),
              'exports_for_characterization': not bad_quality, 'input_sha256': inputs,
              'code_sha256': {p.name: sha(p.read_bytes()) for p in (Path(__file__), Path(source.__file__))},
              'numpy_version': np.__version__, 'hardware_qualified': False}
    return report, files


def analyse_manifest(path):
    try:
        return _analyse_manifest(path)
    except (KeyError, TypeError, OverflowError, FloatingPointError) as exc:
        raise ValueError('Parametri mancanti, non numerici o fuori dal campo numerico: '+str(exc)) from exc


def build_bundle(path):
    report, files = analyse_manifest(path)
    files['report.json'] = json_bytes(report)
    files['manifest.json'] = json_bytes({'schema': 'speaker-complex-sum-bundle-1',
                                        'files': {name: sha(raw) for name, raw in sorted(files.items())}})
    return files


def write_bundle(path, output):
    files = build_bundle(path)
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    for name, blob in files.items():
        target = output/name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(blob)
    return json.loads(files['report.json'])


def check_bundle(path, output):
    expected = build_bundle(path)
    output = Path(output)
    actual = {p.relative_to(output).as_posix(): p for p in output.rglob('*') if p.is_file()}
    errors = ['file inatteso: '+name for name in actual.keys()-expected.keys()]
    errors += ['file assente o diverso: '+name for name, blob in expected.items()
               if name not in actual or actual[name].read_bytes() != blob]
    return sorted(errors)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', required=True, type=Path)
    parser.add_argument('--out', required=True, type=Path)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    try:
        if args.check:
            errors = check_bundle(args.manifest, args.out)
            status = None if errors else json.loads((args.out/'report.json').read_bytes())['status']
            print(json.dumps({'errors': errors, 'data_status': status, 'hardware_qualified': False}))
            return int(bool(errors))
        report = write_bundle(args.manifest, args.out)
        print(json.dumps({'data_status': report['status'], 'hardware_qualified': False}))
        return 0
    except (OSError, ValueError) as exc:
        print('Errore: '+str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
