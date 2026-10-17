# Classical sources and proof dependencies

This is a manuscript audit, not a new numerical experiment or a formal proof certificate. The paper's bibliography contains only the four external references below. No prior paper by Jongmin Choi is cited in the manuscript body or bibliography.

## External mathematical inputs

| Input | Precise source | Applicable class and use |
|---|---|---|
| Jacobi imaginary transformation | [NIST DLMF 20.7.32](https://dlmf.nist.gov/20.7#E32) | The real positive theta parameter and its holomorphic continuation in the stated strip. Section 2.1 differentiates the transformed series to prove evenness and the exact Fourier/Mellin normalization. |
| Completed zeta normalization and functional equation | [DLMF 25.4.3–25.4.4](https://dlmf.nist.gov/25.4) | The paper uses `ξ(s) = s(s−1) π^(−s/2) Γ(s/2) ζ(s)/2` and `Ξ(z) = ξ(1/2+iz)`. It derives the source integral and `ν(R)=1`, including the factor `1/2`. |
| Multiplicative explicit formula | [Connes–Consani, arXiv:2006.13771v1](https://arxiv.org/abs/2006.13771v1), Appendix B, equations (147)–(150) | Smooth compact tests on `(0,∞)`. Section 2.2 applies it to `Φ(y)=y^(−1/2) C_u(log y)` for even complex compact smooth `u`, with `C_u` its autocorrelation. The prime coefficient, pole terms, and coupled archimedean finite part are converted explicitly. |
| Digamma integral, reflection, duplication | [DLMF 5.9.16](https://dlmf.nist.gov/5.9#E16), [5.5.4 and 5.5.8](https://dlmf.nist.gov/5.5) | The convergent difference integral `ψ(1/2)−ψ(1/4)=π/2+log 2` fixes `cΓ=log π+γE+π/2+3 log 2`. No two divergent raw convolutions are separated. |
| Unconditional strip and symmetries | [DLMF §25.10](https://dlmf.nist.gov/25.10) | Nontrivial zero arguments have `|Im z|<1/2`; multiplicities and conjugate symmetries are retained. Neither RH nor simplicity is assumed. |
| Zero counting with multiplicities | [Hasanalizade–Shen–Wong, arXiv:2107.06506](https://arxiv.org/abs/2107.06506), Corollary 1.2 | Only `Nζ(T)=T log(T/(2πe))/(2π)+O(log T)` is used. The cited work supplies a stronger explicit bound. Its numeric constants are not used. A multiplicative normalization of `ξ` does not change the zeros. |
| Divided-difference simplex formula | [Carl de Boor, “Divided differences,” Surveys in Approximation Theory 1 (2005), 46–69](https://arxiv.org/abs/math/0502036) | Section 3 states the normalized simplex formula for entire functions and explains extension to complex nodes and repeated nodes. Repeated nodes never exceed zero multiplicity. |

DLMF was checked in version 1.2.8, released 15 September 2026, accessed 17 October 2026. These targeted source checks are not a comprehensive novelty search.

## Paper-internal chain

1. **Exact source and minimum form.** The displayed infinite theta source, probability measure, symmetric half jump measure, core, and minimum closure are the definitions. Section 2 proves closability, theta estimates, and normalization.
2. **Compact source identity.** The compact-test explicit formula is converted to the physical form `Q`. Cutoffs pass it to fixed even theta derivatives. The zero-side source cancellation and the complex edge identity give `Q(κh)=E(h)−Varν(h)/2` on the core.
3. **Minimum-domain identity and admission.** Bounded prime-translation operators and closedness of the Gamma form extend the identity along form-Cauchy core sequences. The admission lemma first uses the compact identity on cutoff differences, so it does not assume maximal-domain equality.
4. **Known source space.** Fixed derivative ratios satisfy the admission criterion. The mixed source cancellation and the representation theorem give `N ⊂ ker L`. No reverse inclusion is supplied or used.
5. **Exact constraints.** Zero modes and derivatives up to one less than each multiplicity annihilate every derivative-ratio generator. Divided differences are finite linear combinations of these exact modes.
6. **Escape.** Zero counting gives clusters; simplex estimates control their divided differences; the theta weight separation controls physical energy after normalization. A real or imaginary part is bounded separately before normalization. This proves the energy and local-mass parts of the main theorem.
7. **Envelope branch.** Hilbert-valued safe shifts belong to `N`; the no-common-zero condition yields a smooth positive envelope. Existence is proved by avoiding finitely many analytic exceptions, with no numerical pair certified. The elementary prime-weighted Chebyshev bound, the coupled Gamma difference, and cutoff admission give a bounded `AΔ` and bounded decaying `V`. The edge identity extends by the minimum form closure. Applying it to the escape sequence gives the transformed-energy conclusion.
8. **Auxiliary scope.** Appendix A proves local density of mode restrictions and compact-support uniqueness only. Appendix B states the oriented jump estimate for real compact smooth tests, with its remainder measure explicit. It is not an extension of that nonlinear pairing to every form vector.

## Conditions deliberately left open

`N = ker L`, the critical inequality `F≤D` (equivalently `L≥0` under the stated reduction), the Riemann hypothesis, global mode completeness in `N⊥`, an operator-norm residual estimate, and an essential-spectrum statement are not obtained. A numerical shift pair and explicit numerical values of asymptotic constants are not certified.

The paper gives an analytic obstruction to specified uniform estimates while imposing every known source constraint. It does not obtain a contradiction to RH or determine from which side the energy approaches `1/2`.

**RH_PROOF=NOT-OBTAINED.**
