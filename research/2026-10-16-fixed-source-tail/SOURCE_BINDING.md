# Publication note

This is the historical pre-computation input-binding note, with only local source-root paths replaced by source archive descriptions. The later completed computation is preserved in source_tail_M128/. The original Y0 tuple/raw rows were not recovered or used. Selected source excerpts and scalar fields are in sources/.

# Fixed h_A source-tail input binding

Read-only source recovery, 2026-10-15 UTC. No source quadrature, numerical source-tail evaluation, response calculation, new witness or q selection, external request, or old checker execution. A small independent Fraction calculation checked the printed scalar remainder formulas against DESIGN.

## Result

The entire k96 polynomial-kernel output lies below M=128. Its maximal degree on the full low16 space is 126; the particular frozen h_A has degree 28, so its maximal output degree is 124. The actual source tail therefore reduces to the complete logarithm-minus-prime-shift tail plus a rigorously bounded complete kernel/pole remainder. The finite shifted functions themselves are not finite Legendre polynomials, so their infinite tails remain in the calculation.

The old reference Y0's precise independent reference tuple and signed raw rows are not locally recovered. Do not invent them. They are unnecessary if the new finite tail certificate is defined at the actual B and actual logarithms/coefficient values, with interval enclosures of those values.

## Source abbreviations and exact lines

- G = historical graph-coercivity source archive
- C = historical coupled-Schur source archive
- G/SIX_MAIN_PROOF.md:236–251: actual basis, mixed source, k, W, both shift directions, and n=2 overlap.
- G/SIX_MAIN_PROOF.md:298–306: physical polynomial normalization, q_r basis, k96 and complete regular outputs through 126, fixed M=128.
- G/SIX_MAIN_PROOF.md:308–329: signed raw rows, exact logarithmic moments and prime-shift moments, independent reference-box construction. These are definitions, not a recovered 49-row array.
- G/SIX_MAIN_PROOF.md:331–367: complete Ek and cosh tails, recurrences, parameter error and eop; the error proof is a source proof sketch with explicit bounds.
- G/SIX_MAIN_PROOF.md:397–403: complete pole control and explicit coverage of nonpolynomial regular/pole tails.
- G/GRAPH_AUDIT.md:34–37: k(s)=[csch(s/2)-2/s+sech(s/2)]/4.
- C/sources/response_link/MAIN_PROOF.md:238–256: inherited ||Y_actual−Y0||≤eop||h_A||, ||Y0||≤28||h_A||, and distinct inverse/row error.
- C/sources/fixed_inputs/DESIGN.json:21–71: kernel order and regular outputs; 72–124: M and low/log orders; 125–150: independent boxes; 151–154: exact Ek, low/high cosh tails; 170: complete support/tail design statement.
- C/sources/fixed_inputs/EXACT_FIXED_DIRECTION.json:6–42: actual h_A vector and norm. This is not the later witness printed in SIX_MAIN_PROOF.md:405–422.

## 1. Exact degree-96 construction recovered algebraically

Let z=s/2, a=3/4, and define

    U_0=V_0=1,
    U_n=−sum_{j=1}^n U_{n−j}/(2j+1)!,
    V_n=−sum_{j=1}^n V_{n−j}/(2j)!,   1≤n≤48.

The actual polynomial described by the source recurrence is

    k96(s)=(1/4)[sum_{n=1}^{48} U_n(s/2)^{2n−1}
                         +sum_{n=0}^{48} V_n(s/2)^{2n}].

It has odd powers at most 95 and even powers at most 96. This formula is derived from the exact k identity and the source's inverse recurrences; the available source does not separately print a full k96 coefficient array.

For an input monomial y^j and an even exponent l, the integral of |x−y|^l y^j on (−B,B) is a polynomial in x of degree at most l. For odd l, split the integral at y=x; each piece has degree at most l+j+1. Consequently

    deg K_k96 h ≤ max(96,95+deg h+1) ≤126.

For even h the output is even. For the fixed h_A, z_15=0 and z_14≠0 imply deg h_A=28, hence degree at most 124. Therefore the projection onto all even m≥130 annihilates K_k96 h_A exactly. No floating-point orthogonality test is needed.

