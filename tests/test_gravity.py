import math

import pytest

from fermunits.gravity import (
    gravity_points_to_sg,
    plato_to_sg,
    plato_to_wort_refractometer_brix,
    sg_to_gravity_points,
    sg_to_plato,
    wort_refractometer_brix_to_plato,
)


@pytest.mark.parametrize(
    ("specific_gravity", "expected_points"),
    [
        (1.000, 0.0),
        (1.046, 46.0),
        (1.080, 80.0),
    ],
)
def test_sg_to_gravity_points(
    specific_gravity: float,
    expected_points: float,
) -> None:
    result = sg_to_gravity_points(specific_gravity)

    assert result == pytest.approx(expected_points)


@pytest.mark.parametrize(
    "specific_gravity",
    [
        0.0,
        -1.0,
        math.nan,
        math.inf,
        -math.inf,
    ],
)
def test_sg_to_gravity_points_rejects_invalid_sg(
    specific_gravity: float,
) -> None:
    with pytest.raises(ValueError):
        sg_to_gravity_points(specific_gravity)


@pytest.mark.parametrize(
    ("gravity_points", "expected_sg"),
    [
        (0.0, 1.000),
        (46.0, 1.046),
        (80.0, 1.080),
        (-2.0, 0.998),
    ],
)
def test_gravity_points_to_sg(
    gravity_points: float,
    expected_sg: float,
) -> None:
    result = gravity_points_to_sg(gravity_points)

    assert result == pytest.approx(expected_sg)


@pytest.mark.parametrize(
    "gravity_points",
    [
        -1000.0,
        -1001.0,
        math.nan,
        math.inf,
        -math.inf,
    ],
)
def test_gravity_points_to_sg_rejects_invalid_points(
    gravity_points: float,
) -> None:
    with pytest.raises(ValueError):
        gravity_points_to_sg(gravity_points)


def test_gravity_point_conversion_round_trip() -> None:
    original_sg = 1.052

    result = gravity_points_to_sg(sg_to_gravity_points(original_sg))

    assert result == pytest.approx(original_sg)


@pytest.mark.parametrize(
    ("specific_gravity", "expected_plato"),
    [
        (1.000, -0.003),
        (1.048, 11.9120807562),
        (1.080, 19.331001344),
    ],
)
def test_sg_to_plato(
    specific_gravity: float,
    expected_plato: float,
) -> None:
    result = sg_to_plato(specific_gravity)

    assert result == pytest.approx(expected_plato)


@pytest.mark.parametrize(
    "specific_gravity",
    [
        0.0,
        -1.0,
        math.nan,
        math.inf,
        -math.inf,
    ],
)
def test_sg_to_plato_rejects_invalid_sg(
    specific_gravity: float,
) -> None:
    with pytest.raises(ValueError):
        sg_to_plato(specific_gravity)


@pytest.mark.parametrize(
    ("plato", "expected_sg"),
    [
        (-0.003, 1.000),
        (11.9120807562, 1.048),
        (19.331001344, 1.080),
    ],
)
def test_plato_to_sg(
    plato: float,
    expected_sg: float,
) -> None:
    result = plato_to_sg(plato)

    assert result == pytest.approx(expected_sg)


@pytest.mark.parametrize(
    "specific_gravity",
    [
        0.998,
        1.000,
        1.048,
        1.080,
        1.120,
    ],
)
def test_plato_conversion_round_trip(specific_gravity: float) -> None:
    result = plato_to_sg(sg_to_plato(specific_gravity))

    assert result == pytest.approx(specific_gravity)


@pytest.mark.parametrize(
    "plato",
    [
        -300.0,
        200.0,
        math.nan,
        math.inf,
        -math.inf,
    ],
)
def test_plato_to_sg_rejects_invalid_value(plato: float) -> None:
    with pytest.raises(ValueError):
        plato_to_sg(plato)


@pytest.mark.parametrize(
    ("apparent_brix", "correction_factor", "expected_plato"),
    [
        (12.48, 1.04, 12.0),
        (20.80, 1.04, 20.0),
        (13.00, 1.00, 13.0),
    ],
)
def test_wort_refractometer_brix_to_plato(
    apparent_brix: float,
    correction_factor: float,
    expected_plato: float,
) -> None:
    result = wort_refractometer_brix_to_plato(
        apparent_brix,
        correction_factor,
    )

    assert result == pytest.approx(expected_plato)


@pytest.mark.parametrize(
    "apparent_brix",
    [
        math.nan,
        math.inf,
        -math.inf,
    ],
)
def test_wort_refractometer_brix_to_plato_rejects_nonfinite_brix(
    apparent_brix: float,
) -> None:
    with pytest.raises(ValueError, match="Apparent Brix must be finite"):
        wort_refractometer_brix_to_plato(apparent_brix, 1.04)


@pytest.mark.parametrize(
    "correction_factor",
    [
        0.0,
        -1.0,
        math.nan,
        math.inf,
        -math.inf,
    ],
)
def test_wort_refractometer_brix_to_plato_rejects_invalid_factor(
    correction_factor: float,
) -> None:
    with pytest.raises(ValueError):
        wort_refractometer_brix_to_plato(12.0, correction_factor)


@pytest.mark.parametrize(
    ("plato", "correction_factor", "expected_apparent_brix"),
    [
        (12.0, 1.04, 12.48),
        (20.0, 1.04, 20.80),
        (13.0, 1.00, 13.0),
    ],
)
def test_plato_to_wort_refractometer_brix(
    plato: float,
    correction_factor: float,
    expected_apparent_brix: float,
) -> None:
    result = plato_to_wort_refractometer_brix(
        plato,
        correction_factor,
    )

    assert result == pytest.approx(expected_apparent_brix)


@pytest.mark.parametrize(
    "plato",
    [
        math.nan,
        math.inf,
        -math.inf,
    ],
)
def test_plato_to_wort_refractometer_brix_rejects_nonfinite_plato(
    plato: float,
) -> None:
    with pytest.raises(ValueError, match="Plato must be finite"):
        plato_to_wort_refractometer_brix(plato, 1.04)


@pytest.mark.parametrize(
    "correction_factor",
    [
        0.0,
        -1.0,
        math.nan,
        math.inf,
        -math.inf,
    ],
)
def test_plato_to_wort_refractometer_brix_rejects_invalid_factor(
    correction_factor: float,
) -> None:
    with pytest.raises(ValueError):
        plato_to_wort_refractometer_brix(12.0, correction_factor)


def test_wort_refractometer_correction_round_trip() -> None:
    original_apparent_brix = 15.6
    correction_factor = 1.04

    result = plato_to_wort_refractometer_brix(
        wort_refractometer_brix_to_plato(
            original_apparent_brix,
            correction_factor,
        ),
        correction_factor,
    )

    assert result == pytest.approx(original_apparent_brix)
