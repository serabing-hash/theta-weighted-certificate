#!/usr/bin/env python3
"""Reproducibility checks for growing_zero_jet_bands.tex.

Exact rational checks verify the listed scalar algebra, repeated-root
orthogonality and generic determinant identity. Numeric complex-root checks
are illustrations only. Neither replaces the analytic proof or constitutes
formal verification of the band theorem. Python standard library only.
"""
from __future__ import annotations
from fractions import Fraction as F
from math import factorial, comb, sqrt, log, exp, pi
import cmath
import json
from pathlib import Path

checks = []
def exact(name, condition, detail):
    assert condition, name
    checks.append({"name": name, "type": "exact", "passed": True, "detail": detail})

# Elementary e and pi comparison constants used in the whole-ray proof.
e_lower = sum((F(1, factorial(k)) for k in range(4)), F(0))
e_upper = sum((F(1, factorial(k)) for k in range(5)), F(0)) + F(1,100)
exact("elementary e brackets", e_lower>F(5,2) and e_upper<F(11,4),
      "sum through degree 3 is >5/2; sum through degree 4 plus geometric tail 1/100 is <11/4")
exact("log N above 8 for N at least 4096", F(11,4)**2<8 and 8**4==4096,
      "e^2<8 implies e^8<4096")
exact("theta upper constant C4", F(4)*F(22,7)**2*F(17,16)==F(2057,49) and F(2057,49)<42,
      "4(22/7)^2(17/16)=2057/49<42")
exact("theta derivative constant C6", F(21)*F(22,7)**3*F(5,4)<1000,
      "21(22/7)^3(5/4)<1000")
exact("theta logarithmic derivative cap", F(1000,9)<112,
      "C6/cW<1000/9<112")
exact("theta C4 tail ratio", F(3,2)**4/F(2)**15<F(1,2),
      "(3/2)^4 e^-15 < (3/2)^4 2^-15 <1/2")
exact("theta C6 tail ratio", F(3,2)**6/F(2)**15<F(1,2),
      "(3/2)^6 e^-15 < (3/2)^6 2^-15 <1/2")
exact("theta derivative polynomial", F(8)+F(32,3)+F(18,9)<21,
      "(8tau^3+32tau^2+18tau)/tau^3<21 for tau>3")
exact("pointwise negative coefficient", 6*(1-F(4,25))>5,
      "2pi(1-e^-2)>6(1-4/25)>5")
exact("prefactor logarithm less than 18", F(5,2)**9>3300,
      "log25+9+log132=9+log3300<18 since e>5/2")
exact("sqrt coefficient 33", 16*66<33**2,
      "4sqrt66<33")
exact("whole ray prefactor ratio decreases", F(1,17)+F(1,16)-1<0,
      "log derivative at s>=8 is 1/(s+9)+1/(2s)-1<0")
exact("whole ray prefactor initial value", F(34*3,2**8)<3,
      "(18+16)sqrt8/e^8 <34*3/2^8<3")
exact("whole ray absorption", F(36,100)<=1,
      "36N/sqrt(s)-5v<=-4v when v>=100N/sqrt(s)")
exact("complete paired prime tail", 8*F(1,2)**4/(1-F(1,2)**2)<1,
      "8 sum_{n>Y}e^-2n<1 for every Y>=1, using e>2")
exact("local derivative constant", F(41,2)**2*20<100**2,
      "(41sqrt20/2)<100")
exact("adaptive derivative exponent", (224+8+4)//2==118 and (224+8+4)%2==0,
      "e224 times e8 times e4 yields squared factor e236 and norm factor e118")
exact("boundary coefficient identity", F(14400,7200*2)==1,
      "[120sqrt(d)/(2^(3/4)sqrt(pi))]^2=1 at d=pi sqrt2/7200")

# Exact repeated-root Takenaka-Malmquist example, b=2 and zeta=2+3i.
# phi_j(t)=2 exp(-(2+3i)t) L_{j-1}(4t), j=1,...,6.
polys = [[F(2)*(-1)**k*comb(j,k)*F(4)**k/F(factorial(k)) for k in range(j+1)]
         for j in range(6)]
def inner_poly(p,q):
    return sum((a*b*F(factorial(i+j), 4**(i+j+1))
                for i,a in enumerate(p) for j,b in enumerate(q)), F(0))
