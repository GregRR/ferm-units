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
_CHEMICAL_EQUIVALENT_MASS_CONTEXT = "chemical_equivalent_mass"


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


def _mass_concentration_to_chemical_equivalent_concentration(
    ureg: UnitRegistry[Any],
    value: PlainQuantity[Any],
    **kwargs: Any,
) -> PlainQuantity[Any]:
    """Convert mass concentration to chemical-equivalent concentration."""
    equivalent_mass = float(kwargs["equivalent_mass_grams_per_equivalent"])

    return cast(
        PlainQuantity[Any],
        value / equivalent_mass * ureg.Unit("equivalent / gram"),
    )


def _chemical_equivalent_concentration_to_mass_concentration(
    ureg: UnitRegistry[Any],
    value: PlainQuantity[Any],
    **kwargs: Any,
) -> PlainQuantity[Any]:
    """Convert chemical-equivalent concentration to mass concentration."""
    equivalent_mass = float(kwargs["equivalent_mass_grams_per_equivalent"])

    return cast(
        PlainQuantity[Any],
        value * equivalent_mass * ureg.Unit("gram / equivalent"),
    )


def _add_chemical_equivalence_context(registry: UnitRegistry[Any]) -> None:
    """Add factor-based amount/equivalent conversions."""
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


def _add_chemical_equivalent_mass_context(
    registry: UnitRegistry[Any],
) -> None:
    """Add equivalent-mass concentration conversions."""
    context = Context(_CHEMICAL_EQUIVALENT_MASS_CONTEXT)

    context.add_transformation(
        "[mass] / [volume]",
        "[chemical_equivalent] / [volume]",
        _mass_concentration_to_chemical_equivalent_concentration,
    )
    context.add_transformation(
        "[chemical_equivalent] / [volume]",
        "[mass] / [volume]",
        _chemical_equivalent_concentration_to_mass_concentration,
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
    _add_chemical_equivalent_mass_context(registry)

    return registry


ureg: UnitRegistry[Any] = create_registry()
Q_: type[Quantity[Any]] = ureg.Quantity
