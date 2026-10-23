# Joint same-frequency plane in the original minimum domain

## 1. Result and dependency boundary

Let I=[14,29/2], C(x)=cosh(x/2), and use the full, unscaled theta source κ, W=κ/C. For γ∈I put

    u0(x)=W(x)cos(γx),         u1(x)=−xW(x)sin(γx),
    h0(x)=cos(γx)/C(x),       h1(x)=−xsin(γx)/C(x).

Use precisely the minimum closed jump form (E,D), weighted Hilbert space H, signed form ℓ and closed source-generated space N specified below. Define

    p0=P_(N⊥)h0,             p1=P_(N⊥)h1.

The analytic bridge proves:

1. Both h0,h1, and every linear combination, belong to D by common compact-core approximation. Both p0,p1 belong to D∩N⊥.
2. For every i,j∈{0,1},

       ℓ(pi,pj)=ℓ(hi,hj)
               =Q_inv(ui,uj)+2 μ(ui)μ(uj),
       (μ(u0),μ(u1))=(Ξ(γ),Ξ′(γ)).

   All displayed vectors and coefficients are real. The corresponding Hermitian statement also holds after complexification.
3. If G_inv=[[a,c],[c,b]], the complete projected Gram is exactly

       G_projected=G_inv+2 [Ξ,Ξ′]^T[Ξ,Ξ′].                 (1)

   It is NOT asserted to equal G_inv. The extra matrix is positive semidefinite of rank at most one, possibly zero.
4. Consuming the separately proved physical theorem a>0 and b−c²/a>1/62500 gives strict positivity on the entire projected two-dimensional plane, and proves that p0,p1 are independent. The independence is a consequence of the joint Gram, not of separate positive diagonals.
5. The supporting estimates actually proved in the physical proof also give a>9/100 and 0<c<1/125. Consequently, for every nonzero real (r,t), uniformly in γ∈I,

       ℓ(rp0+tp1)>(r²+t²)/64000.                         (2)

   This is a coefficient-space bound for this precisely defined ordered pair, not a global spectral-gap bound or a claim that these vectors are H-orthonormal.
6. Since 1∈N, the changed physical vectors κpi have zero pole moment. Their full and pole-free polarized Grams agree with (1):

       Q_inv(κpi,κpj)=Q_full(κpi,κpj)=ℓ(pi,pj).

The classical Jacobi identity, classical explicit formula for compact smooth convolution tests, unconditional zero-counting bound, and standard Fourier/closed-form representation theory remain external analytic inputs. The physical Schur inequality and its supporting rational bounds remain the separately proved physical theorem. The new steps are joint minimum-domain admission, polarized nullspace projection, independence, and the coefficient estimate. No global positivity, root simplicity, cross-frequency positivity, maximal-domain identification, or RH is concluded.

## 2. Analytic inputs

The physical inequalities are proved in [PHYSICAL_PROOF.md](PHYSICAL_PROOF.md). The classical Jacobi identity, compact-test explicit formula, unconditional zero-counting estimate and closed-form representation theory are external inputs. For the explicit-formula normalization see Connes and Consani, arXiv:2006.13771v1, Appendix B, equations (147)–(150), (152)–(153): https://arxiv.org/html/2006.13771v1#A2. The arguments required for admission and projection are supplied below.

## 3. The actual minimum closed form

Notation: ξ(s)=s(s−1)π^(−s/2)Γ(s/2)ζ(s)/2, Ξ(z)=ξ(1/2+iz), and F_u(z)=∫_R u(x)exp(−izx)dx. N(T) counts nontrivial zeta zeros with 0<Im(ρ)≤T, including multiplicities; the corresponding two-sided count has the same O(T log(2+T)) bound.

On x≥0,

    κ(x)=exp(x/2) Σ_(n≥1)(4z_n²−6z_n)exp(−z_n),
    z_n=πn²exp(2x).

Jacobi inversion gives its even smooth continuation. Positivity follows term by term on x≥0 and then by evenness. For every fixed derivative order j, all derivatives decrease faster than every exponential. Direct Mellin substitution, first on Re s>1 and then by continuation, gives

    ∫κ(x)exp((s−1/2)x)dx=ξ(s),
    F_κ(z)=Ξ(z),    ∫κC=1/2.

Thus dν=2κC dx is a probability measure. Let H=L²_even(R,ν), with conjugate-linear-first inner products, and let the defining core be

    C_core=C_c^∞(R)∩H.

Write ρ(s)=exp(−s/2)/(1−exp(−2s)), s_n=log n and a_n=Λ(n)/sqrt(n), including every prime power. On the core,

    E(f)=∫_0^∞ρ(s)∫κ(x)κ(x+s)|f(x+s)−f(x)|² dx ds
         +Σ_(n≥2)a_n∫κ(x)κ(x+s_n)|f(x+s_n)−f(x)|²dx.