## 2. Complete uniform remainder and scalar identity checks

For j≥1 define

    Tail(j,e)=a^{2j}/(2j+e)! /
              [1−a²/((2j+e+1)(2j+e+2))], e∈{0,1}.

Then the source's exact rational bound is

    Ek=(1/4)sum_{n=0}^{48}a^{2n}
           [|U_n|Tail(49−n,1)/a+|V_n|Tail(49−n,0)].

The recurrence makes (sinh z/z)U(z)−1 and cosh(z)V(z)−1 vanish through degree 96. Bound their remaining full products by the positive factorial tails above, then divide by sinh(z)/z≥1 or cosh(z)≥1. In the first expression additionally divide by z; all surviving powers are at least 98 before this division, so their maximal bound on 0≤z≤a is obtained at a. This proves

    sup_{0≤s≤3/2}|k(s)−k96(s)|≤Ek.

Schur's integral bound gives ||K_k−K_k96||≤2B Ek=(3/2)Ek.

Let

    th=(3/8)^32/[32!(1−(3/8)^2/(33·34))],
    tl=(3/8)^50/[50!(1−(3/8)^2/(51·52))].

The complete Taylor remainder after degree 30 for cosh(x/2) is bounded by th on |x|≤B. Hence ||Pi_high cosh(x/2)||≤sqrt(2B)th. Also |M(h)|≤sqrt(2B)cosh(B/2)||h|| and cosh(3/8)<3/2. Thus

    ||Pi_high[2M(h)cosh(x/2)]||≤(9/2)th||h||.

The independent small exact-Fraction check performed here returned:

    computed Ek == Fraction(DESIGN.kernel_error): true
    computed th == Fraction(DESIGN.pole_high_tail): true
    computed tl == Fraction(DESIGN.pole_low_tail): true
    Ek < 10^(−31): true

This checks exact scalar consistency and the stated elementary remainder derivation. It does not audit the old raw rows or run their original certificate.

## 3. Original eop and an actual-parameter tail reduction

The sources retain

    d=10^(−96),
    epar=4(23sqrt(d)+20700d)+26d,
    eop=epar+(3/2)Ek+(9/2)th.

SIX:361–367 explains the 23/20700 low-space sup/derivative estimates, endpoint-strip/interior translation payment, overlap-safe shift norm, prime coefficient errors, regular derivative and coefficient changes. Response-link:238–245 explicitly applies this whole-source operator error to h_A. Its use is inherited; the precise old Y0 reference constants/raw row array are absent. The row error in response-link:254–256 is a different error and must not be substituted for the source tail.

For a fresh certificate at actual physical parameters, set

    Omega=(−3/4,3/4), B=3/4,
    W_B(x)=−(1/2)log(1−(x/B)^2),
    S_nh(x)=1_{|x−log n|<B}h(x−log n)
                         +1_{|x+log n|<B}h(x+log n),
    c2=log2/sqrt2, c3=log3/sqrt3, c4=log2/2,
    F=W_B h_A−c2S_2h_A−c3S_3h_A−c4S_4h_A.

Let T=I−Pi_even,0:128 on the full even L2 space. Equivalently, on high L2 it is I−Pi_32:128. The actual source identity and Section 1 give

    T Y_actual = T F + r,
    ||r||≤epsilon_regpole ||h_A||,
    epsilon_regpole=(3/2)Ek+(9/2)th≤eop.

Thus any certified sigma_F≥||T F|| gives

    ||T Y_actual||≤sigma_F+eop sqrt(H_A).

Keeping eop, rather than silently removing its epar term, preserves the full inherited allowance conservatively. This equation does not identify F with Y0, omit the pole, or assert the actual kernel tail is zero. Only the polynomial surrogate is annihilated. One may instead use epsilon_regpole if explicitly reporting this newly proved actual-parameter bound.

## 4. Minimal fixed data for a finite complete-tail certificate

The computation needs no fhat, response q, inverse D, source-row archive, new witness, or matrix optimization. Its minimal fields are:

1. B=3/4, M=128, the exact fixed vector z below, its q_r normalization and exact H_A.
2. Actual log2, log3, 1/sqrt2, 1/sqrt3 with certified outward scalar boxes; preserve log4=2log2 and c4=log2/2. A box is not permission to pretend an arbitrary center is the old Y0.
3. Actual signed F above, both directions and overlap; the complete orthonormal Legendre projection through even degree 128, including degrees 0 through 30.
4. Ek/th/eop exact definitions above or the hash-bound DESIGN values.
5. Certified whole squared norm N_F and a certified lower bound L_prefix for the complete finite projection squared norm, with dependency/cancellation preserved.

In normalized coordinates p(t)=sum z_r(1−t²)^r and E0=(1/2)integral_{−1}^1, define d_n=log n/B and

    Fnorm(t)=W(t)p(t)
      −sum_n c_n[1_{|t−d_n|<1}p(t−d_n)
                          +1_{|t+d_n|<1}p(t+d_n)].

Then F(Bt)=Fnorm(t)/sqrt(2B), and exactly

    ||T F||² = E0|Fnorm|²
            −sum_{m=0,2,...,128}(2m+1)|E0[P_m Fnorm]|².

A finite interval proof can enclose the complete norm and finite moments, split at every actual shift breakpoint ±(d_n−1) inside (−1,1), and handle endpoint logarithms analytically. There is no discretization cutoff replacing an infinite tail. Squaring separate log/prime norm bounds would lose all their cross terms; joint integration retains them. Use outward lower bounds on squared projection coefficients when subtracting; do not subtract an upper bound. If interval cancellation leaves a large upper bound, report that bound honestly. A negative calculated upper indicates an invalid enclosure or arithmetic, not a negative squared norm.

Important: subtracting only modes 32 through 128 from ||F||² is a valid but looser upper, not the exact tail identity. The exact identity above also removes low modes 0 through 30.

No sharp N_F, prefix moment boxes, or sigma_F are already present. They are the bounded new finite certificate to construct. No actual tail norm or sign is evaluated in this source-recovery task.

## 5. Frozen vector and scalar boxes

    h_A(x)=p(x/B)/sqrt(2B), p(t)=sum_{r=0}^{15} z_r(1−t²)^r,
    z_r=(following integer)/10^40, in increasing r:

    884351983967001038388331032596
    -502321837179064112839811328004231
    14509739799896203918326523756319811
    -562787878490855011292385604558939089
    6582678899548170799955716813164265416
    -62869017447138396875579041436094283534
    345791616887914584960143929918826122523
    -1381165343232929927534220936797235845154
    3773581980154536045573490326670682760628
    -7337032198660275428997544229909213386698
    10000000000000000000000000000000000000000
    -9360438831407715275689616329058430296064
    5738193775203278363838494921778516145792
    -2073842823697641824667023077981269579416
    335310163392811078007715607984939805155
    0

    H_A = 3096614778920389894432065374494561808298054428938646838502210033521263934729035695524507073/4677400725520733437500000000000000000000000000000000000000000000000000000000000000000000000000000

Inherited exact scalar enclosure fields from DESIGN:

```json
{
  "L2": [
    "11090354888959124950675713943330825089208002149764084065930880151894297951515115449693813231942699/16000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
    "1732867951399863273543080303645441420188750335900638135301700023733484054924236789014658317491046719/2500000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
  ],
  "L3": [
    "10986122886681096913952452369225257046474905578227494517346943336374942932186089668736157548137320887/10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
    "1373265360835137114244056546153157130809363197278436814668367917046867866523261208592019693517165111/1250000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
  ],
  "r2": [
    "7071067811865475244008443621048490392848359376884740365883398689953662392310535194251937671638207863/10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
    "883883476483184405501055452631061299106044922110592545735424836244207799038816899281492208954775983/1250000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
  ],
  "r3": [
    "1443375672974064411272871951254893639119004378175317190046505816209944180757333364234288488964373813/2500000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
    "5773502691896257645091487805019574556476017512701268760186023264839776723029333456937153955857495253/10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
  ]
}
```

## 6. Minimal verification prompt

