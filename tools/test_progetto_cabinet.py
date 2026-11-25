"""Prove geometriche: sottrazioni, collisioni e limiti del candidato nominale."""
import copy
import importlib
import importlib.util
import math
import unittest


class CabinetDetails(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(importlib.util.find_spec('progetto_cabinet'), 'Manca il progetto geometrico')
        self.p = importlib.import_module('progetto_cabinet')
        self.drivers = {
            'W': {'outer_diameter_mm':100., 'rear_diameter_mm':70., 'flange_thickness_mm':5.,
                  'overall_depth_mm':50., 'mount_pcd_mm':90., 'mount_count':4, 'mount_angle_deg':45.},
            'T': {'outer_diameter_mm':40., 'rear_diameter_mm':25., 'flange_thickness_mm':3.,
                  'overall_depth_mm':20., 'mount_pcd_mm':32., 'mount_count':4, 'mount_angle_deg':45.}}
        self.variant = {'id':'TEST', 'cabinet':{'width':200., 'depth':200., 'height':400., 'thickness':20.},
                        'woofer':'W', 'tweeter':'T', 'woofer_z_mm':90., 'tweeter_z_mm':190.,
                        'diameter_clearance_mm':1., 'minimum_web_mm':5.,
                        'brace_z_mm':250., 'brace_border_mm':20., 'brace_front_gap_mm':20.}

    def test_front_volume_subtracts_through_holes_and_rebate_annuli_once(self):
        result = self.p.analyse_variant(self.variant, self.drivers)
        removed = math.pi*((35.5**2 + 13.**2)*20 + (50.5**2-35.5**2)*5 + (20.5**2-13.**2)*3)
        self.assertAlmostEqual(result['front_volume_mm3'], 200*400*20-removed, places=7)
        self.assertEqual(len(result['panels']), 6)
        self.assertEqual(len(result['mount_centres']), 8)
        self.assertAlmostEqual(result['driver_spacing_mm'],100.)

    def test_brace_volume_and_contact_area_have_independent_reference(self):
        result = self.p.analyse_variant(self.variant, self.drivers)
        self.assertAlmostEqual(result['brace']['volume_mm3'],208000.)
        self.assertAlmostEqual(result['brace']['side_contact_area_mm2'],2*140*20.)
        self.assertGreater(result['nominal_internal_free_depth_mm'],100.)

    def test_a_rebate_outside_front_is_rejected(self):
        v=copy.deepcopy(self.variant);v['cabinet']['width']=90.
        with self.assertRaisesRegex(ValueError,'frontale'):
            self.p.analyse_variant(v,self.drivers)

    def test_driver_overlap_is_rejected(self):
        v=copy.deepcopy(self.variant);v['tweeter_z_mm']=120.
        with self.assertRaisesRegex(ValueError,'interferenza'):
            self.p.analyse_variant(v,self.drivers)

    def test_driver_behind_back_or_brace_is_rejected(self):
        for change in ('back','brace'):
            v=copy.deepcopy(self.variant);d=copy.deepcopy(self.drivers)
            if change=='back': d['W']['overall_depth_mm']=300.
            else: v['brace_z_mm']=80.
            with self.subTest(change=change), self.assertRaises(ValueError):
                self.p.analyse_variant(v,d)

    def test_drawing_bolt_circle_is_not_used_as_the_cutout(self):
        result=self.p.analyse_variant(self.variant,self.drivers)
        hole=result['openings'][0]
        self.assertAlmostEqual(hole['cut_diameter_mm'],71.)
        first=result['mount_centres'][0]
        self.assertAlmostEqual(math.hypot(first['x_mm']-100,first['z_mm']-90),45.)

    def test_real_candidates_use_canonical_box_dimensions(self):
        config,drivers=self.p.load_project()
        rows=[self.p.analyse_variant(v,drivers) for v in config['variants']]
        self.assertEqual([r['id'] for r in rows],['A24','B27','C24'])
        self.assertAlmostEqual(rows[0]['external_dimensions_mm'][0],220.)
        self.assertEqual(rows[0]['acoustic_design_approved'],False)
        self.assertEqual(rows[0]['actual_support_verified'],False)


if __name__=='__main__':
    unittest.main()
