# Uniform source-tail extension: valid theorem and exact scope

Research completed 2026-10-15 UTC. Curated proof text. No new source integration, matrix computation, or numerical positivity certificate was performed.

## 1. Main conclusion

The fixed-input certificate extends analytically to a bounded source operator on the entire sixteen-dimensional low space. Its tails converge uniformly on that space's physical L² unit ball. The numerical constant certified for the particular vector h_A does not become an operator-norm constant by linearity or finite dimensionality.

A uniform source-tail certificate can be obtained from a finite tail Gram matrix, or more conservatively from sixteen basis-tail bounds. This is still distinct from certifying the complete low Schur form and its positive gap. The latter, together with the established high-domain comparison, is what would cover every central function in the specified original minimum Gamma domain.

An unrestricted L²-to-L² source operator does not exist: the logarithmic multiplier is unbounded and is not cancelled by the other bounded terms. In fact each finite-cutoff source-tail map is unbounded in the L² input norm. Its graph norm makes the map bounded but does not make the tails converge uniformly. Stronger spatial regularity, or a weaker output norm, can give valid uniform convergence.

None of these conclusions establishes global positivity of the original operator ℒ or an RH conclusion.

## 2. Fixed definitions

Let B=3/4, Ω=(−B,B), H=L²_even(Ω;ℂ), with conjugate-linear first inner product. Set

- e_m(x)=sqrt((2m+1)/(2B)) P_m(x/B)
- L=span{e_0,e_2,…,e_30}
- Π_X=I−Π_L
- P_M=Σ_{0≤m≤M, m even} e_m〈e_m,·〉 and T_M=I−P_M, for even M≥30
- W_B(x)=−(1/2)log(1−x²/B²)
- c(x)=cosh(x/2), m(h)=〈c,h〉
- S_n h(x)=1_Ω(x−log n)h(x−log n)+1_Ω(x+log n)h(x+log n)
- c_2=log2/sqrt2, c_3=log3/sqrt3, c_4=log2/2
- k(s)=exp(−s/2)/(1−exp(−2s))−1/(2s), extended continuously by k(0)=1/4
- K_kh(x)=∫_Ω k(|x−y|)h(y)dy.

The explicit source and its log/translation part are

Z h=W_Bh−K_kh+2c〈c,h〉−Σ_{n=2,3,4}c_nS_nh,
Y h=Π_X Z h,
F h=W_Bh−Σ_{n=2,3,4}c_nS_nh.

The natural multiplication domain is D_W={h∈H: W_Bh∈L²}. In particular L⊂D_W. Since T_MΠ_X=T_M, the low projection does not alter the tail.

The identification of this explicit formula with a source of the larger original operator remains the source-binding assumption specified in the fixed certificate. The present theorem is unconditional for the displayed explicit source; its use for that original source inherits the identification.

Write Z=W_B+R. The remainder R is bounded on H. For example,

||R|| ≤ C_R := 2B sup_{0≤s≤2B}|k(s)| + 2||c||² + 2Σ_n c_n.

Indeed each truncated translation is an L² contraction, ||S_n||≤2, the kernel norm is at most 2B sup|k|, and the rank-one term has norm 2||c||². No sharp estimate is needed for these statements.

## 3. Uniform low16 theorem and finite certificate

### Theorem 1

For every even M≥30, Y|_L:L→H is a bounded operator and

lim_{M→∞, M even} ||T_M Y||_{L→L²}=0.

For M=128, define ε=(3/2)E_k+(9/2)t_h, using exactly the complete rational kernel and cosh remainder bounds from the fixed certificate. Then, for every complex h∈L,

||T_128 Yh|| ≤ ||T_128 Fh||+ε||h||.

The older e_op≥ε may be retained conservatively instead, provided its stated assumptions are kept separate.

### Proof

The images Y e_{2j}, 0≤j≤15, are all in H. For h=Σ_j a_j e_{2j}, Cauchy–Schwarz gives

||T_M Yh|| ≤ (Σ_j ||T_M Y e_{2j}||²)^(1/2) ||h||.

Every summand tends to zero by completeness of the Legendre basis. There are only sixteen summands, which proves uniform convergence.

