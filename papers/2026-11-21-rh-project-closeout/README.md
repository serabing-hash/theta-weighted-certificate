# Fixed-Support Bounds for a Centered Gamma–Prime Form
Final research report, 21 November 2026. Jongmin Choi · Independent Researcher, Seoul, Korea · [ORCID 0009-0008-7448-514X](https://orcid.org/0009-0008-7448-514X).

[Paper (PDF)](rh_project_closeout.pdf) · [LaTeX source](rh_project_closeout.tex) · [SHA-256 manifest](MANIFEST.sha256)

**RH_PROOF=NOT-OBTAINED.** This is a selected closeout record, not a proof, disproof, peer-reviewed result, or complete archive. The global theta-form bound \(1/2\) was not obtained.

## 한국어 요약
- \(B=1\): 12차 및 20차 Legendre 시험공간에서 각각 \(10^{-11}\), \(10^{-18}\)의 양의 하계를 인증했습니다. 별도 실행에서 **같은 구현**으로 결과 JSON 두 개가 바이트 단위로 일치했습니다. 20차의 양의 증인은 12차 하계를 전체 공간으로 확대할 수 없음을 보여 줍니다.
- \(B=1\)의 적응형 22차 공간에 직교하는 전체 보공간 하계는 \(1/5\)입니다. 남은 22×22 Schur 행렬의 부호는 미확정입니다. 이 적응형 공간과 앞의 유한 시험공간은 다릅니다.
- \(B=2\) 미평활 원형식: 특정 두 열과 선택한 무한차원 보공간의 합에서 양성을 보였습니다. 다른 74,998개 저차 방향 및 교차항은 미확정입니다. 저장된 구간 계산을 확인했으며 이번 정리에서 재실행하지 않았습니다.

## Reproduction and verification boundaries

Use the package as the current directory. Keep assertions enabled. Do not use Python -O or set PYTHONOPTIMIZE. An archive hash checks bytes, not mathematics. None of the scientific commands below was executed during closeout.

    sha256sum -c MANIFEST.sha256

**B=1.** The Python 3 standard library reproducer computes the two finite certificates from the included sources. It does not need a zeta zero table or any external input file. The reference files are not overwritten by these commands.

    mkdir -p replay
    python3 r1/certify12_frozen.py --bits 320 --order 256 --out replay/certificate12.json
    python3 r1/certify.py --dimension 20 --bits 400 --order 300 --out replay/certificate20.json
    cmp r1/certificate.json replay/certificate12.json
    cmp r1/certificate20.json replay/certificate20.json

The archived independent invocation used the same code, not a second arithmetic implementation. The JSON contains the witness and pivots, not the full integer comparison matrix. The 20-dimensional code retains a stale comment mentioning the 12-dimensional floor; the actual selected floor is the value recorded in the JSON and used in the test.

**B=2.** The frozen Linux reproducer uses Python 3, SymPy, libmpfi.so.0 and libmpfr.so.6 with matching architecture and ABI. A hermetic environment is not supplied. It needs no external input file or network at run time. The stored Python output is preserved verbatim; compare the enclosing numerical results and bounds, not timing or text formatting across environments.

    python3 b2/pilot.py 6
    python3 b2/pilot.py 9
    python3 b2/bare_weighted.py

The eps6.log and eps9.log files show smoothed controls and the bare two-column head; the two smoothed runs use different complements. The bare_weighted.log includes the default exponent-6 prelude because bare_weighted.py imports pilot, then gives the separate unsmoothed calculation for \(n=150000\). The bare result is not inferred from the positive mass correction in the smoothed controls. Output is numerical; the mathematical identities, domain, and certified scope are described in the paper. This bounded calculation does not construct the entire low matrix.

The distribution excludes historical bulk archives, private working notes and links, incomplete jobs, and results lacking selected replay material. No historical release is replaced. License: [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) for original author-owned contributions, consistent with the parent repository; third-party tools retain their own licenses.
