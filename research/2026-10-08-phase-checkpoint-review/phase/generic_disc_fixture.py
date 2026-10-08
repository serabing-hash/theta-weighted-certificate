"""Source-free rational fixture for a centered-disc phase recurrence.

No FLINT, source phases, logarithms, action/cache imports, or Work execution.
A fixed dyadic mesh is a generic enclosure arithmetic fixture, not a simulation
of the Arb backend. This tests the induction, not 160-bit backend performance.
"""
from fractions import Fraction as F
from math import isqrt
import json

BITS=160
S=1<<BITS

def down(x): return F((x*S).numerator//(x*S).denominator,S)
def up(x): return -down(-x)
def hull(x,y): return (down(min(x,y)),up(max(x,y)))
def add(a,b): return (down(a[0]+b[0]),up(a[1]+b[1]))
def neg(a): return (-a[1],-a[0])
def mul(a,b):
    vs=[x*y for x in a for y in b]
    return (down(min(vs)),up(max(vs)))
def cmul(a,b): return (add(mul(a[0],b[0]),neg(mul(a[1],b[1]))),add(mul(a[0],b[1]),mul(a[1],b[0])))
def point(z): return ((z[0],z[0]),(z[1],z[1]))
def midpoint(a): return (down((a[0][0]+a[0][1])/2),down((a[1][0]+a[1][1])/2))
def ce(a,q): return up(sum(max(abs(q[j]-a[j][0]),abs(a[j][1]-q[j])) for j in (0,1)))
def exactmul(a,b): return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def within_disc(z,q,e): return sum((z[j]-q[j])**2 for j in (0,1))<=e*e

def serialize_cosine(q,e,bits=140):
    scale=1<<bits
    value=q*scale
    m=value.numerator//value.denominator
    discrepancy=(abs(q-F(m,scale))+e)*scale
    r=-(-discrepancy.numerator//discrepancy.denominator)
    return {'midpoint_numerator':str(m),'radius_numerator':str(r),'denominator_bits':bits}

def restore_cosine(record):
    s=1<<record['denominator_bits'];m=F(int(record['midpoint_numerator']),s);r=F(int(record['radius_numerator']),s)
    return m-r,m+r

def roundtrip_tests():
    fixtures=[(F(3,5),F(1,1<<125)),(F(-7,13),F(1,1<<151)),(F(0),F(1,1<<140)),(F(1,1<<160),F(7,1<<148))]
    out=[]
    for q,e in fixtures:
        record=serialize_cosine(q,e);l,u=restore_cosine(record)
        assert l<=q-e and q+e<=u
        assert int(record['radius_numerator'])>0
        out.append({'input_center':str(q),'input_full_cumulative_error':str(e),'record':record,'entire_input_ball_contained':True})
    return out

def run_fixture(rho,N):
    assert rho[0]**2+rho[1]**2==1
    seed_rad=F(1,1<<150)
    R=tuple((down(t)-seed_rad,up(t)+seed_rad) for t in rho)
    q=(F(1),F(0)); e=F(0); E_num=0; exact=q; rectangle=point(q)
    first_rect_radius_one=None
    maxe=F(0)
    for k in range(1,N+1):
        P=cmul(point(q),R)
        local=[]
        for interval in P:
            record=serialize_cosine((interval[0]+interval[1])/2,(interval[1]-interval[0])/2,140)
            local.append((int(record['midpoint_numerator']),int(record['radius_numerator'])))
        q=tuple(F(n,1<<140) for n,r in local)
        E_num+=sum(r for n,r in local)
        e=F(E_num,1<<140)
        exact=exactmul(exact,rho)
        assert within_disc(exact,q,e),(rho,k)
        L,U=restore_cosine(serialize_cosine(q[0],e)); assert L<=q[0]-e and q[0]+e<=U; assert L<=exact[0]<=U
        rectangle=cmul(rectangle,R)
        assert all(rectangle[j][0]<=exact[j]<=rectangle[j][1] for j in (0,1))
        r=max((x[1]-x[0])/2 for x in rectangle)
        if r>=1 and first_rect_radius_one is None:first_rect_radius_one=k
        maxe=max(maxe,e)
    assert e< F(1,1<<130)
    return {'rho':[str(x) for x in rho],'steps':N,'exact_target_contained_every_step':True,'centered_disc_error_upper':str(maxe),'terminal_cumulative_error_numerator_bits140':E_num,'centered_disc_error_lt_2^-130':True,'rectangular_radius_first_ge_1':first_rect_radius_one,'rectangular_final_radius_approx':float(r)}

if __name__=='__main__':
    out={'scope':'generic exact-rational unit phases only; no actual cache; not FLINT backend verification','precision_mesh_bits':BITS,'exact_center_and_error_denominator_bits':140,'cosine_radius_roundtrips':roundtrip_tests(),'fixtures':[run_fixture((F(3,5),F(4,5)),384),run_fixture((F(-3,5),F(4,5)),384),run_fixture((F(0),F(1)),32),run_fixture((F(1),F(0)),32)]}
    print(json.dumps(out,indent=2))
