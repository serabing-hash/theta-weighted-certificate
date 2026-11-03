# Negative spectral counts from the finite-head scalar trace

3 November 2026 UTC. Independent mathematical audit and standalone consequence of the scalar trace decomposition. No originality or literature claim is made. This note does not assert positivity, a gap at zero, or trace-class membership of the negative part.

## 1. Actual setting and full domains

Let

    H = L²_even(dx/W), W(x) = κ(x)/(2 cosh(x/2)),
    κ(x) = e^(x/2) Σ_(n≥1) (4π²y²−6πy)e^(−πy),
    y = n²e^(2x), x≥0, κ(−x)=κ(x).

The exact normalization is ||κ||_H²=1. Put C=I−κ⊗κ, H_c=κ^⊥, and let J:H→L²_even(dx) be inclusion. The ordinary Fourier transform F is unitary with factor (2π)^(-1/2). Set

    cΓ = log π + γ + π/2 + 3 log 2,
    d(t) = Σ_(l≥0) 2t²/[a_l(a_l²+t²)], a_l=2l+1/2,
    X_c = {u∈H_c : ∫d(t)|FJu(t)|²dt<∞}.

The complete centered form and its self-adjoint representative are

    q[u] = ∫d(t)|FJu(t)|²dt − cΓ||Ju||² − p_all[u],
    L_c associated with q on X_c.

Here p_all retains every prime power. The theta envelope and paired-shift estimate give, for every integer N≥1,

    W(x) ≤ 40 exp(4|x|−πe^(2|x|)),
    ||D_(>N)|| ≤ τ_N := 80 Σ_(n>N) Λ(n)n^(3/2)e^(−πn)
                    ≤ 160(N+1)²e^(−π(N+1)).             (1)

Indeed, for s=log n, the geometric mean of the two weight envelopes is bounded by 40 exp(2v−πe^v), where v=|x|+|x+s|≥s. This function decreases for v≥0, so each oriented shift has norm at most 40Λ(n)n^(3/2)e^(−πn). Pairing orientations and summing proves the first bound. For the last bound use Λ(n)≤log n≤√n and the ratio of consecutive n²e^(−πn), at n≥2, being less than 1/2. This is an H-operator-norm convergence assertion, not a boundedness assertion for the infinite tail from all ordinary L² into H.

Bounded W makes J bounded. The closed operator √d FJ on its natural domain gives a closed nonnegative form. Restriction to H_c is closed and densely defined: center smooth even compactly supported approximants using one fixed smooth even compactly supported test with nonzero κ-pairing. No domain assumption about κ is needed for this density argument. The complete correction is bounded by (1), so q is closed and semibounded on exactly X_c.

## 2. Positive trace-class defect of every finite head

For N≥1 define

    c_N(t) = cΓ + 2 Σ_(2≤n≤N) Λ(n)n^(−1/2) cos(t log n),
    C_N = cΓ + 2 Σ_(2≤n≤N) Λ(n)n^(−1/2),
    a_N = (d−c_N)_+, b_N = (c_N−d)_+.

Finite-head Plancherel and the complete tail convergence give the exact form identity

    q[u] = ∫a_N(t)|FJu(t)|²dt − ⟨u,B_Nu⟩_H
                                      − ⟨u,D_(>N)u⟩_H, (2)
    ⟨u,B_Nu⟩_H = ∫b_N(t)|FJu(t)|²dt,
    u∈X_c.

The positive a_N form has exactly the domain X_c because |a_N−d|≤C_N. If A_N denotes its associated nonnegative self-adjoint operator, then L_c=A_N−B_N−D_(>N), as a bounded perturbation on Dom A_N. In particular (2) is not restricted to a numerical test bank.

An integral comparison in the positive decreasing a-variable gives

    d(t) ≥ (1/2)log(1+4t²).

