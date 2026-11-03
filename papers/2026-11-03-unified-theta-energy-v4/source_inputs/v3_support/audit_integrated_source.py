#!/usr/bin/env python3
from pathlib import Path
import re,collections,hashlib
here=Path(__file__).resolve().parent
orig=here/'source_inputs/baseline_unified.tex'
new=here/'unified_theta_energy.tex'
standalone=here/'source_inputs/published_growing_bands.tex'
assert hashlib.sha256(orig.read_bytes()).hexdigest()=='7fb34043acebd8837ef435ef27a5ab9545675491bfe2e3a44519405f84d75a14'
assert hashlib.sha256(standalone.read_bytes()).hexdigest()=='bf587b78fb4e603223822b2797291db2551744e43934c1e220c60e41b4f2c20f'
s=new.read_text(); p=standalone.read_text()
expected=p[p.index(r'\section{The form and the main conclusions}'):p.index(r'\begin{thebibliography}')]
labels=re.findall(r'\\label\{([^}]+)\}',expected)
for old in sorted(labels,key=len,reverse=True): expected=expected.replace('{'+old+'}','{gzb:'+old+'}')
expected=expected.replace(r'\subsection{',r'\subsubsection{').replace(r'\section{',r'\subsection{')
expected=expected.replace('The accompanying script checks exact scalar inequalities, the basis','The accompanying growing-band check script checks exact scalar inequalities, the basis')
expected=expected.replace('The editable source, PDF and reproducibility files are intended for\n'+r'\url{https://github.com/serabing-hash/theta-weighted-certificate/tree/main/publications/growing-zero-jet-bands-2026-11-03}.','The standalone source, PDF and reproducibility files are available at\n'+r'\url{https://github.com/serabing-hash/theta-weighted-certificate/tree/main/publications/growing-zero-jet-bands-2026-11-03}.')
assert expected in s, 'Standalone proof changed beyond specified transformations'
labels_all=re.findall(r'\\label\{([^}]+)\}',s); bibs=re.findall(r'\\bibitem(?:\[[^]]*\])?\{([^}]+)\}',s)
assert len(labels_all)==len(set(labels_all)), 'Duplicate labels'
assert len(bibs)==len(set(bibs)), 'Duplicate bibliography keys'
refs=set(re.findall(r'\\(?:eqref|ref|pageref|autoref)\{([^}]+)\}',s)); assert refs<=set(labels_all), refs-set(labels_all)
cites=set(x.strip() for y in re.findall(r'\\cite(?:\[[^]]*\])*\{([^}]+)\}',s) for x in y.split(',')); assert cites<=set(bibs), cites-set(bibs)
print('PASS: input hashes, complete transformed proof, unique labels/bibliography, references and citations')
print(f'Labels: {len(labels_all)}; references: {len(refs)}; bibliography entries: {len(bibs)}; citation keys: {len(cites)}')
