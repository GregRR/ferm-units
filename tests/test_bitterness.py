import math
import sys

import pytest

from fermunits import (
    absorbance_275nm_to_bitterness_units,
    bitterness_units_to_absorbance_275nm,
)


@pytest.mark.parametrize(
    ("absorbance", "expected_bitterness_units"),
    [
        (0.0, 0.0),
        (0.1, 5.0),
        (0.2, 10.0),
        (0.5, 25.0),
        (1.0, 50.0),
        (2.0, 100.0),
    ],
)
def test_absorbance_275nm_to_bitterness_units(
    absorbance: float,
    expected_bitterness_units: float,
) -> None:
    result = absorbance_275nm_to_bitterness_units(absorbance)

    assert result == pytest.approx(expected_bitterness_units)


def test_absorbance_275nm_keyword_names_method_extract() -> None:
    result = absorbance_275nm_to_bitterness_units(
        extract_absorbance_275nm=0.5,
    )

    assert result == pytest.approx(25.0)


@pytest.mark.parametrize(
    ("bitterness_units", "expected_absorbance"),
    [
        (0.0, 0.0),
        (5.0, 0.1),
        (10.0, 0.2),
        (25.0, 0.5),
        (50.0, 1.0),
        (100.0, 2.0),
    ],
)
def test_bitterness_units_to_absorbance_275nm(
    bitterness_units: float,
    expected_absorbance: float,
) -> None:
    result = bitterness_units_to_absorbance_275nm(bitterness_units)

    assert result == pytest.approx(expected_absorbance)


@pytest.mark.parametrize(
    "absorbance",
    [
        0.0,
        0.1,
        0.5,
        1.0,
        2.0,
    ],
)
def test_bitterness_conversion_round_trip(
    absorbance: float,
) -> None:
    result = bitterness_units_to_absorbance_275nm(
        absorbance_275nm_to_bitterness_units(absorbance)
    )

    assert result == pytest.approx(absorbance)


@pytest.mark.parametrize(
    "value",
    [
        -1.0,
        math.nan,
        math.inf,
        -math.inf,
    ],
)
def test_absorbance_275nm_to_bitterness_units_rejects_invalid_value(
    value: float,
) -> None:
    with pytest.raises(ValueError):
        absorbance_275nm_to_bitterness_units(value)


@pytest.mark.parametrize(
    "value",
    [
        -1.0,
        math.nan,
        math.inf,
        -math.inf,
    ],
)
def test_bitterness_units_to_absorbance_275nm_rejects_invalid_value(
    value: float,
) -> None:
    with pytest.raises(ValueError):
        bitterness_units_to_absorbance_275nm(value)


def test_bitterness_conversion_rejects_nonfinite_result_from_finite_input() -> None:
    with pytest.raises(ValueError, match="representable finite range"):
        absorbance_275nm_to_bitterness_units(sys.float_info.max)
