# Next gate: saved-endpoint assembly and the 68-column trial norm

8 October 2026. Static mathematical and execution plan only.
Author-original material: CC BY-NC 4.0. Inherited sources retain their licenses.

## Decision

The smallest useful next attempt is a **saved-data-only 68-column assembly gate**. It should deliver all 1770 required algebraic/transfer entries, the complete enlarged Gram/energy blocks, a new certified trial-map norm bound, and the 68-column deterministic action-error coefficient. It should then stop. It needs no new source values, H actions, Fourier transforms, node reconstruction, physical quadrature, scientific native backend, coefficient search, solve, eigensolve, or 372-dimensional consumer.

All 1754 physical kernels are already saved: retained column 2 supplies 437 and completed columns 0, 1, 3 supply 1317. More subtly, all 1488 q*W entries are already saved as enclosing frame-moment intervals. They can be reused after source/meaning checks. Thus the gate must account for 1770 entries, but only 282 of those entries have to be newly constructed rather than supplied from existing moment records. Auxiliary exact algebra may still reconstruct R0*W to obtain R0*R0.

This document is not execution approval or a PASS for that gate. No candidate Gram algebra or consumer was executed in preparing it. One separate user approval is needed before the new arithmetic attempt. The later coefficient solve and full 372-coordinate positivity consumer should remain a separate, explicitly budgeted task.

## 1. Fixed mathematical object and provenance

Throughout, * is the Hilbert adjoint; all stored arrays here are real, so numerical adjoints are transposes. The ordinary-Lebesgue and weighted-space functions have the same inner products under the specified unitary U.

- H = H64 = L + I/64 + WW*, on the unchanged minimum operator domain.
- W has the same 372 observation columns and exact coordinate order.
- V = WT has the frozen 64 trial columns, with T numerators divided by 2^30.
- t = 3/64 and G = G0 - tV on the whole line. Outside [-2,2], G = -tV; this exterior is not discarded.
- X is 372 by 4 and Y is 64 by 4, from the original X40.csv and Y40.csv, with denominator 2^40 and fixed column order 0, 1, 2, 3.
- q is the true-source analytic four-column block previously admitted to D(H), not the discontinuously truncated saved residual. Put R0 = WX - GY and Delta = q - R0.
- epsilon_j = sum_i |Y_ij| e_i, where e_i is the OLD analytic-surrogate-to-saved-compact-action norm error. Then ||Delta_j|| <= epsilon_j.
- F is the four saved compact H64 action approximants, in column order 0, 1, 2, 3; ||Hq_j - F_j|| <= Bnew_j.
- eta stays exactly
  1446776856241610348487954379752034183297365381007 /
  92620636523388719034562694367509285563269120000000.

The inherited four-column domain/independence proof stays a premise, bound to the same X, Y, T, old action descriptors, and infinite-source definition. Independence of the four new directions does not certify their enlarged norm or a successful inverse bound. The compact R0 differs from q by epsilon; the physical residual WX-HVY differs by an additional action error. These distinctions must remain explicit.

## 2. Exact saved inputs and data meanings

Paths below are relative to /workspace/scratch/b7173d79ee6b. Define:

- R = checkpoint_saved_run03_20261008/v2_j2_run03
- O = R/original/theta_delta32_release_20261007/replay/restored_full
- B = R/original/residual_block_admission_20261007
- D = R/original/delta64_failure_diagnosis_20261007
- P = R/continuation_01/pilot
- N = remaining_three_run01_20261008/work_root/remaining

The input manifest for an approved attempt must bind the following actual files, not only their containing directories:

1. O/inputs/T64_dyadic_numerators.csv and B/outputs/X40.csv, Y40.csv.
2. D/sources/AOBS_ENCLOSURE.json: A = W*W, 372 by 372, 100-bit midpoint/radius records.
3. O/outputs/G0_GRAM_ENCLOSURES.json: K0 = G0*W and N0 = G0*G0, 100-bit records.
4. O/outputs/AFFINE_GRAM_ENCLOSURES.json: reuse the shift-independent D_old = V*W, P_old = V*V and J0 = V*G0, subject to their recorded A/G0/T bindings. **Its K32, Ng32, Fg32 have t=1/32 and must not be relabeled as delta64 arrays.**
5. O/certificates/ALL64_ACTION_AND_QUADRATURE_BUDGET.json: all 64 exact physical B_i and all 64 e_i. Its etaSharp_exact and nu_exact refer to the older 1/32 certificate; use the eta64 above and derive nu68 anew.
6. P/J2_437_KERNELS.json and N/REMAINING_1317_KERNELS.json: 140-bit final, padded physical-kernel intervals. Their affine correction has already been applied. Never apply it twice.
7. P/J2_FRAME_CERTIFICATE.json and N/columns/j/Jj_FRAME_CERTIFICATE.json for j=0,1,3: read moment_records_bits140, not dyadic_numerators_bits100. The former enclose W*q, with all saved-matrix radii and 2048 epsilon_j already charged. The latter merely define the rounded action coefficients.
8. P/J2_ACTION_CERTIFICATE.json and N/columns/j/Jj_ACTION_CERTIFICATE.json for j=0,1,3; the exact B values and their descriptor bindings. Keep full rational strings, not rounded displays or prebudget targets.
9. Their four ACTION_V2 descriptors, epsilon/frame records, and acceptance receipts. The main combined saved-output evidence is independent_remaining_results_20261008/AUDIT.json and REPORT.md; retained-j2 acceptance remains a separate inherited binding.
10. B/REPORT.md and B/outputs/SAVED_BLOCK_CERTIFICATE.json: analytic q definition, minimum-domain admission and existing nonredundancy certificate.

A record [m,r] with declared bits b means [(m-r)/2^b, (m+r)/2^b]. Require integer parsing, nonnegative r, expected dimensions/order, exact declared denominators, and stable SHA-256. Do not interpret r as a half-width in a different scale or remove it because the midpoint is small.

Normalize the physical-kernel file layouts into K_F = F*W (4 by 372), C = G*F (64 by 4), and N_F = F*F (4 by 4 symmetric). J2's GF list is a 64-entry column; the remaining file's GF is indexed by its three new rows. Verify the semantic orientation while installing it. Install each of the ten unique self/cross records into the appropriate symmetric positions once, including retained (2,2) and new (0,2), (1,2), (2,3).

All alias, tail, analytic-to-compact xi, node, and serialization pads already owned by these physical-kernel files stay inside their input intervals. They are not recomputed or added a second time.

## 3. Required affine old blocks

Using the authenticated shift-independent old arrays, perform enclosing rational algebra:

    K = K0 - t D_old
    N_old = N0 - t(J0 + J0*) + t^2 P_old
    J_old = J0 - t P_old

These are respectively G*W, G*G and V*G at delta=1/64. Reuse a previously saved delta64 enclosure only if it is independently authenticated as enclosing these same formulas. Do not rely on the failed diagnostic's floating cached arrays.

No new physical error is introduced by the exact affine shift: the old ||HV_i-G_i|| bounds are still B_i. There is no reason to regenerate G0, its caches, its polynomial, or its quadrature.

## 4. The 1770 entries and their complete pads

Use the residual identity before taking norms. Form enclosing intervals for:

    R0*W  = X* A - Y* K                         (4 by 372)
    R0*G  = X* K* - Y* N_old                   (4 by 64)
    R0*R0 = X* A X - X* K*Y - Y*K X + Y*N_old Y
    R0*F  = X* K_F* - Y* C                     (4 by 4)

