import math
import sys
import unittest
from pathlib import Path

import numpy as np
from scipy import integrate

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import weighted64 as w


class SourceTests(unittest.TestCase):
    def test_theta_probability_normalization(self):
        val,err=integrate.quad(lambda x:4*math.cosh(x/2)*float(w.theta(x)),0,3,epsabs=2e-13)
        self.assertLess(abs(val-1),5e-12)

    def test_prime_powers_and_four_weight(self):
        pp=w.prime_powers(30)
        self.assertEqual([n for n,_,_ in pp],[2,3,4,5,7,8,9,11,13,16,17,19,23,25,27,29])
        self.assertEqual(dict((n,p) for n,p,_ in pp)[27],3)
        self.assertAlmostEqual(dict((n,a) for n,_,a in pp)[4],math.log(2)/2)

    def test_gamma_potential_against_positive_series(self):
        alpha=2*np.arange(100000)+0.5
        for d in [0.02,0.13,1.0,3.0]:
            ref=np.sum(np.exp(-alpha*d)/alpha**2)
            self.assertLess(abs(w.gamma_potential(d)-ref),2e-14)

    def test_gamma_row_against_difference_integral(self):
        h=.2
        for x in [.017,.2,.37]:
            def hat(t):return max(1-abs(t)/h,0)
            def f(s):
                return math.exp(-s/2)/(-math.expm1(-2*s))*(2*hat(x)-hat(x+s)-hat(x-s))
            breaks=sorted(set([0.,abs(x),abs(x-h),x+h,50.]))
            ref=sum(integrate.quad(f,a,b,epsabs=1e-11)[0] for a,b in zip(breaks,breaks[1:]))
            # For x inside support the remaining 2u(x)rho tail is included.
            ref+=2*hat(x)*integrate.quad(lambda s:math.exp(-s/2)/(-math.expm1(-2*s)),50,200)[0]
            self.assertLess(abs(float(w.gamma_hat(x,h))-ref),1e-10)

    def test_folding_and_prime_matrix_direct(self):
        n=6;h=.2;L=n*h
        nodes=np.array([.3,-.5,.7,.1,-.2,.3])[:,None]
        matrix,primes=w.prime_matrix(n,h,L)
        def g(x):return float(w.values_from_nodes(np.array([x]),nodes,h)[0,0])
        ref=0.
        for value,_,a in primes:
            s=math.log(value)
            knots=sorted(set([-L,L]+[j*h for j in range(-n,n+1)]+[j*h-s for j in range(-n,n+1) if -L<j*h-s<L]))
            ref+=2*a*sum(integrate.quad(lambda x:g(x+s)*g(x),lo,hi,epsabs=1e-13)[0] for lo,hi in zip(knots,knots[1:]))
        self.assertAlmostEqual(float(nodes[:,0]@matrix@nodes[:,0]),ref,places=12)

    def test_exact_mean_formula_and_physical_cosine_normalization(self):
        n=48;h=1.2/n
        mass,mean,M=w.moments_and_mass(n,h,8,16)
        for j in [0,1,16,47]:
            lo=max(0,(j-1)*h);hi=(j+1)*h
            ref=2*integrate.quad(lambda x:math.cosh(x/2)*max(1-abs(x/h-j),0),lo,hi,points=[j*h],epsabs=1e-14)[0]
            self.assertAlmostEqual(mean[j],ref,places=13)
        x,q=w.mesh_quadrature(w.B,64,12)
        E=w.cosines(x,64)
        self.assertLess(np.max(np.abs(E.T@((2*q)[:,None]*E)-np.eye(64))),5e-14)

    def test_riesz_centered_gram_identity(self):
        k=4;F,half,inv,ev,d=w.riesz_gram(k)
        xi,qi=w.mesh_quadrature(w.B,1000,12)
        xo,qo=w.mesh_quadrature(2-w.B,1000,12)
        x=np.r_[xi,xo+w.B];q=np.r_[qi,qo]
        inside=x<w.B
        W=w.weight(x)
        b=np.zeros((len(x),k));b[inside]=W[inside,None]*w.cosines(x[inside],k)
        v=b-2*w.theta(x)[:,None]*d
        direct=v.T@((2*q/W)[:,None]*v)
        self.assertLess(np.max(np.abs(direct-F)),1e-13)
        # DIAG whitening roundoff scales with the smaller true-radius Gram pivot.
        tolerance=8*np.finfo(float).eps*k*np.linalg.norm(inv,2)**2*np.linalg.norm(F,2)
        self.assertLess(np.max(np.abs(inv@F@inv-np.eye(k))),tolerance)
        self.assertLess(np.max(np.abs((2*q*np.cosh(x/2))@v)),1e-13)


if __name__=='__main__':unittest.main()
