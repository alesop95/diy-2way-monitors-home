"""Integrità del kit con byte opachi costruiti; non è un collaudo del formato CAD."""
import hashlib
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


def fixture(root,sources):
    """Costruisce prove di integrità senza richiedere CAD o PDF preesistenti."""
    def write(name,raw):
        path=root/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(raw)
        return hashlib.sha256(raw).hexdigest()
    def jsonfile(name,data):write(name,json.dumps(data).encode('utf-8'))
    for name in sources:write(name,('fixture sorgente '+name).encode('utf-8'))
    digest=lambda name:hashlib.sha256((root/name).read_bytes()).hexdigest()
    normal={'status':'success','source_sha256':digest('tools/cabinet-dettagli-freecad.py'),
            'input_sha256':{'config/cabinet/progetto-candidato.json':digest('config/cabinet/progetto-candidato.json')},'variants':[]}
    gui={'status':'captured','source_sha256':digest('tools/cabinet-dettagli-vista.FCMacro'),'variants':[]}
    cad={'status':'success','source_sha256':digest('tools/cabinet-dettagli-cadcraft.py'),
         'dependency_sha256':{'tools/font_intrawelt.py':digest('tools/font_intrawelt.py')},'variants':[]}
    payloads={}
    for variant in ('A24','B27','C24'):
        def artifact(directory,name):
            raw=('fixture opaca '+variant+' '+name).encode('utf-8')
            payloads[(variant,name)]=raw
            return write(directory+'/'+variant+'/'+name,raw)
        base='build/completamento-20261125-freecad-verificato'
        normal['variants'].append({'id':variant,'native_sha256':artifact(base+'/normal','cabinet-nominale.FCStd'),
                                   'step_sha256':artifact(base+'/normal','cabinet-nominale.step')})
        gui['variants'].append({'id':variant,'native_sha256':artifact(base+'/views','cabinet-con-vista.FCStd'),
                                'preview_sha256':artifact(base+'/views','assieme.png')})
        files={name:artifact('build/completamento-20261125-cadcraft-verificato',name)
               for name in ('pannelli-e-frontale.dxf','pannelli-e-frontale.pdf','pannelli-e-frontale.svg','distinta-coppia.csv')}
        cad['variants'].append({'id':variant,'files':files})
    jsonfile(base+'/normal/esito.json',normal);jsonfile(base+'/views/esito.json',gui)
    jsonfile('build/completamento-20261125-cadcraft-verificato/esito.json',cad)
    for name in ('chiusa-reflex','condotto-ingombro-velocita','direttivita-ideale','condensatore-e-livelli'):
        write('docs/figure/completamento-20261125/'+name+'.svg',b'<svg/>')
    report={'fixture':'contratto di integrita dei byte, non geometria'}
    jsonfile('research-vault/completamento-20261125/risultati.json',report)
    pdf='docs/pdf/reflex-direttivita-cabinet.pdf';pdf_sha=write(pdf,b'%PDF fixture di sola integrita')
    source='docs/64-reflex-direttivita-e-cabinet-nominale.md'
    jsonfile('docs/pdf/manifest.json',{'documenti':[{'pdf':pdf,'sha256':pdf_sha,'sorgenti':{source:digest(source)}}]})
    return report,payloads


class NominalKitIntegrity(unittest.TestCase):
    def setUp(self):
        (ROOT/'build').mkdir(exist_ok=True)
        self.assertIsNotNone(importlib.util.find_spec('consegna_completamento'),'Manca la consegna verificata')
        self.s=importlib.import_module('consegna_completamento')
        temporary=tempfile.TemporaryDirectory(dir=ROOT/'build');self.addCleanup(temporary.cleanup)
        root=Path(temporary.name)
        report,self.payloads=fixture(root,self.s.SOURCES)
        resources={'ROOT':root,'FREECAD':root/'build/completamento-20261125-freecad-verificato',
                   'CADCRAFT':root/'build/completamento-20261125-cadcraft-verificato',
                   'DOC_MANIFEST':root/'docs/pdf/manifest.json','build_report':lambda:report}
        for name,value in resources.items():
            replacement=patch.object(self.s,name,value);replacement.start();self.addCleanup(replacement.stop)

    def test_kit_includes_editable_cad_and_reports_for_each_variant(self):
        raw=self.s.bundle()
        with zipfile.ZipFile(io.BytesIO(raw)) as z:
            for variant in ('A24','B27','C24'):
                for filename in ('cabinet-nominale.FCStd','cabinet-nominale.step','pannelli-e-frontale.dxf','distinta-coppia.csv'):
                    expected='cabinet-con-vista.FCStd' if filename.endswith('.FCStd') else filename
                    self.assertEqual(z.read('cad/'+variant+'/'+filename),self.payloads[(variant,expected)])
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
            manifest=json.loads(self.s.DOC_MANIFEST.read_text(encoding='utf-8'))
            document=next(d for d in manifest['documenti'] if d['pdf'].endswith('reflex-direttivita-cabinet.pdf'))
            document['sorgenti']['docs/64-reflex-direttivita-e-cabinet-nominale.md']='0'*64
            path.write_text(json.dumps(manifest),encoding='utf-8')
            with patch.object(self.s,'DOC_MANIFEST',path,create=True), self.assertRaisesRegex(ValueError,'PDF'):
                self.s.bundle()

    def test_changed_cad_dependency_is_rejected_before_signing(self):
        (self.s.ROOT/'tools/font_intrawelt.py').write_bytes(b'dipendenza modificata')
        with self.assertRaisesRegex(ValueError,'Dipendenza CADCraft'):
            self.s.bundle()


if __name__=='__main__':unittest.main()
