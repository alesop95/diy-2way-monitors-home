import copy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('collaudo_controllo',ROOT/'tools/collauda-controllo-ascolto.py')
module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)


class RecordedEvidence(unittest.TestCase):
    def test_actual_report_detects_changed_metrics_claims_rates_and_sources(self):
        original=json.loads((ROOT/'research-vault/sistema-autonomo-20261120/risultati-controllo.json').read_text(encoding='utf-8'))
        hashes=original['source_sha256']
        self.assertTrue(module.valid_report(original,hashes))
        for change in ('mute','gain','shutdown','rate','source','signal'):
            with self.subTest(change=change):
                r=copy.deepcopy(original)
                if change=='mute': r['cases'][0]['rms_manual_mute_max']=.01
                elif change=='gain': r['cases'][0]['volume_step_measured_db'][0]=0
                elif change=='shutdown': r['cases'][0]['cli_sigterm_mute_verified']=False
                elif change=='rate': r['cases'][1]['rate_hz']=44100
                elif change=='source': r['source_sha256']={}
                else: r['cases'][0]['rms_minus24_per_channel'][0]=0
                self.assertFalse(module.valid_report(r,hashes))


if __name__=='__main__': unittest.main()