Let w_l, g_i, f_k and r_j be certified upper bounds on ||W_l||, ||G_i||, ||F_k|| and ||R0_j||. They come from the upper endpoints of A_ll, (N_old)_ii, (N_F)_kk and (R0*R0)_jj, respectively, followed by outward rational square-root certification. Saved certified ||F_k|| upper bounds in the independent audit may be reused after their diagonal bindings are checked. A valid squared-norm enclosure may have a negative lower endpoint; only a nonnegative upper bound is needed for the norm estimate. A negative upper endpoint is a consistency failure.

Supply:

- q*W: 1488 entries, with additive absolute radius epsilon_j w_l. Minimal route: reuse the existing 1488 frame-moment intervals with their already included 2048 epsilon_j pads. Do not add those pads again. Tightening them from the actual diagonals would be optional fresh algebra and is unnecessary for this minimum proposal.
- q*G: 256 entries, from R0*G with radius epsilon_j g_i.
- q*q: ten unique symmetric entries, from R0*R0 with radius epsilon_j r_k + epsilon_k r_j + epsilon_j epsilon_k. On a diagonal this is 2 epsilon_j r_j + epsilon_j^2.
- q*F: all sixteen entries, from R0*F with radius epsilon_j f_k.

All original interval radii propagate in every product and sum before these transfer pads are added. There is no independence assumption and no cancellation of error radii. The matrix q*F is generally non-Hermitian; do not replace it by its symmetric part at this stage.

The old e_i, residual epsilon_j, new xi_j and physical B_i/Bnew_j have different owners:

- e_i -> epsilon_j -> the R0-to-q pads in this section.
- xi_j -> the already accepted physical F-kernel enclosures.
- B_i and Bnew_j -> the deterministic consumer action correction in section 6.

None can substitute for another. In particular, the measured new frame or pole errors already contribute to Bnew_j; do not add them again as separate action-error columns.

## 5. Assemble the entire 68-column interface

Write U68=[V,q] and G68=[G,F], and use the new q blocks just supplied:

    P68 = U68*U68
        = [[P_old,              T*(q*W)*],
           [(q*W)T,            q*q      ]]

    D68 = U68*W = [D_old; q*W]
    K68 = G68*W = [K; K_F]

    J68 = U68*G68
        = [[J_old,              T*K_F*],
           [q*G,                q*F   ]]

    N68 = G68*G68
        = [[N_old, C],
           [C*,    N_F]]

P68, J68 and N68 are 68 by 68; D68 and K68 are 68 by 372. Preserve full J68 before forming E68=sym(J68)=(J68+J68*)/2. P68, N68 and E68 must be represented by Hermitian enclosures, with radii enlarged if needed when reconciling independently obtained symmetric locations. They cannot be made narrower by an unjustified average.

For the original fixed-eta diagnostic normal model, assemble:

    S_eta = N68 - eta E68
    B_eta = K68 - eta D68

Its new blocks must agree with the original mixed-Gram contract:

    S_cross = C - eta/2 [T*K_F* + (q*G)*]
    S_new   = N_F - eta sym(q*F)
    B_new   = K_F - eta q*W

Assembly of S_eta is not proof that it is positive or invertible. In particular, the old 64-column lower bound S_old >= I/50000 is not an enlarged 68-column bound. A solve or a Schur-complement positivity check is outside the smallest proposed gate.

### A fresh certified nu68

From a symmetric rational center Pc and nonnegative symmetric radius Pr enclosing P68, one simple, fully exact certificate is

    L68 = max_i [Pc_ii + Pr_ii
                 + sum_(k!=i)(|Pc_ik| + Pr_ik)]
    nu68 >= 0,  nu68^2 >= L68.

Gershgorin then proves lambda_max(P68) <= L68 and ||U68|| <= nu68. Record all row bounds and the final exact square comparison. One can instead use the larger absolute row-sum bound if that is the frozen implementation choice; no eigensolve is needed.

Use the existing 100-bit dyadic outward-square-root convention, obtained by integer isqrt and an exact final square comparison, for scalar norm witnesses. This is rational enclosure of saved endpoints, not a new 100-bit physical computation or a reduction of the producer's fixed 160-bit arithmetic. Keep exact rational matrix outputs without requantizing them. No choice of precision is swept on failure.

