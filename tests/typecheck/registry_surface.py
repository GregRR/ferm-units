"""Static regression checks for public registry typing."""

from typing import Any, assert_type

from fermunits import (
    Quantity,
    UnitRegistry,
    co2_volumes_to_mass_concentration,
    create_registry,
    ureg,
)

isolated = create_registry()

assert_type(isolated, UnitRegistry[Any])
assert_type(ureg, UnitRegistry[Any])

carbonation = co2_volumes_to_mass_concentration(1.0, registry=isolated)
assert_type(carbonation, Quantity[Any])
