# First full rigorous-certificate attempt: complete, inconclusive

One bounded run completed normally on2026-10-25. All1104 fine sources,552 quotient coordinates,276 original moment blocks and60 fixed local integration templates were covered. No prior run was repeated.

## Result

The verified inertia conclusion is INCONCLUSIVE. The chosen center has floating second eigenvalue0.6306648326236484; its independently verified positive-subspace projected center lower bound is0.6306648312871473. However the complete operator-error upper bound is307403644829112.9, far larger than the margin. Therefore this run does NOT certify the desired second-sign condition and does NOT prove RH.

The error is almost entirely the conservative full residual quadrature remainder:
- Quadrature norm upper:307403644829112.3.
- Point/input/exactification upper:3.905813588595235e-05.
- BLAS/accumulation upper:6.666244603444821e-05.
- Theta tail upper:1.061062910358484e-101.
- Analytic endpoint tail upper:8.818341228369274e-17.

The full G certificate did succeed as an entry enclosure: its source-coordinate row-radius bound is0.009761389351295417, corrected congruence/input error0.011094162822154512 and BLAS error0.0004958726606849469. This is not sufficient alone for the Schur sign.

## Diagnosed obstruction in this enclosure

Largest remainder templates19 and58 contribute approximately1.53e14 each. The generic jet composition of log(exp(Lu^8)-1) loses interval dependence, and the separate norms of rU-VC and the metric term lose their large cancellation before residual squaring. This is failure of the current error enclosure, not evidence of a negative actual corrected matrix. The positive full-matrix numerical candidate remains unproved.

A new version must address BOTH issues: extract logL+8logu analytically with a regular endpoint jet, and combine the full finite-theta residual vector before taking its derivative norm. Merely repeating the run or increasing precision would not repair these structural overestimates.

## Resources and evidence

Wall399.960591s, final child-tree CPU399.192602s, observed aggregate live RSS peak142794752bytes. Normal exit, resource accounting complete. The precise polled/per-process guard scopes are in RUN_CONTRACT.md. All complete stage outputs, original input hashes, fixed source/binary hashes, H panel budgets, exact candidate bounds, G entry matrices, F center and independent inertia ledger are preserved. No automatic retry.

RH_PROOF=NOT_OBTAINED. A fixed R=1,epsilon=1/8 certificate would still require a separate global sequence argument even if later obtained.