Do not insert 101/100 by inheritance. If the new independently certified inequality nu68 <= 101/100 happens to hold, the same number can be used only because the new certificate proves it. A larger certified nu68 is a valid output; its effect on the final correction must be carried honestly. No upper acceptance target for nu68 has yet been numerically justified.

## 6. All 68 action errors and the decisive later inequality

Use the actual 64 old B_i and the four measured Bnew_j. Preserve all component ownership and validate their recorded acceptance comparisons. Compute exactly

    sigma68^2 = sum_(i=0..63) B_i^2 + sum_(j=0..3) Bnew_j^2
    sigma_bar68 >= 0, sigma_bar68^2 >= sigma68^2.

The old B_i survive the whole-line affine shift unchanged. The fresh physical Bnew_j are for H64 q_j directly. Do not replace them by the conditional analytic prebudget totals or by their common 2^-18 acceptance ceiling.

Retain tau=1/100 from the deterministic consumer. Define the exact rational correction coefficient

    alpha = (1+tau)/eta
    beta  = nu68 sigma_bar68 + (1+1/tau) sigma68^2/eta.

For ANY subsequently frozen rational C68 of shape 68 by 372, the paper's deterministic identity gives

    W*H^-1 W <= U(C68),

    U(C68) = C68^T D68 + D68^T C68 - C68^T E68 C68
             + alpha [A - K68^T C68 - C68^T K68 + C68^T N68 C68]
             + beta C68^T C68.

Here ^T denotes transpose of these real arrays; all products are ordinary matrix products. Normalized symmetrization supplies the stated linear action-error factor. The square term retains exact sigma68^2, while only the linear term uses sigma_bar68. This is deterministic Young/Cauchy-Schwarz propagation, not a statistical error budget.

The simpler uncorrected fixed-eta model and the fixed-tau, error-corrected consumer are different quadratic objectives. If a later step chooses C68 by minimizing this certified upper-model expression, its normal arrays would be

    S_corr = alpha N68 - E68 + beta I68
    B_corr = alpha K68 - D68.

A future solve must identify which objective it uses and certify whatever invertibility/positivity it requires. It cannot silently solve S_eta C=B_eta and describe that as the minimizer of the fixed-tau corrected model. However, a candidate from either source can still be tested by the same valid deterministic consumer because the inequality holds for every C68.

The minimum gate stops after producing beta and the authenticated block interface; it does not choose C68 or assemble U(C68).

## 7. Why the full 372-coordinate consumer stays separate

A full consumer has a different deliverable and resource profile: a new C68, its exact rounding, all 372^2 model entries, interval radii, a Loewner correction and a fresh positivity witness for the SAME newly assembled matrix. It should receive its own explicit execution authorization after the 68-column gate result is known.

For a symmetric model center Uc and radius matrix R, the correct rigorous upper matrix is

    Ucert = Uc + diag(R 1).

An entrywise upper matrix is not automatically an upper bound in Loewner order. Native/serialization radii of every entry must be included before the row correction.

The eventual decisive condition is a strictly positive certified margin for c I372 - Ucert with a predeclared c<1, or directly a strictly positive margin for I372-Ucert. Choosing c=99/100 would reproduce the old paper's 1/100 relative-coercivity format, but that numerical target is not already proved at delta=1/64 and should be frozen explicitly in that later task. No target sweep is authorized.

A new exact LDL/inverse-residual witness can follow the paper's pattern. For the new S_target, require d0>0, e1<1, e_infinity<1 and

    d0 (1-e1)(1-e_infinity)/(m1 m_infinity) - rho0 > 0.

All witness matrices, residuals and norms must refer to that same new S_target. The old 1/32 factor, its old inverse, its old row correction and its old positive margin cannot be reused as the new proof. Alternatively, a freshly justified interval factorization must have certified positive pivots for all 372 indices.

