# Historical INPUT ACCESS HOLD record

This archival package preserves the completed SERABI RH V2 / j=2 input-access HOLD from 2026-10-08 UTC. The original run recorded four HTTP 403 byte-transfer failures, V2 unimplemented, and **zero j=2 pilot attempts**. It did not produce a mathematical failure, a V2 certificate, a delta64 proof, or an RH proof.

This is a historical acquisition record. Any subsequent recovery or execution belongs in a separately dated record. Do not present this HOLD as the latest computational outcome after a continuation has run.

## What is preserved

- `evidence/SERABI_RH_V2_J2_HOLD_REPORT_20261008.md`: original report, unchanged.
- `evidence/SERABI_RH_V2_J2_HOLD_20261008_INPUT_403.zip`: original HOLD ZIP, unchanged.
- `evidence/SERABI_RH_V2_J2_DELIVERY_RECORD_20261008.json`: original delivery record, unchanged.
- `ARCHIVE_READBACK_AUDIT.json`: independent readback, integrity, and publication-safety checks.
- `verify_package.py` and `MANIFEST.sha256`: portable packaging verification.

## New readback verification

On 2026-10-08, these three archived artifacts were fetched through the supported Google Drive connector and materialized using the returned Sediment file IDs. All three byte counts match their Drive metadata. The report and ZIP SHA256 values independently match the original delivery record's reported hashes. The delivery record itself has a newly computed hash; no prior self-hash was available for comparison.

The original ZIP contains 13 files. All 12 manifest entries match; the remaining file is the manifest itself. Its CRC check passes. All 11 entries in its size table match. Its `REPORT_KO.md` exactly matches the separately delivered report.

The original delivery record says its own raw readback was blocked and remote integrity was unverified. That historical record remains unchanged. The later successful readback is documented separately here. It verifies the saved HOLD artifacts, not the four original mathematical input ZIPs.

## Transfer-route finding

The saved acquisition helper uses `urllib.request.urlopen` on a transient download reference. The accompanying metadata records successful raw-fetch calls before four direct HTTP transfer failures. It does not use the supported Sediment materialization call. This strongly supports a transfer-route problem worth addressing in a separately authorized continuation; it does not establish the server-side cause of HTTP 403 or a Drive permission failure.

No blocked raw URL, original mathematical input, or pilot was retried during this preservation. No mathematics was executed.

## Publication review

All 15 leaf text files across the original report, delivery record, and recursively inspected ZIP were read. Credential-pattern and signed-URL checks found no credentials, signed bearer URLs, private authentication payloads, or unrelated raw logs. No nested archives were present. Transient connector results and the private download specification are excluded. No redaction was needed, and all originals are byte-identical. These checks are evidence of inspection, not a guarantee against every possible secret format.

Run `python3 verify_package.py` from this directory. It verifies this wrapper's manifest, the original ZIP CRC, and all 12 original manifest entries without executing acquisition code.

## License and provenance

Author-created reports, records, wrapper, and verification code are licensed under **CC BY-NC 4.0**: https://creativecommons.org/licenses/by-nc/4.0/ . Preserve the original attribution, license notice, source links, and indication of changes. Original third-party rights remain unchanged. No third-party source archives are included.

The source Drive IDs, verified URLs, byte counts, and hashes are recorded in `ARCHIVE_READBACK_AUDIT.json`. Drive URLs are provenance references; availability to every public reader is not asserted. The files needed to verify this archival package are included.

Changes: added this archival wrapper and fresh independent readback evidence; changed no original file. Public GitHub publication has not been performed by this preservation step.