Therefore 0≤b_N≤C_N, and b_N vanishes for |t|≥T_N, where

    T_N = (1/2)√(e^(2C_N)−1) < e^(C_N)/2.              (3)

For even inputs the actual Fourier evaluation vector in H is

    g_t(x) = W(x)cos(tx)/√(2π).

Its centered version is Cg_t, not a unit coordinate vector. Positivity of κ and the normalization imply

    B₀ := ∫W ≤ 1/4,
    h(t) := ||Cg_t||_H² ≤ ||g_t||_H² ≤ B₀/(2π) ≤ 1/(8π).

Indeed W=(2cosh(x/2)κ)/(4cosh²(x/2)) and the numerator has integral 1. Thus the positive rank-one integral

    B_N = ∫_R b_N(t) |Cg_t⟩⟨Cg_t| dt

is trace class, with its true H trace satisfying

    tr B_N = ∫_R b_N(t)h(t)dt
           ≤ (1/(4π))∫₀^T_N [C_N−(1/2)log(1+4t²)]dt
           = [T_N−(1/2)arctan(2T_N)]/(4π)
           < e^(C_N)/(8π).                            (4)

Here b_N(t)≤[C_N−(1/2)log(1+4t²)]_+; the elementary antiderivative and log(1+4T_N²)=2C_N give the equality. Dropping the logarithm also gives the looser cap C_N T_N/(4π). The rank-one integral is trace-norm integrable by the displayed uniform bound and compact frequency support.

## 3. Negative spectral count and strict integer rounding

For δ>0 write

    n_−(δ) = dim Ran 1_(-∞,−δ)(L_c).

For every finite N and δ>τ_N,

    n_−(δ) ≤ dim Ran 1_(δ−τ_N,∞)(B_N).                 (5)

Proof: the right side is finite since B_N is trace class. If the negative spectral subspace of L_c had greater dimension, it would contain a nonzero vector u orthogonal to the displayed B_N spectral subspace. Semiboundedness makes Ran 1_(-∞,−δ)(L_c) a bounded spectral subspace, contained in Dom L_c. For this u, (2) would give q[u]≥−δ||u||_H², whereas its negative spectral support gives q[u]<−δ||u||_H². This is a contradiction.

If S>0 is any upper bound for tr B_N and U≥τ_N with δ>U, (5) yields

    n_−(δ) ≤ ceil(S/(δ−U)) − 1.                       (6)

The strict rounding matters at an integer ratio: k eigenvalues strictly larger than δ−U have sum strictly larger than k(δ−U). If tr B_N=0 one may use n_−(δ)=0 directly. The weaker floor(S/(δ−U)) bound is always safe, but loses one at exact positive integer ratios.

For the closed convention the corresponding exact statement is

    dim Ran 1_(-∞,−δ](L_c)
        ≤ dim Ran 1_[δ−τ_N,∞)(B_N).

Indeed the orthogonal complement of this B_N subspace has strictly smaller Rayleigh quotient than δ−τ_N, contradicting q[u]≤−δ||u||² on the closed negative spectral subspace. With trace cap S and tail cap U, this gives the always-safe floor(S/(δ−U)) bound. All asymptotic conclusions below also hold for that convention.

## 4. Fully explicit logarithmic prime cutoff

For 0<δ≤1 choose

    j = ceil(log₂(2/δ)), m = max(8,j), N=m−1.

Then

    τ_N ≤ 160m²e^(−πm) ≤ e^(−πm/2) ≤ 2^(−m) ≤ δ/2.   (7)

For the middle estimate, 160m²≤e^(πm/2) at m=8 follows already from π>3, e>5/2, and 160·8²<(5/2)^12. Its logarithmic ratio increases for real m≥8 because π/2−2/m>0. The next inequality uses π/2>log 2. This proves (7) with no numerical root finding.

The elementary full von Mangoldt estimate is

    Σ_(2≤n≤N) Λ(n)/√n ≤ 4(log 2)√N+5.                 (8)

