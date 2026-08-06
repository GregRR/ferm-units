"""Conversions for shared solution-chemistry quantities."""

import math
from typing import Any

from pint import Quantity

from fermunits.registry import _CHEMICAL_EQUIVALENCE_CONTEXT


def _require_positive_finite_equivalence_factor(
    equivalence_factor: float,
) -> None:
    """Validate equivalents per mole for a specified entity and reaction."""
    if not math.isfinite(equivalence_factor):
        raise ValueError("Equivalence factor must be finite")

    if equivalence_factor <= 0.0:
        raise ValueError("Equivalence factor must be greater than zero")


def amount_to_equivalents(
    amount: Quantity[Any],
    equivalence_factor: float,
) -> Quantity[Any]:
    """Convert amount of substance to chemical-equivalent amount.

    ``equivalence_factor`` is the number of equivalents per mole for the
    specified chemical entity and reaction or charge convention.
    """
    _require_positive_finite_equivalence_factor(equivalence_factor)

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
    _require_positive_finite_equivalence_factor(equivalence_factor)

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
    _require_positive_finite_equivalence_factor(equivalence_factor)

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
    _require_positive_finite_equivalence_factor(equivalence_factor)

    return equivalent_concentration.to(
        "mole / liter",
        _CHEMICAL_EQUIVALENCE_CONTEXT,
        equivalence_factor=equivalence_factor,
    )
