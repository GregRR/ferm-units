"""Conversions for brewing gravity and extract measurements."""


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
