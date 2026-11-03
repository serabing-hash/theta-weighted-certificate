# Five zero theta certificate

This reproducible finite-space certificate proves q0[v] >= ||v||_H^2/25 on the span of the first five actual functions W(x) cos(gamma_j x). It preserves the full second-derivative Gram in the Gamma interpolation error, includes both prime orientations and the entire prime tail, and treats the zero mean analytically.

The shifted exact Schur complement in the fifth coefficient is greater than 1/2000. Its normalized quotient-direction reserve exceeds 27/1000. Neither value is an eigenvalue increment to add to 1/25. The negative scalar-debit comparison concerns a sufficient lower matrix, not a negative exact direction. No all-dimension positivity, global one-half bound, or RH conclusion is asserted.

## Reproduce

Use Python with python-flint==0.9.0. The checked wheel uses FLINT 3.6.0.

```
python3 certify_five_zeros.py
python3 certify_matrix_error.py
python3 export_rational_matrix.py
python3 check_rational_matrix.py
python3 independent_fraction_audit.py
```

The first stage verifies the SHA256 identity of INPUT4_CERTIFICATE.json. To regenerate the four-function input independently, run `python3 regenerate_input4.py`; outputs go to regenerated_input4. Compare all mathematical fields with INPUT4_CERTIFICATE.json, ignoring elapsed_seconds. Do not replace the hash-fixed input casually.

The standard-library checker verifies only the exported interval matrix sign. independent_fraction_audit.py separately checks exact determinants, normalized Schur bounds, scalar-comparison failure, and K5 squared <75 using Fraction arithmetic. Neither replaces the analytic error proof. To check live Arb serialization as well, run `python3 audit_live_serialization.py`, then rerun the independent fraction audit.

## Reproduction results

All five original stages passed under a 500 MiB memory cap, with peak RSS below 40 MiB. Fresh four-function regeneration reproduced every mathematical input field. The five-function quadrature checkpoint and rational ledgers were byte-identical to the supplied outputs. Both five-function stages also passed at 256 bits using the original certified four-function block and produced the same rational matrix. The four-function calculation has its own complete 256-bit replay.

All 225 live matrix entries survive printed-ball serialization, and all 25 final rational boxes enclose both live and parsed balls. A separate exact determinant implementation yields Schur >0.000528, normalized reserve >0.027, and scalar-comparison Schur <-0.000949. K5 squared is below 75; the four-function bound below 32 is not reused for V5.

These are source review, exact finite rational verification and reproducible ball-arithmetic checks, not proof-assistant formalization or an independent implementation of every analytic integral.