It needs neither PNT nor a zero-location assertion. To check it independently, use the binomial recurrence ψ(n)≤ψ(ceil(n/2))+n log 2. The binomial coefficient covers every prime power strictly between ceil(n/2) and n. Iterating ceil(n/2^k) down to 1 gives ψ(x)≤2(log 2)x+log x+log 2 for real x≥1. Partial summation then gives even the stronger upper bound

    Σ_(2≤n≤N) Λ(n)/√n
        ≤ 4(log 2)√N + 2−log 2−2/√N,

which implies (8). Using cΓ<6 and 8 log 2<6, set

    K_N = 16+6√N, so C_N≤K_N.

Combining (4), (6), and (7) gives the explicit count certificate

    n_−(δ) ≤ ceil( e^(K_N)/(4πδ) ) − 1,
    N=max(8,ceil(log₂(2/δ)))−1.                       (9)

This is a deliberately coarse closed-form certificate; the actual trace and actual finite tail expression can be much smaller. Since N=O(1+log(1/δ)), (9) gives

    n_−(δ) ≤ δ^(−1) exp(O(√(1+log(1/δ)))), δ↓0.       (10)

Even without (8), Λ(n)≤log n and Σ_(n≤N)n^(−1/2)≤2√N give C_N≤cΓ+4√N log N. The same proof then yields δ^(−1)exp(O(√L log L)), with L=1+log(1/δ), which is still δ^(−1−o(1)). Thus the subpolynomial correction and Schatten conclusion do not depend on accepting (8).

## 5. Compact negative part and Schatten consequence

Let L_- = (−L_c)_+. It is bounded because L_c is semibounded. For every δ>0, (5) and (7) show that 1_(δ,∞)(L_-) has finite rank. The finite-rank operators L_-1_(δ,∞)(L_-) approximate L_- in norm with error at most δ. Hence L_- is compact.

For every p>1, choose 0<ε<p−1. Equation (10), or its elementary weaker replacement, implies n_−(δ)≤C_ε δ^(−1−ε) near zero. The layer-cake identity

    tr(L_-^p) = p∫₀^||L_-|| δ^(p−1)n_−(δ)dδ

therefore converges. Consequently

    (L_c)_- ∈ S_p for every p>1.                       (11)

No S_1 conclusion follows from these estimates. They also do not prove finite total negative index, the existence or absence of negative eigenvalues, a quantitative gap at zero, or positivity on a low collar. If negative eigenvalues exist, the result permits infinitely many accumulating only at zero.

## 6. Two immediate implemented finite-threshold certificates

The independently rebuilt, platform-specific MPFI scalar certificate gives

    tr B₂ < S = 0.05699308,
    τ₂ < U = 0.03861903.

These are safe decimal upper caps for the corresponding recorded upper endpoints; U is not a lower bound on the actual tail norm. Exact decimal arithmetic gives

    2(0.08−U) = 0.08276194 > S,
    3(0.06−U) = 0.06414291 > S.

Thus

    dim Ran 1_(-∞,−0.08)(L_c) ≤ 1,
    dim Ran 1_(-∞,−0.06)(L_c) ≤ 2.                      (12)

The same two bounds also hold with closed right endpoints, because both comparisons are strict. These are upper bounds on multiplicity below the stated levels, not claims that one or two negative eigenvalues actually exist.

The numerical input retains its existing qualification: the C interval computation was independently reproduced on its stated x86_64 LP64 / MPFI / MPFR platform, but no formal proof-assistant verification or complete official-header ABI comparison was performed. This audit did not rerun the numerical integration; it checked the deductions and rational threshold arithmetic from the audited output.

## 7. Cheap positive-block norm refinement with all cross terms retained

Let B≥0 be trace class, P a genuine orthogonal projection, and Q=I−P. Then

    ||B|| ≤ ||PBP||+||QBQ||
          ≤ ||PBP||+tr(QBQ)
          = λmax(PBP)+tr B−tr(PBP).                  (13)

