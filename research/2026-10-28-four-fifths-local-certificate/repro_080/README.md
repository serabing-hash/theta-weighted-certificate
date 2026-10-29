# Exact rational replay at B = 4/5

This package verifies a **local** lower bound of `10^-22` in ordinary L2 for the real-even minimum local Gamma-form domain, conditional on the analytic source correspondence and the saved interval enclosures. It does not prove the Riemann hypothesis or positivity at all radii.

Run from this directory using Python 3.11 or newer, without `-O`:

```
python -I -B verify_exact.py --data-dir data --output result.json
```

Only Python's standard library is used. No numerical producer, FLINT, digamma evaluation, prime-source regeneration, parameter search, installation, or network access occurs. Inputs are hash bound. The result also records its checker's SHA-256.

## Independent finite checks

1. Reconstruct the full low matrix's off-diagonal entries from its first row and the exact rank-two displacement identity; use direct diagonal enclosures. Positive square roots are enclosed independently with `isqrt` at 80 fixed decimal places.
2. Reconstruct the complete coupling bound C0 from Cfinite plus the signed vector tail and diagonal remainder. The infinite high tail is retained.
3. Reconstruct M = Btrial + 54 Theta + G. Take a symmetric rational inverse witness X. Bound the exact interval residual I-MX by r, using both absolute row and column sums, and require r<1. Then `delta=||X|| r/(1-r)` bounds the inverse error in operator norm. Analytic positivity of M yields `M^-1 >= X-delta I`.
4. Reconstruct a lower comparison `F=A-C0+Z*XZ-delta||Z||_F^2 I`. All saved tables are compared through endpoint containment / enclosure hulls rather than equality of rounded records.
5. Compute an exact residual against a rational LDL witness and an exact triangular inverse. Derive `mu=min(D)/||L^-1||_F^2-residual>0`.
6. With kappa=8/5 and tau bounding the **complete uncorrected** trace C0, verify `min(mu*kappa/(kappa+2*tau),kappa/2)>=10^-22`.

Interval operations are exact rational operations followed, at specified matrix boundaries, by outward rounding to a fixed 240-bit dyadic grid. This is certified enclosure arithmetic, not floating-point arithmetic. The grid and all dimensions are fixed; no automatic retuning is performed.

## Analytic premises and limits

The finite replay inherits the original special-function interval enclosures, the full-form source identities and normalization, the signed-tail bound, the positive resource compression inequality, high floor kappa=8/5, and extension to the minimum form domain. It independently checks finite algebra, not these analytic premises. The source audit and analytic contracts must accompany a full mathematical claim.

The diagnostic's NOT_CERTIFICATE status is intentional: it is the complete pre-gate matrix record. The separately bound success record contains the producer's witnesses. Neither its printed positive margin nor printed gap is used as proof of this replay's positive margin.

The frozen checker was executed once from a clean portable staging copy on 28 October 2026. It returned `PASS_EXACT_FRACTION_RECONSTRUCTED_SCHUR_CERTIFICATE`. The independently reconstructed gap is approximately `1.4459835891599245e-22`; the exact rational value and input/checker hashes are recorded in `result.json`. The public checker and numerical inputs were unchanged during execution. This is computational certificate replay with analytic premises, not independent human peer review or formal proof-assistant verification.
