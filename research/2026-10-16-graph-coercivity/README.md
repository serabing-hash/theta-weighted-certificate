# Local graph coercivity at B = 3/4

Supporting research artifacts for a local analytic theorem on the actual finite-window arithmetic graph. Prepared 2026-10-15 UTC; the directory date is 2026-10-16 in Asia/Seoul.

The result concerns the complex L2 interval Omega = (-3/4, 3/4), its exact 7-, 4- and 2-vertex translated fibers, a coercive auxiliary quadratic form and its full-space bounded inverse. It is not a proof of the Riemann Hypothesis.

## Main local statement

Put theta = 2^-16, omega = 1-theta, V(x) = R(B+x)+R(B-x), with R(s) = artanh(exp(-s/2))+atan(exp(-s/2)), and c_Gamma = log(pi)+gamma_E+pi/2+3log(2). Define

    delta_0 = 2R(B) - c_Gamma + 5/2 > 0
    j_7 = 29/5 - c_Gamma > 0
    c_coer = omega delta_0 + theta j_7 > 0
    C[f] = integral (omega V + 17omega/5 + 7theta - c_Gamma)|f|^2 - P_B[f].

Here P_B uses the actual two-direction n=2,3,4 shifts with coefficients log(2)/sqrt(2), log(3)/sqrt(3), log(2)/2. On D_g = {f in L2(Omega): integral V|f|^2 < infinity},

    C[f] >= integral (p_g + omega Delta)|f|^2 + c_coer ||f||^2,

where p_g and Delta are the nonnegative position and full-tail reserves defined in PROOF_PREMISES.md. For any a>0, the form a||f||^2+C[f] is densely defined and closed; its associated operator A has

    D(A) = {f in L2(Omega): Vf in L2(Omega)}
    ||(A+mu)^-1|| <= 1/(a+c_coer+mu),  mu >= 0.

The full-space inverse commutes with complex-linear reflection. This does not identify A with an original minimum-domain operator or a constrained high-sector inverse.

## Read and use

1. Read PROOF_PREMISES.md and SCOPE_AND_LIMITATIONS.md.
2. Follow REPRODUCIBILITY.md for the analytic audit route and checksum verification.
3. Inspect the line-numbered source excerpts under sources/. Source labels are provenance identifiers, not external premises that a self-contained manuscript may silently inherit.
4. Compare the selected mathematical reviews under reviews/. Agreement or a PASS label is not proof; the displayed arguments must be checked.
5. Use PROVENANCE.json for the supplied full-source byte identities and exact publication selection. MANIFEST.sha256 binds every payload file except itself.

This package contains no new numerical experiment, no executable research checker, no physical-Q or full-Schur positivity certificate, and no endpoint-jet gain claim. The accompanying standalone manuscript is prepared separately; the source excerpts are supporting historical research records.

## Publication and rights

This directory is additive. Existing repository files, prior research directories and history are not replaced. The repository root LICENSE remains unchanged; no additional relicensing is introduced. For reproducibility, cite the exact commit-pinned directory URL rather than a moving branch URL.
