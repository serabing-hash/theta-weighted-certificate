# Complete response toolkit coverage

## Scope of the integrated appendix

Appendix L, “Complete response certificates and their limiting obligations,” consolidates nine analytical manuscripts into the standalone 207-page monograph `unified_theta_energy.tex`. It uses the centered weighted operator and full form domain established in the main text, except that the physical-null subsection explicitly returns to the ambient operator B and its centered restriction B_c. The appendix proves conditional certification tools; it does not assert a new numerical theta inequality, the global half inequality, or the Riemann hypothesis.

The material is organized by logical dependency rather than by concatenating prior manuscripts. Distinct analytical results and their proofs are retained. Repeated definitions, remainder identities and finite optimization arguments are proved once. Synthetic examples illustrate limitations; older optional numerical substitutions are not substituted for the current evidence. Historical discovery or priority is not claimed.

The tables below identify locations by the exact labels in the standalone TeX source. Exterior equality and deflation results are integrated separately in Appendix M (`ext:sec:exterior`). The source filenames and SHA-256 values at the end identify the inspected inputs; those inputs are provenance records, not external mathematical references or required build dependencies. All proofs needed here are incorporated in the monograph.


## Foundation deduplication

| Repeated material | Existing main proof used | Action |
|---|---|---|
| Theta positivity, normalization, original nonnegative energy | `a:lem:theta`, `a:prop:core` | Shared notation only; not repeated. |
| Complete weak theta source and full bridge/domain | `a:prop:thetanull`, `a:prop:domain`, `eq:actual-unitary`, `eq:Db-physical` | Exact main results retained as dependencies, not downgraded to unsupported assumptions or replaced by citations. |
| Full even compact smooth graph core and H ∩ H1 operator admission | `d:thm:Gamma-graph-core`, `d:lem:Gamma-H1` | Used to prove the new centered compact core and divided-source domain admission. |
| Full-series W envelope and Wsup < 1/2 | `a:lem:explicitW` | Exact equivalent proof already in main; tail subsection references it. |
| Complete weighted prime-power tail r_N | `a:lem:prime`, `a:eq:rN` | Exact formula reused, not claimed new. Ordinary ambient L2 translations are distinguished from even paired shifts. |
| Derivative radicals, independence, actual null rows | `a:lem:radical`, `f:prop:halfeigen` | Not reproved in response-repair subsection. |
| Compact division, origin delta term, centered divided-chain transforms | `d:thm:division`, `d:eq:jump-distribution`, `d:cor:primal` | Reused exactly; actual physical B-domain/row upgrade supplied separately. |
| Full multiplicity jet form/graph cores | `thm:actual-core` | Reused under the full-kernel projection, with changed weighted Gram explicitly retained. |

## Source-by-source mathematical coverage

