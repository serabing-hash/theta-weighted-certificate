# Proof dependency and verification scope

The mathematical proof is in the TeX source. This ledger records its logical dependencies and prevents numerical checks from being mistaken for a proof of RH.

1. The exact weight and complete forms are defined in Section 1. They are not inferred from finite numerical matrices.
2. Lemma 2.1 adapts Zhang's weighted elimination and first-moment concentration method to varying real parts and polynomial prefixes. An elimination removes a selected root prefix by one; its energy identity remains exact for confluent roots.
3. Lemma 3.1 is the classical right-half-plane Takenaka–Malmquist system in Volterra form. Its isometry, orthogonality, endpoint values and negative-real continuation majorant are proved directly. The construction is not claimed as new.
4. Theorem 3.2 combines the energy comparison with the basis evaluation bound. At a=0 and interval length 2 it recovers Zhang Proposition 3.7's constant. General strip and multiplicity claims are established in this manuscript, not imported from the real-frequency theorem.
5. Lemma 4.1 proves full-series theta envelopes cW>9 and C4<42 and a conservative a.e. logarithmic derivative cap 112 exp(2|x|). Only elementary pi and exponential bounds are used.
6. Theorem 4.2 derives a squared pointwise full-ray bound exp(-4 exp(2r)) at exp(2r)>=100N/sqrt(log N), N>=4096. Integration gives the full mass tail and a weighted ordinary-L2 moment. The threshold holds on the entire ray, not just at a sampled endpoint.
7. Lemma 5.1 proves a complete head bound 12 sqrt(X) by a binomial Chebyshev estimate. Theorem 5.2 adds the absolutely convergent entire prime-power tail. No PNT or carrier-phase cancellation is required.
8. Lemma 6.1 derives the local endpoint derivative from the same orthonormal basis. Proposition 6.2 uses adaptive intervals and Fubini, plus the proved theta moment, to obtain an explicit bN=K N^4. This replaces a retained O(N^4 log N) estimate but does not enlarge the claimed width theorem beyond what the smaller prime cap supports.
9. Section 7 proves complete Gamma multiplier bounds and the actual reflected-carrier comparison. The packet tail has prefactor 2. It is retained in the all-prime tail cost, which is 8 sum exp(-2n). The head is charged to the whole packet's norm, so the positive-envelope budget is sufficient without incorrectly halving a generic 2N estimate.
10. Section 8 uses all zeros with multiplicities in a widened-endpoint count. The scalar upper budget is declared before taking arbitrary coefficients. The published HSW explicit theorem has a finite-height numerical verification dependency; the qualitative conclusions only require the classical asymptotic. No zero list is generated here.
11. Theorem 1.1 and Corollary 1.2 follow from the complete prime cap, full Gamma bounds and this common budget. The fixed-boundary proof uses the asymptotic of the declared upper budget, not an unsupported relative zero-count asymptotic.
12. Section 9 uses a positive reference B and exact E=-p-K. Variational Schur minimization retains the actual QVV inverse and all mixed entries. It controls unions already inside a proved complete band, not arbitrary adjacent gluing.

## What the check script establishes

The script verifies exact rational comparisons used for constants, an exact repeated-complex-root Takenaka–Malmquist Gram example, exact endpoint derivatives in that example, and the generic two-by-two determinant polynomial identity. It also illustrates distinct-root basis identities and selected scalar tail majorants using ordinary floating point arithmetic.

The script does not formally verify the analytic lemmas, rigorously compute theta integrals, enumerate zeta zeros, establish an actual finite matrix sign, certify an infinite complement, or prove RH. Those are not conclusions of these checks.

## Review status

The standalone mathematical chain, including its explicit derivative proof and direct repeated-root elimination argument, passed a separate scoped analytical review. Two publication-scope clarifications were incorporated: the Volterra all-pass basis is the classical Takenaka–Malmquist construction, and the published explicit HSW counting theorem has a finite-height numerical zero-verification dependency. The review is not formal verification and makes no global-sign or RH claim. A successful compile and the 61 exact checks remain separate from that mathematical review.
