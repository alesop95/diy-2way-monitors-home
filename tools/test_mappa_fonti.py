"""Contratti del registro degli usi: identità stabile, alias e perdita di testo."""
from pathlib import Path
import tempfile
import unittest
import mappa_fonti_progetto as sources


class SourceIdentity(unittest.TestCase):
    def test_tracking_does_not_create_a_new_source(self):
        self.assertEqual(sources.identity('https://www.linkwitzlab.com/filters.htm?utm_source=x'),
                         sources.identity('http://linkwitzlab.com/filters.htm'))

    def test_distinct_parts_remain_distinct(self):
        self.assertNotEqual(sources.identity('https://aes.org/e-lib/?id=1'),
                            sources.identity('https://aes.org/e-lib/?id=2'))

    def test_alias_is_assigned_to_exactly_one_source(self):
        with self.assertRaises(ValueError):
            sources.alias_index([{'id':'SRC-A','url':'https://a.net/a','aliases':['https://a.net/same']},
                                 {'id':'SRC-B','url':'https://a.net/b','aliases':['https://a.net/same']}])

    def test_adding_a_source_does_not_renumber_others(self):
        before = sources.identity('https://linkwitzlab.com/filters.htm')
        sources.identity('https://www.w3.org/TR/audio-eq-cookbook/')
        self.assertEqual(before,sources.identity('https://linkwitzlab.com/filters.htm'))

    def test_unreviewed_usage_is_not_promoted_to_read(self):
        record = sources.default_source('https://github.com/HEnquist/camilladsp','Etichetta nel documento')
        self.assertEqual(record['lettura']['stato'],'da_riconciliare')
        self.assertEqual(record['verifica']['stato'],'da_verificare')

    def test_reserved_example_is_not_a_public_source(self):
        with self.assertRaises(ValueError):
            sources.identity('https://example.net/paper')

    def test_new_unclassified_source_can_receive_usage(self):
        record = sources.default_source('https://github.com/HEnquist/camilladsp','CamillaDSP')
        record['usi'].append({'file':'docs/prova.md','riga':1,'sezione':'Prova'})
        self.assertEqual(len(record['usi']),1)

    def test_duplicate_seed_identity_is_rejected_before_dictionary_join(self):
        with self.assertRaises(ValueError):
            sources.seed_index([{'id':'SRC-A','url':'https://a.net/one'},
                                {'id':'SRC-A','url':'https://a.net/two'}])

    def test_private_endpoint_is_not_a_public_source(self):
        self.assertFalse(sources.public_url('http://127.0.0.1:1234/'))
        self.assertFalse(sources.public_url('http://192.168.1.5/'))

    def test_context_does_not_relocate_relative_links(self):
        self.assertEqual(sources.context_text('Leggi il [piano](58-piano-dsp-persistente.md).'),
                         'Leggi il piano.')


if __name__ == '__main__':
    unittest.main()
