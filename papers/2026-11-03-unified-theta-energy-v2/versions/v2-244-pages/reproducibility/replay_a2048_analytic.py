#!/usr/bin/env python3
"""Independent rational-only a2048 analytic composition; no theta producer."""
from fractions import Fraction as F
from math import factorial
import json
if not __debug__: raise SystemExit("Run without Python -O.")
v = {}; checks = {}
def put(name, x): v[name] = x; return x
def pos(name, x): checks[name] = x; assert x > 0, name
r = put('r',F(27,512)); a = put('a',F(1,2048))
# Independently reconstruct the mathematical preflight, not execute its script.
A = put('A',64+F(73,21)*8+F(1,9)); assert A==F(5791,63)
M = put('M',42*64*r**8)
J2 = put('J2',168*A*A*r**8)
D = put('D',22*M+96*9**3*r**9)
P2 = put('P2',F(84*8**3,43)*r**8)
t0 = put('t0', F(256*3)*F(20,21)); assert t0==F(5120,7)
pos('exp_21over10_partial6_above_8',sum(F(21,10)**j/factorial(j) for j in range(7))-8)
pos('exp_7over10_partial4_above_2',sum(F(7,10)**j/factorial(j) for j in range(5))-2)
pos('exp_39over20_partial8_above_7',sum(F(39,20)**j/factorial(j) for j in range(9))-7)
pos('sqrt7_above_13over5_squared',F(7)-F(13,5)**2)
pos('e_partial4_above_8over3',sum(F(1,factorial(j)) for j in range(5))-F(8,3))
log2lower=2*(F(1,3)+F(1,3)**3/3); assert log2lower==F(56,81)
logratio_lower=2*F(80-63,80+63); assert logratio_lower==F(34,143)
assert 2*t0/9==128*F(80,63)
pos('first_gamma_term_above_399over100',4*t0*t0/(t0*t0+F(1,4))-F(399,100))
pos('second_gamma_term_above_79over100',F(4,5)*t0*t0/(t0*t0+F(25,4))-F(79,100))
primecap = put('prime_cap',F(3,2)*F(1,2)+F(16,25)+F(7,20)+F(29,40)+F(3,4))
assert primecap==F(643,200); pos('13over4_minus_prime_cap',F(13,4)-primecap)
hroot=put('root_hgamma',F(399,100)+F(79,100)+7*log2lower+logratio_lower-F(383,70)-F(13,4))
assert hroot==F(9209503,8108100)
hproducer=put('reported_short_hgamma',F(63521,56700))
# Independently reconstruct a valid shorter bound, without assuming its derivation.
pos('80over63_above_5over4',F(80,63)-F(5,4))
assert 2*F(5-4,5+4)==F(2,9)
assert hproducer==F(478,100)+F(392,81)+F(2,9)-F(383,70)-F(13,4)
h=put('selected_h',F(11,10))
pos('root_floor_minus_selected_h',hroot-h)
pos('root_floor_minus_reported_short_floor',hroot-hproducer)
pos('reported_short_floor_minus_selected_h',hproducer-h)
epsold=put('root_original_epsilon',D+P2+J2)
nuold=put('root_original_nu',a-epsold)
eps=put('epsilon',D+P2+J2/h); nu=put('nu',a-eps)
assert eps==F(20262735541658121715431,250172086796502324840759296)
assert nu==F(101891603714446529085721,250172086796502324840759296)
assert epsold-eps==nu-nuold==J2/11
put('epsilon_improvement_over_original',epsold-eps)
pos('epsilon_below_a_over5',a/5-eps)
pos('nu_above_4a_over5',nu-F(4,5)*a)
eta=put('eta_reference',D+P2+2*J2/h); pos('eta_below_a_over2',a/2-eta)
C=put('C_res',4/nu+5*a/nu**2)
Cold=put('C_res_root_original',4/nuold+5*a/nuold**2)
coarse=put('C_res_coarse',F(205,16)/a); assert coarse==26240
assert 4/(F(4,5)*a)+5*a/(F(4,5)*a)**2==coarse
pos('coarse_penalty_minus_exact',coarse-C)
pos('original_penalty_minus_exact',Cold-C)
step=put('step',a*nu/(a+4*nu)); b=put('b',a-step)
coef=put('energy_coefficient',F(1,2)-b)
assert coef==F(542006223062224701317434549,1084868104425248291110985728)
stepold=put('root_original_step',a*nuold/(a+4*nuold))
coefold=put('root_original_energy_coefficient',F(1,2)-a+stepold)
coarsestep=put('coarse_step',a*(F(4,5)*a)/(a+4*(F(4,5)*a)))
coarseb=put('coarse_b',a-coarsestep)
coarsecoef=put('coarse_energy_coefficient',F(1,2)-coarseb)
assert coarsestep==F(1,10752) and coarseb==F(17,43008) and coarsecoef==F(21487,43008)
pos('coefficient_above_original',coef-coefold)
pos('coefficient_above_coarse',coef-coarsecoef)
pos('remaining_half_bound_deficit',F(1,2)-coef)
assert step<min(a,nu)
eta_young=put('composition_young_parameter',a/(4*nu))
assert step*(1+eta_young)==a/4 and step*(1+1/eta_young)==nu
Fschur=put('schur_positive_F_factor',a*a/(4*(a+4*nu)))
nu_b=put('complement_at_b',nu-step)
assert step*nu/(nu-step)==a/4
assert step*step/(nu-step)==Fschur
assert nu_b==4*nu*nu/(a+4*nu)
pos('schur_F_positive',Fschur); pos('complement_at_b_positive',nu_b)
result={'status':'PASS: exact rational analytical composition only',
'values':{k:str(x) for k,x in v.items()},'positive_margins':{k:str(x) for k,x in checks.items()},
'actual_gate_status':'NOT CHECKED: actual a2048 response gate and full-domain premises are separate inputs',
'scope':'Arithmetic validation of the stated analytic-composition formulas; no actual-theta or raw numerical replay; no RH proof.'}
print(json.dumps(result,indent=2,sort_keys=True))
