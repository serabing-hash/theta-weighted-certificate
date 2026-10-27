"""Independent integer/Fraction checks; no source or prime evaluation."""
from fractions import Fraction as F
import json

checks = {}
values = {}

def check(name, proposition):
    assert proposition, name
    checks[name] = True

def keep(name, value):
    values[name] = str(value)
    return value

def exp_partial(x, degree):
    term = F(1)
    total = term
    for k in range(1, degree + 1):
        term *= x / k
        total += term
    return total

# The polynomial quotient in the positive integral for 22/7 - pi.
quotient = [F(4), F(0), F(-4), F(0), F(5), F(-4), F(1)]
product = [F(0)] * 9
for degree, coefficient in enumerate(quotient):
    product[degree] += coefficient
    product[degree + 2] += coefficient
product[0] -= 4
check('pi_upper_integral_polynomial', product == [0, 0, 0, 0, 1, -4, 6, -4, 1])
check('pi_upper_integral_rational_part', sum(c / (k + 1) for k, c in enumerate(quotient)) == F(22, 7))
pi_lower = 4 * (F(1, 2) - F(1, 2)**3 / 3 + F(1, 2)**5 / 5
                - F(1, 2)**7 / 7 + F(1, 3) - F(1, 3)**3 / 3)
check('pi_lower_value_and_bracket', pi_lower == F(284663, 90720) and pi_lower > F(25, 8))

check('exp3_lower', exp_partial(F(3), 8) == F(89641, 4480) > 20)
check('exp5over2_lower', exp_partial(F(5, 2), 8) == F(3588667, 294912) > 12)
check('log2_upper', exp_partial(F(7, 10), 3) == F(12013, 6000) > 2)
exp1_upper = exp_partial(F(1), 4) + F(1, 120) / (1 - F(1, 6))
check('exp1_geometric_upper', exp1_upper == F(1631, 600) < F(68, 25) < 3)
check('exp3_upper', F(68, 25)**3 < 21)
check('exp5over2_upper', F(68, 25)**5 < F(49, 4)**2)
check('exp7_upper', F(68, 25)**7 < 1200)
K_upper = keep('K_upper', 4 * F(22, 7)**2 * F(500, 499))
check('K_upper_value', K_upper == F(968000, 24451) < 40)
check('inward_h_constant', 1128 * F(81, 188) == 486)
check('energy_prefactor', 4 * (4 * F(7, 10)) * F(15, 4) == 42)

# Rebuild every tail constant from the displayed definitions, not its value.
check('Y54_quarter_power_upper', F(49, 4) < F(15, 8)**4)
check('Y54_quarter_power_lower', F(20, 11)**4 < 12)
check('Y32_quarter_power_upper', 21 < F(9, 4)**4)
check('Y32_quarter_power_lower', 20 > 16)
bracket54 = F(15, 8) + F(11, 20) + F(15, 8) / 69
bracket32 = F(9, 4) + F(1, 2) + F(9, 4) / 119
check('Y54_bracket', bracket54 == F(282, 115))
check('Y32_bracket', bracket32 == F(659, 238))
check('Y54_exponent_and_q', F(55, 8) - F(25, 8)*12 == F(-245, 8) < -30 and 2*F(25, 8)*12 - 6 == 69)
check('Y32_exponent_and_q', F(33, 4) - F(25, 8)*20 == F(-217, 4) < -54 and 2*F(25, 8)*20 - 6 == 119)
hub54 = keep('hub_Y5over4', 42 * bracket54 * (486 * 40) / 20**10)
hub32 = keep('hub_Y3over2', 42 * bracket32 * (486 * 40) / 20**18)
check('hub_Y54_value_and_cap', hub54 == F(719523, 3680000000000) < F(1, 5000000))
check('hub_Y32_value_and_cap', hub32 == F(480411, 55705600000000000000000) < F(9, 10**18))

label_factor = keep('label_factor', 2 * F(81, 188) * F(15, 4) * 94 * 256 * F(50, 441))
check('label_factor_value', label_factor == F(432000, 49))
check('label_Y54_admissibility', F(49, 4) < 32)
check('label_Y32_admissibility', 21 < 64)
check('label_Y54_exponent', 16*F(49, 4) - F(3*33**2) / F(49, 4) == F(-3464, 49) < -70)
check('label_Y32_exponent', 16*F(21) - F(3*65**2) / F(21) == F(-1873, 7) < -267)
label54 = keep('label_Y5over4_N32', label_factor * 1200 * 33**6 / (2 * 20**23))
label32 = keep('label_Y3over2_N64', label_factor * 3**9 * 65**6 / 20**89)
check('label_Y54_value_and_cap', label54 == F(104608905489, 12845056000000000000000000) < F(1, 10**14))
check('label_Y32_cap', label32 < F(1, 10**96))
check('combined_Y54_rounded_cap', F(1, 5000000) + F(1, 10**14) < F(1, 2000)**2)
check('combined_Y32_rounded_cap', F(9, 10**18) + F(1, 10**96) < F(1, 10**17))
check('combined_Y54_exact_cap', hub54 + label54 < F(1, 2000)**2)
check('combined_Y32_exact_cap', hub32 + label32 < F(1, 10**17))
check('combined_Y32_unsquared_cap', F(1, 10**17) < F(1, 300000000)**2)

result = {
    'status': 'PASS: all exact scalar checks',
    'scope': 'Integer and Fraction arithmetic only; no theta, kappa, prime, quadrature, or spectral evaluation.',
    'check_count': len(checks),
    'checks': checks,
    'rational_values': values,
}
print(json.dumps(result, indent=2))
