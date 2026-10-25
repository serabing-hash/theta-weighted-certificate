# Analytic reproducibility of the theta–prime results

The results are reproduced by checking the definitions, convergence arguments, estimates, and limit order below against the full proofs in [PROOFS.md](PROOFS.md). No numerical experiment, external data set, fitted prime-error function, or numerical certificate is used. This document does not specify an executable experiment or report numerical output.

## Objects and conventions

All logarithms are natural. Fix $R>0$, put $I_R=[-R,R]$, and extend every input $h\in L^2(I_R;\mathbb C)$ by zero outside $I_R$. The Fourier convention is

$$
H(z)=\int_{-R}^R h(x)e^{-izx}\,\mathrm dx,
\qquad H(i/2)=\int h(x)e^{x/2}\,\mathrm dx,
\qquad H(-i/2)=\int h(x)e^{-x/2}\,\mathrm dx.
$$

The arithmetic objects are exact, not sampled or fitted:

$$
\Lambda(n)=\begin{cases}\log p,&n=p^a,\ p\text{ prime},\ a\geq1,\\0,&\text{otherwise},\end{cases}
\quad w_n=\frac{\Lambda(n)}{\sqrt n},
\quad \psi(t)=\sum_{2\leq n\leq t}\Lambda(n),
\quad E(t)=\psi(t)-t.
$$

The function $\psi$ is right-continuous. The theta and archimedean kernels are

$$
\kappa(y)=e^{y/2}\sum_{m\geq1}(4t_m^2-6t_m)e^{-t_m},
\quad t_m=\pi m^2e^{2y},\quad y\geq0,
\qquad
\rho_1(s)=\frac{e^{-5s/2}}{1-e^{-2s}},\quad s>0.
$$

For T1, the source $u$ is real, belongs to $C^1([R,\infty))$, and satisfies

$$
|u(y)|+|u'(y)|\leq C e^{ay-be^{2y}}
\quad(y\geq R),\qquad C,b>0,\ a\in\mathbb R.
$$

For T2, use $u=\kappa^{(j)}$ for a fixed integer $j\geq0$. For T3, use $u=\kappa$ without differentiation. Define

$$
\begin{aligned}
C_{R,u}&=\int_R^\infty u(y)e^{y/2}\,\mathrm dy,\\
K_{R,u}(x)&=\sum_{\substack{n\geq2\\x+\log n>R}}\frac{\Lambda(n)}{\sqrt n}u(x+\log n),\\
B_{R,u}(x)&=K_{R,u}(x)-C_{R,u}e^{-x/2},\\
D_{R,u}(x)&=\int_R^\infty u(y)\rho_1(y-x)\,\mathrm dy\quad(x<R),\\
\mathcal A_{R,u}(h)&=\int_{I_R}h(x)D_{R,u}(x)\,\mathrm dx,\\
\mathcal Q_{R,u}(h)&=\int_{I_R}h(x)B_{R,u}(x)\,\mathrm dx.
\end{aligned}
$$

The pairings are complex-linear in $h$, with no implicit conjugation. All positivity assertions concern real functions. Individual endpoint values of the kernels do not affect these $L^2$ pairings.

## Reproduce T1

The prime cutoff is strict: $x+\log n>R$. For $x<R$, set $a_x=e^{R-x}$ and $f_x(t)=t^{-1/2}u(x+\log t)$. The equivalent Stieltjes integral uses the open lower endpoint $(a_x,\infty)$ and right-continuous $E$. Integration by parts must therefore retain the negative boundary term:

$$
B_{R,u}(x)=-f_x(a_x)E(a_x)-\int_{a_x}^\infty E(t)f_x'(t)\,\mathrm dt.
$$

After the substitution $y=x+\log t$, this is

