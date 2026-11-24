"""Casi fisici indipendenti per il modello preliminare dei cabinet chiusi."""
import math
from pathlib import Path
import json
import subprocess
import sys
import tempfile
import unittest
import studio_sistema_audio as model


class SealedBoxPhysics(unittest.TestCase):
    def test_butterworth_has_minus_three_db_at_natural_frequency(self):
        # Vas/Vb=1 e Qts=0.5 danno Qtc=1/sqrt(2), fc=40*sqrt(2).
        fc = 40 * math.sqrt(2)
        response = model.closed_box(fc, 40, 0.5, 10, 10)
        self.assertAlmostEqual(abs(response), 1 / math.sqrt(2), places=12)
        self.assertAlmostEqual(model.sealed_f3(fc, 1/math.sqrt(2)), fc, places=10)

    def test_large_volume_recovers_free_air_model(self):
        f = 80
        expected = (2j)**2 / ((2j)**2 + 2j/0.4 + 1)
        self.assertAlmostEqual(abs(model.closed_box(f, 40, 0.4, 10, 1e12) - expected), 0, places=10)

    def test_excursion_pressure_scales_with_area_frequency_and_distance(self):
        base = model.excursion_spl(60, 100, 4, 1)
        self.assertAlmostEqual(model.excursion_spl(60, 200, 4, 1)-base, 20*math.log10(2), places=10)
        self.assertAlmostEqual(model.excursion_spl(120, 100, 4, 1)-base, 40*math.log10(2), places=10)
        self.assertAlmostEqual(model.excursion_spl(60, 100, 4, 2)-base, -20*math.log10(2), places=10)


class OfflineBoundary(unittest.TestCase):
    def test_modified_backend_and_external_output_stop_before_engine(self):
        root = Path(__file__).resolve().parents[1]
        build = root/'build'
        build.mkdir(exist_ok=True)
        for kind in ('backend','output'):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory(dir=build) as tmp:
                target = Path(tmp).resolve()
                self.assertTrue(target.is_relative_to(build.resolve()))
                cfg = model.profiles(44100,2,(0,1),'mix')
                if kind == 'backend':
                    cfg['devices']['capture']['type'] = 'Alsa'
                else:
                    cfg['devices']['playback']['filename'] = '../fuori.pcm'
                (target/'pc-44100-mix.json').write_text(json.dumps(cfg),encoding='utf-8')
                run = subprocess.run([sys.executable,str(root/'tools/collauda-profili-autonomi.py'),
                                      '--bin',str(target/'inesistente.exe'),'--profiles',str(target),
                                      '--dest',str(target/'run')],capture_output=True,text=True)
                self.assertNotEqual(run.returncode,0)
                self.assertIn('Profilo non limitato ai file di prova previsti',run.stderr)


if __name__ == '__main__':
    unittest.main()
