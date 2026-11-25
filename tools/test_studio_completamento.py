"""Contratti del rapporto nominale, livelli fisici e integrità della consegna."""
import importlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import numpy as np


class CompletionReport(unittest.TestCase):
    def setUp(self):
        (Path(__file__).resolve().parents[1]/'build').mkdir(exist_ok=True)
        self.assertIsNotNone(importlib.util.find_spec('studio_completamento'), 'Manca il rapporto di completamento')
        self.s=importlib.import_module('studio_completamento')

    def test_excursion_has_inverse_square_frequency_and_pressure_scaling(self):
        r=self.s.radiation_requirements(np.array([60.,120.]),np.ones(2),np.zeros(2),100,1e-3,90)
        self.assertAlmostEqual(r['excursion_peak_mm'][0]/r['excursion_peak_mm'][1],4.,places=12)
        louder=self.s.radiation_requirements(np.array([60.,120.]),np.ones(2),np.zeros(2),100,1e-3,110)
        np.testing.assert_allclose(louder['excursion_peak_mm'],r['excursion_peak_mm']*10,rtol=1e-12)
        np.testing.assert_allclose(r['port_velocity_peak_m_s'],[0.,0.])

    def test_cone_zero_can_still_have_port_velocity(self):
        r=self.s.radiation_requirements(40.,0j,1+0j,124,1e-3,90)
        self.assertAlmostEqual(float(r['excursion_peak_mm']),0.)
        self.assertGreater(float(r['port_velocity_peak_m_s']),30.)

    def test_report_keeps_non_fitting_ports_and_does_not_qualify_hardware(self):
        r=self.s.build_report()
        bad=[p for p in r['reflex'] if not p['straight_geometry_fits']]
        good=[p for p in r['reflex'] if p['straight_geometry_fits']]
        self.assertTrue(bad);self.assertTrue(good)
        self.assertFalse(r['hardware_qualified'])
        self.assertTrue(any(p['port_mach_peak_max']>.05 for p in good))
        self.assertTrue(all(p['within_xmax'] == (p['excursion_peak_max_mm']<=p['xmax_oneway_mm']) for p in r['reflex']))

    def test_capacitor_effect_is_included_in_the_summed_crossover(self):
        r=self.s.build_report()
        rows=[p for p in r['directivity'] if p['depth_offset_mm']==0 and p['crossover_hz']==2600]
        self.assertTrue(rows)
        self.assertTrue(all(p['on_axis_with_capacitor_db']<-.1 for p in rows))
        self.assertTrue(all(abs(p['on_axis_without_capacitor_db'])<1e-10 for p in rows))

    def test_cli_check_rejects_altered_results_not_only_altered_hashes(self):
        root=Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory(dir=root/'build') as temporary:
            path=Path(temporary)/'rapporto.json'
            run=subprocess.run([sys.executable,str(root/'tools/studio_completamento.py'),'--out',str(path)],capture_output=True,text=True)
            self.assertEqual(run.returncode,0,run.stderr)
            data=json.loads(path.read_text(encoding='utf-8'))
            data['reflex'][0]['net_volume_l']+=1
            path.write_text(json.dumps(data),encoding='utf-8')
            check=subprocess.run([sys.executable,str(root/'tools/studio_completamento.py'),'--out',str(path),'--check'],capture_output=True,text=True)
            self.assertNotEqual(check.returncode,0)

    def test_same_inputs_keep_the_original_generation_record(self):
        root=Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory(dir=root/'build') as temporary:
            path=Path(temporary)/'rapporto.json'
            data=self.s.build_report();data['generated_at']='2001-01-01T00:00:00+00:00'
            original=(json.dumps(data,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
            path.write_bytes(original)
            run=subprocess.run([sys.executable,str(root/'tools/studio_completamento.py'),'--out',str(path)],capture_output=True,text=True)
            self.assertEqual(run.returncode,0,run.stderr)
            self.assertEqual(path.read_bytes(),original)


if __name__=='__main__':
    unittest.main()
