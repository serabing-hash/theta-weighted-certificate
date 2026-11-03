# Corrected a2048 generation: execution and scope

The directed-integer-power profile completed source regeneration, T, G, all
33 Gamma phases, the full residual model, all 5,120 K cells, both final gates,
and fresh exact integer sign checks. This is a completed execution of the
specified corrected producer, not only a replay of saved matrix signs.
It is **not a second independent implementation or proof-assistant formalization**.
The analytic, domain, source-inclusion and whole-tail premises stated in the
manuscript and numerical contract remain part of each application.

## What changed

The original Decimal endpoint-power primitive has a demonstrated general
outward-enclosure defect. Directed rounding of that power operation did not
suffice. The separate corrected profile uses sign-aware directed multiplication
for integer powers; all other selected scientific modules are byte-preserved.
See [the repair argument and exact tests](corrected/INTEGER_POWER_REPAIR.md).

The historical profile and its identities have not been rewritten. Historical
`CERT` output or same-code replay alone cannot discharge this arithmetic
obligation. The corrected a2048 execution does **not** by association repair the
distinct historical a1024 enclosure run. The public a1024 integer certificates
remain valid as exact statements about their stored matrices.

The corrected run produced 142 outward scientific endpoint changes:

- Two G cell-weight lower endpoints moved downward. The rational G matrix is unchanged.
- Five residual-model ledger endpoints moved upward. The model and coefficient-radius NPZ archives are unchanged.
- The shifted LDL computation changed 135 endpoints across pivots 188 through 255. Exact rational comparison verifies that all 68 changed intervals contain their old counterparts and that every one of the 256 corrected lower endpoints is positive.

These are real scientific-field differences, not timing metadata. They do not
by themselves prove that an older endpoint missed its particular true value.
The complete old/new field evidence is retained in
[G_SCIENTIFIC_CHANGES.json](corrected/reports/G_SCIENTIFIC_CHANGES.json),
[MODEL_SCIENTIFIC_CHANGES.json](corrected/reports/MODEL_SCIENTIFIC_CHANGES.json), and
[LDL_SCIENTIFIC_CHANGES.json](corrected/reports/LDL_SCIENTIFIC_CHANGES.json).
No historical expected hash was replaced to force a match.

## Execution evidence

The [complete corrected-run report](corrected/reports/CORRECTED_REVALIDATION_REPORT.json)
binds the executed code and output hashes. The
[full comparison](corrected/reports/FULL_CORRECTED_COMPARISON.json) records all
142 outward scientific endpoint changes, 21 direct compact-file comparisons,
and 327,680 unchanged exact matrix entries.
[Report-name mapping](corrected/reports/EVIDENCE_NAME_INDEX.json) preserves the
original names used in its evidence hash map while locating the public copies.

| Stage | Actual checked outcome | Evidence |
|---|---|---|
| Exact frozen candidate and source components | Candidate bytes retained; moments, coordinate bounds, geometry and complete source-tail fields recomputed | [Source identity](corrected/reports/SOURCE_REGENERATION_IDENTITY.json) and the frozen-output verifier |
| T and G | Fresh finite enclosures; all 65,536 rational matrix entries per matrix equal the compact sign packet | [Corrected-to-compact comparison](corrected/reports/CORRECTED_TO_COMPACT_BINDING.json) |
| Gamma | All 33 phases from zero; full 571,867,213-byte archive matches its authenticated reference | [Execution identity](corrected/reports/GAMMA_EXECUTION_IDENTITY.json), [archive comparison](corrected/reports/PRODUCTION_ARCHIVE_COMPARISON.json) |
| Residual model | Full model and coefficient-radius archives regenerated; ledger changes explicitly recorded | [Model identity](corrected/reports/MODEL_EXECUTION_IDENTITY.json), [archive identities](corrected/reports/CORRECTED_TO_HISTORICAL_ARRAY_IDENTITIES.json) |
| K | All 5,120 cells from zero, with all 80 exact-prefix checkpoint boundaries; terminal CERT | [K identity](corrected/reports/K_EXECUTION_IDENTITY.json), [full historical comparison](corrected/reports/K_CORRECTED_TO_HISTORICAL_COMPARISON.json) |
| Stronger gate | Terminal CERT; 256 strictly positive shifted interval LDL pivots; exact independent congruence check | [Fresh sign report](corrected/reports/FRESH_GATE_SIGNS.json) |
| Conservative gate | Terminal CERT_EXACT_INTEGER_SIGN; exact independent congruence check | [Fresh sign report](corrected/reports/FRESH_GATE_SIGNS.json) |
| Fixed retained margin | Original fixed beta and witness rows applied to fresh corrected inputs; 256 strict congruence margins and 256 positive row gaps proving U < 4060 I | [Retained-margin report](corrected/reports/FRESH_RETAINED_MARGIN_REPORT.json), [input hashes](corrected/reports/FRESH_RETAINED_MARGIN_INPUTS.json) |

