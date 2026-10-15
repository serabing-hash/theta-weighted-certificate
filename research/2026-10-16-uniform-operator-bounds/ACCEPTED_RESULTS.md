# Uniform source-tail extension: accepted analytical results

Research completed 2026-10-15 UTC. Publication collection dated 2026-10-16. This is a curated mathematical ledger incorporating the completed analytical review and controlling corrections. It is not a transcript. No source moments, all-low16 matrix entries, eigenvalues, or Schur sign were numerically evaluated.

## 1. Scope and source

Fix B=3/4 and H=L²_even((-B,B);C), with the inner product conjugate-linear in its first argument. Let e_m(x)=sqrt((2m+1)/(2B))P_m(x/B), L=span(e_0,e_2,...,e_30), X=H⊖L, and T_M be the orthogonal projection onto even Legendre degrees greater than the even cutoff M≥30.

Put W_B(x)=−(1/2)log(1−x²/B²), c(x)=cosh(x/2),

k(s)=exp(−s/2)/(1−exp(−2s))−1/(2s), k(0)=1/4,
K_kh(x)=integral_{−B}^B k(|x−y|)h(y)dy,
S_nh(x)=1_Ω(x−log n)h(x−log n)+1_Ω(x+log n)h(x+log n),
c_2=log2/sqrt2, c_3=log3/sqrt3, c_4=log2/2.

The displayed source is

Z h=W_Bh−K_kh+2c<c,h>−sum_{n=2,3,4} c_n S_nh,
Yh=Π_X Zh,
Fh=W_Bh−sum_n c_n S_nh.

The natural source domain is D_W={h in H: W_Bh in L²}. All conclusions about this displayed formula hold without claiming that its identification with an original weighted operator has been independently established. That source binding remains an explicit inherited premise for the original-operator application.

## 2. Uniformity on all low16 inputs

Y:L→H is bounded and ||T_M Y||_{L→H}→0 as M→∞ through even cutoffs. This follows by applying Cauchy–Schwarz to the sixteen basis images and then Parseval to each image. It also holds on any other fixed finite-dimensional subspace of D_W.

Define the exact Hermitian tail Gram matrix

G_M[i,j]=<F e_{2i},F e_{2j}>−sum_{m even,0≤m≤M} conjugate(<e_m,F e_{2i}>)<e_m,F e_{2j}>.

Then G_M[i,j]=<T_MF e_{2i},T_MF e_{2j}> and ||T_MF||²=lambda_max(G_M). The formula includes total cross integrals, all branch overlaps and the full prefix including degrees 0,...,30. A safe alternative to the entire Gram matrix is the root-sum-square of sixteen certified basis-tail bounds.

For the previously certified k96 surrogate, every input of degree≤30 gives an even polynomial output of degree≤126. Thus, at M=128,

||T_128Y|| ≤ sqrt(lambda_max(G_128)) + ε,
ε=(3/2)E_k+(9/2)t_h.

E_k and t_h are the complete kernel and pole remainder bounds from the fixed-source certificate. The actual kernel and pole have not been annihilated; their remainder is paid exactly once. No new numerical value of this all-low16 operator norm has been evaluated.

In nonorthonormal coordinates with physical norm matrix N, use G_M≤γ²N, not G_M≤γ²I. The earlier h_A result supplies one quadratic-form value and cannot bound lambda_max(G_M).

An independently verified coarse bound for the logarithmic part alone is ||T_M W_B||_{L→H}≤sqrt(496)/(M−29). It does not include the shift tails.

There cannot be a uniform full-source O(M^(−s)) estimate on the L or H² unit ball for any s>1: such tail decay would make sum_m m(m+1)|<e_m,Ye_0>|² finite by dyadic summation, hence Ye_0∈H¹_loc. But Ye_0 has an isolated nonzero truncated-shift jump at x=B−log2. This contradicts local H¹ continuity. This argument gives no certified finite-cutoff lower constant. The sharper proposed two-sided M^(−1/2) rate is not part of the adopted theorem.

## 3. Infinite-dimensional input classes

For every fixed M, T_M Y is unbounded in the unrestricted L² input norm. Indeed Z=W_B+R_src with R_src bounded, while P_MW_B is bounded finite-rank, so T_MY is unbounded multiplication plus a bounded perturbation.

The logarithmic graph norm makes Y bounded, but its unit ball does not have uniform L² tails. Endpoint concentration gives graph-normalized g_n with ||T_MYg_n||→1 for every fixed M.

For every fixed s>0, Y:H^s_even(Ω)→L² is compact. Choose 0<σ<min(s,1/2), use compact H^s→L^{2/(1−2σ)}, W_B in L^{1/σ}, and Hölder. Hence ||T_MY||_{H^s→L²}→0. This is qualitative and fixed-B; it does not identify H^s with the original minimum Gamma domain.

