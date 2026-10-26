# Dependencies, arithmetic premises and licenses

## Portable saved-ledger verifier

Python 3.10+ standard library only (`hashlib`, `json`, `struct`, `ast`, `pathlib`, `fractions`). No external runtime files are read. Public payload hashes are integrity identifiers, not trusted digital signatures.

## Historical producer

C++17 compiler; MPFR 4.2.2 at 266-bit precision; GMP; Linux C library and libm; Python 3.12.14; NumPy 2.3.5 / SciPy 1.17.0; single-thread OpenBLAS 0.3.30; threadpoolctl 3.6.0. `HISTORICAL_VERSION_READBACK.json` records the version-file hash readback. Exact historical runtime file identities appear in v4 `RUNTIME_EXPECTED.json` and seven matching snapshots. Their absolute system paths are scientific runtime provenance, not portable installation instructions. The runtime itself is not redistributed, and the hashes do not constitute formal verification of software or hardware.

All quoted local C++ includes resolve inside the evidence tree. System headers/libraries remain external dependencies. Original operational launchers, process receipts and private conversation records are intentionally not distributed. Historical manifests may list them; public `SOURCE_ORIGINS.json` precisely enumerates included sources.

## Third-party notices

`evidence/mpfr_backend/mpfr.h` is the unmodified GNU MPFR 4.2.2 public header. Its SHA-256 is `588c2bd606cba060afb49cd024f9119e996089a341a99d1dc7e0367622335a13`. The full upstream source archive `mpfr-4.2.2.tar.xz` is retained (SHA-256 `b67ba0383ef7e8a8563734e2e889ef5ec3c3b898a01d00fa0a6869ad81c6ce01`) together with the upstream `COPYING` and `COPYING.LESSER` texts. MPFR is distributed under LGPL version 3 or later; see its source notices and included texts for exact terms. Official source: https://www.mpfr.org/mpfr-4.2.2/ . No CC license is applied to these files.

GMP, OpenBLAS, NumPy, SciPy, Python and threadpoolctl binaries/source are not bundled here. Obtain them under their respective upstream licenses; use of these libraries does not replace their notices with this repository's license. The custom `interval.hpp` wrapper is author-owned, not an upstream MPFR file.

Author-owned work retains the repository's existing Creative Commons Attribution-NonCommercial 4.0 International terms: https://creativecommons.org/licenses/by-nc/4.0/ . Existing repository license and third-party exceptions take precedence over a generic metadata label.
