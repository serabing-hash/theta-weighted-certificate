# D-phase HOLD: source and checkpoint audit

8 October 2026. CC BY-NC 4.0 for original audit material; inherited licenses retained.

## Finding

The archived Work producer has the correct mathematical D definition and the
correct absolute-value gate. Its phase implementation repeatedly multiplies a
rectangular complex ball for all 41188 powers with no wrapping control. This
is a concrete enclosure-stability defect and the leading explanation of the
observed HOLD. It is not evidence that the exact D violates its analytic bound.

The original failure's first k, D midpoint/radius/endpoints, maximum D radius,
and finite/nonfinite discriminator were not saved. Therefore the exact numeric
failure cannot be reconstructed from the artifact. No actual phase replay was
performed to invent those missing values. Every phase z.is_finite() assertion
in the loop passed; that fact does not substitute for the missing per-D record.

Verdict: propose ONE rigorously equivalent centered-disc repair at fixed160-bit
precision, with complete error retention. Do not run it until the integrated
patch, source-free backend checks, runtime provenance and one-use aggregate
checkpoint supervisor are reviewed and execution is explicitly authorized. No
analytic blocker was found in the D formula. Production and all other columns
remain HOLD.

## Authoritative evidence

Both downloaded ZIPs match the Work package receipt in actual bytes and SHA256:

- PART01: 4811694 bytes, 8d4c9f18bd69ca119b5f28c064679449b783899d0e002824dffcbd505832f7b0
- PART02: 8993873 bytes, bf75336d9d66f10e8615293531a11b81573a7fa7467894e3e39e03407ef3fb40

All340 output-manifest entries match. All8 baseline code hashes match the frozen
static entry gate. Evidence is in DOWNLOAD_READBACK.json and
STATIC_ARTIFACT_VERIFICATION.json. Archive readback is independent of the Work
UI's later unavailability; no reason for that UI condition is inferred here.

Sources:
https://drive.google.com/file/d/1UBrvTNAQ32Tl2vZy1HUOUmy7Kh1kD-y1/view?usp=drivesdk
https://drive.google.com/file/d/1eDRC2zRkgTwBpZPVXE8QgpB_AWt8OQmF/view?usp=drivesdk
https://drive.google.com/file/d/1XRAAXplgxKp0xeU1YslJakBuEen3x6aU/view?usp=drivesdk
https://drive.google.com/file/d/1lPdQfr_Vlp9_vyV-v0C_YZoGrmqf-fr4/view?usp=drivesdk

## Exact source trace

The frozen v2_action.py has SHA256
627eb62ce947d8b1d76e7ac7eae6acccdcdde0f66052c9acc2c672d2ed79352a.

- Lines70–72 construct cGamma=log(pi)+EulerGamma+pi/2+3log2 and all18
  weights log(p)/sqrt(n), with 2*sum(weights)<32 and cGamma<10 checked.
- v2_support.py line14 has exactly the inherited ordered prime-power list:
  (2,2),(3,3),(4,2),(5,5),(7,7),(8,2),(9,3),(11,11),(13,13),(16,2),
  (17,17),(19,19),(23,23),(25,5),(27,3),(29,29),(31,31),(32,2).
- Lines76–80 take rho=exp(i log(n)/16), start z=1, execute z*=rho for every
  positive k through41188, and add 2*w*Re(z) to the D entry initialized at cGamma.
- Line79 checks each phase z is finite and computes a per-root maximum radius.
  Line82 collects it only in an in-memory phase_records list.
- Line83 is precisely all(v.is_finite() and s.upper(v)<42 for v in D).
- v2_support.py line131 defines s.upper via abs_upper followed by exact dyadic
  extraction. Thus the test is an absolute upper bound, not a positivity test
  or midpoint comparison.
- D serialization begins only on line84. The certificate holding phase_records
  is written only on line86, after the failing gate. Neither was written.
- The traceback identifies v2_action.py line83, from v2_worker.py line20.

Excluded explanations: a D-positivity gate, wrong n/p list, log(p)/log(n) mix-up,
missing two-sided factor2, wrong frequency /16, D serialization failure, and a
comparison using a midpoint in place of an absolute bound. The code and trace
support these exclusions directly. All18 complete phase chains were counted.

