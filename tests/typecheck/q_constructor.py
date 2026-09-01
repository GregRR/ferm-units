"""Static regression checks for the public FermUnits quantity constructor."""

from decimal import Decimal
from fractions import Fraction
from typing import assert_type

from fermunits import Q_, Quantity

q_float = Q_(1.0, "gram")
q_int = Q_(1, "gram")
q_decimal = Q_(Decimal("1.25"), "gram")
q_fraction = Q_(Fraction(5, 4), "gram")

assert_type(q_float, Quantity[float])
assert_type(q_int, Quantity[int])
assert_type(q_decimal, Quantity[Decimal])
assert_type(q_fraction, Quantity[Fraction])
