#!/usr/bin/env python3
"""Exact scalar arithmetic only; no analytic source or spectral evaluation."""
from fractions import Fraction as F
import json
from pathlib import Path
checks = {}
def check(name, truth, expression):
    assert truth, name
    checks[name] = {"passed": True, "expression": expression}
check("upper_root_polynomial", F(27,20)**2-F(75,76)*F(27,20)-F(49,100)==F(1,3800), "(27/20)^2-(75/76)(27/20)-49/100=1/3800")
check("lower_root_polynomial", F(25,16)-F(95,84)-F(4,9)==-F(13,1008), "25/16-95/84-4/9=-13/1008")
check("middle_killing", F(5,4)-F(1,2)-F(121,190)==F(43,380), "5/4-1/2-121/190=43/380")
check("defect_gap", F(15,7)+7+F(1900,43)==F(16052,301) and F(16052,301)<54, "15/7+7+1900/43=16052/301<54")
check("sqrt_two_bound", F(10,7)**2>2, "(10/7)^2>2")
check("feature_tail", F(288,16383)<F(4,225), "288/16383<4/225")
check("feature_energy", (F(10,7)+F(2,15))**2==F(26896,11025) and F(26896,11025)<F(5,2), "(10/7+2/15)^2=26896/11025<5/2")
check("woodbury_coefficient", 1/(F(5,2)+F(5,8))==F(8,25), "1/(5/2+5/8)=8/25")
check("inverse_coefficient", 1/(1+F(27,10)/F(8,5))==F(16,43), "1/(1+(27/10)/(8/5))=16/43")
check("alternative_gap_coefficient", F(16,43)/54==F(8,1161), "(16/43)/54=8/1161")
check("high_floor", F(112,27)-F(11,10)-F(2,25)-F(7,32768)-F(27,20)>F(8,5), "112/27-11/10-2/25-7/32768-27/20>8/5")
check("tail_floor", F(280,27)-F(11,10)-F(2,25)-F(7,32768)-F(27,20)>F(39,5), "280/27-11/10-2/25-7/32768-27/20>39/5")
result = {"status":"PASS", "arithmetic":"Python standard-library Fraction; exact rational operations", "scope":"Only displayed scalar algebra. Does not verify analytic identities, domains, infinite tails, Schur matrix entries, nonzero zeta, or RH.", "checks":checks}
Path(__file__).with_name("constants_check.json").write_text(json.dumps(result, indent=2)+"\n")
print("PASS:",len(checks),"exact scalar checks; no source or matrix calculation")
