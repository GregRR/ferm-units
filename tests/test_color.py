import math
import sys

import pytest

from fermunits import (
    ebc_to_srm,
    lovibond_to_srm_approx,
    srm_to_ebc,
    srm_to_lovibond_approx,
)


@pytest.mark.parametrize(
    ("srm", "expected_ebc"),
    [
        (0.0, 0.0),
        (1.0, 25.0 / 12.7),
        (10.0, 250.0 / 12.7),
        (40.0, 1000.0 / 12.7),
    ],
)
def test_srm_to_ebc(srm: float, expected_ebc: float) -> None:
    assert srm_to_ebc(srm) == pytest.approx(expected_ebc)


@pytest.mark.parametrize(
    ("ebc", "expected_srm"),
    [
        (0.0, 0.0),
        (25.0 / 12.7, 1.0),
        (250.0 / 12.7, 10.0),
        (1000.0 / 12.7, 40.0),
    ],
)
def test_ebc_to_srm(ebc: float, expected_srm: float) -> None:
    assert ebc_to_srm(ebc) == pytest.approx(expected_srm)


@pytest.mark.parametrize(
    "srm",
    [
        0.0,
        1.0,
        5.0,
        20.0,
        40.0,
    ],
)
def test_srm_ebc_round_trip(srm: float) -> None:
    assert ebc_to_srm(srm_to_ebc(srm)) == pytest.approx(srm)


def test_srm_ebc_scale_factor_anchor() -> None:
    assert srm_to_ebc(12.7) == pytest.approx(25.0)
    assert ebc_to_srm(25.0) == pytest.approx(12.7)


@pytest.mark.parametrize(
    ("lovibond", "expected_srm"),
    [
        (1.0, 0.5946),
        (4.0, 4.6584),
        (10.0, 12.786),
        (40.0, 53.424),
    ],
)
def test_lovibond_to_srm_approx(
    lovibond: float,
    expected_srm: float,
) -> None:
    assert lovibond_to_srm_approx(lovibond) == pytest.approx(expected_srm)


@pytest.mark.parametrize(
    "lovibond",
    [
        1.0,
        4.0,
        10.0,
        40.0,
    ],
)
def test_lovibond_srm_approximation_round_trip(
    lovibond: float,
) -> None:
    result = srm_to_lovibond_approx(lovibond_to_srm_approx(lovibond))

    assert result == pytest.approx(lovibond)


@pytest.mark.parametrize(
    ("srm", "expected_lovibond"),
    [
        (0.0, 0.76 / 1.3546),
        (4.6584, 4.0),
        (12.786, 10.0),
        (53.424, 40.0),
    ],
)
def test_srm_to_lovibond_approx(
    srm: float,
    expected_lovibond: float,
) -> None:
    assert srm_to_lovibond_approx(srm) == pytest.approx(expected_lovibond)


@pytest.mark.parametrize(
    "function",
    [
        srm_to_ebc,
        ebc_to_srm,
        lovibond_to_srm_approx,
        srm_to_lovibond_approx,
    ],
)
@pytest.mark.parametrize(
    "value",
    [
        -1.0,
        math.nan,
        math.inf,
        -math.inf,
    ],
)
def test_color_functions_reject_invalid_values(
    function: object,
    value: float,
) -> None:
    with pytest.raises(ValueError):
        function(value)  # type: ignore[operator]


def test_lovibond_approximation_rejects_value_below_useful_range() -> None:
    with pytest.raises(
        ValueError,
        match="below the useful range",
    ):
        lovibond_to_srm_approx(0.0)


@pytest.mark.parametrize(
    "function",
    [
        srm_to_ebc,
        lovibond_to_srm_approx,
    ],
)
def test_color_conversion_rejects_nonfinite_result_from_finite_input(
    function: object,
) -> None:
    with pytest.raises(ValueError, match="representable finite range"):
        function(sys.float_info.max)  # type: ignore[operator]
