# Four-zero low-space certificate coverage

## Mathematical result

Section 13 integrates a separate finite certificate for the actual space spanned by the theta weight times cosines at the first four positive zeta-zero ordinates. It proves the unshifted complete-form lower bound `q0[v] >= ||v||_H^2 / 32`, using the true reciprocal-theta Gram, and certifies `K_V^2 < 32`. The mean is exactly zero by the theta Fourier identity, not a numerical tolerance.

This low space has the finite global exponential-polynomial representation required by the preceding low-to-sparse theorem. It is distinct from the sharp-cut cosine sources, piecewise-linear trial functions and response images used in the large response gates. The new positive margin cannot be added to an unrelated global energy coefficient.

| Integrated component | Main labels | Coverage and limitations |
|---|---|---|
| Four actual zero functions and finite low margin | `fz:thm:finite`, `fz:eq:main` | Exact ordinate balls, simple first four zeros, all complex coefficient combinations; no global RH assumption. |
| Complete theta and physical tails | `fz:eq:envelope`, `fz:eq:theta-omission`, `fz:eq:spatial` | Full weight and first two derivatives, omitted theta terms, two-sided spatial tails and actual physical integrals. |
| All prime powers | `fz:eq:prime-tail` | Exact head through 32, both orientations, complete remaining tail charged against the actual weighted Gram. |
| Complete Gamma interpolation error | `fz:eq:jensen`, `fz:eq:interp`, `fz:eq:debit` | Full Gamma energy controls the smooth-to-P1 error; endpoint ramps and exterior tails are paid. The omitted Gamma labels are nonnegative, not set equal to zero. |
| Sufficient matrix and exact acceptance | `fz:eq:certificate`, `fz:eq:pivots` | All 16 outward rational entry boxes, lowered-midpoint row debit, exact positive pivots; independent Bareiss leading-minor check agrees. Coordinate pivots are not weighted eigenvalues. |
| Weighted low coupling | `fz:eq:KV`, `fz:eq:gram-coords` | Actual inverse-Gram diagonal and full ordinary norm of the weight. |
| Explicit sparse recipe | `fz:hyp:sparse` | Total paired budget at most eight times log height, fixed prefix lists, complete mixed-form estimate and explicit recipe retained as analytical premises. |
| Conditional sparse attachment | `fz:thm:attachment`, `fz:eq:response`, `fz:eq:attached` | Exact finite Schur margin 3/128 of the low Gram and retained-energy bound with low coefficient 1/64, above the explicit height exp(2^512). |
| Infinite passage | `fz:thm:attachment` | Fixed actual form-convergent series and the specified form closure; no bounded inverse in the Hilbert norm or convergence of arbitrary abstract coefficient sequences. |

The budget coefficient 8 does not automatically cover every full actual unit-window zero-jet space. The earlier crude all-jet counting corollary uses coefficient 168. Actual zero jets in this attachment must meet its stated paired budget. Zeros five onward below the threshold, unselected high windows and growing-low-space conditioning remain outside the result.

## Verification scope

The complete source computation was reviewed and replayed with Python-FLINT 0.9.0 / FLINT 3.6.0. The finite-integral checkpoint, exported rational sufficient matrix, Fraction sign result and sparse scalar ledger reproduced. A higher-precision run produced the same rational boxes. A live-ball serialization check verified all sixteen entries against the exported boxes. An additional integer Bareiss calculation checked all four leading principal minors and the rational pivot floors.

The finite result has a proof of the complete error budget and depends on trusted Arb/Acb arithmetic and rigorous integration. Same-code replay is not a second complete implementation or formal proof. The sparse scalar checks instantiate the displayed recipe; they do not independently prove its analytical hypotheses. This computation uses no Decimal interval primitive or source matrix from the separate large response gates and does not validate those gates' arithmetic premises.

## Source identity and integration

The preserved mathematical input `four_zero_certificate.tex` has SHA-256 `f9eeda40d8fb8a4bcdc178febd1d60628aaf3eb89ef24c87a7653d4215f32c62`. Its proof content is internal to the monograph, not cited as an earlier author manuscript.

The reviewed body fragment has SHA-256 `5e67c4ad4b63c0fa4615fa5e506ca995939fc3950c6f67df98736703a8dfe295`. The integrated fragment has SHA-256 `14e29eecadd426a1b665abbbf6be793a177cb40c93280526604ffc5f55dd0ce3`. Their only difference is a local column-spacing wrapper around the large integer matrix; no entry, premise, proof sentence or conclusion changed. All 31 integration checks pass. The public computational companion has its own manifest and reproduction instructions.
