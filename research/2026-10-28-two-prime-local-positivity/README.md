# A two prime certificate for local positivity of a prime gamma form

Jongmin Choi, Independent Researcher, Seoul, Korea.
ORCID: https://orcid.org/0009-0008-7448-514X

## Result and scope

The manuscript gives the computer-assisted bound
q_B(u) >= (1/20000000000000) ||u||_2^2 for 0 < B <= 3/5,
on the entire real-even minimum compact-support Gamma-form domain.
All norms are ordinary L2. Exactly the prime powers 2 and 3 are active at
B=3/5. Complete Gamma and pole contributions and analytic omitted-mode
bounds are retained. This is not an all-radius result or an RH proof.
No historical novelty, independent human peer review, or proof-assistant
verification is claimed. AI assistance is disclosed in the manuscript.

## Files

- two_prime_certificate.pdf: readable manuscript.
- two_prime_certificate.tex and audit_status.tex: editable sources.
- build.sh: PDF compilation only; never runs a numerical producer.
- evidence/verify_three_fifths.py: unchanged frozen interval producer.
- evidence/three_fifths_certificate.json: complete successful saved witness.
- evidence/check_saved_intervals.py: portable independent saved-data check.
- evidence/INDEPENDENT_SAVED_INTERVAL_AUDIT.json: successful portable check output.
- evidence/PORTABILITY.md: precise scope of the portable adaptation.
- SHA256SUMS: package file hashes.

## Compile the manuscript

A normal TeX Live installation with article, amsmath, amsthm, mathtools,
lmodern, microtype, geometry, booktabs, hyperref and xurl is required.
Run `sh build.sh`. It invokes pdflatex with shell escape disabled. This
command does not evaluate Gamma functions or rerun the certificate.

## Check the saved finite arithmetic without python-flint

On a POSIX Python 3 system, run:

    python3 evidence/check_saved_intervals.py

This uses standard-library rational arithmetic with fixed 512-bit outward
dyadic interval rounding. It checks immutable producer/witness hashes,
1305 interval records, fixed scalar extraction equalities, fresh interval
LDL positivity, and a separate preconditioned Gershgorin gap. It writes
its report to evidence/INDEPENDENT_SAVED_INTERVAL_AUDIT.json; elapsed time
changes on rerun, so the report hash will then change. Keep the original
report if exact byte preservation matters. The check does not import or
execute the producer and needs no python-flint. Resource limits are
60 CPU seconds and 512 MiB address space.

The finite check is conditional on the saved F and C enclosing the exact
matrices derived in the paper. It does not independently verify special-
function enclosures, the source-to-formula correspondence, or domain proofs.

## Optional independent reproduction of the producer

The producer requires python-flint exactly 0.9.0, asserts enabled, and fixes
256-bit precision, M=16, N=8192, J=24. It contains an explicit execution
guard. Read its source and command-line interface before choosing to run
it in your own controlled environment. No build or saved-data checking
command in this package runs it automatically. Its original preparatory
header is retained to preserve the frozen source hash; the saved output
records the subsequent successful run.

## Public scope

Only manuscript and mathematical evidence are included. Internal runtime
receipts, conversation identifiers, approval records, private filesystem
paths, private review notes, and internal usage ledgers are excluded.
The project root is https://github.com/serabing-hash/theta-weighted-certificate .
This root link is not a promise that this package already occupies a specific
repository path, and no DOI has been assigned by this package.
