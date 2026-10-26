# Verification and reproduction boundaries

## 1. Portable verify-only: supported and locally tested

Requirements: Python 3.10+ standard library, approximately 100 MB disk space for the unpacked scientific packet. No NumPy, compiler, MPFR, network, credentials or historical `/opt` directory is needed.

```sh
python3 portable/verify_saved.py
```

Expected result: JSON with `status: PASS`, a check count, and `producer_regeneration: false`. Any mismatch exits nonzero. The command does not import or run historical producers. It reads only this release and performs hashes, binary format checks, and rational arithmetic on saved scalar bounds. It checks:

1. Public manifest and provenance hashes, and exact scalar-to-C++ pi/cGamma/t0 constant identity.
2. All 58 smooth parent budgets and their exact q_i/k_i^4 subdivision sum, coverage of 130 children, upward exported budget and the 1/128 target.
3. The 104 signed patch tasks and 58 safe baseline tasks against the saved schedules.
4. Outward sum of final error components and recorded restriction-margin subtraction, including the propagated input error.
5. Exact dyadic Gershgorin row reconciliation of the saved projected center/error arrays (the matrix products and their error bounds remain producer premises).
6. Center and trial payload identities, dimensions, power-of-two scaling, and seven historical runtime snapshot identities.

It **does not** recompute the Loewner enclosure, analytic inequalities, MPFR transcendental evaluations, Gram products, validity of projected product-error bounds, or eigenspaces. These remain premises supplied by the saved producer records and proofs. No theorem follows from hash checks alone.

## 2. Exact inputs and dependencies

All paths below are relative to `evidence/`.

- v1 `Z_dyadic.bin` (552×552) and `Ctrial.bin` (276×2×552): arbitrary exact dyadic trial coefficients. Binary format is headerless little-endian IEEE-754 binary64, C row-major. Their validity does not require recovering the historical optimizer that selected them.
- v1 `Ufloat.bin` (1104×552): stored surrogate; `exact_candidate.cpp` bounds its discrepancy from the analytic lift. It is not asserted to be the exact analytic lift.
- v1 `Gmid.bin`/`Grad.bin`: complete fine-form center/radius; `H_ledger.json`: domain/cap/theta data reused in later stages. v4 does not use the old v1 H/F center or its point-error estimate.
- v2 `H_domain_ledger.json`: complete parent-domain remainders; `scale.npy`: exact dyadic D, not a change to the original 552 moment constraints.
- v3 `refinement_plan.json`, `POINT_SCHEDULE.json`, `POINT_PATCH_LEDGER.json`, `DeltaHmid.bin`: exact allocation and saved signed patch.
- v4 `HSAFE_LEDGER.json`, `Hsafe_mid.bin`, final center/error/inertia records and trial subspace: repaired center and final result.
- `mpfr_backend/` and `rh_two_direction_certificate_2026-10-25/inputs.hpp`: included transitive C++ headers. These are not dependencies on an unpublished checkout.

## 3. Producer regeneration: historical sources, not a turnkey portable runner

**Do not run the historical `pipeline.py` scripts in the archived evidence directories.** They write outputs; some expect omitted historical preparation/guard files, old binary artifacts, or a previously populated run tree. The v4 runtime guard deliberately binds absolute paths and 1538 historical file hashes. Installing packages with similar versions does not satisfy that guard. The original SHA256SUMS/PRELAUNCH_SHA256SUMS and REUSED_INPUTS are historical records; they are not a promise that every operational file listed there is public. The authoritative public manifest is at this release's root.

Full producer regeneration is **not claimed tested or portable by this release**. An independent reproducer must use a separate working tree, rebuild the included C++ sources against a documented MPFR/GMP environment, implement a new explicit runtime-binding policy, and record new source/runtime/output hashes. Merely disabling historical checks and calling the outcome the same certified run is invalid. A future supported regeneration adapter must be reviewed separately and must retain all interval precision, rounding, tail, matrix-product and spectral-premise checks.

The scientific regeneration order is:

1. Treat supplied Z/C as fixed dyadic inputs; validate candidate exactification and U error (`exact_candidate.cpp`).
2. Regenerate fine G entry enclosures (`g_generator.cpp`, `g_jet.hpp`).
3. Regenerate original full-domain derivative/tail bounds (`h_core.cpp`, `h_assemble.py`) and improved contact-domain bounds (`v2/h_domain.cpp`, `h_domain_bound.py`), retaining valid panelwise minima.
4. Verify the saved fixed rational allocation (no optimization needed), then regenerate v3 signed point patch.
5. Regenerate v4 safe 58-point baseline with explicit multiplication; form the repaired center and complete error budget.
6. Validate a 551-dimensional positive restriction with all product/Gram error bounds, retaining the conditional Loewner premise.

