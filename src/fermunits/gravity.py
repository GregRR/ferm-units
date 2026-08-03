"""Conversions for brewing gravity and extract measurements."""

_PLATO_INVERSION_LOWER_SG = 0.5
_PLATO_INVERSION_UPPER_SG = 2.0
_PLATO_INVERSION_TOLERANCE = 1e-12
_PLATO_INVERSION_MAX_ITERATIONS = 100


def sg_to_gravity_points(specific_gravity: float) -> float:
    """Convert specific gravity to gravity points."""
    return (specific_gravity - 1.0) * 1000.0


def gravity_points_to_sg(gravity_points: float) -> float:
    """Convert gravity points to specific gravity."""
    return 1.0 + (gravity_points / 1000.0)


def sg_to_plato(specific_gravity: float) -> float:
    """Estimate degrees Plato from specific gravity.

    This polynomial is provisional pending verification against an
    authoritative ASBC method or extract table.
    """
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
    pending verification against an authoritative ASBC method or extract table.
    """
    lower_sg = _PLATO_INVERSION_LOWER_SG
    upper_sg = _PLATO_INVERSION_UPPER_SG
    lower_plato = sg_to_plato(lower_sg)
    upper_plato = sg_to_plato(upper_sg)

    if not lower_plato <= plato <= upper_plato:
        raise ValueError(
            f"Plato value must be between {lower_plato} and {upper_plato}"
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

    This is a wort-specific refractometer correction, not a general conversion
    between the Brix and Plato scales. No default correction factor is provided
    while the appropriate value remains pending ASBC verification.
    """
    if wort_correction_factor <= 0.0:
        raise ValueError("Wort correction factor must be greater than zero")

    return apparent_brix / wort_correction_factor


def plato_to_wort_refractometer_brix(
    plato: float,
    wort_correction_factor: float,
) -> float:
    """Estimate the apparent wort Brix reading for a Plato value.

    This is the inverse of ``wort_refractometer_brix_to_plato`` and remains
    a wort-specific correction rather than a general scale conversion.
    """
    if wort_correction_factor <= 0.0:
        raise ValueError("Wort correction factor must be greater than zero")

    return plato * wort_correction_factor