The polynomial surrogate k_96 has even powers through 96 and odd powers through 95. Against an input of degree at most 30 its integral output is an even polynomial of degree at most max(96,95+30+1)=126. Thus T_128 K_{k96}h=0 for every h∈L, not merely for h_A. The complete kernel-error norm bound is (3/2)E_k||h||. The complete rank-one tail bound is (9/2)t_h||h||. Their sum proves the claimed estimate. Only the polynomial surrogate is annihilated; the actual regular kernel and cosh tails remain paid.

### Exact Gram-matrix formulation

Put b_j=e_{2j}, g_j=F b_j, for j=0,…,15. Define the 16×16 Hermitian positive-semidefinite matrix

G_M[i,j]=〈g_i,g_j〉−Σ_{0≤m≤M, m even} overline(〈e_m,g_i〉)〈e_m,g_j〉.

Parseval gives the exact identities

G_M[i,j]=〈T_M g_i,T_M g_j〉,
||T_M Fh||²=a*G_M a,
||T_M F||²_{L→L²}=λ_max(G_M).

Consequently

||T_128 Y||_{L→L²} ≤ sqrt(λ_max(G_128))+ε.

This requires all signed log/translation cross terms and all translation-branch overlaps in the Gram entries. The complete prefix includes the low modes 0,…,30 as well as 32,…,128. The source/basis is real, so G_M is real symmetric; its 136 independent entries still control arbitrary complex coefficient vectors.

One need not evaluate all cross entries if a weaker estimate suffices. Certified basis bounds τ_j≥||T_128 F b_j|| imply

||T_128 Y|| ≤ sqrt(Σ_j τ_j²)+ε.

For example, if each τ_j≤τ, the safe factor is 4τ, rather than τ. Independently bounding the log and translation tail matrices yields the further safe estimate

||T_128 Y|| ≤ sqrt(λ_max(G_W))+sqrt(λ_max(G_S))+ε.

Here G_W and G_S are the respective Gram matrices at cutoff 128. It loses their cancellation but preserves validity.

In a nonorthonormal basis q_r(x)=(1−x²/B²)^r/sqrt(2B), coefficient Euclidean norm is not physical L² norm. Let N[i,j]=〈q_i,q_j〉. The relevant exact operator squared norm is

λ_max(N^(−1/2) G_M N^(−1/2)),

or the generalized eigenvalue bound G_M≤γ²N. A certificate must respect this metric.

All matrix statements here are analytical formulas. No new matrix entries, eigenvalues, or numerical all-low16 bound have been certified in this audit.

### Why one fixed vector is insufficient

The h_A certificate bounds one number a_A*G a_A (with the stated remainder), not λ_max(G). Abstractly, for any unit vector u perpendicular to a_A, adding t uu* with t≥0 leaves that one quadratic form unchanged while making the maximal eigenvalue arbitrarily large. This is an information limitation of the one-vector evidence; it does not claim that the actual source Gram matrix is arbitrary.

## 4. An explicit analytic bound for the logarithmic part

For even m≥2,

(1/2)∫_{−1}^1 W(t)P_m(t)dt = 1/[m(m+1)],
W(t)=−(1/2)log(1−t²).

This follows by integrating the Legendre differential equation against log(1−t) and using parity. Therefore the orthonormal coefficients of W in the probability measure dt/2 are sqrt(2m+1)/[m(m+1)].

For even M≥30 put N=M−30. Truncate W at Legendre degree N. Its product with h∈L has degree at most M and is removed exactly by T_M. Moreover

||h||_∞ ≤ sqrt(496/(2B))||h||,

because |P_m(t)|≤1 and Σ_{j=0}^{15}(4j+1)=496. Hence

||T_M(W_Bh)||
 ≤ sqrt(496) [Σ_{m>N, m even}(2m+1)/(m²(m+1)²)]^(1/2)||h||
 ≤ sqrt(496)/(M−29) ||h||.

For the final inequality, use (2m+1)/(m²(m+1)²)=1/m²−1/(m+1)² and enlarge to all integers m>N. This is a deliberately coarse uniform logarithmic-tail bound, not an estimate for the full source. The truncated translation branches have their own nonzero infinite tails.

## 5. Why unrestricted L² is not a valid extension

### Proposition 2

The map Y:D_W→H has no bounded extension with the L² input norm. For every finite even M, T_M Y is also unbounded in that norm.

### Proof by bounded perturbation

