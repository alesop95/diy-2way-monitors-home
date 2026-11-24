"""Prove fisiche della trasformazione e del target: attesi indipendenti."""
import math
import unittest
import numpy as np
import fattibilita_basso as bass


class BassPhysics(unittest.TestCase):
    def test_identity_transform_is_unity_in_complex_domain(self):
        f = np.geomspace(1,10000,301)
        np.testing.assert_allclose(bass.transform(f,75,.8,75,.8),np.ones_like(f),atol=1e-14)

    def test_transform_cancels_original_poles_not_just_magnitude(self):
        f = np.geomspace(5,1000,501)
        actual = bass.highpass(f,74,.78)
        target = bass.highpass(f,43,1/math.sqrt(2))
        np.testing.assert_allclose(actual*bass.transform(f,74,.78,43,1/math.sqrt(2)),target,rtol=1e-12,atol=1e-14)

    def test_target_includes_subsonic_loss(self):
        ft = bass.target_frequency(60,-2,35)
        amplitude = abs(bass.highpass(60,ft,1/math.sqrt(2)))*bass.lr4_hp(60,35)
        self.assertAlmostEqual(20*math.log10(amplitude),-2,places=12)
        self.assertLess(ft,60)

    def test_impossible_target_is_rejected_instead_of_nan(self):
        with self.assertRaises(ValueError):
            bass.target_frequency(60,-.2,35)

    def test_same_output_pressure_still_requires_same_displacement(self):
        # 6 dB di EQ moltiplicano la corsa richiesta, non il limite meccanico.
        ceiling = bass.excursion_spl(60,124,4.5,1)
        self.assertAlmostEqual(bass.required_excursion(ceiling,ceiling,4.5),4.5)
        self.assertAlmostEqual(bass.required_excursion(ceiling+20*math.log10(2),ceiling,4.5),9)


if __name__ == '__main__':
    unittest.main()
