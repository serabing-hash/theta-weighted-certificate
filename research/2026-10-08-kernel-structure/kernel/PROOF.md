# Theta derivative null vectors in the minimum weighted operator

8 October 2026 UTC. Analytic audit on the unchanged infinite theta source and the exact minimum closed even weighted operator. Original text in this directory is licensed CC BY-NC 4.0. This is an analytic argument, not a numerical evaluation, an external peer review, a proof-kernel verification, or a proof of the Riemann hypothesis.

## Result

For every fixed integer j ≥ 0,

    f_j = κ^(2j)/κ belongs to D(L), and L f_j = 0.

Here D(L) is the operator domain of the same minimum realization in the supplied paper. The family {f_j : j ≥ 0} is linearly independent. In particular, ker L is infinite-dimensional.

The mean is exactly ∫f_j dν = 4^(−j). Consequently the centered family

    g_j = f_j − 4^(−j)1,    j ≥ 1,

is linearly independent in ker L ∩ {1}⊥. Constant-only deflation, or any finite-dimensional deflation, leaves an infinite-dimensional exact kernel. None of these assertions determines whether L has negative spectrum.

The proposed cutoff proof is valid. Its essential point is to apply the compact source-transform identity to differences of compact approximants. That proves minimum-form Cauchy convergence. Merely proving finite maximal jump energy would not suffice.

## 1 Exact objects and inputs

Use the definitions and normalizations of the supplied bridge, PROOF.md §§1–5, and of the source paper §§2–3:

    κ(x) = e^(x/2) Σ_(n≥1) (4z_n²−6z_n)e^(−z_n),
    z_n = πn²e^(2x),
    w(x) = 2κ(x)cosh(x/2),    dν = w dx,    ν(R) = 1,
    H = L²_even(R,ν;C),       C = C_c^∞(R;C) ∩ H.

The nonnegative jump form E on C is

    E(f) = ∫_0^∞ ρ(s) ∫_R κ(x)κ(x+s)|f(x+s)−f(x)|² dx ds
           + Σ_(n≥2) c_n ∫_R κ(x)κ(x+s_n)|f(x+s_n)−f(x)|² dx,

where ρ(s)=e^(−s/2)/(1−e^(−2s)), c_n=Λ(n)/√n, and s_n=log n. Its minimum closure is (E,D), and A is its nonnegative self-adjoint form operator. Set

    P_1 f = 1⟨1,f⟩_ν,
    L = A − I/2 + P_1/2,    D(L)=D(A),
    ℓ(f,g) = E(f,g) − ⟨f,g⟩_ν/2
             + overline(⟨1,f⟩_ν)⟨1,g⟩_ν/2.

Inner products are conjugate-linear in the first variable. D has Hilbert norm

    ||f||_D² = E(f) + ||f||_H².

The physical signed form Q is the unchanged Gamma, prime, and pole expression of the supplied bridge. The inputs needed below are:

1. κ is strictly positive, smooth and even. Every fixed derivative decreases faster than every exponential at both ends.
2. The exact compact identity is

       ℓ(f,g) = Q(κf,κg),    f,g ∈ C.                 (1)

   Equivalently, E(f)=Q(κf)+Var_ν(f)/2 on C.
3. The signed form is jointly continuous under the controlling norm

       M(u)=||u||_(H¹(dx)) + ||e^|x|u||_2,
       |Q(u,v)| ≤ C_Q M(u)M(v).                       (2)

4. For every fixed j ≥ 0 and every compact smooth even physical k,

       Q(κ^(2j),k)=0.                                (3)

These are analytic inputs already established in the supplied bridge. For clarity, (2) follows from the small-shift estimate ||u−τ_su||_2 ≤ s||u′||_2, the large-shift estimate ≤2||u||_2, the weighted correlation bound

    |⟨u,τ_s v⟩| ≤ e^(−|s|)||e^|x|u||_2||e^|x|v||_2,

and Σ_(n≥2) Λ(n)n^(−3/2)<∞. The pole functional is bounded in M by Cauchy–Schwarz. This is continuity of a signed form, not positivity of Q.

