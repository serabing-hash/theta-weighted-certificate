# Proofs for theta–prime cancellation and limits of real-zero positivity criteria

This supplement gives the definitions and analytic proofs of three results: full-$L^2$ cancellation (T1), fixed-derivative absolute kernel bounds (T2), and an actual-prime counterexample to a proposed relative-positivity implication on an explicitly defined real-zero test class (T3).

The labels T1–T3 correspond to Theorems 1–3 of the manuscript of the same title. Labels L1–L2 refer to supporting lemmas. Equation labels E1 onward identify complete displays; several related formulas may share a display label. No eigenfunction, minimizing, or ground-state assumption is imposed on the counterexample. These results neither prove nor disprove the Riemann hypothesis. The proofs do not use a numerical experiment or a computational certificate.

## Definitions and conventions

For $R>0$, put $I_R=[-R,R]$. A function $h\in L^2(I_R;\mathbb C)$ is extended by zero to $\mathbb R$, and its Fourier transform is

$$
H(z)=\int_{-R}^R h(x)e^{-izx}\,\mathrm d x,\qquad z\in\mathbb C.
\tag{E1}
$$

In particular,

$$
H(i/2)=\int_{I_R}h(x)e^{x/2}\,\mathrm d x,
 \qquad H(-i/2)=\int_{I_R}h(x)e^{-x/2}\,\mathrm d x.
\tag{E2}
$$

The distinction in (E2) fixes the sign convention for the pole.

Let $\Lambda$ denote the von Mangoldt function, so that $\Lambda(p^a)=\log p$ for primes $p$ and integers $a\geq1$, and $\Lambda(n)=0$ otherwise. Define

$$
w_n=\frac{\Lambda(n)}{\sqrt n},\qquad
 \psi(t)=\sum_{2\leq n\leq t}\Lambda(n),\qquad E(t)=\psi(t)-t\quad(t\geq1),
\tag{E3}
$$

where $\psi$ is right-continuous. Also set

$$
\rho_1(s)=\frac{e^{-5s/2}}{1-e^{-2s}}
          =\sum_{k\geq1}e^{-(2k+1/2)s},\qquad s>0.
\tag{E4}
$$

The theta source used throughout is the actual series

$$
\kappa(y)=e^{y/2}\sum_{m\geq1}(4t_m^2-6t_m)e^{-t_m},
 \qquad t_m=\pi m^2e^{2y},\qquad y\geq0.
\tag{E5}
$$

It is positive on $[0,\infty)$, since $t_m\geq\pi>3/2$. Its smoothness and the estimates needed below follow directly from the series. No extension to negative $y$ is needed.

For the cancellation theorem, it is useful to allow a real-valued source $u\in C^1([R,\infty))$ satisfying

$$
|u(y)|+|u'(y)|\leq C e^{ay-be^{2y}}\quad(y\geq R)
\tag{E6}
$$

for some constants $C,b>0$ and $a\in\mathbb R$. Every fixed derivative $\kappa^{(j)}$ satisfies this condition. Define

$$
\begin{aligned}
C_{R,u}&=\int_R^\infty u(y)e^{y/2}\,\mathrm d y,\\
 K_{R,u}(x)&=\sum_{\substack{n\geq2\\x+\log n>R}}w_nu(x+\log n),\\
 B_{R,u}(x)&=K_{R,u}(x)-C_{R,u}e^{-x/2},\\
 D_{R,u}(x)&=\int_R^\infty u(y)\rho_1(y-x)\,\mathrm d y\qquad(x<R).
\end{aligned}
\tag{E7}
$$

Values of kernels at an individual endpoint are immaterial in $L^2$. We use the complex-linear functionals

$$
\mathcal A_{R,u}(h)=\int_{I_R}h(x)D_{R,u}(x)\,\mathrm d x,
 \qquad
 \mathcal Q_{R,u}(h)=\int_{I_R}h(x)B_{R,u}(x)\,\mathrm d x.
\tag{E8}
$$

