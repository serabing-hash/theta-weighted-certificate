# Independent audit of the two-shift envelope and its minimum-domain identity

17 October 2026 UTC. `RH_PROOF=NOT-OBTAINED`.

The notation and half measure are those checked in SOURCE_AUDIT.md.
The source/kernel inclusion is used as proved there, without assuming
`N=ker L`. The main result of this file is a valid identity and its domain
extension, not a new bound proving `F≤D`.

## 1. Safe shifts really lie in the displayed closed span

Let `a_*=(log2)/2`. For real |t|<a_* set

```text
Φ_t(x)=[κ(x+t)+κ(x−t)]/(2κ(x)),
q_t(x)=Φ_t(x)−cosh(t/2).
```

The theta series is holomorphic in `|Im x|<π/4`. On each compact subset of

```text
U={t∈C: |Im t|<π/4,
             exp(−2|Re t|)cos(2 Im t)>1/2},          (1.1)
```

the shifted theta estimates imply an H-integrable dominating function for
Φ_t and its local t derivatives. Indeed at either end the exponent in
`|κ(x±t)|²/κ(x)` is at most

```text
−π[2 exp(−2|Re t|)cos(2 Im t)−1] exp(2|x|),
```

up to a fixed exponential factor. The bracket has a positive lower bound
on a compact subset of U. Thus `t↦q_t` is H-holomorphic there. The region U
is connected and contains the whole real interval (−a_*,a_*).

At zero its even Taylor coefficients are

```text
q_t=Σ(j≥1) t^(2j)/(2j)! [κ^(2j)/κ−4^(−j)].          (1.2)
```

The series is asserted first in a sufficiently small H-analytic disk.
Apply the quotient map `H→H/N`: the image has zero Taylor series, so is
zero near zero and hence throughout U by analytic continuation. Consequently
`q_t∈N` for every safe real t; no unjustified large-radius Taylor summation
is required. Direct change of variables also gives

```text
∫Φ_t dν=cosh(t/2),    ∫q_t dν=0.
```

Since `N⊂ker L`, these vectors are in D(A), and `Aq_t=q_t/2`.

For h∈N⊥, evenness gives the exact continuous family of moments

```text
0=⟨h,Φ_t⟩_H=2∫ overline(h(x))c(x)κ(x−t)dx.          (1.3)
```

These are convergent by Cauchy–Schwarz in H. This does not assert that hc is
tempered or that (1.3) continues to every real t for arbitrary h∈H.

## 2. Existence of an admissible pair, without a numerical certificate

Fix `0<t_1<a_*`, and write `a_i=exp(−2t_i)`. As x→+∞, the leading theta
term gives, for fixed positive safe t,

```text
q_t(x) ∼ (1/2) exp(−9t/2)
               exp[π(1−exp(−2t))exp(2x)].           (2.1)
```

The same holds with |x| at the other end. Hence q_(t_1) is positive in
both tails and has only finitely many real zeros: on the remaining compact
interval it is a nonzero real analytic function.

The condition `2a_2>1+a_1` is equivalent to

```text
0<t_2<t_*:=−(1/2)log((1+a_1)/2)<t_1.                (2.2)
```

For each zero x of q_(t_1), the real analytic function `t↦q_t(x)` is not
identically zero. For example, as real t→+∞ the numerator κ(x±t) tends to
zero and `q_t(x)∼−cosh(t/2)`. Its zeros on the compact interval [0,t_*]
are therefore finite. Avoid their finite union and choose t_2 in (0,t_*).
The two q's have no common real zero. This is an existence proof only;
no particular numerical pair has been tested or certified.

For any positive weights w_1,w_2 define

```text
R=sqrt(w_1 q_(t_1)²+w_2 q_(t_2)²),
Δ=R−sqrt(w_1)q_(t_1),       K=κR.
```

R is positive, smooth and even. It tends to infinity at both ends, so
`inf R>0`. With `d_i=π(1−a_i)>0`, its tail behavior is

```text
R∼sqrt(w_1)q_(t_1),
Δ∼[w_2/(2sqrt(w_1))] q_(t_2)²/q_(t_1).              (2.3)
```

For the second formula use
`Δ=w_2 q_(t_2)²/(R+sqrt(w_1)q_(t_1))` **only in the tails**, where
q_(t_1)>0. This quotient need not have a nonzero denominator everywhere.
Its exponential coefficient is

```text
2d_2−d_1=π(1−2a_2+a_1)<0.
```

Termwise fixed differentiation of the theta series, followed by the
quotient rule in the tails, gives, for each fixed r,

