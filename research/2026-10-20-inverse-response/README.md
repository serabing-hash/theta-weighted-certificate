# Shared action errors and rank-one inverse-response certificates

Jongmin Choi, 20 October 2026. Conditional mathematical research.
`RH_PROOF=NOT-OBTAINED`.

This directory accompanies *Shared Action Errors and Rank-One Corrections for Coercive Inverse Responses*. It provides two unchanged executed mathematical checkers, their unchanged exact reports, ten commit-pinned public mathematical inputs, safe historical evidence projections, and a portable reader replay path.

The main analytic contribution is retaining the same action error in the energy and residual terms, then combining that bound with the inverse-slack correction obtained from one exact action. The paper states the assumptions and proves the validity and scope of each finite upper certificate. It does not prove the theta-specific physical premises.

| Item | Supported conclusion |
|---|---|
| Joint shared-error and padded Gram bounds | Proved abstractly under the stated hypotheses. |
| Saved shared-error test | Its fixed majorant is excluded. The stronger saved common-base sign also excludes the specified fixed-coefficient Young families. |
| Saved rank-one test | Positive certified corrections; final result **INCONCLUSIVE**. |
| Precision-only capacity theorem | Proved, but **not evaluated** at the saved numbers. |
| Finite-rank, Schur and single-target reductions | Proved for exact actions; **not applied** to this instance. |
| Adequacy ledger, dominant-loss identification, new trials | Proposed and **not performed**. |

Neither finite result is a lower bound on the true inverse response, a negative direction of the actual theta operator, an exclusion of all coefficients/rank-one methods, or an RH proof/counterexample.

## Reproduction boundary

Start with [REPRODUCTION.md](REPRODUCTION.md). The ten dependencies total **10,071,362 bytes** and are individually pinned to existing public commit `f61c7af23c7e4027cc3cb768faa40273f1146ffd`; no Drive account, private path, native mathematics library, or inherited ZIP is required for the optional arithmetic replay. [INPUTS.json](INPUTS.json) records every URL, SHA256, byte count, and restoration path.

The new adapter has been **statically reviewed but not scientifically executed during publication**. The recorded historical tests were each executed once. The adapter preserves their arithmetic bodies and compares full report trees, omitting only three declared provenance fields. It replaces the original absolute-path/interpreter/private-admission chain with public byte admission. It does **not** reproduce the original host process evidence or regenerate the physical inputs.

Package byte verification, dependency restoration, safe extraction and Python syntax checks do not execute either mathematical checker. A successful package check is not a successful replay or a mathematical PASS. A failed or missing result is always HOLD.

## Contents

- `code/shared_checker.py`, `code/rank_one_checker.py`: unchanged executed mathematical source, including historical comments.
- `code/public_worker.py`: clearly separate public admission adapter; original `run`/`evaluate` arithmetic is retained.
- `results/shared_error.json`, `results/rank_one.json`: byte-identical exact historical reports.
- `INPUTS.json`: complete mathematical replay dependency closure.
- `verify_package.py`: source-free byte, restoration and syntax checks.
- `replay_once.py`: optional, explicit, bounded, single-use reader execution.
- `safe_extract.py`: hash/size-checked ZIP extraction to a fresh directory.
- `PROVENANCE.json`, `evidence/`: safe projections and original identity links.
- `PACKAGE_MANIFEST.json`: complete local payload allowlist and hashes, excluding itself and separately pinned downloads.
- `ASSUMPTIONS.md`: inherited premises, excluded claims and verification limits.

The companion PDF and self-contained TeX are published separately in the repository's `papers/2026-10-20-inverse-response/` directory and together with this directory in the release reproduction ZIP. The manuscript identifies the actual fixed artifact commit; use that pin rather than a moving branch.

Author-owned material follows the repository's existing CC BY-NC 4.0 license. Third-party software retains its own license. No runtime binary or additional legal agreement is supplied.
