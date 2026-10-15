# Max: selected mathematical review

This is a selected research-only excerpt of a model-generated review, not a proof certificate or independent peer-review credential. The reviewer did not rehash the original archive bytes. The publication process recomputed the supplied review file identity: 27817 bytes, SHA-256 883454c0c1af27b44828b85b679ed84012a8a9318632a83743c270cb432a5d46.

Selection: original sections 2–7 only. The sentence referring to a fixed mu_0 is omitted. Original sections 8–11 are excluded. The original notation kappa_g for the positive lower bound is preserved in this excerpt; the adopted theorem uses c_coer = omega delta_0 + theta j_7, to avoid the source offset-name collision. The exact historical a is supplementary; arbitrary a > 0 is sufficient.

**2. 실제 구간 분할과 모든 shift edge의 확인**

[J 129–185; SIX 67–95; I 119–162]

양의 로그 급수와 꼬리식
\[
L_N(z)=2\sum_{j=0}^{N-1}\frac{z^{2j+1}}{2j+1},\qquad
0<\log\frac{1+z}{1-z}-L_N(z)
<\frac{2z^{2N+1}}{(2N+1)(1-z^2)}
\]
에서 직접
\[
\frac{842}{1215}<t<\frac{23581}{34020},\qquad
\frac{7379}{6720}<u<\frac{33223}{30240}
\]
를 얻습니다. 따라서 원문의
\[
\frac{693}{1000}<t<\frac{694}{1000},\qquad
\frac{1098}{1000}<u<\frac{1099}{1000}
\]
가 성립합니다. 또한
\[
\log5>
2\left(\frac23+\frac{(2/3)^3}{3}+\frac{(2/3)^5}{5}\right)
=\frac{1924}{1215}>\frac32.
\]

이 유리수 구간으로 다음을 모두 확인할 수 있습니다.
\[
2u-t>2B,\quad4t-u>2B,\quad t+u>2B,\quad
3t-u>B,\quad 2t<2B<\log5.
\]

이제
\[
r_0=B-t,\qquad v_g=u-t,\qquad w_g=2t-u
\]
로 놓습니다. 양의 반구간은 다음처럼 정확히 분할됩니다.

| 물리적 구간 | 이를 채우는 실제 좌표 |
|---|---|
| \((0,r_0)\) | seven의 중앙 좌표 \(x\) |
| \((r_0,w_g-r_0)\) | path의 \(s-u+t\) |
| \((w_g-r_0,w_g+r_0)\) | seven의 \(x+w_g\) |
| \((w_g+r_0,v_g-r_0)\) | pair의 \(y\) |
| \((v_g-r_0,v_g+r_0)\) | seven의 \(x+v_g\) |
| \((v_g+r_0,t-r_0)\) | path의 \(s\) |
| \((t-r_0,B)\) | seven의 \(x+t\) |

음의 구간은 나머지 좌표가 한 번씩 채웁니다. 여기서
\[
J=(-r_0,r_0),\quad
I=(u+B-2t,\,2t-B),\quad
K_0=(B+t-u,\,u-B)
\]
이고, 좌표들은 정확히
\[
\begin{aligned}
\xi_7(x)&=(x,x+t,x-t,x+v_g,x-v_g,x+w_g,x-w_g),\\
\xi_4(s)&=(s-t,s,s-u,s-u+t),\\
\xi_2(y)&=(y-t,y)
\end{aligned}
\]
입니다. **이 좌표들에 별도의 \(\pm\) 복사본을 추가하면 중복됩니다.**

모든 좌표변환의 Jacobian은 \(1\)입니다. 전체 길이도
\[
7|J|+4|I|+2|K_0|
=14(B-t)+4(4t-u-2B)+2(2u-t-2B)=2B
\]
와 일치하며, 위 구간표는 길이 일치보다 강한 무중복 전사성을 보여줍니다.

실제 adjacency는 다음 edge로 완전히 지정됩니다. 행렬은 대칭이고 나머지 성분은 \(0\)입니다.

| 블록 | \(c_2\) edge | \(c_3\) edge | \(c_4\) edge |
|---|---|---|---|
| seven | \(12,13,47,56\) | \(25,34\) | \(23\) |
| path | \(12,34\) | \(23\) | 없음 |
| pair | \(12\) | 없음 | 없음 |

완전성은 다음 구조로 확인됩니다.