```text
|Δ^(r)(x)|≤C_r exp(C_r|x|)
                   exp[−π(2a_2−1−a_1)exp(2|x|)]     (2.4)
```

outside a fixed compact set. One may enlarge C_r or weaken the positive
coefficient slightly without affecting any argument. To see why the
quotient derivatives are controlled, `q_(t_2)/q_(t_1)→0` with all fixed
logarithmic derivative bounds of polynomial size in exp(2|x|), and
`R=sqrt(w_1)q_(t_1)sqrt(1+(w_2/w_1)(q_(t_2)/q_(t_1))²)` in the tails.
The square root stays uniformly away from its singularities there.
On the compact remainder R>0 gives smoothness. Thus Δ and all its fixed
derivatives decrease faster than every exponential. No global bound for
R' is used or claimed. K and its fixed derivatives also decrease rapidly,
with leading tail exponent `−πa_1 exp(2|x|)`.

Finally,

```text
Δ/R=1−sqrt(w_1)q_(t_1)/R∈[0,2].
```

The mean-zero, nonzero q_(t_1) is negative somewhere, since it is positive
on both tails. At such a point Δ/R>1. Therefore the safe range is exactly

```text
1<γ:=sup(Δ/R)≤2.                                    (2.5)
```

Also `inf_(|x|>T)1/[c(x)R(x)]=0` for every finite T. A positive value
cannot be used in a tail comparison.

## 3. The prime-weighted row bound and AΔ

For any rapidly exponentially decreasing nonnegative continuous J,

```text
Σ(n≥2) Λ(n)/sqrt(n) [J(x+log n)+J(x−log n)]
 ≤C_J cosh(x/2).                                    (3.1)
```

Here it is enough that `J(y)≤C_B exp(−B|y|)` for some B>1/2; J=κ
and J=K both qualify. We give the elementary argument to keep the prime
weights and constants of scale explicit.

Chebyshev's bound `ψ(X)=Σ(n≤X)Λ(n)≤C X` follows from
`ψ(2r)−ψ(r)≤log binom(2r,r)≤2r log2` at integer dyadic r, followed by
dyadic summation and monotonicity. The first inequality follows from the
prime-adic valuation of the binomial coefficient: each prime power in
(r,2r] contributes its log prime. Consequently

```text
Σ_(k≤log n<k+1) Λ(n)/sqrt(n)≤C exp(k/2), k≥0.
```

Multiply by the supremum of J(x±s) on each unit interval. The inequality
`k≤|x|+|x±k|` and the exponential bound on J give a uniformly summable
geometric lattice sum times exp(|x|/2). Since exp(|x|/2)≤2c(x), (3.1)
follows. The assertion is about the weighted sum; its unweighted analogue
has not been substituted.

By (2.4), Δ is bounded, has bounded first derivative, and belongs to D by
the compact-difference admission argument of PROOF.md §2. Define

```text
BΔ(x)=c(x)^(-1)∫ κ(z)[Δ(x)−Δ(z)]dμ(x−z).            (3.2)
```

On |x−z|<1, keep the difference coupled and use
`|Δ(x)−Δ(z)|≤||Δ'||∞|x−z|`, with κ bounded and
`∫_0^1 sρ(s)ds<∞`. The large continuous shifts have finite total mass.
For prime shifts, (3.1) and bounded Δ apply. These give

```text
||BΔ||_∞<∞.                                         (3.3)
```

The small-shift raw convolutions in (3.2) are never separated. Pairing
against a compact smooth even test, symmetrization of the half measure
gives `E(Δ,φ)=⟨BΔ,φ⟩_H`. Absolute convergence follows from the preceding
estimates (or edge Cauchy–Schwarz for the paired differences). Extend this
identity to D by form density. Since BΔ∈H, the representing-operator
criterion proves

```text
Δ∈D(A),    AΔ=BΔ.
```

As q_(t_1)∈D(A), also R∈D(A), with

```text
AR=sqrt(w_1)q_(t_1)/2+AΔ.
```

Thus the actual potential is

```text
V=1/2−AR/R=(Δ/2−AΔ)/R.                              (3.4)
```

It is bounded. Moreover (2.1), (2.3), and (3.3) give, for some a_R>0,

```text
|V(x)|≤C_R exp(−a_R exp(2|x|))                       (3.5)
```

for large |x|. In particular V tends to zero at both ends.

## 4. Ground-state identity on the core and the minimum closure

For compact smooth even h, put g=h/R. The test `|h|²/R` is again compact
smooth even. The exact edge algebra is