Its closure from C_core is (E,D), and A is its nonnegative self-adjoint form operator. The signed closed form and operator are

    ℓ(f,g)=E(f,g)−〈f,g〉H/2+〈f,1〉H〈1,g〉H/2,
    L=A−I/2+P_1/2,        D(L)=D(A).

Here P_1 is the orthogonal projection onto 1 because ν(R)=1. Bounded perturbation gives ℓ≥−||f||H²/2 and the form norm is equivalent to (E(f)+||f||H²)^(1/2).

Closability is not an extra numerical admission assumption. Combine the continuous and countable atomic edge measures. They are sigma-finite on bounded x, with s bounded above and away from zero. Their endpoint marginals preserve Lebesgue null sets. For a sequence tending to zero in H whose edge differences are edge-L² Cauchy, select a subsequence tending to zero Lebesgue-almost everywhere, using κC>0. Its differences tend to zero almost everywhere for the edge measure. Their edge-L² limit is therefore zero. Smooth compact even functions are dense in H; their energies are finite by the small-s derivative bound and theta decay. This constructs exactly the required minimum closure, without identifying it with a maximal jump-energy space.

## 4. Exact source identity and its closure extension

For even physical functions put

    μ(u)=∫C(x)u(x)dx,
    DΓ(u)=∫_0^∞ρ(s)||u−τ_su||₂²ds,
    cΓ=logπ+EulerGamma+π/2+3log2,
    Q_full(u)=DΓ(u)−cΓ||u||₂²
              −2Σ_(n≥2)a_n Re〈u,τ_(s_n)u〉₂+2|μ(u)|².

Q_inv is the same expression with the last term removed. On even functions the polarized prime term is equivalently the two-orientation expression. The shift is τ_su(x)=u(x+s).

### 4.1 External explicit formula and source radicality

Insert Φ(y)=y^(−1/2)C_u(log y) into the classical multiplicative explicit formula for compact smooth even u, with C_u its autocorrelation. The finite-place contribution is exactly −2Σa_n C_u(log n). The two poles sum to 2|μ(u)|². The coupled archimedean subtraction is

    −(log(4π)+EulerGamma)||u||₂²
    −2∫_0^∞[exp(s/2)C_u(s)−||u||₂²]/(exp(s)−exp(−s)) ds.

Using ||u−τ_su||₂²=2(||u||₂²−C_u(s)) and

    2∫_0^∞(exp(s/2)−1)/(exp(s)−exp(−s)) ds=π/2+log2

gives exactly DΓ−cΓ||u||₂². There is no uncoupled divergent subtraction. The polarized zero expression is

    Q_full(u,v)=Σ_ρ overline(F_u(conjugate(z_ρ))) F_v(z_ρ),
    z_ρ=(ρ−1/2)/i.

All nontrivial zeros with multiplicities occur, and their unconditional strip bound |Im z_ρ|<1/2 suffices; reality of z_ρ is not assumed.

For physical cutoff control define

    M(u)=||u||H¹(dx)+||exp(|x|)u||₂,
    S₂(u)=Σ_(j=0)^2 ∫exp(|x|)|u^(j)(x)|dx.

Small/large shift splitting gives DΓ(u)≤C(||u′||₂²+||u||₂²). The weighted correlation inequality

    |〈u,τ_sv〉₂|≤exp(−|s|)||exp(|x|)u||₂||exp(|x|)v||₂

and ΣΛ(n)n^(−3/2)<∞ control the prime pairing. Weighted Cauchy–Schwarz controls μ. Therefore |Q_full(u,v)|≤C M(u)M(v). For the zero expression, integration by parts twice gives

    |F_u(z)|≤4 S₂(u)/(1+|z|)²,    |Im z|≤1/2.

Together with N(T)=O(T log(2+T)), this proves continuous extension of the polarized zero expression under S₂ cutoff convergence. Theta derivatives and all their smooth cutoffs have the required M and S₂ convergence. Since

    F_(κ^(2j))(z)=(−1)^j z^(2j)Ξ(z),

one obtains, for every fixed j and compact smooth even physical v,

    Q_full(κ^(2j),v)=0.                                   (3)

This is a polarized radical identity, not an inference from a zero quadratic value of an indefinite form.

### 4.2 Core algebra and minimum extension

Apply (3) for j=0 to v=κ|f|². The exact edge identity

    |aF−bG|²−(a−b)(a|F|²−b|G|²)=ab|F−G|²