C++ uses C++17 and MPFR precision 266 bits. Shared libraries require `-fPIC -shared`; linking requires MPFR and GMP. Binary64 matrix stages require Linux round-to-nearest, NumPy/SciPy, single-thread OpenBLAS and threadpoolctl, with assumptions recorded in the proofs. See `DEPENDENCIES_AND_LICENSES.md`. No producer rerun was performed to assemble this release.

## 4. What to report

Distinguish (a) public-file identity failure, (b) saved-ledger arithmetic failure, (c) analytic objection, (d) independent numerical regeneration discrepancy. Report the precise commit, relative path and SHA-256, command, compiler/library versions, hardware and actual bound. Do not report a failed historical absolute-path runtime gate as a counterexample to the mathematical inequality.

## 5. Concrete independent-regeneration work plan (not executed here)

The following build commands are a **proposed independent build recipe**, not a transcript of the historical compiler invocation and not an already validated portable adapter. Use a disposable copy of `evidence/`; never build or write into the frozen release. Install a C++17 compiler, compatible MPFR 4.2.2/GMP development libraries, and the Python numerical dependencies before starting. Preserve their license notices. A system exposing only the versioned MPFR soname may replace `-lmpfr` by `-Wl,-l:libmpfr.so.6`.

```sh
# In a disposable copy of evidence/, not the immutable archive:
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
export CXX=c++
# Do not enable -ffast-math, reassociation, or an unreviewed alternative BLAS.
FLAGS='-std=c++17 -O2 -fno-fast-math -ffp-contract=off'
v1=rh_full_rigorous_certificate_2026-10-25
v2=rh_full_rigorous_certificate_v2_2026-10-25
v3=rh_full_rigorous_certificate_v3_2026-10-25
v4=rh_full_rigorous_certificate_v4_2026-10-25
(cd "$v1" && "$CXX" $FLAGS exact_candidate.cpp -lmpfr -lgmp -o exact_candidate)
(cd "$v1" && "$CXX" $FLAGS g_generator.cpp -lmpfr -lgmp -o g_generator)
(cd "$v1" && "$CXX" $FLAGS -fPIC -shared h_core.cpp -lmpfr -lgmp -o h_core.so)
(cd "$v2" && "$CXX" $FLAGS -fPIC -shared h_domain.cpp -lmpfr -lgmp -o h_domain.so)
(cd "$v3" && "$CXX" $FLAGS -fPIC -shared h_point.cpp -lmpfr -lgmp -o h_point.so)
(cd "$v4" && "$CXX" $FLAGS -fPIC -shared h_point.cpp -lmpfr -lgmp -o h_point.so)
```

These compilation steps do not evaluate the mathematical operators. Record compiler version, full command line, binary hashes and linkage (`ldd` on Linux). System include paths may differ; the bundled `mpfr.h` must agree with the linked MPFR ABI. The bundled quoted-include closure consists of `interval.hpp`, `mpfr.h`, stage `jet.hpp`/`h_contact.hpp`/`g_jet.hpp`/`inputs.hpp`, and the additional two-direction `inputs.hpp` used by G. No private source checkout is needed for these includes.

### Stage-by-stage inputs and outputs

Each stage below must run with its own stage directory as working directory, in the disposable tree. Save separate logs and never substitute partial output for complete output. These are production calculations, unlike the portable verifier.

