"""Riproduce un modello ideale LR4; non configura CamillaDSP o diffusori reali."""
import argparse
import csv
import hashlib
import json
import math
import platform
from pathlib import Path

import numpy as np


def analog_lr4(frequency, cutoff):
    s = 1j * np.asarray(frequency, dtype=float) / cutoff
    denominator = s * s + math.sqrt(2) * s + 1
    return 1 / denominator**2, s**4 / denominator**2


def digital_biquad(cutoff, samplerate, highpass=False):
    omega = 2 * math.pi * cutoff / samplerate
    cosine = math.cos(omega)
    alpha = math.sin(omega) / math.sqrt(2)
    if highpass:
        numerator = np.array([(1 + cosine) / 2, -(1 + cosine), (1 + cosine) / 2])
    else:
        numerator = np.array([(1 - cosine) / 2, 1 - cosine, (1 - cosine) / 2])
    denominator = np.array([1 + alpha, -2 * cosine, 1 - alpha])
    return numerator / denominator[0], denominator / denominator[0]


def biquad_response(frequency, samplerate, numerator, denominator):
    z = np.exp(-2j * math.pi * np.asarray(frequency) / samplerate)
    return (numerator[0] + numerator[1] * z + numerator[2] * z**2) / (denominator[0] + denominator[1] * z + denominator[2] * z**2)