- 모든 \(2t\) edge의 중점은 \(J\)에 있으므로 seven에 포함됩니다.
- 모든 \(t\)-이동 triple의 중앙점도 \(J\)에 있습니다.
- \(u\)-edge의 끝점 집합은
  \[
  (u-B,B)\cup(-B,B-u)
  \]
  입니다. 각 끝점에는 inward \(t\)-이웃이 하나 있고, 두 inward 영상의 교집합은 \(J\)입니다.
- seven을 제거하면 남은 \(u\)-edge는 서로 다른 두 \(t\)-이웃과 함께 path를 이룹니다. 나머지는 위 pair 구간입니다.
- 나머지 shift가 구간을 벗어난다는 것은 \(2u-t>2B,\ 4t-u>2B,\ t+u>2B\)로 확인됩니다.

따라서 누락된 양의 측도 isolated 구간이나 추가 edge가 없습니다. seven의 최대 degree는 \(3\)입니다.

이로써
\[
\mathcal U:L^2(\Omega)\longrightarrow
L^2(J;\mathbb C^7)\oplus L^2(I;\mathbb C^4)\oplus L^2(K_0;\mathbb C^2)
\]
는 unitary입니다. 이는 \(L^2\) 대표의 평행이동에 관한 명제입니다. 평행이동은 영집합을 보존하므로 추상적 \(L^2\) 원소의 점값을 선택할 필요가 없습니다.

각 무방향 edge의 기여는
\[
2c\,\operatorname{Re}(\overline{z_i}z_j)
\]
입니다. 따라서 \(aI+C_g\)의 비대각은 **\(-c\)** 이며, \(-2c\)가 아닙니다. \(n=4\)도 seven의 \(23\) edge 하나로 정확히 포함됩니다.

반사는
\[
x\mapsto-x,\qquad s\mapsto u-s,\qquad y\mapsto t-y
\]
와 원문에 적힌 정점 순열로 구현됩니다. 복소켤레는 들어가지 않습니다.

**3. 두 가중치 체계의 독립 검산**

먼저 [J 189–203]의 joint reserve입니다. 양의 \(d_i\)에 대해
\[
c\left[
\frac{d_j}{d_i}|z_i|^2+\frac{d_i}{d_j}|z_j|^2
-2\operatorname{Re}(\overline{z_i}z_j)\right]
=cd_id_j\left|\frac{z_i}{d_i}-\frac{z_j}{d_j}\right|^2.
\]
이는 모든 복소 phase에 대해 정확합니다.

계수 상계
\[
c_2<\frac12,\qquad c_3<\frac{13}{20},\qquad c_4<\frac7{20}
\]
도 위 로그 구간과 제곱근의 유리수 비교에서 따릅니다.

실제 weighted row를
\[
d_i^{\rm act}=\sum_{j\sim i}c_{ij}\frac{d_j}{d_i}
\]
라 하면 다음과 같습니다.

| 정점 | joint 가중치 | 실제 weighted row | \(\bar d_i\) |
|---|---:|---:|---:|
| seven center | \(10/9\) | \(\frac95c_2\) | \(9/10\) |
| seven \(t\) | \(1\) | \(\frac{10}{9}c_2+\frac9{10}c_3+c_4\) | \(2683/1800\) |
| seven \(v_g\) | \(9/10\) | \(\frac59c_2+\frac{10}{9}c_3\) | \(1\) |
| seven \(w_g\) | \(1/2\) | \(\frac95c_2\) | \(9/10\) |
| path leaf | \(3/5\) | \(\frac53c_2\) | \(5/6\) |
| path interior | \(1\) | \(\frac35c_2+c_3\) | \(19/20\) |
| pair | \(1\) | \(c_2\) | \(1/2\) |

특히 큰 행은
\[
\frac59+\frac{117}{200}+\frac7{20}
=\frac{2683}{1800}
\]
로 맞습니다.

예를 들어
\[
\varepsilon_2=\frac12-c_2,\quad
\varepsilon_3=\frac{13}{20}-c_3,\quad
\varepsilon_4=\frac7{20}-c_4
\]
라 쓰면 \(t\)-행의 slack은 정확히
\[
\bar d_t-d_t^{\rm act}
=\frac{10}{9}\varepsilon_2+\frac9{10}\varepsilon_3+\varepsilon_4\ge0.
\]
다른 행도 표의 계수대로 비음수 slack을 갖습니다. 따라서
\[
\boxed{\operatorname{diag}(\bar d_i)-A_C\succeq0}
\]
가 edge square와 row slack의 합으로 직접 증명됩니다.