Thus these displayed integrals are bilinear pairings, with no implicit conjugation. Since $u$, $B_{R,u}$, and $D_{R,u}$ are real, they also equal the usual inner products $\langle h,D_{R,u}\rangle$ and $\langle h,B_{R,u}\rangle$ under the convention $\langle f,g\rangle=\int f\overline g$. Positivity assertions below concern real functions.

## Exact cancellation on the full space

### Theorem T1 Full-$L^2$ cancellation

Let $R>0$ and let $u$ satisfy (E6). Then $B_{R,u}\in L^\infty(I_R)$ and $D_{R,u}\in L^2(I_R)$. For almost every $x\in I_R$,

$$
\begin{aligned}
B_{R,u}(x)
 ={}&\int_R^\infty e^{-(y-x)/2}E(e^{y-x})
              \bigl(u(y)/2-u'(y)\bigr)\,\mathrm d y\\
 &\quad-u(R)e^{-(R-x)/2}E(e^{R-x}).
\end{aligned}
\tag{E9}
$$

For $h\in L^2(I_R;\mathbb C)$, define for almost every $y>R$

$$
\begin{aligned}
P_Rh(y)&=\sum_{n\geq2}w_nh(y-\log n),\\
 T_Rh(y)&=\sum_{k\geq1}e^{-(2k+1/2)y}H(i(2k+1/2)),\\
 J_Rh(y)&=T_Rh(y)-e^{y/2}H(-i/2)+P_Rh(y).
\end{aligned}
\tag{E10}
$$

All source-weighted integrals in the following identity converge absolutely, and

$$
\int_R^\infty u(y)J_Rh(y)\,\mathrm d y
       =\mathcal A_{R,u}(h)+\mathcal Q_{R,u}(h).
\tag{E11}
$$

The exponential term in (E10) is exactly the contribution of continuous prime density:

$$
\int_1^\infty t^{-1/2}h(y-\log t)\,\mathrm d t
       =e^{y/2}H(-i/2),\qquad y>R.
\tag{E12}
$$

No derivative or boundary trace of $h$ is assumed.

**Proof.**

We first establish the kernels before interchanging any integral involving $h$. For fixed $R$, condition (E6) bounds the tail of the series in (E7), uniformly for $x\in I_R$, by a constant times a polynomial in $n$ multiplied by $e^{-b e^{-2R}n^2}$. Here $\Lambda(n)\leq\log n$ suffices. The tail is therefore absolutely and uniformly convergent. The finite initial portion consists of bounded functions, possibly with jumps. Thus $K_{R,u}$ and $B_{R,u}$ are bounded.

There is a constant $c$ such that $\rho_1(s)\leq c/s$ for all $s>0$: this follows from $s\rho_1(s)\to1/2$ at zero and exponential decay at infinity. For $d=R-x>0$, split the integral defining $D$ at $R+1$. The first part is bounded by

$$
c\sup_{R\leq y\leq R+1}|u(y)|\int_0^1\frac{\,\mathrm d\delta}{d+\delta},
$$

and the second part is uniformly bounded for $x\in I_R$. Consequently, near $x=R$,

$$
|D_{R,u}(x)|\leq C_{R,u}'\bigl(1+|\log(R-x)|\bigr).
\tag{E13}
$$

Away from that endpoint it is bounded. This proves $D_{R,u}\in L^2$. The same argument applies with $|u|$ in place of $u$.

The boundary term in (E9) can now be derived without differentiating $h$. Fix $x<R$, put $a_x=e^{R-x}>1$, and set

$$
f_x(t)=t^{-1/2}u(x+\log t),\qquad t\geq a_x.
$$

The direct definition of $B$, together with the substitution $y=x+\log t$, gives

$$
B_{R,u}(x)=\int_{(a_x,\infty)}f_x(t)\,\mathrm d E(t).
\tag{E14}
$$

Indeed, the atomic part is the strict-cutoff sum in (E7), while the continuous part is $C_{R,u}e^{-x/2}$. Stieltjes integration by parts yields

$$
B_{R,u}(x)=-f_x(a_x)E(a_x)-\int_{a_x}^\infty E(t)f_x'(t)\,\mathrm d t.
$$

The endpoint at infinity vanishes by (E6) and the elementary bound $E(t)=O(t\log(2t))$. Moreover,

$$
f_x'(t)=t^{-3/2}\bigl(u'(x+\log t)-u(x+\log t)/2\bigr).
$$

