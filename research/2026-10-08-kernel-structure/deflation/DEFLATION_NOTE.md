# Exact constant mode deflation of the shifted certificate

8 October 2026 · Creative Commons Attribution–NonCommercial 4.0 International

## Conclusion and scope

The proposed identity is correct under the stated domain and coercivity premises. It exactly removes the scalar constant block from the operator solve and isolates the known small factor \(\delta/(\delta+c)\) in a finite-dimensional congruence. It does not establish positivity or a uniform certificate margin on the orthogonal complement. It does not, by itself, prove that a residual computation becomes cheaper or more accurate.

This is an analytic later-consumer note for the unchanged operator and observation map. There is no new certificate, changed pilot, physical or source evaluation, phase construction, H action, FFT, Gram calculation, numerical eigensolve, or executable verifier. The source advisory is `../constant_mode_margin_20261008/ADVISORY.md`. Its saved-data inclusions and operator premises remain conditional inputs. No Riemann-hypothesis conclusion is drawn.

## The same domain and an exact block factorization

Let \(L\) be the same self-adjoint realization on a Hilbert space \(\mathcal H\), with

\[
e\in D(L),\qquad Le=0,\qquad \|e\|=1.
\]

Let \(W:\mathbb C^{372}\to\mathcal H\) be bounded, let \(\delta>0\), and assume

\[
H=L+\delta I+WW^*\ge\eta I,\qquad \eta>0.
\]

Set \(P=I-ee^*\), \(\mathcal K=e^\perp\), \(L_0=L|_{\mathcal K}\), and

\[
x=W^*e,\quad c=x^*x,\quad \alpha=\delta+c,\quad
U=PW,\quad A=L_0+\delta I,\quad b=Ux.
\]

For every \(f\in D(L)\), both \(Pf\in D(L)\) and \(PLf=LPf=Lf\). Thus \(e\) and \(\mathcal K\) reduce \(L\), \(L_0\) is self-adjoint on \(D(L)\cap\mathcal K\), and

\[
D(H)=D(L)=\mathbb Ce\oplus D(L_0),\qquad
W=\binom{x^*}{U},\qquad
H=\begin{pmatrix}\alpha&b^*\\ b&A+UU^*\end{pmatrix}.
\]

Define

\[
M=I-\frac{xx^*}{\alpha},\qquad Q=M^{1/2},\qquad
V=UQ,\qquad S=A+UMU^*=A+VV^*.
\]

The matrix \(M\) is positive definite. If \(c>0\), its eigenvalues are \(\mu=\delta/\alpha\) on \(\mathbb Cx\) and \(1\) on \(x^\perp\). If \(x=0\), it is simply \(I\). Bounded perturbation makes \(S\) self-adjoint on \(D(L_0)\). The factorization

\[
H=T^*\begin{pmatrix}\alpha&0\\0&S\end{pmatrix}T,
\qquad
T=\begin{pmatrix}1&b^*/\alpha\\0&I\end{pmatrix}
\tag{1}
\]

is an operator identity on \(\mathbb Ce\oplus D(L_0)\). Both \(T\) and \(T^{-1}\) preserve this domain: only the scalar coordinate changes. Neither \(b\in D(L_0)\) nor \(W\mathbb C^{372}\subset D(L)\) is needed. In particular, no inverse of the possibly indefinite operator \(A\) was assumed.

For \(z\in D(L_0)\), put \(a=-b^*z/\alpha\). Equation (1) gives

\[
\langle z,Sz\rangle
=\langle(a,z),H(a,z)\rangle
\ge\eta\bigl(\|z\|^2+|b^*z|^2/\alpha^2\bigr).
\tag{2}
\]

Consequently \(S\ge\eta I\), and both inverses are bounded, with range in their respective operator domains. The block inverse is therefore legitimate:

\[
H^{-1}=
\begin{pmatrix}
\alpha^{-1}+\alpha^{-2}b^*S^{-1}b&-\alpha^{-1}b^*S^{-1}\\
-\alpha^{-1}S^{-1}b&S^{-1}
\end{pmatrix}.
\tag{3}
\]

## The finite certificate identity and its meaning

Multiplying (3) by \(W^*\) and \(W\) yields

\[
W^*H^{-1}W
=\frac{xx^*}{\alpha}
+\left(U-\frac{bx^*}{\alpha}\right)^*S^{-1}
 \left(U-\frac{bx^*}{\alpha}\right)
=\frac{xx^*}{\alpha}+MU^*S^{-1}UM.
\]

Thus, writing \(C=I-W^*H^{-1}W\),

\[
\boxed{\quad C=QFQ,\qquad F=I-V^*S^{-1}V.\quad}
\tag{4}
\]

The coefficient space still has dimension 372. This is elimination of one physical Hilbert-space mode, not deletion of one observation coordinate.

Since \(Q\) is invertible,

\[
C\succeq0\iff F\succeq0,\qquad C\succ0\iff F\succ0.
\tag{5}
\]

These tests have exactly the same unknown sign. They are also equivalent, respectively, to \(A\ge0\) and to \(A\ge aI\) for some \(a>0\). To check this without presuming \(A^{-1}\), let \(K=S^{-1/2}V\). The form identity

