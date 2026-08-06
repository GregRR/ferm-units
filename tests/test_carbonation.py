import math

import pytest

from fermunits import (
    co2_grams_per_liter_to_volumes,
    co2_volumes_to_grams_per_liter,
)

EXPECTED_GRAMS_PER_LITER_PER_VOLUME = 10.0 / 5.0607


@pytest.mark.parametrize(
    ("co2_volumes", "expected_grams_per_liter"),
    [
        (0.0, 0.0),
        (1.0, EXPECTED_GRAMS_PER_LITER_PER_VOLUME),
        (2.0, 2.0 * EXPECTED_GRAMS_PER_LITER_PER_VOLUME),
        (2.5, 2.5 * EXPECTED_GRAMS_PER_LITER_PER_VOLUME),
        (3.0, 3.0 * EXPECTED_GRAMS_PER_LITER_PER_VOLUME),
    ],
)
def test_co2_volumes_to_grams_per_liter(
    co2_volumes: float,
    expected_grams_per_liter: float,
) -> None:
    result = co2_volumes_to_grams_per_liter(co2_volumes)

    assert result == pytest.approx(expected_grams_per_liter)


@pytest.mark.parametrize(
    ("grams_per_liter", "expected_volumes"),
    [
        (0.0, 0.0),
        (EXPECTED_GRAMS_PER_LITER_PER_VOLUME, 1.0),
        (2.0 * EXPECTED_GRAMS_PER_LITER_PER_VOLUME, 2.0),
        (2.5 * EXPECTED_GRAMS_PER_LITER_PER_VOLUME, 2.5),
        (3.0 * EXPECTED_GRAMS_PER_LITER_PER_VOLUME, 3.0),
    ],
)
def test_co2_grams_per_liter_to_volumes(
    grams_per_liter: float,
    expected_volumes: float,
) -> None:
    result = co2_grams_per_liter_to_volumes(grams_per_liter)

    assert result == pytest.approx(expected_volumes)


@pytest.mark.parametrize(
    "co2_volumes",
    [
        0.0,
        1.0,
        2.0,
        2.5,
        3.0,
        4.5,
    ],
)
def test_carbonation_round_trip(co2_volumes: float) -> None:
    result = co2_grams_per_liter_to_volumes(co2_volumes_to_grams_per_liter(co2_volumes))

    assert result == pytest.approx(co2_volumes)


@pytest.mark.parametrize(
    "value",
    [
        -1.0,
        math.nan,
        math.inf,
        -math.inf,
    ],
)
def test_co2_volumes_to_grams_per_liter_rejects_invalid_value(
    value: float,
) -> None:
    with pytest.raises(ValueError):
        co2_volumes_to_grams_per_liter(value)


@pytest.mark.parametrize(
    "value",
    [
        -1.0,
        math.nan,
        math.inf,
        -math.inf,
    ],
)
def test_co2_grams_per_liter_to_volumes_rejects_invalid_value(
    value: float,
) -> None:
    with pytest.raises(ValueError):
        co2_grams_per_liter_to_volumes(value)
