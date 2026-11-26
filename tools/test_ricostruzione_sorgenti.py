"""Esegue generatori e contratti da sorgenti copiati, senza il build della postazione."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from font_intrawelt import resolve_fonts

ROOT=Path(__file__).resolve().parents[1]


class CleanSourceReconstruction(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        (ROOT/'build').mkdir(exist_ok=True)
        temporary=tempfile.TemporaryDirectory(dir=ROOT/'build')
        cls.addClassCleanup(temporary.cleanup)
        cls.clean=Path(temporary.name)/'sources';cls.clean.mkdir()
        for relative in ('tools','data','config/cabinet','research-vault/completamento-20261125',
                         'research-vault/sistema-autonomo-20261120','docs/figure/completamento-20261125',
                         'docs/figure/sistema-autonomo'):
            shutil.copytree(ROOT/relative,cls.clean/relative,ignore=shutil.ignore_patterns('__pycache__'))
        relative='.claude/templates/tools/rigenera_sicuro.py'
        destination=cls.clean/relative;destination.parent.mkdir(parents=True)
        shutil.copyfile(ROOT/relative,destination)
        cls.environment=dict(os.environ,INTRAWELT_FONT_DIR=str(resolve_fonts()),PYTHONPATH='')
        cls.environment.pop('CODEX_HOME',None);cls.environment.pop('CLAUDE_CONFIG_DIR',None)

    def run_command(self,*arguments,environment=None):
        return subprocess.run([sys.executable,*arguments],cwd=self.clean,
                              env=self.environment if environment is None else environment,
                              capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=100)

    def test_real_figures_build_without_the_old_kit(self):
        self.assertFalse((self.clean/'build/consegna-cabinet-20261119').exists())
        result=self.run_command('tools/figure_completamento.py','--out','build/figures')
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertEqual(len(list((self.clean/'build/figures').glob('*.pdf'))),4)
        for name in ('chiusa-reflex','condotto-ingombro-velocita','direttivita-ideale','condensatore-e-livelli'):
            self.assertEqual((self.clean/'build/figures'/(name+'.svg')).read_bytes(),
                             (ROOT/'docs/figure/completamento-20261125'/(name+'.svg')).read_bytes())
        result=self.run_command('tools/visualizza_simulazioni.py')
        self.assertEqual(result.returncode,0,result.stderr)
        result=self.run_command('tools/visualizza_simulazioni.py','--check')
        self.assertEqual(result.returncode,0,result.stderr+result.stdout)
        relative='docs/figure/sistema-autonomo/fattibilita-basso.svg'
        self.assertEqual((self.clean/relative).read_bytes(),(ROOT/relative).read_bytes())
        self.assertFalse((self.clean/'build/consegna-cabinet-20261119').exists())

    def test_real_cad_reads_all_three_variants_without_the_old_kit(self):
        result=self.run_command('tools/cabinet-dettagli-cadcraft.py','--out','build/cad','--solo-verifica')
        self.assertEqual(result.returncode,0,result.stderr)
        report=json.loads((self.clean/'build/cad/esito.json').read_text(encoding='utf-8'))
        self.assertEqual({v['id'] for v in report['variants']},{'A24','B27','C24'})
        self.assertTrue(all(v['units_mm'] and v['shapes_verified']==12 for v in report['variants']))

    def test_kit_contracts_need_no_generated_cad_or_pdf(self):
        self.assertFalse((self.clean/'docs/pdf').exists())
        self.assertFalse((self.clean/'build/completamento-20261125-freecad-verificato').exists())
        result=self.run_command('tools/test_consegna_completamento.py')
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertIn('Ran 5 tests',result.stderr)

    def test_missing_explicit_font_fails_before_creating_output(self):
        environment=dict(self.environment,INTRAWELT_FONT_DIR=str(self.clean/'absent-fonts'))
        result=self.run_command('tools/figure_completamento.py','--out','build/must-not-exist',environment=environment)
        self.assertNotEqual(result.returncode,0)
        self.assertIn('Altro-Grotesk-Book.ttf',result.stderr)
        self.assertFalse((self.clean/'build/must-not-exist').exists())


if __name__=='__main__':unittest.main()
