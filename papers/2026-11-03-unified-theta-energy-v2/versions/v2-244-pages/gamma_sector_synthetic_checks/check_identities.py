"""Exact rational checks of audit identities, not an actual theta sign certificate."""
from fractions import Fraction as F
import json
from pathlib import Path

def mat(a): return [[F(x) for x in row] for row in a]
def tr(a): return [list(c) for c in zip(*a)]
def add(a,b): return [[x+y for x,y in zip(r,s)] for r,s in zip(a,b)]
def neg(a): return [[-x for x in r] for r in a]
def sub(a,b): return add(a,neg(b))
def mul(a,b): return [[sum((x*y for x,y in zip(r,c)),F(0)) for c in zip(*b)] for r in a]
def eye(n): return [[F(i==j) for j in range(n)] for i in range(n)]
def inverse(a):
    n=len(a); w=[r[:]+s for r,s in zip(a,eye(n))]
    for k in range(n):
        p=next(i for i in range(k,n) if w[i][k])
        w[k],w[p]=w[p],w[k]
        v=w[k][k]; w[k]=[x/v for x in w[k]]
        for i in range(n):
            if i!=k:
                v=w[i][k]; w[i]=[x-v*y for x,y in zip(w[i],w[k])]
    return [r[n:] for r in w]
def ldlt_pivots(a):
    w=[r[:] for r in a]; out=[]
    for k in range(len(w)):
        p=w[k][k]; out.append(p)
        assert p>0
        for i in range(k+1,len(w)):
            for j in range(k+1,len(w)):
                w[i][j]-=w[i][k]*w[k][j]/p
    return out
def quadratic(a,v): return mul(mul([v],a),tr([v]))[0][0]
def serial(a): return [[str(x) for x in r] for r in a]

results=[]

# Positive full form even though no scalar kappa can satisfy the original pair.
A=mat([[1]]); C=mat([[F(1,2),0],[0,2]]); B=mat([[0],[1]])
full=mat([[1,0,1],[0,F(1,2),0],[1,0,2]])
p=ldlt_pivots(full)
response=mul(mul(tr(B),inverse(C)),B)
assert response==mat([[F(1,2)]])
assert F(1)>1-F(1,2)
results.append({'check':'positive block versus scalar sufficient pair','status':'PASS',
                'LDLT_pivots':[str(x) for x in p], 'response':serial(response),
                'scope':'synthetic, not theta'})

# All individual low/high pairs are positive, collective coupling can fail.
pair=mat([[1,F(1,10)],[F(1,10),1]])
ldlt_pivots(pair)
n=101
value=F(1)+n*F(1,100)-n*F(1,50)
assert value==F(-1,100)
results.append({'check':'collective coupling','status':'PASS','N':n,
                'value_at_x_1_all_y_minus_1_over_10':str(value),
                'scope':'synthetic, not theta'})

# Full residual identity with a noncommuting high matrix and two sources.
C=mat([[3,1],[1,2]]); B=mat([[1,2],[0,1]])
Y=mat([[F(1,4),0],[0,F(1,4)]])
Ci=inverse(C)
ldlt_pivots(sub(C,eye(2))) # certifies C >= I, so g=1 is valid.
R=sub(B,mul(C,Y))
H=sub(add(mul(tr(B),Y),mul(tr(Y),B)),mul(mul(tr(Y),C),Y))
response=mul(mul(tr(B),Ci),B)
remainder=mul(mul(tr(R),Ci),R)
assert response==add(H,remainder)
budget=mul(tr(R),R)
ldlt_pivots(sub(budget,remainder))

# Congruence verifies the actual represented Gram budget under nonorthogonal J.
J=mat([[1,1],[0,F(1,2)]])
gram=mul(tr(J),J)
Rj=mul(R,J)
congruent=mul(mul(tr(J),remainder),J)
assert congruent==mul(mul(tr(Rj),Ci),Rj)
results.append({'check':'complete residual identity and Gram congruence',
                'status':'PASS','response':serial(response),
                'residual':serial(R),'remainder':serial(remainder),
                'actual_Gram':serial(gram),'scope':'synthetic, not theta'})

out={'arithmetic':'Python standard-library Fraction; exact rational arithmetic',
     'actual_theta_matrix_sign_test':False,
     'raw_archive_restoration_repeated':False,
     'results':results}
path=Path(__file__).with_name('exact_check_results.json')
path.write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(out,indent=2,ensure_ascii=False))
