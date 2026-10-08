# Phase checkpoint review packet — 8 October 2026

**REVIEW ONLY / NO EXECUTION.** Author-original research, code and documentation: **CC BY-NC 4.0**, © 2026 Jongmin Choi. [License](https://creativecommons.org/licenses/by-nc/4.0/). Third-party material retains its own terms.

This small, UTF-8 text packet supports an independent mathematical and important-choice review of one proposed bounded checkpoint continuation. It does not authorize a run, certify a successful repair, or prove RH. All code is supplied for reading only. Do not run source evaluation, phase generation, H action, DFT, Gram computations, a pilot or the continuation from this packet.

## Read first

1. [D-phase audit](phase/REPORT.md), [repair proof](phase/REPAIR_PROOF.md), and [continuation contract](phase/CONTINUATION_REVIEW_NOTES.md).
2. [Final phase source](phase/v2_action_PHASE_REPAIR_REVIEW_ONLY.py), [exact baseline-to-repair diff](phase/v2_action_PHASE_REPAIR.diff), and [final continuation adapter](phase/v2_checkpoint_continue_REVIEW_ONLY.py). The unchanged supporting and original worker/supervisor source is in [baseline](baseline/).
3. [Independent centered-disc audit](centered/REPORT.md) and [generic fixture records](centered/NATIVE_GENERIC_RESULTS.json). Treat the claimed checks as evidence to inspect, not authority to inherit a PASS label.
4. [Official-wheel provenance result](provenance/PROVENANCE_REPORT.md) and [restoration/license limits](provenance/RESTORATION_AND_LICENSES.md).
5. [Earlier delta64 diagnosis](context/DIAGNOSIS_REPORT.md), [four-direction admission](context/ADMISSION_REPORT.md), [current action contract](context/CONTRACT_REPORT.md), and [mixed-Gram contract](context/MIXED_GRAM_CONTRACT.md).
6. [Supplied mathematical bridge argument](bridge/PROOF.md) and [primary formula references](bridge/SOURCES.md). This is an argument awaiting the present independent review, not an externally certified theorem. Its mathematical body is preserved; the sole introductory edit is recorded in [the exact diff](bridge/INTRODUCTION_ONLY.diff).

## Status and decision boundary

The ultimate goal is RH. The existing finite result is a fixed 1/32 spectral exclusion for the specified minimum closed even weighted operator, conditional on explicit analytic-source and numerical-inclusion premises. It is not global positivity. The bridge claims an equivalence between global positivity of that same operator and RH; a reviewer must mark any part not independently checked as unverified. Global positivity itself remains unproved.

Saved finite-math certificates report a lower bound of −4×10⁻⁹ only on the existing 64-dimensional trial span. The old fixed-G64 residual model exceeds 1.48 for every coefficient matrix C, and has at least four model modes above 1.08. Four new frozen directions are domain-valid and nonredundant, conditional on inherited inclusion premises; none of their new H actions is complete. Model eigenvalues are not physical-operator eigenvalues.

One guard pilot consumed 25.474366778 wall seconds and 25.447845 CPU seconds. It completed 8192 new Gamma multipliers and 741384 phase recurrence products, then failed the strict absolute-D gate. The first failed D index and ball were not saved. Repeated rectangular-ball wrapping is a source-supported instability explanation, not a reconstructed numerical proof of the exact failure. No polynomial/action/DFT/physical-Gram stage followed.

The repair retains native 160-bit arithmetic and exact denominator-2^140 centers, with a nonresetting integer Euclidean error bound. The complete error must remain in cosine, D, serialization and both downstream D uses. The continuation reuses accepted Gamma bytes without reevaluation. Its proposed scope is one fixed zero-based j=2 column through one DFT and 437 kernels, with no other columns or final consumer. It preserves the original failed attempt.

The proposed additional hard wall/monitored CPU limit is 574 seconds, with soft stop 564 seconds, conservative child CPU cap at most 573 seconds, 512 MiB address-space limit and 500 MiB cooperative RSS gate. Prior usage remains charged; measured aggregate wall or CPU above 600 seconds means HOLD, even if the worker returned success. These are stopping limits, not a completion guarantee. Actual-executor runtime admission, generic fixtures and separate explicit execution authorization remain necessary.

Neither this pilot nor a future single 1/64 certificate would establish global positivity or RH. The review should decide whether the bounded continuation yields meaningful information for the ultimate goal, distinguish finite-threshold improvement from a global argument, and state precise stop criteria and any fatal gap.

## Exact identities

- Final phase source SHA-256: `90805abe5756d3400f4609bdde7f3b70c64460f0fc32e113f5e13f0fc06737dc`
- Final adapter SHA-256: `368f9f54392f049d991222c48b749e63c8413101de1ad12403c170f94f1e5fa5`
- Reused Gamma extension SHA-256: `bedc238709490a75279450e0dfd8462121d9cd4bd0513e61664d52896102c025` (524288 bytes, 8192 records; metadata only here)
- Official python-flint wheel SHA-256: `376b88cacd30612479e839ffdba887599d3f9c8c0e214852bf80bb2b194e4d76` (wheel not included)
- Separately existing review ZIP SHA-256: `5e1e03ce1da53c1aa639a198aa4d6065d65768d8776c8a30ec83d1c8ee6d5284` (33897 bytes; not needed or included here)

## Evidence levels and chronology

The inherited source/physical-Gram enclosures are explicit premises. Saved-data rational checks establish finite conclusions conditional on those enclosures; they do not independently regenerate their physical inclusion. Small scalar certificates and the frozen X40/Y40 data are in [evidence](evidence/). This review need not reconstruct the large historical physical certificate or obtain binary inputs just to evaluate the self-contained repair argument and static continuation contract.

The phase audit's runtime-provenance warning describes its earlier state. The later provenance audit found all 112 non-RECORD official-wheel files byte-identical to the copied payload, including 39 extensions and 3 bundled libraries. This updates package origin only. It does not certify the historical installation, interpreter/system libraries, mathematical correctness, or any new execution. Local generic checks are not a substitute for actual-executor checks.

## Packaging and preservation

All Python files, result JSON files, baseline source, and mathematical body of the bridge are byte-preserved from the cited source artifacts. Four prose copies have limited publication-only wording changes; [PUBLICATION_EDITS.json](PUBLICATION_EDITS.json) records them, and [SOURCE_FILE_IDENTITIES.json](SOURCE_FILE_IDENTITIES.json) records original and published sizes and hashes. Ordinary research Drive provenance links remain. The bridge introduction has a separate exact diff.

[MANIFEST.sha256](MANIFEST.sha256) is the authoritative manifest for this packet, covering every other file in this dated directory at publication. [FILE_SIZES.json](FILE_SIZES.json) records exact content sizes/hashes. The older `phase/AUDIT_MANIFEST.json` records its original source audit and includes files outside this selected packet; it is not this packet's manifest. Relative source paths in historical reports refer to their original packages unless a packet link is supplied here. Restored source files retain their original import/layout assumptions and do not form a runnable installation here.

No runtime binaries, wheel, Gamma cache bytes, large input archives or unrelated logs are included. The text is sufficient for the stated static decision review, but is deliberately insufficient to start the numerical workload. No numerical source or native dependency was executed during this publication.

Third-party runtime licenses are not replaced by CC BY-NC 4.0. The provenance folder records their upstream MIT/LGPL/GPL notices and boundaries without redistributing runtime files. No complete binary-redistribution compliance certification is claimed.
