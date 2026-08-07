import math
from typing import Any

import pytest
from pint import DimensionalityError, UnitRegistry

from fermunits import (
    amount_concentration_to_mass_concentration,
    create_registry,
    mass_concentration_to_amount_concentration,
)


@pytest.fixture
def registry() -> UnitRegistry[Any]:
    """Return an isolated FermUnits registry."""
    return create_registry()


@pytest.mark.parametrize(
    (
        "mass_concentration_value",
        "mass_concentration_unit",
        "molar_mass_value",
        "molar_mass_unit",
        "target_unit",
        "expected",
    ),
    [
        (
            0.0,
            "milligram / liter",
            40.0,
            "gram / mole",
            "millimole / liter",
            0.0,
        ),
        (
            40.0,
            "milligram / liter",
            40.0,
            "gram / mole",
            "millimole / liter",
            1.0,
        ),
        (
            58.44,
            "milligram / liter",
            58.44,
            "gram / mole",
            "millimole / liter",
            1.0,
        ),
        (
            98.0,
            "milligram / liter",
            0.098,
            "kilogram / mole",
            "millimole / liter",
            1.0,
        ),
        (
            1.0,
            "gram / liter",
            100.0,
            "gram / mole",
            "millimole / liter",
            10.0,
        ),
    ],
)
def test_mass_concentration_to_amount_concentration(
    registry: UnitRegistry[Any],
    mass_concentration_value: float,
    mass_concentration_unit: str,
    molar_mass_value: float,
    molar_mass_unit: str,
    target_unit: str,
    expected: float,
) -> None:
    mass_concentration = registry.Quantity(
        mass_concentration_value,
        mass_concentration_unit,
    )
    molar_mass = registry.Quantity(
        molar_mass_value,
        molar_mass_unit,
    )

    result = mass_concentration_to_amount_concentration(
        mass_concentration,
        molar_mass,
    )

    assert result.to(target_unit).magnitude == pytest.approx(expected)


@pytest.mark.parametrize(
    (
        "amount_concentration_value",
        "amount_concentration_unit",
        "molar_mass_value",
        "molar_mass_unit",
        "target_unit",
        "expected",
    ),
    [
        (
            0.0,
            "millimole / liter",
            40.0,
            "gram / mole",
            "milligram / liter",
            0.0,
        ),
        (
            1.0,
            "millimole / liter",
            40.0,
            "gram / mole",
            "milligram / liter",
            40.0,
        ),
        (
            1.0,
            "millimole / liter",
            58.44,
            "gram / mole",
            "milligram / liter",
            58.44,
        ),
        (
            1.0,
            "millimole / liter",
            0.098,
            "kilogram / mole",
            "milligram / liter",
            98.0,
        ),
        (
            10.0,
            "millimole / liter",
            100.0,
            "gram / mole",
            "gram / liter",
            1.0,
        ),
    ],
)
def test_amount_concentration_to_mass_concentration(
    registry: UnitRegistry[Any],
    amount_concentration_value: float,
    amount_concentration_unit: str,
    molar_mass_value: float,
    molar_mass_unit: str,
    target_unit: str,
    expected: float,
) -> None:
    amount_concentration = registry.Quantity(
        amount_concentration_value,
        amount_concentration_unit,
    )
    molar_mass = registry.Quantity(
        molar_mass_value,
        molar_mass_unit,
    )

    result = amount_concentration_to_mass_concentration(
        amount_concentration,
        molar_mass,
    )

    assert result.to(target_unit).magnitude == pytest.approx(expected)


def test_molar_mass_conversion_round_trip(
    registry: UnitRegistry[Any],
) -> None:
    original = registry.Quantity(137.5, "milligram / liter")
    molar_mass = registry.Quantity(55.845, "gram / mole")

    amount_concentration = mass_concentration_to_amount_concentration(
        original,
        molar_mass,
    )
    restored = amount_concentration_to_mass_concentration(
        amount_concentration,
        molar_mass,
    )

    assert restored.to("milligram / liter").magnitude == pytest.approx(137.5)


@pytest.mark.parametrize(
    "molar_mass_magnitude",
    [
        0.0,
        -1.0,
        math.nan,
        math.inf,
        -math.inf,
    ],
)
def test_molar_mass_conversions_reject_invalid_molar_mass(
    registry: UnitRegistry[Any],
    molar_mass_magnitude: float,
) -> None:
    concentration = registry.Quantity(1.0, "millimole / liter")
    molar_mass = registry.Quantity(
        molar_mass_magnitude,
        "gram / mole",
    )

    with pytest.raises(ValueError):
        amount_concentration_to_mass_concentration(
            concentration,
            molar_mass,
        )


def test_mass_to_amount_conversion_rejects_wrong_source_dimension(
    registry: UnitRegistry[Any],
) -> None:
    with pytest.raises(DimensionalityError):
        mass_concentration_to_amount_concentration(
            registry.Quantity(1.0, "mole / liter"),
            registry.Quantity(58.44, "gram / mole"),
        )


def test_amount_to_mass_conversion_rejects_wrong_source_dimension(
    registry: UnitRegistry[Any],
) -> None:
    with pytest.raises(DimensionalityError):
        amount_concentration_to_mass_concentration(
            registry.Quantity(1.0, "gram / liter"),
            registry.Quantity(58.44, "gram / mole"),
        )


def test_molar_mass_conversion_rejects_wrong_molar_mass_dimension(
    registry: UnitRegistry[Any],
) -> None:
    with pytest.raises(DimensionalityError):
        mass_concentration_to_amount_concentration(
            registry.Quantity(58.44, "milligram / liter"),
            registry.Quantity(58.44, "gram / liter"),
        )
