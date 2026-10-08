# Future restoration and third-party notices

These are instructions only. No installation, dependency import, native execution or public release was performed by this audit.

## Restore the official binary distribution

1. Use a fresh, approved environment compatible with the wheel: ordinary CPython 3.12 on Linux x86-64 is the previously used target. The wheel advertises CPython 3.10 stable ABI and manylinux2014/glibc 2.17 compatibility. Do not substitute a different platform's wheel without a separate matching provenance check.
2. Retrieve the exact wheel from the URL in `official_wheel_metadata.json`, or use the preserved wheel in this folder. Verify its 10,125,938-byte size and SHA-256 `376b88cacd30612479e839ffdba887599d3f9c8c0e214852bf80bb2b194e4d76` before installation. If the bytes differ, stop.
3. Once installation is authorized, use an existing trusted Python/pip and a new empty target directory; do not overwrite the audit source copy. From this audit directory, an offline pinned installation can be prepared with:

   `python -m pip install --no-index --find-links . --require-hashes --no-deps --only-binary=:all: --no-compile --target /approved/new/runtime_deps -r requirements.official.lock`

   `/approved/new/runtime_deps` is a placeholder requiring the selected environment's authorized path. This command has not been run. `--no-compile` avoids generating bytecode during installation; it does not replace the requirement for execution authorization.
4. Compare the restored package payload to the preserved wheel and file manifest before importing it. Fresh INSTALLER, REQUESTED and RECORD files need not reproduce the earlier installation history; no `.pyc` is needed for payload identity. Retain the original wheel RECORD separately and do not represent installation-generated files as publisher-signed files.
5. Record the interpreter, platform and exact package hashes for any later run. Keep phase/workload-specific admission checks separate from dependency provenance.

To rerun this audit's data-only verification of the existing original copy:

`python -I -S verify_wheel_data_only.py`

That script has no network step, performs no installation, does not import `flint`, and does not execute copied source or native modules. Its current target path is explicit at the top of the script. It rewrites only audit results and license copies in its own directory.

## Preserve licenses separately from authored work

Verified wheel METADATA declares `MIT AND LGPL-3.0-or-later`. These dependency files are not covered by any CC BY-NC license assigned to the user's own report, scripts or other authored material. Do not place the runtime, wheel, upstream notices or library source under a blanket author-output license.

All seven upstream license texts were already present, are byte-identical to the official wheel, and are copied without modification into `licenses_from_official_wheel/`:

- `LICENSE`: python-flint's MIT text and copyright notice
- `python-flint.libs/flint-3.6.0/COPYING` and `COPYING.LESSER`: GPLv3/LGPLv3 texts supplied for FLINT
- `python-flint.libs/gmp-6.3.0/COPYING` and `COPYING.LESSERv3`: GPLv3/LGPLv3 texts supplied for GMP
- `python-flint.libs/mpfr-4.2.2/COPYING` and `COPYING.LESSER`: GPLv3/LGPLv3 texts supplied for MPFR

See `license_manifest.json` for the exact wheel-relative paths, sizes and SHA-256 values. Preserve this directory, the original notices and the verified METADATA when retaining binaries. The [GMP copying conditions](https://gmplib.org/manual/Copying) additionally describe GMP's upstream dual-license choice; the wheel's selected aggregate license expression remains the evidence used here.

## Public audit bundle strategy

Prefer distributing authored audit files, hashes and the pinned restoration instructions while letting recipients obtain the official wheel directly from PyPI. This avoids adding an unnecessary binary redistribution step. Clearly exclude external dependencies from the author's CC BY-NC scope and retain attribution for any upstream material that is included.

If a future bundle embeds the wheel or compiled runtime, retaining license texts alone must not be presented as a completed compliance review. Before publication, review the applicable LGPL/GPL terms for corresponding source, relevant build/patch material, notices, and recipients' replacement/relinking rights. Do not imply that this audit's payload-equivalence check fulfills all redistribution duties. Official source starting points include the [pinned python-flint publishing repository](https://github.com/flintlib/python-flint/tree/572c8a213a88c0f92feb1bdb938ce4622f4517fa), [GMP 6.3.0 project/download page](https://gmplib.org/), and [MPFR 4.2.2 release page](https://www.mpfr.org/mpfr-4.2.2/). Source archives and a complete corresponding-source package were not acquired or audited here.
