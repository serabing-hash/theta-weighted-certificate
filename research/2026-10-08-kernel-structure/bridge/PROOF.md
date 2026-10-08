# Analytic bridge from the minimum theta weighted form to Weil positivity

Date: 7 October 2026 UTC. Scope: the exact infinite theta source and the minimum closed even form in the supplied paper. Status: supplied analytic bridge argument awaiting independent review. Publication copy: this introductory status sentence alone has been changed; the mathematical body is preserved. This is a self-contained bridge argument, not a proof of RH, a numerical regeneration, external human peer review, or formal proof-kernel verification. No matrix, FFT, Gram, or action computation was performed.

## Result

For the definitions in the supplied paper, the following are equivalent:

1. The Riemann hypothesis.
2. The actual arithmetic Weil quadratic form is nonnegative on every real-even physical test in C_c^∞(R).
3. The weighted signed form ℓ is nonnegative on its real-even compact smooth core.
4. The same minimum closed weighted operator L is nonnegative.
5. E(f) ≥ (1/2) Var_ν(f) for every f in the minimum form domain.

The bridge does not require the minimum domain to equal a maximal jump-energy domain, a unitary equivalence with a separate physical Weil operator, a selected ground state, state alignment, a growing-degree estimate, or any numerical inclusion. Its nontrivial symmetry step is proved below: if RH is false, one fixed real-even compact smooth test gives a negative value. Dividing this test by the strictly positive smooth theta source places it in the very core used to define the current L. It even belongs to the operator domain.

The still-unproved statement needed for RH is L ≥ 0 itself. The fixed delta = 1/32 certificate leaves a genuinely negative interval untreated and remains conditional on its numerical-inclusion contract. This audit removes a bridge ambiguity; it does not remove that positivity problem.

## 1. Objects and conventions

All inner products are conjugate-linear in the first variable. Set

    ξ(s) = (1/2)s(s−1) π^(−s/2) Γ(s/2) ζ(s),
    Ξ(z) = ξ(1/2+iz),       F_h(z) = ∫_R h(x)e^(−izx) dx,
    κ(x) = e^(x/2) Σ_{n≥1}(4z_n²−6z_n)e^(−z_n),
    z_n = πn²e^(2x),        w(x) = 2κ(x)cosh(x/2),
    dν = w dx,              H = L²_even(R,ν;C),
    ρ(s) = e^(−s/2)/(1−e^(−2s)),
    c_n = Λ(n)/√n,          s_n = log n,
    c_Γ = log π + γ_E + π/2 + 3log 2.

Here Λ contains every prime power. For even physical functions define

    C_h(s) = ∫ conjugate(h(x)) h(x+s) dx,
    μ(h) = ∫ h(x)cosh(x/2) dx,
    D_Γ(h) = ∫_0^∞ ρ(s) ||h−τ_s h||²_2 ds,
    Q(h) = D_Γ(h) − c_Γ||h||²_2
           − 2 Σ_{n≥2} c_n C_h(s_n) + 2|μ(h)|².            (1)

For an even complex h, C_h is real and even: reflection gives C_h(−s)=C_h(s), whereas conjugation gives C_h(−s)=conjugate(C_h(s)). Its polarization defines the Hermitian Q(h,k). In particular the prime expression in the supplied paper, containing both orientations, equals (1).

On C = C_c^∞(R;C) ∩ H let

    E(f) = ∫_0^∞ ρ(s)∫ κ(x)κ(x+s)|f(x+s)−f(x)|² dx ds
           + Σ_{n≥2} c_n∫ κ(x)κ(x+s_n)|f(x+s_n)−f(x)|² dx. (2)

Let (E,D) be its minimum closure from C, A its nonnegative self-adjoint form operator, P_1 f = 1⟨1,f⟩_ν, and

    L = A − I/2 + P_1/2,
    ℓ(f) = E(f) − ||f||²_ν/2 + |⟨1,f⟩_ν|²/2.             (3)

The term minimum means precisely the closure of this core. No maximal-domain claim is inserted.