Likewise, (3) is an inherited exact radical identity, not a consequence of RH. The entire Fourier transform satisfies

    F_(κ^(2j))(z) = (−1)^j z^(2j) Ξ(z).

It vanishes at every nontrivial-zero argument, irrespective of the zero's position. The bridge proves the mixed explicit-formula identity and its passage from compact cutoffs using the M norm and a separate weighted two-derivative L¹ norm. This gives (3) without choosing any global physical Weil operator.

## 2 The derivative ratio estimate

Fix an integer r ≥ 0. Define polynomials

    P_0(z)=4z²−6z,
    P_(r+1)(z)=P_r(z)/2+2zP_r′(z)−2zP_r(z).

Local uniform convergence of the differentiated theta series gives

    κ^(r)(x)=e^(x/2) Σ_(n≥1) P_r(z_n)e^(−z_n).

The degree of P_r is r+2. Hence there is a finite constant A_r such that

    |P_r(z)| ≤ A_r z^(r+2),    z ≥ π.

For x ≥ 0 put t=πe^(2x), so z_n=n²t and t ≥ π>3. Since all original summands are positive and P_0(t)≥2t²,

    κ(x) ≥ 2e^(x/2)t²e^(−t).

On the other hand,

    |κ^(r)(x)|
      ≤ A_r e^(x/2)t^(r+2)e^(−t)
         Σ_(n≥1) n^(2r+4)e^(−(n²−1)t)
      ≤ A_r S_r e^(x/2)t^(r+2)e^(−t),

where

    S_r = Σ_(n≥1) n^(2r+4)e^(−3(n²−1)) < ∞.

It follows that

    |κ^(r)(x)|/κ(x) ≤ (A_r S_r/2)t^r.

Evenness of κ implies |κ^(r)(−x)|=|κ^(r)(x)|. Absorbing π^r into the constant yields the global estimate

    |κ^(r)(x)|/κ(x) ≤ C_r e^(2r|x|).                  (4)

In particular,

    |f_j(x)| ≤ C_(2j)e^(4j|x|).                       (5)

All constants are permitted to depend on the fixed derivative order. There is no uniform-in-j or growing-degree claim. Positivity is used only for the explicit theta denominator on x≥0, not for Q or L.

Since κ decreases faster than every exponential,

    ∫|f_j|²dν
      ≤ 2C_(2j)² ∫κ(x)cosh(x/2)e^(8j|x|)dx < ∞.      (6)

Thus f_j∈H. Strict positivity of κ also makes f_j smooth and even. No estimate of f_j′ is needed in the minimum-domain argument below: the physical product κf_j is exactly κ^(2j), whose fixed derivatives already have the required decay.

## 3 Admission to the minimum form domain

Choose an even χ∈C_c^∞ with 0≤χ≤1, χ=1 on [−1,1], and support in [−2,2]. Let R≥1 and

    χ_R(x)=χ(x/R),    f_(j,R)=χ_R f_j ∈ C,
    u_j=κ^(2j),       u_(j,R)=κf_(j,R)=χ_R u_j.

By (6) and dominated convergence,

    ||f_(j,R)−f_j||_H → 0.                            (7)

The fixed-order theta decay and the product rule give

    M(u_(j,R)−u_j) → 0.                              (8)

For example, the derivative difference is

    (χ_R−1)u_j′ + R^(−1)χ′(x/R)u_j.

The first term converges to zero in L² by dominated convergence, and the second does so by the uniform derivative bound and u_j∈L². The exponentially weighted term in M follows directly from dominated convergence.

For two radii R,S, put d_(R,S)=f_(j,R)−f_(j,S)∈C. The compact identity (1), not an unproved noncompact extension, gives

    0 ≤ E(d_(R,S))
      = Q(u_(j,R)−u_(j,S)) + Var_ν(d_(R,S))/2
      ≤ C_Q M(u_(j,R)−u_(j,S))²
         + ||d_(R,S)||_H²/2.                          (9)

