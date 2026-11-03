"""Exact rational witnesses for the independently reconstructed N=8 preflight."""
from fractions import Fraction as F
from math import factorial
from pathlib import Path
import json
from target import A, EPSILON, NU, PENALTY

def main():
    checks={}
    def check(name,lhs,rhs):
        assert lhs>rhs,name
        checks[name]={'left':str(lhs),'right':str(rhs),'positive_margin':str(lhs-rhs)}
    check('exp_21_over_10_positive_Taylor_lower',sum(F(21,10)**j/factorial(j) for j in range(13)),F(8))
    check('exp_39_over_20_positive_Taylor_lower',sum(F(39,20)**j/factorial(j) for j in range(17)),F(7))
    check('sqrt7_lower_squared',F(7),F(13,5)**2)
    t=F(5120,7)
    check('Gamma_first_label',4*t*t/(t*t+F(1,4)),F(399,100))
    check('Gamma_second_label',F(4,5)*t*t/(t*t+F(25,4)),F(79,100))
    check('log_tail_argument',2*t/9,F(160))
    gap=F(399,100)+F(79,100)+F(392,81)+F(2,9)-F(383,70)-F(13,4)
    check('local_gap',gap,F(11,10))
    check('local_prime_cap',F(13,4),F(493,200)+F(3,4))
    r=F(27,512);poly=64+8*(F(22,7)+F(1,3))+F(1,9)
    assert poly==F(5791,63)
    J2=168*poly**2*r**8
    D=22*42*64*r**8+96*9**3*r**9
    P2=F(84*8**3,43)*r**8
    eps=D+P2+F(10,11)*J2
    assert eps==EPSILON and NU==A-eps and PENALTY==4/NU+5*A/NU**2
    check('nu_gt_four_fifths_a',NU,4*A/5)
    check('conservative_penalty',F(26240),PENALTY)
    h=A*NU/(A+4*NU);b=A-h;eta=A/(4*NU)
    assert h*(1+eta)==A/4 and h*(1+1/eta)==NU
    out={'status':'PASS_EXACT_ARITHMETIC','analytic_formulas':'PREFLIGHT_RECOMPOSITION.md; inherited R20 premises remain explicit','checks':checks,'epsilon':str(eps),'nu':str(NU),'penalty':str(PENALTY),'hstep':str(h),'b':str(b),'conditional_coefficient':str(F(1,2)-b),'coefficient_float_DIAG':float(F(1,2)-b),'actual_gate':'NOT_RUN'}
    Path('inputs/exact_preflight_checks.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