## 2. Theta properties and exact probability normalization

Put S(x)=e^(x/2)Σ_{n≥1}exp(−πn²e^(2x)). Jacobi inversion gives

    S(x)−S(−x) = (e^(−x/2)−e^(x/2))/2.

Direct differentiation gives κ=(∂_x²−1/4)S. The right side of the preceding difference is killed by this differential expression, so κ is even. On x≥0 every summand defining κ is positive because z_n≥π>3 and 4z_n²−6z_n>0. Hence κ>0 on all R.

On compact sets the series and every fixed derivative converge locally uniformly. On x≥0, each derivative is e^(x/2) times a sum of fixed-degree polynomials in z_n multiplied by e^(−z_n). Polynomial-Gaussian domination, then evenness, gives for each j and each B>0

    sup_x e^(B|x|)|κ^(j)(x)| < ∞.                          (4)

Thus κ is smooth and every fixed derivative decreases faster than every exponential at both ends. A quantitative envelope or a finite theta truncation is not needed here.

For Re s>1, absolute convergence and y=ne^x give

    ∫ κ(x)e^((s−1/2)x) dx
      = ζ(s)∫_0^∞(4π²y⁴−6πy²)e^(−πy²)y^(s−1)dy
      = (1/2)s(s−1)π^(−s/2)Γ(s/2)ζ(s) = ξ(s).

The left side is entire by (4); continuation proves the identity everywhere. Evenness gives F_κ(z)=Ξ(z). Taking s=0 and s=1, where ξ has value 1/2, yields

    ∫κ(x)e^(x/2)dx = ∫κ(x)e^(−x/2)dx = 1/2,
    μ(κ)=1/2,                  ν(R)=1.                    (5)

Consequently P_1 is exactly the orthogonal rank-one projection in (3). Both κ and w are strictly positive smooth even functions. Multiplication by κ is a bijection from real-even C_c^∞ onto real-even C_c^∞; the inverse is h↦h/κ, smooth on the compact support and everywhere because κ never vanishes.

## 3. Match with the actual explicit formula

This section fixes the constants, prime sign, and pole. It is not a definition of a substitute Weil form.

Use the classical multiplicative explicit formula in Connes–Consani, Appendix B, equations (147)–(153), with

    Φ(u) = u^(−1/2) C_h(log u),       u>0.

For compact smooth even h, Φ is compact smooth. More explicitly, if g(u)=u^(−1/2)h(log u), then Φ=g*conjugate(g^sharp) in the multiplicative convolution algebra. Thus this is exactly the convolution square in the arithmetic Weil criterion. Its Mellin transform at s=1/2+iz is

    Φ̃(1/2+iz) = F_h(z) conjugate(F_h(conjugate z)),          (6)

using evenness. The zero multiset includes every nontrivial zero with its multiplicity. Write z_ρ=(ρ−1/2)/i. The two pole terms of that formula sum to 2|μ(h)|². Its finite-place contribution is

    Σ_p log p Σ_{m≥1}[Φ(p^m)+Φ^sharp(p^m)]
      = 2Σ_{n≥2} Λ(n)n^(−1/2) C_h(log n).

This contribution is subtracted from the pole terms. The negative of the archimedean contribution is

    −(log(4π)+γ_E)||h||²_2
    −2∫_0^∞ [e^(s/2)C_h(s)−||h||²_2]/(e^s−e^(−s)) ds.     (7)

Keep the subtraction coupled at s=0. Since

    ||h−τ_sh||²_2 = 2(||h||²_2−C_h(s)),

(7) is D_Γ(h)−c_Γ||h||²_2. In fact its additional constant is

    2∫_0^∞ (e^(s/2)−1)/(e^s−e^(−s)) ds
      = ψ(1/2)−ψ(1/4) = π/2+log 2.

Thus c_Γ=log π+γ_E+π/2+3log 2, with no omitted finite part. Equivalently its Fourier multiplier is Re ψ(1/4+it/2)−log π, consistent with the paper.

