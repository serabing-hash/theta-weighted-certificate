# Source and normalization audit

Date: 17 October 2026 UTC. Repository baseline: `fe7ffbf`.
`RH_PROOF=NOT-OBTAINED`.

This audit reads mathematical definitions and arguments. Historical PASS labels,
saved numerical margins, and archive hashes are not mathematical premises.

## Actual local sources

Paths below are relative to the repository root.

| Source | Exact location | Use and audit boundary |
|---|---|---|
| Original manuscript | `research/2026-10-08-kernel-structure/sources/theta_delta32_certificate.tex`, lines 118–192 | Infinite theta series, probability measure, positive jump energy, compact even core, minimum form closure, operator domains. Read directly. |
| Same manuscript | lines 194–284 | Weak source cancellation and exact signed source transform, including passage to the minimum domain. Read the proof; no numerical inclusion is used. |
| Analytic bridge | `research/2026-10-08-kernel-structure/bridge/PROOF.md`, §§1–5, especially lines 130–212 | Controlling norm, mixed source radical identity, closability, and bounded prime sandwich. Rechecked the estimates used here. |
| Fixed-order kernel proof | `research/2026-10-08-kernel-structure/kernel/PROOF.md`, §§2–5 | Derivative-ratio estimate, compact-difference argument, representing-operator criterion. These supply every fixed order, then the closed span. |
| Provenance ledger | `research/2026-10-08-kernel-structure/SOURCE_IDENTITIES.json` | Identifies preserved manuscript and bridge copies. Used for provenance only. |
| Earlier history | `research/2026-10-08-kernel-structure/sources/history/SERABI_RH_SOURCE_SUBSPACE_AND_SCHUR_2026-09-18.md`, §8 | Prior centered saturation and source transform; no novelty is claimed for these identities. |

No pre-existing local proof of the particular two-shift envelope or the escape
theorem of this package was found. Their proofs are supplied in this package.
No particular parameter pair is numerically certified; only the
parameter-existence argument is used.

## Normalization verdict: agreement

Put `c(x)=cosh(x/2)`. The manuscript uses

```text
κ(x)=exp(x/2) Σ(n≥1) (4z_n²−6z_n) exp(−z_n), z_n=π n² exp(2x),
dν=2κc dx, ν(R)=1,
ρ(s)=exp(−s/2)/(1−exp(−2s)), c_n=Λ(n)/sqrt(n), s_n=log n.
```

The manuscript integrates positive shifts with coefficient ρ(s), and prime
shifts with coefficient c_n. The symmetric measure used here has density
ρ(|s|)/2 and atoms of mass c_n/2 at each ±s_n. Reflection/translation of the
two orientations gives exactly the manuscript's energy, with no extra factor:

```text
E(f)=∫∫ κ(x)κ(z)|f(x)−f(z)|² dμ(x−z) dx.
Af(x)=c(x)^(-1) ∫ κ(z)(f(x)−f(z)) dμ(x−z),
```

where the second formula is used only when the coupled difference is justified.
The symbol μ(h) in the old bridge is a pole functional, not this jump measure.
This notational collision has no mathematical effect but must not be conflated.

`D` is the completion of compact smooth even functions in
`(E(f)+||f||_H²)^(1/2)`. It is not silently replaced by a maximal energy domain.
`A≥0`, `L=A−I/2+P_1/2`, and `D(L)=D(A)` are the conventions used here.

Jacobi inversion gives κ even and positive. The theta Mellin integral gives
`κhat=Ξ`, `∫κ exp(±x/2) dx=1/2`, and hence `ν(R)=1`. In particular the pole
coefficient is exactly 1/2, not a freely adjustable normalization.

## What supports N ⊂ ker L

Write `f_j=κ^(2j)/κ`, including `f_0=1`. The local proof proceeds as follows.

1. Fixed-order theta estimates give `|f_j(x)|≤C_j exp(4j|x|)`, so `f_j∈H`.
2. The physical signed form Q obeys
   `|Q(u,v)|≤C M(u)M(v)`, with
   `M(u)=||u||_(H¹(dx))+||exp(|x|)u||_2`.
   Small shifts use differences; large shifts and primes use
   `|<u,τ_s v>|≤exp(−|s|)||exp(|x|)u||||exp(|x|)v||`.
3. On the compact core, `E(f)=Q(κf)+Var_ν(f)/2`.
   For compact cutoffs `f_(j,R)=χ_R f_j`, both `f_(j,R)→f_j` in H and
   `κf_(j,R)→κ^(2j)` in M. Applying the compact identity to **differences of
   two cutoffs** proves D-Cauchy convergence. Finite maximal energy alone would
   not prove this.
4. The mixed radical identity `Q(κ^(2j),k)=0` for compact even k gives
   `ℓ(f_j,g)=0` first on the core and then on D. The representation theorem
   gives `f_j∈D(L)` and `Lf_j=0`.
5. Integration by parts gives `∫f_j dν=4^(−j)`. The kernel of a closed
   operator is H-closed. Taking the H-closed span of `1` and the centered
   `f_j−4^(−j)` therefore proves the stated inclusion.

Step 4 uses the classical mixed explicit formula in the bridge: the transform
of κ^(2j) is `(-1)^j z^(2j)Ξ(z)`, which vanishes at every nontrivial-zero
argument. The cutoff extension is controlled in M and in the weighted
two-derivative L¹ norm displayed there. This does not use RH. The original
manuscript alternatively derives source cancellation by Mellin inversion and
the divisor identity; its displayed operator-domain treatment starts with
j=0,1. The all-fixed-order completion is the separate kernel proof.

The present package accepts the classical identities named above, rechecks
their normalization and the cutoff/continuity implications, and does not
claim to reprove the entire arithmetic explicit formula. `N=ker L` is never
assumed. The main escape theorem actually uses the **definition** of N and
the j=0 source transform, not completeness of N or the full kernel inclusion.

## Classical analytic sources

- [NIST DLMF, theta transformation 20.7.32](https://dlmf.nist.gov/20.7#E32):
  classical parity input for the theta source.
- [NIST DLMF, zeta zeros](https://dlmf.nist.gov/25.10): unconditional critical
  strip and symmetry. No assumption that zeros lie on the critical line.
- [Hasanalizade–Shen–Wong, Counting zeros of the Riemann zeta function,
  Corollary 1.2](https://arxiv.org/pdf/2107.06506), pp. 1–2: the standard
  consequence `N_ζ(T)=T/(2π) log(T/(2πe))+O(log T)`, counting multiplicities.
  Only this asymptotic is used, not their numerical constants or computations.
  Their ξ normalization omits the factor 1/2; its zero multiset is unchanged.

The proof uses no numerical zero locations and no newly computed source,
FFT, Gram, eigenvalue, or physical integral data.
