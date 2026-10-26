# Fixed three-eighths theta-weighted operator certificate

Research artifacts accompanying the English and Korean preprint by **Jongmin Choi**, Independent Researcher, Seoul, Korea ([ORCID](https://orcid.org/0009-0008-7448-514X)). This is a research preprint and computational evidence release, not a claim of external peer review or formal proof-assistant verification.

The authoritative numerical output is **v4**, at fixed R = 1 and epsilon = 1/8, with 276 original positive cells, 552 moment coordinates, and 1104 fine source modes. Its saved total Loewner error is 0.010231573894279825 and its saved positive 551-dimensional restriction margin is 0.02972681684942717. The latter belongs to a diagonally scaled sufficient matrix, not unchanged to the physical operator. The accompanying analytic argument gives the fixed centered spectral lower bound 3/8, conditional on the stated analytic and arithmetic premises.

**RH_PROOF = NOT_OBTAINED.** This release does not establish the global 1/2 threshold, an epsilon-to-zero family, an explicit height-uniform zero-free strip, or superiority over earlier conditional certificates.

## Start here

Run `python3 portable/verify_saved.py` from any directory using Python 3.10 or later. This checks public file identity and exact arithmetic consistency of saved ledgers; it does not regenerate integrals or matrix products. See [REPRODUCE.md](REPRODUCE.md) for its precise boundary and the separately documented producer-regeneration limitations.

- `analysis/ANALYTIC_APPENDIX.md`: self-contained public analytic reconstruction; `analysis/DEPENDENCY_MAP.json` maps claims to proof sections and numerical roles.
- `evidence/`: selected scientific sources and saved numerical evidence, preserving original directory names.
- `SOURCE_ORIGINS.json`: byte-preserved versus scientific-derivative provenance, with original and public SHA-256 hashes.
- `SHA256SUMS`: the authoritative public-payload manifest (not self-hashed).
- `DEPENDENCIES_AND_LICENSES.md`: arithmetic dependencies, historical environment and third-party notices.
- `portable/verify_saved.py`: standard-library-only public saved-ledger verifier.

We invite other researchers to inspect the analytic arguments, run the verification, independently reimplement the arithmetic, and report errors or missing assumptions in [repository issues](https://github.com/serabing-hash/theta-weighted-certificate/issues). Please identify the release commit, file/hash, exact command, environment, expected result and observed discrepancy. A successful identity check is not an independent proof of the producer's output bounds.

The original v1 and v2 runs were inconclusive. v3 produced a positive result with a historical arithmetic qualification. v4 removes the old H-center power-operation dependency by a fresh 58-point safe baseline plus the saved 104-point signed patch. Historical outputs are included only for the dependencies and provenance explicitly described; their status labels do not override v4's scope.

## License and citation

© 2026 Jongmin Choi. Except where otherwise indicated, author-owned text, code and research artifacts retain **CC BY-NC 4.0** under the repository's existing license. MPFR and other third-party components retain their original licenses; see the dependency notice. Use `CITATION.cff` and cite the actual commit used. No DOI or immutable commit identifier is assigned by these local files.
