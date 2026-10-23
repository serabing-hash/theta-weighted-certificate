# Physical same-frequency two-mode Schur margin

## 1. Statement and reading convention

For the full source W and form Q_inv defined below, a>0 and b-c²/a>1/62500 uniformly on [14,29/2]. This document gives the actual analytic derivation, including all six boundary vertices. Section numbering follows the proof dependency order. This is not a numerical or formal certificate. The derivative coefficient is 5/4, not the unsupported stronger coefficient 1.

## 2. Full source, regularity, physical form, and exact joint entries

For x>=0, define

    t_n = pi n^2 exp(2x),
    P0(t) = 4t^2-6t,
    F0(x) = 2/(1+exp(-x)),
    kappa(x) = exp(x/2) sum_(n>=1) P0(t_n)exp(-t_n),
    W(x) = F0(x) sum_(n>=1) P0(t_n)exp(-t_n)
         = kappa(x)/cosh(x/2).

All summands are positive since t_n>=pi>3. The source is not rescaled or replaced by its first summand.

For completeness, its actual even analytic continuation follows from the classical Jacobi identity. Put Theta(y)=sum_(k in Z)exp(-pi k^2 y) and H(z)=exp(z/2)Theta(exp(2z)). On |Im z|<pi/4 the normally convergent theta series and Theta(y)=y^(-1/2)Theta(1/y) give H(z)=H(-z). Direct differentiation yields

    kappa(z) = (1/2)(d^2/dz^2-1/4)H(z).

The constant theta term is annihilated and the two integer signs give exactly the stated source normalization. The quotient by cosh(z/2) has no pole on this strip. This establishes the even continuation used throughout. The standard theta identity is the sole classical theta input, identified as NIST DLMF 20.7.32.

On the closed inner strip |Im z|<=1/2, all derivatives have normally convergent polynomial-exponential bounds with decay exp[-pi cos(1)exp(2|Re z|)]. Thus the contour shifts below, Fourier integrations by parts, and vanishing boundary terms are legitimate for this actual source. Real-line derivatives have all moments needed below.

For the real test functions considered here, the exact physical form is

    Q_inv(f) = D_Gamma(f)-c_Gamma ||f||_2^2
               -2 sum_(n>=2) Lambda(n) C_f(log n)/sqrt(n),
    C_f(s) = integral_R f(x)f(x+s) dx,
    D_Gamma(f) = integral_0^infinity rho(s)||f-tau_s f||_2^2 ds,
    rho(s) = exp(-s/2)/(1-exp(-2s)),
    tau_s f(x) = f(x+s),
    c_Gamma = log pi+EulerGamma+pi/2+3log2.

Lambda(n) is log p for every positive prime power n=p^k, and zero otherwise. In particular n=4 and all later prime powers remain included. Small-s convergence follows from ||f-tau_s f||<=s||f'|| and rho(s)=O(1/s). Large-s and prime-series convergence follow from the source bounds proved below. Polarization defines Q_inv(q,v).

Use

    F(u) = integral_R W(x)exp(-iux) dx,
    dmu(u) = du/(2pi),
    M = integral F^2 dmu = ||W||_2^2,
    g(t) = sum_(j>=0) 2t^2/[a_j(a_j^2+t^2)],
    a_j = 2j+1/2.

Expansion of rho into its positive exponential series and Plancherel give this g exactly; the factor 2 comes from |1-exp(its)|^2. F is real-even and F' is real-odd.

Set q=W cos(gamma x), v=-xW sin(gamma x). Then

    qhat(xi) = [F(xi-gamma)+F(xi+gamma)]/2,
    vhat(xi) = [F'(xi+gamma)-F'(xi-gamma)]/2.

Write a=Q_inv(q), b=Q_inv(v), c=Q_inv(q,v), and

    h_gamma(u) = [g(gamma+u)+g(gamma-u)]/4-c_Gamma/2.

The Gamma diagonal carriers are integral h_gamma F^2 dmu and integral h_gamma F'^2 dmu. Their opposite-packet terms are respectively

    R_q = (1/2)integral [g(xi)-c_Gamma]F(xi-gamma)F(xi+gamma)dmu,
    R_T = -(1/2)integral [g(xi)-c_Gamma]F'(xi-gamma)F'(xi+gamma)dmu.

Writing F_-=F(xi-gamma), F_+=F(xi+gamma), direct multiplication gives

    qhat*vhat = -(1/8)(F_-^2-F_+^2)'
                 +(1/4)(F_-F_+'-F_+F_-').

Integration by parts, followed by evenness of g'(xi)(F_-^2-F_+^2), therefore gives the exact cross carrier

    D_gamma = (1/4)integral_0^infinity
       g'(xi)[F(xi-gamma)^2-F(xi+gamma)^2] dxi/(2pi).

The cross opposite packet has the prefactor 1/4 and the displayed mixed-product difference. The negative second packet in D_gamma is not optional in lower bounds.

For s=log n, d=s/2, put

    U_s(y)=W(y-d)W(y+d),
    A(s)=integral U_s(y)dy,
    Y(s)=integral y^2 U_s(y)dy,
    A_T(s)=Y(s)-d^2 A(s).

The cosine prime carrier is -sum Lambda(n)A(log n)cos(gamma log n)/sqrt(n); its midpoint term is -sum Lambda(n)integral U_log n(y)cos(2gamma y)dy/sqrt(n).

The tangent carrier is -sum Lambda(n)A_T(log n)cos(gamma log n)/sqrt(n); its midpoint term has a PLUS sign and integrand (y^2-d^2)U_s(y)cos(2gamma y). The cross prime terms, either by direct polarization or half the exact derivative of the cosine diagonal, are

    sum Lambda(n)(s/2)A(s)sin(gamma s)/sqrt(n)
      + sum Lambda(n)integral yU_s(y)sin(2gamma y)dy/sqrt(n).

These decompositions account for all factors of two and all components charged later.

## 3. Elementary scalar certificates

The following inequalities are independently reproducible from elementary series; they are rational bounds, not numerical evaluations:

    157/50 < pi < 22/7,
    163/60 < e < 87/32,
    exp(2)>125/17, exp(2)<200/27,
    502/25 < exp(3) < 201/10,
    529 < exp(2pi) < 540,
    exp(4pi)>280000, exp(6pi)>150732800,
    exp(8)>2900, exp(10)>21600,
    exp(14)>20000000/17>10^6,
    exp(14)<1250000,
    56/81 < log2 < 25/36,
    263/240 < log3 < 11/10.