Both terms tend to zero by (7)–(8). Thus the compact sequence is Cauchy in ||·||_D. Since D is precisely the completion of C for this closed form norm, its H-limit f_j belongs to D and

    f_(j,R) → f_j in D.                              (10)

This proves minimum-form admission directly. It does not assume that the closure equals a maximal jump-energy domain. It also does not require Q≥0: the upper bound in (9) uses |Q| and the lower bound uses only the defining nonnegative jump energy.

## 4 Admission to the operator domain and exact action

Let g∈C. By (1), (2), and (8),

    ℓ(f_j,g)
      = lim_(R→∞) ℓ(f_(j,R),g)
      = lim_(R→∞) Q(u_(j,R),κg)
      = Q(u_j,κg)
      = 0.                                          (11)

The first limit follows from (10). The last equality is (3), since κg is again smooth, even, and compactly supported.

The form ℓ is continuous on D×D: its E term is controlled by the Cauchy–Schwarz inequality for a nonnegative form, and its remaining terms are bounded H forms. Because C is dense in D, (11) extends to

    ℓ(f_j,g)=0 for every g∈D.                        (12)

The representation theorem for the closed semibounded form ℓ says that f∈D belongs to D(L) precisely when its form pairing against D is represented by an H vector. In (12) that vector is zero. Therefore

    f_j∈D(L),    Lf_j=0,    j≥0.                     (13)

This is stronger than Q(u_j)=0 or ℓ(f_j)=0. A zero diagonal value of a signed form would not establish a null vector. The full mixed radical identity and the minimum closure are both used.

## 5 Linear independence and centering

Suppose a finite combination Σ_(j=0)^m a_j f_j vanishes in H. Since w>0 everywhere, it vanishes Lebesgue almost everywhere. Multiplication by κ and continuity give

    Σ_(j=0)^m a_j κ^(2j)(x)=0 for every x.

Taking Fourier transforms yields

    [Σ_(j=0)^m a_j(−1)^j t^(2j)] Ξ(t)=0,    t∈R.

The Fourier transform Ξ is not identically zero, since κ is a nonzero integrable function. By continuity there is a nonempty interval where Ξ is nonzero. The polynomial vanishes on that interval and is therefore identically zero. Every a_j is zero. Thus the family in (13) is linearly independent.

Integration by parts 2j times is legitimate by the fixed-order theta decay. As (d/dx)^(2j)cosh(x/2)=4^(−j)cosh(x/2),

    ⟨1,f_j⟩_ν
      =2∫κ^(2j)(x)cosh(x/2)dx
      =4^(−j) 2∫κ(x)cosh(x/2)dx
      =4^(−j).                                      (14)

For j≥1, set g_j=f_j−4^(−j)f_0. Then

    g_j∈D(L)∩{1}⊥,    Lg_j=0.

Their independence follows from the independence of the original family including f_0=1. In particular,

    dim(ker L∩{1}⊥)=∞.                               (15)

Also, because D(A)=D(L),

    Ag_j=g_j/2,
    E(g_j)=||g_j||_H²/2=Var_ν(g_j)/2.                (16)

More generally these identities hold on every finite linear span of the centered family. Thus A has 1/2 as an infinite-multiplicity eigenvalue, while L has zero as an infinite-multiplicity eigenvalue. Under the standard self-adjoint essential-spectrum convention, 0∈σ_ess(L). No assertion that these vectors exhaust ker L is made.

## 6 Consequences for shifts and finite deflation

### 6.1 Exact margin ceiling

For every δ>0 and nonzero f∈ker L,

    (L+δI)f=δf.

Consequently any valid lower bound

    L+δI ≥ c_δ I

must satisfy c_δ≤δ. The conclusion remains true after restricting the form to the orthogonal complement of any finite-dimensional subspace F: the intersection ker L∩F⊥ is infinite-dimensional. If F does not reduce L, this statement concerns the form restriction or compression, not an unjustified operator restriction.

