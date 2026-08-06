"""Pint registry construction for FermUnits."""

from importlib.resources import as_file, files
from typing import Any, cast

from pint import Context, Quantity, UnitRegistry
from pint.facets.plain import PlainQuantity

_DEFINITION_FILES = (
    "solution_chemistry.txt",
    "vessels.txt",
)
_CHEMICAL_EQUIVALENCE_CONTEXT = "chemical_equivalence"


def _substance_to_chemical_equivalent(
    ureg: UnitRegistry[Any],
    value: PlainQuantity[Any],
    **kwargs: Any,
) -> PlainQuantity[Any]:
    """Convert amount of substance to chemical-equivalent amount."""
    equivalence_factor = float(kwargs["equivalence_factor"])

    return cast(
        PlainQuantity[Any],
        value * equivalence_factor * ureg.Unit("equivalent") / ureg.Unit("mole"),
    )


def _chemical_equivalent_to_substance(
    ureg: UnitRegistry[Any],
    value: PlainQuantity[Any],
    **kwargs: Any,
) -> PlainQuantity[Any]:
    """Convert chemical-equivalent amount to amount of substance."""
    equivalence_factor = float(kwargs["equivalence_factor"])

    return cast(
        PlainQuantity[Any],
        value / equivalence_factor * ureg.Unit("mole") / ureg.Unit("equivalent"),
    )


def _add_chemical_equivalence_context(registry: UnitRegistry[Any]) -> None:
    """Add explicit factor-based mole/equivalent conversions."""
    context = Context(_CHEMICAL_EQUIVALENCE_CONTEXT)

    context.add_transformation(
        "[substance]",
        "[chemical_equivalent]",
        _substance_to_chemical_equivalent,
    )
    context.add_transformation(
        "[chemical_equivalent]",
        "[substance]",
        _chemical_equivalent_to_substance,
    )
    context.add_transformation(
        "[substance] / [volume]",
        "[chemical_equivalent] / [volume]",
        _substance_to_chemical_equivalent,
    )
    context.add_transformation(
        "[chemical_equivalent] / [volume]",
        "[substance] / [volume]",
        _chemical_equivalent_to_substance,
    )

    registry.add_context(context)


def create_registry() -> UnitRegistry[Any]:
    """Return a new Pint registry containing all FermUnits definitions.

    A factory is exposed so applications and tests can create isolated
    registries instead of sharing global mutable state.
    """
    registry: UnitRegistry[Any] = UnitRegistry()
    definition_root = files("fermunits.definitions")

    for definition_name in _DEFINITION_FILES:
        definition = definition_root.joinpath(definition_name)

        with as_file(definition) as definition_path:
            registry.load_definitions(definition_path)

    _add_chemical_equivalence_context(registry)

    return registry


ureg: UnitRegistry[Any] = create_registry()
Q_: type[Quantity[Any]] = ureg.Quantity