We have therefore established the unmodified identity

    Q(h) = Σ_ρ F_h(z_ρ) conjugate(F_h(conjugate(z_ρ))).     (8)

For real-even h, the entire F_h is even and real on the real axis, so this simplifies to

    Q(h) = Σ_ρ F_h(z_ρ)².                                  (9)

It is not Σ|F_h(z_ρ)|² off RH. Under RH all z_ρ are real and (8) does become a sum of absolute squares.

The compact-test sum converges absolutely: integration by parts gives arbitrary polynomial decay in the strip |Im z|≤1/2, and the unconditional zero counting bound is N(T)=O(T log(2+T)). No zero-location assumption is used to derive (8).

## 4. Continuity needed for source cancellation and cutoffs

The following estimates make every extension in this audit explicit.

For physical u,v let a useful controlling norm be

    M(u) = ||u||_{H¹(R)} + ||e^{|x|}u||_2.

For finite M the pole integral is finite by Cauchy–Schwarz. Also

    D_Γ(u) ≤ c_0||u'||²_2 + c_1||u||²_2,
    c_0 = ∫_0^1 s²ρ(s)ds <∞,
    c_1 = 4∫_1^∞ρ(s)ds <∞.                                (10)

The kernel is O(1/s) at zero and O(e^(−s/2)) at infinity. Cauchy–Schwarz for its difference integral controls the polarized Gamma form. For either sign of s,

    |∫conjugate(u(x))v(x+s)dx|
        ≤ e^(−|s|)||e^{|x|}u||_2 ||e^{|x|}v||_2.            (11)

This follows from |x|+|x+s|≥|s|. The resulting prime majorant contains ΣΛ(n)n^(−3/2), bounded by the convergent Σ(log n)n^(−3/2). Equations (10)–(11) and the pole bound prove

    |Q(u,v)| ≤ C M(u)M(v)                                  (12)

for a finite absolute C on the even sector. This is continuity of a signed form, not positivity.

For the zero side define

    S_2(u) = Σ_{j=0}² ∫e^{|x|}|u^(j)(x)|dx.

For |Im z|≤1/2, two integrations by parts and the elementary unintegrated bound give

    |F_u(z)| ≤ 4 S_2(u)/(1+|z|)².                           (13)

The constant is inessential; it follows by treating |z|≤1 and |z|≥1 separately. Consequently the sum in (8) is jointly continuous under S_2 convergence because Σ_ρ(1+|z_ρ|)^(−4)<∞.

If u and all fixed derivatives satisfy (4), choose an even smooth χ with χ=1 on [−1,1], support in [−2,2], and χ_R(x)=χ(x/R). Then

    M(χ_Ru−u)→0,             S_2(χ_Ru−u)→0.                (14)

Leibniz's rule, the factors R^(−j), and exponentially weighted dominated convergence prove both limits. Hence (8) extends to these rapidly decreasing even functions, and to mixed pairings with compact smooth even tests, without treating Q as L²-continuous.

Taking u=κ and a compact smooth even k, F_κ=Ξ vanishes at every z_ρ. The polarized version of (8), justified by (12)–(14), gives the unconditional weak identity

    Q(κ,k)=0.                                              (15)

This independently supplies the source cancellation needed below. It does not require a closed physical Weil operator. The same argument gives Q(κ^(2j),k)=0 for every fixed j, but only j=0 is needed for this bridge.

## 5. The exact source transform and its minimum closure

Take f∈C and apply (15) to k=κ|f|². The elementary edge identity, with a,b real and F,G complex, is

    |aF−bG|² − (a−b)(a|F|²−b|G|²) = ab|F−G|².

Subtract Q(κ,κ|f|²) from Q(κf). The local −c_Γ terms cancel. Symmetrizing the two orientations of each prime edge gives exactly c_n κ(x)κ(x+s_n)|f(x+s_n)−f(x)|². There is no extra factor two. For the pole, (5) gives

    μ(κf) = (1/2)∫f dν,
    μ(κ|f|²) = (1/2)∫|f|² dν,
    2|μ(κf)|² − 2μ(κ)μ(κ|f|²)
         = −(1/2)(||f||²_ν−|∫f dν|²).

