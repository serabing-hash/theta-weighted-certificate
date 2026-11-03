"""Directed enclosures of the COMPLETE P1 Gamma potential, including r=0.

Near zero, a logarithm is separated from a Bernoulli-polynomial power series.
Away from zero, a positive exponential series has an explicit full tail.
"""
from fractions import Fraction
from functools import lru_cache
import math
from interval_bounds import IV,pi_interval


@lru_cache(maxsize=1)
def constants():
    N=128
    differences=[Fraction(1,(2*j+1)**2) for j in range(N)]
    catalan=Fraction(0)
    for j in range(N):
        assert differences[0]>=0
        catalan+=differences[0]/(1<<(j+1))
        differences=[a-b for a,b in zip(differences,differences[1:])]
    G=IV.rational(catalan.numerator,catalan.denominator)+IV(0,IV.rational(1,1<<N).hi)
    pi=pi_interval();H0=pi*pi/4+2*G
    C=-IV.rational(1,2)-IV(2).log()-pi/4
    bern=[Fraction(1)]
    for n in range(1,65):
        bern.append(-sum(Fraction(math.comb(n+1,k))*bern[k] for k in range(n))/(n+1))
    coeff=[IV(0)]*66
    for n in range(1,65):
        bp=sum(Fraction(math.comb(n,k))*bern[k]*Fraction(3,4)**(n-k) for k in range(n+1))
        c=Fraction(1<<(n-1))*bp/Fraction(math.factorial(n)*n*(n+1))
        coeff[n+1]=IV.rational(c.numerator,c.denominator)
    return H0,C,coeff


def phi(distance):
    r=IV(distance)
    if r.lo<0:raise ValueError('Nonnegative distance required')
    H0,C,coeff=constants()
    if r.hi==0:return H0
    if r.lo==0:raise ValueError('Split an interval touching zero; exact zero is supported')
    if r.hi<=1:
        polynomial=IV(0)
        for c in reversed(coeff[2:]):polynomial=polynomial*r+c
        polynomial*=r*r
        value=H0+r*r.log()/2+C*r+polynomial
        # |coefficient of r^n in r*rho(r)|<=4/2^n by Cauchy on |z|=2.
        # Integrate twice. The omitted n>=65 terms have this geometric bound.
        tail=4*r*(r/2)**65/(65*66*(1-r/2))
        return value+IV(tail.hi.copy_negate(),tail.hi)
    z=(-2*r).exp();term=(-r/2).exp();value=IV(0)
    for j in range(32):
        alpha=IV.rational(4*j+1,2)
        value+=term/(alpha*alpha);term*=z
    alpha=IV.rational(129,2)
    tail=term*(1/alpha**2+1/(2*alpha))
    return value+IV(0,tail.hi)


def tlog(t):
    t=IV(t)
    if t.hi==0:return IV(0)
    if t.lo<=0:raise ValueError('Expected positive interval or exact zero')
    return t*t.log()
