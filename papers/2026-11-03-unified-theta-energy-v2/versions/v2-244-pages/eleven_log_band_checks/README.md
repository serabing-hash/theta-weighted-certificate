# Scalar checks for flexible anchors and growing theta bands

Run with Python 3.9 or later:

    python3 check_band_scalars.py

The program uses only the Python standard library. All proof-relevant arithmetic uses exact rational numbers. It checks the fixed eleven-logarithmic-band parameters, the endpoint counting correction, sparse-row exponents and constants, and a finite-dimensional counterexample to unrestricted adjacent assembly. It also computes outward rational enclosures for the descriptive width thresholds and selected asymptotic margins, using the Machin identity for pi, the positive atanh series for log 2, and integer-square-root bounds.

The output must report 25 checks passed. `scalar_checks.json` records the output from the accompanying version.

## Mathematical scope

The analytical statements concern the exact theta prime-Gamma form, with all prime powers and the full unbounded Gamma multiplier retained:

- The improved localization coefficient is log(2e), giving eventual positivity for a complete actual zero-jet band of width A log T whenever 0 < A < 2 pi^2 / log(2e).
- The fixed rational parameters theta = 99/100, delta = 1/100 and c = 11/20 give an eventual lower margin (log T)/100 in ordinary Lebesgue L2 on the full eleven-logarithmic band.
- Growing bands separated in the coordinate integral dT/(log T)^12 admit complete cross-row control. In particular, the earlier eight-logarithmic diagonal margin yields the sparse-family coefficient 1/2000.

These are analytic proof conclusions, not outputs certified by this scalar program. The program does not compute an actual theta matrix, evaluate an effective final height, reproduce the external exponential-sum or zero-counting proofs, or prove RH. It is independent of every response-stage interval-arithmetic pipeline.

## Primary inputs to the analytical proof

- T. Erdélyi, *Inequalities for exponential sums*, author manuscript, 8 November 2016, Lemmas 3.2, 3.4, 3.5 and Theorem 2.9.1: https://people.tamu.edu/~terdelyi/papers-online/sbornik150R.pdf
- E. Hasanalizade, Q. Shen and P.-J. Wong, *Counting zeros of the Riemann zeta function*, Theorem 1.1 and Table 2: https://arxiv.org/pdf/2107.06506
- NIST DLMF 25.16.1 and 25.16.3, the all-prime-power function and unconditional PNT: https://dlmf.nist.gov/25.16

Ordinary and reciprocal-theta weighted Grams are distinct. Arbitrary adjacent chains, a uniform weighted coercivity gap, the global half inequality and RH are not established.