다음은 별도의 [SIX 102–126] \(6/5\) 가중치입니다.
\[
(w_{\rm center},w_t,w_v,w_w)=\left(\frac56,1,\frac23,\frac5{18}\right).
\]

| 정점 | \(\sum c_{ij}w_j\)의 상계 | \((6/5)w_i\) | 상계 기준 slack |
|---|---:|---:|---:|
| center | \(1\) | \(1\) | \(0\) |
| \(t\) | \(\frac5{12}+\frac{13}{30}+\frac7{20}=\frac65\) | \(6/5\) | \(0\) |
| \(v_g\) | \(\frac{13}{20}+\frac5{36}=\frac{71}{90}\) | \(4/5\) | \(1/90\) |
| \(w_g\) | \(1/3\) | \(1/3\) | \(0\) |

path에는 일정 가중치를 쓰면 최대 행합이
\[
c_2+c_3<\frac{23}{20}<\frac65
\]
이고 pair는 더 작습니다. 각 edge에
\[
2|z_i z_j|
\le \frac{w_j}{w_i}|z_i|^2+\frac{w_i}{w_j}|z_j|^2
\]
를 적용하면
\[
|z^*A_Cz|\le\frac65\|z\|^2.
\]
따라서 각 실제 블록에서
\[
\boxed{\|A_C\|_{\rm op}\le\frac65}
\]
이며, 적분하면 모든 복소 \(L^2(\Omega)\) 함수에 대해 같은 bound를 얻습니다.

두 가중치 체계는 용도가 다릅니다. 첫 번째는 위치별 퍼텐셜과 결합할 \(\bar d\)를 만들고, 두 번째는 adjacency의 양쪽 operator norm을 제어합니다.

**4. 내부 kernel, 완전한 exterior reserve와 위치별 \(p_g\)**

[J 98–124; INTERNAL 114–153; I 78–83]

\(z=s/2\)로 두면
\[
k(s)=\frac14\left(\operatorname{csch}z-\frac1z+\operatorname{sech}z\right).
\]
양의 급수에서
\[
\operatorname{csch}z>\frac1z-\frac z6,\qquad
\operatorname{sech}z>1-\frac{z^2}{2}
\]
가 따릅니다. 따라서 \(0<z\le3/4\)에서
\[
k(s)>
\frac14\left(1-\frac z6-\frac{z^2}{2}\right)
\ge\frac{19}{128}.
\]
또 \(\sinh z\ge z,\ \cosh z\ge1\)로 \(k(s)\le1/4\)입니다. 연속 연장까지 포함하여
\[
\boxed{\frac{19}{128}\le k(s)\le\frac14,\qquad 0\le s\le\frac32.}
\]