Multiplication by W_B is unbounded on L². Each finite-rank P_M W_B nevertheless has a bounded extension to L² because

〈e_m,W_Bh〉=〈W_B e_m,h〉,

and W_Be_m∈L² for every fixed m. Thus, on D_W,

T_M Yh = W_Bh + (T_M R−P_M W_B)h,

where the parenthesized operator is bounded on L². A bounded perturbation cannot turn this unbounded multiplication operator into a bounded one.

### Concrete concentration sequence

Let E_n={x∈Ω:n≤W_B(x)<n+1} and h_n=1_{E_n}/sqrt(|E_n|). These are even, belong to D_W, and have L² norm one. Also

n≤||W_Bh_n||≤n+1,
|E_n|=2B[sqrt(1−e^(−2(n+1)))−sqrt(1−e^(−2n))]=O(e^(−2n)).

For any fixed M, the finite Legendre coefficients of W_Bh_n are O((n+1)sqrt(|E_n|)); consequently ||P_M W_Bh_n||→0. It follows that

||T_M Yh_n||≥n−o(1)−C_R→∞.

The source is not even defined in L² for every L² input. For example, an even function behaving near an endpoint as

h(x)=1/[sqrt(δ) log(1/δ)], δ=B−|x|,

with a sufficiently small endpoint support, belongs to L², whereas W_Bh does not.

These are counterexamples to the unrestricted L² source extension, not counterexamples to positivity of the original operator or to the valid low16 theorem.

## 6. Norms that do and do not give uniform tails

### Exact compactness criterion

Let E be a normed input space and suppose Y:E→H is bounded. Then

||T_M Y||_{E→H}→0 if and only if Y:E→H is compact.

If the tails converge in norm, P_MY are finite-rank approximants to Y. Conversely, T_M→0 strongly with ||T_M||≤1, hence uniformly on the relatively compact image of the input unit ball. This separates pointwise Parseval convergence from uniform operator-norm convergence.

### Physical L² norm on a fixed finite-dimensional input space

Yes: the low16 theorem is an immediate instance. More generally, every fixed finite-dimensional subspace contained in D_W has uniform tails. It need not have the same numerical constant or the same polynomial-annihilation cutoff.

### Graph norm of the logarithmic multiplier

Define ||h||_D=(||h||²+||W_Bh||²)^(1/2). Then

||Yh||≤sqrt(1+C_R²)||h||_D.

But this boundedness does not imply uniform L² tails. Normalize the concentration sequence above by g_n=h_n/||h_n||_D. For each fixed M,

||g_n||_D=1,
||T_M Yg_n||→1.

Indeed the multiplier portion approaches norm one, its finite projection tends to zero, and the bounded remainder is divided by a quantity tending to infinity. In particular ||T_M Y||_{D→L²}≥1 for every fixed M.

The weaker endpoint form norm (||h||²+∫W_B|h|²)^(1/2) does not even make Y bounded into L², as the same sequence shows after normalization by approximately sqrt(n).

### Positive Sobolev regularity in the input

Yes: for every fixed s>0, Y:H^s_even(Ω)→L²_even(Ω) is compact, so

sup_{||h||_{H^s}≤1}||T_M Yh||→0.

To see this, choose 0<σ<min(s,1/2). The one-dimensional compact Sobolev embedding gives H^s(Ω) compactly into L^q(Ω), q=2/(1−2σ)>2. Since the logarithm belongs to L^p for p=1/σ and 1/2=1/p+1/q, multiplication by W_B maps L^q continuously to L². Thus its composition with the compact embedding is compact. The bounded remainder R composed with H^s→L² is compact as well.

For the especially elementary case s=1, bounded H¹ sets are relatively compact in C(Ω̄), while W_B∈L²; uniform convergence of inputs therefore gives L² convergence after multiplication by W_B. Neither argument supplies a sharp numerical cutoff constant without quantitative approximation estimates.

These are compact-interval regularity statements. They do not identify H^s with the original minimum Gamma form domain or prove a uniform H^s estimate for every original-domain vector.

### A weaker output norm

For s>0, define the negative Legendre norm

||f||_{−s}²=Σ_{m≥0, m even}(1+m)^(−2s)|〈e_m,f〉|².

Then the logarithmic graph norm gives an explicit uniform estimate