Here is a compact verification of the precision actually needed.

1. Machin's identity and alternating atan bounds give the pi enclosure. The lower bound is 1184/375-4/239=281476/89625>157/50; an upper bound is 4711/1500+16/15625<22/7.
2. The exponential sum through degree five is 163/60. The sum through degree six is 1957/720, and its tail is below 1/4410, proving the upper e bound. Squaring gives exp(2)>125/17 and exp(2)<200/27.
3. The degree-eight sum at 3 is 806769/40320>20009/1000; the next three terms exceed 27/500, 2/125, 1/250. Their sum proves exp(3)>502/25. The upper e bound cubed is below 201/10.
4. Since log(4/3)>2/7, exp(2pi)<exp(44/7)<(201/10)^2(4/3)<540. The degree-four polynomial at 14/25 equals 16407816/9375000>7/4. Therefore exp(4pi)>20^4(7/4)=280000, implying exp(2pi)>529 because 529^2=279841.
5. exp(18)>20^6(1+6/250)=65536000. The degree-four polynomial at 21/25 is 21678081/9375000>23/10. Since 6pi>18+21/25, the claimed exp(6pi) bound follows.
6. exp(10)>20^3(27/10), exp(8)>20^2(125/17), and exp(14)>20^4(125/17). For the upper bound, exp(14)<(201/10)^4(200/27)<164000(200/27)<1250000.
7. The positive series log((1+z)/(1-z))=2 sum_(k>=0)z^(2k+1)/(2k+1), with geometric remainder bounds, gives the logarithm enclosures. At z=1/3 the first two terms are 56/81 and the tail is below 1/540; at z=1/2 the first three terms are 263/240 and the tail is below 1/336.

For later use, 21/4<c_Gamma<571/105<11/2. A sufficient Euler lower bound is EulerGamma>1/2, from the strict trapezoidal inequality for 1/x. The harmonic remainder gives EulerGamma<H6-log6-1/14; H6=49/20 and log6>11581/6480>249/140 give EulerGamma<3/5. Combine with log pi<7/6, pi/2<11/7 and log2<7/10 for the upper c_Gamma bound. For the lower bound use log pi>9/8, pi/2>25/16 and log2>11/16. In turn log pi>9/8 follows from pi>25/8, log3>263/240 and log(25/24)>1/25.

## 4. Full theta envelopes and actual Fourier constants

Let S4(q)=sum_(n>=1)n^4 q^(n-1). Since n^2-1>=3(n-1), exp(3pi)>8000, and the tail ratio from n=2 is below 1/1000,

    S4(exp(-3pi))<101/100,
    4pi^2 S4(exp(-3pi))<40.

Thus on the real axis

    W(x)<80 exp(4|x|-pi exp(2|x|)),
    W(x)<40 exp((9/2)|x|-pi exp(2|x|)).

The second uses F0(x)<=exp(x/2) for x>=0; the first uses F0<=2. Both retain the entire positive theta tail. More precisely, with t=exp(2x)>=1,

    0<W(x)<F0(x)[40t^2-(75/4)t]exp(-pi t).

Only negative tail amplitudes were dropped, while the first negative amplitude -6pi t was retained and then enlarged to -(75/4)t.

For z=x+i/2, x>=0,

    |F0(z)|<=sec(1/4)exp(x/2),
    |4t_n^2-6t_n|<=4|t_n|^2.

The latter follows by squaring, since Re(t_n)>3/4. The alternating cosine bound gives cos(1)>27/50, hence d=pi cos(1)>27/16. Also exp(81/16)>(27/10)^5(17/16)>150, so exp(-3d)<1/150. The entire S4 tail is then below 1/8; for example the n>=3 geometric ratio is bounded even for exponent 8 by (4/3)^8/150<1/15. With sec(1/4)<32/31,

    |W(x+i/2)|<46 t^(9/4)exp(-dt), t=exp(2|x|),
    4pi^2 sec(1/4)S4(exp(-3d))<69696/1519<46.

Evenness and conjugation give both half-lines and both contour orientations. Define

    K=integral |W(x+i/2)|dx,
    J=integral |x+i/2|^2|W(x+i/2)|dx,
    K1=integral |(x+i/2)W(x+i/2)|dx.

After including BOTH real half-lines, t=exp(2|x|) gives dx=dt/t. Using t^(1/4)<=(t+3)/4 and log t<=(t-1)/sqrt(t), the polynomial integrals give

    K<(46/4)exp(-d)(4r+5r^2+2r^3),
    J<(46/16)exp(-d)(4r+5r^2+10r^3+6r^4), r=1/d<16/27.

The degree-four exponential polynomial at 27/16 is greater than 5. Substitution of r=16/27 therefore gives

    K<(23/10)(89408/19683)<21/2,
    J<(23/40)(3691968/531441)<4.

The final integer checks are 4112768<4133430 and 84915264<85030560. Cauchy-Schwarz yields K1^2<=KJ<42. Contour displacement in the sign appropriate to exp(-iux) consequently proves the actual envelopes

    F(u)^2<(441/4)exp(-|u|),
    F'(u)^2<42exp(-|u|).

No shape, unimodality, or sign assumption about F is used.

## 5. Source residual and moment certificates

### 5.1 Positivity of R=W''+20W and exact identities

For p(t)=P0(t)exp(-t) and L=2t d/dt,

    Lp=(-8t^3+28t^2-12t)exp(-t)<0, t>=pi,
    L^2p=(16t^4-104t^3+136t^2-24t)exp(-t).

The logarithmic derivative r=F0'/F0 lies in [0,1/2], and F0''/F0=r(2r-1)>=-1/8. Therefore

    R/F0 >= sum_(n>=1)[L^2p+Lp+(159/8)p](t_n)
          = sum_(n>=1)(t_n/4)B(t_n)exp(-t_n),
    B(t)=64t^3-448t^2+974t-621.

The expansion B(25/8+u)=7/8+49u+152u^2+64u^3 proves all terms of this lower bound positive. Consequently first-summand lower bounds for W and R can be multiplied without losing an adverse theta term.

