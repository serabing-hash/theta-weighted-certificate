import sys
import unittest
from fractions import Fraction
from pathlib import Path
import mpmath as mp
import numpy as np
from scipy import integrate

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from interval_bounds import IV
from freeze_candidate import cosine_table,actual_moments,nonsingularity,exact
from weighted64 import theta,cosines,values_from_nodes
from weighted64 import gamma_row,mesh_quadrature
from evaluate_frozen_diag import uniform_gamma_rows


class FrozenCoordinateTests(unittest.TestCase):
    def test_interval_cosines_at_exact_grid_angles(self):
        mp.mp.dps=100
        table=cosine_table(16)
        for j,v in enumerate(table):
            ref=mp.cos(mp.pi*j/16)
            # Exact cardinal zeros use the exact value, not tiny mp evaluation noise.
            if j in [8,24]:ref=mp.mpf(0)
            self.assertLessEqual(mp.mpf(str(v.lo)),ref)
            self.assertGreaterEqual(mp.mpf(str(v.hi)),ref)

    def test_exact_centering_interval_contains_direct_moments(self):
        # Deliberately nonzero raw means exercise the kappa centering correction.
        vals=np.array([[.5,.1],[.3,-.2],[-.7,.4],[.2,.3],[-.1,.1],[.1,-.2]])
        nodes=[[exact(x) for x in row] for row in vals]
        means,J=actual_moments(nodes,Fraction(1,5),4,k=2)
        for col in range(2):
            def u(x):return float(values_from_nodes(np.array([x]),vals,.2)[0,col])
            mm=2*sum(integrate.quad(lambda x:np.cosh(x/2)*u(x),j*.2,(j+1)*.2,epsabs=1e-13)[0] for j in range(6))
            self.assertLess(abs(float(means[col].lo)-mm),1e-13)
            for mode in range(2):
                val=2*sum(integrate.quad(lambda x:(u(x)-2*mm*float(theta(x)))*cosines(np.array([x]),2,radius=.8)[0,mode],j*.2,(j+1)*.2,epsabs=1e-13)[0] for j in range(4))
                self.assertLessEqual(float(J[mode][col].lo),val)
                self.assertGreaterEqual(float(J[mode][col].hi),val)

    def test_nonsingularity_uses_explicit_norm_conversion(self):
        J=[[IV(2),IV(1)],[IV(1),IV(3)]]
        r=nonsingularity(J)
        self.assertEqual(r['status'],'CERT')
        self.assertGreater(float(r['J_smallest_singular_value_lower']),0)
        self.assertGreater(float(r['F_trial_scalar_lower']),0)

    def test_fast_gamma_kernel_matches_dense_application(self):
        rng=np.random.default_rng(20261102)
        nodes=rng.normal(size=(48,4));h=.025
        for refinement in [1,2]:
            x,_=mesh_quadrature(2.,80*refinement,8)
            dense=gamma_row(x,nodes,h)
            fast=uniform_gamma_rows(nodes,h,2.,8,refinement)
            self.assertLess(np.max(np.abs(dense-fast)),1e-10)


if __name__=='__main__':unittest.main()
