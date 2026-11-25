"""Riferimenti analitici indipendenti per reflex, apertura e somma dei driver."""
import importlib
import importlib.util
import math
import unittest
import numpy as np


class CabinetPhysics(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(importlib.util.find_spec('acustica_cabinet'), 'Manca il modello acustico')
        self.a = importlib.import_module('acustica_cabinet')

    def test_lossless_butterworth_fourth_order_reference(self):
        # Allineamento B4: h=1, alpha=sqrt(2), Qts=sin(pi/8).
        h = self.a.vented_box(np.array([20., 40., 80.]), 40, 0.3826834323650898,
                              14.14213562373095, 10, 40, math.inf)
        np.testing.assert_allclose(abs(h['total']),
                                   [0.06237828615518053, 0.7071067811865476, 0.9980525784828885], rtol=1e-12)

    def test_port_and_cone_sum_keeps_phase(self):
        h = self.a.vented_box(np.array([15., 40., 60., 200.]), 40, .4, 20, 10, 40, 10)
        np.testing.assert_allclose(h['total'], h['cone'] + h['port'], atol=1e-13)
        self.assertLess(abs(h['total'][0]), abs(h['cone'][0]))

    def test_lossless_cone_stops_at_tuning_but_port_radiates(self):
        h = self.a.vented_box(40., 40, .4, 20, 10, 40, math.inf)
        self.assertLess(abs(h['cone']), 1e-12)
        self.assertGreater(abs(h['port']), .1)

    def test_port_losses_change_output_and_remove_cone_zero(self):
        lossless = self.a.vented_box(40., 40, .4, 20, 10, 40, math.inf)
        lossy = self.a.vented_box(40., 40, .4, 20, 10, 40, 5)
        self.assertGreater(abs(lossy['cone']), .01)
        self.assertLess(abs(lossy['total']), abs(lossless['total']))

    def test_port_geometry_conserves_volume_and_helmholtz_tuning(self):
        p = self.a.port_geometry(10., 50., 40., 2., 1.46)
        self.assertAlmostEqual(p['net_volume_l'] + p['tube_displacement_l'], 10., places=11)
        measured_fb = 343 / (2*math.pi) * math.sqrt(
            (math.pi*.020**2) / (p['net_volume_l']*.001 * p['effective_length_mm']*.001))
        self.assertAlmostEqual(measured_fb, 50., places=10)
        self.assertAlmostEqual(p['effective_length_mm'] - p['length_mm'], 29.2, places=10)
        self.assertGreater(p['length_mm'], 0)

    def test_impossible_port_and_invalid_inputs_are_rejected(self):
        for args in [(0.,50.,40.,2.,1.46), (1.,20.,180.,2.,1.46), (10.,50.,40.,-1.,1.46)]:
            with self.subTest(args=args), self.assertRaises(ValueError):
                self.a.port_geometry(*args)
        for f in [0, -1, float('nan'), float('inf')]:
            with self.subTest(f=f), self.assertRaises(ValueError):
                self.a.vented_box(f, 40, .4, 20, 10, 40, 10)

    def test_port_volume_excludes_the_part_inside_the_rear_panel(self):
        p = self.a.port_geometry(10., 50., 40., 2., 1.46, panel_thickness_mm=18.)
        occupied = math.pi*.022**2 * (p['length_mm']-18.)
        self.assertAlmostEqual(p['tube_displacement_l'], occupied, places=11)
        self.assertAlmostEqual(p['net_volume_l'] + occupied, 10., places=11)

    def test_piston_axis_bessel_reference_and_first_null(self):
        # 2*J1(1), primo zero J1 e segno del secondo lobo, da riferimenti Bessel.
        values = self.a.piston_directivity(np.array([0., 1., 3.8317059702075125, 5.]))
        np.testing.assert_allclose(values[:2], [1., .880101171489867], atol=1e-13)
        self.assertLess(abs(values[2]), 1e-12)
        self.assertLess(values[3], 0)
        np.testing.assert_allclose(self.a.piston_directivity(np.array([-1., -5.])), values[[1,3]], atol=1e-13)

    def test_coincident_point_sources_sum_to_unit_magnitude_lr4(self):
        response = self.a.two_way_response(np.array([500., 1300., 2600., 5200., 8000.]), 0,
                                          0, 0, 0, 2600, 0)
        np.testing.assert_allclose(abs(response), np.ones(5), atol=1e-13)

    def test_half_wavelength_path_cancels_at_crossover(self):
        # A 2,6 kHz, interasse 343/2600 m e angolo 30 gradi danno mezzo periodo.
        response = self.a.two_way_response(2600., 30, 0, 0, 343/2.6, 2600, 0)
        self.assertLess(abs(response), 1e-12)

    def test_depth_offset_changes_on_axis_sum(self):
        aligned = self.a.two_way_response(2600., 0, 124, 6.2, 132, 2600, 0)
        shifted = self.a.two_way_response(2600., 0, 124, 6.2, 132, 2600, 20)
        self.assertAlmostEqual(abs(aligned), 1., places=12)
        self.assertLess(abs(shifted), .95)

    def test_electrical_units_and_rc_pole(self):
        self.assertAlmostEqual(self.a.dbu_to_vrms(0), .7745966692414834, places=12)
        self.assertAlmostEqual(self.a.dbu_to_vrms(20), 7.745966692414834, places=11)
        pole = 1/(2*math.pi*3.2*47e-6)
        h = self.a.series_capacitor_response(pole, 3.2, 47)
        self.assertAlmostEqual(abs(h), 1/math.sqrt(2), places=12)
        self.assertAlmostEqual(float(np.angle(h, deg=True)), 45., places=12)


if __name__ == '__main__':
    unittest.main()
