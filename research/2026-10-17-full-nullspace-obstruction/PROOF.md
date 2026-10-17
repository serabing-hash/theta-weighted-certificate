# Bounded-energy escape after imposing every theta-source orthogonality condition

17 October 2026 UTC. Analytic research result on the actual infinite theta
source and the minimum closed even form. `RH_PROOF=NOT-OBTAINED`.

The constants below concern the actual κ, not a truncated theta series.
This is a proof by analytic estimates and existence of zeros; no zeros,
large matrices, or physical integrals are numerically evaluated.

## 1. Statements and scope

Use κ, c, ν, H, E, D, A, L, and N from SOURCE_AUDIT.md. Write

```text
f_j=κ^(2j)/κ, j≥0;   f_0=1;
N=closed span_H {f_j:j≥0}.
```

This equals the closed span of 1 and the centered generators
`f_j-4^(-j)`, j>=1. The space N is the known source-generated space;
no equality N=ker L is assumed or concluded.

**Theorem 1 (escape with all constraints).** There exist real, smooth, even
functions `h_m∈D∩N⊥`, of H norm one, and a fixed finite constant C such that,
for every sufficiently large integer m,

```text
|E(h_m)−1/2| ≤ C m³ exp(−sqrt(m)).                       (1.1)
```

For every fixed T<∞,

```text
||1_[−T,T] h_m||_H² → 0;    h_m ⇀ 0 in H.             (1.2)
```

Every moment `⟨f_j,h_m⟩_H`, for every j≥0, is exactly zero. This is not a
finite-moment approximation or a numerical residual statement. The theorem
does not determine the sign of `E(h_m)−1/2`.

**Corollary 2 (precise obstructions).** After imposing every condition from N:

1. No ε>0 satisfies `E(h)≥(1/2+ε)||h||_H²` for all `h∈D∩N⊥`.
2. No fixed finite T and a>0 satisfy
   `||1_[−T,T]h||_H≥a||h||_H` on that space. This remains false if it is
   restricted to unit vectors with `E(h)≤1/2+ε`, for any ε>0.
3. For every admissible fixed envelope R in ENVELOPE_AUDIT.md,
   `D_R(h_m)→0` and `∫V|h_m|²dν→0`. Consequently no positive C can satisfy
   `D_R(h)≥C||h||_H²`, and no finite nonnegative a,b and fixed T can satisfy
   `||h||_H²≤a D_R(h)+b||1_[−T,T]h||_H²` on `D∩N⊥`.

The last claim uses the independently checked ground-state identity, with
the actual half measure and minimum domain. It does **not** refute
`F(g)≤D(g)`: both sides along this sequence tend to zero and their ordering
is not determined. In particular it is not an RH counterexample.

**Theorem 3 (local density).** Let S<∞. The restrictions to [−S,S] of the
root modes defined in §3 span a dense subspace of `L²_even([−S,S],ν)`.
Those modes are all in `D∩N⊥`. No assertion that they span N⊥ globally is
needed or made.

Theorems 1 and 3 are the new results of this package relative to the local
repository sources inspected. No claim of worldwide priority is made.

## 2. Source estimates and admission to the minimum domain

For x≥0 let y=π exp(2x). Positivity of the first summand and domination of
the remaining Gaussian series give fixed constants a_0,a_1>0 such that

```text
a_0 exp(9x/2−π exp(2x)) ≤ κ(x)
                         ≤ a_1 exp(9x/2−π exp(2x)).    (2.1)
```

For example the lower constant can be `a_0=2π²`, since
`4y²−6y≥2y²` for y≥π. For the upper bound, factor out the n=1 Gaussian:
`Σ n⁴ exp(−(n²−1)y)≤Σ n⁴ exp(−3(n²−1))<∞`.
Differentiating the summands gives, for each fixed r,

```text
|κ^(r)(x)|≤C_r exp(2r x) κ(x), x≥0.                   (2.2)
```

Evenness supplies the corresponding estimates at the other end. All fixed
derivatives decrease faster than every exponential. Put

```text
W(x)=κ(x)/c(x), x≥0.
```

Then `(W+|W'|)exp(ax)` is integrable and bounded for every fixed a≥0.

We use the exact source identity, with the constants in the source audit:

```text
E(h)=||h||_H²/2+D_Γ(κh)−c_Γ||κh||_2²
      −2 Σ(n≥2) Λ(n)/sqrt(n) Re⟨κh,τ_(log n)(κh)⟩_2. (2.3)
```

