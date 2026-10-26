# Fixed full-matrix certificate: composite point patch

## Result
The bounded run completed all 104 scheduled point evaluations and the independently verified 551-dimensional positive trial-space test passed.

- Certified total Loewner error: 0.010363584147761682.
- Verified projected-center Gershgorin lower bound: 0.039958390743906419.
- Verified positive-subspace margin after all supplied error: 0.029594806595937249 > 0.
- Trial Gram defect upper: 2.002022214443372e-11; all 551 trial columns proved independent.
- Center SHA256: `1eacf4ca8d76c1efa88c581f589f2773b7232c499859649f9a6c22506998bb21`.

This is a full 552-coordinate fixed-candidate certificate, not a two-direction or truncated-cross-term test. The inertia helper labels its output conditional on the input Loewner bound; the surrounding integration pipeline supplies that bound via the recorded error ledger and audited reused certificates. The sufficient lower matrix has a strictly positive codimension-one restriction, hence its second ordered eigenvalue is positive. Coordinates are the invertible dyadic D congruence; its numerical eigenvalues are not original physical-operator eigenvalues.

Scope remains R=1, epsilon=1/8, the frozen fine-space correction and original 276-cell moment constraints. It does not establish the entire RH reduction or required parameter family/uniform limit. RH_PROOF remains NOT_OBTAINED. The first eigenvalue shown by floating eigensolvers is diagnostic only; this run certifies the positive codimension-one restriction, not a separate negative eigenvalue claim.

## Error budget
The exact-rational refinement plan changed 16 parent panels into 88 children, retaining 42 parents: 130 total smooth composite panels. The patch subtracts 16 old and adds 88 new point functionals (104 evaluations). Composite quadrature error is at most 0.007439640037244322. Reused nonquadrature error is 0.0029239393607924775. New patch point/rounding error is 4.7497174099096349e-09; tiny coefficient-radius repair and final subtraction/symmetry bounds are separately itemized in error_ledger.json. No empirical quadrature difference enters the certificate.

## Execution and readback
One launch, zero retries, exit code 0; wall 505.435459s; child-tree CPU 504.018698s; observed live-tree RSS peak 173965312 bytes. Full coverage 104/104, input 14/14 hashes unchanged, center bytes match the inertia ledger. Limits and observation-vs-kernel distinctions are in RUN_CONTRACT.md. Old numerical runs and sources were not changed or repeated.

Review order: PATCH_PROOF.md, refinement_plan.json, POINT_SCHEDULE.json, POINT_PATCH_LEDGER.json, error_ledger.json, inertia/inertia_ledger.json (or output.json), guard_receipt.json. PRELAUNCH_SHA256SUMS freezes the execution sources; SHA256SUMS binds final artifacts.
