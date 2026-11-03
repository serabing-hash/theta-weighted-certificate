"""Directed Decimal interval primitives and analytic tails. No global CERT claim.

Arithmetic uses separate ROUND_FLOOR/ROUND_CEILING contexts. Decimal elementary
functions are correctly rounded to nearest; one adjacent representable number
on each side encloses the result. No binary float is admitted as exact input.
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, localcontext, ROUND_FLOOR, ROUND_CEILING
from fractions import Fraction
import json
import math
from pathlib import Path

PRECISION=70


def directed(fn, upper):
    with localcontext() as ctx:
        ctx.prec=PRECISION
        ctx.rounding=ROUND_CEILING if upper else ROUND_FLOOR
        return fn()


def nonnegative_integer_power_bound(x, n, upper):
    """One-sided integer power using only correctly rounded multiplication.

    For x>=0 each product is monotone in both factors. Repeated squaring and
    multiplication in one directed mode therefore preserve a lower/upper bound
    by induction, including gradual underflow. Nonfinite results fail closed
    when constructing IV (or through Decimal's arithmetic traps).
    """
    if x < 0 or not isinstance(n, int) or n < 0:
        raise ValueError('Nonnegative base and integer exponent required')
    result = Decimal(1)
    factor = x
    while n:
        if n & 1:
            result = directed(lambda: result * factor, upper)
        n >>= 1
        if n:
            factor = directed(lambda: factor * factor, upper)
    return result


def integer_power_endpoint_bound(x, n, upper):
    """Sign-correct endpoint bound for a positive integer exponent."""
    magnitude = x.copy_abs()
    if x.is_signed() and n % 2:
        # Negation reverses inequalities; copy_negate is exact/context-free.
        return nonnegative_integer_power_bound(magnitude, n, not upper).copy_negate()
    return nonnegative_integer_power_bound(magnitude, n, upper)


def elementary(fn, x, upper):
    with localcontext() as ctx:
        ctx.prec=PRECISION
        result=fn(x)
        return result.next_plus() if upper else result.next_minus()


@dataclass(frozen=True)
class IV:
    lo: Decimal
    hi: Decimal

    def __init__(self,lo,hi=None):
        if isinstance(lo,IV):
            object.__setattr__(self,'lo',lo.lo);object.__setattr__(self,'hi',lo.hi);return
        if isinstance(lo,float) or isinstance(hi,float):
            raise TypeError('Use exact strings, integers or rational inputs; binary float is not exact')
        lo=Decimal(lo);hi=lo if hi is None else Decimal(hi)
        if not lo.is_finite() or not hi.is_finite() or lo>hi:raise ValueError('Invalid finite interval')
        object.__setattr__(self,'lo',lo);object.__setattr__(self,'hi',hi)

    @classmethod
    def rational(cls,n,d=1):return cls(n)/cls(d)
    def __add__(self,b):
        b=IV(b);return IV(directed(lambda:self.lo+b.lo,False),directed(lambda:self.hi+b.hi,True))
    __radd__=__add__
    def __neg__(self):return IV(self.hi.copy_negate(),self.lo.copy_negate())
    def __sub__(self,b):return self+-IV(b)
    def __rsub__(self,b):return IV(b)+-self
    def __mul__(self,b):
        b=IV(b)
        lows=[directed(lambda:x*y,False) for x in [self.lo,self.hi] for y in [b.lo,b.hi]]
        highs=[directed(lambda:x*y,True) for x in [self.lo,self.hi] for y in [b.lo,b.hi]]
        return IV(min(lows),max(highs))
    __rmul__=__mul__
    def reciprocal(self):
        if self.lo<=0<=self.hi:raise ZeroDivisionError('Interval contains zero')
        return IV(directed(lambda:Decimal(1)/self.hi,False),directed(lambda:Decimal(1)/self.lo,True))
    def __truediv__(self,b):return self*IV(b).reciprocal()
    def __rtruediv__(self,b):return IV(b)*self.reciprocal()
    def __pow__(self,n):
        if not isinstance(n,int):raise TypeError('Integer powers only')
        if n<0:return self.reciprocal()**(-n)
        if n==0:return IV(1)
        if n==1:return self
        if n%2==0 and self.lo<=0<=self.hi:
            top=max(self.lo.copy_abs(),self.hi.copy_abs())
            return IV(0,nonnegative_integer_power_bound(top,n,True))
        lows=[integer_power_endpoint_bound(x,n,False) for x in [self.lo,self.hi]]
        highs=[integer_power_endpoint_bound(x,n,True) for x in [self.lo,self.hi]]
        return IV(min(lows),max(highs))
    def exp(self):return IV(elementary(Decimal.exp,self.lo,False),elementary(Decimal.exp,self.hi,True))
    def log(self):
        if self.lo<=0:raise ValueError('log requires strictly positive input')
        return IV(elementary(Decimal.ln,self.lo,False),elementary(Decimal.ln,self.hi,True))
    def sqrt(self):
        if self.lo<0:raise ValueError('sqrt requires nonnegative input')
        low=Decimal(0) if self.lo==0 else elementary(Decimal.sqrt,self.lo,False)
        return IV(low,elementary(Decimal.sqrt,self.hi,True))
    def cosh(self):return (self.exp()+(-self).exp())/2
    def record(self):return {'lower':str(self.lo),'upper':str(self.hi)}


def atan_inverse(n, terms=120):
    # Alternating series at x=1/n with next-term enclosure. No stored pi digits.
    x=IV.rational(1,n)
    value=IV(0)
    for j in range(terms):value+=((-1)**j)*x**(2*j+1)/(2*j+1)
    remainder=x**(2*terms+1)/(2*terms+1)
    return value+IV(0,remainder.hi) if terms%2==0 else value+IV(remainder.hi.copy_negate(),0)


def pi_interval():
    # Machin identity, principal arctangents in (0,pi/2).
    return 16*atan_inverse(5)-4*atan_inverse(239)


def theta_interval(x,terms=8):
    x=IV(x)
    if x.lo<0:raise ValueError('Use evenness to provide a nonnegative interval')
    pi=pi_interval();tau=pi*(2*x).exp()
    pref=(x/2).exp()
    head=sum(((4*(tau*j*j)**2-6*tau*j*j)*(-tau*j*j).exp() for j in range(1,terms+1)),IV(0))*pref
    # Drop negative polynomial in the positive omitted theta terms; geometric
    # ratio is maximal at the first omitted index and minimal tau.
    j=terms+1
    ratio=IV.rational((j+1)**4,j**4)*(-tau*(2*j+1)).exp()
    if ratio.hi>=1:raise ValueError('Theta remainder geometric ratio not below one')
    tail=4*pref*tau**2*j**4*(-tau*j*j).exp()/(1-ratio)
    return head+IV(0,tail.hi),tail


def weight_interval(x,terms=8):
    x=IV(x);k,tail=theta_interval(x,terms)
    return k/(2*(x/2).cosh())


def gamma_label_bounds(J):
    if not isinstance(J,int) or J<1:raise ValueError('Positive integer label count required')
    al=Fraction(4*J+1,2)
    return {'energy_derivative_gram_multiplier':2/al**3+Fraction(1,2)/al**2,
            'row_derivative_norm_multiplier':1/al**2+Fraction(1,2)/al}


def gamma_potential_interval(d,J):
    d=IV(d)
    if d.lo<0:raise ValueError('Distance must be nonnegative')
    head=IV(0)
    for j in range(J):
        al=IV.rational(4*j+1,2)
        head+=(-al*d).exp()/al**2
    al=IV.rational(4*J+1,2)
    tail=(-al*d).exp()*(1/al**2+1/(2*al))
    return head+IV(0,tail.hi),tail


def spatial_residual_tail(length,radius,D_upper,alpha_upper):
    L=IV(length);R=IV(radius);D=IV(D_upper);ca=IV(alpha_upper);pi=pi_interval()
    if R.lo<=L.hi or D.lo<0 or ca.lo<0:raise ValueError('Invalid residual-tail domain')
    def ip(p):
        den=2*pi*(2*R).exp()-p
        if den.lo<=0:raise ValueError('Nonpositive tail denominator')
        return (p*R-pi*(2*R).exp()).exp()/den
    den=1-(-2*(R-L)).exp()
    if den.lo<=0:raise ValueError('Invalid Gamma separation')
    return 252*(4*L**2*D**2*L.exp()/den**2*ip(3)+D**2*(2*L).exp()*ip(6)+ca**2*ip(5))


def interval_ldl(matrix):
    n=len(matrix);L=[[IV(0) for _ in range(n)] for _ in range(n)];pivots=[]
    if any(len(row)!=n for row in matrix):raise ValueError('Expected square matrix')
    # An interval matrix must have symmetric enclosures, not independent
    # asymmetric input cells silently overwritten during verification.
    for i in range(n):
        for j in range(i):
            if IV(matrix[i][j])!=IV(matrix[j][i]):raise ValueError('Non-symmetric interval input')
    for i in range(n):
        L[i][i]=IV(1)
        p=IV(matrix[i][i])-sum((L[i][j]**2*pivots[j] for j in range(i)),IV(0))
        pivots.append(p)
        if p.lo<=0:return {'positive':False,'failed_pivot':i,'pivots':[p.record() for p in pivots]}
        for j in range(i+1,n):
            L[j][i]=(IV(matrix[j][i])-sum((L[j][k]*L[i][k]*pivots[k] for k in range(i)),IV(0)))/p
    return {'positive':True,'pivots':[p.record() for p in pivots]}


REQUIRED_COVERAGE=('exact_coordinate_map','trial_domain','T_lower','G_upper','F_lower',
                   'residual_head','residual_tail','roundoff','full_centering')


def gate(T,G,F,K,coverage):
    missing=[name for name in REQUIRED_COVERAGE if coverage.get(name) is not True]
    if missing:return {'status':'NOT_RUN','missing':missing,'scope':'actual weighted global256 gate'}
    n=len(T)
    from target import K as target_dimension
    if n!=target_dimension:raise ValueError('Wrong target dimension')
    if any(len(X)!=n or any(len(row)!=n for row in X) for X in [T,G,F,K]):raise ValueError('Dimension mismatch')
    from target import A,PENALTY
    a=IV.rational(A.numerator,A.denominator);penalty=IV.rational(PENALTY.numerator,PENALTY.denominator)
    H=[[4*IV(T[i][j])-5*a*IV(G[i][j])/4+a*IV(F[i][j])/4-penalty*IV(K[i][j]) for j in range(n)] for i in range(n)]
    test=interval_ldl(H)
    return {'status':'CERT' if test['positive'] else 'FAIL','scope':'finite sufficient gate CONDITIONAL on supplied coverage and analytic premises','ldl':test}


def scalar_report():
    from target import A,EPSILON,NU,PENALTY
    a=A;eps=EPSILON
    assert eps==EPSILON and a-eps==NU and 4*a/5<NU<a
    step=a*NU/(a+4*NU);b=a-step
    J=4096;gamma=gamma_label_bounds(J)
    # D<=1 and alpha<=2 are a scalar example only, not certified trial inputs.
    tail=spatial_residual_tail('1.2','2',1,2)
    points={str(x):weight_interval(x).record() for x in ['0','0.4','0.8','1.2','2']}
    report={'status':'CERT','scope':'scalar arithmetic and explicit analytic remainder formulas ONLY; not the global256 response',
            'precision_decimal_digits':PRECISION,'pi':pi_interval().record(),'epsilon256_new_radius':str(eps),
            'a':str(a),'complement_lower':str(NU),'stronger_than_2a_over_3':True,
            'residual_penalty':str(PENALTY),'b_conditional':str(b),'global_coefficient_conditional':str(Fraction(1,2)-b),
            'Gamma_J':J,'Gamma_tail_constants':{k:str(v) for k,v in gamma.items()},
            'weight_point_enclosures':points,
            'spatial_tail_example_with_assumed_D_le_1_alpha_le_2':tail.record(),
            'actual_global256_gate':gate([],[],[],[],{}),
            'trust_boundary':'Python Decimal correctly rounded operations, analytic theta envelope, Machin identity, geometric/integral comparisons; not a formal proof'}
    return report


if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',required=True);args=ap.parse_args()
    report=scalar_report();Path(args.output).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