For the zero finite block, λmax means its nonnegative operator norm. To prove (13), write u=p+q with p=Pu and q=Qu. Positivity gives the exact cross-term estimate

    |⟨p,Bq⟩|² ≤ ⟨p,Bp⟩⟨q,Bq⟩.

Putting α=||PBP|| and β=||QBQ||, one obtains

    ⟨u,Bu⟩ ≤ (√α||p||+√β||q||)²
            ≤ (α+β)||u||².

Thus no off-diagonal block is discarded. Trace additivity gives tr(QBQ)=tr B−tr(PBP), without requiring P to commute with B.

For an actual independent H-column bank V=(v₁,…,v_r), let

    G=V*V>0, K=V*BV, P=VG^(−1)V*,
    M=G^(−1/2)KG^(−1/2).

Then ||PBP||=λmax(M) and tr(PBP)=tr(G^(−1)K)=tr M. If certified bounds give tr B≤S, λmax(M)≤α_up, and tr M≥t_low, the safe conclusion is

    ||B|| ≤ α_up+S−t_low.                             (14)

The inputs being valid guarantee S−t_low≥0. A dependent bank must first be reduced to its true support; it cannot be assigned an identity Gram or an unverified inverse. Only a small finite matrix is needed once its actual H Gram and B matrix entries are certified. The savings over the scalar trace cap are the certified mass of the finite block beyond its largest eigenvalue. A one-dimensional block gives no exact improvement from this lemma alone; a larger block can, but substantial improvement is not guaranteed before its entries are evaluated. Numerical conditioning and entry errors must be included.

For B=B_N, (2) and (14) give a safe lower form bound

    L_c ≥ −(α_up+S−t_low+U) I,

where U≥τ_N. This refinement does not require an inverse of A_N, a collar projection, or an identification of the full kernel. It supplies a finite certification route, not a claim that such a bank has already been computed.

## 8. Kernel scope, comparison, and independence

The proof holds on all H_c and never projects onto a finite radical bank. Let N_rad be the closed span of the known derivative radicals, and let P₀=1_{0}(L_c) be the entire kernel projection. If the separately established identities N_rad⊂ker L_c are used, both N_rad and ker L_c are reducing zero subspaces, so removing either does not change any strictly negative spectral count. No equality N_rad=ker L_c or effective projection rate is needed. In fact no radical identity is needed anywhere in Sections 1–5.

The count bound (10) is asymptotically much smaller than the earlier exp(O(δ^(−1)√(1+log(1/δ)))) negative-count upper bound from signed Fourier-cell compression. This improves the counting consequence, not the separate norm approximation or rank bound for compressed prime-tail operators. The new argument uses the complete finite-head multiplier sign and a trace-class negative defect, rather than approximating the entire correction to δ-relative accuracy on a collar.

The only ingredients are the actual theta normalization and envelope, the full Gamma symbol, finite-head Plancherel, complete prime-tail convergence, a true centered H trace, and the min–max principle. No RH premise, inherited fixed-gap estimate, inverse sign, finite Gram identity approximation, unknown full-kernel identification, or low-collar positivity is used.

### Local provenance

- SCALAR_BRACKET_PROOF_AND_CODE_CONSTANTS.md: actual H, X_c, L_c, centered evaluation vectors, complete tail, and numerical trace caps.
- TRACE_MPFI_FULL_AUDIT_20261103.md: independent build/reproduction and retained platform qualification.
- ../residual_gram_sign_attack_20261103/LOW_COLLAR_EXPLICIT_TAIL_COMPRESSION_AND_FINITE_RADICAL_CERTIFICATES.md, §1: elementary prime-sum bound.
- ../residual_gram_sign_attack_20261103/LOW_COLLAR_SIGNED_FOURIER_CELL_COMPRESSION.md: previous negative-count bound and its separate compression scope.