All mixed pairings are controlled by (12). Finite shift truncations followed by these bounds and nonnegative monotone convergence justify the jump expansion. Therefore

    Q(κf) = E(f) − (1/2)Var_ν(f) = ℓ(f),     f∈C.           (16)

This is the exact sign and pole coefficient in the supplied paper.

For completeness, (2) is densely defined and closable. Combine its continuous and countable atomic edges into a positive sigma-finite measure in (x,s). Sigma-finiteness follows by bounded x and 1/k≤s≤k. On such restrictions each endpoint marginal is absolutely continuous with respect to Lebesgue measure; translations preserve null sets, including each atomic shift. If f_j→0 in L²(ν) and their differences are edge-L² Cauchy, a subsequence tends to zero Lebesgue almost everywhere because w>0. Both endpoint values then tend to zero almost everywhere for the edge measure. Thus its edge-L² limit is zero. This is closability. Compact smooth even functions are dense in L²_even(ν), since w is positive and locally smooth. Their energies are finite by the small-shift derivative estimate and theta decay. These facts construct exactly the minimum closure used here.

The bounded perturbation in (3) makes ℓ closed on D and L self-adjoint on D(A), with L≥−I/2. Its form norm is equivalent to E(f)+||f||²_ν. Therefore positivity on C extends to D, and positivity on D is equivalent to L≥0 by the representation/spectral theorem for closed forms.

The two maps in the paper remain distinct:

    Uf=√w f is unitary H→L²_even(dx),
    κf = bUf,              b=√(κ/(2cosh(x/2))).

The second is not unitary. No inference here treats it as unitary. It only needs to map the compact core bijectively to the physical compact tests.

There is also an exact extension of (16) on the image of D. To check it directly, b is bounded and satisfies b(x)≤C e^{−|x|} by (4). Hence

    K_p = Σc_n M_b(τ_{s_n}+τ_{−s_n})M_b

converges absolutely in operator norm, since each sandwich has norm at most C²e^(−s_n) and ΣΛ(n)n^(−3/2)<∞. On C, (16) is equivalently

    E(f) = ||f||²_ν/2 + D_Γ(κf) − c_Γ||κf||²_2
           − ⟨Uf,K_pUf⟩_2.                                (17)

For a form-Cauchy sequence f_j, applying (17) to differences shows that κf_j is Cauchy in the graph norm of the closed Fourier-multiplier form D_Γ. Since κf_j→κf in L², (17) passes to the minimum closure. The pole equals (1/2)|⟨1,f⟩_ν|² and is bounded there. This extension does not assert that every physical finite-energy function lies in this image or that minimum and maximal domains coincide.

## 6. Why real-even compact tests already detect every failure of RH

A general appeal to the full complex Weil criterion does not by itself justify an even restriction. The following direct argument closes that point.

Assume RH is false. Choose a zero z_0=a+ib of Ξ with b≠0. Its real part a is nonzero. Indeed the zeros of ξ lie in 0<Re s<1, and ζ has no real zero there: for real 0<s<1 the alternating Dirichlet eta series, grouped in positive consecutive pairs, is positive, whereas 1−2^(1−s)<0; hence ζ(s)=η(s)/(1−2^(1−s))<0. Therefore no zero z of Ξ is purely imaginary.

The functional equation and reality give four distinct zeros

    z_0, −z_0, conjugate(z_0), −conjugate(z_0),

all with the same finite multiplicity m≥1. Define

    R(z) = (z²−z_0²)(z²−conjugate(z_0)²),
    H_0(z) = Ξ(z)/R(z)^m.                                  (18)

Every apparent singularity is removable because the full multiplicity m has been divided out at all four distinct roots. H_0 is entire, even, real on the real axis, and nonzero at each chosen root. It still vanishes at every other zero of Ξ. This step does not assume simple zeta zeros.

