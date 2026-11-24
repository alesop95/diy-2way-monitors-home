import unittest
from hashlib import sha256
from verifica_documenti import inspect_document


class DocumentProvenance(unittest.TestCase):
    def test_changed_source_is_reported_even_if_pdf_is_unchanged(self):
        files={'docs/sorgente.md':b'nuovo','docs/pdf/finale.pdf':b'%PDF-finale'}
        record={'pdf':'docs/pdf/finale.pdf','sha256':sha256(files['docs/pdf/finale.pdf']).hexdigest(),
                'sorgenti':{'docs/sorgente.md':sha256(b'vecchio').hexdigest()}}
        self.assertEqual(inspect_document(record,files.__getitem__),['Sorgente cambiata: docs/sorgente.md'])
        record['sorgenti']['docs/sorgente.md']=sha256(b'nuovo').hexdigest()
        self.assertEqual(inspect_document(record,files.__getitem__),[])

    def test_changed_pdf_and_external_source_are_rejected(self):
        record={'pdf':'docs/pdf/finale.pdf','sha256':sha256(b'%PDF-finale').hexdigest(),
                'sorgenti':{'../esterno.md':'x'}}
        with self.assertRaises(ValueError): inspect_document(record,lambda _:b'diverso')
        record['sorgenti']={}
        self.assertEqual(inspect_document(record,lambda _:b'diverso'),['PDF cambiato: docs/pdf/finale.pdf'])


if __name__=='__main__': unittest.main()
