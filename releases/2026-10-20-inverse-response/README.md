# Inverse-response public distribution

The 30-member reproduction archive contains the fixed mathematical package and the 16-page paper. Its ten external numerical inputs are not duplicated: `INPUTS.json` supplies commit-pinned public URLs, sizes, hashes and restoration paths.

- [Reproduction ZIP](inverse_response_reproduction_20261020.zip)
- [Byte counts and SHA256 manifest](RELEASE_MANIFEST.json)
- [SHA256SUMS.txt](SHA256SUMS.txt)
- [PDF at fixed paper commit](https://raw.githubusercontent.com/serabing-hash/theta-weighted-certificate/bcf810f6f5c087f5154eb034971e7f64c9d86129/papers/2026-10-20-inverse-response/shared_error_rank_one_certificates.pdf)
- [Single TeX at fixed paper commit](https://raw.githubusercontent.com/serabing-hash/theta-weighted-certificate/bcf810f6f5c087f5154eb034971e7f64c9d86129/papers/2026-10-20-inverse-response/shared_error_rank_one_certificates.tex)
- [Verification and optional replay instructions](https://github.com/serabing-hash/theta-weighted-certificate/blob/7429e208b0bea64f09102c21d0e97ded76788f86/research/2026-10-20-inverse-response/REPRODUCTION.md)

Download all five named files into one directory to use `sha256sum -c SHA256SUMS.txt`. Verify the archive before using the fixed package's `safe_extract.py`. Byte verification and scientific replay are distinct. The new public adapter was not scientifically executed during publication. `RH_PROOF=NOT-OBTAINED`.