Changing variables gives exactly (E9). The right-continuous convention for $E$ matches the open lower endpoint in (E14). Changing values at the countably many thresholds would not change the resulting $L^2$ functional.

For completeness, the Stieltjes integral term in (E9) is absolutely integrable in $x$ against $|h(x)|$. Its absolute integrand, using $x\in I_R$ and $E(t)=O(t\log(2t))$, is bounded by a constant depending on $R$ times

$$
|h(x)|e^{y/2}(1+y+R)(|u(y)|+|u'(y)|).
$$

This is integrable because $h\in L^1(I_R)$ and (E6) holds. The boundary term has a bounded coefficient on $I_R$. Thus the formula also directly gives a valid integrated identity for all $L^2$ inputs.

For each bounded exterior $y$-interval, (E10) involves only finitely many translated copies of $h$. It is therefore defined almost everywhere and is independent, up to a null set, of the representative chosen for $h$. Absolute Fubini follows from

$$
\int_R^\infty |u(y)|\sum_{n\geq2}w_n|h(y-\log n)|\,\mathrm d y
 =\int_{I_R}|h(x)|K_{R,|u|}(x)\,\mathrm d x<\infty.
$$

In this line $K_{R,|u|}$ means its direct series, which needs only the decay bound, not differentiability of $|u|$. Hence

$$
\int_R^\infty u(y)P_Rh(y)\,\mathrm d y=\int_{I_R}h(x)K_{R,u}(x)\,\mathrm d x.
\tag{E15}
$$

The series in (E10) converges absolutely for $y>R$, since
$|H(ia)|\leq\|h\|_1e^{aR}$ for $a>0$. Equation (E4), the $L^2$ bound for the kernel obtained from $|u|$, and Cauchy–Schwarz justify absolute Fubini and give

$$
\int_R^\infty u(y)T_Rh(y)\,\mathrm d y=\mathcal A_{R,u}(h).
\tag{E16}
$$

Combining (E15), (E16), and (E2) proves (E11).

Finally, the substitution $x=y-\log t$ shows that the left side of (E12) equals

$$
e^{y/2}\int_{-\infty}^{y}h(x)e^{-x/2}\,\mathrm d x.
$$

Since $y>R$ and $h$ vanishes outside $I_R$, this is its asserted value. The calculation holds for complex $h$ and does not require parity.

∎

### Remark The boundary term is arithmetic

As $x$ increases through $R-\log n$, the direct prime kernel has signed jump $u(R)\Lambda(n)/\sqrt n$. The boundary term in (E9) has exactly that jump; the integral term is continuous there by dominated convergence. Omitting the boundary term therefore discards actual prime-power atoms. It is not a regularity convention for $h$.

## Absolute bounds from prime spacing

### Lemma L1 Fixed-order theta envelope

For each fixed integer $j\geq0$, the source $u_j=\kappa^{(j)}$ is smooth and satisfies (E6). As $y\to\infty$,

$$
u_j(y)=4\pi^2(-2\pi)^j e^{(9/2+2j)y}e^{-\pi e^{2y}}
              \bigl(1+O_j(e^{-2y})\bigr).
\tag{E17}
$$

There is $R_j\geq1$ such that $u_j$ is nonzero with constant sign on $[R_j,\infty)$ and, for $R\geq R_j$,

$$
|u_j(R+\delta)|\leq |u_j(R)|e^{-X\delta},
 \qquad X=e^{2R},\quad\delta\geq0.
\tag{E18}
$$

All assertions are for fixed $j$; no uniformity in a derivative order growing with $R$ is asserted.

**Proof.**

Differentiating an individual summand $e^{y/2}P(t)e^{-t}$, where $t=\pi m^2e^{2y}$, replaces $P$ by

$$
\mathcal DP(t)=(1/2-2t)P(t)+2tP'(t).
$$

Starting with $P_0(t)=4t^2-6t$, the polynomial $P_j=\mathcal D^jP_0$ has degree $j+2$ and leading coefficient $4(-2)^j$. On compact $y$-intervals, every differentiated series is uniformly absolutely convergent, by Gaussian decay in $m$. For large $y$, the $m=1$ term has the asymptotic (E17), and the sum over $m\geq2$ is exponentially smaller. The polynomial formula also controls derivatives of the remainder. Thus

$$
\frac{\mathrm d}{\mathrm dy}\log|u_j(y)|
 =-2\pi e^{2y}+(9/2+2j)+O_j(e^{-2y}).
$$

After increasing $R_j$, this is at most $-e^{2y}$. Integrating from $R$ to $R+\delta$, and using $e^{2y}\geq X$ there, proves (E18). The same series bounds for $u_j$ and $u_{j+1}$ imply (E6).

∎

### Lemma L2 Elementary arithmetic estimates

For $Y\geq2$,

$$
\psi(Y)=O(Y),\qquad
 \sum_{n\leq Y}\frac{\Lambda(n)}n=O(1+\log Y),\qquad
 \sum_{n\leq Y}\frac{\Lambda(n)^2}n=O((1+\log Y)^2).
\tag{E19}
$$

**Proof.**

Write $\vartheta(Y)=\sum_{p\leq Y}\log p$. For integer $n\geq1$, every prime in $(n,2n]$ divides $\binom{2n}{n}$, so

$$
\vartheta(2n)-\vartheta(n)\leq\log\binom{2n}{n}\leq2n\log2.
$$

Summing over dyadic $n$ and using monotonicity gives $\vartheta(Y)=O(Y)$. Consequently

$$
\psi(Y)=\sum_{1\leq a\leq\log_2Y}\vartheta(Y^{1/a})
       =O(Y+\sqrt Y\log(2Y))=O(Y).
$$

Partial summation gives

$$
\sum_{n\leq Y}\frac{\Lambda(n)}n
 =\frac{\psi(Y)}Y+\int_1^Y\frac{\psi(t)}{t^2}\,\mathrm d t
 =O(1+\log Y).
$$

The final estimate follows from $\Lambda(n)^2\leq(\log Y)\Lambda(n)$ for $n\leq Y$.

∎

### Theorem T2 Unconditional absolute bounds

For every fixed integer $j\geq0$, there are constants $C_j$ and $R_j$ such that, with $u=\kappa^{(j)}$ and $R\geq R_j$,

$$
\begin{aligned}
\|B_{R,u}\|_{L^2(I_R)}&\leq C_j|u(R)|e^{-R}(1+R),\\
 \|D_{R,u}\|_{L^2(I_R)}&\leq C_j|u(R)|e^{-R}.
\end{aligned}
\tag{E20}
$$

In particular,

$$
|\mathcal Q_{R,u}(h)|\leq C_j\|h\|_2|u(R)|e^{-R}(1+R)
 \qquad(h\in L^2(I_R;\mathbb C)).
\tag{E21}
$$

**Proof.**

Put $X=e^{2R}$, $L=X$, and $T=\log X=2R$. Under the change of variable $s=R-x$, Lemma L1 gives

$$
|K_{R,u}(R-s)|\leq |u(R)|\sum_{n\geq2}w_nv_n(s),\qquad
 v_n(s)=e^{-L(\log n-s)}\mathbf 1_{\{s<\log n\}},\quad0<s<T.
\tag{E22}
$$

An exact integration up to $\min(T,\log m,\log n)$ shows that

$$
\int_0^Tv_m(s)v_n(s)\,\mathrm d s
 \leq\frac1{2L}e^{-L|\log m-\log n|}.
\tag{E23}
$$

If $m,n\leq2X$, then $|\log m-\log n|\geq|m-n|/(2X)$, so the last exponential is at most $e^{-|m-n|/2}$. The matrix with these entries has uniformly bounded row sums. Applying $2w_mw_n\leq w_m^2+w_n^2$ to the double sum, or equivalently the Schur bound, gives

$$
\begin{aligned}
\left\|\sum_{2\leq n\leq2X}w_nv_n\right\|_{L^2(0,T)}^2
 &\leq\frac{C}{L}\sum_{n\leq2X}\frac{\Lambda(n)^2}n\\
 &\leq\frac{C}{X}(1+\log X)^2,
\end{aligned}
\tag{E24}
$$

by Lemma L2. This argument uses the spacing of the integers and does not assume an estimate for primes in short intervals.

For $n>2X$ and $0<s<T$, the sum in (E22) is bounded by

$$
T_X=\sum_{n>2X}\frac{\log n}{\sqrt n}(n/X)^{-L}.
$$

The summand, considered as a function of a real variable, is decreasing for large $X$. The bound by its value at $2X$ plus its integral from $2X$ to infinity gives

$$
\begin{aligned}
T_X\leq 2^{-L}\biggl\{
 &\frac{\log(2X)}{\sqrt{2X}}\\
 &+\sqrt{2X}\left[\frac{\log(2X)}{L-1/2}
                       +\frac1{(L-1/2)^2}\right]\biggr\}.
\end{aligned}
\tag{E25}
$$

Its $L^2(0,T)$ contribution is at most $\sqrt T\,T_X$ and is negligible compared with $X^{-1/2}(1+\log X)$. Hence

$$
\|K_{R,u}\|_2\leq C_j|u(R)|X^{-1/2}(1+\log X).
\tag{E26}
$$

The subtracted continuum kernel is smaller on this scale. Indeed,

$$
|C_{R,u}|\leq\frac{|u(R)|e^{R/2}}{L-1/2},
 \qquad \|e^{-x/2}\|_{L^2(I_R)}^2=e^R-e^{-R}\leq e^R.
$$

Thus

$$
|C_{R,u}|\|e^{-x/2}\|_2
 \leq\frac{|u(R)|e^R}{X-1/2}=O(|u(R)|X^{-1/2}),
$$

which, together with (E26), proves (E20).

For the archimedean kernel, let $d=R-x>0$. From $\rho_1(s)\leq C/s$ and (E18),

$$
|D_{R,u}(R-d)|\leq C|u(R)|\int_0^\infty\frac{e^{-L\delta}}{d+\delta}\,\mathrm d\delta
                =C|u(R)|f(Ld),
$$

where

$$
f(v)=\int_0^\infty\frac{e^{-t}}{v+t}\,\mathrm d t.
$$

Splitting at $t=1$ gives $f(v)=O(1+|\log v|)$ for $0<v\leq1$, while $f(v)\leq1/v$ for $v\geq1$. Thus $f\in L^2(0,\infty)$ and

$$
\|D_{R,u}\|_2^2\leq\frac{C|u(R)|^2}{L}\int_0^\infty f(v)^2\,\mathrm d v.
$$

This proves (E20). Cauchy–Schwarz gives (E21).

∎

### Remark What the norm estimate does not compare

Theorem T2 supplies upper bounds on two linear functionals. It supplies no lower bound for $\mathcal A_{R,u}(h)$ in terms of $\|h\|_2$, even when $\mathcal A_{R,u}(h)>0$. Such a lower bound cannot be inserted implicitly when seeking a relative estimate for $\mathcal Q_{R,u}(h)$.

## A positive real-zero class with negative relative flux

For an integer $q\geq0$, let $\mathcal C_R^q$ be the following explicit test class. Its members are real even functions $h\in C^q(\mathbb R)$ with

1. $\operatorname{supp} h=[-R,R]$ and $h(x)>0$ for every $-R<x<R$;
1. a Fourier transform $H$ of exact exponential type $R$, with all its zeros real;
1. $H(i/2)=1$ and $H(ib)>0$ for every $b>0$.

Here support means the closed support of the function, not merely its convex hull. Exact exponential type means that $H$ has an upper bound of exponential type $R$ and has no such bound of smaller type. This class is defined without an eigenvalue equation.

### Theorem T3 Actual-prime failure of relative positivity

Fix $q\geq0$. For all sufficiently large integers $M$ divisible by $6$, put $R_M=\log M$. There are finite integers $N(M)\geq q+2$ and functions $h_M\in\mathcal C_{R_M}^q$ such that

$$
\mathcal A_{R_M,\kappa}(h_M)>0,
 \qquad
 \frac{\mathcal Q_{R_M,\kappa}(h_M)}{\mathcal A_{R_M,\kappa}(h_M)}
       =-M^3(1+o(1))
\tag{E27}
$$

as $M\to\infty$ along $6\mid M$. In particular, for sufficiently large such $M$,

$$
\mathcal A_{R_M,\kappa}(h_M)+\mathcal Q_{R_M,\kappa}(h_M)<0.
\tag{E28}
$$

Consequently no constant independent of $R$ can make
$|\mathcal Q_{R,\kappa}(h)|\leq C\mathcal A_{R,\kappa}(h)$ hold for every $h\in\mathcal C_R^q$. Even $\mathcal Q_{R,\kappa}(h)\geq-\mathcal A_{R,\kappa}(h)$ fails on this class.

### A full-support spline approximate identity

Fix $R>0$ for the moment. Let $g_N$ be the $N$-fold convolution of the probability density

$$
\frac{N}{2R}\mathbf 1_{[-R/N,R/N]}.
$$

It is the density of $S_N=X_1+\cdots+X_N$, where the independent $X_i$ are uniform on that interval. Its Fourier transform is

$$
G_N(z)=\operatorname{sinc}(Rz/N)^N,\qquad
 \operatorname{sinc} z=\begin{cases}\sin z/z,&z\ne0,\\1,&z=0.\end{cases}
\tag{E29}
$$

Set

$$
a_N=G_N(i/2)=\left(\frac{\sinh(R/(2N))}{R/(2N)}\right)^N,
 \qquad h_N=g_N/a_N,\qquad H_N=G_N/a_N.
\tag{E30}
$$

For $N\geq2$, the convolution is even, positive on $(-R,R)$, and has support exactly $[-R,R]$. For example, strict interior positivity follows by choosing all $N$ summands in small intervals about $x/N$ whenever $|x|<R$. The explicit truncated-power formula

$$
g_N(x)=\frac{(N/(2R))^N}{(N-1)!}
       \sum_{k=0}^N(-1)^k\binom Nk
       \bigl(x+R-2Rk/N\bigr)_+^{N-1}
\tag{E31}
$$

shows $g_N\in C^{N-2}(\mathbb R)$. This formula follows by taking $N$ successive convolutions of interval indicators, or by integrating their distributional derivatives. A finite $g_N$ is not being claimed to be $C^\infty$.

All zeros of (E29) are real. The bound
$|G_N(z)|\leq e^{R|\operatorname{Im}z|}$ follows from its probability-density representation, and

$$
\lim_{t\to\infty}\frac{\log G_N(it)}t=R
$$

follows from the hyperbolic sine formula. Its exponential type is therefore exactly $R$. Moreover, $G_N(ib)>0$ for real $b$, $a_N\to1$, and normalization gives $H_N(i/2)=H_N(-i/2)=1$. In particular, $h_N\in\mathcal C_R^q$ whenever $N\geq q+2$.

Since $\operatorname{Var}(S_N)=R^2/(3N)$, the probability measures $g_N(x)\,\mathrm d x$ converge weakly to $\delta_0$. We record a stronger bound to handle the endpoint singularity of $D$. By convexity and symmetry,

$$
\mathbb E e^{tX_i}\leq\cosh(tR/N)\leq e^{t^2R^2/(2N^2)}.
$$

The last inequality follows by integrating $\tanh v\leq v$ for $v\geq0$. Markov's inequality and the choice $t=Nb/R^2$ give

$$
\Pr(|S_N|>b)\leq2e^{-Nb^2/(2R^2)}\qquad(b>0).
\tag{E32}
$$

Convolution also gives $\|g_N\|_\infty\leq N/(2R)$. Consequently, for fixed $0<b<R$,

$$
\begin{aligned}
\int_{|x|>b}g_N(x)|D_{R,\kappa}(x)|\,\mathrm d x
 &\leq\bigl(\|g_N\|_\infty\Pr(|S_N|>b)\bigr)^{1/2}
                   \|D_{R,\kappa}\|_2\\
 &\longrightarrow0.
\end{aligned}
\tag{E33}
$$

The kernel $D_{R,\kappa}$ is continuous near zero, by dominated convergence in its defining integral. Its local continuity, concentration at zero, and (E33) therefore prove

$$
\mathcal A_{R,\kappa}(h_N)\longrightarrow D_{R,\kappa}(0).
\tag{E34}
$$

Weak convergence alone would not justify this step for an unbounded kernel.

### A composite threshold and its theta tail

Now fix an integer $M$ divisible by $6$ and let $R=\log M$. Since both $2$ and $3$ divide $M$, it is not a prime power, so $\Lambda(M)=0$. The kernel $K_{R,\kappa}$ is continuous at $x=0$. Indeed, the only possible threshold there has index $n=M$ and zero coefficient; all other finitely many initial terms are continuous near zero, and the remaining tail converges uniformly. Its boundedness and concentration at zero give

$$
\int_{I_R}h_N(x)K_{R,\kappa}(x)\,\mathrm d x\longrightarrow
 P_M:=\sum_{n>M}\frac{\Lambda(n)}{\sqrt n}\kappa(\log n).
\tag{E35}
$$

Put

$$
A_M=\int_{\log M}^\infty\kappa(y)\rho_1(y)\,\mathrm d y,
 \qquad C_M=\int_{\log M}^\infty\kappa(y)e^{y/2}\,\mathrm d y.
\tag{E36}
$$

Then (E34) says $\mathcal A_{R,\kappa}(h_N)\to A_M$. Because $H_N(-i/2)=1$, the continuum part of $\mathcal Q$ is exactly $C_M$ for every $N$, not merely in the limit. Therefore

$$
\mathcal Q_{R,\kappa}(h_N)\longrightarrow P_M-C_M
 \qquad(N\to\infty,\ M\text{ fixed}).
\tag{E37}
$$

Lemma L1 with $j=0$ gives

$$
\kappa(\log t)=4\pi^2t^{9/2}e^{-\pi t^2}\bigl(1+O(t^{-2})\bigr).
\tag{E38}
$$

With $t=e^y$, and using $\rho_1(\log t)=t^{-5/2}/(1-t^{-2})$, we obtain

$$
\begin{aligned}
C_M&=4\pi^2\int_M^\infty t^4e^{-\pi t^2}(1+O(t^{-2}))\,\mathrm d t\\
    &=2\pi M^3e^{-\pi M^2}(1+O(M^{-2})),\\
 A_M&=4\pi^2\int_M^\infty te^{-\pi t^2}(1+O(t^{-2}))\,\mathrm d t\\
    &=2\pi e^{-\pi M^2}(1+O(M^{-2})).
\end{aligned}
\tag{E39}
$$

For clarity, the elementary tail rule used here is

$$
\int_M^\infty t^a e^{-\pi t^2}\,\mathrm d t
   =\frac{M^{a-1}}{2\pi}e^{-\pi M^2}(1+O_a(M^{-2}))
$$

for fixed $a$. It follows from $t^2=M^2+s$ and expansion of $(1+s/M^2)^{(a-1)/2}$ under the exponentially decaying $s$-integral. The error terms in (E39)--(E39) obey the same bound.

The prime contribution begins at the next integer, while the continuous tail begins at $M$. By (E38) and $\Lambda(n)\leq\log n$,

$$
0\leq P_M\leq C M^4\log(M+1)e^{-\pi(M+1)^2}.
\tag{E40}
$$

To see the uniform constant, write $n=M+1+k$. Relative to the first Gaussian factor, the exponential is at most $e^{-2\pi(M+1)k}$, while the polynomial and logarithmic ratios are bounded by a fixed power of $1+k$. The resulting series is uniformly summable for $M\geq6$. Equations (E39) and (E40) give

$$
\frac{P_M}{C_M}=O\bigl(M\log(M+1)e^{-\pi(2M+1)}\bigr)\longrightarrow0.
\tag{E41}
$$

It follows that

$$
\frac{P_M-C_M}{A_M}=-M^3(1+o(1))
 \qquad(M\to\infty,\ 6\mid M).
\tag{E42}
$$

### Selection of finite splines

We finish the proof of Theorem T3 without replacing a function by a point mass. For each fixed $M$, the convergences (E34) and (E37) permit a finite $N(M)\geq q+2$ such that

$$
\left|\frac{\mathcal A_{R_M,\kappa}(h_{N(M)})}{A_M}-1\right|\leq\frac1M,
 \qquad
 |\mathcal Q_{R_M,\kappa}(h_{N(M)})-(P_M-C_M)|\leq\frac{C_M}{M}.
\tag{E43}
$$

Define $h_M=h_{N(M)}$ using the construction at radius $R_M$. Positivity of $\kappa$, $\rho_1$, and $h_M$ gives $\mathcal A_{R_M,\kappa}(h_M)>0$ directly. Equations (E39)--(E42) and (E43) yield

$$
\frac{\mathcal Q_{R_M,\kappa}(h_M)}{\mathcal A_{R_M,\kappa}(h_M)}
 =\frac{-C_M(1+o(1))+O(C_M/M)}{A_M(1+O(1/M))}
 =-M^3(1+o(1)).
$$

The class membership was proved above, and the final assertions follow immediately. This completes the proof.
∎

The order is essential: first fix $M$ and let $N\to\infty$ to establish convergence, then select a sufficiently large finite $N(M)$. No rate such as $N(M)\asymp M^2(\log M)^2$, and no effective formula for the least admissible $N(M)$, is claimed.

## Scope and contextual references

The positive splines above are not shown to satisfy an eigenfunction equation or minimize a Weil-type quadratic form. Their negative exterior functional therefore establishes neither a negative ground eigenvalue nor a counterexample to a ground-specific positivity statement. The argument refutes only the relative estimate on the explicitly defined class. It makes no priority or novelty claim.

The references below provide context, not premises in T1–T3. The theta source agrees with the kernel in [2], equations (7.1)–(7.2), under the normalization $\kappa(y)=4k(e^y)$. Box convolutions and sinc powers are established constructions: [3], Section 5, treats cardinal B-spline regularizations related to $\psi$; [4], Section 13.2, uses a sinc-power factor in a different variational construction assuming the Riemann hypothesis. The real-zero ground-state result in [1], Theorem 6.1, has its own realization and core hypotheses, which are not invoked here. Reference [5] concerns explicit prime-number-theorem error estimates; the arithmetic bounds used above were instead proved directly in L2.

1. A. Connes and W. D. van Suijlekom. *Quadratic Forms, Real Zeros and Echoes of the Spectral Action*. arXiv:2511.23257v1 (2025). https://arxiv.org/abs/2511.23257v1
2. A. Connes, C. Consani, and H. Moscovici. *Zeta Spectral Triples*. arXiv:2511.22755v1 (2025). https://arxiv.org/abs/2511.22755v1
3. M. Kunik. *On the formulas for $\pi(x)$ and $\psi(x)$ of Riemann and von Mangoldt*. Preprint No. 09/2005, Otto-von-Guericke University Magdeburg, version dated 9 April 2019. https://math.ovgu.de/math_media/Medien/Institute/IAN/Kunik/Publikationen/prime2019.pdf
4. X. Zhu. *Weil positivity in compact windows: a finite reduction, certified two-sided bounds, and a Landau–Widom decay law*. arXiv:2608.24827v2 (2026). https://arxiv.org/abs/2608.24827v2
5. D. R. Johnston and A. Yang. *Some explicit estimates for the error term in the prime number theorem*. arXiv:2204.01980v2 (2022). https://arxiv.org/abs/2204.01980v2