The [fresh hash-chain report](corrected/reports/FRESH_HASH_CHAIN.json) passes all
59 checked file references. The fresh sign checker reconstructs all 65,536 entries of each sufficient
matrix and performs both full integer congruences. Each has 256 strict positive
diagonal-dominance margins. Successful process exit alone was not the gate:
terminal JSON statuses, pivot bounds and exact signs were checked separately.

The compact comparator independently checks G, K, T, F and both sufficient
matrices against the public exact-arithmetic packet. Every matrix entry matches.
This explicitly rebinds the same compact mathematical data to corrected
production; its original extraction provenance remains unchanged. The fixed
retained-margin check therefore remains reproducible through the public exact
checker after this fresh-output comparison. Its analytic consequence remains
conditional on the stated operator bridge, with rounded-down coefficient
0.499640243163, not the global half inequality.

K's scientific fields and raw Gram arrays match the authenticated historical
record. Its full JSON hash differs because elapsed time and the referenced
model-result identity differ. Both sufficient M files are byte-identical to their
historical counterparts, while the stronger gate's LDL intervals have the
scientific differences described above. File identity, mathematical-field
identity and enclosure correctness are deliberately separate claims.

## Code, storage and environment

The native execution identity enumerates 23 source modules. The curated runtime
selection includes all 19 scientific/runtime dependencies and omits four unused
orchestration modules; their identities remain recorded in
[CURATED_SOURCE_SELECTION.json](corrected/reports/CURATED_SOURCE_SELECTION.json).
A regenerated identity report from this selected directory will enumerate those
19 files instead. It need not be byte-identical to the archived native report.
All 37 producer unit tests passed from the staged selected directory, as recorded
in [STAGED_UNIT_TESTS.json](corrected/reports/STAGED_UNIT_TESTS.json).
A separate copied-only recipe check passed all 20 comparator, storage and
checkpoint fixtures plus both exact preflights, with private workspace access,
network and child execution blocked. See
[STAGED_RECIPE_TESTS.json](corrected/reports/STAGED_RECIPE_TESTS.json).
This is not another complete production run.

The disk-backed adapters preserve the original arithmetic expressions, full BLAS
shapes, phase/cell order and accumulation order. Gamma checkpoints store complete
phase prefixes. K checkpoints store the exact accumulated midpoint/radius,
trace and weight prefix before final symmetrization. The successful corrected
run started from zero; it did not treat an interrupted historical log as a
checkpoint. Resumption and rejection paths also have executable focused tests.

This release supplies the tested numerical bodies and a complete recipe, rather
than claiming a second complete production execution from a clean download of
the curated directory. The small copied-only integer/scalar replays and staged
unit tests are separate portability checks. Follow the
[regeneration guide](README.md), including its source guards, dependencies,
checkpoint rules and final comparison/sign steps.

Full production depends on the recorded Python, NumPy, SciPy, mpmath, Decimal,
BLAS/CPU and thread environment. The compact integer verifier does not require
reference-identical floating proposals. A different production digest is a
replay discrepancy, not automatically a negative theta direction; new differing
enclosures require their own validated bounds and exact sign evidence.
Never replace expected hashes merely to force PASS.

Neither this execution nor its integer certificates prove the global half
inequality, positivity on an unidentified different low space, or RH.
