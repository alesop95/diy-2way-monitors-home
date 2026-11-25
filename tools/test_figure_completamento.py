"""Un clone possiede già gli SVG versionati: deve poter ricostruire i PDF."""
import hashlib
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]


class ExistingPublishedFigures(unittest.TestCase):
    def test_rebuild_accepts_unchanged_published_svg(self):
        (ROOT/'build').mkdir(exist_ok=True)
        public=ROOT/'docs/figure/completamento-20261125'
        before={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in public.glob('*.svg')}
        self.assertEqual(len(before),4)
        with tempfile.TemporaryDirectory(dir=ROOT/'build') as temporary:
            output=Path(temporary)/'figures'
            run=subprocess.run([sys.executable,str(ROOT/'tools/figure_completamento.py'),'--out',str(output)],
                               capture_output=True,text=True,timeout=90)
            self.assertEqual(run.returncode,0,run.stderr)
            self.assertEqual(len(list(output.glob('*.pdf'))),4)
        after={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in public.glob('*.svg')}
        self.assertEqual(after,before)


if __name__=='__main__':unittest.main()
