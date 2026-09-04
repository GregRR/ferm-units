import math
import sys
from typing import Any

import pytest
from pint import DimensionalityError, UnitRegistry

from fermunits import (
    create_registry,
    mass_concentration_to_mass_fraction,
    mass_fraction_to_mass_concentration,
)


@pytest.fixture
def registry() -> UnitRegistry[Any]:
    """Return an isolated FermUnits registry."""
    return create_registry()


@pytest.mark.parametrize(
    (
        "concentration_value",
        "concentration_unit",
        "density_kg_per_liter",
        "target_unit",
        "expected",
    ),
    [
        (100.0, "milligram / liter", 1.0, "milligram / kilogram", 100.0),
        (
            100.0,
            "milligram / liter",
            1.05,
            "milligram / kilogram",
            95.23809523809524,
        ),
        (
            25.0,
            "microgram / liter",
            1.0,
            "microgram / kilogram",
            25.0,
        ),
        (1.0, "gram / liter", 0.8, "gram / kilogram", 1.25),
    ],
)
def test_mass_concentration_to_mass_fraction(
    registry: UnitRegistry[Any],
    concentration_value: float,
    concentration_unit: str,
    density_kg_per_liter: float,
    target_unit: str,
    expected: float,
) -> None:
    concentration = registry.Quantity(
        concentration_value,
        concentration_unit,
    )
    density = registry.Quantity(
        density_kg_per_liter,
        "kilogram / liter",
    )

    result = mass_concentration_to_mass_fraction(
        concentration,
        density,
    )

    assert result.to(target_unit).magnitude == pytest.approx(expected)


@pytest.mark.parametrize(
    (
        "fraction_value",
        "fraction_unit",
        "density_kg_per_liter",
        "target_unit",
        "expected",
    ),
    [
        (100.0, "milligram / kilogram", 1.0, "milligram / liter", 100.0),
        (
            100.0,
            "milligram / kilogram",
            1.05,
            "milligram / liter",
            105.0,
        ),
        (
            25.0,
            "microgram / kilogram",
            1.0,
            "microgram / liter",
            25.0,
        ),
        (1.25, "gram / kilogram", 0.8, "gram / liter", 1.0),
    ],
)
def test_mass_fraction_to_mass_concentration(
    registry: UnitRegistry[Any],
    fraction_value: float,
    fraction_unit: str,
    density_kg_per_liter: float,
    target_unit: str,
    expected: float,
) -> None:
    fraction = registry.Quantity(
        fraction_value,
        fraction_unit,
    )
    density = registry.Quantity(
        density_kg_per_liter,
        "kilogram / liter",
    )

    result = mass_fraction_to_mass_concentration(
        fraction,
        density,
    )

    assert result.to(target_unit).magnitude == pytest.approx(expected)


def test_density_assisted_conversion_round_trip(
    registry: UnitRegistry[Any],
) -> None:
    original = registry.Quantity(137.5, "milligram / liter")
    density = registry.Quantity(1.012, "kilogram / liter")

    mass_fraction = mass_concentration_to_mass_fraction(
        original,
        density,
    )
    restored = mass_fraction_to_mass_concentration(
        mass_fraction,
        density,
    )

    assert restored.to("milligram / liter").magnitude == pytest.approx(137.5)


@pytest.mark.parametrize(
    "density_magnitude",
    [
        0.0,
        -1.0,
        math.nan,
        math.inf,
        -math.inf,
    ],
)
def test_density_assisted_conversions_reject_invalid_density(
    registry: UnitRegistry[Any],
    density_magnitude: float,
) -> None:
    concentration = registry.Quantity(100, "milligram / liter")
    density = registry.Quantity(
        density_magnitude,
        "kilogram / liter",
    )

    with pytest.raises(ValueError):
        mass_concentration_to_mass_fraction(
            concentration,
            density,
        )


def test_mass_concentration_conversion_rejects_wrong_source_dimension(
    registry: UnitRegistry[Any],
) -> None:
    with pytest.raises(DimensionalityError):
        mass_concentration_to_mass_fraction(
            registry.Quantity(1, "mole / liter"),
            registry.Quantity(1, "kilogram / liter"),
        )


def test_mass_fraction_conversion_rejects_wrong_source_dimension(
    registry: UnitRegistry[Any],
) -> None:
    with pytest.raises(DimensionalityError):
        mass_fraction_to_mass_concentration(
            registry.Quantity(1, "milligram / liter"),
            registry.Quantity(1, "kilogram / liter"),
        )


def test_density_assisted_conversion_rejects_wrong_density_dimension(
    registry: UnitRegistry[Any],
) -> None:
    with pytest.raises(DimensionalityError):
        mass_concentration_to_mass_fraction(
            registry.Quantity(100, "milligram / liter"),
            registry.Quantity(1, "liter"),
        )


def test_density_assisted_conversions_reject_nonfinite_results(
    registry: UnitRegistry[Any],
) -> None:
    with pytest.raises(ValueError, match="representable finite range"):
        mass_concentration_to_mass_fraction(
            registry.Quantity(sys.float_info.max, "gram / liter"),
            registry.Quantity(sys.float_info.min, "kilogram / liter"),
        )

    with pytest.raises(ValueError, match="representable finite range"):
        mass_fraction_to_mass_concentration(
            registry.Quantity(sys.float_info.max, "dimensionless"),
            registry.Quantity(sys.float_info.max, "kilogram / liter"),
        )
