# A finite-rank Schur correction from a weighted prime defect

Jongmin Choi, Independent Researcher, Seoul, Korea.
ORCID: https://orcid.org/0009-0008-7448-514X
Analytic research note v0.1, 28 October 2026.

## Proven scope

At B=3/4, the actual prime 2, 3, 4 operator has an explicitly weighted
positive defect E=R I-P with R<27/20 and E>=I/54. A localized observation
is replaced by a finite cosine feature with its entire omitted feature
tail paid for in the same energy norm. The high-block comparison then
subtracts (8/25) zeta zeta* from any valid full diagonal-inverse coupling
majorant. The feature and zeta have explicit finite formulas.

The manuscript derives the Gamma decomposition and scalar high floor
needed for this application. It does not discard the full baseline
coupling tail. Different uses of the same defect are alternatives, not
independent resources that may be added.

## Not established

No certified nonvanishing or quantitative size of the selected finite
vector zeta is reported. A separate fixed-parameter implementation
(B=3/4, M=32, N=16384, J=32, 256 bits) failed its LDL positivity gate.
Its source SHA256 was
8348b5cbb0f88d5c9f34f3553ef4730c625faa7d8ff5f9d36d6db3ad31298acb.
That run produced no successful local-positivity certificate. Its failure
does not exhibit a negative direction of the original form or a RH
counterexample. The qualitative outcome is recorded for transparency;
the failed_fixed_candidate subfolder provides the exact source and a
path-redacted error record, separately from the analytic proof. The
scalar checks do not reproduce or certify that run. This note supplies no new positivity certificate at
B=3/4, no all-radius positivity theorem, and no proof of RH. Historical
novelty, independent human review and formal proof verification are not
claimed. AI assistance is disclosed in the manuscript.

## Reproduction

- Run `sh build.sh` with an ordinary LaTeX installation to build the PDF.
- Run `python3 check_constants.py` to reproduce constants_check.json.
  This uses only standard-library exact rational arithmetic, not source
  function evaluation or a matrix computation. Its PASS is not an
  analytic proof certificate.
- Verify SHA256SUMS to check the packaged files.

Neither command runs the separate failed numerical producer.
See failed_fixed_candidate/README.md for its exact scope and manual
reproduction requirements. Its original preparatory header is retained
for source-hash fidelity and is superseded by FAILURE_STATUS.json.
Private operational notes, identifiers and runtime receipts are excluded.
The package has no DOI and does not assert a particular repository
publication location. Project: https://github.com/serabing-hash/theta-weighted-certificate

## License

Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0),
consistent with the research project. See LICENSE.