| Source and result group | Consolidated location | Coverage and proof treatment |
|---|---|---|
| `theta_physical_kernel.tex`: derivative bound for division and actual domain | `rtc:null:division` | New weighted derivative-kernel proof; existing Hilbert–Schmidt division and H1 admission not duplicated. |
| Same: absolute actual operator row and mixed rough/smooth formula | `rtc:null:row` | Full convergence, conjugation, factor-two, density and actual-row proof. |
| Same: normalized divided source, partial divided null rows | `rtc:null:source` | Full normalization/removable value and mixed-test proof; actual domain verified. |
| Same: values-only physical kernel, range closure, multiplicity differences | `rtc:null:kernel`, `rtc:null:multiplicity` | Full graph-core/range/adjoint proof. New V0/Z0 differ from main's full-jet Z. Conditional multiple-zero assertions preserved. |
| Same: real/nonreal sign blocks, orbit orthogonality, normalized witness | `rtc:null:sign`, `rtc:null:rayleigh` | Complete proof. Necessary source-norm condition retained; no actual nonreal zero asserted. |
| Same: full-kernel deflation and projected full-jet cores/Gram | `rtc:null:deflation` and following paragraph | Full form/graph projection proof; form stays M and norm becomes G*. |
| Same: value-wave resolvent core and general-alpha error gate | `rtc:prop:fixed-core` and following application paragraph | General reducing-space proof subsumes value waves; exact matrix C−(alpha−sigma)G and full-residual costs retained. |
| Fixed-shift audit analytic addendum | `rtc:prop:row-free`, `rtc:eq:row-free-single` | Sharp generic residual quadratic coefficient, row-free alternative and absolute error bound proved by scalar functional calculus. No source checker rerun. |
| `resolvent_filter.tex`: kernel filter and graph/form core | `rtc:thm:filter` | Full spectral truncation/preimage/dense-source proof. No inverse bound near kernel assumed. |
| Same: zero-independent centered Hermite sources | Following `rtc:thm:filter` | Direct Gaussian/Fourier completeness argument, unitary weight map and exact centering. No identity source Gram. |
| Same: bounded signed forms and sign equivalence | `rtc:eq:filter-matrices`, `rtc:thm:filter` | Full multiplier/core proof, kernel sector charged sigma norm. |
| Same: two-solve error identity, joint weighted residual gate and relative version | `rtc:prop:filter-error`, `rtc:eq:filter-gate` | Exact e2 relative to computed z retained; full joint row norm and graph bound proved. Relative-margin minimization included. |
| Filter audit row-free addendum | `rtc:eq:row-free-filter` and preceding/following proof | Full bounded error-row norm, alternative Gram gate and relative margin; not claimed uniformly superior. |
| Same: all-prefix cofinal criterion, convergence versus sign, normalized deficit | `rtc:thm:cofinal` item 1; graph/form paragraphs; text after filter | Full eventual-inclusion proof, graph residual convergence, d_m nondecreasing argument and no cubic gain retained. |
| `coupled_residual_half_gap.tex`: exact signed remainder | `rtc:eq:signed-remainder` | Proved once, reused by all two-response variants. |
| Same: sharp sum residual coefficient and three-square identity | `rtc:thm:endpoint`, `rtc:cor:penalties`, `rtc:eq:chi` and following exact decomposition | General endpoint criterion subsumes sharp coupled theorem. Explicit endpoint equality witness and unconditional zero-shift coefficient 2 retained. |
| Same: three full Grams, signed trial matrix, Galerkin/LS distinctions | `rtc:eq:full-grams`, `rtc:eq:full-leakage`, `rtc:eq:two-matrices`; cofinal LS paragraph | Full D=L−HG^-1H retained; first-row rather than Dom A² admission; signed correction cannot be dropped for LS. |
| Same: two-index completeness | `rtc:thm:cofinal` items 2–3 and LS convergence paragraph | Graph-core existence and strict finite-source margin proof unified with optimized certificates. No effective dimension law. |
| `gap_adapted_residuals.tex`: all universal penalties | `rtc:thm:endpoint` | Full necessary and sufficient endpoint proof including r→0 limit; universality only over A≥aI. |
| Same: rank-one sharp family and unequal companion cost | `rtc:cor:penalties`, `rtc:eq:unequal` | D_t>0 and sigma<d explicit. First-cost minimum does not minimize both residual costs. Relative e2 condition retained. |
| Same: general finite Hessian, prior-gap factorization and optimum | `rtc:eq:two-matrices`, `rtc:thm:opt` | Full coefficients and completion-of-square proof; pseudoinverse/range condition retained. |
| Same: stronger-prior same-response gain | Text after `rtc:eq:reduced-hessian` | Exact (2k²−alpha1) times full sum-residual Gram; no sign inferred from gain alone. Older optional decimal/rational illustration not promoted or substituted for current prior. |
| `monotone_cofinal_certificate.tex`: coarse remainder, positive-energy Hessian and reduced Schur | `rtc:eq:coarse-remainder`, `rtc:eq:two-factor`, `rtc:eq:reduced-hessian` | Coarse objective is a parameter specialization of general proof; E and Delta distinguished from D. Strictness not inferred from semidefinite endpoint. |
| Same: exact optimum, monotonicity and positive Schur gain | `rtc:thm:opt`, `rtc:eq:gain` | One full optimization proof replaces duplicate proofs. Compatible common coordinates and PD prerequisites explicit; upper W gives lower inverse gain. |
| Same: shift cost and source extension | `rtc:eq:two-shift` and following Schur paragraph | Fixed-response identity, signed mixed terms and new-shift block prerequisite retained. |
| Same: rational trial, solve loss and entry-error debit | `rtc:eq:two-round` and following text | Full coefficient norm debit and correct inverse directions retained. |
| Same: successive LS can decrease | Exact 5×5 model in cofinal subsection | Full integer Z and both rational values supplied; substitution/cross multiplication proves claim independently of a source checker. |
| `radical_response_repair.tex`: exact unequal loss and best second response | `rtc:prop:null-loss`, `rtc:eq:unequal-loss` | Full square completion; explicit v* and unavoidable first-energy loss. |
| Same: two-response null repair, general penalty Omega | `rtc:eq:null-gain` and following paragraphs | Both responses corrected, actual AP=RP=P, full overlaps only; exact zero-shift formula retained. |
| Same: gain matrices, nested null gain, full G/H/L augmentation, projected matrices | `rtc:eq:null-matrix`, `rtc:eq:null-augmentation` | Complete derivations, exact rank handling and unchanged H−G retained. |
| Same: robust lower gain and null-preserving head | `rtc:eq:null-robust`, `rtc:eq:null-head` | Upper null Gram inverse order, overlap debit and full same-domain sandwich proved. Repaired entries must be independently enclosed. |
| `single_response_leakage.tex`: inverse target and one-response loss | `rtc:eq:inverse-target`, `rtc:thm:single` | R^(1/2) source-image and actual form domain explicit; Dom sqrt(A(A−aI))=Dom A proved. |
| Same: rectangular finite optimum, captured norm, refinement, shift | `rtc:eq:single-finite`, `rtc:eq:single-payment`, `rtc:eq:captured`, `rtc:eq:single-shift` | Independent Hilbert source and graph response columns; singular range condition/pseudoinverse and shift-independent optimizer retained. |
| Same: exact leakage payment | `rtc:prop:payment` | Full inverse-order/congruence proof, epsilon=d−sigma>0, Hermitian polynomial identity; singular endpoint sources not discarded. |
| Same: positive operator can fail finite common-space optimum | Paragraph after `rtc:prop:payment` | Exact diag(1,100), nonorthogonal source data, finite negative optimum and positive true source target retained. |
| Same: null gain, entry debit, tail transfer, cofinal scheme | `rtc:eq:single-null`, `rtc:eq:single-round`, `rtc:prop:varying`, `rtc:thm:cofinal` | Proved once with the shared abstract machinery; no comparison of different transformed source targets. |
| `explicit_source_lower_bounds.tex`: signed-gamma scalar bound | `rtc:thm:scalar`, `rtc:eq:mu` | Complete noncommuting inverse-order proof; scalar monotonicity applies only to single J. gamma>−d and all denominator signs retained. |
| Same: physical conversion and sharpness | `rtc:eq:beta`, proof of `rtc:thm:scalar` | Full R^(1/2)F conversion, including negative mu; exact 2D extremizer, unobserved −d direction, abstract information-class optimality. |
| Same: relative bound preserving zero directions | `rtc:thm:relative` | Complete normalized inequality, inverse order, scalar identity, weighted additive remainder, sigma<d budget and physical conversion. Absolute zeta cannot spend d² twice. |
| Same: cofinal negative parts tending to zero | `rtc:thm:cofinal` item 4 | Full bounded I−R and form-isometry density proof; no one-stage/global inference. |
| `theta_uniform_tail_transfer.tex`: positive Gamma displacement tail | `rtc:tail-gamma` | Full proof using existing exact Wsup bound. |
| Same: centered head, ordered upper operator, domain/core and shift transfer | `rtc:tail-order` | Signed prime tail and both mean projections retained; no finite-dimensional-head claim. |
| Same: all-stage dyadic cutoff schedule | `rtc:tail-schedule` | Exact base/ratio induction and Gamma budget, j≥1 explicitly. |
| Same: compact centered graph core | `rtc:tail-core` | Full graph approximation with fixed compact mean-one bump, not cutoff of noncompact Cg. |
| Same: raw compensated head rows, exact full/exterior Grams | `rtc:tail-raw-row`, `rtc:tail-gram` | Complete actual representative, support radius, negative mean Gram correction, positive rank-one exterior contribution and no double counting. |
| Same: dimension-free full H/L transfer and graph resolvent convergence | `rtc:tail-relative` | Full noncommuting triangle/resolvent proof with 2h<1. |
| Same: varying-operator cofinal certificates | `rtc:prop:varying` | Full fixed-stage graph-core approximation and cross-stage transfer; no response monotonicity across changed operators. |

