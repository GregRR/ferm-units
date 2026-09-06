"""Pint registry construction for FermUnits."""

import math
from importlib.resources import as_file, files
from typing import Any, cast

from pint import Context, UnitRegistry
from pint.facets.plain import PlainQuantity

_DEFINITION_FILES = (
    "solution_chemistry.txt",
    "vessels.txt",
)
_CHEMICAL_EQUIVALENCE_CONTEXT = "chemical_equivalence"
_CHEMICAL_EQUIVALENT_MASS_CONTEXT = "chemical_equivalent_mass"


def _validated_positive_finite_context_parameter(
    value: Any,
    *,
    name: str,
) -> float:
    """Return a positive finite context parameter representable as ``float``."""
    try:
        normalized = float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} is outside the representable finite range") from exc

    if not math.isfinite(normalized):
        raise ValueError(f"{name} must be finite")

    if normalized <= 0.0:
        raise ValueError(f"{name} must be greater than zero")

    return normalized


def _require_finite_quantity_magnitude(
    value: PlainQuantity[Any],
    *,
    name: str,
) -> None:
    """Require a scalar quantity magnitude within the finite numeric range."""
    try:
        finite = math.isfinite(value.magnitude)
    except OverflowError as exc:
        raise ValueError(f"{name} is outside the representable finite range") from exc

    if not finite:
        raise ValueError(f"{name} must be finite")


def _require_finite_quantity_result(
    value: PlainQuantity[Any],
    *,
    name: str,
) -> PlainQuantity[Any]:
    """Return a finite scalar quantity result or raise a controlled error."""
    try:
        finite = math.isfinite(value.magnitude)
    except OverflowError as exc:
        raise ValueError(
            f"{name} result is outside the representable finite range"
        ) from exc

    if not finite:
        raise ValueError(f"{name} result is outside the representable finite range")

    return value


def _substance_to_chemical_equivalent(
    ureg: UnitRegistry[Any],
    value: PlainQuantity[Any],
    **kwargs: Any,
) -> PlainQuantity[Any]:
    """Convert amount of substance to chemical-equivalent amount."""
    equivalence_factor = _validated_positive_finite_context_parameter(
        kwargs["equivalence_factor"],
        name="Equivalence factor",
    )
    _require_finite_quantity_magnitude(value, name="Chemical-equivalence input")

    result = cast(
        PlainQuantity[Any],
        value * equivalence_factor * ureg.Unit("equivalent") / ureg.Unit("mole"),
    )
    return _require_finite_quantity_result(
        result,
        name="Chemical-equivalence conversion",
    )


def _chemical_equivalent_to_substance(
    ureg: UnitRegistry[Any],
    value: PlainQuantity[Any],
    **kwargs: Any,
) -> PlainQuantity[Any]:
    """Convert chemical-equivalent amount to amount of substance."""
    equivalence_factor = _validated_positive_finite_context_parameter(
        kwargs["equivalence_factor"],
        name="Equivalence factor",
    )
    _require_finite_quantity_magnitude(value, name="Chemical-equivalence input")

    result = cast(
        PlainQuantity[Any],
        value / equivalence_factor * ureg.Unit("mole") / ureg.Unit("equivalent"),
    )
    return _require_finite_quantity_result(
        result,
        name="Chemical-equivalence conversion",
    )


def _mass_concentration_to_chemical_equivalent_concentration(
    ureg: UnitRegistry[Any],
    value: PlainQuantity[Any],
    **kwargs: Any,
) -> PlainQuantity[Any]:
    """Convert mass concentration to chemical-equivalent concentration."""
    equivalent_mass = _validated_positive_finite_context_parameter(
        kwargs["equivalent_mass_grams_per_equivalent"],
        name="Equivalent mass",
    )
    _require_finite_quantity_magnitude(value, name="Equivalent-mass input")

    result = cast(
        PlainQuantity[Any],
        value / equivalent_mass * ureg.Unit("equivalent / gram"),
    )
    return _require_finite_quantity_result(
        result,
        name="Equivalent-mass conversion",
    )


def _chemical_equivalent_concentration_to_mass_concentration(
    ureg: UnitRegistry[Any],
    value: PlainQuantity[Any],
    **kwargs: Any,
) -> PlainQuantity[Any]:
    """Convert chemical-equivalent concentration to mass concentration."""
    equivalent_mass = _validated_positive_finite_context_parameter(
        kwargs["equivalent_mass_grams_per_equivalent"],
        name="Equivalent mass",
    )
    _require_finite_quantity_magnitude(value, name="Equivalent-mass input")

    result = cast(
        PlainQuantity[Any],
        value * equivalent_mass * ureg.Unit("gram / equivalent"),
    )
    return _require_finite_quantity_result(
        result,
        name="Equivalent-mass conversion",
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
Q_ = ureg.Quantity