Only such a complete certificate can imply L+I/64 >= (1-c) eta I (or the corresponding margin-derived lower bound). A 68-column norm PASS, a positive normal matrix, a successful solve, or an improved floating/model eigenvalue is insufficient. Even a successful 1/64 result would concern this specified minimum weighted operator and finite threshold; it would not prove RH, L>=0, or an unestablished bridge to another operator.

## 8. Minimal execution proposal, subject to approval

Proposed scope name: SAVED_1770_AND_68_GRAM_BOUND_ONCE.

One isolated, single-worker saved-endpoint attempt should:

1. Verify manifests, exact input schemas, accepted-column bindings and unchanged sources.
2. Reuse the 1754 physical-kernel intervals and 1488 q*W moment intervals; construct the other 282 q-block entries with their explicit pads.
3. Derive the correct delta64 old affine blocks, assemble P68/D68/K68/J68/N68/E68/S_eta/B_eta, and save exact rational intervals with round-trip readback.
4. Certify nu68, epsilon values and all norm witnesses; compute sigma68^2, sigma_bar68 and beta with exact inequalities and error ownership.
5. Run a separate implementation's saved-output consistency checks within the same charged attempt if the frozen budget permits. Do not import candidate code into that checker. Resource/scope closure and mathematical endpoint verification remain separate verdicts.
6. Serialize final status, source/output hashes, interval widths and exact norm/error certificates; close and reap all attempt processes; then stop before any C solve or 372-dimensional consumer.

Permitted mathematics: integer/rational endpoint arithmetic, deterministic matrix sums/products on saved entries, absolute-value bounds, integer square-root witnesses, and exact comparisons. Standard-library Python is sufficient. NumPy, SciPy, FLINT/Arb, new transcendental enclosures, new native matrix calls, or producer imports are not mathematically required. Exact integer/rational arithmetic is not a rerun of the old 160-bit producer.

There is no need to load the 3912-node Q/Z/F caches, long J coefficients, source Fourier arrays, convolution workspaces or DFT buffers. Hash only the evidence required by the new input manifest; inherited node meanings remain inherited numerical premises. The largest necessary saved input is the 372-by-372 A enclosure, not a new 372-dimensional consumer matrix. Read one JSON object at a time, convert needed records to compact integer/rational arrays, and release parsing trees. Reuse authenticated D_old, P_old and J0 rather than rebuilding their large products. Stage products through skinny 372-by-4 and 64-by-4 temporaries and do not retain all intermediate matrix copies.

Resource judgement: the dominant physical producer work is absent, so this is substantially smaller in numerical scope than the completed action/integration block. The core input JSON files are only a few MB each, and the arithmetic is mostly skinny products plus 68-by-68 assemblies. This makes a single bounded attempt plausible. It does **not** establish a runtime or peak-memory completion guarantee: exact rational numerator/denominator growth and parser/object overhead still need implementation review. No benchmark or candidate-math probe was run for this plan; the preceding 29.8-second block is not a timing certificate for this different route.

### Fixed ceilings and closure

Use a new one-shot attempt token and fresh approved code/input manifest. Preserve the current guard policy rather than silently falling back to the older contract's 600-second description:

- 510-second soft wall and whole-tree CPU stopping thresholds.
- 540-second hard wall and whole-tree CPU ceilings, charged from the authenticated outer start through the required output durability and complete process closure.
- 536870912-byte address-space cap per process (512 MiB).
- 512000-KiB RSS threshold per process (500 MiB).
- Single worker; no worker pool; no automatic retry or resumption.

The current policy does not impose an aggregate-tree memory cap. Do not describe these per-process limits as a verified 512-MiB whole-tree limit. If an aggregate cap is desired, it requires an explicit reviewed policy change, not a misleading label. Include the preparation, supervisor, observer, checker and cleanup in the applicable whole-tree CPU accounting. Do not start a new 540-second allowance for each substage.