$$
\begin{aligned}
B_{R,u}(x)={}&\int_R^\infty e^{-(y-x)/2}E(e^{y-x})
\bigl(u(y)/2-u'(y)\bigr)\,\mathrm dy\\
&-u(R)e^{-(R-x)/2}E(e^{R-x}).
\end{aligned}
$$

The absolute, uniformly convergent prime-series tail gives $B\in L^\infty(I_R)$. The estimate $\rho_1(s)\leq c/s$ gives an integrable logarithmic endpoint singularity for $D$, hence $D\in L^2(I_R)$. Apply the same estimate with $|u|$ to justify absolute Fubini. The continuous-density substitution must yield $e^{y/2}H(-i/2)$, not $H(i/2)$. No differentiation or trace of $h$ is part of this argument.

## Reproduce T2

First fix $j$. Repeated differentiation of a theta summand replaces its polynomial $P$ by

$$
\mathcal DP(t)=(1/2-2t)P(t)+2tP'(t),\qquad P_0(t)=4t^2-6t.
$$

The resulting polynomial has degree $j+2$ and leading coefficient $4(-2)^j$. Its leading term and the exponentially smaller $m\geq2$ tail give

$$
\kappa^{(j)}(y)=4\pi^2(-2\pi)^j e^{(9/2+2j)y}e^{-\pi e^{2y}}
\bigl(1+O_j(e^{-2y})\bigr).
$$

Choose a sufficiently large threshold $R_j$ so that the logarithmic derivative of $|\kappa^{(j)}|$ is at most $-e^{2y}$ for $y\geq R_j$. For $R\geq R_j$, put $X=L=e^{2R}$ and $T=2R$. The source envelope is then $|u(R+\delta)|\leq |u(R)|e^{-L\delta}$.

Retain the exact pulse overlap bound

$$
v_n(s)=e^{-L(\log n-s)}\mathbf1_{\{s<\log n\}},\qquad
\int_0^T v_m(s)v_n(s)\,\mathrm ds
\leq\frac{e^{-L|\log m-\log n|}}{2L}.
$$

For $m,n\leq2X$, use integer spacing to bound the exponential by $e^{-|m-n|/2}$. Its row sums are bounded independently of $X$. Combine this with the directly proved Chebyshev bounds and estimate the entire $n>2X$ tail, as in T2. The continuum subtraction has norm $O(|u(R)|X^{-1/2})$. For the $D$ bound, use

$$
f(v)=\int_0^\infty\frac{e^{-t}}{v+t}\,\mathrm dt\in L^2(0,\infty),
\qquad |D(R-d)|\leq c|u(R)|f(Ld).
$$

This produces the stated absolute upper bounds. It does not produce a lower bound for $\mathcal A(h)$ or any relative inequality.

## Reproduce T3 and the finite diagonal

Fix a finite integer $q\geq0$. For each radius $R$, let $g_{R,N}$ be the $N$-fold convolution of the probability density $\frac{N}{2R}\mathbf1_{[-R/N,R/N]}$. Define

$$
G_{R,N}(z)=\operatorname{sinc}(Rz/N)^N,
\qquad \operatorname{sinc}(z)=\frac{\sin z}{z},\quad \operatorname{sinc}(0)=1,
$$

$$
a_{R,N}=\left(\frac{\sinh(R/(2N))}{R/(2N)}\right)^N,
\qquad h_{R,N}=g_{R,N}/a_{R,N},\qquad H_{R,N}=G_{R,N}/a_{R,N}.
$$

For $N\geq q+2$, these are finite $C^q$ splines after zero extension. They are even, have support exactly $[-R,R]$, and are strictly positive in its interior. Their Fourier transforms have exact exponential type $R$, only real zeros, positive imaginary-axis values, and $H_{R,N}(i/2)=H_{R,N}(-i/2)=1$. A finite spline is not claimed to be $C^\infty$.

Now fix an integer $M\geq6$ with $6\mid M$ and set $R=\log M$. The condition ensures $\Lambda(M)=0$, since $M$ has both 2 and 3 as prime factors. Define the exact positive integrals and actual-prime sum

$$
\begin{aligned}
A_M&=\int_{\log M}^\infty\kappa(y)\rho_1(y)\,\mathrm dy,\\
C_M&=\int_{\log M}^\infty\kappa(y)e^{y/2}\,\mathrm dy,\\
P_M&=\sum_{n>M}\frac{\Lambda(n)}{\sqrt n}\kappa(\log n).
\end{aligned}
$$

At this fixed $M$, prove

$$
\mathcal A_{R,\kappa}(h_{R,N})\longrightarrow A_M,
\qquad
\mathcal Q_{R,\kappa}(h_{R,N})\longrightarrow P_M-C_M
\quad(N\to\infty).
$$

The $K$ limit uses continuity at zero, which depends on $\Lambda(M)=0$. The $D$ limit also needs the concentration and $L^\infty$ density estimates to control its logarithmic endpoint singularity. Weak convergence by itself is insufficient for that unbounded kernel. The continuum contribution equals $C_M$ for every $N$ because the normalization is exact.

Choose a finite integer $N(M)\geq q+2$ for which both inequalities hold:

$$
\left|\frac{\mathcal A_{R,\kappa}(h_{R,N(M)})}{A_M}-1\right|\leq\frac1M,
\qquad
\left|\mathcal Q_{R,\kappa}(h_{R,N(M)})-(P_M-C_M)\right|\leq\frac{C_M}{M}.
$$

The fixed-$M$ convergence proves that the set of such finite integers is nonempty. Any member is sufficient; the theorem does not give an effective formula, a growth rate, a least computed value, or a table of admissible $N(M)$. There is no claim that one fixed spline order works at every radius.

Finally, let $M\to\infty$ along multiples of 6. The analytic scales are

$$
A_M=2\pi e^{-\pi M^2}(1+O(M^{-2})),\qquad
C_M=2\pi M^3e^{-\pi M^2}(1+O(M^{-2})),
$$

$$
0\leq P_M\leq C M^4\log(M+1)e^{-\pi(M+1)^2},
\qquad
\frac{P_M}{C_M}=O\!\left(M\log(M+1)e^{-\pi(2M+1)}\right)\to0.
$$

The selected finite splines therefore satisfy

$$
\mathcal A_{R,\kappa}(h_{R,N(M)})>0,
\qquad
\frac{\mathcal Q_{R,\kappa}(h_{R,N(M)})}{\mathcal A_{R,\kappa}(h_{R,N(M)})}
=-M^3(1+o(1)).
$$

The order is essential: fix $M$, establish convergence as $N\to\infty$, choose finite $N(M)$, and only then take the large-$M$ limit. The point mass at zero is used to identify limits, not as a member of the test class.

## Constants and assumptions

- The positive source-bound constants $C,b$ and real exponent $a$ in T1 belong to the chosen source. Fixed-radius kernel bounds may depend on that source and on $R$.
- The constant in $\rho_1(s)\leq c/s$, the Chebyshev constants, and the pulse row-sum bound can be chosen independently of the radius. The proofs need their finiteness, not numerical values.
- The thresholds $R_j$ and constants $C_j$ in T2 may depend on the separately fixed derivative order $j$. They do not depend on $h$ or on $R\geq R_j$. No explicit numerical threshold or growing-$j$ uniformity is supplied.
- The $O_j$ notation records possible dependence on fixed $j$. Gaussian-tail error constants may depend on a separately fixed power. The asymptotic constants in T3 are independent of large $M$ along $6\mid M$.
- The finite-diagonal choice depends on $q$ and $M$. It is justified by convergence, not by a numerical search or an unstated uniform convergence rate.
- No Riemann-hypothesis assumption, short-interval prime theorem, ground-state identification, or eigenfunction equation is used. The external bibliography is contextual only.

## File identity and the limits of this material

MANIFEST.sha256 contains the SHA-256 hashes of README.md, PROOFS.md, and REPRODUCIBILITY.md. Each line consists of a digest, two spaces, and a filename relative to this directory. The manifest does not hash itself. Checking these digests establishes whether the files match this snapshot; it does not establish mathematical correctness.

The support material records self-contained analytic arguments. It does not claim formal verification, peer-review acceptance, novelty, a numerical ground-state calculation, or any proof or disproof of the Riemann hypothesis.
