# Version 3 validation and scope

The public manuscript remains **Version 3 (working integration)**, 256 pages. A scoped independent integration audit cleared the supplied TeX and PDF without required mathematical edits. This is not a new line-by-line audit of the entire preceding monograph, peer review, or formal verification.

- TeX SHA-256: `dd522af5d13acd39c27d3fb4e09e2ece2c1fe5e6000f287a029230af06e37a56`.
- PDF SHA-256: `2f6741cc1677f30b15fa934c5c135b252dbea4fa04fc09ddf0d73e06a5318b38`.
- The supplied source audit verifies both frozen input hashes, preservation of the complete standalone proof under declared heading/label and publication-sentence transformations, 1,269 unique labels, resolved references and citations, and 16 bibliography entries.
- The growing-band checker replays 61 exact scalar/algebraic checks plus separately labelled floating-point illustrations. It does not calculate an actual theta matrix or formally verify the analytic argument.
- Document production uses the supplied no-shell-escape build script. No external research file or network is required to compile the self-contained manuscript.
- The earlier 244-page release, including its full original validation and all 268 files, is preserved byte-for-byte in `versions/v2-244-pages/`. Its claims about all-page review and historical calculations apply to that prior artifact, not automatically to the new 256-page PDF.

The new result concerns a complete actual zero-jet space in one contiguous band, arbitrary coefficients and all multiplicity prefixes, with complete prime-power and Gamma terms. Its norm is ordinary L2. The stated within-band Schur consequence does not establish positivity on arbitrary unions. The global sign and RH remain unproved. The optional explicit zero-counting estimate has a finite-height numerical-verification dependency; the qualitative asymptotic uses the classical counting asymptotic.

Reproduce in a working copy, without Python -O or -OO:

    python3 audit_integrated_source.py
    python3 growing_zero_jet_checks/check_constants_and_identities.py
    sh build.sh

`source_inputs/` contains the exact already-public baseline and standalone TeX inputs needed by the integration audit. No internal review transcripts, private paths, build logs or raw QA files are included in this update. Cryptographic checks establish file identity, not mathematical truth.