Here `D_Γ(u)=∫_0^∞ρ(s)||u−τ_su||_2²ds` and
`c_Γ=logπ+γ_E+π/2+3log2`. Formula (2.3) first holds on the core and
extends to D by the compact-difference and closed Fourier-form argument
in the manuscript. It is not a positivity assertion for the signed form.

We record the domain argument needed for every function constructed below.
Suppose h is smooth and even, belongs to H, and `u=κh` and its first
derivative decrease faster than every exponential. Let χ_R be even smooth
cutoffs equal to one on [−R,R], zero outside [−2R,2R], with the usual
uniform derivative bounds. Then

```text
χ_R h→h in H,
χ_R u→u in M,   M(u)=||u||_(H¹(dx))+||exp(|x|)u||_2.
```

The signed physical form Q satisfies `|Q(u,v)|≤C M(u)M(v)`.
Indeed the Gamma part follows from `||u−τ_su||≤min(s||u'||,2||u||)`,
the pole from weighted Cauchy–Schwarz, and the prime part from

```text
|⟨u,τ_s v⟩|≤exp(−|s|)||exp(|x|)u||_2||exp(|x|)v||_2,
Σ(n≥2)Λ(n)n^(−3/2)<∞.                               (2.4)
```

For two cutoffs apply the **compact** identity
`E(d)=Q(κd)+Var_ν(d)/2` to `d=(χ_R−χ_S)h`. It proves that the
cutoffs are D-Cauchy. Their H limit is h, so h∈D, with (2.3) inherited
by convergence. This proves membership in the minimum domain, not merely
finite maximal jump energy. Constants can depend on each fixed h in this
admission argument; uniform estimates in m are proved separately below.

## 3. Exact root modes and all the orthogonality conditions

Let Z be the multiset of zeros of
`Ξ(z)=ξ(1/2+iz)=∫κ(x)exp(−izx)dx`. Every z∈Z has `|Im z|<1/2`.
If z has multiplicity d, define, for 0≤r<d,

```text
v_(z,r)(x)=[∂_z^r cos(zx)]/c(x).                    (3.1)
```

These functions are even, smooth, of at most polynomial times exponential
growth, and belong to H. Their physical products with κ have all fixed
derivatives rapidly decreasing. Thus §2 admits them to D.

For every j≥0, integration by parts and differentiation in z give

```text
⟨f_j,v_(z,r)⟩_H
 =2 ∂_z^r ∫κ^(2j)(x)cos(zx)dx
 =2 ∂_z^r [(-1)^j z^(2j)Ξ(z)] =0.                   (3.2)
```

The last equality holds because r is smaller than the multiplicity of the
zero. All integrals and integrations by parts are justified by theta decay.
This verifies every generator, including j=0, exactly. Closedness of N then
gives `v_(z,r)∈D∩N⊥`. Since N is generated by real functions, the real and
imaginary parts also satisfy all the constraints.

This construction uses neither `N=ker L` nor a location of zeros on the real
axis. Multiple and nonreal zeros are explicitly permitted.

## 4. Local density and compact-support uniqueness

### 4.1 Proof of Theorem 3

Suppose `v∈L²_even([−S,S],ν)` annihilates every restricted mode (3.1).
The entire function

```text
B(z)=2∫_[−S,S] κ(x)overline(v(x))cos(zx)dx
```

satisfies `|B(z)|≤C_v exp(S|Im z|)` by Cauchy–Schwarz on a compact set.
It vanishes at each z∈Z to at least its multiplicity, by the assumed
orthogonality. A nonzero entire function of this exponential type has
`O(r)` zeros in |z|≤r, counting multiplicity. To see this, remove any finite
order zero at the origin and apply Jensen's formula at radius 2r; the
growth bound makes the integrated zero count O(r), and the count at r is
at most that integral divided by log 2.

On the other hand, the unconditional Riemann–von Mangoldt formula gives

```text
N_ζ(T)=T/(2π) log(T/(2πe))+O(log T).                 (4.1)
```

Thus the zeros of Ξ in the disk have superlinear count. This is impossible
for a nonzero B, so B is identically zero. Fourier uniqueness for the
compact L¹ function `κ overline(v)` gives v=0. The annihilator is zero,
which proves local density. Real and imaginary parts give the real version.

