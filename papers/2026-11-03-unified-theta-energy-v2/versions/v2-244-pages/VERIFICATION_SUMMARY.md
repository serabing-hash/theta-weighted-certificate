# Verification scope

This release separates mathematical arguments, finite exact arithmetic,
source-enclosure generation and document production. A pass in one layer does
not silently establish the premises of another. **The global half inequality
and the Riemann hypothesis remain unproved.**

## Corrected numerical source versus historical records

A general outward-enclosure defect was demonstrated in the historical Decimal
integer-power primitive. The corrected a2048 profile replaces it by sign-aware
directed multiplication and has completed all dependent source, T, G, Gamma,
model, K and gate stages. The repair argument, adversarial exact-rational tests,
source identities, full execution and exact signs are recorded in
[GENERATION_VALIDATION.md](source_regeneration_a2048/GENERATION_VALIDATION.md).
This remains the same producer family with reviewed storage/checkpoint adapters,
not a second independent implementation or formal verification of all arithmetic.

The corrected run has 142 explicitly recorded outward scientific endpoint
changes: two G lower bounds, five model-ledger upper bounds and 135 shifted-LDL
endpoints across 68 pivots. Every corrected LDL lower endpoint is positive.
G, K, T, the source scalar, both sufficient matrices and the integer witnesses
retain their exact mathematical values. Corrected whole-file hashes and fresh
reference checks are separate from the preserved historical identities.

The corrected a2048 result does not retroactively repair the distinct historical
a1024 enclosure run. Its saved exact matrix signs remain valid, but historical
same-code source replay does not resolve the known primitive obligation.
The counterexample to the old primitive is not itself evidence of a negative
theta direction or of a failed particular production operand.

## What the computational checks establish

| Evidence | Established scope | Not established by that check |
|---|---|---|
| [Compact exact a1024/a2048 replay](reproducibility/README.md) | Lossless G/K/T/F reconstruction and full integer congruences for the specified saved gates | Theta/source quadrature, tail estimates or physical inclusion from the matrix signs alone |
| [Corrected a2048 production](source_regeneration_a2048/README.md) | Exact frozen candidate, fresh source components and complete dependent production; stronger gate CERT with 256 positive shifted LDL bounds; conservative exact-integer sign status; 59 fresh reference checks | An independent full implementation, automatic a1024 repair, or the global half inequality |
| [Retained a2048 margin](source_regeneration_a2048/corrected/reports/FRESH_RETAINED_MARGIN_REPORT.json) | Fixed beta = 10508819/40000000000 and original integer witness applied to fresh corrected data; 256 positive margins and U < 4060 I | A new candidate search, witness fit or unconditional global coefficient |
| [Four-zero certificate](four_zero_certificate/README.md) | Complete Arb/Acb source replay, exact rational sign check and live-ball serialization review; q0 at least the H-norm squared divided by 32 on the stated four-dimensional space; K4 squared <32 | Positivity on all zeros or identification with a different numerical/Gamma-low space |
| [Five-zero certificate](five_zero_certificate/README.md) | Source replay, exact LDL/determinant checks and live-ball serialization review; q0 at least the H-norm squared divided by 25; shifted coordinate Schur >1/2000; normalized quotient reserve >27/1000; K5 squared <75 | Adding either Schur reserve to 1/25 as an eigenvalue increment, inheriting K4, or automatic sparse/global extension |
| [Six-zero fixed split](six_zero_certificate/README.md) | Fresh sixth-row generation retaining certified five-function blocks; live serialization checks; 144 independent exact interval reconstructions and 24 determinant ratios; conditional raw margin 1/40, projected Schur margin 1/50 and complete-high attachment margin 1/51; sixth coefficient reserve >1/5000 | Closed-sector/form-domain/operator-row admission or inherited enclosure validity from hashes alone, all remaining low directions, uniform all-order bounds or completed exhaustion |
| [Graph-to-Schur transfer](graph_schur_transfer_checks/README.md) | Derivative matrix/ball replay, exact containment and determinant signs, 67 independent rational checks; conditional S_R at least 1/35 on L5=P_R V5 at R=2^18 and q0 at least the H-norm squared divided by 36 on L5 plus the complete complementary high form domain | Sector/operator-row admission itself, other low directions of P_R K, a cofinal family, or a new computation of spectral projection/high inverse |
| [Uniform response checks](uniform_response_checks/README.md) | Exact response constants and bracket identities; 2,103 independent rational checks including noncommuting positive/zero/negative Schur examples; elementary correction/prime-tail audits at 160 and 256 bits; combined cubic-plus-prime operator error <5.37e-18 | Actual theta Schur sign, projected moments, spectral projection/high-inverse computation, spatial integration or matrix-enclosure errors, or completed exhaustion |
| [Gamma-sector examples](gamma_sector_synthetic_checks/README.md) | Three exact synthetic block, collective-coupling and residual/Gram examples | An actual theta spectral-sector sign or a cofinal low-space certificate |
| [Eleven-logarithmic band checks](eleven_log_band_checks/README.md) | 25 exact scalar checks for parameters, margins, row exponents and descriptive threshold intervals | Actual theta-matrix computation, an effective final height or replacement of the separate analytic proof |
| [Other scalar reproduction](reproducibility/README.md) | Listed analytic-composition, sparse-window and fixed-low-space scalar identities | Every operator/domain premise or a missing positive low-space margin |

