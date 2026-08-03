"""Pint registry construction for FermUnits."""

from importlib.resources import as_file, files
from typing import Any

from pint import Quantity, UnitRegistry


def create_registry() -> UnitRegistry[Any]:
    """Return a new Pint registry containing all FermUnits definitions.

    A factory is exposed so applications and tests can create isolated
    registries instead of sharing global mutable state.
    """
    registry: UnitRegistry[Any] = UnitRegistry()
    definition = files("fermunits.definitions").joinpath("vessels.txt")

    with as_file(definition) as definition_path:
        registry.load_definitions(definition_path)

    return registry


ureg: UnitRegistry[Any] = create_registry()
Q_: type[Quantity[Any]] = ureg.Quantity
