# 동일 버퍼에 결합된 전체 R의 포함 증명

이 문서는 새 실제 수치 결과를 주장하지 않는다. `whole_r.py`의 전 구간 알고리즘과 `center_replay.py`의 독립 중심 재생이 어떤 포함 관계를 검사하는지 명시한다. 현재 실행 증거는 합성 입력에 관한 것이며, 실제 중심 jet 스트림은 생성하지 않았다. 원본의 해석적 source·Gamma·coercivity 전제는 그대로 조건부이다.

## 1. 하나의 좌표와 중심 모델

각 native cell과 모든 물리 정점은 같은 `t∈[-1,1]`을 사용한다. 물리 좌표는 `X=left+L(y_mid+h t)+shift`, `z=X/(3/4)=offset+slope t`이다. `source_context`, component, cell, normalized cell, 고정 geometry, 전체 양방향 Gamma, 모든 prime edge, 저장된 c0, native row SHA와 legacy field SHA가 한 source binding에 들어간다. 실제 reader는 이 binding을 원본 행 및 보호 manifest의 전체 파일 hash와 대조한다.

생성기는 유한 Legendre prefix를 monomial로 전개해 차수 d=16의 Taylor 계수를 만든다. 독립 재생은 monomial 전개를 쓰지 않고 `D_k P_n=P_n^(k)/k!`의 recurrence

`D_k P_(n+1) = (2n+1)/(n+1) [q D_k P_n + D_(k-1) P_n] - n/(n+1) D_k P_(n-1)`

를 사용한다. `D_-1=0`, `P_0=1`, `P_1=z`이며, 물리 계수를 곱하기 전에 각 Legendre derivative를 계산한다. 실제 입력에서는 두 방식 모두 새 중심 source 평가이므로 현재 gate가 계산 전에 거부한다.

`δ=rad(offset)+mag(slope)`, `k=d+1`일 때 유한 prefix의 uniform remainder는

`ρ_F = δ^k/k! · Σ_m mag(C_m) (m+k)!/[2^k k!(m-k)!]`, 단 `m≥k`

