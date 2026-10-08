# Historical INPUT ACCESS HOLD — 2026-10-08 UTC

**License: CC BY-NC 4.0** — [license terms](https://creativecommons.org/licenses/by-nc/4.0/).

This dated operations record publishes the preserved SERABI RH V2 / j=2 input-access HOLD. It is a historical acquisition record, not an overall project status or a mathematical failure.

## Status of the original run

- Four direct HTTP byte transfers returned HTTP 403, with zero input bytes acquired.
- V2 was not implemented in that run.
- The j=2 pilot was attempted **zero times**.
- No V2 certificate, delta64 proof, or RH proof resulted from that run.

Recovery or continuation is separate from this record. Recovery of the four original mathematical input archives is unconfirmed by the evidence published here. Later recovery, execution, or results must be documented in a separately dated record; this HOLD must not be promoted to the latest computational outcome.

## Preserved artifacts

- [Exact archival ZIP](SERABI_RH_V2_J2_INPUT_ACCESS_HOLD_ARCHIVE_20261008.zip): 22,168 bytes; SHA-256 `07dab24e4578704809fd75e423290de12e12d5f91a87439846e2ffdb3be8264d`.
- [Unchanged expanded package](package/README.md), including the original report, original HOLD ZIP, original delivery record, independent readback audit, and offline verification script.
- [Publication file manifest](PUBLICATION_MANIFEST.sha256): hashes of all other files in this dated directory.

The expanded package is byte-identical to the contents of the archival ZIP. Historical statements in its audit and README that publication had not yet occurred describe the earlier preservation step and are intentionally unchanged. This outer README documents the publication step without rewriting that evidence.

## Verification and limits

The preservation audit records inspection of all 15 leaf text files in the source evidence, with no credential or signed-bearer-URL findings and no redaction required. All 12 original ZIP manifest entries and 11 size-table entries match. ZIP CRC checks and the archived/separate report comparison pass. The wrapper's 7 manifest entries pass. These are performed checks, not a guarantee against every possible secret format.

The supported Google Drive fetch → Sediment materialization route successfully read back the three saved HOLD artifacts. This verifies those artifacts only. It does not demonstrate recovery of the four mathematical inputs.

The original acquisition helper used direct `urllib.request.urlopen` transfers of transient download references after recorded raw-fetch success. This identifies the recorded transfer route; the server-side cause of HTTP 403 remains unknown, and a Drive permission failure has not been established.

For offline verification, run `python3 package/verify_package.py` from this directory. It checks byte integrity without executing the archived acquisition code. On a system with `sha256sum`, also run `sha256sum -c PUBLICATION_MANIFEST.sha256`.

No mathematical computation, acquisition retry, or pilot execution was performed as part of this publication.

## Attribution and license

Preserve the original attribution and source links in the package. Author-created archival reports, records, wrapper, and verification code are licensed under **CC BY-NC 4.0**. Existing third-party rights remain unchanged. No third-party mathematical input archives are included.

Changes in this publication: added this outer README and publication manifest, and published the unchanged preservation package and exact archival ZIP. Repository-level README and release labels are outside this record's scope.
