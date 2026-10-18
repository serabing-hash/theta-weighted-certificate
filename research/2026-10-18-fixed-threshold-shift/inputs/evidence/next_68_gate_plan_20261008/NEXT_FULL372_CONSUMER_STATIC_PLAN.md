# One corrected-model full-372 consumer

8 October 2026. Static proposal only; no candidate arithmetic, solve, eigenproblem, consumer, factorization or benchmark was executed for this plan. A new execution approval is required. Author-original text: CC BY-NC 4.0; inherited material keeps its licenses.

## Decision

Recommend one saved-data-only attempt that uses the corrected normal model, freezes one rational C68, and tests **I372 - Ucert > 0 directly**. Do not impose the old 99/100 target: that would demand additional unproved headroom when the requested conclusion needs only a strict inverse bound below one. Do not sweep targets, tau, precision, coefficient denominators, trial rank, or coefficient models.

The completed saved68 gate is a dependency, not work to repeat. Final independent mathematical acceptance **and** resource/scope/process-closure acceptance must be available before launch. A provisional worker status or checker PASS alone is insufficient.

## 1. Exact premises and the one objective

Keep the same minimum operator domain, 372 observation coordinates, and U68=[V,q0,q1,q2,q3], G68=[G,F0,F1,F2,F3]. Here G=G0-3V/64 on the whole line. Neither the exterior nor the q-versus-saved-residual distinction changes.

The original paper proves, conditional on its analytic/source/cover inclusions,

    H_delta = L + delta I + WW* >= (delta - d_sharp - epsilon_cover) I,
    d_sharp = 960589/4389760000000,
    epsilon_cover = 14194233101692862490101543299783481485 /
                    3284055810247577849424937639623597936869376.

At delta=1/64 this is the saved positive eta64, not a transfer of the old full372 inverse factor. Bind and check the exact scalar identity using the original SHARP_TAIL_REPLAY.json and paper equations genericsharp/eta64. Preserve the inherited admission of every trial to D(H64), the saved Gram inclusion premises, and the accepted physical action errors.

Read the exact saved nu68, sigma68_squared, sigma_bar68, eta, tau, alpha and beta strings. The displayed nu68=1.0236987482387174 and beta approximately 8.2240108557e-9 are not proof inputs. Set E68=sym(J68), tau=1/100 and retain

    alpha = (1+tau)/eta,
    beta  = nu68 sigma_bar68 + 101 sigma68_squared/eta,
    S_corr = alpha N68 - E68 + beta I68,
    B_corr = alpha K68 - D68.

For any rational C of shape 68 by 372 the deterministic consumer is

    U(C) = alpha A - B_corr^T C - C^T B_corr + C^T S_corr C.

This is exactly the expanded corrected consumer, including beta C^T C, all cross terms and all 68 errors. It is different from the old diagnostic normal equations S_eta C=B_eta. Those diagnostic arrays must not choose C in this attempt. Do not reuse the old floating 64-column C, its obstruction direction, or old full372 factors as a candidate or certificate.

### An analytic lower bound for the corrected normal matrix

There is no abstract normal-matrix invertibility barrier. Let sigma=sqrt(sigma68_squared), g=G68 z, and e=(H64 U68-G68)z. Then

    ||U68 z|| <= (||g|| + sigma ||z||)/eta,
    z^T S_corr z >= (tau/eta)||g||^2
                    - (sigma/eta)||g||||z|| + beta ||z||^2
                  >= mu_normal ||z||^2,
    mu_normal = beta - sigma68_squared/(4 tau eta)
              = nu68 sigma_bar68 + 76 sigma68_squared/eta > 0.

The first inequality uses H64>=eta I and the actual operator error bound; the last is completion of a scalar square. No numerical square root is needed in the final exact mu_normal expression. This bound concerns the exact corrected normal matrix. If a symmetric dyadic enclosure has center Sc and radius Rs, then

    Sc >= (mu_normal - max_i sum_j Rs_ij) I.

Require the displayed exact difference to be positive before solving Sc. This sufficient admission test may fail without disproving positivity; such failure is HOLD in this one fixed route. No fallback normal-model search is allowed.

## 2. Minimal authenticated inputs and dependency control

Numerical inputs:

- saved_68_run01_20261008/work_root/saved68/{D68,K68,N68,E68}.json
- The same directory's NORM_ERROR_CERTIFICATE.json, INPUT_VERIFICATION.json, OUTPUT_MANIFEST.json and INDEPENDENT_SAVED68_CHECK.json
- The finalized saved68 independent mathematics and external resource/scope/closure acceptance receipts
- checkpoint_saved_run03_20261008/v2_j2_run03/original/delta64_failure_diagnosis_20261007/sources/AOBS_ENCLOSURE.json
- The original observation order, trial order/T/X/Y bindings, domain and mixed-Gram proofs through the already accepted saved68 input manifest
- The paper and SHARP_TAIL_REPLAY.json for the eta64 premise

Hash and schema-check the exact files, not just directories. Verify denominators, dimensions, nonnegative radii, symmetry where required, trial order, W coordinate order, and the A hash already used by saved68. Preserve the original saved68 bytes. Do not recompute the 1770 entries, old affine blocks, norm certificate, kernels, action ledgers, or any new H/source/DFT/quadrature data.

The proposed producer needs the already provenance-audited python-flint 0.9.0 payload at checkpoint_saved_run03_20261008/v2_j2_run03/runtime_deps, including its bundled FLINT/GMP/MPFR libraries. Recheck its accepted payload manifest and interpreter/library identity under the charged outer start. No fresh install or package change is proposed. Set native thread counts to one. Do not import old cert_support.py: it imports physical-producer modules and initializes source-related quantities at import time. Extract/reimplement only reviewed pure finite-matrix routines in a source-free consumer module.

The independent checker must not import the producer or FLINT. Standard Python integers/Fraction and a separate explicit integer-matrix implementation suffice. If NumPy object arrays are chosen for its integer loops, freeze and verify that dependency first; do not let dtype conversion introduce floating arithmetic. A checker using source-free standard-library loops avoids that added dependency.

## 3. Frozen arithmetic and coefficient proposal

One fixed precision/serialization design:

1. Native arithmetic: fixed 160-bit Arb. After the exact normal-center positivity admission, choose the 68-by-372 coefficient proposal using exactly one LU solve of Sc Cstar = Bc. The fresh 372-dimensional positivity factor uses exactly one fixed-order block LDL with block size 16. If the LU solve fails or is inconclusive, stop with HOLD; do not switch solver or retry. No eigenproblem and no adaptive precision increase.
2. Consumer-input and normal-array enclosures: common denominator 2^160, obtained by exact outward integer division of saved rational endpoints. Reconcile symmetric locations by a containing symmetric hull when necessary.
3. Candidate coefficients: denominator 2^80, round each finite solution-ball midpoint to nearest, ties toward positive infinity, then save/read back exact integer numerators. This convention is fixed for negative values too.
4. Final model center/radius and Ucert: denominator 2^100. Factor L0,D0 and approximate inverse M0: denominator 2^80.

The 7083-character beta fraction and 7018-character sigma-squared fraction must stay scalar objects. Do not broadcast their full denominators into 138384 dense Fraction objects. Their exact scalar identities remain saved; enclose alpha and beta outward at 160 dyadic bits before dense arithmetic. For scalar ball a and matrix ball X use the exact radius |ac| Rx + ra |Xc| + ra Rx. Every input requantization and subsequent normal-array requantization is owned by that array's entry radius. Retain the original exact endpoints as the inclusion reference. No native rounding radius may be discarded.

Build S_corr and B_corr enclosures once. Prove the Sc lower bound above, and execute exactly one Sc Cstar=Bc solve with 372 right-hand sides. Freeze C from its finite Arb solution balls at 80 dyadic bits and write its hash before assembling U. Save solution-ball-to-C error bounds and the exact midpoint normal residual Sc C-Bc. These are proposal diagnostics; the candidate is an arbitrary rational C for the final consumer, **not a certified minimizer for every member of the input interval family**. No solve residual or midpoint eigenvalue decides the full372 verdict.

The final exact producer can use compact homogeneous integer matrices. With A, alpha, S and B enclosed at 160 dyadic bits and C at 80 bits, the compressed consumer products have denominators at most 2^320 before final rounding:

    Xc = C^T Bc,        Xr = |C|^T Br,
    Yc = C^T Sc C,      Yr = |C|^T Sr |C|,
    Uc = center(alpha A) - Xc - Xc^T + Yc,
    Ru = radius(alpha A) + Xr + Xr^T + Yr.

