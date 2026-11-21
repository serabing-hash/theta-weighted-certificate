"""Unsmoothed B=2 only, larger W at n=150000. Reuses exact source data and interval code."""
from pilot import I,F,pm,powers_active,dT,c
from math import floor
a=F(5,8); B=2; n=150_000
Cp=[I(0) for _ in range(55)];Sp=[I(0) for _ in range(55)]
for m,p in powers_active:
    w=I(p).op('log')/I(m).op('sqrt')
    z=(a*I(m).op('log')).op('exp'); C=(z+1/z)/2; S=(z-1/z)/2
    Cp[m]=w*C;Sp[m]=w*S
for m in range(1,55):
    Cp[m]=Cp[m]+Cp[m-1];Sp[m]=Sp[m]+Sp[m-1]
best=0; hiat=None
for l in range(1024):
    x=F(l,512);y=x+F(1,512)
    k=floor((I(B)+y).op('exp').ab()[1]); j=floor((I(B)-x).op('exp').ab()[1]); assert 0<=j<=k<=54
    e=(2*a*I(x)).op('exp');t=(e-1)/(e+1)
    bound=Cp[k]+Cp[j]-t*(Sp[k]-Sp[j])
    if bound.ab()[1]>best:best=bound.ab()[1];hiat=[l,j,k]
print('weighted row bound at 1024 intervals',best,hiat)
assert best<8.75
s=F(2*B,2*n-1);g=4-I(s)**2-(I(s)*F(5,2)).op('log');D=g-c-F(35,4)
print('Legendre reciprocity s',s,'Gamma lower',g.ab(),'C_raw lower (p=8.75)',D.ab())
assert D.ab()[0]>0.180
U=10_000
assert (I(1).op('exp')*B*U/n).ab()[1]<0.5 and (2*B*U).bit_length()<2*n-200
K=pm+c
J=F(1,2**100)*(17*dT(2)+K*dT(0))+(17*dT(6)+K*dT(4))/U**4
print('joint R',J.ab(),'Schur debit',(J**2/F(18,100)).ab())
