import math
import sys

import pytest
from pint import DimensionalityError

from fermunits import (
    Q_,
    co2_grams_per_liter_to_volumes,
    co2_mass_concentration_to_volumes,
    co2_volumes_to_grams_per_liter,
    co2_volumes_to_mass_concentration,
)

EXPECTED_GRAMS_PER_LITER_PER_VOLUME = 1000.0 / 506.07


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
    "co2_volumes",
    [
        0.0,
        1.0,
        2.5,
        4.5,
    ],
)
def test_quantity_aware_carbonation_round_trip(co2_volumes: float) -> None:
    concentration = co2_volumes_to_mass_concentration(co2_volumes)
    restored = co2_mass_concentration_to_volumes(concentration)

    assert concentration.to("gram / liter").magnitude == pytest.approx(
        co2_volumes * EXPECTED_GRAMS_PER_LITER_PER_VOLUME
    )
    assert restored == pytest.approx(co2_volumes)


@pytest.mark.parametrize(
    ("unit_name", "magnitude"),
    [
        ("gram / liter", 2.5 * EXPECTED_GRAMS_PER_LITER_PER_VOLUME),
        ("milligram / liter", 2500.0 * EXPECTED_GRAMS_PER_LITER_PER_VOLUME),
        ("kilogram / meter ** 3", 2.5 * EXPECTED_GRAMS_PER_LITER_PER_VOLUME),
    ],
)
def test_co2_mass_concentration_to_volumes_accepts_compatible_units(
    unit_name: str,
    magnitude: float,
) -> None:
    result = co2_mass_concentration_to_volumes(Q_(magnitude, unit_name))

    assert result == pytest.approx(2.5)


@pytest.mark.parametrize(
    "value",
    [
        -1.0,
        math.nan,
        math.inf,
        -math.inf,
    ],
)
def test_co2_volumes_to_mass_concentration_rejects_invalid_value(
    value: float,
) -> None:
    with pytest.raises(ValueError):
        co2_volumes_to_mass_concentration(value)


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


@pytest.mark.parametrize(
    "value",
    [
        -1.0,
        math.nan,
        math.inf,
        -math.inf,
    ],
)
def test_co2_mass_concentration_to_volumes_rejects_invalid_value(
    value: float,
) -> None:
    with pytest.raises(ValueError):
        co2_mass_concentration_to_volumes(Q_(value, "gram / liter"))


def test_co2_mass_concentration_to_volumes_rejects_wrong_dimension() -> None:
    with pytest.raises(DimensionalityError):
        co2_mass_concentration_to_volumes(Q_(2.5, "psi"))


def test_carbonation_conversion_rejects_nonfinite_result_from_finite_input() -> None:
    with pytest.raises(ValueError, match="representable finite range"):
        co2_volumes_to_mass_concentration(sys.float_info.max)
