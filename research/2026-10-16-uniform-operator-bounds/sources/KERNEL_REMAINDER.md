# Complete polynomial-kernel and pole remainder definitions

This mathematical excerpt retains the exact recurrence and proof from the previously published fixed-source binding note. Here B=3/4, and the symbol a=3/4 below is the kernel expansion radius, not the response coercivity constant a. These are distinct constants.

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

