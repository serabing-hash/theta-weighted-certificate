"""Pure finite-matrix native proposal routines, imported only after charged admission.
No physical source/action/DFT/quadrature modules. CC BY-NC 4.0.
"""
from fractions import Fraction as Q
import os, time
if os.environ.get('SHIFT_CHARGED_NATIVE_ADMISSION') != '1' or not 0 < time.monotonic_ns()-int(os.environ.get('SHIFT_EPOCH_NS','0')) < 60_000_000_000:
    raise RuntimeError('native import outside timed admitted attempt')
from flint import arb,arb_mat,fmpz_mat,ctx
from shift_exact import require,gate,enclosure,requant,scalar_product,round_dyadic


def exact(a):
    m,e=a.man_exp();m,e=int(m),int(e)
    return Q(m<<e) if e>=0 else Q(m,1<<(-e))

def scaled_endpoint(a,bits,up):
    m,e=a.man_exp();m,e=gate(int(m)),int(e)+bits
    if e>=0:
        require(abs(m).bit_length()+e<=1024,'native endpoint shift ceiling')
        return gate(m<<e)
    k=-e
    if k>abs(m).bit_length()+1:
        return (1 if m>0 else 0) if up else (-1 if m<0 else 0)
    den=1<<k
    return gate(-((-m)//den) if up else m//den)

def ball_record(a,bits=160):
    require(a.is_finite(),'nonfinite native ball')
    l=scaled_endpoint(a.lower(),bits,False);u=scaled_endpoint(a.upper(),bits,True)
    c=gate((l+u)//2)
    return c,gate(max(c-l,u-c))

def midpoint(a):
    require(a.is_finite(),'nonfinite native solution/factor')
    m,e=a.mid().man_exp();return gate(int(m)),int(e)

def point(n,bits):return arb((n,-bits))

def point_matrix(rows,bits):return arb_mat([[point(n,bits) for n in row] for row in rows])

def maxbits(a):
    return max((abs(int(a[i,j])).bit_length() for i in range(a.nrows()) for j in range(a.ncols())),default=0)

def mul(a,b,guard):
    require(a.ncols()==b.nrows(),'native product shape')
    # This absolute partial-sum bound gates every hidden exact accumulation,
    # before allocating/executing a native integer matrix product.
    require(maxbits(a)+maxbits(b)+(a.ncols()-1).bit_length()<=1024,'native product a priori 1024-bit accumulation bound')
    guard();c=a*b;require(maxbits(c)<=1024,'native product output bit ceiling');guard();return c

def rows(a):return [[gate(int(a[i,j])) for j in range(a.ncols())] for i in range(a.nrows())]



def solve(Sc,Bc,guard):
    require(ctx.prec==160,'native precision changed')
    guard();S=point_matrix(Sc,160);B=point_matrix(Bc,160)
    # Exactly one 68 by 68 center solve, 372 RHS, fixed precision LU.
    sol=S.solve(B,algorithm='lu');guard()
    C=[];M=[];cent=[];rad=[];err=[]
    for i in range(sol.nrows()):
        cr=[];mr=[];sr=[];rr=[];er=[]
        for j in range(sol.ncols()):
            a=sol[i,j];m,e=midpoint(a);n=round_dyadic(m,e,80);c,r=ball_record(a)
            cr.append(n);mr.append([str(m),e]);sr.append(c);rr.append(r);er.append(str(gate(abs(gate(c-gate(n<<80)))+r)))
        C.append(cr);M.append(mr);cent.append([str(x) for x in sr]);rad.append([str(x) for x in rr]);err.append(er)
    guard()
    return C,{'format':'FULL372_CENTER_SOLVE_DIAGNOSTICS_V1','shape':[68,372],'solution_midpoints':M,'solution_enclosures':{'bits':160,'center':cent,'radius':rad},'C_error_upper_numerators_bits160':err,'purpose':'Proposal diagnostics only; C is not asserted to minimize every input interval member.','algorithm':'lu','precision_bits':160,'coefficient_solves':1}

def normal_residual(Sc,C,Bc,guard):
    v=mul(fmpz_mat(Sc),fmpz_mat(C),guard)
    return [[gate(int(v[i,j])-gate(Bc[i][j]<<80)) for j in range(v.ncols())] for i in range(v.nrows())]

def consumer(alpha,A,S,B,C,guard):
    ac,ar=alpha;Ac,Ar=A;Sc,Sr=S;Bc,Br=B
    cn=fmpz_mat(C);ab=fmpz_mat([[abs(x) for x in row] for row in C]);ct=cn.transpose();at=ab.transpose()
    X=mul(ct,fmpz_mat(Bc),guard);Xr=mul(at,fmpz_mat(Br),guard)
    skinny=mul(fmpz_mat(Sc),cn,guard);Y=mul(ct,skinny,guard);del skinny
    skinny=mul(fmpz_mat(Sr),ab,guard);Yr=mul(at,skinny,guard);del skinny,cn,ab,ct,at
    U=[];R=[];n=len(Ac)
    for i in range(n):
        cc=[];rr=[]
        for j in range(n):
            c,r=scalar_product(ac,ar,Ac[i][j],Ar[i][j])
            c=gate(c-gate(gate(int(X[i,j])+int(X[j,i]))<<80));c=gate(c+int(Y[i,j]))
            r=gate(r+gate(gate(int(Xr[i,j])+int(Xr[j,i]))<<80));r=gate(r+int(Yr[i,j]))
            c,r=requant(c,r,320,100);cc.append(c);rr.append(r)
        U.append(cc);R.append(rr);guard()
    for i in range(n):
        for j in range(i):require(U[i][j]==U[j][i] and R[i][j]==R[j][i],'final consumer symmetry')
    rc=[gate(sum(row)) for row in R]
    cert=[[gate(U[i][j]+(rc[i] if i==j else 0)) for j in range(n)] for i in range(n)]
    return U,R,cert,rc

def ldlt_blocks(S,guard,block=16):
    """Outward fixed-order block LDL; extracted finite-matrix routine only.
    Every exact Schur complement and factor entry remains inside Arb balls.
    """
    n=S.nrows();Schur=S;L=arb_mat(n,n);piv=[]
    for offset in range(0,n,block):
        size=min(block,n-offset);left=Schur.nrows()
        B=arb_mat([[Schur[i,j] for j in range(size)] for i in range(size)])
        lb=arb_mat(size,size);db=[]
        for k in range(size):
            d=B[k,k]-sum((lb[k,j]*lb[k,j]*db[j] for j in range(k)),arb(0))
            require(d.is_finite(),'nonfinite LDL pivot '+str(offset+k))
            if not d.lower()>0:
                pc,pr=ball_record(d,160)
                raise RuntimeError('unaccepted LDL pivot '+str(offset+k)+'; accepted='+str(len(piv)+len(db))+'; bits160 center='+str(pc)+' radius='+str(pr))
            db.append(d);lb[k,k]=1
            for i in range(k+1,size):lb[i,k]=(B[i,k]-sum((lb[i,j]*lb[k,j]*db[j] for j in range(k)),arb(0)))/d
        for i in range(size):
            for j in range(i+1):L[offset+i,offset+j]=lb[i,j]
        piv.extend(db)
        if left>size:
            cross=arb_mat([[Schur[i,j] for j in range(size)] for i in range(size,left)])
            tail=B.solve(cross.transpose(),algorithm='lu').transpose()*lb
            for i in range(left-size):
                for j in range(size):L[offset+size+i,offset+j]=tail[i,j]
            td=arb_mat(left-size,size)
            for i in range(left-size):
                for j in range(size):td[i,j]=tail[i,j]*db[j]
            rest=arb_mat([[Schur[i,j] for j in range(size,left)] for i in range(size,left)])
            Schur=rest-td*tail.transpose()
        guard();require(ctx.prec==160,'LDL precision changed')
    return L,piv

def factor(U,guard,on_inverse):
    n=len(U);q=1<<80
    T=point_matrix([[gate((1<<100 if i==j else 0)-U[i][j]) for j in range(n)] for i in range(n)],100)
    L,piv=ldlt_blocks(T,guard);del T
    # Round newly produced factor midpoints, never reuse any previous factor.
    ln=[[round_dyadic(*midpoint(L[i,j]),80) if j<i else q if i==j else 0 for j in range(n)] for i in range(n)]
    dn=[round_dyadic(*midpoint(d),80) for d in piv]
    pe=[list(map(str,ball_record(d,160))) for d in piv]
    require(all(int(c)-int(r)>0 for c,r in pe),'serialized LDL pivot not strictly positive')
    require(min(dn)>0,'rounded D not positive');del L,piv
    on_inverse();guard();Inv=point_matrix(ln,80).inv();guard()
    mn=[[round_dyadic(*midpoint(Inv[i,j]),80) if j<=i else 0 for j in range(n)] for i in range(n)]
    del Inv
    # Exact witness verification using independently recomputed native integer products.
    Lz=fmpz_mat(ln);Mz=fmpz_mat(mn)
    ld=fmpz_mat([[gate(ln[i][j]*dn[j]) for j in range(n)] for i in range(n)])
    prod=mul(ld,Lz.transpose(),guard);del ld
    rho_num=0
    for i in range(n):
        rs=0
        for j in range(n):
            v=gate((1<<240 if i==j else 0)-gate(U[i][j]<<140));v=gate(v-int(prod[i,j]));rs=gate(rs+abs(v))
        rho_num=max(rho_num,rs);guard()
    del prod
    ir=mul(Lz,Mz,guard);del Lz,Mz
    col=[0]*n;einf_num=0
    for i in range(n):
        rs=0
        for j in range(n):
            v=abs(gate(int(ir[i,j])-(1<<160 if i==j else 0)));col[j]=gate(col[j]+v);rs=gate(rs+v)
        einf_num=max(einf_num,rs)
    del ir
    e1=Q(max(col),1<<160);einf=Q(einf_num,1<<160)
    m1=Q(max(gate(sum(abs(mn[i][j]) for i in range(n))) for j in range(n)),q);minf=Q(max(gate(sum(abs(x) for x in row)) for row in mn),q)
    d0=Q(min(dn),q);rho=Q(rho_num,1<<240)
    require(e1<1 and einf<1 and m1>0 and minf>0 and d0>0,'finite factor inverse norm gates')
    mu=d0*(1-e1)*(1-einf)/(m1*minf)-rho;require(mu>0,'nonpositive direct-I exact witness margin')
    vals={k:str(v) for k,v in [('rho0',rho),('e1',e1),('einf',einf),('m1',m1),('minf',minf),('d0',d0),('mu372',mu)]}
    return {'format':'SHIFT372_EXACT_FACTOR_V1','shape':[n,n],'bits':80,'L_numerators':[[str(x) for x in row] for row in ln],'D_numerators':[str(x) for x in dn],'inverse_factor_numerators':[[str(x) for x in row] for row in mn],'target':'1','pivot_enclosures_bits160':pe,'accepted_pivots':n,'precision_bits':160,'block_size':16,'exact_check_values':vals}
