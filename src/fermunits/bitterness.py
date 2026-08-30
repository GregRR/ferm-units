"""Conversions for analytical beer bitterness measurements."""

import math

_BITTERNESS_UNITS_PER_ABSORBANCE = 50.0


def _require_nonnegative_finite(value: float, name: str) -> None:
    """Validate a nonnegative finite bitterness measurement."""
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")

    if value < 0.0:
        raise ValueError(f"{name} must not be negative")


def absorbance_275nm_to_bitterness_units(absorbance: float) -> float:
    """Calculate beer bitterness units from method-derived 275 nm absorbance.

    ASBC Beer-23A and EBC Method 9.8 determine beer bitterness after acidic
    liquid-liquid extraction of bitter compounds into a nonpolar phase. For
    the method-derived extract absorbance:

    ``bitterness units = absorbance at 275 nm * 50``

    This helper applies that reporting factor; it does not implement the
    extraction or sample-preparation procedure. Raw beer absorbance at 275 nm
    is therefore not an equivalent input. The result is an operational
    analytical measurement and must not be interpreted as an exact
    iso-alpha-acid concentration or direct measurement of perceived
    bitterness.
    """
    _require_nonnegative_finite(absorbance, "Absorbance at 275 nm")

    return absorbance * _BITTERNESS_UNITS_PER_ABSORBANCE


def bitterness_units_to_absorbance_275nm(
    bitterness_units: float,
) -> float:
    """Calculate the method-extract 275 nm absorbance for bitterness units.

    This is the numerical inverse of
    ``absorbance_275nm_to_bitterness_units`` and refers to the same
    method-derived extract absorbance, not raw beer absorbance.
    """
    _require_nonnegative_finite(
        bitterness_units,
        "Bitterness units",
    )

    return bitterness_units / _BITTERNESS_UNITS_PER_ABSORBANCE
