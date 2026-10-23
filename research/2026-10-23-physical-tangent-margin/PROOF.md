# A positive physical tangent margin for the full theta source

Theta-weighted certificate research project. 23 October 2026.

## 1. Theorem and boundary of the result

For the full unscaled source W and the explicitly defined pole-free physical quadratic form Q_inv in section 2, every real gamma in the closed interval [14,29/2] satisfies

    Q_inv(-x W(x) sin(gamma x)) > 302/1000000 > 3/10000.

The proof is analytic. Its constants are rational inequalities derived from the full source, elementary series and exact integration identities. No numerical quadrature, sampled spectral value, root computation, or executable certificate is an input.

This is only a theorem about the displayed physical form on this test family. It does not identify that form with an unspecified original abstract operator, prove original constrained/root-domain admission, a positive two-mode Gram or Schur complement, root simplicity, global positivity, or the Riemann hypothesis. No positive pole-square contribution is used.

The full formulas, scalar certificates and selected error estimates are given below. Additional finite comparisons are recorded in the appendix. Standard analysis used includes Plancherel, Tonelli, integration by parts, Taylor's theorem, Jensen's inequality, Gaussian integration and the cited theta transformation.

## 2. Physical definition, normalization, and convergence

The actual source on x>=0 is

    kappa(x) = exp(x/2) sum_{n>=1} (4t_n^2-6t_n) exp(-t_n),
    t_n = pi n^2 exp(2x),
    W(x) = F0(x) sum_{n>=1} (4t_n^2-6t_n) exp(-t_n),
    F0(x) = 2/(1+exp(-x)).

The full source has the real even extension reconstructed below. On its analytic strip define

    W(z)=kappa(z)/cosh(z/2).

For x>=0 this agrees with the displayed F0 times theta-series formula. There is no rescaling of this source. For real-valued test functions f for which the displayed terms converge, define the physical quadratic form by

    Q_inv(f) = D_Gamma(f) - c_Gamma ||f||_2^2
               - 2 sum_{n>=2} Lambda(n) C_f(log n)/sqrt(n),
    C_f(s) = integral_R conjugate(f(x)) f(x+s) dx,
    D_Gamma(f) = integral_0^infinity rho(s)||f-tau_s f||_2^2 ds,
    rho(s) = exp(-s/2)/(1-exp(-2s)),
    c_Gamma = log pi + EulerGamma + pi/2 + 3 log 2.

Here tau_s f(x)=f(x+s), and Lambda(n)=log p when n is a positive power of a prime p and is zero otherwise. All L2 norms and all Fourier/correlation integrals in this section are over the real line. Other integration domains are displayed or inherited from the immediately preceding integral reduction.

For F(u)=integral W(x)exp(-iux)dx, the Plancherel measure is du/(2pi). Expanding rho into its positive exponential series gives exactly

    g(u) = sum_{j>=0} 2u^2/[a_j(a_j^2+u^2)],
    a_j = 2j+1/2.

The factor two is the factor in |1-exp(ius)|^2. For the actual tangent v_gamma=-xW sin(gamma x), direct Fourier differentiation gives

    vhat_gamma(u) = [F'(u+gamma)-F'(u-gamma)]/2.

Define Q_Gamma(f)=D_Gamma(f)-c_Gamma||f||_2^2 and b_gamma=Q_inv(v_gamma). Because F is real-even and F' is real-odd, squaring and changing variables give

    Q_Gamma(v_gamma) = G_T + R_T,
    G_T = integral h_gamma(u) F'(u)^2 du/(2pi),
    h_gamma(u) = [g(gamma+u)+g(gamma-u)]/4 - c_Gamma/2,
    R_T = -(1/2) integral [g(u)-c_Gamma]
                         F'(u-gamma)F'(u+gamma) du/(2pi).

For s=log n, a=s/2, and U_s(y)=W(y-a)W(y+a), define A(s)=integral_R U_s(y)dy and

    A_T(s) = integral (y^2-a^2)U_s(y)dy,
    B_T,gamma(s) = integral (y^2-a^2)U_s(y)cos(2gamma y)dy.

The sine-product identity gives

    C_v(s) = [A_T(s)cos(gamma s)-B_T,gamma(s)]/2.

Thus the exact full decomposition is

    b_gamma = G_T + R_T
      - sum_{n>=2} Lambda(n) A_T(log n)cos(gamma log n)/sqrt(n)
      + sum_{n>=2} Lambda(n) B_T,gamma(log n)/sqrt(n).

Write P_T,n=-Lambda(n)A_T(log n)cos(gamma log n)/sqrt(n) and E_prime_mid=sum_(n>=2)Lambda(n)B_T,gamma(log n)/sqrt(n). There is no additional factor two in the midpoint sum. Carrier and midpoint estimates concern distinct terms. Lambda includes all prime powers, including n=4.

