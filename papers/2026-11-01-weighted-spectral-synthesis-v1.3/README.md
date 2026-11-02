# Weighted spectral synthesis and zero-jet cores in a theta Fourier space

**Jongmin Choi**  
Independent Researcher, Seoul, Korea  
ORCID: [0009-0008-7448-514X](https://orcid.org/0009-0008-7448-514X)

Manuscript v1.3, November 1, 2026. Research manuscript, not peer reviewed or accepted.

## Deliverables

- **theta_weighted_spectral_synthesis_v1_3.pdf**: complete 42-page manuscript.
- **theta_weighted_spectral_synthesis_v1_3.tex**: complete editable LaTeX source, proofs, and bibliography.
- **theta_weighted_spectral_synthesis_v1_3_source.zip**: portable source distribution.
- **build.sh**: document-only build script for a complete LaTeX installation.
- **LICENSE.txt**: the existing CC BY-NC 4.0 license notice.
- **CHANGELOG.md**: the v1.3 Gamma-topology extension and preserved scope limits.
- **DOCUMENT_QA.json**: build and all-page visual-review record.
- **PAPER_MANIFEST.json**: version, scope, release files, and artifact hashes.
- **SHA256SUMS.txt**: release-file checksums, excluding the checksum file itself.

The source ZIP contains only the TEX, this README, build.sh, LICENSE.txt, and CHANGELOG.md. It contains no PDF, research code, datasets, private research notes, TeX cache, build intermediates, or rendered pages. Local build/, .texcache/, qa/, and build_local.sh support document production and are not part of the portable source distribution.

## Main theorem: full weighted Hilbert synthesis

The paper works in the even weighted Hilbert space H = L2(R, dx/W), where W = kappa/(2 cosh(x/2)) and kappa is the positive theta kernel. Theta normalization, analytic continuation, tail estimates, and the Fourier-Mellin identification Xi(z) = xi(1/2 + iz) are proved directly.

Let Hc be the subspace with F_u(i/2) = 0. Let N be the H-closed span of the centered even derivatives kappa^(2j) - 4^(-j) kappa, j >= 1. Let I consist of the u in Hc for which F_u/Xi is even and entire, retaining the full multiplicity at every zero of Xi. Then:

- **I = N.** Every admitted fully divisible centered source is approximable in the actual weighted Hilbert norm by finite centered derivative combinations.
- **K = Z**, where K = Hc orthogonal to N and Z is the H-closed span of all zero-jet waves up to the actual multiplicity. The orthogonal complement is relative to Hc, not all of H.
- The centered Abel maps, defined by F_(A_r u)(z) = Xi(z)[Q(r z) - Q(r i/2)] for Q = F_u/Xi, satisfy a **uniform operator bound for 3/4 <= r < 1**.
- **A_r u tends strongly to u in H** for every u in I as r tends to one. Operator-norm convergence to the identity is not asserted.

The full-multiplicity Hilbert synthesis theorem is retained. The present version additionally proves the exact Gamma form and ambient graph closure theorem below. No signed-energy, zero-simplicity, or Riemann-hypothesis conclusion follows.

## New theorem: exact Gamma form and ambient graph zero-jet closure

Define rho(s) = exp(-s/2)/(1-exp(-2s)) for s > 0 and retain the complete form

    t_Gamma[u] = integral_0^infinity rho(s) ||u(.+s)-u||_ordinary_L2^2 ds.

Let X be its finite-energy domain within H, with squared norm ||u||_H^2 + t_Gamma[u], and let T_Gamma be its nonnegative self-adjoint representative in H. For any bounded self-adjoint operator D on H, put B_D = T_Gamma - D on Dom(T_Gamma), and use its ambient graph norm. If J_fin is the algebraic span of every actual full zero jet, then

    closure_X J_fin = X intersect K,
    closure_graph(B_D) J_fin = Dom(T_Gamma) intersect K.

These are precise stronger-topology approximation theorems. The graph statement does **not** assert that K reduces an arbitrary B_D, that the finite jet span is invariant, or that a restriction to K is self-adjoint. The arbitrary bounded perturbation is written in a distinct sans-serif symbol in the manuscript, separate from spatial differentiation and the ordinary Gamma multiplier.

The proof is self-contained in the stated abstraction:

1. The exact Gamma form is proved closed, with compact smooth form core. H intersect ordinary H1 is admitted to the actual weighted operator domain by the closed-form representation criterion.
2. A weighted cutoff commutator proves operator-domain invariance and graph cutoff convergence. A compact graph vector has a globally ordinary-L2 Gamma row, including its noncompact exterior tail. Only then is ordinary mollification used to prove the compact smooth graph core.
3. An arbitrary stronger-topology annihilator of J_fin defines an even tempered distribution and an entire Xi-divisible numerator. The extra derivative factor removes the earlier reciprocal-linear quotient gain, but preserves the closed-lens exponential carrier.
4. The dual Borel contour reconstructs an ordinary smooth H1 source, not an assumed weighted H source. Test-level Fourier inversion identifies it with the distribution, fixing conjugation and transform normalization.
5. Compact testing gives b_R = ell(chi_R v_0) and ||chi_R v_0||_H^2 <= b_R. Its ordinary H1 cost is already uniformly bounded. A quadratic inequality forces actual weighted admission by Fatou, without circular graph or form admission at infinity.
6. Compact smooth density extends the functional identity. Only then is Hilbert synthesis applied after exact centering. The complete annihilator is represented by C kappa plus N; Hahn-Banach gives both closure identities.

No old physical energy bridge, radical-eigenvector identity, physical prime correction, or reduction theorem is imported. X here is defined by the exact displayed Gamma form itself. Stronger-norm finite-jet approximation is proved; stronger-norm Abel convergence, an approximation rate, a bounded-coefficient expansion, and uniform conditioning are not claimed.

## The actual-weight endpoint proof

The crucial argument is included in full, not imported as an external completeness theorem:

1. A fixed exterior Borel contour is used only as a scalar source with ordinary exponential integrability. Fourier uniqueness identifies it with the given actual H source; no exterior H-valued contour admission is assumed.
2. The complete theta series, including its lower-degree term, gives an exact Volterra identity. The actual H weight becomes a Laplace-source tail weight t^(3/2) exp(t).
3. Explicit Volterra recovery first bounds the full theta sum. Identical finite Neumann sums converge in both a crude exponential Banach space and the weighted Hilbert space; matching their limits proves the leading source is weighted-admitted without assuming the conclusion.
4. A positive fractional-power kernel is constructed from finite compound-Poisson measures and gamma convolution. The representation applies to arbitrary complex sources, without positivity of the source or Borel functional.
5. A keyhole resolvent calculation gives the positive pole and cut terms. Integrated potentials yield a uniform weighted row/column estimate, including all small input variables and the no-atom condition at zero.
6. Forward reconstruction and explicit centering give the uniform actual-H Abel bound. Weak compactness then proves I = N; finite-derivative approximation gives strong convergence.

## Supporting results retained

**Exact translation lens.** Within the theta continuation strip, symmetrized translations are admitted exactly in the open lens 2 exp(-2 |Re b|) cos(2 Im b) > 1. Its boundary is excluded, including the purely imaginary interference points. The centered translation span equals N. Entire quotients of strict circular type below (log 2)/2 have absolutely H-convergent derivative series after centering.

**Global quotient growth and carrier.** Every admitted quotient Q = F_u/Xi with u in I satisfies |Q(z)| <= C ||u|| exp(H_L(z))/(1 + |z|), where L is the closed lens and H_L(z) = sup Re(i b z), b in L. The proof includes Jensen-Poisson order control, complex Stirling with its polynomial factor, an explicit sector barrier, and directional Laplace continuation. For P(w) = Q(-i w), L is the smallest common closed convex Borel carrier; individual carriers may be smaller. The Q-variable carrier is rotated to iL.

**Interior Abel structure.** For every 0 < r < 1, A_r is compact and injective, has range closure N = I, and satisfies A_r A_s = A_(rs). The earlier coarse bound C (1-r)^(-5/4) log(e/(1-r)) remains valid but is superseded near the endpoint by the uniform actual-weight estimate. It is not evidence of actual blow-up.

**Sharp boundary family.** For real alpha > 0, integrating centered translations toward any boundary point with weight (1-t)^(alpha-1) gives an H source exactly when alpha > 5/4. In that range the source belongs to N and its Abel means converge strongly. The imaginary-tip interference is treated separately. A centered sinc quotient obeys the same growth shape but has no H inverse; it still demonstrates that carrier growth alone does not ensure admission, not that synthesis fails inside I.

**Compact spectral model.** An explicit Hilbert-Schmidt tail kernel realizes division by w^2-z^2 under the required zero condition. Centered division at i/2 gives a compact dense-range operator with exact generalized nullspaces and nonzero adjoint zero-jet root spaces, with actual multiplicities. Its restriction to I is quasinilpotent; the new theorem proves its generalized nullspace dense and its quotient I/N zero. The abstract compact and semigroup countermodels concern insufficient structural hypotheses, not a residual theta-space defect.

**Inherited-norm obstruction.** In the squared spectral variable, the inherited Fourier norm fails the isometric nonreal zero-flip axiom of a de Branges space, including on the centered subspace. This does not contradict synthesis or exclude every equivalent norm or auxiliary embedding.

## Scope and verification boundary

The manuscript is self-contained at the specialized Hilbert-space level. It does not import an old zero-values-only kernel theorem, an energy-operator eigenspace identification, or a physical form-domain bridge. The new exact Gamma form and ambient graph spaces are constructed directly; they are not identified with an external physical energy realization. The bibliography contains only external sources, not the author's prior papers.

No hypothesis about unknown zero locations is used. The only zero-free-region estimate follows from the absolutely convergent Euler product in Re s >= 3/2; it is not a critical-strip or RH assumption. The theorem keeps full zero multiplicities and does not prove simplicity.

H completeness alone does not prove stronger density; the additional dual-recovery proof establishes it only for the exact Gamma form and ambient perturbed Gamma graph norms specified above. No K reduction for arbitrary D, self-adjoint K restriction, signed half inequality, global half bound, or RH result is claimed. Carrier growth alone still does not guarantee actual H admission for an arbitrary entire quotient.

No numerical research, zero or prime enumeration, numerical spectral calculation, or computational checker was used. Compilation, rendering, metadata inspection, archive validation, and hashing are document-production steps only. Independent analytical audit is not peer review or formal proof-assistant verification.

## Rebuild

Use a complete LaTeX installation with pdflatex and the packages fontenc, lmodern, amsmath, amssymb, amsthm, geometry, microtype, and hyperref.

    sh build.sh

The script runs pdfLaTeX three times with shell escape disabled, writes intermediates to build/, and copies the completed PDF to the release filename. It requires no network, external datasets, BibTeX run, or research computation. The supplied PDF was produced with pdfTeX 1.40.26. Byte-identical rebuilds across different TeX versions and metadata timestamps are not claimed.

## Version preservation and license

This v1.3 distribution is preserved separately. All recorded release-file checksums of v1.0, v1.1, and v1.2 were rechecked successfully; no prior version was overwritten. The older versions remain historical snapshots, not the current theorem statement.

Copyright (c) 2026 Jongmin Choi. The existing **Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)** terms are preserved. See LICENSE.txt and the [license](https://creativecommons.org/licenses/by-nc/4.0/). External references retain their respective rights. No license change, historical-priority claim, peer-review claim, or journal-acceptance claim is made.
