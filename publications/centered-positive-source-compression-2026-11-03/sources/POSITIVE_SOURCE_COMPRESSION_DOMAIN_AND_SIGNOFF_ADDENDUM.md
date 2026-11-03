# Positive-source compression: domain qualifications and independent signoff

3 November 2026 UTC. Analytical documentation only. No numerical integration, inverse solve, or sign test was run. This addendum does not alter the frozen source note or the earlier fixed negative-count note.

## 1. Frozen source and exact audit scope

The frozen source is `EXPLICIT_POSITIVE_SOURCE_COMPRESSION_AUDIT.md`, SHA256

    136bebc353c898d74ff3f817836a813022d39e7cfb7cfa4858222d757f75763d.

The independent report `INDEPENDENT_ALL_SCHATTEN_NEGATIVE_COUNT_AUDIT.md`, SHA256

    10ce793e45633b6833c2f9ce0f132f98470f3e4458b9da4ac3a73788e8fd1cb4,

passes the source compression, true-Gram and rank bounds, full-domain negative count, and every-positive-exponent Schatten consequence of source Sections 1–5 and 7–8. It explicitly does not sign off the entire inverse-residual interface in source Section 6. Thus the frozen source's initial provisional status is superseded for the audited compression/count/Schatten statements only.

The abstract regularized positive-compression lemma and shifted error inequality are independently proved in `INDEPENDENT_CORE_AND_POSITIVE_COMPRESSION_REVIEW.md`, SHA256

    f1485b528a7482d3ec6a151a30ea8b30ddcd8e32dfd16c8a02cafad1939e6712.

That earlier review is not a numerical validation of the new source bank, its conditioning, the compact-cosine source evaluation, or an actual inverse margin. No runtime or finite zero-sign certificate follows.

## 2. Explicit parameter and constant conventions

The finite prime-head cutoff N is an integer with N≥1. In the shrinking-threshold application, 0<δ≤1 and

    N=max(8,ceil(log₂(2/δ)))−1≥7.

The source-bank parameters satisfy 0<R<∞, r≥1 integer, m=r−1≥0 integer, and k=2r=2m+2≥2 even. The explicit prescription h=max(1,T/ε), R=(1/2)log log(80h) has R>0 for every ε>0. All displayed logarithms are therefore defined. A rigorous implementation can use upper-enclosed real cutoffs and a larger integer degree rather than decide equality at a ceiling boundary.

All O constants in the δ-asymptotics are independent of δ. For the general target ε=aδ^p they may depend on the fixed a>0 and p>0, together with the fixed, explicitly bounded theta/Gamma constants. No inverse norm, bank-conditioning bound, or unknown sign margin is hidden in these rank constants.

## 3. The operator-domain point in the codimension argument

Semiboundedness gives a finite lower spectral bound ℓ for L_c. Hence the spectral subspace E_δ=Ran 1_(−∞,−δ](L_c) has support in the bounded interval [ℓ,−δ], and every vector in E_δ belongs to Dom L_c, hence to the full form domain.

If dim E_δ>r, choose a nonzero u already in E_δ with V*u=0, using the finite-rank map V*:E_δ→C^r. Then u∈Ran Q and the full form identity applies to that same u. This does not apply Q to an arbitrary form-domain vector and assume that Q preserves the domain. The indicator source columns need only lie in H_c; they need not lie in the form domain or Dom A_N.

For this vector,

    q[u]≥−(tr(QB_NQ)+τ_N)||u||²>−3δ||u||²/4,

which contradicts q[u]≤−δ||u||² on E_δ. Thus the count bound includes the closed threshold without discarding any cross term or imposing source-bank domain membership.

## 4. Meaning of the strengthened conclusion

The audited result is

    dim Ran 1_(−∞,−δ](L_c)≤exp(O(√(1+log(1/δ)))),
    (L_c)_−∈S_p for every p>0, including S_1.

For 0<p<1, S_p is the usual Schatten quasi-class. Finiteness of the negative trace permits nonzero negative eigenvalues and even infinitely many accumulating at zero. It does not prove that the negative trace is zero, nonnegativity, a spectral gap, finite negative index, kernel completeness, or RH.

The source rank bound does not bound the number of inverse trial vectors, the arithmetic precision, true-Gram conditioning, total runtime, or the actual Birman–Schwinger margin. The source projection is not a derivative-radical or low-collar spectral projection.

## 5. Version provenance and unchanged earlier note

No edits to the base have occurred after the freeze at hash 136bebc. The following local snapshots preserve the exact earlier bytes; archived versions are historical, not the active corrected source:

- `EXPLICIT_POSITIVE_SOURCE_COMPRESSION_AUDIT_ARCHIVE_d70c44d3.md`: SHA256 `d70c44d32c3715c5b7ef336cd14bcc89571951acf709758b93c898d370271af4`.
- `EXPLICIT_POSITIVE_SOURCE_COMPRESSION_AUDIT_ARCHIVE_59e03edf.md`: SHA256 `59e03edf520c9b52fb9f2984a3849b76278c4210b809e5a3c4a6ea6c73ee2310`.
- `EXPLICIT_POSITIVE_SOURCE_COMPRESSION_AUDIT_PRE_SIGNOFF_136bebc3.md`: SHA256 `136bebc353c898d74ff3f817836a813022d39e7cfb7cfa4858222d757f75763d`.

The d70c44d3→59e03edf change added the explicit representation F_i=W p_i−κβ_i, with a compact-cosine integral and a computable uniform p_i bound. The 59e03edf→136bebc change corrected one sentence to specify that F*S^(−1)F represents the nonzero spectrum of S^(−1/2)XS^(−1/2), not of X itself. Neither change altered the compression, rank, count, or Schatten arguments.

The earlier fixed file `scalar_first_bracket_20261103/NEGATIVE_SPECTRAL_COUNT_AND_SCHATTEN_AUDIT_20261103.md` remains unchanged at SHA256

    16a0abbf796b1606aff6cf93dcc1954ea098b5cb90b72424e11efae1ee8c86b0.

The stronger all-p conclusion is documented as a new analytic consequence rather than a silent replacement of that earlier note.
