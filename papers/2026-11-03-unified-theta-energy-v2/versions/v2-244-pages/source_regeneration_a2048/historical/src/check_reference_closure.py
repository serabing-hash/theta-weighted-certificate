"""Exact new-radius reference comparison, with no numerical response claim."""
from fractions import Fraction as F
from pathlib import Path
import json
from target import A,EPSILON,NU
r=F(27,512);J2=168*F(5791,63)**2*r**8
D=22*42*64*r**8+96*9**3*r**9;P2=F(84*8**3,43)*r**8
eta=D+P2+F(20,11)*J2
assert D+P2+F(10,11)*J2==EPSILON and NU==A-EPSILON
assert A/2-eta>0
result={'status':'PASS_EXACT_ARITHMETIC','target':{'a':str(A),'B':'log(8)/2','k':256},'Young_theta':'1/2','eta':str(eta),'positive_margin_a_over_2_minus_eta':str(A/2-eta),'comparison':'P_a/2 <= ell_a <= 3P_a/2 on the SAME constrained Z','inherited_premises':'R20 closed reference form on minimum/full domain; absolute source/exterior/mean bounds','actual_gate':'NOT_RUN_BY_THIS_CHECK'}
Path('inputs/reference_closure_checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
