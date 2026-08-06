"""Water-treatment engine unit contract tests."""

from typing import Any

import pytest
from pint import DimensionalityError, UnitRegistry

from fermunits import Q_, create_registry


@pytest.fixture
def registry() -> UnitRegistry[Any]:
    """Return an isolated FermUnits registry."""
    return create_registry()


@pytest.mark.parametrize(
    "unit_name",
    [
        "liter",
        "milliliter",
        "US_liquid_gallon",
        "imperial_gallon",
        "hectoliter",
        "kilogram",
        "gram",
        "milligram",
        "microgram",
        "ounce",
        "pound",
        "milligram / liter",
        "microgram / liter",
        "gram / liter",
        "mole / liter",
        "millimole / liter",
        "gram / milliliter",
        "kilogram / liter",
        "degree_Celsius",
        "degree_Fahrenheit",
        "kelvin",
        "gram / US_liquid_gallon",
        "gram / hectoliter",
        "pound / us_beer_barrel",
        "us_beer_barrel",
    ],
)
def test_required_water_engine_units_parse(
    registry: UnitRegistry[Any],
    unit_name: str,
) -> None:
    """Every required water-engine unit must parse in FermUnits."""
    registry.Unit(unit_name)


@pytest.mark.parametrize(
    ("magnitude", "source_unit", "target_unit", "expected"),
    [
        (1.0, "US_liquid_gallon", "liter", 3.785411784),
        (1.0, "imperial_gallon", "liter", 4.54609),
        (
            1.0,
            "gram / US_liquid_gallon",
            "milligram / liter",
            264.1720523581484,
        ),
        (1.0, "gram / hectoliter", "milligram / liter", 10.0),
        (
            1.0,
            "pound / us_beer_barrel",
            "gram / hectoliter",
            386.53686231256977,
        ),
        (1.0, "mole / liter", "millimole / liter", 1000.0),
        (1.0, "gram / milliliter", "kilogram / liter", 1.0),
        (0.0, "degree_Celsius", "degree_Fahrenheit", 32.0),
        (273.15, "kelvin", "degree_Celsius", 0.0),
    ],
)
def test_required_water_engine_conversions(
    registry: UnitRegistry[Any],
    magnitude: float,
    source_unit: str,
    target_unit: str,
    expected: float,
) -> None:
    """Representative downstream conversions must remain stable."""
    converted = registry.Quantity(magnitude, source_unit).to(target_unit)

    assert converted.magnitude == pytest.approx(expected, rel=1e-12, abs=1e-12)


def test_us_beer_barrel_is_31_us_gallons(
    registry: UnitRegistry[Any],
) -> None:
    """FermUnits must retain the established US beer barrel definition."""
    converted = registry.Quantity(1, "us_beer_barrel").to("US_liquid_gallon")

    assert converted.magnitude == pytest.approx(31.0)


def test_compound_units_preserve_expected_dimensionality(
    registry: UnitRegistry[Any],
) -> None:
    """Compound units must resolve to the expected physical dimensions."""
    assert (
        registry.Unit("milligram / liter").dimensionality
        == registry.Unit("gram / liter").dimensionality
    )
    assert (
        registry.Unit("mole / liter").dimensionality
        == registry.Unit("millimole / liter").dimensionality
    )
    assert (
        registry.Unit("gram / milliliter").dimensionality
        == registry.Unit("kilogram / liter").dimensionality
    )


def test_incompatible_water_engine_dimensions_are_rejected(
    registry: UnitRegistry[Any],
) -> None:
    """Pint must reject dimensionally invalid conversions."""
    with pytest.raises(DimensionalityError):
        registry.Quantity(1, "gram / liter").to("mole / liter")


def test_package_level_quantity_alias_uses_fermunits_registry() -> None:
    """The public Q_ alias must know FermUnits custom definitions."""
    converted = Q_(1, "us_beer_barrel").to("US_liquid_gallon")

    assert converted.magnitude == pytest.approx(31.0)
