#!/usr/bin/env python3
"""Independent 256-bit elementary constants, using the quarter-digamma identity."""
from flint import arb, ctx
from pathlib import Path
import json
ctx.prec=256
pi=arb.pi(); z=(-pi/2).exp(); one=arb(1)
# psi(1/4)=-EulerGamma-pi/2-3 log2, independently of digamma evaluation.
c=arb.const_euler()+pi/2+(8*pi).log()
c_direct=pi.log()-(one/4).digamma()
assert (c-c_direct).contains(0)
all_n_square=z*(1+z)/(1-z)**3
head_bound=2*c+84*(all_n_square-z)
assert head_bound<36
assert 42*(-pi).exp()<2
# Shift n=33+j; geometric first two moments retain the entire integer tail.
start=33
tail=84*z**start*((start*start)/(1-z)+(2*start)*z/(1-z)**2+z*(1+z)/(1-z)**3)
assert tail<arb(3609)/10**21
g=arb(262108); d=arb(36); R=arb(262144)
schur=tail*(1+(d/g)**2)
assert schur<arb(361)/10**20
cubic=(d*d/g)*(d/R)**4
assert cubic<arb(176)/10**20
assert schur+cubic<arb(537)/10**20
out={'status':'PASS','precision_bits':ctx.prec,'quarter_digamma_identity_verified_by_overlapping_enclosures':True,
     'full_correction_bound':str(head_bound),'prime_tail32':str(tail),
     'prime_schur_bound':str(schur),'cubic_plus_prime_schur':str(schur+cubic),
     'scope':'Elementary analytic envelopes only; no theta quadrature, low matrix, projected moment, or positivity certificate.'}
Path(__file__).with_name('INDEPENDENT_SCALAR_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
