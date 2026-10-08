# Sources and verified formula locations

Retrieved or inspected on 7 October 2026 UTC. The formula notes below are concise mathematical snapshots and original paraphrases. They are not quoted AI answers and are not treated as proof merely because a prior report stated them.

## Primary external mathematical sources

### Alain Connes and Caterina Consani

Weil positivity and Trace formula the archimedean place, arXiv:2006.13771v1.

- Verified URL: https://arxiv.org/html/2006.13771v1
- Appendix A, equations (144)–(146): multiplicative convolution/involution and the Fourier–Mellin change of normalization.
- Appendix B, equations (147)–(150): Mellin explicit formula, positive pole terms, subtracted local terms, prime powers, and the coupled archimedean finite part.
- Equations (152)–(153): negative archimedean distribution has multiplier Re ψ(1/4+it/2)−log π.
- Appendix C, equation (155): a classical positivity criterion with finite Mellin vanishing conditions. It does not establish the specific real-even restriction required here; that restriction is proved in PROOF.md §6.
- Formula-only source snapshot: sources/connes_consani_explicit_formula_snapshot.md. The full HTML was retrieved for verification; its title and relevant equations matched the web rendering. Its retrieval SHA-256 was eb5bd775b433004896086d719bd14b1b81315f2317addb6aee64ac2b40a81436. The full external article is not redistributed in this audit.

Key mathematical data transcribed for the audit:

    Φ̃(s)=∫_0^∞Φ(u)u^(s−1)du,
    Φ^sharp(u)=u^(−1)Φ(u^(−1)),
    Σ_ρΦ̃(ρ)=∫Φ+∫Φ^sharp−Σ_v W_v(Φ),
    W_p(Φ)=log p Σ_{m≥1}[Φ(p^m)+Φ^sharp(p^m)],
    W_R(Φ)=(log 4π+γ)Φ(1)
      +∫_1^∞[Φ(u)+Φ^sharp(u)−2Φ(1)/u]du/(u−u^(−1)).

The audit substitutes Φ(u)=u^(−1/2)C_h(log u) and derives its own normalization calculation from these equations.

### Jeffrey C Lagarias

The Riemann Hypothesis Arithmetic and Geometry, author-hosted PDF.

- Verified URL: https://websites.umich.edu/~lagarias/doc/mt-holyoke-rev.pdf
- PDF pp. 5–6, Theorems 3.1 and 3.2: multiplicative explicit formula and the full Weil positivity criterion.
- Role: cross-check of the classical criterion, not a source for an automatic even-sector restriction.
- Read through the web PDF tool; no local PDF snapshot is claimed.

### NIST Digital Library of Mathematical Functions

- https://dlmf.nist.gov/20.7#E32: theta imaginary transformation. At zero argument and τ=it, this gives θ_3(0|it)=t^(−1/2)θ_3(0|i/t), used to derive the exact parity identity for S and κ.
- https://dlmf.nist.gov/25.4#E3 and https://dlmf.nist.gov/25.4#E4: ξ(s)=ξ(1−s) and ξ(s)=(1/2)s(s−1)Γ(s/2)π^(−s/2)ζ(s).
- https://dlmf.nist.gov/25.10: the nontrivial zeros lie in the open critical strip and have reflection/conjugation symmetry. This page was not used as a numerical zero verification.
- https://dlmf.nist.gov/5.9#E16: ψ(z)+γ=∫_0^∞(e^(−t)−e^(−zt))/(1−e^(−t))dt. Subtract two instances to obtain the convergent digamma difference integral.
- https://dlmf.nist.gov/5.5#E4 and https://dlmf.nist.gov/5.5#E8: digamma reflection and duplication identities. At quarters, ψ(3/4)−ψ(1/4)=π and ψ(1/4)+ψ(3/4)=2ψ(1/2)−2log 2, yielding ψ(1/2)−ψ(1/4)=π/2+log 2.
- https://dlmf.nist.gov/5.11#E9 was checked for fixed-strip gamma decay but is not needed by the final proof: PROOF.md derives rapid strip decrease directly from the theta Fourier integral.

### Elchin Hasanalizade Quanli Shen and Peng Jie Wong

Counting zeros of the Riemann zeta function, arXiv:2107.06506.

- Verified URL: https://arxiv.org/abs/2107.06506
- Abstract states an explicit O(log T+log log T) error around T/(2π) log(T/(2πe)). The audit only uses its standard weaker consequence N(T)=O(T log(2+T)), with multiplicities.
- This suffices for Σ_ρ(1+|z_ρ|)^(−4)<∞ by dyadic summation. No explicit error constant or large-height computation is consumed.

## Supplied and prior local sources

1. Current paper snapshot: sources/theta_delta32_certificate_input.tex.
   Original restored path: /workspace/shared/theta_delta32_release_20261007/theta_delta32_certificate.tex.
   SHA-256: e900409bd91a0125e688c7c03c9935ebca090877e1c8bd0ba7d630647ec6e4ed.
   Read for exact definitions in §§2–3 and scope of the fixed-threshold theorem.

2. Original admission source snapshot: sources/ANALYTIC_ADMISSION_input.md.
   Original restored path: /workspace/shared/theta_delta32_release_20261007/replay/restored_full/ANALYTIC_ADMISSION_EN.md.
   SHA-256: 311cdcba5d36708223a8266b85496ca65ac884934565f247ecd209217a6a7aee.
   Read for operator identity, minimum-domain meaning, and retained premises; numerical claims were not regenerated.

3. /workspace/shared/local_compactness_audit/sources/history/THETA_SOURCE_AUDIT_2026-09-18.md.
   Narrow duplication check: §§6–8 already discuss the cofinal full-space Schur criterion and the theta transform. These statements were not used as authority for the new even-test proof.

4. /workspace/shared/weighted_cost_1305/rh_theta_weighted_observation_audit/sources/inherited/EXTERIOR_COERCIVITY_PROOF.md.
   Narrow duplication check: §§1–4 give conventions, theta normalization, and the even transform while explicitly inheriting radicality. The present audit independently obtains radicality from the explicit formula and controlled approximation.

## Retrieval limits

The Connes–Consani HTML download succeeded and was inspected; only a concise formula snapshot is included. The Lagarias PDF was successfully read through the web tool, but the attempted shell download did not produce a file, so none is listed in the archive. The DLMF TeX-query endpoints failed; the ordinary rendered DLMF pages succeeded and supply the verified formulas above. No failed retrieval is presented as a verified snapshot.
