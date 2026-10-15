"""Independent short sanity checks for the source-tail audit (external reviewer).
Exact rationals only. Does NOT rerun the certificate or any 65-mode moment."""
import resource, math, json
resource.setrlimit(resource.RLIMIT_AS, (512 * 1024 * 1024, 512 * 1024 * 1024))
from fractions import Fraction as F

data = {
 "nums": [884351983967001038388331032596, -502321837179064112839811328004231,
  14509739799896203918326523756319811, -562787878490855011292385604558939089,
  6582678899548170799955716813164265416, -62869017447138396875579041436094283534,
  345791616887914584960143929918826122523, -1381165343232929927534220936797235845154,
  3773581980154536045573490326670682760628, -7337032198660275428997544229909213386698,
  10000000000000000000000000000000000000000, -9360438831407715275689616329058430296064,
  5738193775203278363838494921778516145792, -2073842823697641824667023077981269579416,
  335310163392811078007715607984939805155, 0],
 "H_A": "3096614778920389894432065374494561808298054428938646838502210033521263934729035695524507073/4677400725520733437500000000000000000000000000000000000000000000000000000000000000000000000000000",
 "L2": ["11090354888959124950675713943330825089208002149764084065930880151894297951515115449693813231942699/16000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
        "1732867951399863273543080303645441420188750335900638135301700023733484054924236789014658317491046719/2500000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"],
 "L3": ["10986122886681096913952452369225257046474905578227494517346943336374942932186089668736157548137320887/10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
        "1373265360835137114244056546153157130809363197278436814668367917046867866523261208592019693517165111/1250000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"],
 "r2": ["7071067811865475244008443621048490392848359376884740365883398689953662392310535194251937671638207863/10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
        "883883476483184405501055452631061299106044922110592545735424836244207799038816899281492208954775983/1250000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"],
 "r3": ["1443375672974064411272871951254893639119004378175317190046505816209944180757333364234288488964373813/2500000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
        "5773502691896257645091487805019574556476017512701268760186023264839776723029333456937153955857495253/10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"],
 "pi": ["78539816339744830961566084581987572104929234984377645524373614807695410157155224965700870633552926699553702162832057666177346115238764555793/25000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
        "314159265358979323846264338327950288419716939937510582097494459230781640628620899862803482534211706798214808651328230664709384460955058223173/100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"],
 "Ek_head": "39024135524311375226288268609949499970630279593787326169263095253181598200301604374468929465718334527687548649124868806221930080414906569668565088081205393262854606103841793035412661247592297072999235619904966663572923126910255351596607231069285699647880082093346309334350566709276346806402662836678640448959645174955643973592986898395391135867382880034267902799615115194831077461563278726225897645089342639305471000100649918465434968973118719889908315292813362472868256489966693/2264485876880805324353923639041092294595890068795862329872684995083671168245279685417086828498367325006122099403000514411921612999690382490648127937216597254017820313985826777836575592415151623806123763680232859558381081415738235215818222461803208992371101939142650644249368469434759074768130065871288316439132923155631888424935905215385731967959210144662939801615136123876613430227914629891752574838321370055950176624141444980651381509555393840284966469164794038330470361325426595751526400000000000000000000000",
 "th": "387420489/4358121455899753807609472569259690437235950349189120000000",
}
res = {}
fails = []
def check(label, f):
    try:
        ok = bool(f())
    except Exception as e:
        ok = False; label += " [exception: %r]" % (e,)
    res.setdefault("checks", []).append([label[:90], ok])
    if not ok: fails.append(label)

# 1. H_A = E0[p^2] with p(t)=sum z_r (1-t^2)^r  (independent expansion via polynomial in s=t^2)
z = [F(n, 10**40) for n in data["nums"]]
ps = [F(0)] * 16                      # coefficients in s = t^2
for r, zr in enumerate(z):
    for k in range(r + 1):
        ps[k] += zr * math.comb(r, k) * (-1) ** k