\[
\mathfrak a[z]
=\langle S^{1/2}z,(I-KK^*)S^{1/2}z\rangle
\]

uses the common form domain of the bounded perturbations \(A\) and \(S\). Because \(S^{1/2}\) maps that form domain onto \(\mathcal K\), \(A\ge0\) is equivalent to \(\|K\|\le1\), hence to \(F=I-K^*K\ge0\). If \(F\ge\gamma I>0\), then \(A\ge\gamma S\ge\gamma\eta I\). Conversely, if \(A\ge aI>0\), a now-valid inverse formula gives

\[
F=(I+V^*A^{-1}V)^{-1}
\ge\frac{a}{a+\|V\|^2}I>0.
\tag{6}
\]

Together with \(L+\delta I=\delta I\oplus A\), this identifies the remaining problem precisely. Establishing (5) still establishes positivity of the shifted operator on \(e^\perp\); it is not supplied by \(H\ge\eta I\).

Because \(V^*S^{-1}V\ge0\), equation (4) gives \(C\le M\). For \(c>0\), more explicitly,

\[
\frac{x^*Cx}{c}
=\mu-\frac{\mu^2}{c}b^*S^{-1}b\le\mu.
\tag{7}
\]

Therefore any positive original gap remains at most \(\delta/(\delta+c)\), exactly as in the source advisory. The precise weighted equivalence is \(F\ge\gamma I\iff C\ge\gamma M\). In particular, a reduced certificate \(F\ge\gamma I>0\) transfers as

\[
C\ge\gamma M\ge\gamma\frac{\delta}{\delta+c}I.
\tag{8}
\]

There is no analogous compulsory upper bound \(\lambda_{\min}(F)\le\mu\). The following finite-dimensional examples establish the distinction; they illustrate what the abstract premises do or do not imply, and make no assertion about additional modes of the actual operator. Unused coefficient coordinates may be padded to 372.

* If \(U=0\) and \(L_0=aI\) with \(a>0\), then \(F=I\) while \(C=M\). The forced constant-mode scale is completely isolated.
* On orthonormal \(e,f\), take \(L=0\), \(W_1=\sqrt c\,e\), and \(W_2=\sqrt d\,f\), with \(c,d>0\). Then \(H\) is uniformly coercive even as \(\delta\downarrow0\), but \(F=\operatorname{diag}(1,\delta/(\delta+d),1,\ldots)\). A second zero mode recreates an \(O(\delta)\) reduced gap.
* Replacing \(Lf=0\) by \(Lf=-a f\), where \(d>a>\delta>0\), leaves \(H>0\) but makes the second reduced entry \((\delta-a)/(\delta+d-a)<0\).

Thus the explicit constant factor is removed from the reduced margin, but other zero modes, negative directions, and small spectral values on \(e^\perp\) remain unexamined. No unverified family of putative null vectors is used here. An independently proved lower bound \(L_0\ge gI>0\) would, for example, give the sufficient reduced margin \((g+\delta)/(g+\delta+\|V\|^2)\) through (6); no such bound is established in this note.

A further conditional consequence is immediate: if a separate domain-valid argument establishes \(\dim\ker L_0=\infty\), then \(\ker L_0\cap\ker U^*\) is infinite-dimensional because \(U\) has finite rank. On that subspace \(Sf=\delta f\), so \(\delta\) is an infinite-multiplicity eigenvalue of \(S\) and \(\|S^{-1}\|\ge\delta^{-1}\). A scalar inverse estimator then cannot be uniform as \(\delta\downarrow0\). The same vectors are eigenvectors of \(H\) with eigenvalue \(\delta\). This is a conditional implication, not a domain proof for any proposed null family.

## Residual estimators and what can actually improve

Let a prospective reduced trial map \(Z:\mathbb C^{372}\to D(S)\) have residual \(R=V-SZ\), and set

\[
J_Z=V^*Z+Z^*V-Z^*SZ.
\]

Exact completion of the square, with no Galerkin assumption, gives

\[
V^*S^{-1}V=J_Z+R^*S^{-1}R,
\qquad
0\le R^*S^{-1}R\le\eta^{-1}R^*R.
\tag{9}
\]

Hence \(I-J_Z-\eta^{-1}R^*R\succ0\) is a sufficient reduced certificate. This can use a nonvanishing reduced margin when the actual \(F\) has one. But the available reduced trial, residual, enclosure cost, and actual margin have not been certified, so a computational benefit does not follow.

In particular, let an existing full-space trial be \(Y:\mathbb C^{372}\to D(H)\), with \(E=W-HY\). The exact prospective transformation

\[
Z=PYQ^{-1},\qquad
R=\left(PE-\frac b\alpha e^*E\right)Q^{-1}
\tag{10}
\]

shows why a small old scalar residual bound need not become a better one. The factor \(\|Q^{-1}\|=\sqrt{(\delta+c)/\delta}\) can amplify errors, in addition to the eliminated-block coupling. Likewise, merely transforming an old matrix-error estimate \(\|\Delta C\|\le\varepsilon\) gives only \(\|Q^{-1}\Delta C Q^{-1}\|\le\varepsilon/\mu\).

