# python-flint 0.9.0 provenance check

Result: **OFFICIAL_PYPI_WHEEL_CONTENT_MATCH**. Checked 2026-10-08 UTC.

The copied package payload is byte-for-byte identical to the corresponding official PyPI wheel, apart from fully reconciled installation bookkeeping. The prior absence of original wheel bytes has now been resolved for payload identity. No dependency code was imported, executed or installed, and no phase, Gamma, H, FFT or integral calculation was run. The source runtime tree was not changed.

## Official distribution

- Project/version: python-flint 0.9.0
- Wheel: `python_flint-0.9.0-cp310-abi3-manylinux2014_x86_64.manylinux_2_17_x86_64.whl`
- Size: 10,125,938 bytes
- SHA-256: `376b88cacd30612479e839ffdba887599d3f9c8c0e214852bf80bb2b194e4d76`
- [Authoritative release JSON](https://pypi.org/pypi/python-flint/0.9.0/json), saved as `pypi_python_flint_0.9.0.json`
- [Official wheel download](https://files.pythonhosted.org/packages/db/3f/5f57004f9f43ac6508f874cc97123f11b27b6811b5bb0d320c43f600f0cb/python_flint-0.9.0-cp310-abi3-manylinux2014_x86_64.manylinux_2_17_x86_64.whl), saved here under its original filename
- [PyPI provenance](https://pypi.org/integrity/python-flint/0.9.0/python_flint-0.9.0-cp310-abi3-manylinux2014_x86_64.manylinux_2_17_x86_64.whl/provenance), saved as `pypi_wheel_provenance.json`

The official release JSON and downloaded archive agree on SHA-256 and exact size. The wheel's METADATA also matches PyPI's separately published core-metadata hash. Downloading used reviewed HTTPS curl calls; no denied network route was bypassed.

PyPI's provenance response names GitHub repository `flintlib/python-flint`, workflow `buildwheel.yml`, environment `pypi`. Its decoded attestation subject matches this exact filename and SHA-256. The [release page](https://pypi.org/project/python-flint/0.9.0/) attributes publishing to commit `572c8a213a88c0f92feb1bdb938ce4622f4517fa`; the linked [publishing workflow](https://github.com/flintlib/python-flint/blob/572c8a213a88c0f92feb1bdb938ce4622f4517fa/.github/workflows/buildwheel.yml) was read. This audit relied on official HTTPS metadata and did not independently revalidate Sigstore signatures, certificate chains or transparency-log proofs.

## Exhaustive comparison

Target: `/workspace/shared/phase_gate_audit_20261008/work_artifacts/v2_j2_local_20261008/runtime_deps`

- Official wheel: 113 files, including RECORD; all 112 hashed RECORD entries validated against archive bytes.
- Copied tree: 115 regular files, no symlinks or special files.
- 112 copied files exactly match the wheel: 39 native extensions, 3 bundled libraries, 24 Python sources, 36 typing stubs, 7 license texts, METADATA, WHEEL, and `py.typed`.
- No wheel payload is missing; no unexplained extra file exists.
- Bundled native libraries: FLINT 3.6.0, GMP 6.3.0 and MPFR 4.2.2, as identified by the verified wheel metadata/license paths.
- Every one of the previous 114 manifest entries matches its recorded bytes and SHA-256. The 115th file is RECORD, explicitly outside that earlier hashed-file list.

RECORD differs only as installation bookkeeping: all 113 wheel rows remain semantically unchanged. The installed version adds `INSTALLER` containing `pip\n`, empty `REQUESTED`, and 24 unhashed Python 3.12 bytecode paths. Those bytecode files are absent from the copy; none was executed or relied upon. Row order/newline serialization also differs. The two added metadata files match their installed RECORD hashes.

`file_comparison_manifest.json` records every copied file's hash, size, mode, category and wheel comparison. `record_reconciliation.json` records all RECORD differences. `verify_wheel_data_only.py` reproduces the checks using isolated standard-library Python; it never imports the runtime. `PROVENANCE_RESULT.json` is the machine-readable summary.

## Limits and next use

This establishes identity with the current official PyPI distribution, rather than merely consistency with a copied manifest. It does not reconstruct the original install/download chain or independently prove reproducible builds, absence of defects, mathematical correctness, interpreter authenticity or external system-library provenance. Package authenticity does not itself authorize execution: existing execution holds and workload-specific gates remain in force.

The provenance-only reason to require a fresh install is resolved. A future authorized run can use the currently verified payload after rechecking its manifest. A fresh known-official installation remains an optional cleaner restoration route; see `RESTORATION_AND_LICENSES.md`. Nothing was installed during this audit.

## Acquisition caveats

The separate curl request for the human-facing PyPI HTML page returned a `Client Challenge` document, saved as `pypi_release_page_client_challenge.html`. It is not release evidence and no challenge was solved. The official JSON, wheel and integrity API all downloaded successfully; those are the preserved primary evidence. The human-facing release page was also readable through the web tool. A supplemental FLINT downloads-page lookup returned HTTP 403; it was not retried through an alternate bypass route and was unnecessary for wheel verification.
