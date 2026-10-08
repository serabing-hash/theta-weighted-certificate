# Review notes and exact cached-algebra verification

This supplements the frozen pre-execution PROOF.md without rewriting its
execution hash. The trial, operator, precision, theta/prime cutoffs and
resource policy were unchanged during the successful computation.

The far-Gamma estimate in section 5 can be read without its phrase about
an absorbed factor as follows. For |z|>=48 and |y-z|<=1, every point in
the Cauchy circle about y of radius 1/8 has real absolute part >=46.875.
The source majorant times the polynomial and exp(256) modulation factor is
less than exp(-2|z|), using
exp(2|z|-9/4)>=(2|z|-3)^4/24 and |z|>=48. Its logarithmic polynomial
factors are bounded by 16+2|z|. The resulting bound for the local second
derivative, combined with the distant convolution, is comfortably below
2^22 A_i exp(-|z|/2). Thus both physical images and the final constant in
the original proof are valid for the entire stated range; an endpoint
shift of 1+1/8 is not dropped.

The finite-source local term also uses an explicit safe inequality: on
[0,1], |a^(3/2)-a8^(3/2)| <=(3/2)|a-a8|. Since the source error is at most
2^-320, this is less than 2^-160. For a prime product,
sqrt(2^-321)+2^-321 <2^-160. These prove the two constants 30 and 2368
in equation (9), rather than adding two independent square-root bounds
with an incorrect factor.

## Exact coefficient algebra, separate from action execution

All 1,055,904 saved cosine coefficients were checked by a second arithmetic
route. Let the source coefficient midpoint and radius have denominator
2^140, as do the multiplier and phase inputs. The phase inputs are checked
from the frozen T using rational Machin pi bounds and integer square-root
enclosures at 180 bits. Their coefficients are the original cosine/sine
coefficients, with no rotation or normalization.

For r=0,2 the source and phase midpoint arrays are real and even. For r=1
both are imaginary and odd. Hence the finite real coefficient convolution
is exactly A0*P0 - A1*P1 + A2*P2. The verifier uses fmpz integer polynomial
products, with denominator 2^280, rather than native complex ball products.
After multiplying the midpoint multiplier, the denominator is 2^420. It
compares every positive cosine coefficient, including DC and all zero
midpoints, with the stored numerator at denominator 2^100.

Write E_A,r and N_A,r for source coefficient L1 radius and midpoint norm,
and E_P,r, N_P,r for the corresponding phase quantities. A valid input
uncertainty is

  E_h <= sum_r [E_A,r N_P,r +(N_A,r+E_A,r) E_P,r].

If M bounds all multiplier magnitudes and E_m bounds its radii, the full
Gamma coefficient error is at most

  exact_midpoint_discrepancy + M E_h
       + E_m sum_r N_A,r N_P,r.

This proves an outer L1 enclosure independently of the complex-convolution
rounding implementation. The FINAL_ACTION_CERTIFICATE files take the
outer maximum of this error and the native-run error before summing the
whole-line ledger. This small enlargement does not change any approximant
or require another H action, DFT, digamma evaluation or source integral.

The source DFT, the special-function primitive contracts, and the inherited
analytic source identities remain author-side first-key inputs. Integer
replay is not an independent external mathematical audit of those facts.
The fresh 224-bit scalar cross-check verifies the six analytic budget
endpoints against their frozen 160-bit enclosures; it does not repeat a
source transform or action.

## The implementation correction

The first pilot formed its caches and one Gamma polynomial but failed
while evaluating the stored polynomial at x=1/2 with rectangular complex
Horner arithmetic. That arithmetic accumulated exponentially large box
radii around a long unit-circle polynomial. Direct validated cosine
evaluation of the same coefficients removed this implementation loss.
No numerical-error gate was weakened. The complete failed code, descriptor,
exit record and counts are preserved. Its Gamma column was reconstructed
once because its aggregate coefficient-radius ledger had not yet been
saved. The second descriptor is byte-identical to the failed descriptor.
All eight transforms, moments and multipliers were reused. The repair
had a reduced 590-second cap after the 9.02-second failure, within the
same 600-second pilot budget. The 31-column main run was executed once.

The original handoff contains FLOAT diagnostic arrays and its old
run_diag.py. They are preserved only as provenance; none is a certification
input. The large optional FLOAT archive was not fetched or executed.

No full residual Gram, inverse, LDL, spectral matrix, trial search, or
spectral exclusion is part of this task.
