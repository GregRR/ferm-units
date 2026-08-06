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


def srm_to_ebc(srm: float) -> float:
    """Convert a modern ASBC SRM color index to an EBC color index.

    The conversion uses the ratio between the modern EBC and ASBC
    spectrophotometric scale factors:

    ``EBC = SRM * (25 / 12.7)``
    """
    _require_nonnegative_finite(srm, "SRM")

    return srm * _SRM_TO_EBC_FACTOR


def ebc_to_srm(ebc: float) -> float:
    """Convert a modern EBC color index to an ASBC SRM color index."""
    _require_nonnegative_finite(ebc, "EBC")

    return ebc / _SRM_TO_EBC_FACTOR


def lovibond_to_srm_approx(lovibond: float) -> float:
    """Approximate SRM from degrees Lovibond.

    This is an empirical approximation involving the older Lovibond visual
    scale. It is not equivalent to the direct modern SRM/EBC relationship.

    Values that would produce a negative SRM result are rejected because a
    negative brewing color index is not meaningful.
    """
    _require_nonnegative_finite(lovibond, "Lovibond")

    srm = _LOVIBOND_TO_SRM_SLOPE * lovibond + _LOVIBOND_TO_SRM_INTERCEPT

    if srm < 0.0:
        raise ValueError(
            "Lovibond value is below the useful range of this approximation"
        )

    return srm


def srm_to_lovibond_approx(srm: float) -> float:
    """Approximate degrees Lovibond from SRM.

    This numerically inverts ``lovibond_to_srm_approx``.
    """
    _require_nonnegative_finite(srm, "SRM")

    return (srm - _LOVIBOND_TO_SRM_INTERCEPT) / _LOVIBOND_TO_SRM_SLOPE
