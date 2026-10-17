# Assumptions and dependency ledger

`RH_PROOF=NOT-OBTAINED`.

| ID | Input | Status | Used by |
|---|---|---|---|
| D1 | Actual infinite theta κ, c, ν, half jump measure, and minimum closed form | Matched to original manuscript; see SOURCE_AUDIT.md | All results |
| D2 | Jacobi transformation and theta Mellin identity `κhat=Ξ` | Classical identities; normalization checked | Root modes, analytic shifts, compact uniqueness |
| D3 | Exact compact source identity and its continuity estimates | Local manuscript/bridge arguments checked; classical source cancellation retained | Admission to D and energy estimates |
| D4 | `N⊂ker L` for the displayed derivative family | Fixed-order minimum-domain proof checked; no equality assumption | Shift action and envelope audit |
| D5 | Nontrivial zeros in the strip; Riemann–von Mangoldt counting asymptotic with multiplicity | Classical unconditional input, checked against primary/official sources | Local density and clustered-root escape |
| D6 | Positive weights and two shifts satisfying the stated inequalities, with no common real zero | Existence proved in ENVELOPE_AUDIT.md; no numerical pair certified | Envelope, V, and D_R consequences |
| D7 | Closed-form representation, Fourier uniqueness, identity theorem, Jensen formula | Standard functional/complex analysis; their applications are shown | Domain and density arguments |

The escape construction uses D1–D3, D5, and D7. Its membership in N⊥ is
verified against every generator directly. It does not require D4, D6, RH,
simple zeros, real zero arguments, or a completeness theorem for root modes.

The ground-state consequences additionally use D4 and D6. The bounded
prime row estimate there is proved from an elementary Chebyshev estimate;
no PNT error term is used.

The interpretation that the remaining inequality `E(h)≥||h||²/2` on
`D∩N⊥` is equivalent to nonnegativity of L uses D4 and the reducing
decomposition by N. The further equivalence with RH is the separate existing
bridge. It is contextual, not an input to the new obstruction.

Not assumed: `N=ker L`; `L≥0`; `D=D_max`; uniform positive tail conductance;
a positive center-observation constant; a uniform spectral gap after imposing
all known source constraints; a bounded global derivative of R; unweighted prime-row summability;
that arbitrary `hc` is tempered; or any past numerical PASS label.

All constants in the asymptotic escape theorem are finite, independent of the
sequence index, and justified by the displayed estimates. They are not
numerically calibrated enclosures, and no finite starting index is certified.
The zero heights `exp(m³)` are an analytic existence device, not a request or
claim of a zero computation at those heights.