The corresponding exact residual energy decomposition is

\[
E^*H^{-1}E
=\alpha^{-1}(e^*E)^*(e^*E)+Q R^*S^{-1}R Q.
\tag{10a}
\]

Conversely, a reduced trial can be lifted algebraically to

\[
Y=e\,\alpha^{-1}(x^*-b^*ZQ)+ZQ.
\tag{11}
\]

Its scalar block equation is exact and \(E=(0,RQ)\). Therefore the exact full residual correction is

\[
E^*H^{-1}E=Q R^*S^{-1}R Q.
\tag{12}
\]

Equations (9) and (12) contain the same information when the anisotropic matrix weights are retained. A scalar norm majorant may discard that structure. Deflation is a principled way to expose and preserve it, and may guide a later trial or estimator, but it is not an unconditional improvement over an equally precise full-space treatment. Equations (10) and (11) are prospective identities only; no frozen trial or pilot has been changed.

## Transfer of the inherited cover bound

The source advisory supplies the fixed-map bound

\[
H_\delta\ge\eta_\delta I,\qquad
\eta_\delta=\delta-\rho,
\]

\[
\rho=
\frac{420589436338386427087719740298403628714618993}
{92620636523388719034562694367509285563269120000000}.
\]

For \(\delta>\rho\), (2) immediately transfers the same certified scalar bound to \(S\):

\[
S\ge(\delta-\rho)I,\qquad
\|S^{-1}\|\le(\delta-\rho)^{-1}.
\tag{13}
\]

The scalar bound need not improve: a direction orthogonal to the eliminated coupling can attain the same lower bound. For \(\delta\le\rho\), this particular cover proves no positive inverse bound for either operator. Deflation does not extend its range of validity; a different coercivity proof would be needed.

There is an optional analytic rank-one refinement. Necessarily \(\alpha\ge\eta\). If \(\alpha>\eta\), completing the square in \(H-\eta I\ge0\) gives

\[
S\ge\eta\left(I+\frac{bb^*}{\alpha(\alpha-\eta)}\right),\qquad
S^{-1}\le\eta^{-1}
\left(I+\frac{bb^*}{\alpha(\alpha-\eta)}\right)^{-1}.
\tag{14}
\]

If \(\alpha=\eta\), positivity forces \(b=0\), and (13)'s general \(\eta\) version applies. For the inherited cover, \(\alpha-\eta_\delta=c+\rho>0\). Formula (14) is a rigorously smaller inverse majorant in the coupling direction and can replace \(\eta^{-1}I\) in (9) if its data can be bounded. Its useful effect on a particular residual, and the cost of obtaining the needed data, remain unknown. It does not remove the cover threshold. No such data were calculated here.

## Exact or enclosed constant overlaps are essential

Applying the reduction requires the complete vector \(x=W^*e\), not just a scalar lower bound on \(c\) or one certified overlap \(x^*t\). The source advisory's \(c>127/64\) is enough for its obstruction but does not determine the direction \(xx^*\), \(U\), or the reduced trial equations.

Acceptable inputs are exact overlaps, or rigorous complex enclosures for all 372 coordinates, tied to the unchanged observation order, normalization, phase signs, conjugations, and whole-line source construction. An interval treatment must contain one consistent exact vector \(x\) throughout \(c=x^*x\), \(U=W-ex^*\), \(M\), and all residual formulas. It may uniformly enclose the identities over those inputs, or explicitly bound every perturbation from an approximate vector. Substituting an interval midpoint as an exact vector is invalid: generally \(e^*(W-e\widehat x^*)=x^*-\widehat x^*\ne0\).

Convenient exact rank-one formulas are

\[
Q=I-\frac{xx^*}{\alpha+\sqrt{\alpha\delta}},\qquad
Q^{-1}=I+\frac{xx^*}{\delta+\sqrt{\alpha\delta}},\qquad
M^{-1}=I+\frac{xx^*}{\delta}.
\tag{15}
\]

They remain valid when \(x=0\) and avoid division by \(c\). Interval square roots and all subsequent arithmetic require outward enclosures. An upper enclosure \(c\le c_+\), as well as the vector direction, is needed to certify a useful lower transfer factor \(\mu\ge\delta/(\delta+c_+)\). This note does not claim that the existing saved inputs already provide a sufficiently narrow full-vector enclosure or a usable reduced residual.

## Verification and final limitation

The block factorization, inverse multiplication, positivity equivalence, and residual identities were checked analytically, including a separate independent algebra review. No exact fatal flaw was found under the stated assumptions. The requirements \(\delta>0\), the unchanged self-adjoint domain containing \(e\), and a proved strictly positive inverse bound are essential. At \(\delta=0\) with \(c>0\), \(M\) is singular and the invertible-congruence conclusions cannot be reused.

The outcome is an exact reparameterization that separates a known bad scale. Certifying the reduced sign, handling any further zero modes, and demonstrating a practical residual advantage are separate unfinished tasks.

This new note is licensed under CC BY-NC 4.0. The referenced advisory and any reused source material retain their stated attribution and rights. See `LICENSE`.
