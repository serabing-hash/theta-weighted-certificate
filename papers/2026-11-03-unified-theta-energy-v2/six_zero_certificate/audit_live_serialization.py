#!/usr/bin/env python3
"""Recompute sixth rows, test live Arb serialization, and verify rational export.
This supplements rather than replaces analytic tail and integration justification.
"""
from pathlib import Path
import runpy,json,re
from flint import arb,acb,ctx
import flint
p=Path(__file__).resolve().parent
s=runpy.run_path(str(p/'certify_six_zeros.py'),run_name='__main__')
x=json.loads((p/'CERTIFICATE.json').read_text())
producer=[]
for key,var in [('G','G'),('H','H'),('P_head','P'),('Gamma_positive_truncation','Gamma')]:
 for i in range(6):
  for j in range(6):
   assert arb(x[key][i][j]).contains(s[var][i,j]),(key,i,j)
   producer.append([key,i,j,True])
m=runpy.run_path(str(p/'certify_matrix_error.py'),run_name='__main__')
y=json.loads((p/'MATRIX_ENCLOSURE.json').read_text())
secondary=[]
for key,var in [('D2_Gram','D2'),('Gamma_error_matrix_upper','Err'),('sufficient_q0_matrix','Qlower')]:
 for i in range(6):
  for j in range(6):
   assert arb(y[key][i][j]).contains(m[var][i,j]),(key,i,j)
   secondary.append([key,i,j,True])
f=runpy.run_path(str(p/'verify_fixed_split.py'),run_name='__main__')
z=json.loads((p/'FIXED_SPLIT_CERTIFICATE.json').read_text())
ledger=json.loads((p/'RATIONAL_MATRICES.json').read_text())
row=[];exports=[]
ctx.prec=256
for i in range(6):
 for j in range(6):
  assert arb(z['full_row_Gram_majorant'][i][j]).contains(f['row_majorant'][i,j])
  row.append([i,j,True])
for key,A in f['matrices'].items():
 scale=int(ledger[key]['scale'])
 for i in range(6):
  for j in range(6):
   lo,hi=map(int,ledger[key]['entries'][i][j])
   assert arb(lo)/scale<=A[i,j].lower() and arb(hi)/scale>=A[i,j].upper(),(key,i,j)
   exports.append([key,i,j,True])
roots=[]
for i,zr in enumerate(acb.zeta_zeros(1,6)):
 old=arb(re.search(r'(\[.*?\])j',x['zeros'][i]).group(1))
 assert old.contains(zr.imag) and zr.real==arb(1)/2 and zr.zeta().contains(0)
 roots.append({'index':i+1,'root_256_inside_160':True,'residual_contains_zero':True})
out={'status':'PASS','python_flint':flint.__version__,'flint_version':flint.__FLINT_VERSION__,
 'producer_matrices':producer,'derivative_matrices':secondary,'complete_row_majorant':row,
 'four_rational_exports':exports,'root_consistency':roots,
 'scope':'288 saved matrix entries enclose live balls; 144 rational boxes enclose live export matrices. This is not a second quadrature implementation.'}
(p/'LIVE_SERIALIZATION_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS: 288 live serialized entries; 144 rational boxes; six 256-bit root consistency checks.')