In particular, constant-only deflation leaves infinitely many vectors with shifted Rayleigh quotient exactly δ. It cannot create a strictly positive gap for unshifted L on {1}⊥, or a positive gap uniform as δ tends to zero. It can still be a useful finite-dimensional algebraic reorganization; the conclusion does not reject such a reorganization.

### 6.2 Finite-rank positive frames

Let W:C^m→H be bounded with m finite, and define

    H_δ=L+δI+WW*.

Because K=ker L is infinite-dimensional and W*|_K has finite rank,

    dim(K∩ker W*)=∞.

Every f in this intersection belongs to D(H_δ)=D(L) and obeys H_δf=δf. Therefore δ is an infinite-multiplicity eigenvalue of H_δ, and any coercivity estimate H_δ≥η_δ I has η_δ≤δ.

At δ=0 no finite-rank WW* can make L+WW* coercive on all H, even if L itself were nonnegative. Finite-dimensional deflation does not remove this obstruction. This limits a zero-shift or uniform-margin strategy; it does not preclude a separate strictly positive certificate at each δ>0.

### 6.3 The observation-side lower barrier

For completeness there is a purely analytic matrix consequence, without evaluating any new overlaps. Assume δ>0 and H_δ≥ηI for some η>0, so its inverse is bounded. Set

    B_δ=W*H_δ^(−1)W.

Let K_0 be any closed subspace of ker L, let P_0 be its orthogonal projection, and put C_0=W*P_0W≥0. The variational formula for a positive inverse, with its supremum restricted to K_0, gives

    B_δ ≥ C_0(δI+C_0)^(−1).                           (17)

Indeed, for z∈C^m the full variational supremum over f∈D(H_δ) of

    2 Re⟨Wz,f⟩ − ⟨f,H_δf⟩

is ⟨Wz,H_δ^(−1)Wz⟩. On K_0, its quadratic term is

    δ||f||² + ||W*f||².

Maximizing there gives the right side of (17); the identity follows by setting V=P_0W and using

    V*(δI+VV*)^(−1)V=C_0(δI+C_0)^(−1).

If c_0=||C_0||>0, any bound B_δ≤(1−ε)I must therefore obey

    ε ≤ δ/(δ+c_0).                                    (18)

The constant-mode bound is the case K_0=span{1}, where C_0=(W*1)(W*1)* and c_0=||W*1||². Additional null directions may yield a stronger observation-side bound, but (17) supplies no new numerical value. In particular, the existence of infinitely many null vectors by itself does not establish a larger c_0 or a numerical delta64 failure beyond the already certified constant-mode obstruction.

## 7 What is inherited and what was checked here

The all-orders physical radical family is already in the supplied bridge §4 and in older source records. The derivative-ratio estimate, weighted integrability, centered saturation family, and obstruction to a strictly larger global Poincaré constant are also present in earlier records. They are not claimed as discoveries of this audit.

The source paper already admits 1 and κ''/κ to the precise minimum D(L) and proves their null action in its subsection “The two noncompact source directions.” Thus the j=0 and j=1 operator statements are explicitly inherited, too.

The exact additional check here is that the compact-difference argument (9) admits every fixed order to the same minimum D; the mixed pairing then admits it to the same D(L). Linear independence makes the infinite-dimensional kernel conclusion explicit, and §§6.1–6.3 record its finite-deflation and certificate implications. This is a bounded local provenance statement, not a claim of global literature priority.

## 8 Audit limits and verdict

No fatal premise, uncontrolled derivative ratio, circular Weil positivity, or minimum-domain gap was found in the candidate argument once the estimates and compact-difference step above are stated explicitly.

The proof does not establish L≥0, RH, absence of negative spectrum, completeness of the displayed kernel, a growing-order estimate, any new numerical observation norm, or a new inclusion certificate. It does not change the source, phase, H actions, FFT data, Gram data, observation map, or operator realization. No numerical source, phase, H, FFT, Gram, or eigensolver evaluation was performed.

Verdict: the all-orders minimum-operator null-family statement is analytically supported by the exact inherited identities and the displayed minimum-closure proof.
