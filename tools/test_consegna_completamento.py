"""Il kit firma soltanto i file CAD ancora coincidenti con quelli collaudati."""
import importlib
import importlib.util
import io
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT=Path(__file__).resolve().parents[1]


class NominalKitIntegrity(unittest.TestCase):
    def setUp(self):
        (ROOT/'build').mkdir(exist_ok=True)
        self.assertIsNotNone(importlib.util.find_spec('consegna_completamento'),'Manca la consegna verificata')
        self.s=importlib.import_module('consegna_completamento')

    def test_kit_includes_editable_cad_and_reports_for_each_variant(self):
        raw=self.s.bundle()
        with zipfile.ZipFile(io.BytesIO(raw)) as z:
            for variant in ('A24','B27','C24'):
                for filename in ('cabinet-nominale.FCStd','cabinet-nominale.step','pannelli-e-frontale.dxf','distinta-coppia.csv'):
                    self.assertGreater(len(z.read('cad/'+variant+'/'+filename)),50)
            manifest=json.loads(z.read('manifest.json'))
            self.assertFalse(manifest['manufacturing_release'])
            self.assertFalse(manifest['hardware_qualified'])
            self.assertIn('reports/risultati.json',manifest['files'])

    def test_altered_extracted_model_is_rejected(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'build') as temporary:
            folder=Path(temporary)
            with zipfile.ZipFile(io.BytesIO(self.s.bundle())) as z:z.extractall(folder)
            self.assertGreater(self.s.verify_installed(folder),20)
            (folder/'cad/A24/cabinet-nominale.step').write_bytes(b'alterato')
            with self.assertRaises(ValueError):self.s.verify_installed(folder)

    def test_altered_step_is_rejected_before_the_new_manifest_is_signed(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'build') as temporary:
            copied=Path(temporary)/'cad'
            shutil.copytree(self.s.FREECAD,copied)
            (copied/'normal/A24/cabinet-nominale.step').write_bytes(b'alterato prima del kit')
            with patch.object(self.s,'FREECAD',copied), self.assertRaisesRegex(ValueError,'STEP'):
                self.s.bundle()

    def test_stale_pdf_source_is_rejected_before_signing_the_kit(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'build') as temporary:
            path=Path(temporary)/'manifest.json'
            manifest=json.loads((ROOT/'docs/pdf/manifest.json').read_text(encoding='utf-8'))
            document=next(d for d in manifest['documenti'] if d['pdf'].endswith('reflex-direttivita-cabinet.pdf'))
            document['sorgenti']['docs/64-reflex-direttivita-e-cabinet-nominale.md']='0'*64
            path.write_text(json.dumps(manifest),encoding='utf-8')
            with patch.object(self.s,'DOC_MANIFEST',path,create=True), self.assertRaisesRegex(ValueError,'PDF'):
                self.s.bundle()


if __name__=='__main__':unittest.main()
