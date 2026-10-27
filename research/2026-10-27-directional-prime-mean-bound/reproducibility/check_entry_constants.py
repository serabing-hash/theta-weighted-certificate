"""Exact rational source-free checks for entry constants.
Does not evaluate kappa, theta sums, prime sums, quadrature, or spectra.
"""
from fractions import Fraction as F
from math import factorial, comb
import json
checks=[]
def check(name,condition):
    assert condition,name
    checks.append(name)
def E(x,n): return sum((x**j/F(factorial(j)) for j in range(n+1)),F())
def U(x,n): return E(x,n)+x**(n+1)/F(factorial(n+1))/(1-x/F(n+2))
for x,n,upper in [(F(44,7),50,537),(F(13,25),12,F(17,10)),(F(27,5),40,225),(F(3,5),12,F(11,6)),(F(29,5),40,333),(F(1,3),12,F(3,2)),(F(1,4),12,F(4,3)),(F(1,8),12,F(8,7)),(F(2),25,8)]:
    check(f'exp_upper_{x}',U(x,n)<upper)
for x,n,lower in [(F(13,25),8,F(5,3)),(F(39,20),6,7),(F(3,4),3,2),(F(3,2),4,4),(F(3),8,20)]:
    check(f'exp_lower_{x}',E(x,n)>lower)
check('e2_partial',E(F(2),4)==7)
loglo=2*sum((F(1,(2*j+1)*3**(2*j+1)) for j in range(7)),F())
loghi=loglo+2*F(1,3**15)/15/(1-F(1,9))
check('log2_bracket',F(693,1000)<loglo<loghi<F(69315,100000))
check('a2',F(99,70)**2>2 and F(693,1000)/F(99,70)==F(49,100))
check('sqrt2_lower',F(140,99)**2<2)
check('root4',F(19,16)**4<2<F(6,5)**4)
for x,n,upper in [(F(1,5),4,F(50,49)),(F(1,2),4,F(8,7)),(F(1),6,F(25,16))]:
    v=sum((x**(2*j)/F(factorial(2*j)) for j in range(n+1)),F())
    v+=x**(2*n+2)/F(factorial(2*n+2))/(1-x*x/F((2*n+3)*(2*n+4)))
    check(f'cosh_upper_{x}',v<upper)
# Polynomial arithmetic in ascending coefficients.
def add(a,b):
    c=[F()]*max(len(a),len(b))
    for i,x in enumerate(a):c[i]+=x
    for i,x in enumerate(b):c[i]+=x
    return c
def scale(a,c):return [x*c for x in a]
def mul(a,b):
    c=[F()]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]+=x*y
    return c
def L(a):
    return add([x*(F(1,2)+2*i) for i,x in enumerate(a)],[F()]+scale(a,-2))
h0=list(map(F,[0,-6,4]));h1=L(h0);h2=L(h1);h4=L(L(h2))
check('h1',h1==list(map(F,[0,-15,30,-8])))
check('h2',h2==[0,F(-75,2),165,-112,16])
check('h4',h4==[0,F(-1875,8),F(15465,4),-8512,5176,-1056,64])
Q=list(map(F,[-58275,135730,-121856,49088,-8448,512]))
check('Q_identity',add(add(h4,scale(h2,60)),scale(h0,800))==[F()]+scale(Q,F(1,8)))
rows={3:[88575,113521,139459,163285,181127,190905],4:[190905,200683,202397,193967,175105,149875],5:[149875,124645,93047,59145,31355,25005]}
for j,row in rows.items():
    left=[5*sum((Q[k]*comb(k,i)*j**(k-i) for k in range(i,6)),F()) for i in range(6)]
    right=[sum((F(row[i]*comb(5,i)*comb(5-i,k-i)*(-1)**(k-i)) for i in range(k+1)),F()) for k in range(6)]
    check(f'Bernstein_{j}',left==right and min(row)>0)
shift=[sum((Q[k]*comb(k,i)*6**(k-i) for k in range(i,6)),F()) for i in range(6)]
check('Q_tail',shift==[5001,-6350,42880,30656,6912,512])
check('Q_discriminant',4*42880*5001-6350**2==817449020>0)
check('core_first',F(6,5)*F(475,4)/F(12325,24)==F(684,2465))
check('core_theta_tail',F(49152,5*20**8)<F(1,10**6)<F(13,44370)==F(5,18)-F(684,2465))
check('core_mass',F(5,9)*(F(6,5)/F(13,2)+1/F(15,2))==F(62,351))
check('cosh_a',F(1,2)+F(3,4)/F(140,99)==F(577,560)<F(41,40)**2)
check('KI',F(20,41)*F(289,351)==F(5780,14391)>F(2,5))
check('source_lower_endpoints',F(325,504)>F(2,5) and F(19,16)*F(475,4)/537>F(21,80) and F(113,100)*F(2106,25)/225>F(2,5) and F(23,20)*F(2494,25)/333>F(1,3))
check('finite_returns',F(49,100)**2*F(21,80)>F(1,16) and F(49,750)>F(1,16) and F(196,3125)>F(1,16))
check('tail_h2',16+F(112,60)+F(165,60**2)+F(75,2*60**3)<18)
check('tail_h4',64+F(1056,60)+F(5176,60**2)+F(8512,60**3)+F(15465,4*60**4)+F(1875,8*60**5)<84)
check('g_tail_coefficient',(27*18/F(60**2)+84)/47<2 and (27*(4+F(6,60))/F(60**4)+18/F(60**2))/47<2)
check('g_full_tail',F(2*14**7,20**10)/(1-F(1,20**30))<F(1,100))
check('large_y_row',F(107,376)-F(1,6)-F(97,3600)==F(15391,169200)>F(1,16))
check('gamma_constant',F(1,2)+F(8,25)-F(5,7)==F(37,350))
check('mass_and_h',F(81,188)*1128==486 and (F(1,4)+20)/47==F(81,188))
check('outward_tail',F(16,20**27)<F(1,2) and F(4,3)**6/20**7<F(1,2) and F(4*3**6,20**5)==F(729,800000)<1)
output={'scope':'source-free exact rational and polynomial entry checks','assertion_count':len(checks),'checks':checks,'status':'PASS','excluded':'No theta source, prime enumeration, quadrature, numerical spectral or prior certificate replay'}
print(json.dumps(output,indent=2))
