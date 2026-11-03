import random
import sys
import unittest
from fractions import Fraction
from pathlib import Path

import mpmath as mp
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from interval_bounds import IV,pi_interval,theta_interval,weight_interval,gamma_potential_interval,gamma_label_bounds,spatial_residual_tail,interval_ldl,gate,REQUIRED_COVERAGE


def contains(iv,q):return Fraction(iv.lo)<=q<=Fraction(iv.hi)


class IntervalTests(unittest.TestCase):
    def test_exact_rational_arithmetic_enclosures(self):
        rng=random.Random(20261102)
        for _ in range(150):
            a=Fraction(rng.randint(-100000,100000),rng.randint(1,10000))
            b=Fraction(rng.randint(1,100000),rng.randint(1,10000))
            x=IV.rational(a.numerator,a.denominator);y=IV.rational(b.numerator,b.denominator)
            for z,q in [(x+y,a+b),(x-y,a-b),(x*y,a*b),(x/y,a/b),(x**2,a*a)]:self.assertTrue(contains(z,q))
        self.assertEqual((IV(-2,3)**2).lo,0)
        self.assertGreaterEqual((IV(-2,3)**2).hi,9)
        with self.assertRaises(TypeError):IV(0.1)
        with self.assertRaises(ZeroDivisionError):1/IV(-1,1)

    def test_pi_and_elementary_independent_high_precision_diagnostic(self):
        # Independent high-precision consistency check; not the reason the bounds hold.
        mp.mp.dps=110
        for v,ref in [(pi_interval(),mp.pi),(IV('1.2').exp(),mp.exp(mp.mpf('1.2'))),
                      (IV(2).log(),mp.log(2)),(IV(2).sqrt(),mp.sqrt(2))]:
            self.assertLess(mp.mpf(str(v.lo)),ref);self.assertGreater(mp.mpf(str(v.hi)),ref)

    def test_theta_and_positive_gamma_remainders(self):
        mp.mp.dps=100
        for x0 in ['0','0.4','0.8','1.2']:
            x=mp.mpf(x0);v,tail=theta_interval(x0,3)
            tau=mp.pi*mp.exp(2*x)
            ref=mp.exp(x/2)*sum((4*(tau*j*j)**2-6*tau*j*j)*mp.exp(-tau*j*j) for j in range(1,30))
            self.assertLessEqual(mp.mpf(str(v.lo)),ref);self.assertGreaterEqual(mp.mpf(str(v.hi)),ref)
            self.assertGreater(weight_interval(x0).lo,0)
        v,tail=gamma_potential_interval('0.03',64)
        ref=mp.fsum(mp.exp(-(2*j+mp.mpf('.5'))*mp.mpf('.03'))/(2*j+mp.mpf('.5'))**2 for j in range(5000))
        self.assertLessEqual(mp.mpf(str(v.lo)),ref);self.assertGreaterEqual(mp.mpf(str(v.hi)),ref)

    def test_tail_monotonicity_and_domain_guards(self):
        t=spatial_residual_tail('1.2','2',1,2)
        bigger=spatial_residual_tail('1.2','2',2,4)
        self.assertLess(t.hi,bigger.lo)
        self.assertLess(t.hi,IV('1e-67').lo)
        with self.assertRaises(ValueError):spatial_residual_tail('1.2','1',1,2)
        self.assertGreater(gamma_label_bounds(64)['row_derivative_norm_multiplier'],gamma_label_bounds(128)['row_derivative_norm_multiplier'])

    def test_interval_ldl_positive_negative_and_ambiguous(self):
        self.assertTrue(interval_ldl([[IV(2),IV(1)],[IV(1),IV(2)]])['positive'])
        self.assertFalse(interval_ldl([[IV(1),IV(2)],[IV(2),IV(1)]])['positive'])
        self.assertFalse(interval_ldl([[IV('-0.001','0.001')]])['positive'])
        with self.assertRaises(ValueError):interval_ldl([[IV(1),IV(0)],[IV(1),IV(1)]])

    def test_global_gate_requires_every_full_coverage_field(self):
        for field in REQUIRED_COVERAGE:
            coverage={name:True for name in REQUIRED_COVERAGE};coverage[field]=False
            r=gate([],[],[],[],coverage)
            self.assertEqual(r['status'],'NOT_RUN');self.assertIn(field,r['missing'])

    def test_sharp_constants_are_exact(self):
        from target import A,EPSILON,NU,PENALTY,radius_interval
        self.assertEqual(A,Fraction(1,2048));self.assertEqual(NU,A-EPSILON)
        self.assertGreater(NU,4*A/5);self.assertLess(NU,A)
        self.assertEqual(PENALTY,4/NU+5*A/NU**2)
        self.assertLess(PENALTY,26240);self.assertGreater(PENALTY,24538)
        mp.mp.dps=100
        self.assertLess(mp.mpf(str(radius_interval().lo)),mp.log(8)/2);self.assertGreater(mp.mpf(str(radius_interval().hi)),mp.log(8)/2)



if __name__=='__main__':unittest.main()
