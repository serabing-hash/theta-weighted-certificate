# Exact scope of counterexamples and unresolved steps

`RH_PROOF=NOT-OBTAINED`.

## Statements disproved under all known source constraints

The sequence in PROOF.md satisfies all constraints, has norm one, belongs to
the minimum D, and obeys `E(h_m)→1/2`, local mass→0, and `D_R(h_m)→0`.
It disproves exactly the uniformly quantified assertions in Corollary 2.
This includes a center observation bound on any fixed energy sublevel
`E(h)≤1/2+ε`, ε>0. It also disproves uniform coercivity of D_R with any
fixed finite center term added.

These are constructive analytic obstructions, not definitions of unknown
optimal constants that merely rephrase `L≥0`. The explicit comparison
integral d_m in the proof normalizes an exhibited sequence and has a proved
theta lower bound. No unknown spectral sign is hidden in it.

## Distinctions that must be preserved

| Claim or construction | What is established | What is not established |
|---|---|---|
| New h_m | Noncompact, real, smooth, even, exactly in D∩N⊥; energy approaches 1/2 | Compact support, exact vanishing on a center interval, or negative signed energy |
| New local-density theorem | Root-mode restrictions are dense on each finite symmetric interval | Global completeness of root modes in N⊥ |
| Compact-support uniqueness | Compactly supported h∈N⊥ must be zero | The same Fourier argument for arbitrary unbounded tails or non-tempered hc |
| Center-mass obstruction | No uniform positive ratio of center norm to total norm, even with energy ≤1/2+ε | Existence of an exactly tail-only nonzero N⊥ function for an unbounded tail |
| Form quotient limit | `E(h_m)−1/2→0` with weakly null h_m | `||Lh_m||→0`, domain D(L) for this whole sequence, or a complete essential-spectrum identification |
| Ground-state limit | D_R(h_m) and F(h_m/R) both tend to zero | Their relative ordering, or any negative example for D−F |

## Older routes and retractions

1. `inf_(|x|>T)1/(c(x)R(x))=0`, not a positive tail constant. This follows
   from the proved tail asymptotic and is not left as a numerical question.
2. A signed tail moment can cancel. Cauchy–Schwarz gives a lower bound for
   center norm in terms of that particular signed moment, not tail norm.
   The new exact-constraint sequence rules out the proposed uniform upgrade.
3. The earlier PNT-based compact-tail U-Relay examples were on the full or
   mean-zero spaces. They are not retroactively labelled N⊥ examples. The
   new N⊥ construction is independent and noncompact; it uses zero counting,
   not a PNT tail estimate.
4. At s=0, raw Gamma convolutions without their difference may diverge.
   Every estimate here retains the difference.
5. Unweighted prime-row sums are not uniformly bounded. The Λ(n)/sqrt(n)
   weights remain in every bound. ENVELOPE_AUDIT.md proves the required
   Chebyshev estimate.
6. R' is not globally bounded. Only compact smoothness of R and the separate
   global decay of Δ and its derivatives are used.
7. The ground-state identity, nullspace projection, and the reduction to
   `F≤D` are identities or equivalences. They are not counted as a new
   positivity estimate.

For contrast, any finite collection of J linear moment constraints admits a
nonzero compact even tail function satisfying them: choose J+1 nonzero even
smooth bumps with disjoint supports outside the prescribed center and take
a nonzero vector in the kernel of their J-by-(J+1) moment matrix. If the mean
is an additional condition, count it as another row and add another bump.
Disjoint supports ensure the resulting function is nonzero; smooth compact
support places it in the core. This finite-dimensional observation does not
extend to all the constraints, as compact-support uniqueness shows.

## The critical problem remains open

No inequality proving

```text
E(h)−||h||²/2≥0,  h∈D∩N⊥,
```

has been obtained. Equivalently, the proof of `F(g)≤D(g)` is still missing.
The oriented-jump coefficient is greater than one, and its extra weight
terms remain. The new escape theorem prevents closing this gap by an
unconditional positive uniform norm margin, even after a fixed center term.
It does not prevent a sharp, noncoercive comparison that controls F by D
at the exact threshold.

Other unproved claims: `N=ker L`; nonnegativity of L; exclusion of all
negative spectrum; RH; a finite certified admissible parameter pair;
quantitative conditioning of a specific finite root cluster; and a certified
finite starting index for the asymptotic theorem.

## Verification limits

The missing critical sign is a mathematical question. This release preserves
analytic proofs and the saved exact polynomial checks; it does not add
numerical zero locations, physical-integral evaluations, FFTs, Gram matrices,
or spectral computations. Internal checking is not external peer review or
formal proof verification. No novelty or priority claim is made.