||T_M Yh||_{−s} ≤ sqrt(1+C_R²)(M+3)^(−s)||h||_D

for even M, since the first retained index is M+2. This is a valid different-norm theorem. It does not replace an L² source-tail estimate in a response argument unless that argument is separately proved continuous in this weaker norm.

## 7. What is needed for all central functions

The actual I/J source is a mixed map whose input is low16. For a central original-domain function g, decompose

g=h+q, h=Π_Lg∈L, q∈V_high,

where V_high is the original minimum high Gamma domain. The source pairing Q(q,h)=〈q,Yh〉 and the high coercive form are already formulated for this decomposition. Thus the relevant extension is uniformity in the sixteen low coefficients, not an unrestricted-L² extension of the source formula.

Under the source identities and high/shell premises stated in I/J, a sufficient remaining certificate is a full Hermitian inequality, with an explicit λ>0, of the form

Q(h)−ε_out||h||²−C(Yh) ≥ λ||h||² for every h∈L,

where C uses the actual filtered source, the full pole, and the constrained inverse. Equivalently one can use the stronger retained comparison prescribed in I/J. The present source-tail theorem supplies only one error-control ingredient for such a certificate.

In particular, the filtered forcing is A_0 B_*^(−1)Y, not Y in general. Source tail control does not authorize replacing it. The exact full-pole filter identity in RESPONSE_CERTIFICATE.md retains this distinction; a source tail bound alone is not a bound for the filtered response.

If the complete low inequality were independently certified, the inherited high/shell transfer would yield the corresponding supported-sector coercive estimate for every admissible central g and the specified shell families. This would be a genuine function-uniform result, but still not global original-operator positivity.

## 8. Why a global support or original-ℒ conclusion needs more

1. The present arithmetic source uses only n=2,3,4 because log n<2B=3/2. On larger supports, additional prime powers contribute. The graph geometry, component decomposition, constants, and source all change.
2. The kernel approximation is certified only on 0≤|x−y|≤3/2, and the pole remainder only for |x|≤3/4. Neither the numerical remainder bounds nor polynomial-output cutoff automatically survive an increasing-support limit.
3. A fixed compact interval plus the stipulated narrow external shells has not been shown here to form a core or dense positivity-testing class for the original weighted form. Approximation in plain L² alone is insufficient for an unbounded-form transfer.
4. I/J explicitly keep the original realization independent: H_original=L²_even(κ C_weight dx), C_weight=2cosh(x/2), the original minimum form/domain, positive smooth κ, form continuity, and ℓ(h/κ)=Q(h) on original tests must be established with the correct norms and domains.
5. To pass from tested functions to all of an original form domain, one needs an actual form-core/closure theorem or another justified approximation argument, together with the required inequalities on that class. No equality of minimum and maximal supported-energy domains follows merely from the source calculation.
6. The separate global criterion connecting the original operator to RH is not proved by source-tail or low-space bounds.

## Appendix A. Focused verification of the H² endpoint-jet lemma and response matrix

All statements below are analytical; no new numerical moments or certificate were evaluated. The accompanying RESPONSE_CERTIFICATE.md supplies the complete metric-aware error contract.

### A1. Endpoint-jet decomposition

The endpoint-jet subtraction is valid for complex even H² functions. It removes the endpoint value and derivative that cause the truncated translations' interior jumps and corners. The weighted Legendre derivative of the logarithmic residual is square integrable. This does not assert that the logarithmic residual belongs to ordinary H².

Set

