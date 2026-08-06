"""Conversions for dissolved carbon dioxide in fermented beverages."""

import math

_ASBC_VOLUMES_PER_MASS_PERCENT_FACTOR = 5.0607
_GRAMS_PER_LITER_PER_MASS_PERCENT_AT_SG_ONE = 10.0
_GRAMS_PER_LITER_PER_VOLUME = (
    _GRAMS_PER_LITER_PER_MASS_PERCENT_AT_SG_ONE / _ASBC_VOLUMES_PER_MASS_PERCENT_FACTOR
)


def _require_nonnegative_finite(value: float, name: str) -> None:
    """Validate a nonnegative finite carbonation value."""
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")

    if value < 0.0:
        raise ValueError(f"{name} must not be negative")


def co2_volumes_to_grams_per_liter(co2_volumes: float) -> float:
    """Convert volumes of dissolved CO₂ to grams per liter.

    The factor is derived from an ASBC-hosted presentation relating volumes
    of CO₂ to mass percent and beverage specific gravity. It gives
    approximately 1.976 g/L per volume.

    The exact reference conditions and relationship to the complete ASBC
    analytical method remain pending verification.
    """
    _require_nonnegative_finite(co2_volumes, "CO2 volumes")

    return co2_volumes * _GRAMS_PER_LITER_PER_VOLUME


def co2_grams_per_liter_to_volumes(
    grams_per_liter: float,
) -> float:
    """Convert dissolved CO₂ in grams per liter to volumes of CO₂."""
    _require_nonnegative_finite(
        grams_per_liter,
        "CO2 grams per liter",
    )

    return grams_per_liter / _GRAMS_PER_LITER_PER_VOLUME
