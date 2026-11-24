"""Riferimenti analitici e casi fuori dai limiti per lo studio del ripiano."""
import math
import unittest
import studia_ingombri as study


class FootprintTest(unittest.TestCase):
    def test_axes_and_30_degree_reference(self):
        self.assertEqual(study.footprint(230,300,0),(230,300))
        x,y=study.footprint(230,300,90)
        self.assertAlmostEqual(x,300);self.assertAlmostEqual(y,230)
        x,y=study.footprint(230,300,30)
        self.assertAlmostEqual(x,349.1858428704209)
        self.assertAlmostEqual(y,374.8076211353316)

    def test_bad_inputs_are_refused(self):
        for w,d,a in [(0,10,0),(10,10,-1),(10,10,91),(math.nan,10,0),(10,math.inf,30)]:
            with self.subTest(values=(w,d,a)),self.assertRaises(ValueError): study.footprint(w,d,a)

    def test_panel_volume_matches_independent_shell_volume(self):
        panels=study.panel_specs(220,190,430,18)
        self.assertEqual(len(panels),6)
        volume=sum(math.prod(p['size']) for p in panels)
        self.assertEqual(volume,220*190*430-184*154*394)
        with self.assertRaises(ValueError): study.panel_specs(30,200,400,18)

    def test_contact_distinguishes_face_edge_and_gap(self):
        a=[0,10,0,20,0,30]
        self.assertEqual(study.box_contact_area(a,[10,15,0,20,0,30]),600)
        self.assertEqual(study.box_contact_area(a,[10,15,20,25,0,30]),0)
        self.assertEqual(study.box_contact_area(a,[10.1,15,0,20,0,30]),0)

    def test_depth_margin_changes_the_result_at_the_boundary(self):
        shelf={'width':1180,'depth':300,'outer_margin':10,'depth_margin':10,'screen_gap':10}
        box={'width':220,'depth':280,'height':430,'thickness':18,'yaw_deg':0}
        self.assertTrue(study.layout(box,shelf,540)['fits_nominal_rectangle'])
        box['depth']=281
        self.assertFalse(study.layout(box,shelf,540)['fits_nominal_rectangle'])

    def test_axis_intersection_uses_transformed_front_centers(self):
        shelf={'width':1180,'depth':300,'outer_margin':10,'depth_margin':10,'screen_gap':10}
        box={'width':220,'depth':190,'height':430,'thickness':18,'yaw_deg':30}
        result=study.layout(box,shelf,540)
        left=result['front_centers'][0]
        right=result['front_centers'][1]
        eye=result['axis_intersection']
        self.assertAlmostEqual(eye[0],590)
        self.assertAlmostEqual((eye[0]-left[0])/(left[1]-eye[1]),math.tan(math.pi/6))
        self.assertAlmostEqual((right[0]-eye[0])/(right[1]-eye[1]),math.tan(math.pi/6))
        self.assertLess(result['front_center_separation'],1180-20-result['footprint'][0])


if __name__=='__main__':unittest.main()
