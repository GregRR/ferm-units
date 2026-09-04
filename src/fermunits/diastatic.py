"""Conversions between common malt diastatic-power scales."""

import math

_LINTNER_TO_WK_SLOPE = 3.5
_LINTNER_TO_WK_INTERCEPT = -16.0


def _require_nonnegative_finite(value: float, name: str) -> None:
    """Validate a nonnegative finite diastatic-power value."""
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")

    if value < 0.0:
        raise ValueError(f"{name} must not be negative")


def _require_finite_result(value: float, name: str) -> float:
    """Return a finite conversion result or raise a controlled error."""
    if not math.isfinite(value):
        raise ValueError(f"{name} result is outside the representable finite range")

    return value


def lintner_to_windisch_kolbach(lintner: float) -> float:
    """Convert a reported degrees-Lintner value to Windisch-Kolbach units.

    FermUnits uses the conventional numerical relationship
    ``WK = 3.5 * Lintner - 16``. Current ASBC and EBC diastatic-power method
    identities are documented, and the conversion is independently reproduced
    in peer-reviewed brewing literature, but the primary provenance, exactness,
    range, and reporting conventions of the cross-scale relationship remain
    verification pending.

    Values producing a negative Windisch-Kolbach result are rejected because
    negative reported diastatic power is not meaningful.
    """
    _require_nonnegative_finite(lintner, "Degrees Lintner")

    windisch_kolbach = _require_finite_result(
        _LINTNER_TO_WK_SLOPE * lintner + _LINTNER_TO_WK_INTERCEPT,
        "Windisch-Kolbach",
    )

    if windisch_kolbach < 0.0:
        raise ValueError(
            "Degrees Lintner value is below the useful range of this conversion"
        )

    return windisch_kolbach


def windisch_kolbach_to_lintner(windisch_kolbach: float) -> float:
    """Convert a reported Windisch-Kolbach value to degrees Lintner.

    This is the algebraic inverse of ``lintner_to_windisch_kolbach`` and has
    the same provisional source-status limitations.
    """
    _require_nonnegative_finite(
        windisch_kolbach,
        "Windisch-Kolbach units",
    )

    return _require_finite_result(
        (windisch_kolbach - _LINTNER_TO_WK_INTERCEPT) / _LINTNER_TO_WK_SLOPE,
        "Degrees Lintner",
    )
