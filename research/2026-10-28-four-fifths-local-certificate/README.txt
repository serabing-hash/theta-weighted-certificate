A TWO TERM TAIL CERTIFICATE FOR LOCAL PRIME GAMMA POSITIVITY
Consolidated revision v1.1 -- 28 October 2026
Jongmin Choi, Independent Researcher, Seoul, Korea
24ping@naver.com | ORCID 0009-0008-7448-514X

SCOPE
For the ordinary unweighted L2 norm and the entire real-even minimum local
Gamma form domain defined in the manuscript:
  q_B(u) >= 10^-20 ||u||_2^2,  0 < B <= 3/4;
  q_B(u) >= 10^-22 ||u||_2^2,  0 < B <= 4/5.
The smaller-radius bound remains stronger. Both endpoints retain complete
Gamma, full pole and active prime powers 2,3,4; n >= 5 vanish by support.
This is not positivity at all radii, a theta-weighted spectral gap, or RH.
The old frozen v1.0 packet has NOT been altered. This is a consolidated revision,
not a claim of a second historically novel paper or a radius record.

FILES
prime_gamma_local_certificate.pdf / .tex : complete manuscript and TeX source
audit_status.tex, new_certificate_status.tex : included verification details
build.sh : manuscript-only build; no numerical producer calls
repro_075/ : unchanged tested portable replay/data from the 3/4 certificate
repro_080/ : separately tested exact replay and freshly generated 4/5 data
evidence/ : all three original numerical producers, byte-identical
REVIEW_KO.txt : Korean scope/review summary
LICENSE : CC BY-NC 4.0
SHA256SUMS.txt : public file hash manifest

REPLAY EACH ENDPOINT SEPARATELY
Python 3.11+, standard library only. Do not use -O.
  cd repro_075
  python -I -B verify_exact.py --data-dir data --output my_replay.json
  cd ../repro_080
  python -I -B verify_exact.py --data-dir data --output my_replay.json
Each entrypoint was actually executed successfully in its own clean staging
copy. Each binds its own input hashes. Neither replay loads the other dataset.

The 3/4 replay reconstructs the two-term replacement, LDL residual and exact
triangular inverse, and gives a full gap approximately 1.10142502550e-20.
Its original diagnostic records failure of the OLD coarse-tail sufficient
matrix. Its valid containing arrays were reused; that old failure is not hidden.

The 4/5 replay reconstructs A, complete C0 and M=Btrial+54Theta+G, uses an
independently checked inverse residual, then a lower Schur comparison and LDL
residual. It obtains approximately 1.44598358916e-22, smaller than the original
interval producer's approximately 1.45317810846e-22. The theorem uses the clean
rational 1e-22. Exact rational strings, not printed decimals, are proof inputs.
All matrix dimensions, interval grids and source parameters are fixed.

SOURCE GENERATION AND TRUST BOUNDARY
Original numerical sources require python-flint 0.9.0. Their historical headers
and guards are retained for provenance. Their controlled operational supervisors,
approval identifiers and receipts are NOT public mathematical inputs and are
excluded. Invoking those preserved files directly in this layout is not claimed
to reproduce their guarded launch. Use the tested portable replays for checking
saved finite certificates. Source producer regenerations are a separate activity.

The new 4/5 producer recomputed all source matrices at the actual new radius;
no old-radius numerical matrices were imported. The exact displacement identity
uses the actual first row for EVERY required index, not only the 32 low entries;
diagonals are computed separately. No infinite bounded rank-two commutator or
controlled performance comparison is claimed.

The replays independently check finite algebra, inverse/LDL residuals and norm
conversion. The analytic source correspondence and initial transcendental ball
enclosures remain premises; they are explained in the manuscript and preserved
sources. This does not constitute independent human peer review, a proof-assistant
formalization, or independent regeneration of all special-function inputs.

DOCUMENT BUILD
With ordinary TeX Live and the packages listed in the source, run sh build.sh.
This compiles only the manuscript. No numerical gate is executed by the build.

RIGHTS
Copyright (c) 2026 Jongmin Choi. Original manuscript, code and data are licensed
under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC4.0).
See LICENSE. Third-party software is not bundled and retains its own licenses.
No historical priority is claimed. Zhu's preprint claim at radius .8/both parities
is acknowledged but not used as a proved input or independently reproduced here.
Project: https://github.com/serabing-hash/theta-weighted-certificate
This identifies the project, not an asserted upload or DOI for this revision.
