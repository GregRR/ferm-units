"""Conversions for dissolved carbon dioxide in fermented beverages."""

import math
from typing import Any

from pint import Quantity

from fermunits.registry import Q_

_MILLILITERS_PER_LITER = 1000.0
_CO2_MILLILITERS_PER_GRAM = 506.07
_GRAMS_PER_LITER_PER_VOLUME = _MILLILITERS_PER_LITER / _CO2_MILLILITERS_PER_GRAM


def _require_nonnegative_finite(value: float, name: str) -> None:
    """Validate a nonnegative finite carbonation value."""
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")

    if value < 0.0:
        raise ValueError(f"{name} must not be negative")


def _require_finite_result(value: float, name: str) -> float:
    """Return a finite conversion result or raise a controlled error."""
    if not math.isfinite(value):
        raise ValueError(f"{name} result is outside the representable finite range")

    return value


def _validated_co2_mass_concentration(
    mass_concentration: Quantity[Any],
) -> Quantity[Any]:
    """Return a finite nonnegative CO₂ mass concentration in grams per liter."""
    normalized = mass_concentration.to("gram / liter")
    magnitude = float(normalized.magnitude)

    _require_nonnegative_finite(magnitude, "CO2 mass concentration")

    return normalized


def co2_volumes_to_mass_concentration(co2_volumes: float) -> Quantity[Any]:
    """Convert volumes of dissolved CO₂ to a mass-concentration quantity.

    The result is returned in grams per liter and can be converted to any
    dimensionally compatible Pint mass-concentration unit.

    The factor reuses the 506.07 mL/g volumes-to-weight conversion constant
    reported by an EBC Analysis Committee publication inside an ASBC-adopted
    Fills-1 package-density equation. It gives approximately 1.976 g/L per
    volume.

    That source does not state the reference temperature or pressure attached
    to the constant, and FermUnits does not implement the surrounding package-
    density correction terms. Direct Beer-13/Fills-1 method verification is
    still pending, so this standalone mass-concentration interpretation remains
    provisional.
    """
    _require_nonnegative_finite(co2_volumes, "CO2 volumes")

    magnitude = _require_finite_result(
        co2_volumes * _GRAMS_PER_LITER_PER_VOLUME,
        "CO2 mass concentration",
    )

    return Q_(magnitude, "gram / liter")


def co2_mass_concentration_to_volumes(
    mass_concentration: Quantity[Any],
) -> float:
    """Convert a dissolved-CO₂ mass concentration to volumes of CO₂.

    ``mass_concentration`` may use any Pint unit dimensionally compatible with
    mass per volume. The carbonation factor and reference conditions remain
    provisional pending authoritative ASBC verification.
    """
    normalized = _validated_co2_mass_concentration(mass_concentration)

    return _require_finite_result(
        float(normalized.magnitude) / _GRAMS_PER_LITER_PER_VOLUME,
        "CO2 volumes",
    )


def co2_volumes_to_grams_per_liter(co2_volumes: float) -> float:
    """Convert volumes of dissolved CO₂ to grams per liter.

    This scalar API is retained for compatibility. New unit-aware downstream
    code should prefer :func:`co2_volumes_to_mass_concentration` so the physical
    mass-concentration unit remains explicit.
    """
    return float(co2_volumes_to_mass_concentration(co2_volumes).magnitude)


def co2_grams_per_liter_to_volumes(
    grams_per_liter: float,
) -> float:
    """Convert dissolved CO₂ in grams per liter to volumes of CO₂.

    This scalar API is retained for compatibility. New unit-aware downstream
    code should prefer :func:`co2_mass_concentration_to_volumes`.
    """
    _require_nonnegative_finite(
        grams_per_liter,
        "CO2 grams per liter",
    )

    return co2_mass_concentration_to_volumes(Q_(grams_per_liter, "gram / liter"))
