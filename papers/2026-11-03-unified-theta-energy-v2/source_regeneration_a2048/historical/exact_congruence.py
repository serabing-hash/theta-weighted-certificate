"""Independent integer sign certificate for a completed replay gate only."""
from pathlib import Path
from fractions import Fraction as Q
from hashlib import sha256
import argparse,json,math,time
import numpy as np
from scipy.linalg import cholesky,solve_triangular
A=Path(__file__).resolve().parent

def run(path,gap):
 start=time.time();path=Path(path);g=json.loads(path.read_text());d=int(g['common_denominator'])
 n=len(g['matrix_numerators']);assert n==256
 D=math.lcm(d,gap.denominator)
 M=np.array([[int(v)*(D//d)-(gap.numerator*(D//gap.denominator) if i==j else 0)
              for j,v in enumerate(row)] for i,row in enumerate(g['matrix_numerators'])],dtype=object)
 assert np.array_equal(M,M.T)
 # Floating construction only proposes an integer witness, never supplies proof.
 mid=np.array([[float(Q(int(v),D)) for v in row] for row in M])
 L=cholesky(mid,lower=True)
 proposal=solve_triangular(L.T,np.eye(n),lower=False)
 Qint=np.array([[int(round(float(v)*(1<<44))) for v in row] for row in proposal],dtype=object)
 H=Qint.T@(M@Qint)
 assert np.array_equal(H,H.T)
 margins=[int(H[i,i])-sum(abs(int(H[i,j])) for j in range(n) if i!=j) for i in range(n)]
 assert min(margins)>0
 record={'status':'EXACT_INTEGER_POSITIVE_DEFINITE','gate_sha256':sha256(path.read_bytes()).hexdigest(),
  'gap':str(gap),'matrix_denominator':str(D),'witness_integer_rows':[[str(v) for v in row] for row in Qint],
  'strict_diagonal_dominance_margin_numerators':[str(v) for v in margins],
  'proof':'Q^T(M-gap I)Q has exact positive strict diagonal dominance. Hence it is positive definite, Q is nonsingular, and M-gap I is positive definite.',
  'witness_construction':'binary64 Cholesky proposes integers only; every sign premise is rechecked by exact integer arithmetic',
  'elapsed_seconds':time.time()-start}
 (A/'independent_congruence_certificate.json').write_text(json.dumps(record,indent=2)+'\n')
 print('PASS: all 256 exact integer diagonal dominance margins positive; shifted gate positive definite.')
 print('Gate SHA256:',record['gate_sha256'])
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--gate',required=True);parser.add_argument('--gap',default='1/2000');args=parser.parse_args();run(args.gate,Q(args.gap))
