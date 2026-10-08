# Explicit formula source snapshot

Verified 7 October 2026 UTC against Alain Connes and Caterina Consani, arXiv:2006.13771v1, Appendix B.

Source: https://arxiv.org/html/2006.13771v1#A2

Mathematical data used, with the source's equation numbers:

(147) F̃(s)=∫_0^∞F(x)x^(s−1)dx.

(148) Σ_ρF̃(ρ)=∫_0^∞F(x)dx+∫_0^∞F^sharp(x)dx−Σ_v W_v(F), where F^sharp(x)=x^(−1)F(x^(−1)).

(149) W_p(F)=(log p)Σ_{m≥1}[F(p^m)+F^sharp(p^m)].

(150) W_R(F)=(log 4π+γ)F(1)+∫_1^∞[F(x)+F^sharp(x)−2F(1)/x]dx/(x−x^(−1)).

(152)–(153) W_∞(F)=∫_R h_+(t)F̃(1/2+it)dt/(2π), with W_∞=−W_R and h_+(t)=−log π+Re ψ(1/4+it/2).

Audit use: substitute F(x)=x^(−1/2)C_h(log x), retain both pole terms, and convert the coupled archimedean integral to the difference-square form. The transformations and even-sector argument are derived in PROOF.md; they are not assertions that this source already proves the exact weighted bridge.