## 4. Quantitative H² theorem

For even h in H²(Ω), set p_0=1, p_1=(x²−B²)/(2B²), α=h(B), β=Bh'(B), g=h−αp_0−βp_1. Then g∈H²_0(Ω), its zero extension is H², and

||g''||²=||h''||²−2|β|²/B³≤||h''||².

Let Λ_M=(M+2)(M+3), τ_j(M)=||T_MFp_j||, κ_j=sup_{0≤s≤2B}|k^(j)(s)| for j=1,2, and

C_F=B²[1/sqrt6+2+1/sqrt2+1/(2e)+6 sum_n c_n],
C_K=B²[1/24+4κ_1+2Bκ_2],
t_M=(B/2)^(M+2)/(M+2)! / [1−(B/2)²/((M+3)(M+4))].

Then

||T_MYh|| ≤ |α|τ_0(M)+|β|τ_1(M)
  +[C_F||g''||+C_K||h||]/Λ_M
  +2 sqrt(B+sinh B) sqrt(2B) t_M ||h||.

The proof uses L_Bu=−((B²−x²)u')', the exact identity
L_B(W_Bg)=−g−2xg'+2xW_Bg'−(B²−x²)W_Bg'',
and vanishing Green boundary terms. It does not assume W_Bg is in ordinary H², which is false in general. The exact regular kernel has the distributional cusp term (K_kh)''=−h/24+integral k''(|x−y|)h(y)dy. The complete kernel and pole are each included once.

The profiles satisfy
τ_0²=2B G_00,
τ_1²=(2B/9)[G_00+G_11/5−2 Re(G_01)/sqrt5].

These are analytical expressions, not newly interval-evaluated constants. Only the clamped/regular contribution has the stated Λ_M^-1 estimate; the full source includes endpoint-profile tails.

## 5. Response operator and all-coefficient certificate

Assume on X: a>0; A0=aI+2vv†; P=Bplus≥0; B*=P+A0; and H_X is the self-adjoint operator of the closed form A0+C_g, with H_X≥βI for some β>0. Keep the original high-domain comparison separate. Write R=H_X^-1 and K=B*^-1.

If C_g≥cI as forms and 0<c≤a, then

0≤M_resp=KPK+KA0RA0K≤ρI, ρ=1/(a+c).

Proof: R≤(A0+cI)^-1, so Δ=A0−A0RA0≥ac/(a+c)I=:dI. Thus M_resp≤K−dK²≤ρI by scalar spectral calculus for B*≥aI. No noncommuting factors are reordered. R≤ρI alone is insufficient for this sharp conclusion. The actual structural constants satisfy c_L≤a, conditional on the inherited source/high realization.

Let E:C^16→L be the orthonormal injection, U=P^(1/2)KYE, F0=A0KYE. For any complex-linear trial J:C^16→D(H_X), put Ξ=F0−H_XJ. Then

C_16=U†U+F0†RF0
≤U†U+F0†J+J†F0−J†H_XJ+ρ_R Ξ†Ξ,

where ρ_R≥||R||. The residual coefficient controls R, while a head-tail source split uses a separately justified ρ_resp≥||M_resp||. A trial only in the form domain is insufficient for this L² residual identity.

The accompanying response theorem supplies rigorous operator-norm error inflation for source head/tail, full-pole filter tails, H_XJ errors and finite interval enclosures. An entry-radius matrix r yields the Loewner enclosure ±diag(sum_j r_ij). Every isotropic eI budget transforms to eN in nonorthonormal physical coordinates. Matrix-valued or endpoint-adapted budgets can be recommended for sharpness; their necessity has not been proved.

## 6. Next finite condition and remaining original-operator obligations

The remaining finite target is one simultaneous Hermitian inequality

Q_lower−ε_out I−C_upper≥λI

on all low coefficients (or the congruent physical-metric version). It is not enough to check sixteen scalar signs. No such matrix sign has been evaluated in this work. J=0 remains admissible; whether a particular frozen J=0 certificate fails requires its own same-source numerical/error linkage.

Under the actual mixed identity, original minimum high-domain admissibility/comparison and shell transfer, a successful full matrix certificate would yield the corresponding all-central-functions result for the fixed supported sector. Uniform source tails alone do not establish it.

The original weighted realization, map h↦h/κ, correct form topology, genuine core/closure or support-exhaustion argument, and the separate global criterion remain unproved here. Increasing B changes the arithmetic shifts and approximation ranges. No original whole-line operator positivity or RH conclusion follows.
