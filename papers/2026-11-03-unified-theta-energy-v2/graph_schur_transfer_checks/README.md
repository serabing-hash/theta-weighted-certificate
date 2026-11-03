# Graph to Schur transfer certificate

This certificate transfers the five-function bound q0[v] >= ||v||_H^2/25 to the projected source L5 = P_R V5 at the Gamma spectral cutoff R = 2^18. Under the stated closed-sector and operator-row admission hypotheses, it proves S_R >= 1/35 on L5 and q0 >= 1/36 on L5 plus the entire complementary Gamma high form domain. It does not certify the other low directions of P_R K, a cofinal family, the global one-half inequality, or RH.

The exact identity is S_R[P_R v] = q0[v] - <Q_R L_K v, C^-1 Q_R L_K v>. The residual is the complete high row, not a finite compression. The finite comparison D2 <= 2^20 G5 and a logarithmic Gamma multiplier bound imply ||L_K v||_H <= 52 ||v||_H on V5. All prime powers and both shift orientations are bounded together.

## Reproduce

Use Python with python-flint==0.9.0 for the first command. The remaining commands use only the standard library.

```
python3 verify_graph_bound.py
python3 check_rational_transfer.py
python3 independent_fraction_audit.py
```

The frozen inputs retain their original hash identities. Their mathematical G5 and D2 fields agree exactly with the separately replayed five-zero certificate; only its recorded elapsed time and the dependent input hash differ. No new theta integral, spectral projection, or high inverse is computed here. The accompanying five-zero certificate supplies the earlier positivity and analytic integral enclosures.

The two original scripts reproduce all three saved outputs byte-for-byte. The independent checker parses the printed balls as exact decimal-rational intervals, proves containment in all 25 exported matrix boxes, and verifies positive definiteness by determinant expansion rather than the supplied LDL recurrence. Its 67 exact checks also verify the final rational inequalities. All five determinant-ratio pivots exceed 14000.

The Schur transfer constant before rounding is 48627/1638175. The complete high-attachment constant before rounding is 613398247/21468939455. The normalized complete-high interaction bound is kappa = 9/65536, and the complete relative coupling coefficient on L5 is 2835/16384 < 1-kappa. These statements concern the same Gamma spectral split, not an unrelated zero-height or sparse-window split.

These are source review, ball-arithmetic replay, and independent exact finite rational checks. They are not proof-assistant formalization or an independent implementation of the prior theta integrals. Operator domains and membership in the chosen closed sector remain explicit analytic inputs.
