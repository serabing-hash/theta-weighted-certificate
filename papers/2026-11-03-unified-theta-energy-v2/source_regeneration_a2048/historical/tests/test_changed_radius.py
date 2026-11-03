import math,random,sys,unittest
from pathlib import Path
from fractions import Fraction as F
import numpy as np
import mpmath as mp
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from integer_convolution import signed_convolution
from source_geometry import geometry,moment_coefficients
from verify_gram_upper import gram_trace_exact,gram_integer_matrix
from validated_quadrature import prime_geometry
from ball_array import fraction_pair

class ChangedRadiusTests(unittest.TestCase):
    def test_signed_integer_convolution_large_and_negative(self):
        rng=random.Random(1024)
        for bits in [1,20,80,170]:
            for n,m in [(1,1),(2,7),(9,6),(33,17)]:
                a=[rng.randint(-(1<<bits),1<<bits) for _ in range(n)]
                b=[rng.randint(-(1<<bits),1<<bits) for _ in range(m)]
                expected=[sum(a[i]*b[j-i] for i in range(n) if 0<=j-i<m) for j in range(n+m-1)]
                self.assertEqual(signed_convolution(a,b),expected)
        self.assertEqual(signed_convolution([0,0],[1,-3]),[0,0,0])

    def test_fast_trace_matches_exact_full_gram(self):
        nodes=[[[j-c,8] for c in range(4)] for j in range(7)]
        M,d=gram_integer_matrix(nodes,[[1,1]]*7,F(1,16))
        self.assertEqual(gram_trace_exact(nodes,F(1,16)),sum(F(int(M[i,i]),d) for i in range(4)))

    def test_nonrational_terminal_moments_against_independent_quadrature(self):
        mp.mp.dps=100;h=F(1,80);k=20;n=96
        g=geometry(h,k);q=g[1];C=moment_coefficients(n,h,k,g)
        B=mp.log(8)/2;hh=mp.mpf(1)/80
        for mode in [0,1,7,19]:
            norm=1/mp.sqrt(B*(2 if mode==0 else 1))
            for j in [0,1,q-1,q,q+1,q+2]:
                lo=max(mp.mpf(0),(j-1)*hh);hi=min(B,(j+1)*hh)
                if lo>=hi:exact=mp.mpf(0)
                else:
                    points=sorted(set([lo,hi]+([j*hh] if lo<j*hh<hi else [])))
                    exact=2*norm*mp.quad(lambda x:(1-abs(x/hh-j))*mp.cos(mode*mp.pi*x/B),points)
                self.assertLessEqual(abs(exact-mp.mpf(float(C.mid[mode,j]))),mp.mpf(float(C.rad[mode,j])))
        B0=g[2];self.assertNotEqual(F(float(B0)),B0)
        center,radius=fraction_pair(B0)
        self.assertLessEqual(abs(F(center)-B0),F(radius))

    def test_new_mesh_and_true_boundary_partition(self):
        h=F(1,2560);phase=F(12345,65536)
        records,points=prime_geometry(16,h,[phase])
        self.assertIn(phase,points)
        self.assertIn(7,[r['n'] for r in records]);self.assertIn(8,[r['n'] for r in records])
        for r in records:
            for q in [r['shift']/h,-r['shift']/h]:self.assertIn(q-q.__floor__(),points)

if __name__=='__main__':unittest.main()