## Provenance and scope caveats

- The accompanying audit notes were inspected for domain, sign, scope and implementation cautions. Analytical consolidation does not upgrade their historical computational verification status.
- A high-block Schur audit note was available, but its underlying source manuscript was not among the inspected inputs. No unseen formula is reconstructed. Its generic signed finite-block criteria overlap `lat:thm:blocks` and the complete-residual and Schur tools here. The distinction between direct-jet sources and R^(1/2)-transformed sources is retained. The sharper actual-prime ordinary-L2 cosine proof path must not be replaced by a generic bounded-D assumption or by mixing constants from the two paths.
- Synthetic examples establish only their stated logical limitations. The a1024 and a2048 evidence boundaries are recorded separately in the monograph's current dependency and verification map. This analytical coverage map is not a numerical source-replay report.

## Retained restrictions

1. Full residual rows and D=L−HG^-1H, not projected output residuals; Delta=G−HL^-1H is different.
2. Exact centering and the original weighted norm. Mean leakage is not a null direction.
3. sigma<d wherever d−sigma is inverted; D_t>0 for rank-one penalties; gamma>−d for finite inverse formulas.
4. R^(1/2)Ran Phi is not direct Ran Phi or R Ran Phi. All source and response maps remain explicit.
5. Hilbert source density and graph response density serve separate purposes. Cofinal means all stages/eventual inclusion, not finitely many tests.
6. Pseudoinverse range conditions at semidefinite endpoints; PD required for ordinary Schur inverses.
7. Scalar/penalty optimality only over the stated abstract class, never claimed for theta specifically.
8. Source extension, shift reduction, operator change and response refinement are separate comparisons.

