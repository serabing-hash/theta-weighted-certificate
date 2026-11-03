#!/usr/bin/env python3
"""Independent exact checks; synthetic blocks are not theta certificates."""
from fractions import Fraction as F
from itertools import combinations, permutations
from pathlib import Path
import json

checks = 0
def ck(v):
    global checks
    assert v
    checks += 1
def mat(rows): return [[F(x) for x in row] for row in rows]
def eye(n): return mat([[int(i == j) for j in range(n)] for i in range(n)])
def zero(m,n): return mat([[0]*n for _ in range(m)])
def add(a,b): return [[x+y for x,y in zip(r,s)] for r,s in zip(a,b)]
def sc(c,a): return [[c*x for x in row] for row in a]
def sub(a,b): return add(a,sc(-1,b))
def tr(a): return [list(col) for col in zip(*a)]
def mm(a,b): return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def det(a):
    n=len(a); ans=F(0)
    for p in permutations(range(n)):
        term=F((-1)**sum(p[i]>p[j] for i in range(n) for j in range(i+1,n)))
        for i in range(n): term *= a[i][p[i]]
        ans += term
    return ans
def psd(a):
    if a != tr(a): return False
    return all(det([[a[i][j] for j in ids] for i in ids])>=0
               for n in range(1,len(a)+1) for ids in combinations(range(len(a)),n))
def inv(a):
    n=len(a); aug=[r+s for r,s in zip(a,eye(n))]
    for i in range(n):
        pivot=next(j for j in range(i,n) if aug[j][i])
        aug[i],aug[pivot]=aug[pivot],aug[i]
        value=aug[i][i]; aug[i]=[x/value for x in aug[i]]
        for j in range(n):
            if j!=i:
                value=aug[j][i]; aug[j]=[x-value*y for x,y in zip(aug[j],aug[i])]
    answer=[row[n:] for row in aug]
    ck(mm(a,answer)==eye(n)); ck(mm(answer,a)==eye(n))
    return answer
def enc(a): return [[str(x) for x in row] for row in a]
def block(a,rs,cs): return [[a[i][j] for j in cs] for i in rs]
def row_bound(a): return max(sum(abs(x) for x in row) for row in a)

R,d=262144,36; k=F(d,R); g=R-d
ck(k==F(9,65536)); ck(F(d*d,R)/(1-k)==F(324,65527))
tails=[F(d*d,g)*k**(2*n) for n in range(10)]
for n in range(9): ck(tails[n+1]==k*k*tails[n])
for n,cap in enumerate([F(4945,10**6),F(933,10**13),F(176,10**20),F(332,10**28)]): ck(tails[n]<cap)
prime=F(3609,10**21)*(1+F(d,g)**2)
ck(prime<F(361,10**20)); ck(prime+tails[2]<F(537,10**20))
ck(306*F(2,6401)**2==F(1224,40972801))

# Exact scalar endpoint/interior tests supplement, not replace, the proof.
for kap in [F(0),F(1,8),F(1,2),F(9,10)]:
    for n in range(7):
        for j in range(-8,9):
            x=kap*F(j,8); p=sum((x**i for i in range(2*n)),F(0))
            t=kap**(2*n)/(1-kap)
            ck(F(1)/(1-x)-p==x**(2*n)/(1-x))
            ck(0<=F(1)/(1-x)-p<=t)
            ck(x**(2*n)*(1+x)>=0)
            ck(kap**(2*n)*(1+kap)-x**(2*n)*(1+x)>=0)

# A distinct 2-low/3-high noncommuting example, including full-block stability.
Gamma=mat([[0,0,0,0,0],[0,1,0,0,0],[0,0,16,0,0],[0,0,0,25,0],[0,0,0,0,36]])
D1=mat([[F(1,5),F(1,7),F(1,11),F(-1,13),F(1,17)],
        [F(1,7),F(-1,3),F(1,19),F(1,23),F(-1,29)],
        [F(1,11),F(1,19),F(1,2),F(1,5),F(-1,7)],
        [F(-1,13),F(1,23),F(1,5),F(-1,2),F(1,11)],
        [F(1,17),F(-1,29),F(-1,7),F(1,11),F(1,3)]])