The input (4.1) is classical and unconditional; the source checked here is
[Hasanalizade–Shen–Wong, Corollary 1.2](https://arxiv.org/pdf/2107.06506).
Only its asymptotic consequence is used.

### 4.2 Verification of the compact-support claim in the request

If h∈N⊥ has compact support, `f=hc` is compact L¹ and even. The function
`κ*f(t)` is analytic in `|Im t|<π/4`, by uniform convergence of the complex
theta series on compact subsets and compact support of f. All its
derivatives at zero vanish: the even ones are precisely (3.2)'s generator
moments without the root specialization, and the odd ones vanish by parity.
Hence it vanishes first near zero and then on the whole strip. On the real
line, Fourier transformation gives `Ξ·fhat=0`. The real zeros of the
nonzero entire Ξ are isolated; continuity of fhat and Fourier uniqueness
give f=0, hence h=0.

This proves the supplied compact-support candidate, but is not claimed as
a new idea. It does not extend this Fourier argument to arbitrary H
functions, since hc need not be tempered. It is compatible with Theorem 1:
the escaping functions are noncompact and are never cut off after imposing
their exact constraints.

## 5. Narrow zero clusters without computing any zeros

For an integer m set `T_m=exp(m³)`. By (4.1),

```text
N_ζ(2T_m)−N_ζ(T_m) ∼ T_m m³/(2π).
```

Partition [T_m,2T_m] into at most `mT_m+1` intervals of length at most
1/m. For every sufficiently large m, one interval contains at least m+1
zero arguments, counted with multiplicity. Select them as

```text
z_0,...,z_m,   λ_m≤Re z_j≤λ_m+1/m,
T_m≤λ_m≤2T_m,   |Im z_j|<1/2.                        (5.1)
```

An endpoint convention or a final shorter interval does not affect the
pigeonhole argument. Repeated nodes are allowed up to the actual zero
multiplicity. The height exp(m³) is only an existence device, chosen so
that its logarithm is polynomial in m and its size dominates the later
oscillatory error. No numerical feasibility is asserted.

Write `[z_0,...,z_m]F` for the divided difference, with confluent derivatives
at repeated nodes. Define the even exponential polynomial

```text
P_m(x)=m! i^(−m) [z_0,...,z_m] cos(zx).               (5.2)
```

It is a finite linear combination of the numerators in (3.1). Consequently
`p_m=P_m/c` belongs exactly to `D∩N⊥`.

For later bounds let θ be uniform probability measure on the simplex
`θ_j≥0, Σθ_j=1`, and put

```text
A_m(x)=E_θ exp(ix Σ_j θ_j(z_j−λ_m)).
```

The elementary divided-difference integral formula gives

```text
P_m(x)=x^m/2 [exp(iλ_m x)A_m(x)
                    +(-1)^m exp(−iλ_m x)A_m(−x)].    (5.3)
```

For completeness the integral formula is
`[z_0,...,z_m]F=(1/m!)E_θ F^(m)(Σθ_jz_j)`.
For distinct nodes it follows by repeated fundamental theorem of calculus
along straight complex segments. Both sides extend continuously to repeated
nodes. Alternatively, expanding an entire F in powers proves it from the
simplex moments and the complete homogeneous polynomial formula for divided
differences. It is valid for complex nodes, not just ordered real nodes.

For m≥2, (5.1) implies, for real x,

```text
|A_m(±x)|≤exp(|x|/2),   |A_m'(±x)|≤exp(|x|/2),
|P_m(x)|≤|x|^m exp(|x|/2),
|P_m'(x)|≤[m|x|^(m−1)+(λ_m+1)|x|^m]exp(|x|/2).       (5.4)
```

For `0≤x≤b_m=m/4`, each phase in A_m(±x) has magnitude at most 1/4.
Thus

```text
Re A_m(±x)≥cos(1/4)exp(−x/2).                       (5.5)
```

These bounds remain uniform under arbitrary clustering and multiplicity.
They avoid estimates of individual divided-difference coefficients, which
can be extremely large.

## 6. A lower bound for the norm, including oscillatory cancellation

Define a positive comparison integral

```text
d_m=∫_0^(b_m) x^(2m) W(x)exp(−x)dx.                 (6.1)
```

It is not an unknown best constant for the desired energy inequality. It
is a concrete source moment used only to normalize an explicit construction.

Expanding (5.3), the diagonal terms give, by (5.5),

```text
∫_0^(b_m) W|P_m|²
 ≥ [cos²(1/4)/2]d_m − |I_m|/2,
I_m=∫_0^(b_m) x^(2m)W(x) A_m(x)overline(A_m(−x))
                                      exp(2iλ_m x)dx. (6.2)
```

Let `B_m=x^(2m)W A_m(x)overline(A_m(−x))`. Integration by parts, with
`B_m(0)=0`, and (5.4) yield

```text
|I_m|≤[|B_m(b_m)|+∫_0^(b_m)|B_m'|]/(2λ_m)
     ≤C(m+1)(1+m)^(2m)/λ_m.                         (6.3)
```

To check the last constant, bound the derivative by

```text
2m x^(2m−1)W exp(x)+x^(2m)(|W'|+2W)exp(x).
```

The integrals of the fixed source weights and their suprema are finite by
§2; only the displayed polynomial factors depend on m. For m≥8,
`d_m≥∫_1^2 W exp(−x)dx>0`. Since `λ_m≥exp(m³)`, (6.3) is o(d_m).
Evenness gives `||p_m||_H²=4∫_0^∞W|P_m|²`, so for all sufficiently large m,

```text
||p_m||_H² ≥ d_m/2.                                  (6.4)
```

This explicitly controls destructive interference between the ±λ_m terms.
Using only the pointwise upper bound in (5.4) would not prove (6.4).

## 7. Quantitative separation of the two theta weights

For fixed a≥0 put

```text
u_m(a)=∫_0^∞ x^(2m) κ(x)² c(x)^(−2) exp(ax)dx,
M_m=(log m)/4,   C_0=π exp(4).                        (7.1)
```

**Lemma 4.** For each fixed a≥0 there is C_a<∞ such that, for sufficiently
large m,

```text
u_m(a)/d_m ≤ C_a exp(−sqrt(m)),
1/d_m ≤ C exp(−sqrt(m)).                              (7.2)
```

The starting index may depend on a; no numerical threshold is claimed.

**Proof.** The interval `[M_m+1,M_m+2]` is contained in `[0,b_m]` for large m.
By (2.1), `c(x)≤exp(x/2)`, and `exp(2M_m)=sqrt(m)`,

```text
d_m≥2π² (M_m+1)^(2m) exp(−C_0 sqrt(m)).              (7.3)
```

This proves the second assertion of (7.2), since
`2m log(M_m+1)−C_0 sqrt(m)` grows faster than sqrt(m).

Split the integral defining u_m into `[0,M_m]`, `[M_m,b_m]`, and
`[b_m,∞)`. On the first part it is at most
`C_a M_m^(2m)`, because the fixed weight is integrable. Dividing by (7.3),

```text
u_m,low(a)/d_m
 ≤C_a exp[−2m/(M_m+1)+C_0 sqrt(m)].                 (7.4)
```

Here `log(M/(M+1))≤−1/(M+1)`. The right side is
`O_a(exp(−sqrt(m)))`, because `m/log m` dominates sqrt(m).

On the middle interval the ratio of the numerator weight to the weight in
d_m equals

```text
[κ(x)/c(x)] exp((a+1)x)
 ≤C_a exp[−(π/2)exp(2x)]
 ≤C_a exp[−(π/2)sqrt(m)].                            (7.5)
```

This follows directly from (2.1), absorbing the fixed exponential factor
into half the theta exponent. Thus this part is bounded by (7.5) times d_m.

On the final interval the source weight is at most
`C_a exp(−π exp(2x))`. Uniformly for `x≥m/4` and sufficiently large m,
`2m log x≤(π/2)exp(2x)`; check the left/right ratio at m/4 and use the
decrease of `log x/exp(2x)` thereafter. The remaining integral is at most
`C_a exp(−c exp(m/2))` for a fixed c>0. Divide by the positive lower bound
`∫_1^2 W exp(−x)` for d_m. Together these three estimates prove (7.2). ∎

We will also use

```text
u_(m−1)(1)≤u_m(1)+C,                                (7.6)
```

by splitting at x=1. It follows from (7.2) that any fixed polynomial in m
times `(u_m(a)+u_(m−1)(1)+1)/d_m` tends to zero.

## 8. Energy estimate and real-valued normalization

Let `q_m=κ p_m=κP_m/c` be the physical function. Bounds (5.4), (2.2), and
the derivative of c give

```text
||q_m||_2²≤2u_m(1),
||exp(|x|)q_m||_2²≤2u_m(3),
||q_m'||_2²≤C[(λ_m+1)²u_m(1)+u_m(5)+m²u_(m−1)(1)].  (8.1)
```

Constants are independent of m and of the selected cluster. For example,
`|(κ/c)'|≤C exp(2x)κ/c` for x≥0 explains u_m(5).

The logarithmic, rather than first-derivative, size of the Gamma form is
essential. For Λ≥2 and any u∈H¹(dx), split its shift integral at 1/Λ and 1:

```text
D_Γ(u)≤C[Λ^(−2)||u'||_2²+(1+logΛ)||u||_2²].         (8.2)
```

On `(0,1/Λ)` use `||u−τ_su||≤s||u'||` and `ρ(s)≤C/s`; on `(1/Λ,1)` use
`2||u||`; the remaining ρ tail is integrable. Thus (8.2) does not require
a separate asymptotic assertion about the digamma multiplier.

Choose `Λ=λ_m+2`. We have `logΛ≤m³+C` by (5.1). Equations (7.2), (7.6),
and (8.1) imply

```text
D_Γ(q_m)+||exp(|x|)q_m||_2²
 ≤ C m³ exp(−sqrt(m)) d_m.                           (8.3)
```

The primes are controlled by (2.4), retaining Λ(n)/sqrt(n). In particular,

```text
2 Σ(n≥2) Λ(n)/sqrt(n) |⟨q_m,τ_(log n)q_m⟩|
 ≤ C||exp(|x|)q_m||_2².                              (8.4)
```

No unweighted shifted-source sum is used. Inserting (8.3)–(8.4) into the
exact source identity (2.3) gives

```text
|E(p_m)−||p_m||_H²/2|
 ≤ C m³ exp(−sqrt(m)) d_m.                           (8.5)
```

To obtain real functions, choose r_m to be either Re p_m or Im p_m, with
`||r_m||_H²≥||p_m||_H²/2≥d_m/4`. Each is in `D∩N⊥`. The estimates
(8.1)–(8.4) hold for each part with the same upper bounds. Apply the source
identity to the chosen real part separately; do not infer its signed error
from possible cancellation between the two errors in (8.5). Setting

```text
h_m=r_m/||r_m||_H
```

proves (1.1).

For any fixed T>0, (5.4), (7.3), and the norm lower bound give

```text
||1_[−T,T] h_m||_H²
 ≤ C_T [T/(M_m+1)]^(2m) exp(C_0 sqrt(m)) →0.          (8.6)
```

For sufficiently large m the bracket is less than one, and its negative
logarithmic contribution dominates the final factor. This is an explicit
range-of-application inequality for every fixed T. Norm-one boundedness
and density of compact restrictions in H imply weak convergence to zero.
This completes the proof of Theorem 1.

The same calculation with `T=M_m` gives the useful moving-cutoff estimate

```text
||1_[−M_m,M_m]h_m||_H²
 ≤ C exp[−2m/(M_m+1)+C_0 sqrt(m)],                   (8.7)
```

because `∫_0^∞W(x)exp(x)dx<∞` makes the constant in the numerator
independent of the cutoff. This also tends to zero faster than
`exp(−sqrt(m))` after increasing the starting index.

## 9. Ground-state consequences and what they do not say

ENVELOPE_AUDIT.md proves, for every fixed admissible envelope, that

```text
V∈L∞,   |V(x)|≤C_R exp(−a_R exp(2|x|)) for large |x|,
E(h)−||h||_H²/2=D_R(h)−∫V|h|²dν,  h∈D,             (9.1)
```

where a_R>0. Split the potential integral at `M_m=(log m)/4`. Equations
(8.7) and (9.1) yield, for some fixed a>0,

```text
∫|V||h_m|²dν ≤C_R exp(−a sqrt(m)),
0≤D_R(h_m)≤C_R m³ exp(−a sqrt(m))→0.                 (9.2)
```

Replace a by a smaller positive constant if necessary. The upper bound for
D_R follows from (1.1) and the identity, without choosing a sign for ℓ(h_m).
Equations (1.1), (1.2), and (9.2) prove Corollary 2.

Thus a center observation or a positive uniform gap cannot be obtained merely
by imposing the entire displayed nullspace constraint; the obstruction
persists for actual finite-energy functions satisfying it exactly.
This is stronger in scope than the earlier compact-tail counterexamples
on the full or mean-zero spaces, but is a different construction.

The unresolved critical inequality is still

```text
E(h)≥||h||_H²/2 for all h∈D∩N⊥,
equivalently F(g)≤D(g), g=h/R.
```

No sign of its defect is established by a sequence whose defect tends to
zero. This package does not claim a negative example, a proof of positivity,
`N=ker L`, a global root-mode expansion, or an operator-norm Weyl sequence.
In particular, convergence of form Rayleigh quotients alone has not been
misreported as `||Lh_m||→0` or as a complete essential-spectrum theorem.