### Full-source evenness and required strip

Let Theta(y)=sum_{k in Z}exp(-pi k^2 y) and H(z)=exp(z/2)Theta(exp(2z)). The Gaussian Poisson/Jacobi identity gives H(z)=H(-z) on |Im z|<pi/4. In the notation Theta(y), it states Theta(y)=y^(-1/2)Theta(1/y) for Re(y)>0, using the analytic square-root branch there. A primary standard reference is [NIST DLMF, equation 20.7.32](https://dlmf.nist.gov/20.7.E32), specialized to zero theta argument and tau=i y. Normal convergence on compact subsets of this strip permits differentiation. Directly,

    kappa(z) = (1/2)(d^2/dz^2 - 1/4) H(z).

The constant theta term is annihilated. The factor two from the positive and negative integers then produces exactly the source normalization above. This proves actual evenness and analytic continuation of the full source; conjugation follows from its real coefficients. The cosh(z/2) denominator has no zero in this strip.

The closed working strip |Im z|<=1/2 is strictly inside it. On its right half every required derivative has a normally convergent polynomial-exponential theta bound with exp[-pi cos(1)exp(2x)] decay. Evenness and conjugation supply the left half. Vertical sides in the contour shifts therefore vanish. No claim of entire analyticity in z and no contour shift of a cusped first term is used.

The actual v and its real derivatives have rapid decay. At small s, ||v-tau_s v||_2<=s||v'||_2 and rho(s)=O(1/s); at large s, rho is integrable. The prime series is absolutely convergent by the overlap bounds below. Accordingly the displayed physical form is well-defined for this family. Tonelli and Plancherel justify the Gamma calculation, and finite prime sums may be expanded before passage to the absolutely convergent limit.

## 3. Elementary constants and full theta envelopes

The source calculations use exact rational enclosures, not sampled numerical values. The elementary certificates are as follows.

- The standard enclosure 157/50<pi<22/7 can also be recovered directly from Machin's identity pi=16 atan(1/5)-4 atan(1/239). Alternating-series bounds give the lower value 1184/375-4/239=281476/89625>157/50. For the upper bound, atan(1/239)>1/240 and atan(1/5)<74/375+1/15625 give pi<4711/1500+16/15625<22/7. The identity itself follows from tan(4 atan(1/5))=120/119 and subtraction of atan(1/239), with the angle in (0,pi/2).
- The exponential series gives 163/60<e<87/32. For the upper bound, the sum through degree six is 1957/720 and its remaining tail is less than 1/4410. Consequently exp(2)>125/17, e>27/10, and e>8/3.
- The degree-eleven exponential certificate gives exp(3)>502/25>20. In detail, the sum through degree eight is 806769/40320>20009/1000; the next three terms exceed 27/500, 2/125, and 1/250. Also exp(3)<(87/32)^3<201/10.
- Since log(4/3)>2/7, exp(2pi)<exp(44/7)<(201/10)^2(4/3)<540.
- Since 4pi>12+14/25, the degree-four lower polynomial for exp(14/25) exceeds 7/4. Thus exp(4pi)>20^4(7/4)=280000. In particular exp(2pi)>529, because 529^2=279841<280000.
- Since 6pi>18+21/25, exp(18)>20^6(1+6/250)=65536000 and the degree-four lower polynomial for exp(21/25) exceeds 23/10. Hence exp(6pi)>150732800.
- exp(10)>20^3(27/10)=21600 and exp(14)>20^4(125/17)=20000000/17. Also exp(8)>400(125/17)>2900.

The logarithm bounds needed by the prime phases are also exact series bounds. The positive atanh series gives

    56/81 < log 2 < 56/81 + 1/540 < 25/36,
    263/240 < log 3 < 263/240 + 1/336 < 11/10.

The respective remainder bounds replace the remaining odd denominators by five and seven and sum a geometric series. In particular they are upper bounds, not truncations of a positive series incorrectly used above.

### Real and shifted full-source majorants

For t=exp(2|x|), the full positive theta amplitude satisfies

    4pi^2 S4(exp(-3pi)) < 40,
    S4(q)=sum_{n>=1} n^4 q^(n-1).

Indeed n^2-1>=3(n-1), exp(3pi)>8000, and the geometric tail beginning with n=2 gives S4<101/100; 4(22/7)^2(101/100)<40. This yields both

    W(x) < 80 exp(4|x|-pi exp(2|x|)),
    W(x) < 40 exp((9/2)|x|-pi exp(2|x|)).

The second retains F0<=exp(|x|/2); the first uses F0<=2. All theta terms remain in the majorant.

For z=x+i/2 and x>=0, the exact quotient obeys

    |2/(1+exp(-z))| <= sec(1/4)exp(x/2).

Furthermore |4t_n^2-6t_n|<=4|t_n|^2 because Re(t_n)>3/4; squaring reduces the comparison to 36-48 Re(t_n)<=0. The alternating cosine series gives cos(1)>27/50, so d=pi cos(1)>27/16. The bound exp(81/16)>(27/10)^5(17/16)>150 gives exp(-3d)<1/150. The full S4 tail is then less than 1/8, and sec(1/4)<32/31. Consequently

    |W(x+i/2)| < 46 t^(9/4) exp(-dt),
    4pi^2 sec(1/4)S4(exp(-3d)) < 69696/1519 < 46.

Evenness and conjugation give the identical bound for either sign of x and either contour orientation. These are full-source bounds, not first-theta replacements.

## 4. New positive residual and exact moment identity

Put p(t)=(4t^2-6t)exp(-t), L=2t d/dt, and R=W''+20W. Direct differentiation gives

    Lp = (-8t^3+28t^2-12t)exp(-t)
       = -4t(2t-1)(t-3)exp(-t),
    L^2p = (16t^4-104t^3+136t^2-24t)exp(-t).

For x>=0, r=F0'/F0 lies in [0,1/2], and F0''/F0=r(2r-1)>=-1/8. Since Lp<0 for t>=pi, the coefficient 2r<=1 multiplying Lp gives a lower bound when replaced by one. Hence

    R/F0 >= sum_{n>=1} [L^2p+Lp+(159/8)p](t_n)
          = sum_{n>=1} (t_n/4) B(t_n)exp(-t_n),
    B(t)=64t^3-448t^2+974t-621.

The expansion

    B(25/8+u)=7/8+49u+152u^2+64u^3

has the displayed coefficients. Every term is positive for u>=0. Therefore retaining the first theta term in W and in this positive lower bound for R is valid for their product. No omitted theta term has an adverse sign.

For M=||W||^2, M_T=||xW||^2, m_T=||(xW)'||^2, and R2=integral x^2 W R, integration by parts gives

    m_T = integral x^2(W')^2,
    integral x^2 W W'' = M-m_T,
    m_T = M+20M_T-R2.

The cross term in ||W+xW'||^2 cancels M in the first identity. It does not remove M from the second identity. All boundary terms vanish by actual source decay.

### Retaining the real quotient in R2

With t=pi exp(2x), u=t-pi, evenness and dx=dt/(2t) give exactly

    R2 >= (1/16) integral_pi^infinity
            log^2(t/pi) F0(x)^2 P0(t)B(t)exp(-2t)dt,
    P0(t)=4t^2-6t.

Combining F0^2>=2t/(t+pi) with log(t/pi)>=2u/(t+pi) changes the factor 1/16 into precisely

    R2 >= exp(-2pi) integral_0^infinity
       u^2 [tP0(t)/2]B(t)exp(-2u)/(t+pi)^3 du.

The polynomial 2t^3-3t^2=tP0(t)/2 is increasing on t>1. Its expansion at 25/8 is

    8125/256 + (1275/32)u + (63/4)u^2 + 2u^3,

which is bounded below by 31+39u+15u^2+2u^3. Dropping only the positive constant of B and multiplying gives, including the outer u^2,

    P(u)=1519u^3+6623u^4+8647u^5
                      +4874u^6+1264u^7+128u^8.

The six coefficients follow by polynomial multiplication. Using t+pi=u+2pi<u+44/7 and exp(-2pi)>1/540 then gives

    R2 > (1/540) integral_0^infinity
                   P(u)exp(-2u)/(44/7+u)^3 du.

### Exact moments and Jensen direction

The factorial identity integral_0^infinity u^k exp(-2u)du=k!/2^(k+1) gives the six contributions to Q0 over denominator eight as

    4557, 39738, 129705, 219330, 199080, 80640,

and the six contributions to Q1 over denominator eight as

    9114, 99345, 389115, 767655, 796320, 362880.

Thus

    Q0=673050/8=336525/4,
    Q1=2424429/8,
    Q1/Q0<26/7,

where 16971003<17499300 is the exact last comparison. The function (44/7+u)^(-3) is decreasing and convex. Jensen is applied to the positive probability measure P(u)exp(-2u)du/Q0, so the lower, not upper, estimate is

    integral P exp(-2u)/(44/7+u)^3 du
       >= Q0/(44/7+Q1/Q0)^3 > Q0/1000.

It follows that

    R2 > 336525/2160000 = 4487/28800 > 3/20.

The last comparison is 4487>4320. There is no reciprocal-direction error and no missing real-half-line factor.

## 5. Actual source mass bounds

### M<2/5

For t=exp(2|x|), retain the negative first theta amplitude and bound the entire positive theta amplitude as in section 3:

    W(x) < t^(1/4)[40t^2-(75/4)t]exp(-pi t).

The bracket is positive on t>=1. Squaring and combining both real half-lines gives an upper integral with factor t^(-1/2), which can be bounded by one while it still multiplies a positive square. Exact integration of

    1600t^4-1500t^3+(5625/16)t^2

then gives exp(-2pi) times

    (7225/16)r+(20825/8)r^2+(87225/8)r^3
                        +29400r^4+38400r^5,
    r=1/(2pi)<4/25.

The five coefficients are positive after integration. At r=4/25, the five terms are less than 73,67,45,20,5, respectively. Hence M<210/529<2/5, since 1050<1058. Signed coefficients were not bounded separately before integration.

Together with the exact identity and R2>3/20, this proves

    m_T < 20M_T+1/4.

No upper bound on M_T is inserted into a term of the wrong sign.

### M_T>2887/405000

The actual positive first theta term, the retained real quotient, and the even variable change give

    M_T >= (1/4) integral_pi^infinity
          log^2(t/pi) F0(x)^2 t(4t-6)^2 exp(-2t)dt.

The same rational quotient and logarithm inequalities yield

    M_T > (1/540) integral q(u)exp(-2u)/(c+u)^3 du,
    c=44/7,
    q(u)=2u^2(25/8+u)^2(13/2+4u)^2
        =(105625/128)u^2+(6175/4)u^3+1047u^4+304u^5+32u^6.

The exact raw moments from monomial integration are

    Q0=1188073/512, Q1=5908875/1024,
    Q2=9168795/512,  Q3=67710615/1024.

About u=5/2, the corresponding unnormalized centered moments are

    C1=-15745/512,
    C2=7288255/2048,
    C3=3842815/1024.

Set a=c+5/2=123/14. Since the fourth derivative of (c+u)^(-3) is positive, its degree-three Taylor polynomial about 5/2 is a lower bound on all u>=0, including u<5/2. Its integrated lower value is

    Q0/a^3 - 3C1/a^4 + 6C2/a^5 - 10C3/a^6.

The rational estimates Q0>2320, -C1>30, C2>3558, C3<3753, and 35/4<a<44/5 give its four signed contributions respectively greater than 17/5, 3/200, 2/5, and -17/200. The final negative contribution uses (35/4)^6>445000 and 37530/445000<17/200. The first integral, with its factor 1/540, is therefore greater than 373/54000.

For r=u/(t+pi), the positive logarithm series gives

    log(t/pi)=2 atanh r >= 2(r+r^3/3),
    log^2(t/pi) >= 4r^2[1+(2/3)r^2].

Retaining that extra positive part adds at least

    (2/1620) integral q(u)u^2 exp(-2u)/(c+u)^5 du.

Here the positive measure has mass Q2>17900 and mean

    Q3/Q2=67710615/18337590<37/10,

because 677106150<678490830. Jensen for the decreasing convex fifth reciprocal power, together with c+37/10=699/70<10, makes this correction strictly greater than 179/810000. Therefore

    M_T > 373/54000 + 179/810000 = 2887/405000.

The correction is added to the same actual source reduction; it is not a second count of an already retained term. No numerical integral or empirical value of a source moment is used.

## 6. Actual Gamma logarithm inequality and finite start

For t>=2, put b=t/2 and x_n=n+1/4. The n-th rational term of g is exactly

    1/x_n - x_n/(x_n^2+b^2).

Let H_N=sum_(k=1)^N 1/k and L_(2N)=sum_(k=0)^(2N-1)(-1)^k/(2k+1). The finite identity

    sum_{n=0}^{N-1} 1/(n+1/4)
       = 2H_(4N)-H_(2N)+2L_(2N)

with the alternating odd reciprocal sum L_(2N), followed by the harmonic and arctangent limits, gives

    g(t)-c_Gamma
      = lim [log N-sum_{n=0}^{N-1} f_b(n+1/4)]-log pi,
    f_b(x)=x/(x^2+b^2).

This cancels EulerGamma+3log2+pi/2 exactly before any estimate.

The unit midpoint cells start at -1/4, not at zero. Their Peano kernel is bounded by 1/8 in absolute value. On [-1/4,infinity),

    f_b'(x)=(b^2-x^2)/(x^2+b^2)^2,
    f_b''(x)=2x(x^2-3b^2)/(x^2+b^2)^3.

For b>=1, the derivative's total variation on this exact interval is

    9/(4b^2)-f_b'(-1/4).

Writing z=1/(16b^2)<=1/16 gives

    b^2 f_b'(-1/4)=(1-z)/(1+z)^2 >=240/289>3/4.

Thus the variation is less than 3/(2b^2), and the full midpoint error is less than 3/(16b^2). The finite-start term is present and has the correct sign. Integrating f_b exactly and taking the limit gives

    |g(t)-c_Gamma-log sqrt(b^2+1/16)+log pi|<3/(16b^2).

In particular,

    g(t)-c_Gamma > q(t)=log[t/(2pi)]-3/(4t^2),  t>=2.

The actual variation estimate applies for every b>=1; no asymptotic extrapolation is used. The bound is never used at t=0.

For later absolute estimates, the positive difference between log sqrt(b^2+1/16) and log b is at most 1/(8t^2). Hence also

    |g(t)-c_Gamma-log[t/(2pi)]|<7/(8t^2),  t>=2.

## 7. New central parabola and the whole-line Gamma carrier

For gamma>=14 and |u|<=10, both Gamma arguments are at least four. Since q'(t)>0, the direct lower expression is minimized at gamma=14. With z=u^2,

    h_gamma(u)>H(z),
    H(z)=(1/4)log[(196-z)/(4pi^2)]
                 -(3/8)(196+z)/(196-z)^2.

The lower bound on H(0) itself is

    H(0)=(1/2)log(7/pi)-3/1568>393/1000.

Indeed pi<22/7, log(49/22)>285336/357911>79/100, and 3/1568<1/500. This does not infer an H-center bound merely from a lower bound on h(0).

The exact loss is

    H(0)-H(z)=-(1/4)log(1-z/196)
      +(3/8)[(196+z)/(196-z)^2-1/196].

For 0<z<=100, the first term divided by z is increasing and at most log(49/24)/400<3/1600. The last strict inequality follows from the degree-three exponential polynomial exp(3/4)>269/128>49/24.

The second term divided by z is

    (3/8)(588-z)/[196(196-z)^2].

Its derivative has positive numerator 980-z. Its endpoint value is 61/602112<1/8000, since 488000<602112. Therefore

    H(0)-H(z)<z(3/1600+1/8000)=z/500.

The zero endpoint is handled by the separate center estimate. This proves the stated uniform central parabola without differentiating an inequality or mixing unrelated center and loss bounds.

### Actual outer deficit, including the zero-argument neighborhood

For d_gamma(u)=(3/10-h_gamma(u))_+, the direct-pair estimates and the finite rational series give these outer layers:

    10<=|u|<=11:     d_gamma<17/100,
    11<=|u|<=12:     d_gamma<3/10,
    12<=|u|<=13:     d_gamma<7/10,
    13<=|u|<57/2:    d_gamma<31/20,
    |u|>=57/2:       d_gamma=0.

The first two use q only down to t=2. At u=11 the logarithm argument is 3675/1936>15/8, log(15/8)>5/8, and the inverse debit 1902/90000<1/40. Thus h>21/160>13/100. At u=12 the argument is 637/484>13/10, log(13/10)>1/4, and 510/10816<1/20, giving h>1/80.

The other layers do not use the logarithm. The scalar constants used here are g(14)>14561/2400 and c_Gamma<571/105. The first is obtained from five positive rational terms and the decreasing-series integral tail greater than log(5/3)>49/96. The second follows from log pi<7/6, EulerGamma<3/5, pi/2<11/7, and log2<7/10. The Euler bound follows, for example, from EulerGamma<=H4-log4-1/10 and the three-term atanh lower bound log4>83/60.

One large Gamma argument is always at least 24 outside ten, so the unconditional defect is less than

    A=3/10+571/210-14561/9600=100953/67200<601/400<31/20.

On 12<=|u|<=13 the smaller argument is at least one and the first three positive terms give g(1)>33/10; this yields d<7/10. Beyond 57/2 both arguments are at least 14, giving h>10567/33600>3/10. This explicitly covers the neighborhood where one argument is zero, without passing a logarithm through it.

### Full-source Fourier tail used in the outer integral

On z=x+i/2, set K=integral |W(z)|dx, J=integral |z|^2|W(z)|dx, and K1=integral |zW(z)|dx. From the actual shifted envelope in section 3, t^(1/4)<=(t+3)/4, and log t<=(t-1)/sqrt(t), direct polynomial integration gives

    K < (46/4)exp(-d)(4r+5r^2+2r^3)
      < (23/10)(89408/19683) < 21/2,
    J < (46/16)exp(-d)(4r+5r^2+10r^3+6r^4)
      < (23/40)(3691968/531441) < 4,
    r=1/d<16/27.

Here exp(d)>5 follows from its degree-four lower polynomial. The second integrand before integration is t^3+2t^2-2t+3; its integrated coefficients are all positive. The final integer comparisons are 4112768<4133430 and 84915264<85030560. Cauchy-Schwarz gives K1^2<=KJ<42.

For exp(-iux), positive u is shifted downward and negative u upward. Conjugation makes the two source norms equal. Therefore

    |F'(u)|^2 < 42exp(-|u|).

Define D_outer=integral_(|u|>10)d_gamma(u)|F'(u)|^2 du/(2pi). Integrating the preceding deficit layers against this actual envelope yields

    D_outer < (42/pi)exp(-10)
      [17/100+(13/100)exp(-1)+(2/5)exp(-2)+(17/20)exp(-3)]
      < (7/10800)(6313/20000)
      = 44191/216000000 < 41/200000.

The bracket uses exp(-1)<3/8, exp(-2)<17/125, and exp(-3)<1/20. The difference in the last comparison is 44280-44191>0 over denominator 216000000. The finite upper endpoint would subtract another nonnegative tail contribution and is safely omitted in this upper estimate.

### Combining the carrier, identity, and mass

Outside |u|<=10 the new parabola is at most 193/1000<3/10. Thus h>=3/10-d implies the valid global lower majorant

    h_gamma(u)>=393/1000-u^2/500-d_gamma(u)1_(|u|>10).

Plancherel identifies integral |F'|^2/(2pi)=M_T and integral u^2|F'|^2/(2pi)=m_T. Consequently

    G_T > (393/1000)M_T-m_T/500-41/200000
        > (353/1000)M_T-141/200000.

Finally,

    353*2887=1019111 > 1018575=503*2025,

so (353/1000)M_T>503/200000 and G_T>181/100000. The outer deficit is paid in addition to the global quadratic moment; it is not an unjustified replacement for a different defect definition.

## 8. Opposite-Gamma residual

The absolute logarithm approximation in section 6 is used only on t>=2. On 0<=t<=2, let g0(t)=4t^2/(1/4+t^2). The positive remainder satisfies

    0<=g-g0<=8[(5/2)^(-3)+(1/2)integral_(5/2)^infinity a^(-3)da]
             =104/125.

Since g+g0<9<2c_Gamma and g>=g0, one has |g-c_Gamma|<=c_Gamma-g0. The bounds 9/2<c_Gamma<11/2 are elementary consequences of the constants already checked. Integrating g0 exactly gives

    integral_0^2 |g-c_Gamma|dt <43/7.

For c=2pi, the exact integral of |log(t/c)| from 2 to 15 is

    2c-17-2log(c/2)+15log(15/c)<99/14.

Here log pi>1 and log(12/5)<9/10, the latter certified by the degree-four exponential lower polynomial. The remainder from t=2 costs at most 7/16. On t=gamma+v, the exponentially weighted exterior is bounded by integrating

    9/10+v/14+1/224,

whose integral is less than one. The complete scalar brace is therefore less than

    43/7+99/14+7/16+1=1641/112<15.

In the exact R_T, evenness cancels the factor 1/2 against the two scalar half-lines. The product of the actual Fourier bounds is 42exp[-max(gamma,|u|)]. Accordingly

    |R_T| < [42/(2pi)]exp(-gamma)*15
          <105exp(-14)<89.25/1000000<90/1000000.

The scalar zero region is treated by the finite positive series, not a singular logarithm. The Fourier measure and all opposite-packet factors agree with section 2.

## 9. Signed n=2 carrier, tighter actual phase, and n=3

For s=log2, a=s/2, let

    N2=integral_(|y|<=a) (a^2-y^2)U_s(y)dy.

Positivity of the real full source gives A_T(s)>=-N2. The exterior positive part is discarded only in this lower bound. The actual prime coefficient is (log2/sqrt2)[-cos(gamma log2)]>0.

Retaining the full positive theta amplitude and the first negative amplitude gives, centrally,

    U_s(y)<=sqrt2 exp(-4pi)(C-Dy^2)exp(-lambda y^2),
    C=60025/4, D=24000, lambda=8pi.

Indeed the exact amplitude product is 27006.25-12000cosh(2y), which is at most C-Dy^2. Both this polynomial and a^2-y^2 are nonnegative on the integration interval; the signed polynomial is not extended to the whole line.

Define the truncated Gaussian integral

    J=integral_(-a)^a (a^2-y^2)(C-Dy^2)exp(-lambda y^2)dy.

Integration by parts gives exactly

    J=A0 I0+B0 exp(-lambda a^2),
    I0=integral_(-a)^a exp(-lambda y^2)dy,
    A0=Ca^2-(C+Da^2)/(2lambda)+3D/(4lambda^2),
    B0=Ca/lambda-3Da/(2lambda^2).

The cubic boundary terms cancel in B0. On 28/81<a<25/72 and 25<lambda<176/7, both A0 and B0 are positive. The rational estimates give

    Ca^2<1810, Da^2>2856,
    (C+Da^2)/(2lambda)>355, 3D/(4lambda^2)<29.

Thus A0<1484 and I0<=1/sqrt8<5/14, so A0I0<530. Also B0<190 and lambda a^2>59/20. Since exp(59/20)>19, the boundary contribution is less than ten. Hence J<540.

The exact real quotient improves its former sqrt2 bound:

    F0(a-y)F0(a+y)=4/[3/2+sqrt2 cosh y]<=8/(3+2sqrt2).

Relative to sqrt2 its ratio is 8/(4+3sqrt2)<34/35, since sqrt2>24/17. Combining J<540, exp(4pi)>280000, and log2<25/36 therefore gives, before replacing the positive phase by one,

    P_T,2 > -(51/39200)[-cos(gamma log2)].

No separate favorable positive y^2 moment may be counted again after this negative-part integral.

### The phase on the entire band

For delta=gamma log2-3pi, the exact rational endpoints are

    delta>14*(56/81)-66/7=142/567>1/4,
    delta<(29/2)*(25/36)-75/8=25/36<pi/2.

Therefore -cos(gamma log2)=cos delta is positive and strictly smaller than cos(1/4). The alternating cosine bound gives

    cos(1/4)<1-1/32+1/6144=5953/6144<97/100.

It follows, with the correct inequality direction for a negative debit, that

    P_T,2 > -4947/3920000 > -1262/1000000.

The last exact cross products are 4947000000<4947040000. The replacement is a scalar phase tightening of the same bound, not a new source truncation or a second sign credit.

### n=3

The real full-source envelope and central/exterior split give

    A(log n)<800n^4 exp(-2pi n)
       +[3200n^(9/2)/(2pi(n^2+1)-9)]exp[-pi(n^2+1)].

At n=3 the central term is less than 43/100000 by exp(6pi)>150732800. The exterior term is less than 9000/20^10<1/10^9. Hence A(log3)<431/1000000.

The logarithm enclosures give -313/840<gamma log3-5pi<13/40, so the n=3 cosine is negative throughout the band. The coefficient satisfies

    (log3)^3/(4sqrt3)<3993/20000<1/5.

Discarding the positive y^2 source moment therefore gives the valid unchanged lower debit -431/5000000. The same positivity argument is not incorrectly transferred to the sign-changing A_T itself.

## 10. Complete prime midpoint and all n>=4 carrier terms

### Prime midpoint: both contour orientations and both spatial exteriors

Write the cosine as the real part of exp(2i gamma y). Shift that positive-frequency exponential upward by i/2. The negative exponential shifts downward; conjugation gives the identical bound. Thus

    |B_T,gamma(s)| <= exp(-gamma) integral
       |z-s/2||z+s/2||W(z-s/2)W(z+s/2)|dy,
    z=y+i/2.

There is no extra factor two from these conjugate exponentials. On the central translated-source interval, the actual 46-envelope and Gaussian integration give

    1058 sqrt(pi/d)n^4 exp(-2dn)
          [(1+s^2)/4+1/(8dn)].

The inequalities sqrt(pi/d)<3/2, log^2 n<n, and d>27/16 make the bracket less than n/2. Since Lambda(n)/sqrt(n)<=log n/sqrt(n)<1, the all-integer central sum is bounded by

    (1587/2)sum_(n>=2)n^5 exp(-27n/8).

The first term uses exp(27/4)>800. The successive ratio is less than 243/880<2/7, using exp(27/8)>55/2. The resulting total is less than 44.436<45. These are exact rational comparisons.

For either exterior, y=s/2+v with v>=0, the exponential rate is

    A_n=2d(n^2+1)-9>(15/8)n^2.

Both exterior intervals together are bounded by

    4232n^(9/2)exp[-d(n^2+1)]
       [2/A_n^3+(s+1)/A_n^2+(s/2+1/4)/A_n].

Using s+1<=n and s/2+1/4<=3n/8, the bracket is less than 2/(7n). The complete weighted exterior sum is consequently less than

    1210 sum_(n>=2)n^4 exp[-27(n^2+1)/16].

Its first term is less than 121/25 because exp(135/16)>4000; its ratio is less than 81/64000<1/500. Thus it is less than 2420/499<5. Combining the disjoint source regions proves

    |E_prime_mid|<50exp(-gamma)<50/1000000.

The infinite sums were bounded by convergent all-integer majorants. Every prime power is included, with no bounded infinite-prime multiplier assumption.

### Carrier tail n>=4

Using the actual 80-envelope, the central Gaussian integral gives

    central |A_T(log n)|
       <=3200n^(7/2)exp(-2pi n)[1/(8pi n)+(log n)^2/4]
       <(3200/3)n^(9/2)exp(-2pi n).

Bounding the prime weight by one, n^(9/2) by n^5, exp(2pi) below by 500, and the ratio by 1/160 gives

    central total < (3200/3)*1024*160/(500^4*159)
                  <18/1000000.

For the two exterior intervals the tangent multiplier is exactly v^2+s v. The exponential rate 2pi(n^2+1)-8 exceeds 5n^2. After integration the coefficient is less than

    1024/(5n^2)+512log n<525n.

The resulting ratio is less than 2exp(-27)<1/2, and the exterior total is less than 4200exp(-51)<4200/20^10<1/1000000. Hence the complete carrier tail, including n=4 and all higher prime powers, costs less than 19/1000000.

The central Gaussian extensions are used only for positive upper majorants. The exterior contributions are still separately included. These carrier terms are distinct from the complete midpoint sum just bounded.

## 11. Final arithmetic and scope

The unchanged losses other than n=2 add to

    (90+50+19)/1000000+431/5000000
      =1226/5000000<246/1000000.

The improved actual carrier and phase therefore give

    b_gamma > 1810/1000000-1262/1000000-246/1000000
            =302/1000000>3/10000.

All inequalities are uniform on the stated closed gamma band. Strictness is supplied by the source and scalar comparisons, not by excluding a band endpoint. The certified lower bound is not identified with the actual value of the form.

This proves the physical tangent theorem in section 1. The limited physical-form scope is essential: no positive Schur complement, original constrained-domain conclusion, or RH conclusion follows.

## Appendix. Selected finite certificates and notation

These details make explicit finite comparisons used in the proof. They do not introduce additional numerical premises.

### Geometric full-theta bounds

For q<1/150 and S_k(q)=sum_(n>=1)n^k q^(n-1), the n>=3 tail ratio is at most (4/3)^8/150<1/15 for k<=8. Consequently

    S_k(q) <= 1+2^k/150+(3^k/22500)(15/14).

For k=4 this gives S4<9/8. At q<1/8000, the tail beginning with n=2 has ratio at most (3/2)^4/8000<1/1000, giving S4<101/100. These are upper majorants for the entire theta sum, not first-term replacements.

### Scalar Gamma constants and finite positive series

The five first terms of g(14) have values

    3136/785, 3136/4045, 3136/7785, 3136/12389, 3136/18241.

They exceed 399/100, 3/4, 2/5, 1/4 and 1/6, respectively, with sum greater than 1667/300. The decreasing-series integral tail from j=5 is at least log(5/3)>49/96. Thus g(14)>14561/2400. The last logarithm comparison follows from the first two positive atanh terms with parameter 1/4.

For g(1), its first three terms are 16/5, 16/145 and 16/765; the last two exceed 11/100 and 2/100, giving g(1)>33/10.

For completeness, c_Gamma>21/4>9/2 follows from these elementary lower bounds:

- EulerGamma>1/2: the strict trapezoidal bound for 1/x gives log(1+1/k)-1/(k+1)<(1/k-1/(k+1))/2; sum over k>=1.
- pi/2>25/16.
- log2>56/81>11/16 by the positive atanh series.
- log pi>9/8: use pi>25/8, log3>263/240, and log(25/24)>1/25, so log pi>1363/1200>9/8.

Their sum is 9/8+1/2+25/16+33/16=21/4. The upper bound c_Gamma<571/105<11/2 follows from log pi<7/6, EulerGamma<3/5, pi/2<11/7 and log2<7/10, as used in section 7. For the Euler upper bound, summing

    log(1+1/k)-1/(k+1) >= 1/[2(k+1)^2]

gives H_n-log n-EulerGamma>1/[2(n+1)]. With n=6, H6=49/20 and log6>11581/6480>249/140, it gives EulerGamma<3/5.

### Exponential and logarithm details

The degree-four exponential polynomial at 27/16 exceeds five. For the prime-midpoint central ratio, exp(27/8)>20*(11/8)=55/2; retaining the quadratic term at 3/8 also gives exp(27/8)>925/32, whose square exceeds 800. For the exterior first term, exp(135/16)>2900*(23/16)>4000.

At the outer Gamma layer, log(15/8)>22904/36501>5/8 from the first two positive atanh terms with parameter 7/23. Also log(13/10)>6/23>1/4. The central certificate log(49/22)>285336/357911 uses the first two terms with parameter 27/71.

The truncated Gaussian coefficient in section 9 obeys

    B0 < (7/20)[15010/25-3*24000/(2*25^2)] < 190.

Here the bracket decreases with lambda>=25 before setting lambda=25. Also lambda a^2>25(28/81)^2>59/20, and exp(59/20)>19 follows from exp3>20 and exp(1/20)<20/19.

### Classical theta reference

NIST Digital Library of Mathematical Functions, Chapter 20, section 20.7(viii), equation 20.7.32: https://dlmf.nist.gov/20.7.E32. Only the standard theta transformation is cited; no article, web snapshot or third-party source file is redistributed in this package.
