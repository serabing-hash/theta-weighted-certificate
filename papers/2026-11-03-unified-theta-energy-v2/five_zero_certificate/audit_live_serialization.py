#!/usr/bin/env python3
"""Replay both five-zero stages and verify all live balls survive serialization.
Supplementary check; not a separate analytic quadrature implementation.
"""
from pathlib import Path
import runpy,json,re
from flint import arb,acb,ctx
import flint
p=Path(__file__).resolve().parent
g=runpy.run_path(str(p/'certify_five_zeros.py'),run_name='__main__')
d=json.loads((p/'CERTIFICATE.json').read_text())
producer=[]
for key,var in [('G','G'),('H','H'),('P_head','P'),('Gamma_positive_truncation','Gamma'),('certifying_matrix','M')]:
    for i in range(5):
        for j in range(5):
            ok=arb(d[key][i][j]).contains(g[var][i,j]);assert ok,(key,i,j)
            producer.append([key,i,j,bool(ok)])
m=runpy.run_path(str(p/'certify_matrix_error.py'),run_name='__main__')
md=json.loads((p/'MATRIX_CERTIFICATE.json').read_text());ctx.prec=256
runpy.run_path(str(p/'export_rational_matrix.py'),run_name='__main__')
runpy.run_path(str(p/'check_rational_matrix.py'),run_name='__main__')
ledger=json.loads((p/'RATIONAL_MATRIX.json').read_text());D=int(ledger['scale']);matrix=[]
for key,var in [('D2_Gram','D2'),('Gamma_error_matrix_upper','Err'),('sufficient_q0_matrix','Qlower'),('certifying_matrix','M')]:
    for i in range(5):
        for j in range(5):
            parsed=arb(md[key][i][j]);live=m[var][i,j]
            assert parsed.contains(live),(key,i,j)
            if key=='certifying_matrix':
                lo,hi=map(int,ledger['entries'][i][j])
                assert arb(lo)/D<=live.lower() and arb(hi)/D>=live.upper()
                assert arb(lo)/D<=parsed.lower() and arb(hi)/D>=parsed.upper()
            matrix.append([key,i,j,True])
roots=[]
for i,z in enumerate(acb.zeta_zeros(1,5)):
    original=arb(re.search(r'(\[.*?\])j',d['zeros'][i]).group(1))
    assert original.contains(z.imag) and z.real==arb(1)/2 and z.zeta().contains(0)
    roots.append({'index':i+1,'root_256_inside_160':True,'zeta_residual_contains_zero':True})
out={'status':'PASS','python_flint':flint.__version__,'flint_version':flint.__FLINT_VERSION__,
     'producer_matrix_checks':producer,'derivative_stage_matrix_checks':matrix,
     'root_consistency':roots,'scope':'Live-ball containment and exact export only; root residuals supplement isolation/counting.'}
(p/'LIVE_SERIALIZATION_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS: all 225 serialized matrix entries enclose live Arb balls; all 25 final rational boxes enclose live and parsed balls.')
