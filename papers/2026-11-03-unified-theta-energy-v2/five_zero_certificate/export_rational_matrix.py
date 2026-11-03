#!/usr/bin/env python3
"""Convert the already enclosed sufficient matrix to an integer interval ledger."""
from flint import arb,ctx
from pathlib import Path
import json
ctx.prec=256
p=Path(__file__).resolve().parent
data=json.loads((p/'MATRIX_CERTIFICATE.json').read_text())
D=10**18
entries=[]
for row in data['certifying_matrix']:
    entries.append([[str(int((arb(s).lower()*D).floor().fmpz())),
                     str(int((arb(s).upper()*D).ceil().fmpz()))] for s in row])
out={'scale':str(D),'entries':entries,
     'meaning':'Each true sufficient-matrix entry is enclosed by [lower,upper]/scale.',
     'scope':'Finite matrix enclosure exported from the complete ball-arithmetic calculation.'}
(p/'RATIONAL_MATRIX.json').write_text(json.dumps(out,indent=2)+'\n')
print('Exported 25 outward integer entry intervals.')
