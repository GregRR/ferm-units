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
    """Calculate beer bitterness units from absorbance at 275 nm.

    ASBC Beer-23 and EBC Method 9.8 calculate bitterness units as:

    ``bitterness units = absorbance at 275 nm * 50``

    The result is an operational analytical measurement of extracted bitter
    substances. It must not be interpreted as an exact concentration of
    iso-alpha-acids or as a direct measurement of perceived bitterness.
    """
    _require_nonnegative_finite(absorbance, "Absorbance at 275 nm")

    return absorbance * _BITTERNESS_UNITS_PER_ABSORBANCE


def bitterness_units_to_absorbance_275nm(
    bitterness_units: float,
) -> float:
    """Calculate the corresponding 275 nm absorbance from bitterness units.

    This is the numerical inverse of
    ``absorbance_275nm_to_bitterness_units``.
    """
    _require_nonnegative_finite(
        bitterness_units,
        "Bitterness units",
    )

    return bitterness_units / _BITTERNESS_UNITS_PER_ABSORBANCE