Writing

    R0=integral WR,
    M_T=integral x^2 W^2,
    m_W=||W'||^2,
    m_T=||(xW)'||^2,
    R2=integral x^2 WR,

integration by parts gives exactly

    m_W=20M-R0>=0,
    m_T=integral x^2(W')^2=M+20M_T-R2.

In particular the tangent identity retains the term M. The two derivative moments must not be interchanged.

### 5.2 Lower M and the selected sharper upper M

The positive first summand and F0>=1 give

    M>=integral_pi^infinity (4t^2-6t)^2 exp(-2t)dt/t
      =exp(-2pi)(8pi^3-12pi^2+6pi+3)
      >9517/35200>27/100.

The polynomial is increasing for t>=3 and equals 9517/64 at 25/8; exp(2pi)<540<550 suffices for the stated certificate.

For the upper bound now use the DIFFERENT variable t=exp(2x)=1+u. The full-source upper envelope of section 4 gives

    M<integral_1^infinity (F0^2/t)[40t^2-(75/4)t]^2exp(-2pi t)dt.

The exact quotient is

    H(u)=F0^2/t=4/(sqrt(1+u)+1)^2
        =integral_0^1 integral_0^1 [(1+su)(1+vu)]^(-1/2)ds dv.

Every term of its third derivative has negative sign. Taylor's theorem at zero, using H(0)=1, H'(0)=-1/2 and H''(0)=5/8, therefore gives the GLOBAL bound

    H(u)<=1-u/2+5u^2/16, u>=0.

The quadratic is everywhere positive. Its product with the square in the integral is

    [115600+608600u+1098525u^2+764850u^3
      +218525u^4+187200u^5+128000u^6]/256.

All coefficients are positive. Exact monomial integration and 1/(2pi)<4/25, exp(2pi)>529 give M<(1/529) times the sum of these seven rational terms:

    289/4,
    3043/50,
    1098525/31250,
    4589100/390625,
    20978400/9765625,
    359424000/244140625,
    5898240000/6103515625.

The last five are below 141/4, 47/4, 43/20, 3/2, 1. The decisive cross products are

    4394100<4406250,
    18356400<18359375,
    419568000<419921875,
    718848000<732421875,
    5898240000<6103515625.

The seven simple upper bounds sum to 4619/25<185. Hence

    M<185/529<7/20, because 3700<3703.

This verifies the ceiling for the actual full source, not for a truncation or a numerical approximation.

### 5.3 Quantitative R0

Return to t=pi exp(2x), u=t-pi. The exact quotient obeys F0^2>=2t/(t+pi). Combining it with the positive first-summand bounds gives

    R0>integral_pi^infinity [tP0(t)/2]B(t)exp(-2t)/(t+pi)dt.

The factor follows from 2dx=dt/t and the factor t/4 in R: before inserting the quotient it is (1/4)F0^2 P0B. There is no extra factor 1/4 afterward.

Since pi>25/8,

    tP0(t)/2>31+39u+15u^2+2u^3,
    B(t)>49u+152u^2+64u^3.

Their product is

    Q(u)=1519u+6623u^2+8647u^3+4874u^4+1264u^5+128u^6.

The factorial formula integral u^k exp(-2u)du=k!/2^(k+1) gives

    Q0=integral Q exp(-2u)=96189/8,
    Q1=integral uQ exp(-2u)=224939/8.

For example the six Q0 numerators over 8 are 3038,13246,25941,29244,18960,5760; the Q1 numerators are 3038,19869,51882,73110,56880,20160. Both sums check.

The reciprocal is decreasing and convex. Jensen, pi<22/7 and exp(2pi)<540 give

    R0>L0=(1/540)Q0/(44/7+Q1/Q0)
          =7*96189^2/[4320*5806889].

Here 5806889=44*96189+7*224939. Since Q1/Q0<5/2,

    L0>1346646/531360>5/2,

with the last integer comparison 2693292>2656800. This is the selected actual lower bound. The auxiliary L0<13/5 is also true (Q1/Q0>7/3 and Q0<12024 suffice), but it is NOT an upper bound on actual R0 and is not needed by the final consumer.

### 5.4 R2 and M_T used by the restored tangent row

The same even substitution, quotient bound, and log(t/pi)>=2u/(t+pi) yield

    R2>(1/540)integral_0^infinity
          u^2 Q(u)exp(-2u)/(44/7+u)^3 du.

For the positive density u^2 Q(u)exp(-2u), its mass and first moment are 673050/8 and 2424429/8. The six mass numerators over 8 are 4557,39738,129705,219330,199080,80640; the first-moment numerators are 9114,99345,389115,767655,796320,362880. Its mean is below 26/7 because 16971003<17499300. Jensen for the decreasing convex reciprocal cube gives

    R2>336525/2160000=4487/28800>3/20.

For M_T, the actual first-summand reduction gives

    M_T>(1/540)integral q(u)exp(-2u)/(44/7+u)^3 du,
    q(u)=2u^2(25/8+u)^2(13/2+4u)^2
        =(105625/128)u^2+(6175/4)u^3+1047u^4+304u^5+32u^6.

Its raw moments Q_j=integral u^j q(u)exp(-2u)du are

    Q0=1188073/512, Q1=5908875/1024,
    Q2=9168795/512, Q3=67710615/1024.

About u=5/2 the centered moments are

    C1=-15745/512, C2=7288255/2048, C3=3842815/1024.

With a=123/14, the degree-three Taylor lower polynomial of the reciprocal cube integrates to

    Q0/a^3-3C1/a^4+6C2/a^5-10C3/a^6.

This polynomial is a global lower bound for u>=0: the fourth derivative is positive and the remainder contains (u-5/2)^4, also when u<5/2. Using Q0>2320, -C1>30, C2>3558, C3<3753 and 35/4<a<44/5 bounds the four signed terms below by

    17/5, 3/200, 2/5, -17/200.

For the last term, (35/4)^6>445000 and 37530/445000<17/200. Thus this part of M_T is greater than 373/54000.

Retaining also log(t/pi)^2>=4r^2[1+(2/3)r^2], r=u/(t+pi), adds at least

    (2/1620)integral q(u)u^2 exp(-2u)/(44/7+u)^5 du.

Its measure has mass Q2>17900 and mean Q3/Q2<37/10. Jensen and 44/7+37/10=699/70<10 bound this additional term below by 179/810000. Consequently

    M_T>2887/405000,
    (353/1000)M_T>503/200000,

where 353*2887=1019111>1018575=503*2025. The correction is a distinct positive logarithm term, not a repeated use of an already retained moment.

## 6. Gamma lower carrier and complete opposite-packet constants

### 6.1 The actual logarithmic approximation

Set b=t/2, x_j=j+1/4. The j-th term of g equals 1/x_j-x_j/(x_j^2+b^2). The finite identity

    sum_(j=0)^(N-1)1/(j+1/4)=2H_(4N)-H_(2N)+2L_(2N),
    L_(2N)=sum_(k=0)^(2N-1)(-1)^k/(2k+1),

and the harmonic/arctangent limits cancel EulerGamma+3log2+pi/2 exactly. Apply unit-cell midpoint integration to f_b(x)=x/(x^2+b^2), with cells beginning at -1/4, not zero. Its derivatives are

    f_b'=(b^2-x^2)/(x^2+b^2)^2,
    f_b''=2x(x^2-3b^2)/(x^2+b^2)^3.

For b>=1, total variation of f_b' on [-1/4,infinity) is 9/(4b^2)-f_b'(-1/4)<3/(2b^2), since b^2f_b'(-1/4)>=240/289>3/4. The midpoint Peano kernel is at most 1/8, so the error is below 3/(16b^2). Exact integration gives

    g(t)-c_Gamma>log[t/(2pi)]-3/(4t^2)=q(t), t>=2,
    |g(t)-c_Gamma-log[t/(2pi)]|<7/(8t^2), t>=2.

The latter includes the finite-start correction (1/2)log(1+1/(4t^2))<1/(8t^2). No scalar inequality is differentiated.

### 6.2 Whole-line parabola with an actual outer debit

For |u|<=10 and gamma>=14, both arguments are at least 4, and q is increasing. Thus h_gamma(u)>H(u^2), where

    H(z)=(1/4)log[(196-z)/(4pi^2)]
           -(3/8)(196+z)/(196-z)^2.

The center satisfies H(0)>393/1000, using log(49/22)>285336/357911>79/100 and 3/1568<1/500. The logarithm bound follows from the first two positive atanh terms with parameter 27/71. For 0<z<=100, the logarithmic loss divided by z is increasing and at most log(49/24)/400<3/1600; the degree-three exponential polynomial gives exp(3/4)>269/128>49/24. The rational loss divided by z is

    (3/8)(588-z)/[196(196-z)^2],

which increases on this interval and is at most 61/602112<1/8000. Therefore H(0)-H(z)<z/500.

Let d_gamma(u)=(3/10-h_gamma(u))_+. The outer layers are

    10<=|u|<=11: d_gamma<17/100;
    11<=|u|<=12: d_gamma<3/10;
    12<=|u|<=13: d_gamma<7/10;
    13<=|u|<57/2: d_gamma<31/20;
    |u|>=57/2: d_gamma=0.

The first two follow by q at endpoints: at u=11 the logarithm argument exceeds 3675/1936>15/8 and the inverse loss is 1902/90000<1/40, giving h>21/160>13/100; at u=12 use 637/484>13/10 and 510/10816<1/20 to get h>1/80. The required logarithms follow from log(15/8)>22904/36501>5/8 (two atanh terms at 7/23) and log(13/10)>6/23>1/4 (the first term).

For the remaining layers, the first five positive g(14) terms exceed 399/100,3/4,2/5,1/4,1/6. The decreasing integral tail exceeds log(5/3)>49/96, so g(14)>14561/2400. The first three terms of g(1) give g(1)>33/10. One argument is at least 24 outside ten, and the smaller argument is at least 1 on [12,13]; these prove the third and fourth layers with c_Gamma<571/105. Beyond 57/2 both arguments in absolute value are at least 14, and h>10567/33600>3/10. This explicitly handles the zero-argument neighborhood without applying a singular logarithm there.

Since the parabola 393/1000-u^2/500 is at most 193/1000<3/10 outside ten,

    h_gamma(u)>=393/1000-u^2/500-d_gamma(u)1_(|u|>10).

Integrating the layers against F'^2<42exp(-|u|) gives the full tangent outer debit

    D_outer < (42/pi)exp(-10)
      [17/100+(13/100)exp(-1)+(2/5)exp(-2)+(17/20)exp(-3)]
      <(7/10800)(6313/20000)
      =44191/216000000<41/200000.

Here exp(-1)<3/8, exp(-2)<17/125 and exp(-3)<1/20. Scaling this positive envelope by (441/4)/42=21/8 gives the cosine outer debit 861/1600000. The central parabola is not asserted on the whole line without these debits.

Consequently

    G_q>(353/1000)M+R0/500-861/1600000,
    G_T>(353/1000)M_T+R2/500-M/500-41/200000
       >1810/10^6+(2/5-M)/500.

The second expression follows from the actual M_T and R2 bounds BEFORE replacing M by a constant. This is the source of the retained M dependence in the tangent row.

### 6.3 Opposite-Gamma scalar brace

For 0<=t<=2 let g0(t)=4t^2/(1/4+t^2). The remaining positive series obeys

    0<=g-g0<=8[(5/2)^(-3)+(1/2)integral_(5/2)^infinity a^(-3)da]
             =104/125.

Thus g+g0<9<2c_Gamma and |g-c_Gamma|<=c_Gamma-g0. Exact integration gives integral_0^2|g-c_Gamma|dt<43/7. On [2,15], exact integration of |log(t/(2pi))| gives a value below 99/14, using log pi>1 and log(12/5)<9/10. The approximation remainder costs at most 7/16. On t=gamma+v, v>=0, the exponentially weighted exterior is bounded by integrating 9/10+v/14+1/224, whose integral against exp(-v) is below 1. Thus the complete brace is below

    43/7+99/14+7/16+1=1641/112<15.

The Fourier products have the exact envelope exp[-max(gamma,|xi|)]. Evenness and the prefactors in section 2 then give

    |R_T|<42*15 exp(-gamma)/(2pi)<90/10^6,
    |R_q|<(441/4)*15 exp(-gamma)/(2pi)<235/10^6,
    |R_cross|<K K1*15 exp(-gamma)/(2pi)<146/10^6.

For the last bound use K<21/2, K1<13/2 and exp(14)>20000000/17; its rational coefficient is 4641/32<146 in millionths. The other two coefficients are 89.25<90 and 37485/160<235 in millionths. These are disjoint opposite-packet costs, not substitutions for carrier errors.

## 7. Complete prime budgets and the lifted low-prime constraints

### 7.1 Positive midpoint-product majorant

For the tangent midpoint term shift the positive exponential exp(2i gamma y) upward by i/2. The conjugate exponential shifts downward and has the same bound; averaging them introduces no extra factor two. With z=y+i/2 and s=log n, the positive integrand is

    |z-s/2||z+s/2||W(z-s/2)W(z+s/2)|.

Centrally, the full 46-envelope and the Gaussian integral bound its integral by

    1058 sqrt(pi/d)n^4 exp(-2dn)
       [(1+s^2)/4+1/(8dn)].

Use sqrt(pi/d)<3/2, log^2 n<n, and the bracket<n/2. Also Lambda(n)/sqrt(n)<=log n/sqrt(n)<1. The weighted central sum is below

    (1587/2)sum_(n>=2)n^5 exp(-27n/8)<45.

Indeed exp(27/8)>20(1+3/8+(3/8)^2/2)=925/32, whose square exceeds 800. The weaker exp(27/8)>55/2 bounds the successive ratio by 243/880<2/7; the resulting rational upper bound is 44.436.

On the two outer half-lines y=+/-s/2+/-v, v>=0, let A_n=2d(n^2+1)-9>(15/8)n^2. The two positive integrals together are at most

    4232n^(9/2)exp[-d(n^2+1)]
      [2/A_n^3+(s+1)/A_n^2+(s/2+1/4)/A_n].

Since s+1<=n and s/2+1/4<=3n/8, the bracket is below 2/(7n). To check this uniformly, multiply the resulting upper bound by n and maximize at n=2: it is 947/3375<2/7. The weighted exterior sum is therefore below

    1210sum_(n>=2)n^4 exp[-27(n^2+1)/16]<5.

Its first term is below 121/25 using exp(135/16)>2900(23/16)>4000; its ratio is below 81/64000<1/500, giving 2420/499<5. Thus the COMPLETE tangent midpoint sum has absolute value below 50exp(-gamma)<50/10^6.

For the cross midpoint, put A=|z-s/2| and B=|z+s/2|. Since A,B>=1/2,

    |z|<=(A+B)/2<=2AB.

Its positive majorant is at most twice the tangent majorant, giving 100/10^6. For the cosine midpoint the omitted tangent product is at least 1/4, giving 200/10^6. These comparisons are of nonnegative contour majorants, not of signed oscillatory integrals.

### 7.2 All n>=4 carriers, with the unsigned transfer checked

The real 80-envelope gives central A(log n)<=3200n^(7/2)exp(-2pi n). Multiplying by (log n)/2 and the prime weight, and using log n<n, gives the positive weighted cross-tail central majorant

    1600sum_(n>=4)n^5exp(-2pi n)<27/10^6.

Use exp(2pi)>500; the successive ratio is at most (5/4)^5/500<1/160. The first term and geometric sum give exactly the source's bound 1600*1024*160/(500^4*159)<27/10^6.

The two spatial exteriors for A(log n) are at most

    12800n^4 exp[-pi(n^2+1)]/[2pi(n^2+1)-8].

The denominator exceeds 5n^2. Multiplication by (log n)/2 and the prime weight bounds the positive cross exterior by 1280n^3exp[-pi(n^2+1)]. Its first term is below 81920exp(-51), and its ratio is below 2exp(-27)<1/2, so its sum is below 1/10^6. Thus the proof establishes the genuinely UNSIGNED inequality

    sum_(n>=4)[(log n)/2]Lambda(n)A(log n)/sqrt(n)<28/10^6.

For n>=4, (log n)/2>=log2>2/3. Division of this positive majorant, not of a signed sine sum, proves

    sum_(n>=4)Lambda(n)A(log n)/sqrt(n)<42/10^6.

For the tangent carrier, centrally the positive bound is

    3200n^(7/2)exp(-2pi n)[1/(8pi n)+(log n)^2/4]
      <(3200/3)n^(9/2)exp(-2pi n).

The same ratio test gives a sum below 18/10^6. On the two spatial exteriors the multiplier is v^2+s v; integration and the denominator>5n^2 bound the coefficient by 1024/(5n^2)+512log n<525n. Its complete tail is below 4200exp(-51)<1/10^6. Thus the tangent n>=4 carrier costs below 19/10^6. Every prime power is included in all these convergent all-integer majorants.

### 7.3 Full-source A(log2) and A(log3)

The sharper A(log2) upper bound preserves the entire positive theta amplitude. Let delta=S4(exp(-3pi))-1>=0. For x>=0 the full-source upper envelope is

    W(x)<F0(x)exp(4x-pi exp(2x))4pi^2[1-3/(2t_1)+delta].

On |y|<=s/2, s=log2, let t_-=2pi exp(-2y), t_+=2pi exp(2y). With M_+=1-3/(2t_+) and M_-=1-3/(2t_-), both positive,

    M_-M_+<=(1-3/(4pi))^2,
    M_-+M_+<=2(1-3/(4pi)).

The nonnegative delta therefore keeps all main/tail cross terms in the central amplitude bound (4pi^2 S4-3pi)^2. The exact quotient product is at most 8(3-2sqrt2). Gaussian integration gives the central bound

    32(3sqrt2-4)(4pi^2 S4-3pi)^2 exp(-4pi).

Using sqrt2<99/70 and pi>157/50, its coefficient is below (272/35)(4676/5)=181696/25. The outer bound from the full 40-envelope is

    [51200sqrt2/(10pi-9)]exp(-5pi).

Its ratio to 12800exp(-4pi) is below 1/70. With exp(-4pi)<9/2500000, the two parts are below 262/10000 and 7/10000. Therefore

    0<A(log2)<269/10000<27/1000.

For n>=2 the same 40-envelope directly gives

    A(log n)<800n^4exp(-2pi n)
      +[3200n^(9/2)/(2pi(n^2+1)-9)]exp[-pi(n^2+1)].

At n=3 the first term is below 43/100000 by exp(6pi)>150732800; the two exteriors together are below 9000/20^10<1/10^9. Hence A(log3)<431/10^6.

The n=3 phase satisfies -313/840<gamma log3-5pi<13/40, so its cosine is negative throughout the band. Its cosine carrier is favorable and may be discarded. For the tangent, discard only Y(log3)>0, obtaining the adverse bound

    P_T,3>-(1/5)A(log3)>-431/5000000,

because (log3)^3/(4sqrt3)<3993/20000<1/5. For the cross use the absolute bound

    |P3|<(1331/3800)(431/10^6)<151/10^6,

using sqrt3>19/11; 573661<573800 is the exact comparison. The n=3 sine is NOT assumed to have one sign throughout the band.

### 7.4 The phase-free n=2 negative-part certificate

Let s=log2, d=s/2 and N2=integral_(|y|<=d)(d^2-y^2)U_s(y)dy. The full-source envelope retaining the first negative theta amplitude gives centrally

    U_s(y)<=sqrt2 exp(-4pi)(C0-D0y^2)exp(-lambda y^2),
    C0=60025/4, D0=24000, lambda=8pi.

Indeed the product amplitude is 108025/4-12000cosh(2y)<=C0-D0y^2. Both this polynomial and d^2-y^2 are nonnegative on the integration interval; the signed polynomial is not extended to the whole line.

For J0=integral_(-d)^d(d^2-y^2)(C0-D0y^2)exp(-lambda y^2)dy, integration by parts gives

    J0=A0 I0+B0 exp(-lambda d^2),
    I0=integral_(-d)^d exp(-lambda y^2)dy,
    A0=C0d^2-(C0+D0d^2)/(2lambda)+3D0/(4lambda^2),
    B0=C0d/lambda-3D0d/(2lambda^2).

Both coefficients are positive. With 28/81<d<25/72 and 25<lambda<176/7,

    C0d^2<1810, D0d^2>2856,
    (C0+D0d^2)/(2lambda)>355, 3D0/(4lambda^2)<29.

Thus A0<1484 and I0<=1/sqrt8<5/14, giving A0I0<530. The bracket defining B0 decreases with lambda>=25, so B0<(7/20)[15010/25-72000/(2*25^2)]<190. Also lambda d^2>59/20 and exp(59/20)>19, giving the boundary term<10. Hence J0<540.

The exact real quotient improves the preceding sqrt2 coefficient by a factor

    8/(4+3sqrt2)<34/35,

using sqrt2>24/17. Therefore, with omega=s/sqrt2,

    omega N2<(25/36)(34/35)(540/280000)=51/39200=:K2.

Since the exterior part of Y-d^2A is nonnegative,

    omega(Y-d^2 A)>-K2.

This certificate already includes the central positive y^2 contribution. It cannot be given an additional independent refund of that same contribution.

### 7.5 The separate actual Y lower bound

For |y|<=1/5, the two real source arguments are positive after evenness since s/2>1/3. Retain only their positive first theta summands and F0>=1. With a=2pi>6,

    P0(a exp(-2y))P0(a exp(2y))
      =a^2[16a^2-48a cosh(2y)+36].

The positive cosh series gives cosh(2y)<=25/23<11/10. The resulting lower polynomial in a is increasing on a>=6 and at 6 equals 53136/5. Also t_-+t_+<484/35<14. Thus

    U_s(y)>53136/6250000, |y|<=1/5,
    Y> (53136/6250000)(2/375)=106272/2343750000.

Since omega>4/9, the actual variable Z=omega Y satisfies

    Z>425088/21093750000>1/50000=:Zmin.

This and Z-beta A>-K2, beta=omega d^2, are simultaneous source constraints. They are retained geometrically, not summed as two separate credits in b.

## 8. Independent actual positive sign of c

The exact cross decomposition from sections 2 and 7 is

    c=D_gamma+P2+P3+E,
    |E|<(146+100+28)/10^6=274/10^6.

A positive upper surrogate for c would not establish c>0. The actual sign follows separately as follows.

For f_t(a)=4at/(a^2+t^2)^2, the exact left-cell quadrature on [a_j,a_j+2] has error -integral w_j f_t', with 0<=w_j<=1. For t>=1 the peak is at a=t/sqrt3>1/2, so its positive variation gives

    g'(t)>=(1/2)integral_(1/2)^infinity f_t
             -max f_t+f_t(1/2).

Here the three values are t/(t^2+1/4), 9/(4sqrt3 t^2), and 2t/(t^2+1/4)^2. The finite-start correction satisfies

    t/(t^2+1/4)+2t/(t^2+1/4)^2-1/t
      =[(7/4)t^2-1/16]/[t(t^2+1/4)^2]>0.

Hence g'(t)>1/t-3/(2t^2), t>=1.

For |u|<=10 and z=u^2, average this lower bound at gamma+u and gamma-u. The resulting expression

    L_gamma(z)=gamma/(gamma^2-z)
                -(3/2)(gamma^2+z)/(gamma^2-z)^2

has z-derivative numerator gamma^2(gamma-9/2)-(gamma+3/2)z>=1862-1600=262>0. Its minimum over the band and central interval is therefore L_(29/2)(0)=52/841.

The full Fourier tail gives central mass

    integral_(-10)^10 F^2 dmu>27/100-147/80000>67/250.

For the ENTIRE negative packet use the global bound g'<6. This follows directly from max_(t>=0)4at/(a^2+t^2)^2=9/(4sqrt3 a^2) and sum a_j^(-2)<=109/25, giving g'<2943/500<6. Its complete negative-packet cost is below 441/16000000. Consequently

    D_gamma>(1/4)(52/841)(67/250)-441/16000000
           =871/210250-441/16000000>1/250.

Indeed 871/210250-1/250=3/21025 and 441*21025<3*16000000.

For delta2=gamma log2-3pi,

    1/4<delta2<1169/1800,
    P2>-(7/40)(27/1000)(1169/1800)=-73647/24000000.

The coefficient bound is (log2)^2/(2sqrt2)<7/40. For n=3, gamma log3>4pi and gamma log3-5pi<1/4. Its sine is nonnegative below 5pi, and greater than -1/4 above 5pi. Thus

    P3>-(10/27)(431/10^6)(1/4)=-431/10800000.

The full signed result is therefore

    c>1/250-73647/24000000-431/10800000-274/10^6
      =133373/216000000>3/5000.

The common-denominator numerator is 864000-662823-8620-59184=133373, exceeding 129600. This proof retains the complete negative Gamma packet and all adverse residuals. It neither differentiates a bound for a nor infers a sign from c_bar.

## 9. New midpoint derivative bound and affine D_gamma upper row

### 9.1 Exact midpoint lemma with coefficient 5/4

For a C^2 function on [c-1,c+1], the exact cell-average identity is

    f(c)-(1/2)integral_(c-1)^(c+1) f(a)da
      =-integral_(c-1)^(c+1) K_c(a)f''(a)da,
    K_c(a)=(1-|a-c|)^2/4.

The nonnegative kernel has maximum 1/4 and integral 1/6. For f(a)=a^2 it gives -1/3, checking the normalization.

For f_t(a)=4at/(a^2+t^2)^2,

    f_t'=4t(t^2-3a^2)/(a^2+t^2)^3,
    f_t''=48at(a^2-t^2)/(a^2+t^2)^4.

The cells centered at a_j=2j+1/2 partition [-1/2,infinity). For t>=1/2, f_t''>=0 on [-1/2,0], is negative on (0,t), and nonnegative beyond t. Thus the complete upper error is at most

    (1/4)integral_0^t(-f_t'')da
      =(1/4)[f_t'(0)-f_t'(t)]=5/(4t^3).

The first negative-a half-cell is accounted for. Since f_t=O(a^-3) and f_t''=O(a^-5), finite-cell summation passes to an absolutely convergent limit. Exact integration gives

    (1/2)integral_(-1/2)^infinity f_t=t/(t^2+1/4).

Therefore

    g'(t)<=t/(t^2+1/4)+5/(4t^3)<1/t+5/(4t^3), t>=1/2.

Nothing here proves or uses the coefficient 1 in place of 5/4.

### 9.2 Symmetric central packet and safe rounding

For an UPPER bound discard only the nonpositive second packet in D_gamma. On |u|<=8, evenness of F^2 allows the average at gamma+u and gamma-u; both arguments are at least 6. With v=u^2,

    average < gamma/(gamma^2-v)
       +(5/4)gamma(gamma^2+3v)/(gamma^2-v)^3.

Subtracting the constant terms gives

    gamma/(gamma^2-v)<=1/gamma+v/[gamma(gamma^2-64)],
    gamma(gamma^2+3v)/(gamma^2-v)^3-1/gamma^3
      =v(6gamma^4-3gamma^2v+v^2)/[gamma^3(gamma^2-v)^3]
      <=6gamma v/(gamma^2-64)^3.

The numerator comparison uses v<=64<3gamma^2. The coefficients decrease with gamma; in particular the derivative of gamma/(gamma^2-64)^3 is -(5gamma^2+64)/(gamma^2-64)^4. Evaluation at gamma=14 gives

    average < alpha+eta u^2,
    alpha=789/10976,
    eta=1/1848+105/2299968.

Extending this nonnegative polynomial integral to the whole real line yields

    D_central<(alpha M+eta m_W)/4.

Now, and only now, use alpha<9/125, eta<3/5000, M>=0 and m_W>=0, then substitute m_W=20M-R0:

    D_central<21M/1000-3R0/20000.

It would be invalid to enlarge the negative R0 coefficient in isolation. The selected proof does not do so.

### 9.3 Both exterior regions, including the moving left endpoint

Let r(t)=1/t+5/(4t^3) for t>=1, and let H(t)=6 for t<1, H(t)=r(t) for t>=1. This is a nonincreasing positive majorant of g' on t>=0. The left exterior, after v=gamma-xi, obeys

    integral_0^(gamma-8)g'(xi)exp(xi-gamma)dxi
      <=integral_8^gamma H(gamma-v)exp(-v)dv
      <=integral_8^infinity H(14-v)exp(-v)dv.

This handles the moving endpoint rather than replacing gamma-8 by 6. The extension to negative arguments is only a majorant device. On [1,2],...,[5,6], use r(1),...,r(5)=9/4,21/32,41/108,69/256,21/100. Integration and telescoping give

    (15/4)e^-13+(51/32)e^-12+(239/864)e^-11
      +(761/6912)e^-10+(381/6400)e^-9+(21/100)e^-8.

The right exterior has xi>=22 and contributes at most r(22)e^-8, where r(22)=1941/42592. Since K^2/(8pi)<147/32, all exterior contributions together are below

    E_star=(147/32)[15/(4*432000)+51/(32*160000)
      +239/(864*58320)+761/(6912*21600)
      +381/(6400*8000)+21/(100*2900)
      +1941/(42592*2900)].

The exponential denominators follow from section 3. The seven bracket terms lie between consecutive millionths with lower numerators 8,9,4,5,7,72,15. Thus

    (147/32)(120/10^6)<E_star<(147/32)(127/10^6),
    1/2000<E_star<3/5000.

The lower statement is only about this certificate constant, not about an actual positive exterior contribution. We obtain the complete selected affine bound

    D_gamma<21M/1000-3R0/20000+3/5000.

## 10. Uniform phases and the three conservative entry rows

The more precise atanh bound needed now is

    log2<842/1215+1/6804=23581/34020<1733/2500.

The final integer comparison is 58952500<58956660. For delta=gamma log2-3pi,

    delta>14*(56/81)-66/7=142/567>1/4,
    delta<(29/2)*(1733/2500)-3*(157/50)=3157/5000.

Hence, throughout the entire band, with C=-cos(gamma log2)=cos delta and S=-sin(gamma log2)=sin delta,

    4/5<C<97/100,
    S>95/384.

Indeed 3157^2=9966649<10000000, and cos delta>1-delta^2/2>4/5. Also sin(1/4)>95/384 and cos(1/4)<5953/6144<97/100.

With omega=log2/sqrt2 and d=log2/2,

    omega>196/405>12/25,
    omega d>21952/131220>1/6,
    omega C>3/8,
    omega d S>1/25.

These follow from sqrt2<10/7 and log2>56/81; the last comparison is 2375>2304. They are simultaneous uniform inequalities, not a combination of incompatible favorable endpoint phases.

The exact cosine losses from sections 6-7 add to

    Ca=861/1600000+235/10^6+200/10^6+42/10^6
      =8121/8000000.

Retaining the n=2 cosine carrier, using R0>5/2, and discarding favorable n=3 gives

    a>a_bar=(353/1000)M+1/200+(3/8)A-Ca,
    A=A(log2).

The cross error is 274/10^6 and the absolute n=3 contribution is below 151/10^6. The new D upper bound and the exact negative n=2 cross carrier therefore give

    0<c<c_bar=(21/1000)M+13/20000-A/25.

The intercept is precisely -3(5/2)/20000+3/5000+425/10^6=13/20000. The actual positive sign on the left comes from section 8, not from c_bar.

For the tangent, its non-n=2 losses are

    (90+50+19)/10^6+431/5000000
      =1226/5000000<246/10^6.

Retaining the exact n=2 contribution and the restored M dependence gives

    b>b_under=B(M)+C(Z-beta A),
    B(M)=1564/10^6+(2/5-M)/500,
    Z=omega Y(log2), beta=omega d^2=(log2)^3/(4sqrt2).

This is not obtained by assigning the separate scalar tangent margin to arbitrary fictitious A,Y corners. Its M dependence is derived from the actual Gamma carrier, and its retained low-prime term is constrained as in section 7.

## 11. Lifted geometry and all six exact rational corner checks

The actual source belongs to the relaxed set

    27/100<=M<=7/20,
    0<=A<=27/1000,
    Z>=Zmin=1/50000,
    Z>=beta A-K2, K2=51/39200.

Allowing A=0 is merely a relaxation. From log2>2/3 and sqrt2<3/2,

    beta>4/81.

For the upper bound use the sufficiently sharp pair log2<25/36 and sqrt2>7/5:

    beta<78125/1306368<3/50.

The rougher pair log2<7/10 and sqrt2>7/5 would not by itself prove this upper constant.

On the entire M,A rectangle,

    a_bar>9/100,
    c_bar>= (21/1000)(27/100)+13/20000-(27/1000)/25
           =131/25000>0.

For each fixed gamma, C and beta are constants. Define

    S_bar=B(M)+C(Z-beta A)-c_bar^2/a_bar.

Square-over-positive-linear is convex (equivalently -c_bar^2/a_bar is the infimum over t of a_bar*t^2-2c_bar*t). Hence S_bar is jointly concave in M,A,Z. Its Z derivative is C>0, so first reduce to

    Z=max(Zmin,beta A-K2).

The kink is Astar=(Zmin+K2)/beta. It satisfies

    Astar>(1/50000+13/10000)/(3/50)=11/500,
    Astar<27/1000.

For the upper location, beta*(27/1000)>1/750 while Zmin+K2<133/100000<1/750. Each lower-boundary piece is an affine line segment, whose product with the M interval is a rectangle under an affine parametrization. Concavity reduces these two rectangles to six distinct vertices: A=0, A=Astar and A=27/1000, each at the two M endpoints. Upward Z rays cannot lower the value.

This is a fixed-gamma convex-geometric argument followed by UNIFORM estimates of the six vertex values. It is not a claim that a gamma-dependent minimum occurs at a band endpoint.

### 11.1 A=0, both M endpoints

Here Z=Zmin and CZmin>0. Discard that favorable term; do not replace its C by an upper bound. We have

    a_bar>9/100,
    c_bar<=1/125,
    b_under>B(M)>=1664/10^6>1/625.

Therefore

    S_bar>1/625-(1/125)^2/(9/100)=1/1125>1/62500.

### 11.2 M=7/20, A=Astar or A=27/1000

At BOTH vertices Z-beta A=-K2. Only after this reduction may C<97/100 be used on the negative value, giving

    CK2<1262/10^6,

because 4947000000<4947040000. Since A>=Astar>11/500,

    a_bar>(353/1000)(7/20)+1/200+(3/8)(11/500)-8121/8000000
          =1086279/8000000>27/200,
    c_bar<(21/1000)(7/20)+13/20000-(11/500)/25
          =89/12500<9/1250,
    b_under>1664/10^6-1262/10^6=402/10^6>1/2500.

The same bounds cover the right endpoint because increasing A increases a_bar and decreases the still-positive c_bar. Consequently

    S_bar>1/2500-(9/1250)^2/(27/200)
          =1/2500-6/15625=1/62500.

Strictness is retained; no margin is inferred from rounded decimal evaluation.

### 11.3 M=27/100, A=Astar or A=27/1000

The same sign handling gives

    a_bar>860359/8000000>1/10,
    c_bar<136/25000<3/500,
    b_under>1824/10^6-1262/10^6=562/10^6>1/2000.

Hence

    S_bar>1/2000-(3/500)^2/(1/10)=7/50000>1/62500.

All six vertices are strictly above the selected constant. Concavity on each boundary rectangle and monotonicity in Z therefore prove

    S_bar>1/62500

throughout the relaxed feasible set for every gamma in the closed band.

## 12. Passage to the actual Schur complement and scope conclusion

At the actual source we have proved

    a>a_bar>0, b>b_under, 0<c<c_bar.

The positive actual cross sign is essential to the simple squared comparison:

    c^2/a<c_bar^2/a_bar,
    b-c^2/a>b_under-c_bar^2/a_bar>1/62500.

This is an actual Schur-complement lower bound. It does not require, and does not assert, a Loewner-order lower bound from the three entrywise surrogate inequalities. For real coefficients r,t the exact form completes as

    Q_inv(rq+tv)=a(r+(c/a)t)^2+(b-c^2/a)t^2.

Both coefficients are strictly positive. The two modes are independent: at x=0 the cosine mode is nonzero and the tangent mode is zero, while the tangent mode is not identically zero for gamma in this band.

The historical failed corner in the primary proof used M=2/5 and the old much larger cosine-tail debit. Its calculation S_old<-13/3200000 is a negative value of a LOWER SURROGATE, not an upper bound on the actual Schur complement. The new actual ceiling M<7/20 excludes that corner, and the unsigned cosine-tail bound independently improves the diagonal. Thus there is no contradiction between that historical failure and the present positive proof.

This proves precisely the physical same-frequency two-mode theorem with selected margin 1/62500. No larger theorem, optimized constant, original-domain bridge, arbitrary root-pair statement, or RH conclusion is certified here.