def db(value):
    return 20 * np.log10(np.maximum(np.abs(value), 1e-15))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dest', type=Path, required=True)
    parser.add_argument('--font-dir', type=Path, default=Path('build/consegna-cabinet-20261119/assets'))
    args = parser.parse_args()
    cutoff, samplerate, sound_speed = 2000.0, 48000.0, 343.0
    frequency = np.unique(np.r_[np.geomspace(20, 20000, 8193), cutoff])
    low, high = analog_lr4(frequency, cutoff)
    s = 1j * frequency / cutoff
    allpass = (s*s - math.sqrt(2)*s + 1) / (s*s + math.sqrt(2)*s + 1)
    low_at_cutoff, high_at_cutoff = analog_lr4(cutoff, cutoff)
    bn, an = digital_biquad(cutoff, samplerate)
    bh, ah = digital_biquad(cutoff, samplerate, highpass=True)
    digital_low = biquad_response(frequency, samplerate, bn, an)**2
    digital_high = biquad_response(frequency, samplerate, bh, ah)**2
    digital_at_cutoff = [biquad_response(cutoff, samplerate, b, a)**2 for b, a in ((bn, an), (bh, ah))]
    # Bilinear prewarping: compare at the mapped analog frequency, not raw f.
    mapped = cutoff * np.tan(math.pi*frequency/samplerate) / math.tan(math.pi*cutoff/samplerate)
    mapped_low, mapped_high = analog_lr4(mapped, cutoff)
    pole_radius = float(max(abs(np.roots(an))))
    path_difference = 0.02
    path_delay = path_difference / sound_speed
    phase_error = 2 * math.pi * cutoff * path_delay
    delayed_sum = low + high * np.exp(-2j*math.pi*frequency*path_delay)
    exact_delayed = low_at_cutoff + high_at_cutoff * np.exp(-1j*phase_error)
    null_distance = sound_speed / (2 * cutoff)
    # Counterexamples change the actual complex transfer functions.
    inverted_at_cutoff = low_at_cutoff - high_at_cutoff
    null_at_cutoff = low_at_cutoff + high_at_cutoff * np.exp(-2j*math.pi*cutoff*null_distance/sound_speed)
    # Common causal first-order shelving example, 3 dB at LF and 0 dB at HF.
    shelf_gain = 10**(3/20)
    shelf_s = 1j * frequency / 150.0
    common_profile = (shelf_s + shelf_gain) / (shelf_s + 1)
    base_ratio = low / high
    profile_ratio = (common_profile * low) / (common_profile * high)
    checks = {
        'analog_magnitude_error': float(np.max(np.abs(np.abs(low+high)-1))),
        'allpass_complex_error': float(np.max(np.abs(low+high-allpass))),
        'digital_magnitude_error': float(np.max(np.abs(np.abs(digital_low+digital_high)-1))),
        'bilinear_mapped_error': float(max(np.max(abs(digital_low-mapped_low)), np.max(abs(digital_high-mapped_high)))),
        'common_profile_ratio_relative_error': float(np.max(abs(profile_ratio-base_ratio)/abs(base_ratio))),
        'phase_delay_formula_error': float(abs(abs(exact_delayed)-abs(math.cos(phase_error/2)))),
    }
    if not all(value < 1e-9 for value in checks.values()):
        raise AssertionError(checks)
    if not all(abs(abs(value)-0.5) < 1e-9 for value in digital_at_cutoff):
        raise AssertionError('Digital cutoff level differs from -6.0206 dB')
    if not pole_radius < 1 or abs(inverted_at_cutoff) > 1e-12 or abs(null_at_cutoff) > 1e-12:
        raise AssertionError('Stability or actual negative counterexample not confirmed')
    k = 3 - math.sqrt(2)
    report = {
        'kind': 'deterministic_ideal_model', 'passed': True, 'hardware_benchmark': False,
        'inputs': {'fc_hz': cutoff, 'fs_hz': samplerate, 'c_m_s_assumed': sound_speed,
                   'frequency_points': len(frequency), 'range_hz': [20, 20000]},
        'environment': {'python': platform.python_version(), 'numpy': np.__version__},
        'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'checks': checks,
        'cutoff': {'each_branch_db': float(db(low_at_cutoff)), 'sum_magnitude': float(abs(low_at_cutoff+high_at_cutoff)),
                   'analog_group_delay_ms': 1000*math.sqrt(2)/(math.pi*cutoff)},
        'digital': {'lp_b': bn.tolist(), 'hp_b': bh.tolist(), 'a': an.tolist(), 'pole_radius': pole_radius},
        'path': {'difference_m': path_difference, 'delay_us': path_delay*1e6,
                 'delay_samples': path_delay*samplerate, 'phase_at_fc_deg': math.degrees(phase_error),
                 'sum_at_fc_db': float(db(exact_delayed))},
        'negative_controls': {'inverted_magnitude_at_fc': float(abs(inverted_at_cutoff)),
                              'null_distance_m': null_distance, 'null_magnitude_at_fc': float(abs(null_at_cutoff))},
        'analog_equal_component_example': {'Q': 1/math.sqrt(2), 'K_each': k, 'K_cascade': k*k,
            'cascade_gain_db_before_normalization': 20*math.log10(k*k),
            'C_farad_example': 10e-9, 'R_ohm_example': 1/(2*math.pi*cutoff*10e-9),
            'fc_min_R1percent_C5percent_hz': cutoff/(1.01*1.05),
            'fc_max_R1percent_C5percent_hz': cutoff/(0.99*0.95)},
        'latency_examples': {'one_1024_frame_interval_ms': 1024/samplerate*1000,
                            'fir_1025_tap_linear_phase_delay_ms': (1025-1)/(2*samplerate)*1000},
        'headroom_sinusoid_example': {'input_peak': 0.8, 'boost_db': 6,
                                     'output_peak_without_preamp': 0.8*10**(6/20)},
        'excursion_ratio_60_to_40_hz_equal_pressure_ideal': (60/40)**2,
        'energy_examples_not_measured': {'delta_W': [5, 15], 'hours_per_year': 8*365,
                                       'delta_kWh_per_year': [5*8*365/1000, 15*8*365/1000]},
        'limits': ['No real driver, enclosure, room, ADC/DAC, CPU load or power measurement.',
                   'fc is illustrative and is not the crossover design for the monitors.',
                   'An ideal common profile preserves the branch ratio only under the stated linear assumptions.']
    }
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib import font_manager
    for filename in ('Altro-Grotesk-Book.ttf', 'Altro-Serif-Light.ttf'):
        path = args.font_dir / filename
        if not path.is_file(): raise FileNotFoundError(path)
        font_manager.fontManager.addfont(str(path))
    body = font_manager.FontProperties(fname=str(args.font_dir/'Altro-Grotesk-Book.ttf')).get_name()
    plt.rcParams.update({'font.family': body, 'font.size': 11, 'text.color': '#0A0A0A',
        'axes.labelcolor': '#0A0A0A', 'axes.edgecolor': '#D0D4E3', 'grid.color': '#D0D4E3',
        'figure.facecolor': 'white', 'axes.facecolor': 'white', 'svg.fonttype': 'path',
        'legend.fancybox': False, 'legend.framealpha': 1, 'legend.edgecolor': '#D0D4E3'})
    title_font = font_manager.FontProperties(fname=str(args.font_dir/'Altro-Serif-Light.ttf'), size=18)
    args.dest.mkdir(parents=True, exist_ok=False)
    fig, axes = plt.subplots(2, 1, figsize=(9, 7), sharex=True, layout='constrained')
    axes[0].semilogx(frequency, db(low), color='#4D11A7', label='Passa-basso LR4')
    axes[0].semilogx(frequency, db(high), color='#4D11A7', linestyle='--', label='Passa-alto LR4')
    axes[0].semilogx(frequency, db(low+high), color='#0A0A0A', linewidth=2, label='Somma coerente ideale')
    axes[0].set_ylim(-70, 5)
    axes[0].set_ylabel('Modulo [dB]')
    axes[0].set_title('LR4 ideale a 2 kHz: modulo piatto, fase variabile')
    axes[0].title.set_fontproperties(title_font)
    axes[0].legend(loc='lower left')
    axes[1].semilogx(frequency, np.unwrap(np.angle(low+high))*180/math.pi, color='#4D11A7')
    axes[1].set_ylabel('Fase della somma [gradi]')
    axes[1].set_xlabel('Frequenza [Hz]')
    for axis in axes: axis.grid(True, which='both', alpha=.7)
    for suffix in ('svg', 'png', 'pdf'): fig.savefig(args.dest/('lr4-modulo-fase.'+suffix), dpi=160)
    plt.close(fig)
    fig, axis = plt.subplots(figsize=(9, 4.8), layout='constrained')
    axis.semilogx(frequency, db(low+high), color='#0A0A0A', label='Sorgenti coerenti e coincidenti')
    axis.semilogx(frequency, db(delayed_sum), color='#4D11A7', label='Cammino aggiuntivo di 20 mm')
    null_sum = low+high*np.exp(-2j*math.pi*frequency*null_distance/sound_speed)
    axis.semilogx(frequency, np.maximum(db(null_sum), -70), color='#4D11A7', linestyle='--', label='Cammino aggiuntivo di 85,75 mm')
    axis.set(title='Controesempi del modello: il filtro elettrico non basta', xlabel='Frequenza [Hz]', ylabel='Modulo della somma [dB]', ylim=(-70, 5))
    axis.title.set_fontproperties(title_font)
    axis.grid(True, which='both', alpha=.7)
    axis.legend(loc='lower left')
    for suffix in ('svg', 'png', 'pdf'): fig.savefig(args.dest/('cammino-e-somma.'+suffix), dpi=160)
    plt.close(fig)
    with (args.dest/'frequenze.csv').open('x', newline='', encoding='utf-8') as handle:
        writer = csv.writer(handle)
        writer.writerow(['frequency_hz', 'analog_lp_db', 'analog_hp_db', 'sum_db', 'sum_phase_deg', 'sum_20mm_db', 'digital_sum_db'])
        writer.writerows(zip(frequency, db(low), db(high), db(low+high), np.unwrap(np.angle(low+high))*180/math.pi, db(delayed_sum), db(digital_low+digital_high)))
    report['environment']['matplotlib'] = matplotlib.__version__
    (args.dest/'risultati.json').write_text(json.dumps(report, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    manifest = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(args.dest.iterdir()) if p.is_file()}
    (args.dest/'MANIFEST-SHA256.json').write_text(json.dumps(manifest, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
