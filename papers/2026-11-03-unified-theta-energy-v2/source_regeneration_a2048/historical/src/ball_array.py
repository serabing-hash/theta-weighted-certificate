"""Binary64 array balls with explicit outward arithmetic/error bounds.

Basic +,-,*,/,sqrt are IEEE binary64; BLAS dot products use the conservative
standard gamma_(2k+2) bound, including the error of positive magnitude dots.
No transcendental library result is admitted without a separate interval.
"""
from fractions import Fraction
import numpy as np
from interval_bounds import IV

EPS=2.0**-52
TINY=np.nextafter(0.,1.)


def up(x):return np.nextafter(x,np.inf)
def ua(a,b):return up(np.asarray(a)+np.asarray(b))
def um(a,b):return up(np.asarray(a)*np.asarray(b))
def usum(a,axis=None):
    a=np.asarray(a);n=a.size if axis is None else a.shape[axis]
    value=np.sum(a,axis=axis)
    return ua(um(value,up(1/(1-(n+2)*EPS))),TINY*(n+2))
def norm_upper(a,axis=None):return up(np.sqrt(usum(um(np.abs(a),np.abs(a)),axis)))


def iv_pair(v):
    v=IV(v);lo=Fraction(v.lo);hi=Fraction(v.hi)
    mid=float((lo+hi)/2)
    error=max(abs(Fraction(mid)-lo),abs(Fraction(mid)-hi))
    return mid,float(np.nextafter(float(error),np.inf))


def fraction_pair(v):
    v=Fraction(v);mid=float(v);error=abs(Fraction(mid)-v)
    return mid,float(np.nextafter(float(error),np.inf))


def positive_dot_upper(a,b):
    a=np.asarray(a);b=np.asarray(b);k=a.shape[-1]
    v=a@b
    if not np.isfinite(v).all():raise ArithmeticError('Nonfinite dot product')
    factor=up(1/(1-(2*k+2)*EPS))
    return ua(um(v,factor),TINY*(2*k+2))


class Ball:
    __array_priority__=1000
    def __init__(self,mid,rad=0.):
        self.mid=np.asarray(mid,dtype=np.float64);self.rad=np.broadcast_to(np.asarray(rad,dtype=np.float64),self.mid.shape)
        if np.any(self.rad<0) or not np.isfinite(self.mid).all() or not np.isfinite(self.rad).all():raise ValueError('Invalid ball')
    @classmethod
    def iv(cls,v):return cls(*iv_pair(v))
    @classmethod
    def fraction(cls,v):return cls(*fraction_pair(v))
    def __getitem__(self,key):return Ball(self.mid[key],self.rad[key])
    def __neg__(self):return Ball(-self.mid,self.rad)
    def __add__(self,b):
        b=b if isinstance(b,Ball) else Ball(b)
        mid=self.mid+b.mid
        return Ball(mid,ua(ua(self.rad,b.rad),ua(um(EPS,np.abs(mid)),TINY)))
    __radd__=__add__
    def __sub__(self,b):return self+-b if isinstance(b,Ball) else self+Ball(-b)
    def __rsub__(self,b):return Ball(b)+-self
    def __mul__(self,b):
        b=b if isinstance(b,Ball) else Ball(b)
        mid=self.mid*b.mid
        rad=ua(ua(um(np.abs(self.mid),b.rad),um(np.abs(b.mid),self.rad)),um(self.rad,b.rad))
        return Ball(mid,ua(rad,ua(um(EPS,np.abs(mid)),TINY)))
    __rmul__=__mul__
    def __truediv__(self,b):
        b=b if isinstance(b,Ball) else Ball(b)
        lower=np.nextafter(np.abs(b.mid)-b.rad,-np.inf)
        denominator=np.nextafter(np.abs(b.mid)*lower,-np.inf)
        if np.any(denominator<=0):raise ZeroDivisionError('Ball denominator contains zero')
        mid=self.mid/b.mid
        num=ua(um(self.rad,np.abs(b.mid)),um(np.abs(self.mid),b.rad))
        rad=up(num/denominator)
        return Ball(mid,ua(rad,ua(um(EPS,np.abs(mid)),TINY)))
    def __rtruediv__(self,b):return Ball(b)/self
    def __matmul__(self,b):
        b=b if isinstance(b,Ball) else Ball(b)
        k=self.mid.shape[-1];mid=self.mid@b.mid
        mag=positive_dot_upper(np.abs(self.mid),np.abs(b.mid))
        roundoff=ua(um(up((2*k+2)*EPS/(1-(2*k+2)*EPS)),mag),TINY*(2*k+2))
        rad=ua(ua(positive_dot_upper(self.rad,np.abs(b.mid)),positive_dot_upper(np.abs(self.mid),b.rad)),positive_dot_upper(self.rad,b.rad))
        return Ball(mid,ua(rad,roundoff))
    @property
    def T(self):return Ball(self.mid.T,self.rad.T)
    def reshape(self,*shape):return Ball(self.mid.reshape(*shape),self.rad.reshape(*shape))


def pairs_ball(pairs):
    data=np.asarray(pairs,dtype=float)
    return Ball(data[...,0],data[...,1])
