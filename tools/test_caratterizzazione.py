"""Prove su dati noti: parsing, copertura e integrità, senza acquisizione audio."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import numpy as np
from caratterizzazione import Curve, read_curve, analyse_curve, analyse_dataset, build_bundle, write_bundle, check_bundle

ROOT=Path(__file__).resolve().parents[1]
TARGET={'minimum_hz':60,'maximum_hz':20000,'reference_db':0,'tolerance_db':2,
        'max_gap_octaves':1/12,'minimum_coherence':0.9}


class ResponseFiles(unittest.TestCase):
    def setUp(self):
        (ROOT/'build').mkdir(exist_ok=True)
        temporary=tempfile.TemporaryDirectory(dir=ROOT/'build');self.addCleanup(temporary.cleanup)
        self.folder=Path(temporary.name)

    def file(self,text,name='response.frd'):
        path=self.folder/name;path.write_text(text,encoding='utf-8');return path

    def dense(self,magnitude=0,phase=True,coherence=None):
        f=np.geomspace(50,24000,241)
        return Curve(f,np.full(len(f),magnitude),np.zeros(len(f)) if phase else None,coherence)

    def dataset(self,extra=None):
        self.file('60 0 0\n20000 0 -180\n')
        data={'schema':'speaker-response-dataset-1','data_kind':'synthetic',
              'level_unit':'dB_relative','target':dict(TARGET,max_gap_octaves=9),
              'required_directions':[{'plane':'axial','angle_deg':0}],
              'curves':[{'id':'axial','plane':'axial','angle_deg':0,'path':'response.frd','format':'frd'}]}
        if extra:data.update(extra)
        path=self.folder/'dataset.json';path.write_text(json.dumps(data),encoding='utf-8');return path

    def test_frd_preserves_phase_zero_and_bom_comments(self):
        curve=read_curve(self.file('\ufeff# dati costruiti\n* commento\n60 0 0\n1000 20 90\n20000 0 180\n'),'frd')
        np.testing.assert_allclose(curve.complex_response(),[1,10j,-1],atol=1e-12)

    def test_magnitude_only_is_not_zero_phase(self):
        curve=read_curve(self.file('60 -1\n20000 1\n'),'frd')
        self.assertIsNone(curve.phase_deg)
        with self.assertRaisesRegex(ValueError,'fase'):curve.complex_response()

    def test_osm_csv_has_four_columns_and_coherence(self):
        curve=read_curve(self.file('60,0,0,1\n20000,-1,-180,0.8\n'),'osm_csv')
        np.testing.assert_allclose(curve.phase_deg,[0,-180])
        np.testing.assert_allclose(curve.coherence,[1,0.8])

    def test_osm_frd_is_not_silently_parsed_as_three_columns(self):
        path=self.file('60 0 0 1\n20000 -1 -180 0.95\n')
        with self.assertRaises(ValueError):read_curve(path,'frd')
        np.testing.assert_allclose(read_curve(path,'osm_frd').coherence,[1,0.95])

    def test_invalid_rows_are_rejected(self):
        cases=['60 0 0\n60 1 20','100 0 0\n60 1 20','0 0 0\n100 0 0',
               '60 NaN 0\n100 0 0','60 0 inf\n100 0 0','60 0 0\n100 0',
               '60 0 0 1.1\n100 0 0 1','60 * * 1\n100 0 0 1']
        for text in cases:
            with self.subTest(text=text),self.assertRaises(ValueError):
                read_curve(self.file(text),'osm_frd' if len(text.splitlines()[0].split())==4 else 'frd')

    def test_dense_flat_response_meets_only_the_sampled_target(self):
        result=analyse_curve(self.dense(),TARGET)
        self.assertEqual(result['status'],'within_bounds')
        self.assertEqual(result['maximum_deviation_db'],0)
        self.assertFalse(result['physical_validity_verified'])

    def test_common_level_reference_keeps_off_axis_attenuation(self):
        result=analyse_curve(self.dense(-3),TARGET)
        self.assertEqual(result['status'],'outside_bounds')
        self.assertAlmostEqual(result['maximum_deviation_db'],3)

    def test_endpoints_sparse_grid_and_valid_band_cannot_pass(self):
        cases=[(Curve(np.geomspace(100,24000,241),np.zeros(241)),None,'frequency_coverage'),
               (Curve(np.geomspace(50,15000,241),np.zeros(241)),None,'frequency_coverage'),
               (Curve([60,20000],[0,0]),None,'frequency_grid'),
               (self.dense(),[200,20000],'declared_valid_band')]
        for curve,valid,reason in cases:
            with self.subTest(reason=reason):
                result=analyse_curve(curve,TARGET,valid)
                self.assertEqual(result['status'],'insufficient_coverage')
                self.assertIn(reason,result['coverage_issues'])

    def test_low_coherence_is_reported(self):
        coherence=np.ones(241);coherence[100]=0.5
        self.assertEqual(analyse_curve(self.dense(coherence=coherence),TARGET)['status'],'low_coherence')

    def test_large_interpolation_bracket_at_band_edge_is_not_hidden(self):
        for f in (np.r_[20,np.geomspace(60.01,24000,241)],np.r_[np.geomspace(50,19999,241),40000]):
            with self.subTest(endpoint=float(f[0])):
                result=analyse_curve(Curve(f,np.zeros(len(f))),TARGET)
                self.assertEqual(result['status'],'insufficient_coverage')
                self.assertIn('frequency_grid',result['coverage_issues'])

    def test_low_coherence_outside_target_band_does_not_change_its_result(self):
        coherence=np.ones(241);coherence[0]=0.1
        self.assertEqual(analyse_curve(self.dense(coherence=coherence),TARGET)['status'],'within_bounds')

    def test_missing_direction_is_not_a_pass(self):
        path=self.dataset({'required_directions':[{'plane':'axial','angle_deg':0},
                                                    {'plane':'vertical','angle_deg':10}]})
        report,_=analyse_dataset(path)
        self.assertEqual(report['status'],'incomplete')
        self.assertEqual(report['missing_directions'],[{'plane':'vertical','angle_deg':10.0}])

    def test_declared_measured_data_does_not_qualify_hardware(self):
        report,_=analyse_dataset(self.dataset({'data_kind':'measured'}))
        self.assertEqual(report['status'],'within_bounds')
        self.assertFalse(report['hardware_qualified'])
        self.assertEqual(report['provenance_status'],'declared_not_independently_verified')

    def test_duplicate_id_or_direction_is_rejected(self):
        path=self.dataset();data=json.loads(path.read_text())
        data['curves'].append(dict(data['curves'][0],id='another'))
        path.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError,'direzione'):analyse_dataset(path)
        data['curves'][1]['angle_deg']=1;data['curves'][1]['plane']='horizontal';data['curves'][1]['id']='axial'
        path.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError,'ID'):analyse_dataset(path)

    def test_path_traversal_is_rejected(self):
        path=self.dataset();data=json.loads(path.read_text());data['curves'][0]['path']='../outside.frd'
        path.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError,'percorso'):analyse_dataset(path)

    def test_resolved_directory_link_cannot_escape_dataset(self):
        outside=self.folder/'outside';outside.mkdir();(outside/'curve.frd').write_text('60 0 0\n20000 0 0\n')
        self.folder=self.folder/'dataset';self.folder.mkdir()
        manifest=self.dataset();data=json.loads(manifest.read_text());data['curves'][0]['path']='link/curve.frd'
        manifest.write_text(json.dumps(data));link=self.folder/'link'
        if os.name=='nt':
            quoted=lambda p:"'"+str(p).replace("'","''")+"'"
            subprocess.run(['powershell','-NoProfile','-Command',
                            'New-Item -ItemType Junction -Path '+quoted(link)+' -Target '+quoted(outside)+' | Out-Null'],
                           check=True,capture_output=True)
        else:link.symlink_to(outside,target_is_directory=True)
        try:
            with self.assertRaisesRegex(ValueError,'percorso'):analyse_dataset(manifest)
        finally:
            if os.name=='nt':link.rmdir()
            else:link.unlink()

    def test_manifest_shapes_are_validated(self):
        path=self.dataset()
        for data in ([],{'schema':'speaker-response-dataset-1','data_kind':'synthetic','level_unit':'dB_relative',
                         'target':TARGET,'required_directions':[{'plane':'axial','angle_deg':0}],'curves':[None]}):
            path.write_text(json.dumps(data))
            with self.subTest(data=data),self.assertRaises(ValueError):analyse_dataset(path)

    def test_extra_direction_does_not_redefine_the_requested_window(self):
        path=self.dataset();self.file('60 -30 0\n20000 -30 0\n','outside.frd');data=json.loads(path.read_text())
        data['curves'].append({'id':'horizontal90','plane':'horizontal','angle_deg':90,'path':'outside.frd','format':'frd'})
        path.write_text(json.dumps(data));report,_=analyse_dataset(path)
        self.assertEqual(report['status'],'within_bounds')
        self.assertEqual(report['curves'][1]['status'],'outside_bounds')

    def test_export_has_three_frd_columns_and_preserves_phase(self):
        files=build_bundle(self.dataset())
        self.assertEqual(len(files['curves/axial.frd'].decode().splitlines()[0].split()),3)
        self.assertEqual(files['inputs/response.frd'],(self.folder/'response.frd').read_bytes())
        output=self.folder/'roundtrip.frd';output.write_bytes(files['curves/axial.frd'])
        np.testing.assert_allclose(read_curve(output,'frd').phase_deg,[0,-180])

    def test_magnitude_only_export_does_not_invent_phase(self):
        path=self.dataset();self.file('60 0\n20000 -1\n')
        files=build_bundle(path)
        self.assertNotIn('curves/axial.frd',files)
        self.assertIn('curves/axial.csv',files)
        self.assertIn('60,0,,',files['curves/axial.csv'].decode())

    def test_check_rejects_changed_output_and_input(self):
        manifest=self.dataset();out=self.folder/'output'
        write_bundle(manifest,out);self.assertEqual(check_bundle(manifest,out),[])
        result=out/'report.json';original=result.read_bytes();result.write_bytes(b'alterato')
        self.assertTrue(check_bundle(manifest,out));result.write_bytes(original)
        self.file('60 1 0\n20000 1 -180\n')
        self.assertTrue(check_bundle(manifest,out))

    def test_existing_output_is_preserved(self):
        out=self.folder/'output';out.mkdir();(out/'human.txt').write_text('conservare')
        with self.assertRaises(FileExistsError):write_bundle(self.dataset(),out)
        self.assertEqual((out/'human.txt').read_text(),'conservare')

    def test_relative_dot_path_roundtrips(self):
        manifest=self.dataset();data=json.loads(manifest.read_text());data['curves'][0]['path']='./response.frd'
        manifest.write_text(json.dumps(data));out=self.folder/'output'
        write_bundle(manifest,out)
        self.assertEqual(check_bundle(manifest,out),[])

    def test_cli_reports_invalid_input_before_writing(self):
        manifest=self.dataset();self.file('60 NaN\n20000 0\n');out=self.folder/'output'
        result=subprocess.run([sys.executable,str(ROOT/'tools/caratterizzazione.py'),
                               '--manifest',str(manifest),'--out',str(out)],capture_output=True,text=True)
        self.assertNotEqual(result.returncode,0)
        self.assertFalse(out.exists())

    def test_check_cli_separates_integrity_from_target_result(self):
        manifest=self.dataset();self.file('60 -3 0\n20000 -3 -180\n');out=self.folder/'output'
        write_bundle(manifest,out)
        result=subprocess.run([sys.executable,str(ROOT/'tools/caratterizzazione.py'),'--manifest',str(manifest),
                               '--out',str(out),'--check'],capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)
        report=json.loads(result.stdout)
        self.assertEqual(report['data_status'],'outside_bounds')
        self.assertFalse(report['hardware_qualified'])

    def test_versioned_example_matches_the_tracked_input_files(self):
        report,_=analyse_dataset(ROOT/'data/caratterizzazione-demo/manifest.json')
        saved=json.loads((ROOT/'research-vault/caratterizzazione-aperta-20261126/risultati-esempio.json').read_text(encoding='utf-8'))
        self.assertEqual(report,saved)
        self.assertEqual([r['id'] for r in report['curves'] if r['status']=='outside_bounds'],['v_pos10'])
        self.assertFalse(report['hardware_qualified'])


if __name__=='__main__':unittest.main()