p(x)=B²−x², L_Bu=−(pu')',
p_0(x)=1,
p_1(x)=(x²−B²)/(2B²),
α=h(B), β=B h'(B),
g=h−αp_0−βp_1.

The H² traces exist. Evenness gives g(±B)=g'(±B)=0, so g∈H²_0(Ω). Its zero extension is in H²(ℝ); each truncated shift S_ng consequently lies in H²(Ω), with

||(S_ng)'||≤2||g'||,
||(S_ng)''||≤2||g''||.

There is a useful exact improvement over a crude trace estimate:

g''=h''−β/B²=h''−(1/(2B))∫_Ωh''.

Thus g'' is the orthogonal complement of the constant part of h'', and

||g''||²=||h''||²−(2/B³)|β|²≤||h''||²,
|β|≤sqrt(B³/2)||h''||.

No extra factor is needed to control the residual second derivative.

For d(x)=B−|x|, integration from the nearer endpoint and Cauchy–Schwarz give

|g'(x)|≤sqrt(d(x))||g''||,
|g(x)|≤d(x)^(3/2)||g''||/sqrt3.

Consequently

||g'||≤B||g''||,
||g||≤B²||g''||/sqrt6.

A valid value-trace estimate, also for complex h, is

|α|≤(2B)^(−1/2)||h||+sqrt(2B/3)||h'||.

For example, derive it from h(B)=(1/(2B))∫h+(1/(2B))∫(x+B)h'(x)dx.

### A2. Explicit logarithmic and shift constants

Since pW_B'=x, direct differentiation on the open interval gives

L_B(W_Bg)=−g−2xg'+2xW_Bg'−pW_Bg''.

Every term is in L². In particular

sup_Ω pW_B=B²/(2e),
∫_Ω d(x)W_B(x)²dx≤B²/8.

For the second estimate, 1−x²/B²≥d/B implies W_B≤(1/2)log(B/d); integration gives 2∫_0^B d[(1/2)log(B/d)]²dd=B²/8.

It follows that

||L_B(W_Bg)||≤C_W||g''||,
C_W=B²[1/sqrt6+2+1/sqrt2+1/(2e)].

Furthermore,

||L_B(S_ng)||≤2B||(S_ng)'||+B²||(S_ng)''||≤6B²||g''||.

Therefore, for the exact signed F=W_B−Σc_nS_n,

||L_B(Fg)||≤C_F||g''||,
C_F=B²[1/sqrt6+2+1/sqrt2+1/(2e)+6Σ_{n=2,3,4}c_n].

These constants are conservative analytical expressions, not newly evaluated interval results.

The endpoint bounds also show W_Bg→0 and (W_Bg)'→0 at both endpoints. Hence the Legendre Green boundary term p[u'e_m−ue_m'] vanishes for u=W_Bg. It vanishes for S_ng as well, since those functions are H² with bounded value and derivative traces and p vanishes at the endpoints. Local integration by parts, followed by endpoint limits, gives

〈e_m,u〉=〈e_m,L_Bu〉/[m(m+1)], m≥1.

Thus for even M≥0 and even u of these types,

||T_Mu||≤||L_Bu||/[(M+2)(M+3)].

The vanishing boundary flux is essential. The bare function W_B has L_BW_B=−1 in the open interval but nonzero endpoint flux, so the same spectral identity cannot be applied to W_B without the residual subtraction.

### A3. The exact regular kernel is H²-smoothing

The right-hand Taylor expansion at zero begins

k(s)=1/4−s/48−s²/32+O(s³),
k'(0+)=−1/48, k''(0+)=−1/16.

The apparent singularity at zero is removable on the half-line; k and its right derivatives extend continuously to [0,2B]. Set

κ_1=sup_{0≤s≤2B}|k'(s)|,
κ_2=sup_{0≤s≤2B}|k''(s)|.

These are finite, computable constants. The even kernel k(|s|) has a first-derivative jump, so its distributional second derivative is

(d²/ds²)k(|s|)=2k'(0+)δ_0+k''(|s|).

Consequently, for every h∈L²(Ω),

(K_kh)'(x)=∫_Ω sign(x−y)k'(|x−y|)h(y)dy,
(K_kh)''(x)=−h(x)/24+∫_Ωk''(|x−y|)h(y)dy.

The last k'' is the ordinary half-line derivative with its continuous endpoint limit. The convolution identities follow in distributions and show K_kh∈H²(Ω), with

||(K_kh)'||≤2Bκ_1||h||,
||(K_kh)''||≤(1/24+2Bκ_2)||h||,
||L_BK_kh||≤C_K||h||,
C_K=B²[4κ_1+1/24+2Bκ_2].

The Green boundary flux vanishes for K_kh, so the same spectral tail bound applies. This proof uses the full exact kernel, not the polynomial surrogate, and creates no fixed nonzero kernel-error floor as M increases.

### A4. A complete quantitative H² tail inequality

For even M≥30 define

τ_j(M)=||T_M Fp_j||, j=0,1,
t_M=(B/2)^(M+2)/(M+2)! · [1−(B/2)²/((M+3)(M+4))]^(−1).

At B=3/4 the denominator is positive. The cosh Taylor polynomial through degree M is killed by T_M, and its complete remainder gives

||T_M cosh(x/2)||≤sqrt(2B)t_M.

Since ||c||²=B+sinh B, the complete pole, included exactly once, therefore obeys

||T_M[2c〈c,h〉]||≤2 sqrt(B+sinh B) sqrt(2B)t_M||h||.

Combining A1–A3 gives, for every complex even h∈H²(Ω),

||T_M Yh||
≤ |α|τ_0(M)+|β|τ_1(M)
  +[C_F||g''||+C_K||h||]/[(M+2)(M+3)]
  +2 sqrt(B+sinh B) sqrt(2B)t_M||h||.

This version keeps the entire kernel on h and the entire pole on h, so neither is split across the two endpoint profiles or paid twice. Only F is split into endpoint jets and the clamped residual.

With ||h||_{H²}²=||h||²+||h'||²+||h''||², a direct uniform consequence is

||T_M Y||_{H²_even→L²}
≤ sqrt[1/(2B)+2B/3] τ_0(M)
  +sqrt(B³/2)τ_1(M)
  +(C_F+C_K)/[(M+2)(M+3)]
  +2 sqrt(B+sinh B) sqrt(2B)t_M.

Each τ_j(M) is a fixed-profile complete tail, computable by the exact whole-norm-minus-prefix identity. These quantities tend to zero by Parseval; t_M tends to zero as well. This supplies a quantitative bound in terms of explicitly defined finite-profile tails. It does not claim the entire source has an O(M^(−2)) tail: the endpoint-profile tails, including translated jumps, need not have that rate.

The profile normalization is

p_0=sqrt(2B)e_0,
p_1=(sqrt(2B)/3)(e_2/sqrt5−e_0).

Writing G_ij=〈T_MFe_{2i},T_MFe_{2j}〉,

τ_0²=2B G_00,
τ_1²=(2B/9)[G_00+G_11/5−2 Re(G_01)/sqrt5].

Without the cross entry, the safe alternative is

τ_1≤sqrt(2B)/3[sqrt(G_00)+sqrt(G_11)/sqrt5].

Thus the first two diagonal entries can give a triangle bound with these scale factors, but the e_2 diagonal alone is not the p_1 tail.

The required finite-profile constants have not been numerically certified. The fixed t_h remainder is valid as a fixed upper bound but cannot alone establish a vanishing M→∞ rate; t_M corrects that issue.

### A5. The response bound M_resp≤ρ_L I is valid under the actual extra assumption

Use the original high Hilbert space X. Assume:

- a>0, 0<c≤a, and ρ=(a+c)^(−1).
- A_0=aI+2vv* is bounded and positive.
- P=B_plus is a nonnegative self-adjoint form/operator and B_*=P+A_0≥aI, with the form-sum meaning understood.
- H_X is the self-adjoint operator associated with A_0+C_g, where C_g is a densely defined closed form satisfying C_g≥cI.
- R=H_X^(−1).

The actual constants satisfy the required c=c_L≤a: the source gives a>4/5 and c_L=78638069/35169763328<1/100.

Define the bounded response operator by its positive form representation

M_resp=B_*^(−1)P B_*^(−1)+B_*^(−1)A_0 R A_0B_*^(−1).

The first term is rigorously (P^(1/2)B_*^(−1))*P^(1/2)B_*^(−1); it equals B_*^(−1)−B_*^(−1)A_0B_*^(−1). Therefore

M_resp=B_*^(−1)−B_*^(−1)D B_*^(−1),
D=A_0−A_0 R A_0.

Form ordering gives R≤(A_0+cI)^(−1), hence

D≥c A_0(A_0+cI)^(−1)≥dI,
d=ac/(a+c).

Thus

0≤M_resp≤B_*^(−1)−dB_*^(−2)≤ρI.

The last inequality follows from the scalar function f(b)=1/b−d/b² on b≥a. It is decreasing there when c≤a because 2d≤a, and f(a)=1/(a+c). No commutativity between P and A_0, or between C_g and either of them, was assumed.

The sharp response bound therefore follows from the full form-order assumption above; an inverse norm bound alone is insufficient.

The condition is substantive: with scalar a=1, c=3, A_0=1, P=1, H_X=4, one has ρ=1/4 but M_resp=5/16>ρ. The general bound does not follow from positivity and R≤ρI alone without additional structure or conditions.

### A6. Exact all-coefficient residual identity and its domains

Let the low coefficient space be ℂ^16, and define the exact maps

Z=B_*^(−1) Y E,
F_0=A_0Z,
U=P^(1/2)Z,

where E injects the orthonormal low coordinates. These are bounded maps from a finite-dimensional space to X. Let J:ℂ^16→D(H_X) be a linear trial map whose sixteen columns all belong to the operator domain. Then H_XJ is bounded as a map from ℂ^16 to X, and

N=F_0−H_XJ

is an X-valued residual map. The matrices J*H_XJ and F_0*J are ordinary finite Gram/pairing matrices; no unrestricted adjoint of an unbounded product is being invoked.

Using RH_XJ=J and H_XRF_0=F_0 gives the exact identity

F_0*RF_0=F_0*J+J*F_0−J*H_XJ+N*RN.

Because R≤ρ_LI,

F_0*RF_0≤F_0*J+J*F_0−J*H_XJ+ρ_LN*N.

This is one Loewner inequality valid simultaneously for every low coefficient vector, not sixteen unrelated diagonal inequalities. Adding the complete B_plus term yields

C_16=U*U+F_0*RF_0
≤U*U+F_0*J+J*F_0−J*H_XJ+ρ_LN*N.

If J has only form-domain columns, the displayed L² residual H_XJ need not exist. One must either require operator-domain trials as above or formulate and certify a different dual-form residual theorem. The operator-domain hypothesis is not optional in this formula.

### A7. Safe Loewner treatment of source, truncation, and interval errors

For illustration, suppose certified approximations satisfy

||U−Û||≤δ_U,
||F_0−F̂||≤δ_F,
N̂=F̂−H_XJ,

with exact admissible J. Then the following is a valid common upper matrix:

C_16≤Û*Û+F̂*J+J*F̂−J*H_XJ+ρ_LN̂*N̂+eI,

e=2δ_U||Û||+δ_U²+2δ_F||J||
  +ρ_L[2δ_F||N̂||+δ_F²].

The estimate follows by expanding each Gram product and bounding the Hermitian cross terms in operator norm. Any uncertainty in J, H_XJ, or the remaining finite integrals needs its own rigorous allowance; it is not covered by δ_F automatically.

If the exact source map YE is approximated by Ŷ with ||YE−Ŷ||≤δ_Y and the full B_* inverse is retained exactly, then safe propagation bounds are

δ_F≤(||A_0||/a)δ_Y,
δ_U≤δ_Y/sqrt(a).

The second follows from P≤B_* as forms. A_0B_*^(−1) must not be called an L² contraction merely from A_0≤B_*; noncommutativity forbids that shortcut. Additional approximation of the full-pole inverse requires its own error budget.

To turn entrywise outward intervals into a Loewner enclosure, choose a Hermitian center Ĉ and a symmetric nonnegative entry-radius matrix r. Then

||C−Ĉ||≤max_i Σ_j r_ij

is a valid Hermitian spectral error bound (a Frobenius radius is another safe option). Therefore Ĉ+δI is an upper enclosure, and Ĉ−δI a lower enclosure, for a certified δ. Entrywise upper endpoints alone do not form a Loewner upper matrix.

The remaining sufficient finite condition is a certified Hermitian inequality

Q_lower−ε_out I−C_upper≥λI

on all complex low coefficients, with the intended λ≥0 or λ>0. No such sign is established here.

### A8. Additional scope corrections

- The auxiliary graph form domain D_g∩X must not be silently substituted for the original minimum high Gamma domain V_high when transferring the physical lower bound. Domain enlargement is allowed in the specific inverse relaxation, not as an unproved equality of original form domains.
- The original realization, source binding, physical form identities, shell costs, and original form topology/core remain separate assumptions or proof obligations. The H² estimate does not discharge them.
- A proposed expression ℓ[f]+||f||² is not automatically a positive form norm without the required semibound and correct original Hilbert norm.
- A support-exhaustion argument need not have a B-uniform strictly positive gap if all it seeks is nonnegativity and has a genuine form core. Uniform-gap exhaustion is one sufficient strategy, not a necessary condition for every global proof.

