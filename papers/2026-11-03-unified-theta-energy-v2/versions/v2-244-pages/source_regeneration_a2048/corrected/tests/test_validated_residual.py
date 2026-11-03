import math
from fractions import Fraction
import sys
from pathlib import Path
import unittest
import numpy as np
import mpmath as mp

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from interval_bounds import IV
from validated_phi import phi
from ntt_gamma_rows import ntt,PRIMES,crt_signed
from ball_array import Ball,pairs_ball,fraction_pair
from validated_quadrature import logarithmic_moments,gauss_verified,cheb_vandermonde_ball,prime_geometry


class ValidatedResidualTests(unittest.TestCase):
    def test_complete_phi_enclosures_against_high_precision(self):
        mp.mp.dps=100
        for s in ['0','0.00001','.2','.9999','1','1.00001','2','3.2']:
            r=mp.mpf(s);z=mp.exp(-r/2)
            v=mp.polylog(2,z)-mp.polylog(2,-z)+2*mp.im(mp.polylog(2,1j*z));b=phi(IV(s))
            self.assertLessEqual(mp.mpf(str(b.lo)),v);self.assertGreaterEqual(mp.mpf(str(b.hi)),v)

    def test_moduli_roots_and_exact_signed_convolutions(self):
        for p,g in PRIMES:
            self.assertTrue(all(p%d for d in range(2,math.isqrt(p)+1)))
            for size in [4096,16384]:
                root=pow(g,(p-1)//size,p)
                self.assertEqual(pow(root,size,p),1);self.assertNotEqual(pow(root,size//2,p),1)
        rng=np.random.default_rng(20261102)
        for bound in [100,1<<40]:
            aa=rng.integers(-bound,bound,size=9,dtype=np.int64);bb=rng.integers(-bound,bound,size=7,dtype=np.int64)
            a=np.r_[aa,np.zeros(32-len(aa),dtype=np.int64)];b=np.r_[bb,np.zeros(32-len(bb),dtype=np.int64)]
            residues=[]
            for p,g in PRIMES:
                self.assertTrue(np.array_equal(ntt(ntt(a,p,g),p,g,True),a%p))
                residues.append(ntt(ntt(a,p,g)*ntt(b,p,g)%p,p,g,True))
            actual=crt_signed(residues);expected=np.convolve(a.astype(object),b.astype(object))[:32]
            self.assertTrue(np.array_equal(actual,expected))

    def test_array_ball_dots_against_exact_rationals(self):
        rng=np.random.default_rng(7);a=rng.normal(size=(5,11));b=rng.normal(size=(11,4));c=Ball(a)@Ball(b)
        for i in range(5):
            for j in range(4):
                exact=sum(Fraction(float(a[i,k]))*Fraction(float(b[k,j])) for k in range(11))
                self.assertLessEqual(abs(exact-Fraction(float(c.mid[i,j]))),Fraction(float(c.rad[i,j])))

    def test_chebyshev_error_budget_against_exact_polynomials(self):
        points=[Fraction(-999,1000),Fraction(-1,7),Fraction(0),Fraction(13,17),Fraction(999,1000)]
        x=pairs_ball([fraction_pair(v) for v in points]);T=cheb_vandermonde_ball(x,32)
        for i,v in enumerate(points):
            a=Fraction(1);b=v;exact=[a,b]
            for _ in range(1,32):a,b=b,2*v*b-a;exact.append(b)
            for j,e in enumerate(exact):
                self.assertLessEqual(abs(e-Fraction(float(T.mid[i,j]))),Fraction(float(T.rad[i,j])))

    def test_log_moments_and_verified_gauss_polynomial_exactness(self):
        mp.mp.dps=90;points=[Fraction(0),Fraction(1,7),Fraction(1,2),Fraction(1)]
        L,R,UU,VV,UV=logarithmic_moments(points,32)
        for i,(a,b) in enumerate(zip(points,points[1:])):
            aa=mp.mpf(a.numerator)/a.denominator;bb=mp.mpf(b.numerator)/b.denominator
            for k in [0,1,8,32]:
                exact=mp.quad(lambda t:mp.chebyt(k,2*t-1)*t*mp.log(t),[aa,bb])
                self.assertLessEqual(abs(exact-mp.mpf(float(L.mid[i,k]))),mp.mpf(float(L.rad[i,k])))
            exact=mp.quad(lambda t:t*(1-t)*mp.log(t)*mp.log(1-t),[aa,bb])
            self.assertLessEqual(abs(exact-mp.mpf(float(UV.mid[i]))),mp.mpf(float(UV.rad[i])))
        x,w=gauss_verified(33);T=cheb_vandermonde_ball(x,32)
        integral=w.reshape(1,33)@T
        for j in range(33):
            exact=Fraction(0) if j%2 else Fraction(2,1-j*j)
            self.assertLessEqual(abs(exact-Fraction(float(integral.mid[0,j]))),Fraction(float(integral.rad[0,j])))

    def test_prime_geometry_retains_all_powers_and_shifted_mesh_phases(self):
        records,points=prime_geometry()
        self.assertEqual([r['n'] for r in records],[2,3,4,5,7,8,9,11,13,16,17,19,23])
        for r in records:
            for q in [r['shift']*640,-r['shift']*640]:self.assertIn(q-q.__floor__(),points)
        self.assertEqual(points[0],0);self.assertEqual(points[-1],1)


if __name__=='__main__':unittest.main()
