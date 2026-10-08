# Independent centered-disc phase audit

Date: 2026-10-08. Scope: the single fixed-160-bit centered-disc phase repair and
its checkpoint-continuation requirements. No actual prime phase cache, new Gamma
values, polynomial products, H action, DFT, or physical integral was computed.

## Verdict

GO for exactly one explicitly approved checkpoint continuation, conditional on
successful final-code Work-native generic API fixtures and full runtime-identity
admission. This is an audit verdict, not authorization to execute. The original
worker/supervisor must not be rerun. No actual phase cache was generated here.

Reviewed final files in `phase_gate_audit_20261008`:

- `v2_action_PHASE_REPAIR_REVIEW_ONLY.py`, SHA-256
  `90805abe5756d3400f4609bdde7f3b70c64460f0fc32e113f5e13f0fc06737dc`.
- `v2_checkpoint_continue_REVIEW_ONLY.py`, SHA-256
  `368f9f54392f049d991222c48b749e63c8413101de1ad12403c170f94f1e5fa5`.

Any change to these files requires renewed review and hash-bound admission.

## Independently established evidence

- Baseline: `phase_gate_audit_20261008/work_artifacts/v2_j2_local_20261008`.
- The saved failure is the post-recurrence `all(... s.upper(v)<42 ...)` assertion
  in `v2_action.shared`, after exactly 741384 recurrence products and 8192 Gamma
  extension evaluations. No offending index or D ball was saved. The evidence
  cannot identify or reconstruct the exact failing numerical value.
- The baseline has the correct 18 ordered prime powers, weights
  `log(p)/sqrt(n)`, cGamma, 160-bit precision, k=0..41188, both-shift-sign factor 2,
  and absolute-value gate. Its repeated rectangular `z *= rho` has no wrapping
  control. The identified repair concerns that representation; it does not
  change the mathematical multiplier.
- The Gamma extension has 8192 records, 524288 bytes, denominator bits 140, and
  SHA-256 `bedc238709490a75279450e0dfd8462121d9cd4bd0513e61664d52896102c025`.
  Every record is positive; recorded maximum center/radius bit lengths match.
- All 114 files in the saved dependency manifest match their bytes and hashes.
  Copied python-flint 0.9.0 / FLINT 3.6.0 loads successfully in this local audit.
  At that point this established only consistency with the supplied manifest;
  the saved restoration report explicitly lacked original-wheel provenance.
- The separate data-only provenance audit subsequently resolved payload origin:
  all 112 non-RECORD official-wheel files, including 39 extensions and 3 bundled
  libraries, match the copied bytes. Official PyPI wheel SHA-256 is
  `376b88cacd30612479e839ffdba887599d3f9c8c0e214852bf80bb2b194e4d76`.
  The 114 manifest entries plus RECORD are the 115 copied files. Differences
  are ordinary installed RECORD/bookkeeping metadata. See
  `flint_provenance_check_20261008/PROVENANCE_RESULT.json` and its report.
  This establishes official package-payload identity, not the historical install
  chain, interpreter/system-library authenticity, mathematical correctness, or
  permission for new execution. No native execution was repeated after that
  provenance result.

## Outwardness and induction

The unchanged support helper obtains the exact dyadic midpoint of a finite ball
x, floors it onto the denominator-2^140 grid, and computes an outward absolute
upper bound for x minus that exact center. Exact rational arithmetic then rounds
the radius numerator up. Thus the record (c,r) encloses the entire x in
[(c-r)/2^140,(c+r)/2^140], including native subtraction rounding. It does not
retain only x's midpoint.

The reviewed primitive forms P = q_previous R using native 160-bit multiplication,
where q_previous is an exact dyadic point and R contains the particular exact
unit root rho. It applies the same outward recorder to both coordinates, chooses
the two recorded dyadic centers as q, and adds the two nonnegative radius
numerators to the prior integer E numerator without resetting it.

For the exact rho, |rho|=1. Hence

    |rho^k - q_k|_2
      <= |rho| |rho^(k-1)-q_(k-1)|_2 + |q_(k-1)rho-q_k|_2
      <= E_(k-1) + (r_real+r_imag)/2^140 = E_k.

The local L1 radius is an upper bound for the local Euclidean discrepancy. This
argument needs neither independence of errors nor a unit-modulus assertion for
every point in R. It retains all accumulated error. Re(q) +/- E therefore
encloses the exact cosine. Using the inflated rectangle as the next recurrence
operand, renormalizing q without a proved error charge, or resetting E would
break this implementation contract.