로 상계한다. 전체 실수 domain `[-1,1]`을 먼저 확인한다. Jacobi derivative 공식과 최대값 부등식을 반복 적용한 결과다. [NIST DLMF 18.9.15](https://dlmf.nist.gov/18.9.E15), [18.14.1](https://dlmf.nist.gov/18.14.E1). 낮은 함수 16개도 각각 전체 차수 0,2,…,30과 물리 정규화를 사용하며, d보다 높은 항은 같은 remainder에 지급한다.

240 decimal places의 저장은 정수 floor/ceiling으로 바깥쪽 반올림한다. 거대한 rational을 문자열로 먼저 변환하거나 Python의 정수 변환 제한을 높이지 않는다. 독립 재생에서 모든 저장 coefficient box가 재생 coefficient box를 포함하고 저장 remainder가 위 bound 이상인지 확인한다.

## 2. 오차를 잃지 않는 공통 polynomial

`TJet`은 `P(t)+e(t)`를 뜻하며, P의 계수는 singleton rational이고 `|e(t)|≤Σ_tag ρ_tag`이다. 원본 coefficient box의 반폭 합은 `coefficient_and_rounding`으로 지급한다. 따라서 geometry와 물리 계수의 불확실성도 이 항에 포함된다. 별도 `geometry_parameter`는 적분 Jacobian L의 불확실성이다. 항의 이름 때문에 affine geometry 오차가 사라지는 것은 아니다.

곱셈에서 d까지의 정확한 convolution을 보존하고, d 초과 계수의 절댓값 합, `ρ_P mag(Q)`, `ρ_Q mag(P)`, `ρ_Pρ_Q`를 모두 지급한다. chi에 속한 오차와 다른 오차의 혼합항도 chi tag로 유지한다. 어떤 Gamma box도 고정 coefficient로 취급하지 않는다. Gamma는 box midpoint와 전 구간 varying remainder로 들어가므로 홀수항 소거로 Gamma 변동을 줄일 수 없다.

적분은 P의 홀수 coefficient만 정확히 0으로 소거하고, 짝수 k는 `1/(k+1)`을 곱한다. 모든 varying remainder는 남긴다. normalized 폭과 물리 L을 한 번씩 곱하며 L 반폭과 remainder의 혼합항도 지급한다.

## 3. 동일 M에서 g−Mc0와 response

모든 정점에서 `M_vv=a+kappa+omega(Gamma_plus+Gamma_minus)`, off-diagonal은 원본 graph의 `-c2,-c3,-c4`이다. 전체 seven/path/pair edge를 같은 M 버퍼로 만든다. `g=a Fhat−E alpha`, `r=g−M c0` 또한 같은 Fhat/E/M/c0에서 계산한다.

원본의 조건부 `M≽aI`, `a_lo>0` 전제 아래 실제 해 `c=M^(-1)g`에 대해

`|c_v−c0_v| ≤ ||c−c0||_2 ≤ ||r||_2/a_lo ≤ Σ_v [mag(P_rv)+ρ_rv]/a_lo`.

중심 residual polynomial의 범위와 coefficient, Taylor, 전체 Gamma, parameter, convolution 및 혼합 오차를 모두 오른쪽에 지급한다. 실제 Gamma는 다시 평가하지 않는다. 합성 fixture에서는 diagonal dominance를 직접 검사한다. 실제 입력의 전제 hash는 저장된 feasibility packet과 결합되지만, hash 자체가 coercivity의 새 증명이 되는 것은 아니다. 해당 해석적 정당화는 보존된 `INVERSE_GAIN_MAIN_PROOF.md` 식 (11) 및 그 source 전제에 의존한다.

## 4. 전체 chi/Ag와 전체 R

첫 pass는 모든 4,416 cell의 `chi_j=∫E_j^T M Fhat`와 `Ag=∫Fhat^T M Fhat`를 누적하고, 세 component의 양 끝 strip에 대한 전체 cached endpoint bound를 더한다. endpoint norm trace와 complete Gamma log integral도 원본 packet에 대조한다. chi에는 자신의 모든 Taylor/Gamma/geometry/coefficient/product 오차와 endpoint 오차가 남는다.

두 번째 pass는 이 새 전체 chi만 사용하여 같은 cell에서

`weighted = ∫ c(t)^T [Σ_j E_j(t) chi_j] dt`

를 직접 포함한다. 새 chi의 모든 오차와 response 및 E의 혼합항을 지급한다. beta_j도 함께 누적한다. 두 pass의 canonical row/source stream SHA가 일치해야 하며, 첫 pass에서 재생 검증한 중심 모델을 두 번째 pass에서 다시 source 평가하지 않는다. Header SHA도 두 pass 사이에 고정되어야 한다.

response endpoint는 `||c||≤G0/a_lo`와 `||E_j||≤E0_j`에 의해 `2 epsilon G0/a_lo · Σ_j E0_j mag(chi_j)`로 지급하며, 이때도 새 전체 chi를 사용한다. pole은 전 구간 scalar로만 `R=weighted−2 sigma ell`, `H=Ag+2 ell²`에 각각 한 번 들어간다. sigma·ell의 linear와 mixed uncertainty는 모두 `whole_pole_cross`에 지급한다.

`R=center_new±rho_new`. 새 실제 중심값을 계산하지 않았으므로 center_new와 rho_new는 현재 미평가이다. 저장된 이전 중심 m_old와의 이동은 `drift=|center_new−m_old|`이며, 이전 중심을 기준으로 한 포함 반경은 `drift+rho_new`이다. drift를 rho_new에도 다시 더하지 않는다.

## 5. 전체 예산 및 판정

14개 필수 ledger 항 중 audit 항인 `midpoint_drift`를 제외한 13개 지급액의 합은 정확히 R의 certified radius와 같아야 한다. 각 chi-derived remainder는 `global_chi_all_errors`에 포함된다. 이 분류는 물리 원인의 유일한 분해가 아니라, 모든 혼합항이 지급되었음을 검산하기 위한 분류다. 원시 tag ledger도 보존한다. chi를 통해 들어온 endpoint/product 오차는 global chi 항에서 지급되므로 별도 항이 0일 수 있다.

부분 bound를 전체 R로 제출, 필수 항 누락, 항별 과소 지급, stale chi, source stream 변경, 실제 source를 현재 stage에서 재생하려는 경우를 모두 거부한다. 제출된 radius 필드도 재생 radius 이상이어야 하고, 제출된 중심은 재생 중심과 같으며, 13개 제출 지급액 합은 제출 radius와 같아야 한다. 제출 interval은 그 중심±radius 전체를 포함해야 한다. 기존 response-only Fhat carry `1.25231e−26`은 전체 R 반경이 아니다. 기존 response 오차를 전부 제거해도 저장된 다른 반경 합은 이전 중심의 약 395.149배이다. 이번 실제 전체 error 상한은 `SAVED_ANALYSIS.json`에 0 대신 미평가 null로 기록한다. 이 포함 정리는 개선된 반경이나 실제 부호 분리를 보장하지 않는다.
