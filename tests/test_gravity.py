import pytest

from fermunits.gravity import (
    gravity_points_to_sg,
    sg_to_gravity_points,
    sg_to_plato,
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
    ("gravity_points", "expected_sg"),
    [
        (0.0, 1.000),
        (46.0, 1.046),
        (80.0, 1.080),
    ],
)
def test_gravity_points_to_sg(
    gravity_points: float,
    expected_sg: float,
) -> None:
    result = gravity_points_to_sg(gravity_points)

    assert result == pytest.approx(expected_sg)


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
