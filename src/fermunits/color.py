"""Conversions among common brewing color indices."""

import math

_SRM_TO_EBC_FACTOR = 25.0 / 12.7
_LOVIBOND_TO_SRM_SLOPE = 1.3546
_LOVIBOND_TO_SRM_INTERCEPT = -0.76


def _require_nonnegative_finite(value: float, name: str) -> None:
    """Validate a nonnegative finite color-index value."""
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")

    if value < 0.0:
        raise ValueError(f"{name} must not be negative")


def _require_finite_result(value: float, name: str) -> float:
    """Return a finite conversion result or raise a controlled error."""
    if not math.isfinite(value):
        raise ValueError(f"{name} result is outside the representable finite range")

    return value


def srm_to_ebc(srm: float) -> float:
    """Convert a modern method-derived ASBC SRM index to EBC.

    For the modern 430 nm spectrophotometric scales in a 10 mm cell,
    ASBC color uses a factor of 12.7 and EBC color uses a factor of 25.
    FermUnits therefore converts the reported indices with:

    ``EBC = SRM * (25 / 12.7)``

    This helper converts reported color indices only. It does not perform the
    analytical sample preparation, clarification, dilution, or turbidity
    checks required by the underlying methods.
    """
    _require_nonnegative_finite(srm, "SRM")

    return _require_finite_result(srm * _SRM_TO_EBC_FACTOR, "EBC")


def ebc_to_srm(ebc: float) -> float:
    """Convert a modern method-derived EBC color index to ASBC SRM."""
    _require_nonnegative_finite(ebc, "EBC")

    return _require_finite_result(ebc / _SRM_TO_EBC_FACTOR, "SRM")


def lovibond_to_srm_approx(lovibond: float) -> float:
    """Approximate SRM from degrees Lovibond.

    This is a common empirical brewing approximation involving the older
    Lovibond visual scale. Its primary coefficient provenance, material scope,
    valid range, and expected error remain unverified, so it must not be
    treated as a general physical conversion between arbitrary Lovibond and
    modern spectrophotometric measurements.

    Values that would produce a negative SRM result are rejected because a
    negative brewing color index is not meaningful.
    """
    _require_nonnegative_finite(lovibond, "Lovibond")

    srm = _require_finite_result(
        _LOVIBOND_TO_SRM_SLOPE * lovibond + _LOVIBOND_TO_SRM_INTERCEPT,
        "SRM",
    )

    if srm < 0.0:
        raise ValueError(
            "Lovibond value is below the useful range of this approximation"
        )

    return srm


def srm_to_lovibond_approx(srm: float) -> float:
    """Approximate degrees Lovibond from SRM.

    This algebraically inverts ``lovibond_to_srm_approx`` and inherits the
    same provisional scope and limitations.
    """
    _require_nonnegative_finite(srm, "SRM")

    return _require_finite_result(
        (srm - _LOVIBOND_TO_SRM_INTERCEPT) / _LOVIBOND_TO_SRM_SLOPE,
        "Lovibond",
    )
