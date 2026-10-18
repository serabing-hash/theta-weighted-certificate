"""Source-free finite dyadic interval routines. No production work at import.
Adapted for delta128/P_up; original helpers CC BY-NC 4.0; 2026-10-18.
"""
from fractions import Fraction as Q
import hashlib
import json
import os
from pathlib import Path

BITS=160
DENSE_BITS=1024
class Hold(RuntimeError): pass

def require(test,message):
    if not test: raise Hold(message)

def integer(value):
    require(type(value) is str and value.isascii() and value and (value=='0' or (value[0]!='0' and value.isdecimal()) or (value[0]=='-' and len(value)>1 and value[1]!='0' and value[1:].isdecimal())), 'noncanonical integer')
    return int(value)

def gate(x):
    require(type(x) is int and abs(x).bit_length()<=DENSE_BITS, '1024-bit dense integer ceiling')
    return x

def ceildiv(a,b): return -((-a)//b)

def enclosure(lo,hi,den,bits):
    require(den>0 and lo<=hi,'invalid endpoints')
    scale=1<<bits
    l=lo*scale//den;u=ceildiv(hi*scale,den)
    c=(l+u)//2;r=max(c-l,u-c)
    return gate(c),gate(r)

def scalar(q,bits=160): return enclosure(q.numerator,q.numerator,q.denominator,bits)

def requant(c,r,frombits,tobits):
    require(r>=0,'negative radius')
    if frombits<=tobits:return gate(c<<(tobits-frombits)),gate(r<<(tobits-frombits))
    d=1<<(frombits-tobits);lo=(c-r)//d;hi=ceildiv(c+r,d);v=(lo+hi)//2
    return gate(v),gate(max(v-lo,hi-v))

def scalar_product(ac,ar,c,r):
    return gate(ac*c),gate(gate(gate(abs(ac)*r)+gate(ar*abs(c)))+gate(ar*r))

def shifted_model(alpha, p, q, k, beta, Pup, N, F, K, D, guard):
    """S=alpha*N-q*F+k*P_up+beta*I, B=alpha*K-p*D.
    Products first live on the 320-bit scale, then round outward once.
    P_up is exact before its separate160-bit encoding; no raw P radius here.
    This assembly makes no positivity or coefficient-optimality claim.
    """
    def build(xball, yball, multiplier, diagonal):
        xc, xr = xball; yc, yr = yball
        outc, outr = [], []
        for i, row in enumerate(xc):
            cc, rr = [], []
            for j, x in enumerate(row):
                a, ar = scalar_product(*alpha, x, xr[i][j])
                b, br = scalar_product(*multiplier, yc[i][j], yr[i][j])
                c, r = gate(a-b), gate(ar+br)
                if diagonal:
                    pc, pr = scalar_product(*k, Pup[0][i][j], Pup[1][i][j])
                    c, r = gate(c+pc), gate(r+pr)
                    if i == j:
                        c = gate(c + gate(beta[0] << 160))
                        r = gate(r + gate(beta[1] << 160))
                c, r = requant(c, r, 320, 160)
                cc.append(c); rr.append(r)
            outc.append(cc); outr.append(rr); guard()
        return outc, outr
    return build(N, F, q, True), build(K, D, p, False)


def trial_gram_upper(obj, trial, guard):
    """Finite row-witness replay only; true P inclusion remains inherited N3."""
    require(obj['format']=='RATIONAL_MID_RADIUS_MATRIX_V1' and
            obj['shape']==[68,68] and obj['symmetric'] is True, 'P68 schema')
    den=gate(integer(obj['denominator'])); require(den>0, 'P68 positive denominator')
    entries=obj['entries']
    require(type(entries) is list and len(entries)==68 and
            all(type(row) is list and len(row)==68 for row in entries), 'full P68 shape')
    centers=[]; radii=[]
    for row in entries:
        cc=[]; rr=[]
        for pair in row:
            require(type(pair) is list and len(pair)==2, 'P68 pair')
            c,r=[gate(integer(v)) for v in pair]; require(r>=0, 'P68 negative radius')
            cc.append(c); rr.append(r)
        centers.append(cc); radii.append(rr); guard()
    require(all(centers[i][j]==centers[j][i] and radii[i][j]==radii[j][i]
                for i in range(68) for j in range(i)), 'P68 exact transpose symmetry')
    rowrho=[]; upper=[]
    for i in range(68):
        rho=0; off=0
        for j in range(68):
            rho=gate(rho+radii[i][j])
            if i!=j: off=gate(off+abs(centers[i][j]))
        rowrho.append(rho); upper.append(Q(gate(gate(centers[i][i]+rho)+off),den)); guard()
    require(len(trial['row_upper_bounds'])==68 and
            upper==[Q(v) for v in trial['row_upper_bounds']], 'all68 saved P row witnesses')
    L=max(upper); nu=Q(trial['nu68']); slack=nu*nu-L
    require(L==Q(trial['L68']) and slack==Q(trial['nu68_square_slack'])>0,
            'P row maximum and positive saved norm slack')
    nums=[[gate(centers[i][j]+(rowrho[i] if i==j else 0)) for j in range(68)] for i in range(68)]
    # Exact rational P_up; the following radius is ONLY outward encoding loss.
    ballc=[]; ballr=[]
    for row in nums:
        pairs=[enclosure(x,x,den,160) for x in row]
        ballc.append([c for c,r in pairs]); ballr.append([r for c,r in pairs]); guard()
    exact_up={'format':'RATIONAL_EXACT_MATRIX_V1','shape':[68,68],'symmetric':True,
              'denominator':str(den),'numerators':[[str(x) for x in row] for row in nums]}
    witness={'method':'Pc+diag(row_sum(R)); physical R charged once',
             'physical_inclusion':'INHERITED-N3-NOT-REPROVED',
             'rho_rows':[str(Q(x,den)) for x in rowrho],
             'row_upper_bounds':[str(x) for x in upper], 'L68':str(L),
             'nu68':str(nu),'nu68_square_slack':str(slack),
             'encoding_radius':'exact P_up encoding loss only'}
    return exact_up,(ballc,ballr),witness

def parse_source(obj,shape,bits=160,legacy_A=False,symmetric=False):
    if legacy_A:
        require(obj['shape']==list(shape) and obj['bits']==100,'A schema')
        den=1<<100
    else:
        require(obj['format']=='RATIONAL_MID_RADIUS_MATRIX_V1' and obj['shape']==list(shape),'saved68 matrix schema')
        den=integer(obj['denominator']);require(den>0,'source denominator')
        require(obj['symmetric'] is symmetric,'source symmetry declaration')
    rows=obj['entries'];require(len(rows)==shape[0] and all(len(row)==shape[1] for row in rows),'source shape')
    c=[];r=[]
    for i,row in enumerate(rows):
        cc=[];rr=[]
        for j,pair in enumerate(row):
            require(isinstance(pair,list) and len(pair)==2,'mid-radius pair')
            m,rad=map(integer,pair);require(rad>=0,'source negative radius')
            lo,hi=m-rad,m+rad
            if symmetric:
                pair2=rows[j][i];require(isinstance(pair2,list) and len(pair2)==2,'transpose pair')
                tm,tr=map(integer,pair2);require(tr>=0,'transpose negative radius')
                lo=min(lo,tm-tr);hi=max(hi,tm+tr)
            u,v=enclosure(lo,hi,den,bits);cc.append(u);rr.append(v)
        c.append(cc);r.append(rr)
    return c,r


def interval_object(c,r,bits,symmetric=False):
    require(len(c)==len(r) and len(c)>0,'interval shape')
    return {'format':'DYADIC_INTERVAL_MATRIX_V1','shape':[len(c),len(c[0])],'bits':bits,'center':[[str(gate(x)) for x in row] for row in c],'radius':[[str(gate(x)) for x in row] for row in r],'symmetric':symmetric}

def exact_object(a,bits):
    return {'format':'DYADIC_EXACT_MATRIX_V1','shape':[len(a),len(a[0])],'bits':bits,'numerators':[[str(gate(x)) for x in row] for row in a]}

def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        while b:=f.read(1<<20):h.update(b)
    return h.hexdigest()

def save(path,obj):
    path=Path(path)
    with path.open('x',encoding='utf8') as f:
        json.dump(obj,f,separators=(',',':'),ensure_ascii=True);f.write('\n');f.flush();os.fsync(f.fileno())
    with path.open(encoding='utf8') as f:require(json.load(f)==obj,'exact JSON readback '+path.name)
    fd=os.open(path.parent,os.O_RDONLY)
    try:os.fsync(fd)
    finally:os.close(fd)

def read(path):
    def unique(pairs):
        d={}
        for k,v in pairs:require(k not in d,'duplicate JSON key');d[k]=v
        return d
    with Path(path).open() as f:return json.load(f,object_pairs_hook=unique)

def round_dyadic(m,e,bits=80):
    shift=e+bits
    gate(m)
    if shift>=0:
        require(abs(m).bit_length()+shift<=1024,'rounded coefficient/factor shift ceiling')
        return gate(m<<shift)
    k=-shift
    if k>abs(m).bit_length()+1:return 0
    d=1<<k
    return gate((2*m+d)//(2*d))