```text
|a u−b v|²−(a−b)(a|u|²−b|v|²)=ab|u−v|²,
```

with a=R(x), b=R(z). Multiplying by κ(x)κ(z) and using the actual half
measure gives

```text
E(h)−E(R,|h|²/R)=D_R(h),
D_R(h)=∫∫ K(x)K(z)|h(x)/R(x)−h(z)/R(z)|²dμ(x−z)dx.
```

One can first truncate the shifts. The mixed form converges absolutely by
edge Cauchy–Schwarz, and the positive transformed energy passes by monotone
convergence. Since R∈D(A),

```text
E(h)−||h||_H²/2=D_R(h)−∫V|h|²dν.                   (4.1)
```

For h∈D choose core h_n→h in the form norm. Boundedness of V and (4.1)
applied to differences make `h_n/R` Cauchy for the positive edge energy
with weight K(x)K(z). They also converge in `L²(R²dν)` to h/R. A subsequence
converges at both endpoints almost everywhere for the sigma-finite edge
measure: its restricted endpoint marginals are Lebesgue absolutely
continuous, including each countable atomic shift. The edge-L² limit is
therefore the difference of h/R. This proves convergence in transformed
energy, finiteness of D_R(h), and (4.1) on all of D.

This argument uses the minimum closure directly. It does not assume the
minimum and maximal domains coincide or that arbitrary truncation of a
noncompact function preserves all the nullspace constraints.

On N⊥ the mean vanishes. Writing h=Rg gives exactly

```text
F(g)=∫g²R²Vdν,    D(g)=D_R(Rg),
E(h)−||h||_H²/2=D(g)−F(g)                           (4.2)
```

for real h (use |g|² for complex h). Since N is a closed subspace of ker L,
it reduces L and is contained in D. Decomposing any form vector into its
N and N⊥ parts leaves only the latter part in ℓ. Thus `F≤D` on this
constrained space is equivalent to `L≥0`; the transformation has not made
the missing assertion easier by definition.

## 5. The oriented signed-jump estimate: valid, but insufficient

For real compact smooth h and g=h/R define

```text
J_signed=∫∫κ(x)κ(z)(Δ(z)−Δ(x))
                         (R(x)g(x)²−R(z)g(z)²)dμ dx.
```

Let Ω_+ be the oriented edges with Δ(z)>Δ(x), and put d=Δ(z)−Δ(x).
The integrand is unchanged by swapping endpoints, and zero on equality
edges. Therefore J_signed is twice its integral over Ω_+. For α>0,

```text
R(x)g(x)²−R(z)g(z)²
 ≤(1+α)R(x)(g(x)−g(z))²
   +[(1+1/α)R(x)−R(z)]g(z)².
```

On Ω_+, `d≤Δ(z)≤γR(z)`. The transformed squared difference is symmetric,
so twice its Ω_+ integral is at most its whole integral, even if equality
edges have positive energy. Hence

```text
J_signed ≤ (1+α)γ D(g)+∫g(z)² Wtilde_jump(z)dz,

Wtilde_jump(z)=2κ(z)∫_(Δ(z)>Δ(x)) κ(x)(Δ(z)−Δ(x))
                    [(1+1/α)R(x)−R(z)]_+ dμ(x−z).   (5.1)
```

The final integral is with respect to dz; its displayed density already
contains κ(z). For these compact h, the terms converge: near zero the
Δ difference cancels the Gamma singularity, while far shifts use the
prime-weighted row bound for K. General-domain use requires the same
integrability or a specified limiting interpretation; no unrestricted
nonlinear form pairing is silently asserted.

The coefficient really is `(1+α)γ`, instead of `2(1+α)γ`. But (2.5) gives

```text
1+α < (1+α)γ ≤ 2(1+α),
```

so this estimate alone does not absorb D with a coefficient below one.
Also `F=(1/2)∫ΔR g²dν+J_signed` on the core; the extra terms have not
vanished. Neither a halving of the total constant nor `F≤D` follows.

## 6. Audit verdict

The specified envelope identity and its extension to the **minimum** form
domain are valid on the stated assumptions, with V bounded and vanishing
at infinity. The parameter-existence argument is valid; no particular pair
is certified. The signed-jump improvement is valid on the explicit scope
above, with the factor and measure recorded.

The false tail lower bound, a bounded global R', raw singular convolution
splitting, and an unweighted prime-row sum are not used. The full
orthogonality constraint still requires a proof of the critical signed
comparison. PROOF.md instead supplies a precise obstruction to a uniform
gap or to repairing that gap by any fixed center observation.
