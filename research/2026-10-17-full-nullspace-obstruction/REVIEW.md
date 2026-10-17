# Review record and bounded publication claim

17 October 2026 UTC. This record lists analytic checks and their scope.
It is not external peer review or formal proof verification.
`RH_PROOF=NOT-OBTAINED`.

## Proof points checked

| Possible failure | Resolution in the proof |
|---|---|
| Wrong factor from the half measure | Matched to positive shifts in the original manuscript; A has the factor 1/c. |
| Only finitely many moments vanish | Equation (3.2) in PROOF.md holds for every j≥0 and every chosen root mode. Closed span then gives N⊥. |
| Assumed real/simple zeros | Complex nodes remain in the unconditional strip; confluent divided differences use precisely the permitted multiplicities. |
| Local density confused with global completeness | Theorem 3 is explicitly only a restriction theorem. The escape sequence is built directly, not inferred from a global expansion. |
| Huge divided-difference coefficients | The simplex representation gives uniform amplitude and derivative bounds without estimating those coefficients. |
| ±frequency cancellation destroys normalization | Equations (6.2)–(6.4) bound the oscillatory cross term by integration by parts; exp(m³) dominates exp(O(m log m)). |
| A derivative energy bound grows like the frequency squared | The Gamma integral is split at the inverse frequency, giving the logarithmic bound (8.2). Only log λ=O(m³) multiplies the physical mass. |
| Ratio of theta moments treated heuristically | Lemma 4 splits into three explicit intervals and proves an exp(−sqrt(m)) ratio using (7.3). |
| Complex-to-real selection loses the signed estimate | The physical estimates are applied to the selected real or imaginary part separately. No cancellation of signed errors is assumed. |
| Finite maximal energy mistaken for minimum admission | The source identity is applied to differences of compact cutoffs before passing to D. |
| Positive envelope identity used without domain control | Δ∈D(A), AΔ bounded, and R∈D(A) are proved before the core algebra and minimum-closure extension. |
| Raw Gamma convolution or missing prime weights | Coupled differences are retained; both Chebyshev and correlation bounds retain Λ(n)/sqrt(n). |
| Convergence to zero misread as negativity | The sign remains explicitly undetermined. No RH conclusion is drawn. |

The exact polynomial check verifies the complex edge identity and the real
Young completion-of-square identity by vanishing coefficients, not floating
point samples. It has no role in validating the analytic estimates, zero
counting, or domain limits. File hashes likewise establish only identity.

## Publication scope

A suitable bounded subject is **failure of a positive gap and of fixed-center
coercivity after imposing every known theta-source constraint**. The central result is the
exactly constrained, normalized escape sequence with a quantitative energy
error. The local-density lemma provides context; the envelope-domain proof
can serve as a technical appendix. The already known source transform and
compact-support uniqueness candidate should be attributed, not promoted as
new discoveries.

Internal analytic checks do not replace external mathematical review,
especially of the cluster/multiplicity construction, oscillatory lower bound,
and uniform moment separation. Literature priority has not been established.

The published research note makes no claim that the critical nonnegative
comparison follows from this obstruction. The known source-generated space
N is not identified with the full kernel of L.
