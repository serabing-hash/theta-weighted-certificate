import sys
import unittest
from fractions import Fraction
from pathlib import Path
import numpy as np
from scipy import integrate

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from verify_gram_upper import gram_integer_matrix
from verify_energy_lower import label_kernel,contract_even_kernel
from interval_bounds import IV
import math


class GramUpperTests(unittest.TestCase):
    def test_exact_integer_assembly_against_polynomial_integration(self):
        # Two half-line cells, two columns, constant cell reciprocal weights.
        nodes=[[[1,2],[-1,4]],[[3,4],[1,8]]]
        weights=[[2,1],[4,1]];h=Fraction(1,8)
        numer,denom=gram_integer_matrix(nodes,weights,h)
        v=np.array([.3,-.7]);values=np.array([[.5,-.25],[.75,.125],[0,0]])
        ref=0.
        for cell,weight in enumerate([2,4]):
            ref+=2*float(h)*weight*integrate.quad(lambda t:float(((1-t)*values[cell]+t*values[cell+1])@v)**2,0,1,epsabs=1e-14)[0]
        matrix=np.array([[float(Fraction(int(x),denom)) for x in row] for row in numer])
        self.assertLess(abs(v@matrix@v-ref),1e-15)
        self.assertTrue(np.array_equal(numer,numer.T))

    def test_finite_gamma_label_against_independent_hat_integral(self):
        h=.1
        for alpha in [.5,3.,20.]:
            values=label_kernel(IV(str(alpha)),IV(str(h)),5)
            for lag in range(5):
                def integrand(x):
                    u=max(1-abs(x)/h,0);s=x-lag*h
                    row=(2*math.exp(-alpha*abs(s))-math.exp(-alpha*abs(s-h))-math.exp(-alpha*abs(s+h)))/(h*alpha**2)
                    return u*row
                reference=integrate.quad(integrand,-h,h,points=[0],epsabs=1e-13)[0]
                self.assertLess(abs(float(values[lag].lo)-reference),2e-12)

    def test_exact_kernel_folding_contraction(self):
        nodes=[[[1,2],[-1,4]],[[3,4],[1,8]]]
        kernel=[3,-2,1,0]
        result,den,trace=contract_even_kernel(nodes,kernel,8)
        # Folded 2x2 kernel is [[J0,2J1],[2J1,2(J0+J2)]].
        expected=np.array([[3.,-4.],[-4.,8.]])/8
        D=np.array([[.5,-.25],[.75,.125]])
        actual=np.array([[float(Fraction(int(x),den)) for x in row] for row in result])
        self.assertLess(np.max(np.abs(actual-D.T@expected@D)),1e-15)


if __name__=='__main__':unittest.main()
