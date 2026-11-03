#!/usr/bin/env python3
"""Enclose only elementary theta constants; no theta matrix integration."""
from flint import arb,ctx
from pathlib import Path
import json
ctx.prec=160
pi=arb.pi();z=(-pi/2).exp()
W=42*(-pi).exp();assert W<2
c=pi.log()-(arb(1)/4).digamma()
d=2*c+84*z*z*(4/(1-z)+4*z/(1-z)**2+z*(1+z)/(1-z)**3)
assert d<36
m=33
r=84*z**m*(arb(m*m)/(1-z)+2*m*z/(1-z)**2+z*(1+z)/(1-z)**3)
assert r<arb(3609)/10**21
out={'status':'PASS','weight_sup_envelope':str(W),'full_correction_envelope':str(d),
 'prime_tail_32':str(r),'analytic_inputs':'The stated theta and weighted-shift envelopes.',
 'scope':'Elementary scalar bounds only; no actual low-frequency Schur entries.'}
Path(__file__).with_name('THETA_CONSTANTS.json').write_text(json.dumps(out,indent=2)+'\n')
for k,v in out.items():print(k,v)
