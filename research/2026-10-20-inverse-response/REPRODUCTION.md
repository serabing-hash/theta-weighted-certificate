# Reproduction: bytes, optional arithmetic, and historical evidence

The publication task performed no scientific replay. The procedure below separates checks of public bytes from a reader's optional new arithmetic execution. Its mathematical premises are listed in `ASSUMPTIONS.md`.

## 1. Obtain the fixed public package

Use the **40-character artifact commit printed in the companion paper**, not `main`. No unpublished commit or download URL is guessed here. With Git and a shell:

```sh
ARTIFACT_COMMIT=REPLACE_WITH_THE_40_HEX_ARTIFACT_COMMIT_FROM_THE_PAPER
git init inverse-response-checkout
cd inverse-response-checkout
git remote add origin https://github.com/serabing-hash/theta-weighted-certificate.git
git fetch --depth=1 origin "$ARTIFACT_COMMIT"
git checkout --detach FETCH_HEAD
test "$(git rev-parse HEAD)" = "$ARTIFACT_COMMIT"
cd research/2026-10-20-inverse-response
python3 -I -B verify_package.py
```

Alternatively, download the reproduction ZIP from the actual release linked by the publisher. Obtain its byte count and SHA256 from that release's `SHA256SUMS.txt` and `RELEASE_MANIFEST.json`. The archive's digest must match **before** extraction. Use `safe_extract.py` from the fixed Git checkout, not an unverified copy inside the archive:

```sh
python3 -I -B safe_extract.py /absolute/path/reproduction.zip \
  /absolute/path/new-extraction-directory \
  --sha256 SHA256_FROM_THE_RELEASE --bytes BYTE_COUNT_FROM_THE_RELEASE
cd /absolute/path/new-extraction-directory/reproduction
python3 -I -B verify_package.py
```

The extractor rejects traversal, absolute/noncanonical names, duplicate names, encrypted members, symlinks and other special files. It requires a nonexistent destination and admits at most 200 files / 20,000,000 uncompressed bytes. It never invokes code from the archive. Do not use unrestricted `unzip`/`tar` extraction as a substitute.

## 2. Restore all mathematical inputs

The following command downloads only the ten exact files in `INPUTS.json`, from their existing commit-pinned raw GitHub URLs. It validates their declared byte counts and SHA256 values before installing them under `dependencies/`. An existing correct file is reused; a conflicting file is rejected and never overwritten.

```sh
python3 -I -B verify_package.py --fetch-inputs --require-inputs
```

Expected status:

```text
PACKAGE-BYTES-AND-SYNTAX-VERIFIED
dependencies_present = 10
dependency_count = 10
scientific_executions = 0
```

This command does not parse mathematical fractions, import checker modules, perform contractions, evaluate roots, or run an old checker. No private or environment-specific file is an input to the public replay. The package contains the two saved reports; the rank-one calculation consumes the saved shared-error report and `saved_SHIFT_SCALARS`, while shared-error arithmetic consumes the ten external files.

The fixed source of those external files is:

`https://github.com/serabing-hash/theta-weighted-certificate/tree/f61c7af23c7e4027cc3cb768faa40273f1146ffd/research/2026-10-18-coefficient-obstruction`

This is a mathematical-input closure, not a recursive rerun of every prior producer or the original physical-source certification.

## 3. Optional reader execution — not performed by publication

Requirements: Linux with procfs, `sched_setaffinity`, `wait4`, and POSIX resource limits; CPython 3.11 or later, standard library only. Historical runs used CPython 3.12.14. The adapter is portable source, not a distribution of that exact interpreter binary. Neither Python-flint nor NumPy/SciPy/mpmath is needed or admitted.

Choose a new output parent outside the package. Each command starts exactly one scientific worker. Running these commands is a new scientific replay, unlike steps 1–2:

```sh
mkdir /absolute/path/new-reader-output-parent
python3 -I -B replay_once.py --kind shared --execute-once \
  --output-root /absolute/path/new-reader-output-parent/shared-once
python3 -I -B replay_once.py --kind rank-one --execute-once \
  --output-root /absolute/path/new-reader-output-parent/rank-one-once
```

The rank-one replay uses the byte-pinned saved report, not the newly produced shared replay report; no accidental change of experiment is allowed.

