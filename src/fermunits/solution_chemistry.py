"""Conversions for shared solution-chemistry quantities."""

import math
from typing import Any

from pint import Quantity

from fermunits.registry import (
    _CHEMICAL_EQUIVALENCE_CONTEXT,
    _CHEMICAL_EQUIVALENT_MASS_CONTEXT,
)

_CACO3_EQUIVALENT_MASS_GRAMS_PER_EQUIVALENT = 50.0


def _require_positive_finite_value(
    value: float,
    *,
    name: str,
) -> None:
    """Require a finite value greater than zero."""
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")

    if value <= 0.0:
        raise ValueError(f"{name} must be greater than zero")


def amount_to_equivalents(
    amount: Quantity[Any],
    equivalence_factor: float,
) -> Quantity[Any]:
    """Convert amount of substance to chemical-equivalent amount.

    ``equivalence_factor`` is the number of equivalents per mole for the
    specified chemical entity and reaction or charge convention.
    """
    _require_positive_finite_value(
        equivalence_factor,
        name="Equivalence factor",
    )

    return amount.to(
        "equivalent",
        _CHEMICAL_EQUIVALENCE_CONTEXT,
        equivalence_factor=equivalence_factor,
    )


def equivalents_to_amount(
    equivalent_amount: Quantity[Any],
    equivalence_factor: float,
) -> Quantity[Any]:
    """Convert chemical-equivalent amount to amount of substance."""
    _require_positive_finite_value(
        equivalence_factor,
        name="Equivalence factor",
    )

    return equivalent_amount.to(
        "mole",
        _CHEMICAL_EQUIVALENCE_CONTEXT,
        equivalence_factor=equivalence_factor,
    )


def amount_concentration_to_equivalent_concentration(
    amount_concentration: Quantity[Any],
    equivalence_factor: float,
) -> Quantity[Any]:
    """Convert amount concentration to equivalent concentration."""
    _require_positive_finite_value(
        equivalence_factor,
        name="Equivalence factor",
    )

    return amount_concentration.to(
        "equivalent / liter",
        _CHEMICAL_EQUIVALENCE_CONTEXT,
        equivalence_factor=equivalence_factor,
    )


def equivalent_concentration_to_amount_concentration(
    equivalent_concentration: Quantity[Any],
    equivalence_factor: float,
) -> Quantity[Any]:
    """Convert equivalent concentration to amount concentration."""
    _require_positive_finite_value(
        equivalence_factor,
        name="Equivalence factor",
    )

    return equivalent_concentration.to(
        "mole / liter",
        _CHEMICAL_EQUIVALENCE_CONTEXT,
        equivalence_factor=equivalence_factor,
    )


def mass_concentration_to_equivalent_concentration(
    mass_concentration: Quantity[Any],
    equivalent_mass_grams_per_equivalent: float,
) -> Quantity[Any]:
    """Convert mass concentration using an explicit equivalent mass.

    ``equivalent_mass_grams_per_equivalent`` is specific to the stated
    chemical entity, reaction, or reporting basis.
    """
    _require_positive_finite_value(
        equivalent_mass_grams_per_equivalent,
        name="Equivalent mass",
    )

    return mass_concentration.to(
        "equivalent / liter",
        _CHEMICAL_EQUIVALENT_MASS_CONTEXT,
        equivalent_mass_grams_per_equivalent=(equivalent_mass_grams_per_equivalent),
    )


def equivalent_concentration_to_mass_concentration(
    equivalent_concentration: Quantity[Any],
    equivalent_mass_grams_per_equivalent: float,
) -> Quantity[Any]:
    """Convert equivalent concentration using an explicit equivalent mass."""
    _require_positive_finite_value(
        equivalent_mass_grams_per_equivalent,
        name="Equivalent mass",
    )

    return equivalent_concentration.to(
        "gram / liter",
        _CHEMICAL_EQUIVALENT_MASS_CONTEXT,
        equivalent_mass_grams_per_equivalent=(equivalent_mass_grams_per_equivalent),
    )


def caco3_basis_mass_concentration_to_equivalent_concentration(
    mass_concentration_as_caco3: Quantity[Any],
) -> Quantity[Any]:
    """Convert a CaCO3-basis report to equivalent concentration.

    The input is a reporting-basis quantity such as alkalinity or hardness
    expressed in mass-per-volume units *as CaCO3*. It does not represent the
    concentration of actual dissolved calcium carbonate.

    FermUnits uses the conventional water-analysis factor
    ``50 mg/L as CaCO3 = 1 mEq/L``.
    """
    return mass_concentration_to_equivalent_concentration(
        mass_concentration_as_caco3,
        _CACO3_EQUIVALENT_MASS_GRAMS_PER_EQUIVALENT,
    )


def equivalent_concentration_to_caco3_basis_mass_concentration(
    equivalent_concentration: Quantity[Any],
) -> Quantity[Any]:
    """Convert equivalent concentration to a CaCO3-basis mass report.

    The result is a plain mass-concentration quantity whose *as CaCO3*
    reporting basis must remain explicit in the calling application.
    """
    return equivalent_concentration_to_mass_concentration(
        equivalent_concentration,
        _CACO3_EQUIVALENT_MASS_GRAMS_PER_EQUIVALENT,
    )
