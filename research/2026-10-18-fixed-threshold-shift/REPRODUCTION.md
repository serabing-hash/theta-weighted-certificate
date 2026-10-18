# Reproduction levels and environment

## 1. Verify this distribution without mathematical replay

From this artifact directory:

```sh
sha256sum -c MANIFEST.sha256
python3 tools/verify_archive.py
```

The script reads bytes, manifests, dimensions recorded in reports and exact
string equalities. It imports no producer, matrix checker or native runtime,
and does not recalculate any matrix, factor, scalar margin or decimal.
This is the verification performed during publication. It is not a new
independent numerical replay. Decimal displays were separately formatted
from the saved exact rational strings with Decimal.

The original timed result is evidence/timed/math/INDEPENDENT_CHECK.json.
The original host measurement is evidence/host/EXTERNAL_TERMINAL_WITNESS.json;
the actual tool exit is evidence/ACTUAL_HOST_TOOL_TRANSCRIPT.json.
The former provisional report's resource-pending label is preserved; the
external witness and actual exit resolve it without rewriting the report.

## 2. Optional reader-side saved arithmetic replay

The frozen checker has no native dependency and imports no producer helper.
A separately provided adapter, tools/replay_saved_checker.py, copies exactly
the 16 checker inputs to a new directory, uses the original launch metadata
as provenance, and invokes the unchanged checker with a new local time limit.
**This adapter was syntax-reviewed, but it was not executed during publication.**
Its output is a new reader replay, not the original process/resource receipt.
The original checker emits a historical literal stating that native mappings
remain present; the adapter preserves that raw report and writes a mandatory
REPLAY_CONTEXT.json clarifying that this literal does not describe the
standard-library-only reader process. No original resource claim is replayed.

The original checker binds the source root by absolute path. On an isolated
Linux filesystem, expose this distribution's inputs/evidence at exactly:

```text
/workspace/shared/theta-full-certificate-shift-preparation-delivery-20261018/source/evidence
```

Use a bind mount, not a symlink whose resolved path differs. The adapter
checks the path and original manifest hash; it does not patch the checker,
modify an input manifest or weaken an admission predicate. Then, with
CPython 3.12.14 and a fresh writable output directory:

```sh
python3 tools/replay_saved_checker.py --output /fresh/replay-output
```

For example, an independently prepared Linux container can mount this
artifact directory read-only, bind inputs/evidence read-only at the exact
path above, disable networking, and provide one fresh writable output
directory. No specific container image digest is claimed. The adapter enforces
a 60-second local wall/CPU fallback, 384-MiB address-space limit, 320-MiB
observed RSS cap, one CPU and no descendant creation under a non-root user.
The original 20.839672121-second whole-tree receipt cannot be recreated by
this saved-checker-only replay. Stop on any failed obligation; do not interpret
a timeout or portability failure as mathematical nonpositivity.

## 3. Historical producer and full-run reproduction

frozen/ contains the exact executed source, host, plan, commands and fixture.
The plan records CPython 3.12.14 (executable SHA-256
fa67443527ed9647f760d807e2a38f26340757123e643c4639cf273ed15d5ea7),
python-flint 0.9.0, FLINT 3.6.0 and the archived 115-payload runtime manifest.
The runtime files are available in the prior public archive linked in
SOURCE_MAP.md. They are not copied into this publication, and third-party
licenses remain applicable. Version strings alone do not establish ABI
identity; historical runtime hashes and the timed runtime receipt do.

Historical full commands are environment-bound, single-use commands,
not a portable one-command installer. Reconstructing the original full
host requires the bound source/contract/plan paths, original runtime bytes,
Linux pidfd/subreaper/prctl/procfs/rlimit support, CPU 0, non-root identical
real/effective/saved/fs identities, zero capabilities including the bounding
set, and no-new-privileges. The frozen host and fixture sources specify the
complete admission predicates. Do not reuse the spent launch identity or
overwrite its attempt directories. A new reproduction needs its own isolated
plan/release and process audit; resulting plan/receipt hashes will differ.

No producer, source/H action, quadrature, matrix factorization, coefficient
solve or checker replay was run to prepare the paper. This publication
provides saved inputs, complete outputs, exact source and environment
premises; it does not claim a newly tested hermetic end-to-end environment.

## 4. Manuscript compilation

The single TEX includes its bibliography and needs no external data,
figures or bibliography files. With TeX Live packages used in the preamble:

```sh
pdflatex -interaction=nonstopmode -halt-on-error fixed_threshold_shift.tex
pdflatex -interaction=nonstopmode -halt-on-error fixed_threshold_shift.tex
```

Compile in an empty build directory to keep generated files separate.
The publication PDF was compiled from that exact TEX and inspected on every
page. Its artifact URL pins the data/source commit, avoiding a circular
reference to the later paper commit.