The supervisor consumes each output directory before admission. It never deletes the marker, retries, increases precision, changes parameters, relaxes resource limits, or substitutes a fallback input. **After a failure, interruption, or uncertain outcome, stop; do not delete the directory or choose a new one to retry this attempt.** Investigate separately and record any later experiment under a separate explicit protocol.

Before numerical work, the supervisor verifies package and input bytes. That source-free preflight has a separate 45-second timeout. The worker spawn-to-reap interval has a strict 60-second wall cap, a 60-second CPU cap, one allowed CPU/thread/worker, 384-MiB address-space cap, and 320-MiB observed/high-water/wait4 RSS cap. It rejects unexpected child processes. Supervisor and worker share one allowed CPU during the timed interval; the interval also bounds their aggregate CPU capacity. This new single-worker supervisor is **not** the historical registered-tree witness.

The arithmetic retains dense 1024-bit gates where applicable, 100000 decimal-digit scalar limits, 332193-bit scalar pre-operation gates, seven shared-error direction contractions, two 68-term error-budget sums, and exactly six rank-one roots at 128 fractional binary bits. There are no coefficient solves, new source integrals, parameter searches, full-372 factorization, or precision escalation.

## 4. Required outputs and exact acceptance

A completed reader run must have:

- process exit 0;
- `math/INDEPENDENT_CHECK.json` with the complete expected scientific status;
- `math/PUBLIC_REPLAY_RESULT.json` with `EXACT-MATHEMATICAL-REPORT-MATCH`;
- `REPLAY_COMPLETION.json` with `PUBLIC-ARITHMETIC-REPLAY-COMPLETE` and resource acceptance true.

The adapter compares the entire newly produced and saved report trees by exact JSON values/string identity except the top-level keys `input_manifest_sha256`, `input_sha256`, and `admission`. Those three fields describe the deliberately replaced private provenance chain. No mathematical, precision, operation-count, convention or decision field is omitted. Both sources and saved references are independently hard-pinned in the adapter.

Expected numerical verdicts:

| Replay | Verdict | Meaning |
|---|---|---|
| shared | `CONDITIONAL-FIXED-SHARED-ERROR-MAJORANT-EXCLUDED` | This fixed upper majorant exceeds the target; it does not lower-bound the true response. |
| rank-one | `INCONCLUSIVE` | Both certified corrections are positive, but neither corrected upper bound is below the exact target. |

`PUBLIC-ARITHMETIC-REPLAY-COMPLETE` means faithful arithmetic reproduction, **not** that the mathematical target passed. `HOLD`, missing files, malformed/duplicate JSON, a hash mismatch, a reversed/invalid interval, negative norm upper, denominator inconsistency, report mismatch, signal, timeout or nonzero exit is never success. A provisional mathematical report cannot overrule supervisor failure.

## 5. Preserved historical evidence and sanitization

The two `results/*.json` files and both checker sources are byte-identical to the historical files. Their original hashes are retained. Public `evidence/*_projection.json` records contain only the listed original JSON fields plus the original file's byte count/SHA256. `PROVENANCE.json` gives the projection rule. The historical final manifests are preserved as indices; they identify omitted process files but do not assert that every indexed file is in this public payload.

Original result ZIPs and original approval/release/private process records are deliberately not republished. Their historical identities are not reused for the new public archive. A hash of an omitted original does not make its contents reconstructible and does not independently authenticate a projection. Historical process acceptance is documented at that stated trust boundary. Public mathematical replay requires none of those omitted records.

All original local records remain unchanged. No conversation, approval quotation, credential, signed delivery URL, unrelated personal information or private note is needed for the public package. The author's previously published contact block remains in the manuscript.

## 6. What the publication checks do and do not establish

The publication verification record lists actual byte downloads, exact hash/size checks, source-only AST inspection, negative packaging tests, and PDF/TeX checks. It records scientific executions as zero. The adapter/supervisor has not been runtime-validated by a scientific execution in this publication task. Resource acceptance and report matching for a future reader run must be established by that run's actual completion record.

No new adequacy ledger, precision-capacity comparison, higher-rank test, input regeneration, physical premise certification, or RH proof is claimed.
