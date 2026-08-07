"""Conversions for shared solution-chemistry quantities."""

import math
from typing import Any, cast

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


def _validated_solution_density(
    solution_density: Quantity[Any],
) -> Quantity[Any]:
    """Return a positive finite density in kilograms per liter."""
    density = solution_density.to("kilogram / liter")
    magnitude = float(density.magnitude)

    _require_positive_finite_value(
        magnitude,
        name="Solution density",
    )

    return density


def _validated_molar_mass(
    molar_mass: Quantity[Any],
) -> Quantity[Any]:
    """Return a positive finite molar mass in grams per mole."""
    normalized = molar_mass.to("gram / mole")
    magnitude = float(normalized.magnitude)

    _require_positive_finite_value(
        magnitude,
        name="Molar mass",
    )

    return normalized


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


def mass_concentration_to_mass_fraction(
    mass_concentration: Quantity[Any],
    solution_density: Quantity[Any],
) -> Quantity[Any]:
    """Convert mass concentration to mass fraction using solution density.

    The returned dimensionless quantity may be expressed explicitly as
    ``milligram / kilogram``, ``microgram / kilogram``, or another compatible
    mass ratio. No dilute-water density assumption is made.
    """
    concentration = mass_concentration.to("gram / liter")
    density = _validated_solution_density(solution_density)

    return cast(Quantity[Any], concentration / density)


def mass_fraction_to_mass_concentration(
    mass_fraction: Quantity[Any],
    solution_density: Quantity[Any],
) -> Quantity[Any]:
    """Convert mass fraction to mass concentration using solution density.

    ``mass_fraction`` must be dimensionless and may be supplied as an explicit
    ratio such as ``milligram / kilogram`` or ``microgram / kilogram``.
    """
    fraction = mass_fraction.to("dimensionless")
    density = _validated_solution_density(solution_density)

    return cast(Quantity[Any], fraction * density)


def mass_concentration_to_amount_concentration(
    mass_concentration: Quantity[Any],
    molar_mass: Quantity[Any],
) -> Quantity[Any]:
    """Convert mass concentration to amount concentration using molar mass.

    ``molar_mass`` must identify the same chemical entity, including hydration
    state where applicable, as ``mass_concentration``. No chemical identity is
    inferred from either unit expression.
    """
    concentration = mass_concentration.to("gram / liter")
    normalized_molar_mass = _validated_molar_mass(molar_mass)

    return cast(Quantity[Any], concentration / normalized_molar_mass)


def amount_concentration_to_mass_concentration(
    amount_concentration: Quantity[Any],
    molar_mass: Quantity[Any],
) -> Quantity[Any]:
    """Convert amount concentration to mass concentration using molar mass.

    ``molar_mass`` must identify the same chemical entity, including hydration
    state where applicable, as ``amount_concentration``.
    """
    concentration = amount_concentration.to("mole / liter")
    normalized_molar_mass = _validated_molar_mass(molar_mass)

    return cast(Quantity[Any], concentration * normalized_molar_mass)