## Integration validation

The full 27-proof response-toolkit fragment received a scoped independent mathematical integration review with **72/72 exact and structural checks passing**. The checks cover endpoint interpolation, rank-one positive-energy factorization, scalar-to-physical conversion, relative leakage bounds, the positive-operator example with a failed finite optimum, both exact rational successive least-squares values, domain restrictions, and the complete residual costs. These are algebra and proof-integration checks, not numerical theta evidence, source-enclosure regeneration, formal verification, or a fresh independent audit of every foundational theorem.

The reviewed fragment has 114 distinct `rtc:` labels and occurs byte-for-byte in the final standalone source. Its SHA-256 is `23cc005695e3add4dd6560830053b6ae5a1f34f59ba51e8c36b912723315ad5a`. All references resolve in the integrated manuscript. The full 207-page PDF was compiled and every page was rendered and visually inspected, with no clipping, overlap, missing glyphs, malformed displays, or unresolved references found. See `VALIDATION.md` for the document-wide checks and their scope.

## Inspected source identities


| Source filename | SHA-256 |
|---|---|
| `theta_physical_kernel.tex` | `4550e331625316b8d02de6c65617ec93b5100834ea924d95ff9652b7bc591ad5` |
| `resolvent_filter.tex` | `c4223b8523a0a8c3e32bca2eaa8ce8c6b24067d68cbaf15408595fdd593532f6` |
| `coupled_residual_half_gap.tex` | `cdfdd2f389140a33cd7b962815f700d2026fa68aeffc87eeb0a97437612da25f` |
| `gap_adapted_residuals.tex` | `cb514c1a03b3622cded030e842f8644bcc0a25c9e60e5e96a05a42e5a9fef2aa` |
| `monotone_cofinal_certificate.tex` | `7fa931c0bba65d6cadd52301523b82686e05900e6ab7872b6821e5e6fe20307d` |
| `radical_response_repair.tex` | `a049f1c60303eb3b42813471f55a585cea094b4dcfc6da4bbe772e20f78d10c6` |
| `single_response_leakage.tex` | `59cb7f0867a8bf2b3389fad7c31764c07a4b73f976a283a9569902305ce4743a` |
| `theta_uniform_tail_transfer.tex` | `a420f21605cfc5ab0608b5c1961af8a614eb6a8db959438754a46a823f4cc33e` |
| `explicit_source_lower_bounds.tex` | `d2842d85ced590e395b341b1ebdd75e754a6c03bdb29c882459e5b32a0e12b3a` |
