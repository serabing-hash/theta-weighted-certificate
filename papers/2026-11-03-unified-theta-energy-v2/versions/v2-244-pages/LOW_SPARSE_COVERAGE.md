# Fixed low space to sparse windows coverage

The section “Vanishing coupling from a fixed low space to sparse windows” proves an exact response estimate using the complete packet estimates and sparse-family theorem already proved in the monograph. It retains all prime powers, both prime orientations, the unbounded Gamma multiplier and the actual weighted low Gram. It does not prove the global half inequality or the Riemann hypothesis.

## Mathematical coverage

| Result | Standalone TeX label | Treatment |
|---|---|---|
| Packet derivative, normalized tail, reconstruction and sparse positivity | `sw:prop:analytic`, `sw:thm:sparse` | Existing internal proofs discharge the stated analytical inputs. |
| Full mixed carrier estimate, all prime and Gamma tails | `sw:sec:cross`, `ls:eq:unpaired` | Exact previously proved cross estimate reused, not duplicated or replaced by a finite truncation. |
| Fixed low carrier against one high packet | `ls:lem:mixed` | Full proof and explicit logarithmic cost retained. |
| True weighted low Gram and K_V coordinate cost | `ls:eq:KV`, `ls:eq:coordinate` | Gram inverse retained, with no condition-number normalization. |
| Complete squared coupling sum | `ls:lem:packing` | Full spacing-coordinate packing and exact integral proof. |
| Exact finite Schur response and retained high energy | `ls:thm:main`, `ls:eq:response` | Full proof, exact combined high matrix, independent high-block bases and uniformity in selected window count. |
| Infinite variational response and monotone matrix limit | `ls:prop:infinite` | Actual form-norm closure and continuity, not an asserted bounded inverse on the reciprocal-theta Hilbert space. |
| Exact centering and low positive margin | `ls:eq:mean` and following text | Exact high mean zero is required; low mean remains. No positive low margin is supplied by the response estimate. |
| Many sparse classes needed to cover all high zero windows | `ls:prop:counting` | Full zero-counting proof. Coverage by windows is not identified with closed-span completeness. |
| Numerical source-space mismatch | Final paragraph of Section 12 | Centered sharp-cut cosine sources cannot be directly identified with nonzero global theta exponential-polynomial sources; an analytic identity proof is included. Future approximation or transfer with paid form and Gram errors is not excluded. |

## Restrictions

The low space has a fixed finite even basis. Each basis vector is a finite sum of real carriers in a bounded interval times theta-weighted exponential-polynomial envelopes with offsets in the stated rectangle and a finite prefix budget. This is not an arbitrary finite-dimensional subspace of the full form domain. The cutoff must dominate the low carrier bound, low complexity and derivative scale as stated. The constant K_V need not stay bounded as the low space grows.

High blocks use fixed independent frequency-prefix bases with a total paired logarithmic complexity cap and the specified logarithmic-power separation. Arbitrary adjacent windows are not covered. The infinite extension requires the actual form closure; arbitrary abstract square-summable block coefficients are not admitted automatically. A positive low margin, exact compatibility of low null directions, growing-space controls and all omitted couplings remain separate obligations.

The finite response-gate source Gram, piecewise-linear trial space and optimized response-image spaces do not automatically supply this theorem’s low Gram or positive unshifted low margin. A global comparison strictly below one half is not such a margin, even for a matching space.

## Source identity and scoped checks

Inspected source: `low_sparse_response.tex`, SHA-256 `9f6ac222bf37456ee188fb3f3c6e5859cc744164fb906ae5f3d42fb2eae5952b`. The separate and bundled TeX bytes agree. Source PDFs differ in bytes but have identical extracted layout text; no byte identity between those PDFs is asserted.

All five unique proof environments are retained after declared notation and cross-reference mapping. The 17 supplied exact assertions were replayed successfully with identical output; 13 rational fields and the 17 conclusions were also checked independently. These overlapping finite algebra checks are not numerical source-enclosure generation. A scoped mathematical review of the full integrated fragment, including the source-space mismatch proof, passed. The integrated fragment SHA-256 is `e584623c13ca2b128b0802340b8f61819830ac202b41784ee0afc6a0e5f4a168`.

The complete monograph’s build and every-page visual review are reported in `VALIDATION.md`. No a2048 source replay is certified by these low-to-sparse checks.

This response theorem retains its declared unit-window sparse geometry. The later theorem for sparse families of whole growing bands needs a separate low-to-growing-band mixed estimate before a corresponding attachment can be claimed.