단조성도 원문 논증으로 성립합니다. \(A=z^2\le9/16\)에 대해
\[
\frac{\sinh z}{z}\le\frac1{1-A/6},\qquad
\cosh z\ge1+\frac A2,
\]
\[
(1+A/2)(1-A/6)^2-1
=\frac{A(12-10A+A^2)}{72}>0.
\]
따라서 \(z^2\cosh z>\sinh^2z\)이고
\[
\left(\operatorname{csch}z-\frac1z\right)'<0,\qquad
(\operatorname{sech}z)'<0.
\]
즉 \(k'(s)<0\)입니다.

완전한 tail은
\[
R(s)=\operatorname{artanh}(e^{-s/2})+\arctan(e^{-s/2}),
\qquad R'=-\rho
\]
이며,
\[
F_k(s)=\int_0^s k(t)\,dt
\]
에 대해
\[
R(s)+F_k(s)=\log2+\frac\pi4-\frac12\log s.
\]
이는 미분과 \(s\downarrow0\) 극한으로 확인됩니다.

따라서
\[
\Delta_\Gamma(x)
=V_{\rm full}(x)-V_0-W_B(x)
=2F_k(B)-F_k(B+x)-F_k(B-x).
\]
\(F_k\)의 오목성으로 \(\Delta_\Gamma\ge0\)이고, \(x\ge0\)에서는
\[
\Delta_\Gamma(x)
=\int_0^x[k(B-t)-k(B+t)]\,dt
\le\frac{13}{128}x\le\frac{39}{512}.
\]
즉
\[
\boxed{0\le\Delta_\Gamma\le\frac{39}{512}.}
\]
여기서는 \(k\)를 무한구간에서 적분하거나 exterior tail을 자르지 않았습니다.

이제 [J 217–234]의 위치별 reserve를 검산합니다. \(t>69/100\)에서
\[
W_B(2t-B)>
\frac12\log\frac{625}{184}.
\]
\(z=441/809\)를 쓰면
\[
\frac12\log\frac{625}{184}
=\operatorname{artanh}z
>z+\frac{z^3}{3}
=\frac{317214828}{529475129}.
\]
원문의 마지막 비교도 정확합니다.
\[
\frac{317214828}{529475129}-\frac{1063}{1800}
=\frac{8154628273}{953055232200}>0.
\]
또
\[
W_B(u-B)>
\frac12\left(\frac{34}{75}\right)^2
=\frac{578}{5625},\qquad
\frac{578}{5625}-\frac1{10}=\frac{31}{11250}>0.
\]

seven의 \(t\)-정점에는 \(|x|\ge2t-B\), \(v_g\)-정점에는 \(|x|\ge u-B\)가 적용됩니다. path의 두 내부 정점도 \(|x|>u-B\)입니다. 따라서
\[
\eta=W_B+\frac9{10}-\bar d
\]
는 정점 종류별로
\[
W_B,\quad W_B-\frac{1063}{1800},\quad W_B-\frac1{10},
\quad W_B+\frac1{15},\quad W_B-\frac1{20},\quad W_B+\frac25
\]
중 하나이며 모두 비음수입니다.

결국
\[
\boxed{p_g=\omega\eta\ge0.}
\]
이 단계는 큰 graph row와 해당 정점의 물리적 위치를 결합한 증명입니다. 퍼텐셜의 독립적인 전역 최솟값으로 치환한 증명이 아닙니다.

**5. SAUDIT의 scalar 증명과 정확한 \(a\)**

[SAUDIT 28–38; GRAPH 299–303]

먼저
\[
\int_0^1\frac{x^4(1-x)^4}{1+x^2}\,dx=\frac{22}{7}-\pi>0
\]
이므로 \(\pi<22/7\)입니다. 이 항등식은 다항식 나눗셈으로 직접 확인됩니다.

Euler 상수에는
\[
b_n=H_n-\log(n+1/2)
\]
를 쓰면
\[
b_n-b_{n+1}
=2\operatorname{artanh}\frac1{2n+2}-\frac1{n+1}>0.
\]
따라서 \(b_n\downarrow\gamma_E\)이고
\[
\gamma_E<H_5-\log(11/2).
\]
\(y=9/13\)인 양의 atanh 급수의 처음 일곱 항은 각각 다음 유리수보다 큽니다.
\[
\frac1{10000}(13846,\ 2212,\ 636,\ 217,\ 81,\ 31,\ 12).
\]
그 합은
\[
\frac{3407}{2000}>\frac{511}{300}.
\]
그러므로
\[
\boxed{\gamma_E<\frac{137}{60}-\frac{511}{300}=\frac{29}{50}.}
\]

SAUDIT의 두 exp 비교도 유한 양의 합으로 충분합니다.
\[
\sum_{j=0}^{5}\frac{(23/20)^j}{j!}
>\frac{3152}{1000}>\frac{22}{7},
\]
\[
\sum_{j=0}^{7}\frac{(46/25)^j}{j!}
>\frac{6289}{1000}>\frac{44}{7}.
\]
따라서
\[
\log\pi<\frac{23}{20},\qquad
\log(2\pi)<\frac{46}{25}.
\]
이로써
\[
\Lambda_a=\log(2\pi)+\gamma_E<\frac{121}{50},
\]
\[
c_\Gamma
<\frac{23}{20}+\frac35+\frac{11}{7}+\frac{21}{10}
=\frac{759}{140}<\frac{383}{70}.
\]
특히
\[
\boxed{j_7=\frac{29}{5}-c_\Gamma>\frac{53}{140}>\frac{23}{70}>0.}
\]
원문이 사용하는 약한 하계 \(23/70\)는 유효합니다.

\(\delta_0\)도 직접 증명됩니다. \(z=B/4=3/16\)에 대해
\[
(3+z^2)z\cosh z-(3+2z^2)\sinh z
=\sum_{n=2}^{\infty}
\frac{8n^2(n-1)}{(2n+1)!}z^{2n+1}>0.
\]
따라서
\[
z\coth z\ge1+\frac{z^2}{3+z^2}
=1+\frac3{259}.
\]
\(u_0=3/259\)라 하면
\[
2\operatorname{artanh}(e^{-B/2})=\log\coth z,
\]
\[
2\arctan(e^{-B/2})\ge\frac\pi2-\frac B2.
\]
뒤의 식은 \(B\)에 대한 도함수가 \(-1/(2\cosh(B/2))\)인 데서 따릅니다. 여기에
\(\log(1+u_0)\ge u_0-u_0^2/2\)를 결합하면
\[
2R(B)-c_\Gamma
\ge\log(4/3)-\Lambda_a-\frac38+u_0-\frac{u_0^2}{2}.
\]
따라서
\[
\begin{aligned}
\delta_0
&>\frac52+\frac27-\frac{121}{50}-\frac38
  +\frac{1545}{134162}\\
&=-\frac{13}{1400}+\frac{1545}{134162}
=\frac{209447}{93913400}>0.
\end{aligned}
\]
즉 후대 SAUDIT는 이 국소 scalar 공백을 실제로 해소합니다.

마지막으로 유한 조화합은
\[
H_{32}=\frac{586061125622639}{144403552893600}
\]
이며, 이를 정의에 대입하면
\[
\boxed{
a=\frac{65535}{65536}\left(H_{32}-\frac{4067}{1280}\right)
-\frac8{65536}
=\frac{261572074620463589}{296898235056783360}.
}
\]
차이는 정확히
\[
a-\frac45
=\frac{24053486575036901}{296898235056783360}>0.
\]
GRAPH의 과거 checker 판정을 사용하지 않아도 이 등식과 부호는 유리수 연산으로 확인됩니다.

**6. 실제 \(M_C\) 항등식과 \(C_g\) 자체의 하계**

[I 64–117, 164–178]

원문의 정의를 전개하면
\[
C_g[q]
=\int_\Omega\gamma_g|q|^2-P_B[q],
\]
\[
\gamma_g
=\omega(V_{\rm full}-V_0+9/10+\delta_0)+\theta(7-c_\Gamma)
=\omega V_{\rm full}+\frac{17}{5}\omega+7\theta-c_\Gamma.
\]
\(P_B\)의 계수는 \(\omega+\theta=1\) 때문에 정확히 \(1\)입니다.

여기서 중요한 중간식은
\[
\boxed{
\gamma_g-\omega\bar d
=p_g+\omega(\Delta_\Gamma+\delta_0)+\theta(7-c_\Gamma).
}
\]
좌변에서 \(\theta c_\Gamma\)를 다시 빼는 식은 틀립니다.

실제 각 fiber에서
\[
M_C=\operatorname{diag}(a+\gamma_g(\xi_i))-A_C
\]
이고, 따라서
\[
\begin{aligned}
M_C-\operatorname{diag}(a+p_{g,i})
={}&\omega\left[
\operatorname{diag}(\bar d_i)-A_C
+\operatorname{diag}(\Delta_{\Gamma,i}+\delta_0)\right]\\
&+\theta\left[(7-c_\Gamma)I-A_C\right].
\end{aligned}
\]
앞에서 독립적으로 증명한 두 graph bound를 적용하면
\[
(7-c_\Gamma)I-A_C\succeq j_7I
\]
이므로
\[
\boxed{
M_C\succeq
\operatorname{diag}(a+p_{g,i}+\omega\Delta_{\Gamma,i})
+(\omega\delta_0+\theta j_7)I.
}
\]
요청한 원문 부등식은 즉시 따릅니다.

특히 \(C_g\) 자체에는 다음 하계가 적용됩니다.
\[
\boxed{
C_g[q]\ge
\int_\Omega(p_g+\omega\Delta_\Gamma)|q|^2
+(\omega\delta_0+\theta j_7)\|q\|^2.
}
\]
따라서
\[
C_g[q]\ge\kappa_g\|q\|^2,\qquad
\kappa_g:=\omega\delta_0+\theta j_7>0.
\]
이는 **실제 edge square, scalar 하계 및 위치 결합에서 나온 결과**입니다. 유한 블록이라는 이유로 얻은 양성이 아닙니다. 또한 이 하계의 상수는 \(a\)가 아닙니다.

이 식들은 보존된 항들의 중복 사용도 배제합니다. \(\delta_0,\Delta_\Gamma,\theta J_7\)는 이미 \(C_g\)에 들어 있으며, 별도의 독립 gain으로 다시 더할 수 없습니다.

**7. 전공간 inverse fields와 닫힌 보조 형식**

[I 185–235]

\[
D_g=\left\{q\in L^2(\Omega):
\int_\Omega V_{\rm full}|q|^2<\infty\right\}
\]
로 둡니다. \(V_{\rm full}\)은 내부에서 연속이고 끝점에서 로그로 발산합니다. 각 열린 parameter 구간에서 \(M_C\)는 연속이며
\[
M_C\succeq(a+\kappa_g)I.
\]
따라서
\[
M_C^{-1}=\frac{\operatorname{adj}M_C}{\det M_C}
\]
는 measurable이고
\[
\|M_C^{-1}\|\le\frac1{a+\kappa_g}\le\frac1a.
\]
끝점의 행렬값은 정할 필요가 없습니다.

다음 형식을 전공간 \(L^2(\Omega)\)에서 정의합니다.
\[
\mathfrak a_g[q]=a\|q\|^2+C_g[q],\qquad D(\mathfrak a_g)=D_g.
\]
그 대각 곱셈항은
\[
m_g(x)=a+\gamma_g(x)
=\omega V_{\rm full}(x)+\text{상수}
\]
입니다. \(m_g>0\)이고 \(\int m_g|q|^2\)는 닫힌 곱셈 형식입니다. 그 정의역은 \(D_g\)와 같습니다. \(C_c^\infty(\Omega)\subset D_g\)이므로 조밀합니다.

이제 bounded self-adjoint adjacency를 빼면 닫힘과 정의역이 보존됩니다. 따라서
\[
\mathfrak a_g[q]\ge(a+\kappa_g)\|q\|^2
\]
인 닫힌 조밀 형식이 얻어집니다. 그 associated operator가 \(A_g^{\rm op}\)이고
\[
\boxed{T_g=(A_g^{\rm op})^{-1}}
\]
가 전공간에서 존재합니다. unitary fiber 표현 아래에서는 정확히 \(M_C^{-1}\)입니다.

보다 구체적으로 bounded perturbation 성질로
\[
D(A_g^{\rm op})
=\{q:m_gq\in L^2\}
=\{q:V_{\rm full}q\in L^2\}.
\]
이는 form domain \(D_g\)보다 강한 조건입니다.

\(u=T_gf\)이면
\[
\mathfrak a_g[u]=\langle u,f\rangle
\le\frac{\|f\|^2}{a+\kappa_g}.
\]
또
\[
m_gu=f+A_{\rm graph}u\in L^2.
\]
따라서 응답 \(u\)의 operator-domain 및 weighted-domain 소속은 결과로 증명됩니다. 원래 \(z_0=B_*^{-1}Yh\)의 weighted 소속을 가정한 것이 아닙니다.

동일한 이유로 모든 \(\mu\ge0\)에 대해
\[
\boxed{
T_{g,\mu}=(A_g^{\rm op}+\mu I)^{-1}
=\mathcal U^{-1}(M_C+\mu I)^{-1}\mathcal U,
\quad
\|T_{g,\mu}\|\le\frac1{a+\kappa_g+\mu}.
}
\]

이 보조 연산자는 앞서 \(A_b\)로 썼던
\[
(a+\textstyle\frac{17}{5}\omega+7\theta-c_\Gamma)I
+\omega V_{\rm full}-A_{\rm graph}
\]
와 같은 대상입니다. 원래 weighted minimum 연산자나 physical high operator가 아닙니다.

반사와의 가환성은 실제 좌표 순열과 \(V_{\rm full}\)의 짝성에서 따릅니다. 따라서 \(T_g,T_{g,\mu}\)는 even subspace를 보존합니다. **low/high 투영과의 가환성은 여기서 따라오지 않습니다.**

또 [I 214–218]의
\[
p_g-\omega V_{\rm full}
=\omega(9/10-\bar d-V_0-\Delta_\Gamma)
\]
는 bounded 함수이므로
\[
D_g=D_{p_g}
\]
입니다. 이는 두 보조 곱셈 **form domain** 사이의 등식입니다.

반대로 \(D_g\)는 \(L^2\)-닫힌 집합이 아닙니다. 끝점 거리 \(d\)에 대해, 작은 구간에서
\[
|q|^2=\frac1{d(\log(1/d))^2}
\]
로 잡으면 \(q\in L^2\)지만
\[
V_{\rm full}|q|^2\asymp\frac1{d\log(1/d)}
\]
는 적분되지 않습니다. 끝점에서 자른 함수들은 \(D_g\)에 속하면서 \(q\)로 \(L^2\)-수렴합니다. 닫혀 있는 것은 \(\mathfrak a_g\)의 **형식 노름에 관한 완비성**입니다.

