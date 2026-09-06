"""Static regression checks for public registry typing."""

from typing import Any, assert_type

from fermunits import UnitRegistry, create_registry, ureg

isolated = create_registry()

assert_type(isolated, UnitRegistry[Any])
assert_type(ureg, UnitRegistry[Any])
