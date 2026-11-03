#!/usr/bin/env python3
"""Assemble a draft without mutating or silently replacing the frozen v3."""
from pathlib import Path
import difflib, hashlib, re
ROOT = Path(__file__).resolve().parent
BASE = ROOT/'source_inputs/unified_theta_energy.tex'
EXPECTED = 'dd522af5d13acd39c27d3fb4e09e2ece2c1fe5e6000f287a029230af06e37a56'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
if sha(BASE) != EXPECTED: raise SystemExit('Frozen v3 TeX digest mismatch')
for line in (ROOT/'source_inputs/SHA256_INPUTS.txt').read_text().splitlines():
    expected, name = line.split('  ',1)
    if sha(ROOT/name) != expected: raise SystemExit('Input mismatch: '+name)
fragments = ['prime_obstruction.tex','low_window.tex','computable_energy.tex','source_compression.tex']
missing = [p for p in fragments if not (ROOT/'appendices'/p).is_file()]
if missing: raise SystemExit('Missing draft appendix: '+', '.join(missing))
base=BASE.read_text(); out=base
old_date=r'\date{November 2026\\Version 3 (working integration)}'
new_date=r'\date{November 2026\\Version 4 (working integration; review pending)}'
if out.count(old_date)!=1: raise SystemExit('Version anchor mismatch')
out=out.replace(old_date,new_date,1)
# Update only the two current-distribution destinations. The frozen v3 is unchanged.
old_release = 'https://github.com/serabing-hash/theta-weighted-certificate/tree/main/papers/2026-11-03-unified-theta-energy-v2'
new_release = 'https://github.com/serabing-hash/theta-weighted-certificate/tree/main/papers/2026-11-03-unified-theta-energy-v4'
old_repro = old_release + '/reproducibility'
new_repro = new_release + '/source_inputs/v3_support/reproducibility'
if out.count(old_repro) != 1 or out.count(old_release) != 2: raise SystemExit('Distribution link anchors mismatch')
out = out.replace(old_repro, new_repro, 1).replace(old_release, new_release, 1)
abstract_add=(r' New appendices analyze finite-prime artifacts, exact known-radical repair, quantitative low-window tail compression, and absolute-error computability of the centered ground energy under the stated inputs. A source-compression proof gives a subpolynomial negative-count bound and all-positive-exponent Schatten membership; these qualitative conclusions were previously obtained by Schubr for the equivalent even realization. None resolves the global sign or the Riemann hypothesis.'+'\n')
anchor=r'\end{abstract}'
if out.count(anchor)!=1: raise SystemExit('Abstract anchor mismatch')
out=out.replace(anchor,abstract_add+anchor,1)
intro_anchor=r'\section{Introduction and logical structure}\label{sec:intro}'
intro_add=r'''

\paragraph{Version 4 additions and scope.}
Appendices~\ref{vfourA:sec:prime-obstruction}--\ref{vfourD:section} collect separately reviewed finite-head obstructions, compact null repair, full-tail low-window approximations, an absolute-error computability construction, and an alternative positive-source proof of spectral decay. The known derivative-radical closure is not identified with the entire physical kernel. Schubr's earlier all-positive-Schatten and subpolynomial-count theorem for the equivalent even realization is explicitly acknowledged in Appendix~\ref{vfourD:prior}. These additions use the stated exact form-realization and arithmetic inputs; their integration does not re-certify historical numerical source enclosures or prove the global sign, exact-zero decision, or Riemann hypothesis.
'''
if out.count(intro_anchor)!=1: raise SystemExit('Introduction anchor mismatch')
out=out.replace(intro_anchor,intro_anchor+intro_add,1)
parts='\n\n% BEGIN VERSION 4 APPENDICES\n'+ '\n\n'.join((ROOT/'appendices'/p).read_text() for p in fragments)+'\n% END VERSION 4 APPENDICES\n\n'
license_anchor=r'\section*{License}'
if out.count(license_anchor)!=1: raise SystemExit('License anchor mismatch')
out=out.replace(license_anchor,parts+license_anchor,1)
bib=r'''
\bibitem{vfourPrimeHead} J. Choi, \emph{Finite Prime Heads and the Known Theta Radical: Infinite Signed Index and Compact Null Repair}, 2026, \url{https://github.com/serabing-hash/theta-weighted-certificate/tree/3d905c59f30da17b54245074cfbd2080e89f35a7/publications/finite-prime-head-obstruction-2026-11-03}.
\bibitem{vfourPositiveRange} J. Choi, \emph{Two Essential Signs of the Prime Tail on Positive Spectral Ranges}, 2026, \url{https://github.com/serabing-hash/theta-weighted-certificate/tree/8718f2380bb8934be2c72ea4a2bf49f0844007ac/publications/positive-range-prime-tail-2026-11-03}.
\bibitem{vfourLowWindow} J. Choi, \emph{Low-Window Prime-Tail Compression and Radical Certificates}, 2026, \url{https://github.com/serabing-hash/theta-weighted-certificate/tree/b3ac3d6f4970e6c08b0f64fdc7e8dc40f65c57aa/publications/low-collar-tail-2026-11-03}.
\bibitem{vfourComputable} J. Choi, \emph{Computable Ground-Energy Brackets with Finite Null Constraints}, 2026, \url{https://github.com/serabing-hash/theta-weighted-certificate/tree/e0e996d7ae4af3cdc96afd2bba68b9dc0b016626/publications/computable-theta-ground-energy-2026-11-03}.
\bibitem{vfourTrace} J. Choi, \emph{A Trace Bound for Negative Theta-Form Spectrum}, 2026, \url{https://github.com/serabing-hash/theta-weighted-certificate/tree/c27148a7423b06a6cb5bc73092a994e5ca2ee3f7/publications/negative-spectrum-trace-bound-2026-11-03}.
\bibitem{vfourSourceCompression} J. Choi, \emph{Positive-Source Compression and All Schatten Classes for a Centered Theta Form}, 2026, \url{https://github.com/serabing-hash/theta-weighted-certificate/tree/c615d9fa93c3348ebeafee1337d10d5c88b69ccd/publications/centered-positive-source-compression-2026-11-03}.
\bibitem{vfourSchubr} S. Schubr, \emph{Joint Cutoffs and Negative-Spectrum Decay for Weighted Weil Operators}, edition 3, 27 October 2026, Theorem 1.1 and Section 2, \url{https://research.luminaryoddities.com/joint-cutoffs-negative-spectrum-decay-weighted-weil-operators/v/3}.
\bibitem{vfourSimon} B. Simon, \emph{Trace Ideals and Their Applications}, 2nd ed., Mathematical Surveys and Monographs 120, American Mathematical Society, 2005, \url{https://doi.org/10.1090/surv/120}.
'''
# Normalize the exact verified source-compression commit, not a shortened or mistyped ID.
bib=bib.replace('c615d9fa93c3348ebeafee1337d10d5c88b69ccd','c615d9fa93c3348ebeafee1337d10d5a8bb69ccd')
bib_anchor=r'\begin{thebibliography}{99}\small'
if out.count(bib_anchor)!=1: raise SystemExit('Bibliography anchor mismatch')
out=out.replace(bib_anchor,bib_anchor+'\n'+bib,1)
# Prove all original v3 bytes survive after reversing the exact named additions.
recovered=out.replace(new_repro,old_repro,1).replace(new_release,old_release,1).replace(new_date,old_date,1).replace(abstract_add,'',1).replace(intro_add,'',1).replace(parts,'',1).replace(bib_anchor+'\n'+bib,bib_anchor,1)
if recovered != base: raise SystemExit('Original v3 reconstruction failed')
(ROOT/'unified_theta_energy.tex').write_text(out)
(ROOT/'integration.diff').write_text(''.join(difflib.unified_diff(base.splitlines(True),out.splitlines(True),fromfile='v3-frozen.tex',tofile='v4-working.tex')))
labels=re.findall(r'\\label\{([^}]+)\}',out); refs=re.findall(r'\\(?:eqref|ref)\{([^}]+)\}',out)
from collections import Counter
badlabels=[x for x,n in Counter(labels).items() if n>1]; missingrefs=sorted(set(refs)-set(labels))
keys=re.findall(r'\\bibitem(?:\[[^]]*\])?\{([^}]+)\}',out)
cites=[]
for c in re.findall(r'\\cite(?:\[[^]]*\])?\{([^}]+)\}',out): cites.extend(k.strip() for k in c.split(','))
missingcites=sorted(set(cites)-set(keys)); dupkeys=[x for x,n in Counter(keys).items() if n>1]
report='v3 reconstruction: PASS\nlabels: %d; duplicate: %s\nreferences missing: %s\nbibliography keys duplicated: %s\ncitations missing: %s\n'%(len(labels),badlabels,missingrefs,dupkeys,missingcites)
(ROOT/'qa').mkdir(exist_ok=True)
(ROOT/'qa/static_report.txt').write_text(report)
print(report)
if badlabels or missingrefs or missingcites or dupkeys: raise SystemExit('Static reference check failed')