with positive real a,b gives the continuous jump energy. Symmetrizing the two prime orientations gives exactly one coefficient a_n in E. The local terms cancel. The pole difference is

    2|μ(κf)|²−2μ(κ)μ(κ|f|²)
      =−||f||H²/2+|〈1,f〉H|²/2.

Thus, by polarization,

    ℓ(f,g)=Q_full(κf,κg),    f,g∈C_core.                  (4)

For the closure extension set Uf=sqrt(2κC)f and B=sqrt(κ/(2C)), so κf=BUf. U is unitary; multiplication by κ is not. B is bounded and B(x)≤C exp(−|x|). Hence

    Kp=Σa_n M_B(τ_(s_n)+τ_(−s_n))M_B

converges in operator norm because each shift sandwich is bounded by C²exp(−s_n) and ΣΛ(n)n^(−3/2)<∞. The core identity also reads

    E(f)=||f||H²/2+DΓ(κf)−cΓ||κf||₂²−〈Uf,KpUf〉₂.        (5)

If f_m is form-Cauchy, (5) applied to differences shows κf_m is Cauchy in the closed DΓ graph norm. Its L² limit is κf because multiplication by B is bounded. All bounded terms and μ(κf)=〈1,f〉H/2 pass to the limit. Consequently (4) holds for every f,g∈D, with the absolutely bounded prime pairing and finite DΓ energy. This is an identity on κD, not a claim of surjectivity onto a maximal physical domain.

## 5. Joint cutoff admission, not a diagonal-only inference

For γ∈I and real r,t let h=rh0+th1, u=κh=ru0+tu1. The estimates

    |h0(x)|≤2exp(−|x|/2),
    |h1(x)|≤2|x|exp(−|x|/2)

show h∈H. The functions u,u′ decrease faster than every exponential, uniformly when γ∈I and r²+t²≤1. These assertions follow from the actual theta decay and bounded γ; no lower bound on a Fourier transform or root assumption is needed.

Choose one common smooth even cutoff χ_R, equal to one on [−R,R] and zero outside [−2R,2R], with derivative O(1/R). Then

    χ_R h→h in H,       M(χ_Ru−u)→0.

For d=(χ_R−χ_S)h, the compact identity (4) gives

    E(d)=Q_full(κd)+Varν(d)/2
        ≤C M((χ_R−χ_S)u)²+||d||H²/2 →0.

Thus the same cutoff family converges in the minimum form norm for every combination, uniformly on bounded coefficient sets and this compact γ band. Completeness proves h∈D. Applying polarized continuity to the paired cutoffs establishes all four joint Gram entries in (4). This supplies the cross term directly; separate cosine/tangent diagonal positivity is not being promoted to joint positivity.

The pole moments are exact:

    μ(u0)=∫κ(x)cos(γx)dx=Ξ(γ),
    μ(u1)=d/dγ ∫κ(x)cos(γx)dx=Ξ′(γ).

Differentiation is justified by theta decay. Therefore the unprojected h-plane has Gram G_inv+2[Ξ,Ξ′]^T[Ξ,Ξ′].

## 6. Operator-null source space and whole-Gram preservation

Define g_j=κ^(2j)/κ and N=closure_H span{g_j:j≥0}. The fixed-order theta ratio estimate

    |κ^(m)(x)/κ(x)|≤C_m exp(2m|x|)

is essential here: rapid decay of numerator and denominator separately would not suffice. To verify it, on x≥0 put z=πexp(2x); the differentiated series has absolute bound by a fixed multiple of

    exp(x/2)z^(m+2)exp(−z)
      ·Σ_(n≥1)n^(2m+4)exp(−(n²−1)π).

The series is finite, and the positive first summand bounds κ below by a fixed multiple of exp(x/2)z²exp(−z). Parity handles x<0. Consequently every g_j∈H, and κg_j=κ^(2j) with its derivative has rapid decay. The same cutoff proof of §5 gives g_j∈D, one fixed j at a time.

For k∈C_core, combine (3), cutoff convergence and (4) to get ℓ(g_j,k)=0. Core density and form continuity extend this to every k∈D. The operator representation criterion then gives

    g_j∈D(L),      Lg_j=0.

For finite source combinations n_m→n in H, Ln_m=0→0; closedness of L proves n∈D(L) and Ln=0. Hence

    N⊂D(L)∩ker L.                                        (6)

There is no need for a uniform estimate in j or an assertion N=ker L.

For any f∈D, P_Nf∈N⊂D(L)⊂D and ℓ(P_Nf,k)=0 for every k∈D. Therefore

    P_(N⊥)f∈D∩N⊥,
    ℓ(P_(N⊥)f,P_(N⊥)g)=ℓ(f,g),    f,g∈D.                (7)