| Stage | Entry point / reference | Required scientific inputs | Outputs used downstream |
|---|---|---|---|
| Scalar admission | `rh_scalar_screen_2026-10-25/screen.py` | Frozen constants and directed Decimal routines contained in script | `output.json`, including fixed R=1 admission/count row |
| Exact candidate | v1 `./exact_candidate` | `Z_dyadic.bin`, `Ufloat.bin`, `Ctrial.bin`, MPFR | `exact_candidate.json` with analytic-lift discrepancy and coefficient norm bounds |
| Fine G | v1 `./g_generator` | included `inputs.hpp`, analytic formulas and MPFR | `Gmid.bin`, `Grad.bin`, `g_output.json` |
| Original domain/tails | v1 `python3 h_assemble.py` | `h_core.so`, candidate JSON, U/C binaries, scientific helper functions and rounding/BLAS checks | `H_ledger.json`; old `Hmid.bin` is incidental and **not** a v4 center dependency |
| Contact domain | v2 `python3 h_domain_bound.py` | `h_domain.so`, v1 candidate/H ledgers and U/C, `scale.npy`, `h_arithmetic.py`, `inertia_check.py` | `H_domain_ledger.json` with valid panelwise minima and cap reuse |
| Fixed allocation | saved plan or exact audit using `plan_refinement.py` as reference | v2 parent ledger | fixed `refinement_plan.json`; do not silently change the 58/130 allocation when claiming the fixed experiment |
| Signed patch | v3 `python3 h_point_assemble.py` | `h_point.so`, v1 candidate/U/C, `scale.npy`, frozen 104-task schedule, local helpers | `DeltaHmid.bin`, `POINT_PATCH_LEDGER.json` |
| Safe baseline | v4 `h_point_assemble.py` **after new runtime policy is independently implemented and reviewed** | v4 `h_point.so`, v1 candidate/U/C, `scale.npy`, frozen 58-task schedule, local helpers | `Hsafe_mid.bin`, `HSAFE_LEDGER.json` |
| Final assembly | arithmetic in v4 `pipeline.py` from the saved G congruence through `certify_inertia` | G/Grad, candidate/U, v1 cap/theta bounds, v2/3 plan, v3 patch, v4 baseline, D | repaired `Hmid_composite.bin`, `Fmid_composite.bin`, `error_ledger.json`, inertia arrays/ledger, `output.json` |

The old v1 `prepare_candidate.py` and optimizer NPZ are **not required scientific dependencies**: the public Z/C are fixed exact dyadic trial inputs, and U is a surrogate whose error is independently bounded. The optional old optimizer only explains how those trial numbers were selected. Historical v1–v3 final F matrices and old H-center rounding are also not needed for v4. The historical guard/launcher scripts enforced local process-group/resource rules; they are not a missing mathematical kernel. The required mathematical kernels, constants, exact inputs and stage helpers listed above are distributed.

### Fresh-runtime binding invariants

A new reproducer must create an explicit new-run identity, not overwrite historical expected hashes. Before execution:

1. Verify the public archive, copy it, and record all changed/new source hashes. Keep original-vs-adapted code and a reviewable diff. Changes to launch paths/timeouts are operational; changes to arithmetic, scheduling, precision, dimension, projection or intervals require a new mathematical review.
2. Record actual Python executable; NumPy/SciPy/threadpoolctl implementation files; all loaded BLAS, MPFR/GMP, libm/libc/libstdc++ binaries; the rebuilt point library; compiler and flags; OS, CPU and rounding configuration. The historical `runtime_guard.py` shows the fingerprinting scope. Bind the new absolute paths and their hashes **before** the new production run, then require equality before/after workers and final assembly. Do not relabel new hashes as a historical MATCH.
3. Preserve MPFR precision 266 and directed endpoint semantics, binary64 round-to-nearest, nonfinite/subnormal/overflow guards, operation-count product error bounds, underflow allowances, single-thread classical OpenBLAS checks, all cap/theta/Gamma/prime terms, and exact dyadic scale round-trip checks. A different BLAS implementation needs its own arithmetic justification.
4. Keep the original 276-cell projection / 552 moments, 1104 fine source modes, R=1, epsilon=1/8, fixed D and arbitrary exact trial coefficients. Preserve 58 parents, 104 signed point tasks, 130 composite smooth pieces, and two analytic caps. Never replace full-domain bounds with empirical quadrature differences.
5. Rebind **both** fresh input hashes and expected source/binary hashes in the new pipeline. Historical PRELAUNCH/REUSED hashes cannot be retained if a dependency was regenerated; merely deleting those comparisons is not equivalent. A separately reviewed driver should validate completion/schema/dimensions, positivity of radii, exact task coverage, upward summations, and the full final Loewner premise.
6. Record timeout/failure/inconclusive outcomes honestly. Local historical time limits may need adjustment on different hardware; a timeout is no certificate. A differing valid outward bound may remain mathematically sufficient, but is a new run, not byte-identical reproduction. Recheck positive-subspace independence and strictly positive margin rather than requiring matching diagnostic eigenvalues.

There is no unpublished scientific kernel required by this work plan. The unresolved engineering task for independent full regeneration is a reviewed fresh-runtime driver and its validation, not access to private operational approvals. No such driver is claimed delivered or executed in this release.
