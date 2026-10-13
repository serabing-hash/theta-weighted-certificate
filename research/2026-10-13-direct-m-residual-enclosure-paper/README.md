# Affine residual enclosure: reproducibility deposit

Repository: https://github.com/serabing-hash/theta-weighted-certificate

Directory: `research/2026-10-13-direct-m-residual-enclosure-paper/`

This deposit records a standard operator-order residual enclosure and the
canonical definitions of its finite-interval source application. It makes
no bibliographical priority claim and no Riemann-hypothesis claim.

## Public files

- `source_definitions.json`: the exact operator/basis/reserve definitions
  and mechanically preserved F49 and alpha16 coefficient strings.
- `source_manifest.json`: related scientific input names, byte identities
  and anchors. Historical source files and response archives are not
  redistributed; internal filesystem locations and Library identifiers
  are omitted. The manuscript supplies the required analytic proofs.
- `SOURCE_COPY_RECEIPT.json`: exact source-string preservation and the
  canonical alpha vector hash.
- `AUDIT_CORRECTIONS.md`: the canonical weighted reserve and target correction.
- `EXTERNAL_SOURCES.json`: official bibliographic verification sources.
- `SOURCE_DATA_SHA256SUMS`: the immutable source/data deposit's file hashes.
- `direct_m_residual_enclosure.tex` and
  `output/pdf/direct_m_residual_enclosure.pdf`: the accompanying manuscript
  sources and PDF, published after the source/data deposit.
- `zenodo_pdf_tex.zip`: exactly the PDF and TeX, without supplementary data.
- `SHA256SUMS`: hashes for the final public package.

The manuscript's Data availability section identifies the immutable
source/data revision used for its final compilation. The final manuscript
files are deposited separately in this same directory; its source/data
revision need not contain the manuscript PDF itself.

## Compile from the TeX alone

Copy only the TeX into an otherwise empty directory with a normal TeX Live
installation, then run twice:

```bash
pdflatex -no-shell-escape -halt-on-error -interaction=nonstopmode direct_m_residual_enclosure.tex
pdflatex -no-shell-escape -halt-on-error -interaction=nonstopmode direct_m_residual_enclosure.tex
```

The bibliography is internal. No external image, `.bib`, or coefficient file
is needed to compile. The JSON coefficient data are supplementary definitions.

With Python 3, pypdf and Poppler installed, the document-only helper commands are:

```bash
python3 build_document.py compile
python3 build_document.py render
python3 build_document.py standalone
python3 validate_document.py --source-ref SOURCE_DATA_COMMIT_SHA
```

The last argument is the confirmed source/data commit printed in the paper.
The helper compiles/renders documents, not a research response or Gram target.
Page images under `tmp/` are local review intermediates.

## Static byte and public readback verification

```bash
sha256sum -c SHA256SUMS
python3 verify_public_package.py --manifest SHA256SUMS
python3 verify_public_package.py --manifest SOURCE_DATA_SHA256SUMS --remote-ref SOURCE_DATA_COMMIT_SHA
```

For final-publication readback, use `SHA256SUMS` with the final paper commit.
The script uses anonymous public raw GitHub URLs and compares the exact bytes
with the manifest. It neither creates credentials nor writes to a remote app.
The source/data manifest belongs to its own immutable revision; final records
are additional files, rather than a retroactive change of that source data.

## Mathematical limits

The affine correction must be retained for an inexact x0. Exact Galerkin
orthogonality removes it. At x0=0, the norm-based interval always contains
zero; this does not assert M=0. The radius comparison uses the same full
residual and the same positive lower bound lambda.

The canonical dbar is a piecewise bound on weighted actual rows, not P_B
applied to the supported constant function. The prime coefficients retain
their actual values and both directions, without an additional omega or 2.
The paper reconstructs the analytic bound lambda_b=a+29 omega/14000 for
the auxiliary finite-interval operator. It does not identify it with an
original whole-line realization.

No new research response/Gamma/prime/Gram evaluation was performed for this
deposit. In the inspected scientific input scope, no certified m, Gx0, full
residual norm, or matching C,D,Nm,Nr supplier was found. Other Grams, scalar
H, chi, projected residual norms, and the numerical result affected by
transcribed beta endpoints are not substitutes. An actual signed numerical
M enclosure remains unevaluated.
