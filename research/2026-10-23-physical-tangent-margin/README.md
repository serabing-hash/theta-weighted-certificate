# Physical tangent-margin research support

Theta-weighted certificate research project. 23 October 2026.

For the full unscaled theta source W and the explicitly defined physical pole-free form Q_inv, the analytic result is

    Q_inv(-x W(x) sin(gamma x)) > 302/1000000 > 3/10000,
    14 <= gamma <= 29/2.

This directory contains research support, not the separate paper or TeX submission. It is a written analytic proof package, not a numerical experiment or executable verifier.

## Contents

- [PROOF.md](PROOF.md): complete physical definitions, full-source analyticity, selected estimates, exact rational certificates and final inequality.
- [VERIFICATION.md](VERIFICATION.md): analytic-review scope and limitations.
- [REPRODUCTION.md](REPRODUCTION.md): reading order and byte-check instructions.
- [MANIFEST.sha256](MANIFEST.sha256): payload byte identities only.

## Scope

The result concerns this physical evaluation on one explicit family in a fixed band. It does not prove a positive Schur complement, original constrained/root-domain admission, an actual two-root theorem, root simplicity, global operator positivity or RH. There is no positive pole-square gain in the proof. No claim of priority over the literature is made.

The classical theta transformation is cited to the public [NIST DLMF equation 20.7.32](https://dlmf.nist.gov/20.7.E32). All source-specific estimates used here are written in PROOF.md; no private report, account, external dataset or prior numerical package is needed.

## Attribution and license

Author-owned project material follows the repository's existing [CC BY-NC 4.0 license](https://github.com/serabing-hash/theta-weighted-certificate/blob/5c9015383ce2ad1f17fac2ec9bf2829eaac2b250/LICENSE) and [attribution notice](https://github.com/serabing-hash/theta-weighted-certificate/blob/5c9015383ce2ad1f17fac2ec9bf2829eaac2b250/README.md). This package does not relicense third-party material and includes no third-party article or web snapshot. Public availability is not unrestricted-use licensing.