Because Im(z_0²)=2ab≠0, there exist unique real α,β with

    α+βz_0² = i/H_0(z_0).

Set

    H(z) = (α+βz²)H_0(z).                                  (19)

Then H is entire, even, real on the real axis, and its values at the four selected zeros are respectively i,i,−i,−i. All its values at other zeros are zero.

### 6.1 Decay and inverse transform

The theta Fourier representation and (4), integrated by parts any fixed number of times, imply for every B,N>0

    sup_{|y|≤B} |Ξ(t+iy)| ≤ C_{B,N}(1+|t|)^(−N).            (20)

For example integrate the derivatives of e^(yx)κ(x) against e^(−itx); their L¹ norms are uniformly finite for |y|≤B. Division by the fixed polynomial R^m and multiplication by the fixed polynomial in (19) preserve (20): outside a bounded set |R(t+iy)| is comparable to |t|⁴, and inside that set the removable entire quotient is bounded. Thus H decreases rapidly on each fixed horizontal strip.

Define

    h(x) = (1/2π)∫_R H(t)e^(itx)dt.

The real-even symmetry gives real-even h. The rapid strip decrease allows differentiation under the integral and contour translation to Im z=B for x>0 and to Im z=−B for x<0. The vertical sides tend to zero by (20). For each derivative order j,

    |h^(j)(x)| ≤ C_{B,j} e^(−B|x|).                         (21)

Here B is any fixed positive number; no uniform-in-B estimate is asserted. Fourier inversion gives F_h=H on the real line and then everywhere by entire continuation, justified by (21).

### 6.2 One compact negative witness

Take h_R=χ_Rh with the real-even cutoffs of §4. These are real-even compact smooth functions. By (13)–(14), uniformly over the zero strip,

    |F_{h_R}(z)−H(z)| ≤ ε_R(1+|z|)^(−2),     ε_R→0,
    |F_{h_R}(z)|+|H(z)| ≤ C(1+|z|)^(−2).

Hence the zero-counting bound and dominated convergence show, using (9) only for the compact h_R,

    Q(h_R) = Σ_ρ F_{h_R}(z_ρ)²
       → Σ_ρ H(z_ρ)² = −4m.                               (22)

Each member of the selected quartet contributes −1 with multiplicity m. This proves the exact sign without confusing the off-line square with an absolute square. It also avoids needing to define Q(h) merely to obtain a compact witness. Separately (12) and (14) justify Q(h_R)→Q(h), so the extended expression is consistent.

Fix one sufficiently large finite R for which Q(h_R)<0, and set

    f_* = h_R/κ.

By §2, f_* is a fixed nonzero real-even member of C. By (16),

    ℓ(f_*) = Q(h_R) < 0.                                   (23)

The cutoff R is chosen once. It does not depend on an ensuing numerical shift, basis size, trial count, or approximation sequence. There is no claim that the uncut h/κ lies in H; division is used only after compact cutoff.

This proves the contrapositive of real-even sufficiency. The forward implication under RH follows at once from (8). Thus the compact real-even criterion is equivalent to RH.

## 7. The witness is also in the operator domain

The argument above already suffices at the form-core level. To avoid any ambiguity in “same domain,” every f∈C actually belongs to D(L).

Let u=Uf and h=κf=b u; h is compact smooth and in H²(dx). The Bochner integral

    G_Γ h = ∫_0^∞ρ(s)[2h−τ_s h−τ_{−s}h]ds

converges in L²: near zero its integrand before ρ is bounded by s²||h''||_2, and for large s by 4||h||_2. The vector

    v = b(G_Γ h−c_Γh) − K_pu
        + (1/2)√w ⟨√w,u⟩_2                               (24)

lies in L², because b is bounded, K_p is bounded as established above, and ||√w||_2=1. The polarization of (17) pairs v with every compact core test exactly as ℓ(f,·). Both sides are continuous in the minimum form norm, so core density extends the identity to all D. The closed-form representation theorem gives f∈D(L) and ULf=v. In particular (23) can be written ⟨f_*,Lf_*⟩_ν<0.