The fixed retained-margin consequence has exact coefficient
2415896663121887366359985794094352519 / 4835272370827926282795053961934979072,
strictly above the rounded-down 0.499640243163. Its use retains the manuscript's
specified analytic bridge and source-space assumptions. It is strictly below
one half.

The four-zero sparse attachment is separately conditional on its explicit
estimates with C0 = 8 and U = exp(2^512). It does not establish the complete
unit-window claim associated with the separate coarse coefficient 168. The
five-zero space does not automatically inherit those sparse hypotheses.
Likewise, finite positive raw theta-carrier spaces are not automatically the
Gamma-low spectral sector. The graph-to-Schur result supplies a specific transfer
only under its explicit closed-sector and operator-row admission hypotheses.
It uses the complete high residual, not a finite high compression. The projected
five-dimensional space and its six-dimensional extension are not the whole
Gamma-low sector.

## Mathematical and document review

The monograph's coverage maps identify the preserved proofs, hypotheses, spaces,
norms and limits. The conditional graph-to-Schur transfer and its six-zero extension supply
positive bounds on their specific projected five- and six-dimensional low
spaces and complete high attachments. The other low directions and cofinal
Schur signs remain open. The fixed-split exhaustion theorem retains its
unverified nested-space, vanishing-error and projected-density hypotheses. The growing-band results are asymptotic statements, not
unrestricted adjacent assembly or a uniform reciprocal-theta weighted gap.
The uniform-response polynomial retains the complete high operators; finite
polynomial degree is not a finite response-space compression. Its small operator
error constants do not supply an actual theta low sign or a positive endpoint
gap. Projected exhaustion retains the whole exact zero-jet form-core input,
including all required frequency and multiplicity jets. A fixed prime cutoff
M=32 does not make the prime-tail error vanish. The obstruction to a fixed raw
graph debit leaves the established finite five/six-direction certificates intact.

Scoped proof/interface reviews and exact examples are not proof-assistant
formalization of the whole manuscript or an independent reconstruction of every
external theorem.

[VALIDATION.md](VALIDATION.md) records the final document checks, all-page visual
review and isolated standalone build. Those checks concern completeness,
formatting and reproducible document production; they are not a numerical or
mathematical proof by themselves.

The selected mathematical inputs and public code are enumerated in
[PUBLICATION_FILES.txt](PUBLICATION_FILES.txt). [DATA_AVAILABILITY.md](DATA_AVAILABILITY.md)
explicitly identifies what is included and omitted. This integrated paper does
not claim that every historical raw archive, every large production array, or
every previous numerical stage has been restored and republished.

## Reproduce at the appropriate level

Check the release SHA-256 manifest before running commands that rewrite outputs,
and use a working copy. Never disable Python assertions with `-O` or `-OO`.
The compact integer/scalar checks require only the standard library; the
zero-space source producers require their recorded python-flint dependency;
full a2048 generation has separate numerical dependencies and resource costs.

Expected byte equality identifies a particular reference execution. A mismatch
is not automatically a mathematical counterexample. Do not alter expected hashes
to obtain PASS: differing enclosures require their own validated bounds, identity
and exact sign evidence. Cryptographic hashes establish identity, not the truth
of the underlying analytic premises.