This proves the entire bilinear/Hermitian Gram identity, not merely diagonal preservation. The projection need not preserve E, H norms, the original physical vectors, or Q_inv before restoring the pole. Since every g_j is real, N is invariant under conjugation; its orthogonal projection preserves real-even vectors.

Applying (7) to h0,h1 proves (1). Since g_0=1∈N,

    μ(κpi)=〈1,pi〉H/2=0.

The actual projected physical modes are ui−κP_Nhi. They need not retain the original explicit cosine/tangent shape, but they belong to κD and their pole-free polarized form is exactly (1).

## 7. Independence, exact Schur transfer, and quantified coefficients

The physical input, for this same γ, is

    a=Q_inv(u0)>0,
    c=Q_inv(u0,u1),
    S=b−c²/a>1/62500.

Thus

    Q_inv(ru0+tu1)=a(r+(c/a)t)²+S t².                    (8)

For every nonzero (r,t) this is strictly positive. Adding 2(rΞ+tΞ′)² is nonnegative, so (1) is positive definite. If rp0+tp1=0 in H, its ℓ value would be zero, contradicting (8) unless r=t=0. The projected vectors are therefore independent, even if no explicit projection coefficients are known.

An optional exact check on the full Gram's Schur complement is useful. Put X=Ξ(γ), Y=Ξ′(γ), k=c/a. Its first pivot is A=a+2X²>0, and direct expansion gives

    (b+2Y²)−(c+2XY)²/(a+2X²)
       =S+[2a/(a+2X²)](Y−kX)² ≥ S >1/62500.            (9)

No strictly positive pole gain is claimed: the square can vanish. Equation (9) is an algebraic consequence of the positive rank-one update, not an entrywise-order argument with an unknown cross sign.

For a coefficient-space constant, the PHYSICAL_PROOF.md §§10–11 proves

    a>a_bar>9/100,
    0<c<c_bar=(21/1000)M+13/20000−A_overlap/25,
    M≤7/20,       A_overlap≥0.

Therefore c<147/20000+13/20000=1/125, and 0<k<4/45. For y=r+kt,

    r²+t²=(y−kt)²+t²
          ≤2y²+(1+2k²)t²
          ≤2y²+(2057/2025)t².

Meanwhile

    a>9/100>2/64000,
    S>1/62500>2057/(2025·64000).

The second comparison is the exact integer inequality

    62500·2057=128562500 <129600000=2025·64000.

Substituting into (8), at least one square is nonzero, and gives

    Q_inv(ru0+tu1)>(r²+t²)/64000.

Adding the pole square and using (7) proves (2). The more conservative 1/125000 coefficient constant follows as well. Neither estimate uses numerical evaluation of a,b,c,Ξ,Ξ′ or of projection coefficients.

If desired, a plane-only H-normalized consequence follows with the explicit finite positive integral

    C_plane=2∫(1+x²)W(x)dx.

Pointwise Cauchy–Schwarz and contraction of the H projection show

    ||rp0+tp1||H²≤||rh0+th1||H²≤C_plane(r²+t²).

Thus every nonzero f in this particular plane satisfies

    ℓ(f)/||f||H²>1/(64000 C_plane).

This is uniform over this two-mode family and the fixed band only. C_plane has not been numerically evaluated, and no global normalized coercivity follows.

## 8. Constraint distinction and remaining limits

The unprojected modes are not automatically in N⊥. Integration by parts gives

    〈g_j,h0〉H=2(−1)^j γ^(2j)Ξ(γ),
    〈g_j,h1〉H=2(−1)^j[2jγ^(2j−1)Ξ(γ)+γ^(2j)Ξ′(γ)].

For h=rh0+th1, the j=0 and j=1 constraints are equivalent, since γ>0, to

    rΞ+tΞ′=0,      tΞ=0.

These equations imply all higher generator constraints. In particular:

- If Ξ≠0, the unprojected plane intersects N⊥ only in zero.
- If Ξ=0 and Ξ′≠0, that intersection is the cosine line.
- If Ξ=Ξ′=0, the whole unprojected plane lies in N⊥.

These are conditional algebraic classifications, not claims that a particular root is simple, multiple or even present. The projected-plane theorem does not require any of them to hold.

The analytic bridge has no remaining minimum-domain or polarized-projection gap under the stated classical inputs and exact operator definitions. It does not prove those external theorems from first principles or reprove all scalar estimates in the frozen physical theorem. It does not compute P_N, identify N with the entire kernel, establish operator-domain membership of the two trial modes, identify a maximal form domain, compare different γ values, give a dense positive core, or prove positivity outside these same-frequency projected two-planes. Positivity of each such plane separately says nothing about mixed terms between different planes. No RH or global spectral conclusion is obtained.
