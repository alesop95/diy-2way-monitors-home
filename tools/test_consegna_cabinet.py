"""Integrazione CADCraft reale: frontali riletti e mutazione dimensionale respinta."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]


class CabinetDrawingDelivery(unittest.TestCase):
    def test_real_cadcraft_roundtrip_and_wrong_cut_radius(self):
        (ROOT/'build').mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=ROOT/'build') as temporary:
            base=Path(temporary)
            for negative in (False,True):
                out=base/('negative' if negative else 'normal')
                command=[sys.executable,str(ROOT/'tools/cabinet-dettagli-cadcraft.py'),'--out',str(out),'--solo-verifica']
                if negative: command.append('--errore-raggio-per-prova')
                run=subprocess.run(command,capture_output=True,text=True,timeout=120)
                if negative:
                    self.assertNotEqual(run.returncode,0)
                    self.assertIn('raggio',run.stderr.lower())
                else:
                    self.assertEqual(run.returncode,0,run.stderr)
                    report=json.loads((out/'esito.json').read_text(encoding='utf-8'))
                    self.assertEqual(report['status'],'success')
                    self.assertTrue(all(v['shapes_verified']==12 for v in report['variants']))
                    self.assertTrue(all(v['units_mm'] for v in report['variants']))


if __name__=='__main__':
    unittest.main()