Denominators in these expressions must be aligned exactly. This is exact interval propagation with an exact C. It preserves the full beta C^T C term through S_corr. Serialize enclosing 100-bit center/radius entries with the complete final rounding radius, require exact symmetry, and define

    Ucert = Uc + diag(Ru 1).

All 138384 entries and all 372 row sums must be checked. An entrywise upper matrix is not a Loewner upper bound. Exact integer products have no native rounding loss; any Arb used instead for assembly would need its full enclosing radii, plus independent exact inclusion checks.

## 4. Fresh full372 positivity witness and independent check

The sole target is T=I372-Ucert. Rehydrate this **new exact rational T**. Run one fixed-order 160-bit outward block LDL. Require all 372 pivot lower endpoints positive; a negative or inconclusive pivot is HOLD, with no permutation, target change, alternate factor, or precision retry.

Round the new factor to 80-bit dyadic unit-lower L0 and positive diagonal D0, and form one fresh 80-bit approximate inverse M0 of that finite L0. This is a finite matrix inverse, not an H64 inverse application. Never use a factor, inverse, row correction, pivot, or margin from delta32.

Using exact integers compute

    rho0 = max_i sum_j |(T-L0 D0 L0^T)_ij|,
    e1   = ||L0 M0-I||_1,
    einf = ||L0 M0-I||_infinity,
    m1   = ||M0||_1,   minf = ||M0||_infinity,
    d0   = min_i D0_ii,
    mu372 = d0(1-e1)(1-einf)/(m1 minf) - rho0.

Require d0>0, m1>0, minf>0, e1<1, einf<1 and mu372>0, all exactly. With the chosen scales the factor residual has common denominator 2^240: its numerator is delta_ij 2^240 - Ucert_numerator_ij 2^140 - sum_k Lnum_ik Dnum_k Lnum_jk. The inverse residual denominator is 2^160. No old 99/100-specific factor of 25 or 100 may survive in this direct-I target formula.

The separate checker reads only frozen inputs and emitted artifacts. It independently verifies endpoint inclusions for the dyadic preprocessing and S/B assembly; coefficient dimensions/denominator/hash; the exact normal residual and normal-admission scalar; every final model entry and radius; Ucert row correction; factor/matrix/C bindings; and all exact factor residual/norm comparisons. It does not import producer arithmetic, rerun physical work, regenerate saved68, or perform a second coefficient solve/factorization. It must finish inside the same attempt budget.

Only after its PASS and external resource/process closure PASS may the result state, conditionally on the unchanged analytic/inclusion premises,

    W*H64^-1 W <= (1-mu372) I,
    L + I/64 >= mu372 eta I > 0.

This excludes the endpoint-inclusive interval (-infinity,-1/64] for the specified operator. It proves neither L>=0 nor RH nor a new operator bridge. A failed witness is not an impossibility theorem.

## 5. Static cost, allocation and one-shot budget

For r=68 and n=372 the exact center/radius compressed consumer needs, without sparsity:

- C^T B center and radius: 2 n^2 r = 18820224 integer multiply-add terms
- C^T S C center and radius: 2(r^2 n+n^2 r) = 22260480 terms
- Total consumer: 41080704 terms per implementation, plus scalar/serialization work
- Exact factor residual and inverse residual: at most two dense n^3 products, or 17298248 terms total when a separate checker explicitly exploits triangularity and residual symmetry
- One small 68-by-68 solve with 372 right sides, one 372-by-372 block factor, and one finite triangular-factor inverse

The old independent delta32 replay recorded 9.077 seconds and 232316 KiB RSS; the old exact-factor stage recorded 3.906 wall seconds. These are historical plausibility evidence only. Its reported CPU value was cumulative process CPU, not the factor-stage CPU. None of those records certifies the new runtime, denominator growth, memory footprint or mathematical success.

