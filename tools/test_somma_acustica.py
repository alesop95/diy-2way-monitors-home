"""Casi analitici indipendenti per filtri e somma: nessun diffusore misurato."""
import unittest
import copy
import csv
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from unittest.mock import patch
import numpy as np

from caratterizzazione import Curve, analyse_dataset, read_curve
import somma_acustica as sa
from somma_acustica import sos_response, sum_branches


class ComplexSumTests(unittest.TestCase):
    def setUp(self):
        self.f = np.array([100., 2000., 10000.])
        self.unit = Curve(self.f, [0., 0., 0.], [0., 0., 0.])
        self.identity = {'sos': [], 'gain_db': 0., 'polarity': 1, 'delay_ms': 0.}

    def test_sos_normalizes_a0_and_preserves_complex_delay(self):
        # H(z)=z^-1; coefficients deliberately not normalized.
        response = sos_response(self.f, 48000, [[0, 2, 0, 2, 0, 0]])
        np.testing.assert_allclose(response, np.exp(-2j*np.pi*self.f/48000), atol=1e-14)

    def test_sos_cascade_matches_geometric_series(self):
        expected = (1/(1-.5*np.exp(-2j*np.pi*self.f/48000)))**2
        actual = sos_response(self.f, 48000, [[1, 0, 0, 1, -.5, 0]]*2)
        np.testing.assert_allclose(actual, expected, atol=1e-14)

    def test_opposite_driver_phases_cancel_instead_of_adding_magnitudes(self):
        opposite = Curve(self.f, [0., 0., 0.], [180., 180., 180.])
        result = sum_branches(self.unit, opposite, 48000, self.identity, self.identity)
        np.testing.assert_allclose(result['sum'], 0, atol=1e-14)

    def test_gain_and_polarity_keep_absolute_reference(self):
        settings = dict(self.identity, gain_db=20*np.log10(.5), polarity=-1)
        result = sum_branches(self.unit, self.unit, 48000, self.identity, settings)
        np.testing.assert_allclose(result['sum'], .5, atol=1e-14)

    def test_positive_delay_is_later_not_earlier(self):
        settings = dict(self.identity, delay_ms=1.)
        result = sum_branches(self.unit, self.unit, 48000, self.identity, settings)
        np.testing.assert_allclose(result['tweeter'], np.exp(-2j*np.pi*self.f*.001), atol=1e-14)

    def test_missing_phase_or_different_grid_is_rejected(self):
        other = [Curve(self.f, [0, 0, 0]), Curve(self.f+1, [0, 0, 0], [0, 0, 0])]
        for curve in other:
            with self.subTest(curve=curve), self.assertRaises(ValueError):
                sum_branches(self.unit, curve, 48000, self.identity, self.identity)

    def test_invalid_sos_and_nyquist_are_rejected(self):
        for sos in ([[1, 0, 0, 0, 0, 0]], [[1, 0, 0, 1, -1, 0]],
                    [[1, 0, 0, 1, -1.1, 0]], [[1, 0, float('nan'), 1, 0, 0]], [[1, 2]]):
            with self.subTest(sos=sos), self.assertRaises(ValueError):
                sos_response(self.f, 48000, sos)
        for frequencies, rate in (([100, 24000], 48000), ([100, 30000], 48000),
                                  ([100, 200], 0), ([0, 100], 48000)):
            with self.subTest(frequencies=frequencies, rate=rate), self.assertRaises(ValueError):
                sos_response(frequencies, rate, [])

    def test_invalid_branch_parameters_are_rejected(self):
        for settings in (dict(self.identity, polarity=0), dict(self.identity, delay_ms=-1),
                         dict(self.identity, gain_db=float('nan')), {}, None):
            with self.subTest(settings=settings), self.assertRaises(ValueError):
                sum_branches(self.unit, self.unit, 48000, self.identity, settings)


class BundleTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.f = np.unique(np.r_[np.geomspace(50, 20000, 241), 2000.])
        raw = ''.join(f'{f:.12g}\t0\t0\n' for f in self.f)
        for name in ('woofer.frd', 'tweeter.frd'):
            (self.root/name).write_text(raw, encoding='utf-8')
        self.config = {
            'schema': 'speaker-complex-sum-1', 'data_kind': 'synthetic', 'level_unit': 'dB_relative',
            'samplerate_hz': 48000,
            'references': {'level': 'same_excitation_voltage', 'time': 'common_time_origin',
                           'observation': 'same_direction_and_distance', 'drivers': 'without_applied_crossover'},
            'direction': {'plane': 'axial', 'angle_deg': 0},
            'target': {'minimum_hz': 100, 'maximum_hz': 10000, 'reference_db': 0,
                       'tolerance_db': .5, 'max_gap_octaves': .125, 'minimum_coherence': .9},
            'branches': {name: {'path': name+'.frd', 'format': 'frd', 'valid_range_hz': [50, 20000],
                              'filter': {'sos': [], 'gain_db': 20*np.log10(.5),
                                         'polarity': 1, 'delay_ms': 0}}
                         for name in ('woofer', 'tweeter')},
        }
        self.manifest = self.root/'manifest.json'

    def save(self, config=None):
        self.manifest.write_text(json.dumps(self.config if config is None else config), encoding='utf-8')
        return self.manifest

    def test_common_reference_and_raw_snapshot_are_preserved(self):
        self.config['branches']['woofer']['path'] = './woofer.frd'
        self.save()
        report, files = sa.analyse_manifest(self.manifest)
        self.assertEqual(report['status'], 'within_bounds')
        self.assertFalse(report['hardware_qualified'])
        self.assertEqual(files['inputs/woofer.frd'], (self.root/'woofer.frd').read_bytes())
        self.assertEqual(files['inputs/manifest.json'], self.manifest.read_bytes())
        self.assertEqual(report['references_status'], 'declared_not_independently_verified')
        self.assertEqual(set(report['code_sha256']), {'somma_acustica.py', 'caratterizzazione.py'})

    def test_reused_input_path_is_read_once_even_if_source_changes(self):
        self.config['branches']['tweeter']['path'] = './woofer.frd'
        self.save()
        path = self.root/'woofer.frd'
        initial = path.read_bytes()
        read_bytes = Path.read_bytes
        reads = []

        def read_then_change(current):
            raw = read_bytes(current)
            if current == path:
                reads.append(current)
                current.write_bytes(initial.replace(b'\t0\t0', b'\t-6\t0'))
            return raw

        with patch.object(Path, 'read_bytes', read_then_change):
            report, files = sa.analyse_manifest(self.manifest)
        self.assertEqual(len(reads), 1)
        self.assertEqual(files['inputs/woofer.frd'], initial)
        self.assertEqual(report['status'], 'within_bounds')

    def test_null_has_blank_phase_and_two_column_frd(self):
        self.config['branches']['tweeter']['filter']['polarity'] = -1
        report, files = sa.analyse_manifest(self.save())
        self.assertEqual(report['undefined_phase_bins'], len(self.f))
        self.assertEqual(report['magnitude_floor_db'], -300.)
        rows = list(csv.DictReader(io.StringIO(files['system.csv'].decode())))
        self.assertTrue(all(row['phase_deg'] == '' for row in rows))
        self.assertTrue(all(len(line.split()) == 2 for line in files['system.frd'].decode().splitlines()))
        self.assertEqual(report['status'], 'outside_bounds')

    def test_output_is_compatible_with_characterization_and_keeps_simulated_kind(self):
        self.config['data_kind'] = 'measured'
        out = self.root/'result'
        report = sa.write_bundle(self.save(), out)
        downstream, _ = analyse_dataset(out/'dataset.json')
        self.assertEqual(downstream['status'], 'within_bounds')
        self.assertEqual(downstream['data_kind'], 'simulated')
        self.assertEqual(report['input_data_kind'], 'measured')
        self.assertFalse(downstream['hardware_qualified'])
        self.assertIsNotNone(read_curve(out/'system.frd').phase_deg)

    def test_low_input_coherence_is_not_invented_for_the_sum(self):
        self.config['branches']['woofer']['format'] = 'osm_frd'
        (self.root/'woofer.frd').write_text(''.join(f'{f:.12g}\t0\t0\t0.2\n' for f in self.f), encoding='utf-8')
        report, files = sa.analyse_manifest(self.save())
        self.assertEqual(report['status'], 'input_quality_insufficient')
        self.assertEqual(report['input_quality']['woofer']['minimum_coherence'], .2)
        self.assertIsNone(report['analysis']['minimum_coherence'])
        self.assertNotIn('dataset.json', files)
        self.assertNotIn('system.frd', files)
        self.assertIn('system.csv', files)

    def test_declared_band_and_grid_of_inputs_cannot_be_hidden_by_filters(self):
        self.config['branches']['woofer']['valid_range_hz'] = [500, 20000]
        self.config['branches']['woofer']['filter']['gain_db'] = -100
        report, _ = sa.analyse_manifest(self.save())
        self.assertEqual(report['status'], 'input_quality_insufficient')
        self.assertIn('declared_valid_band', report['input_quality']['woofer']['coverage_issues'])

    def test_invalid_shapes_references_and_paths_are_rejected(self):
        bad = [[], None, dict(self.config, references={}), dict(self.config, branches=[])]
        for config in bad:
            self.manifest.write_text(json.dumps(config), encoding='utf-8')
            with self.subTest(config=config), self.assertRaises(ValueError):
                sa.analyse_manifest(self.manifest)
        for mutation in ('missing_phase', 'traversal', 'filter_typo'):
            config = copy.deepcopy(self.config)
            if mutation == 'traversal':
                config['branches']['woofer']['path'] = '../outside.frd'
            elif mutation == 'filter_typo':
                config['branches']['woofer']['filter']['dalay_ms'] = 0
            else:
                (self.root/'woofer.frd').write_text('100 0\n1000 0\n', encoding='utf-8')
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                sa.analyse_manifest(self.save(config))

    def test_bundle_detects_report_input_and_extra_file_changes(self):
        self.save()
        out = self.root/'result'
        sa.write_bundle(self.manifest, out)
        self.assertEqual(sa.check_bundle(self.manifest, out), [])
        for name in ('report.json', 'inputs/woofer.frd', 'unexpected.txt'):
            path = out/name
            before = path.read_bytes() if path.exists() else None
            path.write_bytes(b'altered')
            self.assertTrue(sa.check_bundle(self.manifest, out), name)
            if before is None:
                path.unlink()
            else:
                path.write_bytes(before)
        (self.root/'woofer.frd').write_text((self.root/'woofer.frd').read_text().replace('\t0\t0', '\t-1\t0'), encoding='utf-8')
        self.assertTrue(sa.check_bundle(self.manifest, out))

    def test_existing_output_and_invalid_input_do_not_destroy_human_work(self):
        self.save()
        out = self.root/'human'
        out.mkdir()
        (out/'notes.txt').write_text('keep', encoding='utf-8')
        with self.assertRaises(FileExistsError):
            sa.write_bundle(self.manifest, out)
        self.assertEqual((out/'notes.txt').read_text(), 'keep')
        self.manifest.write_text('[]', encoding='utf-8')
        with self.assertRaises(ValueError):
            sa.write_bundle(self.manifest, self.root/'must-not-exist')
        self.assertFalse((self.root/'must-not-exist').exists())

    def test_one_null_does_not_invent_phase_and_keeps_other_csv_phases(self):
        self.config['branches']['woofer']['filter']['gain_db'] = 0
        self.config['branches']['tweeter']['filter'].update(gain_db=0, delay_ms=.25)
        report, files = sa.analyse_manifest(self.save())
        rows = list(csv.DictReader(io.StringIO(files['system.csv'].decode())))
        at_cutoff = next(row for row in rows if float(row['frequency_hz']) == 2000)
        self.assertEqual(at_cutoff['phase_deg'], '')
        self.assertTrue(any(row['phase_deg'] for row in rows))
        self.assertGreaterEqual(report['undefined_phase_bins'], 1)
        self.assertTrue(all(len(line.split()) == 2 for line in files['system.frd'].decode().splitlines()))

    def test_invalid_cli_input_creates_no_output(self):
        self.manifest.write_text('[]', encoding='utf-8')
        out = self.root/'absent'
        run = subprocess.run([sys.executable, str(Path(sa.__file__)), '--manifest', str(self.manifest),
                              '--out', str(out)], capture_output=True, text=True, timeout=10)
        self.assertEqual(run.returncode, 2)
        self.assertFalse(out.exists())

    def test_cli_reports_integrity_separately_from_outside_bounds(self):
        self.config['branches']['tweeter']['filter']['polarity'] = -1
        self.save()
        command = [sys.executable, str(Path(sa.__file__)), '--manifest', str(self.manifest),
                   '--out', str(self.root/'cli')]
        run = subprocess.run(command, capture_output=True, text=True, timeout=10)
        self.assertEqual(run.returncode, 0, run.stderr)
        check = subprocess.run(command+['--check'], capture_output=True, text=True, timeout=10)
        self.assertEqual(check.returncode, 0, check.stderr)
        self.assertEqual(json.loads(check.stdout)['data_status'], 'outside_bounds')
        self.assertFalse(json.loads(check.stdout)['hardware_qualified'])