The earlier attempt's single-use token is consumed; it does not authorize this new gate. Authorization must name the new saved-algebra/68 scope. It does not authorize new actions, physical kernels, coefficient optimization, or a full 372 consumer.

## 9. Acceptance, HOLD and stopping rules

A gate PASS means only:

- the fixed four columns and all 1754 physical inputs are authenticated;
- all 1770 q-block entries are delivered with their correct source/transfer ownership;
- the complete enlarged blocks are enclosing and dimensionally/semantically consistent;
- fresh exact certificates prove nu68^2 >= lambda_max(P68), sigma_bar68^2 >= sigma68^2, and the stated beta;
- round-trip interval inclusion and error-ledger checks pass;
- the resource/scope audit shows one attempt, closed processes and no forbidden execution.

Stop with HOLD or FAIL, without automatic retry, if an input hash/schema/coordinate/shift disagrees; a required interval/pad/physical B value is missing; saved q*W coefficients are confused with moment intervals; symmetry cannot be enclosed; a purported squared norm has negative upper endpoint; an exact witness comparison fails; a resource limit approaches or allocation fails; process accounting/closure is unverified; or the implementation needs an unapproved numerical/backend operation. Retain the partial outputs and identify the first unresolved obligation. Do not increase rank, cutoff, precision, duration, memory or trial count to get a PASS.

Reaching a valid finite nu68 with a larger correction than hoped is not a mathematical impossibility result. Do not turn a wide interval or unsuccessful later positivity check into a claim about the exact resolvent or RH. This gate ends after the authenticated 68-column/error interface, even if time remains.

## 10. Source map and verification boundary

Primary contract:

- R/contract_context/review/MIXED_GRAM_CONTRACT.md, lines 197-249: exact kernel count, four residual identities, transfer pads, fixed-eta blocks and fresh trial norm.
- Its SHA-256 is 98ba7b1ae4d755e40049ac960e71d3a62456df387c87816e60c2f3e80a26ab59. Static hashing confirmed it is byte-identical to R/original/residual_action_contract_20261008/review/MIXED_GRAM_CONTRACT.md.
- R/contract_context/REPORT.md, sections 7-8, lines 228-287: epsilon, frame/pole ownership, physical B_j ledger and enlarged consumer boundary.
- B/REPORT.md, sections 1-4: frozen block, uncorrected fixed-eta objective, residual definition and minimum-domain proof.

Paper baseline:

- mirror_stage_paper_20261007/theta_delta32_certificate.tex, lines 1026-1037: conditional enclosure premises.
- Lines 1102-1110: old 64-column trial norm only.
- Lines 1140-1162: whole-line affine algebra.
- Lines 1165-1200: deterministic inverse consumer and action correction.
- Lines 1209-1258: radius-to-Loewner conversion and exact new-factor positivity criterion.
- Lines 1305-1320: exact eta64 and limits of the failed same-64 diagnostic.

Completed output and resource evidence:

- independent_remaining_results_20261008/AUDIT.json and REPORT.md: saved 1317 + retained 437 acceptance, moment-interval checks, final pads, norms, and unexecuted next gate.
- independent_remaining_results_20261008/audit_saved.py, sqrt_bounds: existing exact outward 100-bit scalar norm-witness convention; read only, not executed for this plan.
- independent_remaining_resource_audit_20261008/INDEPENDENT_RESOURCE_CLOSURE_AUDIT.json: completed prior scope, current 540/510 whole-tree limits, per-process memory limits, and explicit zero downstream consumers.
- remaining_three_run01_20261008/admission/PRODUCTION_PLAN_REMAINING.json: current guard-policy values; it is evidence of policy, not authorization for this new attempt.

This plan was prepared by static reads, schema/metadata inspection and source-byte hashing only. It provides formulas and an authorization boundary, not newly evaluated block entries, nu68, sigma68, beta, a new C68, positivity or a strengthened spectral theorem.