Read/convert one input JSON at a time; release parser trees. Do not retain A JSON plus multiple A copies. Stream/check final matrices in row blocks where possible; keep only the required accumulator, skinny products, and one factor-residual workspace. Release solve/source-enclosure workspaces before the full factor stage. To preserve the already reviewed single-worker process graph, run producer and independent checker sequentially in the same capped registered worker. The producer returns only its small status and releases its dense workspaces, followed by explicit garbage collection. The native FLINT runtime may remain mapped and allocator memory may remain resident; all of it remains charged to that worker’s AS/RSS ceilings. The independent checker imports neither producer nor FLINT and makes no native calls. A saved phase-boundary record must disclose this same-process arrangement; garbage collection is not a claim that memory returned to the operating system. The largest raw 372-square matrix is 138384 integers; at the proposed fixed 1024-bit dense-integer ceiling, its integer payload is about 17 MiB before Python/native object overhead. Apply that ceiling to every produced dense numerator and accumulation result, including coefficient/factor witnesses; the original rational input records and scalar proof fractions are exempt. This is an allocation design, not a verified peak. Overflow of the bit-length gate is HOLD, never silent truncation or a raised ceiling.

The bounded attempt is plausible because all physical work is removed, the dimension is already supported by the old implementation, and dense denominators are kept dyadic. There is no analytic obstruction inherited from the old 64-column all-C model theorem: that theorem fixes the old 64-column family. Full372 positivity at rank 68 remains genuinely untested.

Use one new single-use attempt token. Charge preparation, dependency and input hashing/staging, imports, candidate arithmetic, solve, full372 assembly/factor, independent checker, serialization/readback/fsync, supervisor/observer and complete closure from the same authenticated outer start:

- Soft stop: 510 seconds wall **or whole-tree CPU**
- Hard ceiling: 540 seconds wall **and whole-tree CPU**
- Per process RLIMIT_AS: 536870912 bytes (512 MiB)
- Per process RSS threshold: 512000 KiB (500 MiB)
- One numerical worker at a time, one thread; no pool, automatic retry or continuation

A proposed internal allocation is 60 seconds preparation, 180 seconds producer, 210 seconds independent check, and 60 seconds durable closeout, totaling the 510-second soft envelope. These are admission allocations, not predicted completion times or renewed clocks. Hard-limit handling must retain time for mandatory cleanup and receipts. Do not advertise an aggregate-tree memory cap that the guard does not impose.

## 6. Exact HOLD conditions

HOLD before launch for missing fresh user authorization; incomplete saved68 final acceptance; missing/changed evidence; unauthenticated runtime; or an unreviewed code/resource manifest.

HOLD during the attempt for a source/hash/schema/order mismatch; changed eta/tau/model; negative radius or failed endpoint containment; a denominator/bit-length gate failure; nonpositive mu_normal-row_radius; nonfinite/inconclusive solve; failed exact C freeze/readback; omitted/duplicated action or serialization charge; asymmetric final enclosure; any unaccepted LDL pivot; nonpositive rounded D0; failed e1/einf/m1/minf/mu372 comparison; independent-checker disagreement or timeout; soft/hard resource boundary; incomplete fsync/hash readback; surviving/unreaped process; missing authentic whole-tree resource evidence; or any prohibited H/source/DFT/quadrature/eigen/extra coefficient-candidate solve activity. The block solves inside the one fixed LDL and the one finite factor inverse are expressly included in this plan; they are not second coefficient proposals.

Preserve partial evidence and report the first unmet obligation. No failure authorizes 99/100-to-I switching, a new tau, a new C model, higher precision, different rounding, a different order/rank, rerunning saved68, or another attempt. This proposal already fixes direct I as its sole target.

## Sources read, not executed

- next_68_gate_plan_20261008/NEXT_68_GATE_PLAN.md
- original/theta_delta32_release_20261007/theta_delta32_certificate.tex, especially genericsharp, eta64, consumer32, Ucert32, factor32 and margin32
- original/theta_delta32_release_20261007/replay/restored_full/code/{run_once,cert_support,exact_factor,verify_saved}.py
- original/theta_delta32_release_20261007/replay/current_exact/independent_verify.py and its saved verdict.json
- original/residual_action_contract_20261008/review/MIXED_GRAM_CONTRACT.md
- original/delta64_failure_diagnosis_20261007/REPORT.md and code/certify_model_obstruction.py
- The saved68 interface/acceptance metadata, saved68 implementation description, and existing runtime provenance manifests

Here original/ abbreviates checkpoint_saved_run03_20261008/v2_j2_run03/original/.
