from fractions import Fraction
A=Fraction(1,2048)
B_EXACT="log(8)/2"
K=256
EPSILON=Fraction(20262735541658121715431,250172086796502324840759296)
NU=A-EPSILON
PENALTY=4/NU+5*A/NU**2
assert NU>4*A/5 and PENALTY<26240
def radius_interval():
    from interval_bounds import IV
    return IV(8).log()/2