for i,p in enumerate(polys):
    for j,q in enumerate(polys):
        exact(f"repeated-root Gram {i+1},{j+1}", inner_poly(p,q)==int(i==j),
              "Exact polynomial integral with weight exp(-4t), zeta=2+3i")
    derivative_real = (p[1] if len(p)>1 else 0) - 2*p[0]
    derivative_imag = -3*p[0]
    exact(f"repeated-root endpoint {i+1}",
          p[0]==2 and derivative_real==-2*(2+4*i) and derivative_imag==-6,
          "phi_j(0)=2 and phi_j'(0)=-(zeta+4(j-1))*2")

# Generic 2 by 2 determinant identity as an exact polynomial in eight variables.
zero = (0,)*8
one = {zero:F(1)}
def var(i):
    t=list(zero);t[i]=1;return {tuple(t):F(1)}
def add(*ps):
    out={}
    for p in ps:
        for m,c in p.items():out[m]=out.get(m,F(0))+c
    return {m:c for m,c in out.items() if c}
def neg(p):return {m:-c for m,c in p.items()}
def mul(p,q):
    out={}
    for m,c in p.items():
        for n,d in q.items():
            k=tuple(a+b for a,b in zip(m,n));out[k]=out.get(k,F(0))+c*d
    return {m:c for m,c in out.items() if c}
a,b,c,d,e,f,g,h=[var(i) for i in range(8)]
detH=add(mul(a,d),neg(mul(b,c)))
detF=add(mul(e,h),neg(mul(f,g)))
detHF=add(mul(add(a,e),add(d,h)),neg(mul(add(b,f),add(c,g))))
trace=add(mul(d,e),neg(mul(b,g)),neg(mul(c,f)),mul(a,h))
exact("generic determinant identity", add(detHF,neg(detH),neg(trace),neg(detF))=={},
      "det(H+F)=det(H)+tr(adj(H)F)+det(F) as an exact polynomial identity")

# Distinct complex roots, floating point illustration (not an enclosure).
roots=[complex(2,3), complex(3,-2), complex(1,7), complex(4,1)]
functions=[]
for j,z in enumerate(roots):
    coeff={j:complex(sqrt(2*z.real))}
    for i in reversed(range(j)):
        zz=roots[i];new={}
        for k,v in coeff.items():
            assert k!=i
            factor=2*zz.real/(zz-roots[k])
            new[k]=new.get(k,0)+v*(1-factor)
            new[i]=new.get(i,0)+v*factor
        coeff=new
    functions.append(coeff)
def ip_exp(p,q):
    return sum(v*w.conjugate()/(roots[i]+roots[j].conjugate())
               for i,v in p.items() for j,w in q.items())
gram_error=max(abs(ip_exp(p,q)-int(i==j))
               for i,p in enumerate(functions) for j,q in enumerate(functions))
endpoint_error=0.
for j,p in enumerate(functions):
    expect=-(roots[j]+2*sum(z.real for z in roots[:j]))*sqrt(2*roots[j].real)
    actual=-sum(roots[k]*v for k,v in p.items())
    endpoint_error=max(endpoint_error,abs(actual-expect))
assert gram_error<1e-11 and endpoint_error<1e-11
checks.append({"name":"distinct complex Volterra illustration", "type":"floating point illustration", "passed":True,
               "max_Gram_error":gram_error,"max_endpoint_error":endpoint_error})

# Numerical samples of the scalar whole-ray majorant. Proof is in the text.
rows=[]
for N in (4096,8192,10**6,10**12):
    s=log(N);M=100*N/sqrt(s)
    for multiple in (1,2,10):
        v=multiple*M;r=log(v)/2;Cr=8*N/(r-1)+2
        log_majorant=log(25)+9+log(2*N*Cr)+4*sqrt(N*Cr)-2*pi*(1-exp(-2))*v
        slack=-4*v-log_majorant
        assert slack>0
        rows.append({"N":N,"cutoff_multiple":multiple,"logarithmic_slack":slack})
checks.append({"name":"whole ray sampled majorant", "type":"floating point illustration", "passed":True,"samples":rows})

result={"status":"PASS", "scope":"Exact scalar and algebraic checks plus labelled floating point illustrations; not formal verification or a new numerical sign certificate.",
        "exact_checks":sum(x["type"]=="exact" for x in checks), "checks":checks,
        "boundary_d_approx":pi*sqrt(2)/7200}
print(json.dumps(result,indent=2))
