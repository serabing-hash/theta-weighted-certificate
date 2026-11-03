# a2048 corrected source-enclosure regeneration

The **corrected/** profile is the primary regeneration route. The original
producer and its reports are preserved separately under
[historical/](historical/README_ARITHMETIC_HOLD.md): its Decimal integer-power
primitive has a demonstrated outward-enclosure defect. A historical printed
`CERT` or matching output digest is not a remedy for that defect.

The corrected profile replaces only the scientific integer-power implementation
by sign-aware directed multiplication. It also uses separately reviewed
storage/checkpoint adapters. This is the same producer family with a documented
arithmetic repair, **not a second independent implementation or a formal proof**.
The [generation validation report](GENERATION_VALIDATION.md) distinguishes
primitive tests, actual dependent production, comparisons and exact final signs.
A repaired primitive alone is not a completed corrected source replay.
The [repair note](corrected/INTEGER_POWER_REPAIR.md) gives the counterexample,
one-sided multiplication argument, exact-rational tests and complete power-site
inventory. The historical numerical notes describe the intended analytic
contract and must be read with their arithmetic-hold notice.

The exact candidate remains a = 1/2048, B = log(8)/2, k = 256, 3072 positive-side
cells, mesh width 1/2560, support [-6/5, 6/5], SHA-256
`a9294f657d5c5bb2cdf6859f1370894af141457d03f83fcf5d6294029de5520d`.
It contains exact frozen dyadics, not enclosures of a fresh floating solve. The
residual cutoff is exactly 2. No new candidate search is required.

## Dependencies and preparation

Read [DEPENDENCIES.md](DEPENDENCIES.md). The recorded libraries are Python
3.12.14, NumPy 2.3.5, SciPy 1.17.0 and mpmath 1.3.0; the audited runtime uses
libmpdec 4.0.0. Version strings alone are not a full BLAS/CPU specification.
Check the release SHA-256 manifest before running commands. Enter `corrected/` as shown below; the remaining commands use that working
directory, with new output and scratch directories.

```sh
set -eu
unset PYTHONOPTIMIZE
export OPENBLAS_NUM_THREADS=1
export PYTHONDONTWRITEBYTECODE=1
cd corrected
python3 -m unittest discover -s tests -v
python3 ../test_public_verifiers.py -v
python3 adapter/test_storage_adapters.py --source-dir src -v
python3 adapter/test_Gamma_checkpoints.py --source-dir src -v
python3 adapter/test_K_checkpoints.py --source-dir src -v
python3 src/check_preflight.py
python3 src/check_reference_closure.py
```

The last two commands write exact rational reports under `inputs/`. The tests
include synthetic rejection/storage/resumption fixtures; they are not substitutes
for complete source production. Do not disable assertions with Python `-O`/`-OO`.

## 1. Restore the exact definition and recompute source components

```sh
python3 ../unpack_candidate.py --output work/input/candidate.json
python3 adapter/regenerate_frozen_components.py \
  --source-dir src --candidate work/input/candidate.json --output results/frozen256_n3072
python3 ../verify_frozen_outputs.py --frozen results/frozen256_n3072
```

Only the candidate is unpacked. Source moments, actual coordinate rank bound,
source scalar, mean/tail bounds, derivative trace and geometry are recomputed.
The omitted diagnostic floating-solve archive is not a hidden prerequisite.
The comparison checks all scientific source fields and raw geometry arrays
against the explicitly labeled reference; copied files alone are not execution.

## 2. Produce all finite enclosures sequentially

```sh
python3 src/verify_energy_lower.py \
  --candidate results/frozen256_n3072 --output results/T256_n3072 --labels 1024
python3 src/verify_gram_upper.py \
  --candidate results/frozen256_n3072 --output results/G256_n3072
python3 adapter/run_gamma_checkpointed.py --source-dir src \
  --candidate results/frozen256_n3072 --output results/gamma256_n3072 --scratch work/storage/Gamma \
  --checkpoints work/checkpoints/Gamma --degree 32
python3 ../verify_production_archives.py --reference inputs/PRODUCTION_ARCHIVE_REFERENCE.json --gamma results/gamma256_n3072
python3 adapter/run_model_disk_backed.py --source-dir src \
  --candidate results/frozen256_n3072 --gamma results/gamma256_n3072 --output results/model256_n3072 \
  --scratch work/storage/model
python3 ../verify_production_archives.py --reference inputs/PRODUCTION_ARCHIVE_REFERENCE.json --gamma results/gamma256_n3072 --model results/model256_n3072
python3 adapter/run_K_checkpointed.py --source-dir src \
  --candidate results/frozen256_n3072 --model results/model256_n3072 --output results/K256_n3072 \
  --scratch work/storage/K --checkpoints work/checkpoints/K --weight-refinement 16
```

The source guard pins all 19 selected scientific modules. The archived native
execution identity lists 23 snapshot modules, including four unused orchestration
modules omitted from this runtime selection. A fresh public run therefore records
the selected module set; identity-report bytes need not match the archived record.
See [the selection record](corrected/reports/CURATED_SOURCE_SELECTION.json).
Storage adaptations
retain full BLAS shapes, phase/cell order and the reviewed arithmetic sequence;
they do not split or reassociate the Gram accumulation. Complete residual tails
and all stated prime-power terms remain required. No optional diagnostic NPZ or
hidden scalar cache is used.

Gamma commits independent phase rows atomically; K commits its exact accumulated
midpoint/radius, trace and weight prefix every 64 completed cells, **before** final
symmetrization. Only a complete, hash-bound checkpoint is accepted; log progress
is never state. Candidate, source, helpers, configuration and arithmetic
environment must match. A complete K prefix receives final symmetrization exactly
once. Do not delete identity checks or combine checkpoints from different
executions to force a resume.

For resumption, first establish that the old writer has terminated. Preserve its
partial output and scratch under distinct names, then run the same command with
`--resume`, the same checkpoint directory, an empty canonical output directory
and new empty scratch. Keep the `results/*` names shown above: the final reference
and sign checkers deliberately use that layout.

A lost connection alone does not establish termination. If an old writer may
still be live, do not reuse its output or checkpoint paths. Use a new isolated
working root with the same canonical `results/*` layout, byte-identical upstream
inputs and code, and a copied, verified complete checkpoint prefix. Copy only
committed generations, not partial staging directories or logs. The checkpoint
identity is bound to content, configuration and arithmetic environment rather
than an absolute path; the resume command must still validate the entire copied
prefix. Keep the two executions' writable directories separate.

## 3. Check both fresh gates and the retained-margin consequence

```sh
python3 src/run_gate400.py \
  --candidate results/frozen256_n3072 --T results/T256_n3072/T_lower_exact.json \
  --G results/G256_n3072/G_upper_exact.json --K results/K256_n3072/K_upper_exact.json \
  --gap 1/2000 --output results/gate256_n3072_p400
python3 adapter/run_conservative_gate.py \
  --source-dir src --exact-checker adapter/exact_congruence.py \
  --candidate results/frozen256_n3072 --T results/T256_n3072/T_lower_exact.json \
  --G results/G256_n3072/G_upper_exact.json --K results/K256_n3072/K_upper_exact.json \
  --output results/conservative_gate
python3 adapter/check_fresh_gate_signs.py --fresh . \
  --exact-checker adapter/exact_congruence.py --output work/FRESH_GATE_SIGNS.json
python3 adapter/verify_corrected_hash_chain.py \
  --root . --output work/FRESH_HASH_CHAIN.json
python3 ../verify_enclosure_outputs.py \
  --frozen results/frozen256_n3072 --T results/T256_n3072/T_lower_exact.json \
  --G results/G256_n3072/G_upper_exact.json --K results/K256_n3072/K_upper_exact.json \
  --exact-gate results/gate256_n3072_p400/sufficient_gate_exact.json \
  --conservative-gate results/conservative_gate/sufficient_gate_exact.json
python3 ../../reproducibility/replay_saved_gates.py --parameter 2048
python3 ../../reproducibility/replay_a2048_retained_margin.py
```

A producer can exit normally while reporting `FAIL`: check the JSON status, all
256 positive shifted pivots and the exact integer signs, not just the exit code.
The comparison requires every regenerated matrix/scalar to match the public
exact-sign inputs; the separate integer replays then bind their signs and fixed
retained-margin extraction. The comparison itself does not prove regeneration
was performed. The conservative floating witness is a proposal only; its signs
are checked with exact integer products.

## Reference equality is not the definition of mathematical correctness

The explicitly selected corrected production reference has its own identity;
the historical reference in the shared parent `inputs/` remains unchanged.
Equality, when actually achieved
by corrected production, can bind the same saved mathematical data to new
execution evidence. A repaired run is not required in principle to reproduce
unsafe historical arithmetic: different enclosures need their own validated
bounds, identities and finite sign report. **Never replace expected hashes or
weaken checks merely to force PASS.**

The compact saved-data verifier uses exact integers/rationals and does not depend
on a new floating proposal. Full generation additionally depends on BLAS, CPU,
Decimal and other implementation details. A digest mismatch is a replay
discrepancy, not automatically a negative theta direction. Checkpoint bindings
are deliberately stricter than library version strings.

Fresh diagnostic proposals are different experiments. Do not rewrite the frozen
candidate identity to make a new solve appear to be the historical input.

## Scope

The a2048 corrected execution does not automatically repair the distinct a1024
historical run. All operator applications retain their complete-domain, source
inclusion and analytic premises. See the integrated paper and
[data-availability map](../DATA_AVAILABILITY.md). The restricted low-space theorem
does not identify its low space with the sharp-cut numerical source space or
supply a positive unshifted low margin. The global half inequality and RH remain
unproved.