The constructor accepts exact dyadic tuples and rounds nonzero radii outward;
abs_upper returns an exact outward-rounded endpoint. These native API properties
are documented in the official [python-flint arb reference](https://python-flint.readthedocs.io/en/latest/arb.html).
Complex values use real and imaginary ball components as documented in the
[acb reference](https://python-flint.readthedocs.io/en/latest/acb.html).

## Native generic tests

`native_generic_fixture.py` executes the exact proposed primitive and only the
AST-extracted side-effect-free support helpers. It does not import or execute a
Work production module. At precision 160 and one thread, it checks:

- Eight rational unit roots: +/-1, +/-i, and all sign choices of (3+4i)/5.
- 129 steps per root, each compared to exact Fraction powers through the squared
  Euclidean-error inequality. All centers are exact, finite dyadics and all E
  updates equal the prior integer E plus the two local radius numerators.
- Entire local product-coordinate, cosine, serialized-record, and rehydrated
  enclosures, using exact midpoint/radius endpoints rather than overlap tests.
- Positive, negative, zero, off-grid, and zero-straddling serialization inputs.
- Rational interval-weighted sums and exact k=0 treatment.
- Strict absolute gates: +/-41 pass; +/-42 and intervals reaching beyond them
  fail. Negative D values are not rejected merely for being negative.

All checks pass. See `NATIVE_GENERIC_RESULTS.json`. These tests run copied Work
binaries in the local audit executor; their scope is the particular hash-bound
supplied runtime, subsequently matched to the official wheel as above.
Work-executor native API preflight is still required before a continuation, and
must exercise the final integrated core or prove its equivalence to the tested
primitive. The final fixture record must bind the repaired phase-code hash,
unchanged support-code hash, complete runtime manifest, precision 160, denominator
140, generic exact-unit roots and full-error roundtrip. The existing local result
is supporting evidence, not that Work admission record. These tests are not a
production runtime forecast or certification of actual D/downstream budgets.

## Integrated source audit

The AST scope check confirms that all original functions outside shared() are
unchanged. shared()'s Gamma prefix is unchanged and now delegates to the isolated
phase builder; the continuation calls only that builder. Exact constants were
independently checked by integer prime-power enumeration. There are 18 roots,
741384 nonzero-index center products, and 741402 weighted updates including DC.

The integrated recurrence uses q=1,E=0 at each root's k=0, then carries the full
integer E through k=41188. D updates consume outward restored cosine intervals,
not center-only values. The original weight intervals, cGamma, factor 2, and
downstream even-frequency D[abs(k)] convention are preserved. Completed-root
diagnostics and exact midpoint/radius records for the first bad native D are
saved. A complete-ball containment check and strict |D|<42 check apply after D
serialization/readback as well as before it. Packed 256-bit slot guards remain.

## Required single checkpoint continuation

The original one-use marker and failed attempt must remain immutable. A separate,
explicitly approved, hash-bound continuation record must name that attempt and
the repaired code. It must resume from the verified completed Gamma extension;
it must not call the old shared() path that recomputes the extension, or rerun
the original fresh-pilot worker/supervisor.

The reviewed adapter satisfies that design: it creates a distinct continuation
directory and exclusive marker, binds the parent's PID and approval hash, checks
the frozen original manifest and 91-source archive/extracted mapping, reuses the
Gamma/frame/old-node caches by hash, and cannot silently regenerate Gamma. Full
runtime-tree identity and native-fixture records are required before import.
Only j=2 production, its one polynomial DFT, and 437 kernels follow. The original
integer-only saved checker is scoped to the new output and its save destination
is intercepted so original verification evidence cannot be overwritten.

From `SUPERVISOR_TERMINATION.json`, charge prior wall 25.47436677800033 seconds and
prior CPU at least 25.447845 seconds (the exact sum of saved user/system fields).
For the same aggregate 600-second allowances:

- Remaining hard wall: 574.52563322199967 seconds.
- Remaining wall before the aggregate 590-second cooperative stop:
  564.52563322199967 seconds.
- Remaining hard CPU: 574.552155 seconds. An integer RLIMIT_CPU of 574 seconds is
  conservative; restarting at 600 seconds is invalid.
- Retain the 512 MiB address-space cap and 500 MiB cooperative RSS boundary.
- Include continuation startup, checks, serialization, and supervision; do not
  start budget clocks only around numerical kernels. Conservatively account for
  any additional charged setup or fixture work before deriving final deadlines.

The adapter conservatively uses continuation soft/hard wall and combined
worker/supervisor CPU thresholds of 564/574 seconds, a child CPU limit no greater
than 573 seconds, and a worker CPU soft stop of 563 seconds. Thus it does not
reset the old 600-second allowance. Actual recorded aggregate wall/CPU exceeding
600 produces an authoritative HOLD and nonzero exit even if the worker exits 0.
Signal delivery and accounting still have OS scheduling granularity; a completion
or in-limit runtime is not promised. Check the authoritative supervisor/final
status, not just a worker's earlier success record.

The phase builder must preserve full weight/log/root intervals, cosine E pads,
the exact D formula, strict full-ball |D|<42 gates and all downstream unchanged
error gates. Serialized D readback should also pass the strict gate, because
outward quantization can enlarge a pre-serialization ball. Both inner and outer
uses of D must consume that rehydrated enclosure. No success at this phase alone
authorizes more columns or removes the eJ, em, frame, B2, support, bit-length,
nonfinite, memory, or runtime gates.

## Audit records

- `INDEPENDENT_ARTIFACT_CHECKS.json`: immutable baseline identities, Gamma check,
  dependency verification, exact saved failure, and aggregate budget arithmetic.
- `NATIVE_GENERIC_RESULTS.json`: detailed native generic fixture outcomes and
  primitive/support hashes.
- `native_generic_fixture.py`: reproducible source-free fixture, with no
  production entrypoint.
- `PHASE_PATCH_SCOPE.json`: final repaired/adapter hashes and AST-scope checks.
- `STATIC_CONSTANT_CHECKS.json`: independent exact prime-power/support counts.
- `VERDICT.json`: machine-readable conditional verdict and execution boundary.
