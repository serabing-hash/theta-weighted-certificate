# Nine-feature Schur comparison: reproducible negative-comparison record

**Date:** 28 October 2026 (UTC). **Author:** Jongmin Choi, Independent Researcher,
Seoul, Korea. ORCID: 0009-0008-7448-514X. **License:** CC BY-NC 4.0 (see LICENSE).

## Result and limits

This is a negative result for a **finite sufficient comparison matrix**, not a
negative direction of the physical prime–Gamma quadratic form. It is **not an
RH counterexample**, and it does **not prove positivity at B = 3/4**, a global
spectral gap, or RH. No new formal paper or historical novelty claim is made.

The nine-feature improvement is real but insufficient on an explicit rational
vector. Saved interval arithmetic gives the strict enclosures

| Quadratic quantity on the same vector z | Exact-decimal containing interval |
|---|---|
| z^T F9 z | [-0.0000004941393, -0.0000004941391] |
| z^T F_failed z | [-0.0000005664564, -0.0000005664563] |
| z^T (F9 - F_failed) z | [0.0000000723171, 0.0000000723172] |

Here z has 32 entries; its first four are the exact decimals
`81.78419471194, 77.560436244137, 20.738337066071, 1`, and its remaining
28 entries are zero. These are rational numbers, not binary64 inputs.
The script derives them by exact rational elimination and rounding and outputs
all 32 exact rational entries. The full rational interval endpoints are in
`saved_arithmetic_certificate.json`.

On the same vector the saved low-only matrix satisfies z^T A z > 0
(approximately 5.7682700295e-6), while the conservative complete coupling bound
is larger. Thus **negative F9 does not mean negative A or negative actual q**.
The normalized F9 quotient, approximately -3.7619024309e-11, is only a
comparison-matrix quotient, not an actual spectral gap.

## Mathematical scope and normalization

The source uses the real-even minimum compact-support Gamma form domain at
B = 3/4 and ordinary L2 normalization; Euclidean coefficient norms refer to
its orthonormal basis. They are not the weighted N_X norm from other research.
The active prime powers are 2, 3, 4 (Lambda(4) = log(2)).

The saved sufficient matrix has the structure

    H9 = W^{-1} + G,
    Corr9 = Z H9^{-1} Z^T,
    F9 = A - C0 + Corr9 = A - C_new.

C0 includes the complete high-row cost envelope, including its infinite tail.
The nine selected finite features comprise one prime-defect slack feature,
one merged Gamma label-zero/pole feature, individual Gamma labels 1, 2, 3,
and aggregate label blocks 4–15, 16–63, 64–255, 256–1023. Selection of a
finite positive resource does not mean deletion of the complete source form.

Parameters are M = 32 low modes, N = 16384 tail start, J = 32 exponential
terms, precision 256 bits. J is distinct from the selected Gamma labels
0 through 1023. The saved H9 has nine strictly positive LDL pivots; the first
three F9 pivots are positive and the fourth is strictly negative. The replay
also verifies 32 nonzero zeta interval coordinates and 256 nonzero Y_s
coordinates. This is not a claim about every possible feature choice.

F_failed is the previous *formula comparison evaluated in this diagnostic*;
it is not a reconstruction of an absent matrix from an older run.

## Reproduce saved arithmetic first (standard library only)

Run from the extracted directory, with assertions enabled:

    python3 replay_saved_arithmetic.py > replay_output.json

No installation, network, producer import, Gamma evaluation, prime evaluation,
quadrature, or new analytic tail estimation occurs. The script verifies the
unaltered source and two input JSON hashes, checks symmetry, independently
performs saved-endpoint LDL arithmetic, and certifies the rational witness,
positive improvement and positive low-only A budget. It rewrites
`saved_arithmetic_certificate.json` deterministically. All arithmetic bounds
use exact rational endpoints with outward rounding to 512 binary fractional
bits; floating-point values in the output are display aids only.

On systems with Python's `resource` module it enforces CPU 60 seconds and
address-space 512 MiB. On systems without that module the mathematics is the
same, but limits are not imposed by the script; use external limits if needed.
The supplied replay was run under both limits. Python 3.12.14 was used.
Do not use `python -O`.

## Original producer (included unchanged; separate optional reproduction)

`verify_three_quarters_joint_gamma.py` is included byte-for-byte with its
original SHA256. Its original header says "prepared, unexecuted"; that is
historical pre-run wording preserved to keep the executed source identity.
This record contains the result of its later run: exit 2 and
`FAILED_POSITIVITY_GATE_NOT_CERTIFICATE`, not a success certificate.

The source requires python-flint 0.9.0 and keeps an explicit execution guard.
An independent reviewer who chooses to run the producer can use a fresh
output stem (this is distinct from the cheap saved-arithmetic replay):

    python3 verify_three_quarters_joint_gamma.py --execute-approved-once --output independent_result.json

Expect a diagnostic JSON and failure JSON, exit 2, and no success JSON. Use a
fresh directory, assertions enabled, and appropriate external resource limits.
The original bounded run used CPU 180 seconds, wall 240 seconds, address-space
1 GiB, and a source-enforced combined output cap of 8 MiB. No producer rerun was
performed when assembling this bundle. `requirements-producer.txt` is not
needed for the saved replay.

## Trust boundary

The replay independently verifies **arithmetic consequences of saved rational
intervals**. It does not independently establish that those intervals enclose
the intended analytic matrix, rederive the complete-tail estimates, validate
all form-domain reductions, or audit FLINT itself. Interpreting A as the actual
low form and F9 as a rigorous lower comparison still relies on those analytic
and source-enclosure assumptions. This is neither proof-assistant verification
nor independent human peer review. Output hashes establish byte identity, not
the mathematical truth of analytic premises or execution-history authenticity.

The producer source and mathematical diagnostic/failure files are unchanged.
The public replay is adapted from a saved arithmetic audit to remove private
execution-receipt dependencies, use package-local paths, and omit receipt and
attempt-history fields. Every retained certificate field was checked equal to
the original certificate. Original audit hashes and adaptations are documented
in `provenance.json`; the new certificate has its own hash in `SHA256SUMS`.
Private execution logs and approval identifiers are not part of this package.

## Files and integrity

- README.md: scope, interpretation, reproducibility and trust boundary.
- verify_three_quarters_joint_gamma.py: unchanged original producer.
- joint_gamma_result.diagnostic.json: unchanged pre-gate mathematical intervals.
- joint_gamma_result.failure.json: unchanged fourth-pivot failure and linkage.
- replay_saved_arithmetic.py: portable standard-library saved-endpoint checker.
- saved_arithmetic_certificate.json: exact witness and independent arithmetic.
- replay_output.json: shorter deterministic replay output.
- provenance.json: source identities, adaptation record and recorded environment.
- requirements-producer.txt: dependency of the optional full producer only.
- LICENSE: project CC BY-NC 4.0 license.
- SHA256SUMS: checksums of all other package files (not a self-hash).

Check integrity with `sha256sum -c SHA256SUMS` on a system providing sha256sum.
The ZIP is a transport copy; its separate digest is supplied outside the ZIP.