## 8. Exact implication chain and the remaining obstruction

Combine the preceding results:

    L≥0
      ⇒ ℓ(f)≥0 for every compact real-even f
      ⇒ Q(h)≥0 for every compact real-even h, via f=h/κ
      ⇒ RH, by §6.

Conversely,

    RH
      ⇒ Q(h)≥0 on every compact even complex h, by (8)
      ⇒ ℓ≥0 on C, by (16)
      ⇒ ℓ≥0 on D, by minimum-form density
      ⇒ L≥0.

Real and complex positivity agree for this real symmetric form: ℓ(f_1+if_2)=ℓ(f_1)+ℓ(f_2) for real f_1,f_2. No odd-sector estimate is needed.

Thus there is no additional analytic bridge lemma left between nonnegativity of this precise L and RH. The unsolved gate is the full inequality

    E(f) ≥ (1/2)Var_ν(f)   for all f∈D.                     (25)

Stating (25) as an assumption would merely assume the RH-equivalent missing step. The fact E≥0 by itself gives only L≥−I/2, not (25).

## 9. Exactly what the finite delta 1/32 result removes

The supplied paper, under its full-coordinate numerical-inclusion contract, proves

    L+I/32 ≥ c_32 I,
    c_32 = 2893974301919559083402996479244366770223445381007
           /9262063652338871903456269436750928556326912000000000.

Equivalently

    L ≥ −δ_eff I,     δ_eff = 1/32−c_32
                           ≈ 0.03093754540990562425 > 0.   (26)

Its strongest elementary spectral consequence is exclusion of (−∞,−δ_eff); equality at −δ_eff is not ruled out by a non-strict lower bound. In particular it excludes (−∞,−1/32], as the paper states. Possible negative spectrum in [−δ_eff,0) remains.

Via (16), for every compact real-even physical h it conditionally gives

    Q(h) ≥ −δ_eff ∫_R [2cosh(x/2)/κ(x)] |h(x)|² dx.          (27)

The norm on the right is the weighted norm of h/κ. It is not the ordinary physical L² norm, and multiplication by b does not permit replacing it by that norm with a uniform inverse constant. Inequality (27) is not Weil positivity.

If RH were false, §6 would provide one f_* with strictly negative Rayleigh quotient. Nothing in that construction bounds the quotient away from zero by δ_eff; (26) can coexist with such a witness. The finite certificate therefore supplies no contradiction to the hypothetical off-line zero.

A logically sufficient future route would be independently proved inequalities L≥−ε_j I on this same minimum closed operator with ε_j→0. Evaluating any fixed f∈D and taking j→∞ would then give L≥0 and RH. This sentence specifies the required quantifiers; it does not supply such estimates or justify a numerical extrapolation.

## 10. Audit provenance and limits

Input paper SHA-256:

    e900409bd91a0125e688c7c03c9935ebca090877e1c8bd0ba7d630647ec6e4ed

The local source snapshot is sources/theta_delta32_certificate_input.tex. The current paper §§2–3 were checked directly for normalization, closability, source cancellation, and pole algebra; its theorem at delta 1/32 was read only to delimit its consequence. The restored original ANALYTIC_ADMISSION_EN.md confirms the same minimum operator and retains numerical premises. No numerical integrations or matrix certificate were regenerated in this audit.

Relevant earlier records were checked narrowly: the 18 September source/Schur audit already contains the theta transform and a cofinal full-space Schur criterion; the 6 October exterior theorem inherits source radicality and proves the same even source transform. Neither is used as an unquestioned proof of the even-real restriction. Sections 3–7 above derive the present bridge and witness directly from the classical explicit formula, theta identity, and closed-form theory.

Primary references and checked formula locations are recorded in SOURCES.md. The source summaries there are retrieval notes, not quoted AI output. This argument is separate from the released paper and has not silently changed or promoted that paper's numerical or RH claims.
