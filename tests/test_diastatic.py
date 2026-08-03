import math

import pytest

from fermunits import (
    lintner_to_windisch_kolbach,
    windisch_kolbach_to_lintner,
)


@pytest.mark.parametrize(
    ("lintner", "expected_windisch_kolbach"),
    [
        (16.0 / 3.5, 0.0),
        (40.0, 124.0),
        (60.0, 194.0),
        (100.0, 334.0),
    ],
)
def test_lintner_to_windisch_kolbach(
    lintner: float,
    expected_windisch_kolbach: float,
) -> None:
    result = lintner_to_windisch_kolbach(lintner)

    assert result == pytest.approx(expected_windisch_kolbach)


@pytest.mark.parametrize(
    ("windisch_kolbach", "expected_lintner"),
    [
        (0.0, 16.0 / 3.5),
        (124.0, 40.0),
        (194.0, 60.0),
        (334.0, 100.0),
    ],
)
def test_windisch_kolbach_to_lintner(
    windisch_kolbach: float,
    expected_lintner: float,
) -> None:
    result = windisch_kolbach_to_lintner(windisch_kolbach)

    assert result == pytest.approx(expected_lintner)


@pytest.mark.parametrize(
    "lintner",
    [
        10.0,
        40.0,
        60.0,
        100.0,
        160.0,
    ],
)
def test_diastatic_power_round_trip(lintner: float) -> None:
    result = windisch_kolbach_to_lintner(
        lintner_to_windisch_kolbach(lintner)
    )

    assert result == pytest.approx(lintner)


@pytest.mark.parametrize(
    "value",
    [
        -1.0,
        math.nan,
        math.inf,
        -math.inf,
    ],
)
def test_windisch_kolbach_to_lintner_rejects_invalid_value(
    value: float,
) -> None:
    with pytest.raises(ValueError):
        windisch_kolbach_to_lintner(value)


@pytest.mark.parametrize(
    "value",
    [
        -1.0,
        math.nan,
        math.inf,
        -math.inf,
    ],
)
def test_lintner_to_windisch_kolbach_rejects_invalid_value(
    value: float,
) -> None:
    with pytest.raises(ValueError):
        lintner_to_windisch_kolbach(value)


def test_lintner_conversion_rejects_value_below_useful_range() -> None:
    with pytest.raises(
        ValueError,
        match="below the useful range",
    ):
        lintner_to_windisch_kolbach(0.0)