No exact mathematical contract mismatch was found. The computational weakness
is the enclosure representation: repeated rotated rectangles can widen by a
factor related to |cos(theta)|+|sin(theta)| despite exact unit modulus. Carrying
all rectangular radii, as this source does, preserves inclusion but need not
preserve usefulness. Simply clipping cosines to[-1,1] would establish the easy
D bound while leaving poor arithmetic errors; it is not the proposed recovery.

## Counters, gates and resources

PILOT_STATUS reports one attempt, zero retries, 64 inherited descriptors scanned,
8192 new Gamma multipliers and 741384 phase recurrence products. Code order and
absence of later phase logs place the failure before all seven polynomial
products, new residual action, length131072 DFT, theta/node reconstruction and
437 kernels. e_J, e_m and B_2 were not measured. The saved frame gate passed.

The supervisor confirms:

- wall25.47436677800033 seconds; wait4 CPU25.447844999999997 seconds
- exit1 from the AssertionError; no TERM/KILL event or resource timeout
- RSS45368KiB; VmPeak86772KiB
- RLIMIT_AS536870912 bytes; CPU600 seconds; TERM590/KILL600 configuration
- python-flint0.9.0, FLINT3.6.0, precision160, one thread

The unsuccessful D stage itself ran for approximately3.5934 seconds. This
cannot predict any of the unstarted action/DFT/old64/Gram phases. All1754 full
four-column kernels remain uncompleted, including the representative437.

## Accepted reusable data

Independent exact integer inspection confirms GAMMA_EXTENSION.bin has8192
records and524288 bytes, SHA256
bedc238709490a75279450e0dfd8462121d9cd4bd0513e61664d52896102c025.
Every saved lower endpoint is positive. Every saved radius is below2^-100;
the largest stored radius numerator at denominator2^140 is2. No digamma value
was recomputed. Its inherited multiplier hash is
412c0966f8066769c07d8e7cd6496d3a516ef22ca06cda5265d85d7e73bc9cd1.

Other accepted files include the372-entry frame certificate,64 compact old
Gamma-only node caches and old frame dyadics. They are not complete old Z64,
Q, weights, new F2 or physical-Gram checkpoints. The proposed continuation
validates and copies them into distinct outputs without changing the original
HOLD directory or marker.

## Proposed repair and continuation

See REPAIR_PROOF.md, centered_disc_candidate.py, GENERIC_FIXTURE_RESULTS.json,
v2_action_PHASE_REPAIR_REVIEW_ONLY.py and v2_action_PHASE_REPAIR.diff.

The selected implementation keeps each phase center as exact dyadics over2^140.
For every native160-bit product, the existing outward record helper supplies
coordinate local-error radii. Their sum increments an exact integer Euclidean
error bound E_num. Since the exact rho has modulus1, inherited error propagates
with factor1. All E enters each cosine, weighted D, both uses of D, serialization
and the eventual e_J ledger. No error is reset or assumed independent.

The integrated phase patch adds early-persisted root diagnostics, a first-bad-D
record, full-ball readback containment, and a strict absolute-D gate after
readback. Other producer functions are unchanged.

The explicit review-only continuation entrypoint is
v2_checkpoint_continue_REVIEW_ONLY.py. It requires a separately reviewed approval
record, starts wall accounting before checks/copies, uses TERM564/KILL574 and
512MiB AS, combines supervisor/worker CPU monitoring with a conservative child
CPU cap, and retains the prior wall/CPU cost in the aggregate ledger. It verifies
all old manifest files,91 source bindings, actual extracted source bytes,
accepted frame records and Gamma extension before doing only the remaining
j=2 phases. No other column or consumer is called. New output is continuation_01;
the original pilot/supervisor/single-use record is untouched. This entrypoint has
been syntax-checked only and is still subject to independent review.

Runtime provenance remains a preflight condition: the shipped installed-tree
hashes and RECORD verification establish byte integrity, but the package itself
states its original wheel URL/hash were not captured. The adapter therefore
requires a complete independently authenticated runtime identity in the actual
executor, including native dependency files; a packaged tree is usable only
after that provenance check. It rechecks hashes before importing that tree. No downloaded
binary or Work script was executed by this audit.

No execution approval record, continuation marker, phase cache or action was created.