Delta=mat([[0,0,F(1,31),0,0],[0,F(1,41),0,0,0],[F(1,31),0,0,F(-1,37),0],[0,0,F(-1,37),0,0],[0,0,0,0,0]])
D2=add(D1,Delta); dm=F(2); Rm=F(16); km=dm/Rm; gm=Rm-dm
ck(row_bound(D1)<dm); ck(row_bound(D2)<dm)
lo=range(2); hi=range(2,5); G=block(Gamma,hi,hi)
half=mat([[F(1,4),0,0],[0,F(1,5),0],[0,0,F(1,6)]])
def schur(D):
    L=sub(Gamma,D); A=block(L,lo,lo); B=block(L,hi,lo); C=block(L,hi,hi)
    Ci=inv(C); return sub(A,mm(mm(tr(B),Ci),B)),A,B,C,Ci,L
S,A,B,C,Ci,L=schur(D1); S2,*_=schur(D2)
Dh=block(D1,hi,hi); K=mm(mm(half,Dh),half); T=mm(half,B); TT=mm(tr(T),T)
ck(mm(G,Dh)!=mm(Dh,G)); ck(psd(sub(sc(km,eye(3)),K))); ck(psd(add(sc(km,eye(3)),K)))
ck(Ci==mm(mm(half,inv(sub(eye(3),K))),half))
cost=mm(mm(tr(B),Ci),B); models=[]
for sign in [-1,0,1]:
    AA=add(cost,sc(sign,eye(2))); SS=sc(sign,eye(2)); p=zero(3,3); power=eye(3); last=None
    for n in range(9):
        if n:
            for _ in range(2): p=add(p,power); power=mm(power,K)
        t=km**(2*n)/(1-km); U=sub(AA,mm(mm(tr(T),p),T)); Fm=sub(U,sc(t,TT))
        ck(psd(sub(U,SS))); ck(psd(sub(SS,Fm)))
        ck(psd(sub(sc(t,TT),sub(U,SS)))); ck(psd(sub(sc(t,TT),sub(SS,Fm))))
        if last:
            ck(psd(sub(last[0],U))); ck(psd(sub(Fm,last[1])))
        if sign==0: ck(not psd(Fm))
        last=(U,Fm)
    models.append({'Schur_sign':sign,'stages':9,'last_upper':enc(U),'last_lower':enc(Fm)})
# Preserve the exact high inverse energy for arbitrary lifts.
for v in [mat([[1],[2],[3],[4],[5]]),mat([[F(1,3)],[F(-2,5)],[F(7,11)],[0],[F(-4,13)]])]:
    ell=v[:2]; residual=mm(L,v)[2:]
    q=mm(mm(tr(v),L),v)[0][0]
    inverse_cost=mm(mm(tr(residual),Ci),residual)[0][0]
    ck(q-inverse_cost==mm(mm(tr(ell),S),ell)[0][0])
r=row_bound(Delta); stability=r*(1+(dm/gm)**2); difference=sub(S2,S)
ck(psd(sub(sc(stability,eye(2)),difference)))
ck(psd(add(sc(stability,eye(2)),difference)))
out={'status':'PASS','exact_checks':checks,'error_exact':[str(x) for x in tails],
     'model':'Independent two-low/three-high rational noncommuting blocks',
     'models':models,'stability_upper':str(stability),
     'scope':'Scalar arithmetic and synthetic finite-block checks only. The analytic proof handles infinite operators. No theta moment, projection, whole-low sign, core theorem, global one-half or RH is certified.'}
Path(__file__).with_name('INDEPENDENT_RESPONSE_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS:',checks,'exact checks, including independent residual identity and Schur stability')
