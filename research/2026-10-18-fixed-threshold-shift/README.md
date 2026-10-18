# A small certified improvement of a fixed theta-operator threshold

**Conditional computational result. RH_PROOF=NOT-OBTAINED.**

For the same minimum self-adjoint theta operator, the same 372 observations,
the corrected 68 trials and the unchanged 68-by-372 coefficient matrix,
one fixed shift `h = 2 delta_star` gives a strictly stronger negative
lower edge. The analytic shift-reuse lemma retains all full-line action
errors. Simple scalar continuity alone reproduces the old bound exactly.

| Saved quantity | Rounded display (18 significant digits) |
|---|---:|
| Old lower edge | -0.0156184544151869108 |
| New lower edge | -0.0156055131540838210 |
| Strict improvement | 0.0000129412611030897828 |
| Fresh response margin mu1 | 0.000409785708624514505 |

The exact rational strings in [EXACT_RESULT_VALUES.json](EXACT_RESULT_VALUES.json)
decide the inequalities. [DECIMAL_DISPLAY.json](DECIMAL_DISPLAY.json) is only
formatting of those saved strings. This is a small improvement of a fixed
negative threshold, not nonnegativity, a proof of RH, or evidence for a
sequence of thresholds tending to zero.

## What is proved and what is inherited

[PROOF.md](PROOF.md) proves the abstract shift-reuse inequality, the
no-improvement calculation for scalar continuity, and the form-domain
transfer. [ASSUMPTIONS.md](ASSUMPTIONS.md) states A1–A4/N1–N4 explicitly.
Those analytic-source, domain/action and physical-inclusion premises were
**not regenerated** by the 18 October calculation or this publication.
Hashes identify bytes; previous PASS labels do not prove those premises.

The fresh checker verified all 138,384 matrix locations (69,378 independent
triangular locations), all 372 row-radius sums, all 64+4 action-error
bounds, shifted scalar pads, the original C, a full factor residual and
inverse-factor bounds. It ran inside the single charged execution.
Implementation independence is not process isolation: the native runtime
already loaded by the producer remained mapped in the same worker.

## Start here

- [Exact result](EXACT_RESULT_VALUES.json), [scoped verdict](FINAL_SCOPED_VERDICT.json),
  [postflight byte/binding report](POSTFLIGHT_VERIFICATION.json).
- [Timed independent checker report](evidence/timed/math/INDEPENDENT_CHECK.json).
- [External terminal witness](evidence/host/EXTERNAL_TERMINAL_WITNESS.json) and
  [actual host tool transcript](evidence/ACTUAL_HOST_TOOL_TRANSCRIPT.json).
- [Reproduction and environment instructions](REPRODUCTION.md).
- [Source map](SOURCE_MAP.md), [failure history](FAILURE_HISTORY.md),
  [public file allowlist](PUBLIC_ALLOWLIST.json), [file hashes](MANIFEST.sha256).
- The separately published manuscript uses a commit-pinned URL to this
  artifact directory. Its PDF and single self-contained TEX are under the
  repository's `papers/2026-10-18-fixed-threshold-shift/` directory.

## Exact input and implementation identities

The frozen input manifest binds **63 roles / 62 distinct files**.
All of those files are included under `inputs/evidence/`, byte unchanged.

| Item | SHA-256 |
|---|---|
| Input manifest | `5bb28142e4bbc8fee7060467097db8b732fceb1564857b5dcca5ef3326b3fc58` |
| Original C | `c459b5c283020808e6d52ac60e3749137c11cd9db21e98fa5178ff0698ade513` |
| Executed plan | `b4b1dccccd64259ca7d2c91f4675340c178a6f947320339709bba7bbe2cffb49` |
| Independent checker source | `e6ba2e463ea098276a99ea03175051ff2b9b5cbce09b2e602edf1387bc5b2a2f` |
| Timed checker report | `962ca57e7e07b57e47874edf5742a0f98489f51da4a71288435ecbf8320781e1` |
| Exact result extract | `08d52ed1f96eaa5b987214c073625e283adad22349c67c01d6a22c344a6cfe25` |

## Execution limits and timing

The successful scientific launch was
`theta-full372-h2-star-fixedC-20261018-compat01`.
It used one scientific worker, one thread and one CPU; a 60-second
whole-tree wall/CPU-capacity limit; a 384-MiB worker address-space cap;
and a 320-MiB RSS cap. Input/scalar intervals used 160 bits, C and factor
serialization 80 bits, final model 100 bits, with a 1024-bit dense-integer
ceiling. There was one consumer, one factorization, one finite triangular
inverse, zero coefficient solves and zero scientific retries.

The external host interval, from before its first fork through actual
observer reaping and final ECHILD, was **20.839672121 seconds**. This also
bounds the aggregate CPU capacity on the one allowed CPU; it is not a
separately measured aggregate CPU usage. Observed RSS/HWM was **166,520 KiB**;
wait4 maxrss was 166,348 KiB. Actual host/observer/controller/worker exits
were zero and the registered tree was closed.

These figures exclude research preparation, review, manuscript compilation,
upload and file readback. They do not describe the duration of this publication
task. Runtime/ABI admission (CPython 3.12.14, python-flint 0.9.0, FLINT 3.6.0)
occurred inside the successful run. Resource validation assumes the recorded
trusted host/OS/native-source boundary; it is not a hostile-native-code sandbox.

## Historical records and publication scope

The frozen plan, contract and pre-execution proof deliberately retain their
historical PENDING/NOT-RUN text. The completed receipts and current documents
resolve that history; they are not silently rewritten. The earlier host
compatibility failure is separated in [FAILURE_HISTORY.md](FAILURE_HISTORY.md).
It happened before scientific work and is not a numerical counterexample.

This publication includes this fixed-shift result and its necessary evidence
only. No unpublished trace-paper package is included. Native runtime binaries
are not redistributed here; the prior public archive is an explicitly
hash-bound external dependency for reconstructing that runtime. The saved
arithmetic checker itself uses the Python standard library.

Author-owned original contributions follow the repository's CC BY-NC 4.0
license. Third-party components retain their own licenses. The author's public
contact block is retained in the manuscript; unrelated personal data, private
Drive indexes, credentials and delivery bearer URLs are excluded.

