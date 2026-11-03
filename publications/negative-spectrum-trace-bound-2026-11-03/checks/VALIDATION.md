# Validation record

- A clean three-pass pdflatex build with shell escape disabled produced a five-page PDF. The log contains no undefined references or overfull boxes. The epstopdf shell-escape warning is harmless because no EPS graphics are used.
- `python3 checks/check_algebra.py` checks the integrated Gamma majorant, a finite weighted-Gram projection identity, and a model equality at the closed spectral threshold. It is not a numerical trace certificate, a proof of the actual operator inputs, or a spectral sign check.
- The trace-count working audit note is included at SHA-256 `16a0abbf796b1606aff6cf93dcc1954ea098b5cb90b72424e11efae1ee8c86b0`. Its separate N=2 numerical statements are not used in this paper; the official-header/ABI verification of that separate numerical work remains unresolved.
- The supplied preceding manuscript TeX and PDF are byte-identical to GitHub commit `91e8742de9b03fd363c1c6b2c25363dc861c4515`: their respective Git blob IDs are `5e6b8b0f1cb424597eefb4d3ef4185df2fbde3e9` and `9eb2041cfb8cc88f3f4961f40a4be8e12611ac74`. The immutable repository link appears in the bibliography.
- The form domain and its closed lower-bounded realization are explicit inputs. Both spectral comparisons use the closed/greater-than-or-equal threshold. The actual weighted Gram is retained, no S1 or RH sign is claimed, and the general trace principle is identified as classical.
- These checks do not constitute an independent mathematical audit of the manuscript. Publication must await the requested separate review; no public upload is included.
