# Dependencies and resource boundary

`inputs/environment.json` preserves the original producer's recorded Python
3.12.14, NumPy 2.3.5, SciPy 1.17.0 and mpmath 1.3.0 versions on x86-64 Linux.
`requirements-recorded.txt` records the three Python packages. The audited runtime
uses Decimal 1.70 and system libmpdec 4.0.0. This is not a complete OS/compiler/
BLAS/container lockfile or a guarantee of byte-identical floating proposals.
No dependencies were installed to prepare this public source copy, and no
third-party package source is redistributed here.

The primary route is `corrected/`, not the original `historical/src/`. The
historical 31-test success remains recorded, but missed a demonstrated integer-
power enclosure defect. The corrected primitive uses directed multiplications
instead of Decimal power. The original 31 tests and six additional exact-rational
power test groups passed for the repaired profile; this does not by itself
establish complete corrected production. See `GENERATION_VALIDATION.md` for
actual stage execution and sign evidence.

From this directory, with dependencies already installed:

```sh
OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 \
  python3 -m unittest discover -s corrected/tests -v
```

Full generation is substantially more expensive than the compact exact-matrix
replay. The retained historical Gamma array was 571,867,213 bytes; residual model
and coefficient-radius archives were 159,969,753 and 247,958,912 bytes. They are
not included as downloads. Disk-backed scratch buffers, exact-prefix checkpoints
and fresh outputs require additional space. Plan for multiple gigabytes of work
data, with extra headroom for interrupted attempts. No portable peak-memory or
runtime guarantee is established; a small source download is not a memory budget.

Original high-memory Gamma execution and an early storage-only retry were
interrupted without a mathematical assertion failure. Later storage/lifetime
adapters preserve the numerical operation order while reducing resident
allocation. Checkpoint adapters preserve exact state and refuse incompatible
resumption. Historical resource measurements in `HISTORICAL_RESOURCES.json`
remain observations of that run, not timings of the repaired profile or promised
performance. Do not infer completed corrected K production from an earlier
partial log.

The corrected run records its per-stage timings in
[CORRECTED_REVALIDATION_REPORT.json](corrected/reports/CORRECTED_REVALIDATION_REPORT.json).
For scale, Gamma took about 1,358 seconds and K about 3,355 seconds in that
execution. These are observations under that environment and workload, not
portable completion-time or resource guarantees.

A checkpoint binds library/Decimal versions and context, NumPy error policy,
BLAS configuration, CPU dispatch, relevant thread settings and code/input hashes.
`OPENBLAS_NUM_THREADS=1` is mandatory for the supplied checkpoint route. A changed
binding must not be bypassed. Use the documented fresh-output procedure instead.

Cross-platform digest differences are replay discrepancies, not by themselves
negative theta directions. Differing regenerated enclosures or witnesses need
their own validated bounds, identity and exact sign report. Do not change expected
hashes, candidate identities or acceptance conditions merely to obtain PASS.
