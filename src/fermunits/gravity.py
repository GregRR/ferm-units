"""Conversions for brewing gravity and extract measurements."""

import math

_PLATO_INVERSION_LOWER_SG = 0.5
_PLATO_INVERSION_UPPER_SG = 2.0
_PLATO_INVERSION_TOLERANCE = 1e-12
_PLATO_INVERSION_MAX_ITERATIONS = 100


def _require_finite(value: float, name: str) -> None:
    """Raise ValueError when a numeric input is NaN or infinite."""
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")


def _require_positive_specific_gravity(specific_gravity: float) -> None:
    """Validate a specific-gravity value."""
    _require_finite(specific_gravity, "Specific gravity")

    if specific_gravity <= 0.0:
        raise ValueError("Specific gravity must be greater than zero")


def _require_positive_correction_factor(wort_correction_factor: float) -> None:
    """Validate a wort refractometer correction factor."""
    _require_finite(wort_correction_factor, "Wort correction factor")

    if wort_correction_factor <= 0.0:
        raise ValueError("Wort correction factor must be greater than zero")


def sg_to_gravity_points(specific_gravity: float) -> float:
    """Convert specific gravity to algebraic gravity points relative to SG 1.000."""
    _require_positive_specific_gravity(specific_gravity)

    return (specific_gravity - 1.0) * 1000.0


def gravity_points_to_sg(gravity_points: float) -> float:
    """Convert algebraic gravity points relative to SG 1.000 to specific gravity."""
    _require_finite(gravity_points, "Gravity points")

    specific_gravity = 1.0 + (gravity_points / 1000.0)

    if specific_gravity <= 0.0:
        raise ValueError(
            "Gravity points must correspond to a specific gravity greater than zero"
        )

    return specific_gravity


def sg_to_plato(specific_gravity: float) -> float:
    """Estimate degrees Plato from specific gravity.

    The exact coefficients are reproduced in peer-reviewed brewing literature
    and attributed there to the American Society of Brewing Chemists. The
    original ASBC table or method, reference conditions, and scientific
    validity range still require direct verification.

    No scientific validity range is asserted yet. The input must be finite and
    greater than zero. For SG below 1.000, the polynomial is used algebraically
    and may return negative Plato; FermUnits does not claim that extrapolation is
    a separately standardized brewing convention.
    """
    _require_positive_specific_gravity(specific_gravity)

    return (
        -616.868
        + (1111.14 * specific_gravity)
        - (630.272 * specific_gravity**2)
        + (135.997 * specific_gravity**3)
    )


def plato_to_sg(plato: float) -> float:
    """Estimate specific gravity from degrees Plato.

    This function numerically inverts ``sg_to_plato`` so the two provisional
    conversions remain internally consistent. The underlying polynomial is
    reproduced in peer-reviewed brewing literature with ASBC attribution, but
    its primary table or method and scientific range still require direct
    verification.

    The current numerical search interval is SG 0.5 through 2.0. This is an
    implementation limit and must not be interpreted as an ASBC-approved
    measurement range.
    """
    _require_finite(plato, "Plato")

    lower_sg = _PLATO_INVERSION_LOWER_SG
    upper_sg = _PLATO_INVERSION_UPPER_SG
    lower_plato = sg_to_plato(lower_sg)
    upper_plato = sg_to_plato(upper_sg)

    if not lower_plato <= plato <= upper_plato:
        raise ValueError(
            "Plato value is outside the current numerical inversion range "
            f"of {lower_plato} to {upper_plato}"
        )

    for _ in range(_PLATO_INVERSION_MAX_ITERATIONS):
        midpoint_sg = (lower_sg + upper_sg) / 2.0
        midpoint_plato = sg_to_plato(midpoint_sg)

        if abs(midpoint_plato - plato) <= _PLATO_INVERSION_TOLERANCE:
            return midpoint_sg

        if midpoint_plato < plato:
            lower_sg = midpoint_sg
        else:
            upper_sg = midpoint_sg

    return (lower_sg + upper_sg) / 2.0


def wort_refractometer_brix_to_plato(
    apparent_brix: float,
    wort_correction_factor: float,
) -> float:
    """Correct an apparent wort Brix reading to estimated degrees Plato.

    This is a wort-specific refractometer correction for unfermented wort, not
    a general conversion between the Brix and Plato scales. Alcohol changes the
    refractometer response, so this simple correction must not be used for
    fermenting or fermented samples. No default correction factor is provided
    while the appropriate value remains pending ASBC verification.
    """
    _require_finite(apparent_brix, "Apparent Brix")
    _require_positive_correction_factor(wort_correction_factor)

    return apparent_brix / wort_correction_factor


def plato_to_wort_refractometer_brix(
    plato: float,
    wort_correction_factor: float,
) -> float:
    """Estimate the apparent wort Brix reading for a Plato value.

    This is the inverse of ``wort_refractometer_brix_to_plato`` and remains
    an unfermented-wort correction rather than a general scale conversion. It
    must not be used to model refractometer readings once alcohol is present.
    """
    _require_finite(plato, "Plato")
    _require_positive_correction_factor(wort_correction_factor)

    return plato * wort_correction_factor