p2 = [F(0)] * 31
for i, x in enumerate(ps):
    for j, y in enumerate(ps):
        p2[i + j] += x * y
H_A = sum(c / (2 * k + 1) for k, c in enumerate(p2))  # E0[t^{2k}] = 1/(2k+1)
check('H_A == F(data["H_A"])', lambda: (H_A == F(data["H_A"])))
check('ps[14] != 0 and z[15] == 0', lambda: (ps[14] != 0 and z[15] == 0))

# 2. E_k and t_h independent recomputation
U, V = [F(1)], [F(1)]
for n in range(1, 49):
    U.append(-sum(U[n - j] / math.factorial(2 * j + 1) for j in range(1, n + 1)))
    V.append(-sum(V[n - j] / math.factorial(2 * j) for j in range(1, n + 1)))
q0 = F(3, 4)
def tail(j, e):
    return q0 ** (2 * j) / math.factorial(2 * j + e) / (1 - q0 ** 2 / ((2 * j + e + 1) * (2 * j + e + 2)))
Ek = sum(q0 ** (2 * n) * (abs(U[n]) * tail(49 - n, 1) / q0 + abs(V[n]) * tail(49 - n, 0)) for n in range(49)) / 4
check('Ek == F(data["Ek_head"])', lambda: (Ek == F(data["Ek_head"])))
th = F(3, 8) ** 32 / math.factorial(32) / (1 - F(3, 8) ** 2 / (33 * 34))
check('th == F(data["th"])', lambda: (th == F(data["th"])))
# recurrence sanity: reciprocal series really cancel up to u^96 (coefficient check)
check("reciprocal recurrences cancel all coefficients u^2..u^96", lambda: all(
    sum(U[n] / math.factorial(2 * (N - n) + 1) for n in range(N + 1)) == 0 and
    sum(V[n] / math.factorial(2 * (N - n)) for n in range(N + 1)) == 0 for N in range(1, 49)))

# 3. constant boxes contain the true constants (rigorous series bounds)
def artanh_box(x, N):
    s = sum(x ** (2 * j + 1) / (2 * j + 1) for j in range(N))
    t = x ** (2 * N + 1) / ((2 * N + 1) * (1 - x * x))
    return 2 * s, 2 * (s + t)
def atan_box(x, K):                    # alternating, decreasing terms
    s = sum((-1) ** j * x ** (2 * j + 1) / (2 * j + 1) for j in range(K))
    s2 = s + (-1) ** K * x ** (2 * K + 1) / (2 * K + 1)
    return min(s, s2), max(s, s2)
def inside(box, lo, hi):
    b = [F(v) for v in box]
    return b[0] <= lo and hi <= b[1]
l2 = artanh_box(F(1, 3), 140)
check('inside(data["L2"], *l2)', lambda: (inside(data["L2"], *l2)))
l3 = artanh_box(F(1, 2), 230)
check('inside(data["L3"], *l3)', lambda: (inside(data["L3"], *l3)))
a5, a239 = atan_box(F(1, 5), 130), atan_box(F(1, 239), 45)
pib = (16 * a5[0] - 4 * a239[1], 16 * a5[1] - 4 * a239[0])
check('inside(data["pi"], *pib)', lambda: (inside(data["pi"], *pib)))
r2 = [F(v) for v in data["r2"]]; r3 = [F(v) for v in data["r3"]]
check('0 < r2[0] and r2[0] ** 2 <= F(1, 2) <= r2[1] ** 2', lambda: (0 < r2[0] and r2[0] ** 2 <= F(1, 2) <= r2[1] ** 2))
check('0 < r3[0] and r3[0] ** 2 <= F(1, 3) <= r3[1] ** 2', lambda: (0 < r3[0] and r3[0] ** 2 <= F(1, 3) <= r3[1] ** 2))
res["box_widths_upper"] = {k: float(F(data[k][1]) - F(data[k][0])) for k in ("L2", "L3", "r2", "r3", "pi")}