class VersionedDemoTests(unittest.TestCase):
    folder = Path(__file__).resolve().parents[1]/'data/somma-acustica-demo'

    def test_lr4_matches_bilinear_analog_model_and_cutoff_counterexamples(self):
        for filename, expected in (('manifest.json', 1.), ('invertito.json', 0.),
                                    ('ritardo-6-campioni.json', np.sqrt(.5))):
            config = json.loads((self.folder/filename).read_bytes())
            result = sum_branches(read_curve(self.folder/'woofer.frd'), read_curve(self.folder/'tweeter.frd'),
                                   48000, config['branches']['woofer']['filter'], config['branches']['tweeter']['filter'])
            index = int(np.flatnonzero(result['frequency_hz'] == 2000)[0])
            with self.subTest(filename=filename):
                self.assertAlmostEqual(abs(result['sum'][index]), expected, places=10)
            if filename == 'manifest.json':
                mapped = np.tan(np.pi*result['frequency_hz']/48000)/np.tan(np.pi*2000/48000)
                s = 1j*mapped
                denominator = (s*s+np.sqrt(2)*s+1)**2
                np.testing.assert_allclose(result['woofer'], 1/denominator, atol=1e-11)
                np.testing.assert_allclose(result['tweeter'], s**4/denominator, atol=1e-11)
                np.testing.assert_allclose(abs(result['sum']), 1, atol=1e-11)

    def test_versioned_reports_match_current_code_and_original_inputs(self):
        root = Path(__file__).resolve().parents[1]
        saved = json.loads((root/'research-vault/somma-acustica-20261126/risultati.json').read_bytes())
        for case, filename in (('allineato', 'manifest.json'), ('invertito', 'invertito.json'),
                                ('ritardo-6-campioni', 'ritardo-6-campioni.json')):
            with self.subTest(case=case):
                self.assertEqual(sa.analyse_manifest(self.folder/filename)[0], saved['cases'][case])


if __name__ == '__main__':
    unittest.main()