Verify only the fixed h_A, B=3/4, low16, k96, M=128 complete-source-tail reduction in this packet. Do not choose a new h or q, change a cutoff/order/precision design, import an old checker, claim a sign, or evaluate an inverse response. Check the exact k96 formula, its polynomial output support, the full Ek and th proofs, physical normalization, and the identity for ||T F||² with all signed logarithm/prime cross terms and both n=2 images. Distinguish the actual-parameter construction from unrecovered old Y0. State the smallest genuinely missing finite enclosures for sigma_F, and whether the complete bound ||T Y_actual||≤sigma_F+eop sqrt(H_A) is justified. If a finite numerical certificate is separately authorized, produce reproducible outward arithmetic for exactly those fields and report failure to close without broadening the task.

## Source byte identities

- historical coupled-Schur source archive/sources/fixed_inputs/DESIGN.json: 9579 bytes; SHA256 `77282ff043ce37f3589dccec3ca1feedda5eebba176736e0819db0412840e6ce`
- historical coupled-Schur source archive/sources/fixed_inputs/EXACT_FIXED_DIRECTION.json: 25572 bytes; SHA256 `a81c85c84fbdce916c677f2c5003adc8b9f274f1ef011f8d14111514ff5f318a`
- historical coupled-Schur source archive/sources/response_link/MAIN_PROOF.md: 27306 bytes; SHA256 `28d482ff16e4248dfe911d825abe10d68dd1ce454a9036f1604c3e709ec6e5a3`
- historical graph-coercivity source archive/SIX_MAIN_PROOF.md: 22827 bytes; SHA256 `469226da39cc94d8947493ea90eb4dbf1af7de32e6b2fce86ff6b6bce0a65c74`
- historical graph-coercivity source archive/GRAPH_AUDIT.md: 12255 bytes; SHA256 `76354de63517a31c5ae6c4bcf385be9d89e1805eed29a92c9cdf62777fd52842`

## 7. Closed moments for the 65-mode certificate (analytic formulas only)

For k≥0 let H_j=sum_{i=1}^j1/i and

    D_k=2H_{2k+2}−H_{k+1}−2log2.

Then

    E0[t^{2k} W(t)] = D_k/[2(2k+1)],
    E0[t^{2k} W(t)^2]
      =[D_k²+4sum_{j=0}^k1/(2j+1)²−pi²/3]/[4(2k+1)].

Odd moments vanish by parity. These follow from the first and second beta-parameter derivatives of (1/2)B(k+1/2,b) at b=1, together with the integer/half-integer digamma and trigamma recurrences. They are algebraic identities, not evaluated source coefficients.

Write Sp=sum_{n=2,3,4}c_n S_n p in normalized coordinates. The whole norm splits as

    E0|Fnorm|²=E0[W²p²]−2E0[W p Sp]+E0[(Sp)²].

The first term uses only the whole-interval W² moments above. The second term consists of finite interval polynomial-log moments. The last term consists of finite interval polynomial moments on all branch-pair overlaps, retaining n=2 overlap and every sign. No product of two different logarithmic singularities at shifted arguments occurs because W multiplies only the unshifted p.

For truncated polynomial-log moments define

    J_l(u)=u^(l+1)[log(u)/(l+1)−1/(l+1)²],
    J_l(0)=0 by its continuous endpoint limit.

Valid primitives are

    integral t^j log(1−t)dt
      =−sum_{l=0}^j binom(j,l)(−1)^l J_l(1−t),
    integral t^j log(1+t)dt
      = sum_{l=0}^j binom(j,l)(−1)^(j−l) J_l(1+t).

Their sum times −1/2 is a primitive of t^j W(t). Evaluate over actual interval endpoints with certified outward log bounds. These formulas include the low 0:30 modes, where the source's high-row f_r(m) quotient may have zero denominators and should not be used.

The inherited DESIGN.pi_interval at lines 156–159 is:

[
  "78539816339744830961566084581987572104929234984377645524373614807695410157155224965700870633552926699553702162832057666177346115238764555793/25000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
  "314159265358979323846264338327950288419716939937510582097494459230781640628620899862803482534211706798214808651328230664709384460955058223173/100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
]

No new numerical source evaluations accompany these formulas.