# 4. cosh(3/8) < 128/119 < 3/2 via (2k)! >= 2^k
check('all(math.factorial(2 * k) >= 2 ** k for k in range(80)) and F(128, 119) < F(3, 2)', lambda: (all(math.factorial(2 * k) >= 2 ** k for k in range(80)) and F(128, 119) < F(3, 2)))
res["cosh38_bound"] = True

# 5. Legendre monomial coefficients used by the code vs Bonnet recurrence (exact, m<=40)
P = [[F(1)], [F(0), F(1)]]
for n in range(1, 40):
    a = [F(0)] * (n + 2)
    for k, c in enumerate(P[n]): a[k + 1] += F(2 * n + 1, n + 1) * c
    for k, c in enumerate(P[n - 1]): a[k] -= F(n, n + 1) * c
    P.append(a)
def leg_ok():
    for m in range(0, 41, 2):
        a = [0] * (m + 1)
        for k in range(m // 2 + 1):
            a[m - 2 * k] = (-1) ** k * math.comb(2 * m - 2 * k, m - k) * math.comb(m - k, k)
        if [F(c, 2 ** m) for c in a] != P[m]: return False
    return True
check("Legendre closed-form coefficients == Bonnet recurrence, even m<=40", leg_ok)

# 6. support endpoints 1 - tau_n from the boxes (tau_n = (4/3) log n, log4 = 2 log2)
L2lo, L2hi = (F(v) for v in data["L2"]); L3lo, L3hi = (F(v) for v in data["L3"])
ends = {"1-tau2": (1 - 4 * L2hi / 3, 1 - 4 * L2lo / 3),
        "1-tau3": (1 - 4 * L3hi / 3, 1 - 4 * L3lo / 3),
        "1-tau4": (1 - 8 * L2hi / 3, 1 - 8 * L2lo / 3)}
check('ends["1-tau2"][0] > 0 and ends["1-tau3"][1] < 0 and ends["1-tau4"][1] < ends["1-tau3"][0]', lambda: (ends["1-tau2"][0] > 0 and ends["1-tau3"][1] < 0 and ends["1-tau4"][1] < ends["1-tau3"][0]))
check('ends["1-tau4"][0] > -1', lambda: (ends["1-tau4"][0] > -1))
res["endpoints"] = {k: [float(v[0]), float(v[1])] for k, v in ends.items()}

# 7. reporting only (no assertion): display-level consistency of the claimed decimals
import decimal
def sqrt_box(x, digits=60):
    s = 10 ** digits
    n = x.numerator * s * s // x.denominator
    r = math.isqrt(n)
    return F(r, s), F(r + 1, s)
sH_lo, sH_hi = sqrt_box(F(data["H_A"]))
Ekv, thv = F(data["Ek_head"]), F(data["th"])
res["sqrtH_A_approx"] = "%.20e" % float(sH_lo)
res["28_sqrtH_A_lo"] = str(decimal.Decimal(28 * sH_lo.numerator) / decimal.Decimal(sH_lo.denominator))[:26]
res["Ek_approx"] = "%.12e" % float(Ekv)
res["th_approx"] = "%.12e" % float(thv)
res["rem_coeff_(3Ek/2+9th/2)"] = "%.12e" % float(F(3, 2) * Ekv + F(9, 2) * thv)
res["rem_times_sqrtH_hi"] = "%.12e" % float((F(3, 2) * Ekv + F(9, 2) * thv) * sH_hi)
q = F("8.4874678247291907546e-12") / F("2.2782392677405310185e-2")
decimal.getcontext().prec = 30
res["displayed_ycert_over_displayed_crude"] = str(decimal.Decimal(q.numerator) / decimal.Decimal(q.denominator))
res["claimed_ratio_bound"] = "3.7254505902475865958e-10"
res["all_checks_passed"] = not fails
res["failed"] = fails
print(json.dumps(res, indent=1))
