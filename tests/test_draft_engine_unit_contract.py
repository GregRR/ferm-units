"""Draft-system engine unit contract tests."""

from typing import Any

import pytest
from pint import DimensionalityError, UnitRegistry

from fermunits import (
    co2_mass_concentration_to_volumes,
    co2_volumes_to_mass_concentration,
    create_registry,
)


@pytest.fixture
def registry() -> UnitRegistry[Any]:
    """Return an isolated FermUnits registry."""
    return create_registry()


@pytest.mark.parametrize(
    "unit_name",
    [
        "degree_Celsius",
        "degree_Fahrenheit",
        "kelvin",
        "delta_degC",
        "delta_degF",
        "psi",
        "kilopascal",
        "bar",
        "pascal",
        "foot",
        "inch",
        "millimeter",
        "meter",
        "US_fluid_ounce / second",
        "US_liquid_gallon / minute",
        "liter / minute",
        "milliliter / second",
        "kilogram / meter ** 3",
        "kilogram / liter",
        "gram / milliliter",
        "pascal * second",
        "centipoise",
        "psi / foot",
        "pascal / meter",
        "gram / liter",
    ],
)
def test_required_draft_engine_units_parse(
    registry: UnitRegistry[Any],
    unit_name: str,
) -> None:
    """Every required draft-engine physical unit must parse in FermUnits."""
    registry.Unit(unit_name)


@pytest.mark.parametrize(
    ("magnitude", "source_unit", "target_unit", "expected"),
    [
        (38.0, "degree_Fahrenheit", "degree_Celsius", 10.0 / 3.0),
        (4.0, "degree_Celsius", "degree_Fahrenheit", 39.2),
        (1.0, "delta_degF", "kelvin", 5.0 / 9.0),
        (1.0, "delta_degC", "delta_degF", 1.8),
        (1.0, "bar", "pascal", 100000.0),
        (1.0, "psi", "kilopascal", 6.894757293168361),
        (10.0, "foot", "meter", 3.048),
        (3.0 / 16.0, "inch", "millimeter", 4.7625),
        (1.0, "US_fluid_ounce / second", "milliliter / second", 29.5735295625),
        (1.0, "US_liquid_gallon / minute", "liter / minute", 3.785411784),
        (1.0, "liter / minute", "meter ** 3 / second", 1.0e-3 / 60.0),
        (1.0, "gram / liter", "kilogram / meter ** 3", 1.0),
        (1.0, "centipoise", "pascal * second", 0.001),
        (1.0, "psi / foot", "pascal / meter", 22620.59479385945),
    ],
)
def test_required_draft_engine_conversions(
    registry: UnitRegistry[Any],
    magnitude: float,
    source_unit: str,
    target_unit: str,
    expected: float,
) -> None:
    """Representative downstream conversions must remain stable."""
    converted = registry.Quantity(magnitude, source_unit).to(target_unit)

    assert converted.magnitude == pytest.approx(expected, rel=1e-12, abs=1e-12)


def test_draft_engine_contract_distinguishes_us_and_imperial_liquid_volume(
    registry: UnitRegistry[Any],
) -> None:
    """Explicit US aliases must not silently resolve as Imperial measures."""
    us_ounce = registry.Quantity(1.0, "US_fluid_ounce").to("milliliter")
    imperial_ounce = registry.Quantity(1.0, "imperial_fluid_ounce").to("milliliter")
    us_gallon = registry.Quantity(1.0, "US_liquid_gallon").to("liter")
    imperial_gallon = registry.Quantity(1.0, "imperial_gallon").to("liter")

    assert us_ounce.magnitude == pytest.approx(29.5735295625)
    assert imperial_ounce.magnitude == pytest.approx(28.4130625)
    assert us_gallon.magnitude == pytest.approx(3.785411784)
    assert imperial_gallon.magnitude == pytest.approx(4.54609)


def test_pressure_gradient_has_pressure_per_length_dimensionality(
    registry: UnitRegistry[Any],
) -> None:
    """Draft line restriction is represented as pressure drop per length."""
    assert (
        registry.Unit("psi / foot").dimensionality
        == registry.Unit("pascal / meter").dimensionality
    )

    with pytest.raises(DimensionalityError):
        registry.Quantity(1.0, "pound / foot").to("psi / foot")


@pytest.mark.parametrize(
    ("source_unit", "target_unit"),
    [
        ("psi", "meter"),
        ("liter / minute", "meter"),
        ("psi / foot", "psi"),
        ("gram / liter", "psi"),
        ("centipoise", "liter / minute"),
    ],
)
def test_incompatible_draft_engine_dimensions_are_rejected(
    registry: UnitRegistry[Any],
    source_unit: str,
    target_unit: str,
) -> None:
    """Pint must reject dimensionally invalid draft-engine conversions."""
    with pytest.raises(DimensionalityError):
        registry.Quantity(1.0, source_unit).to(target_unit)


def test_draft_engine_carbonation_boundary_is_quantity_aware() -> None:
    """Physical CO₂ concentration must cross the boundary as a Pint quantity."""
    concentration = co2_volumes_to_mass_concentration(2.5)
    restored = co2_mass_concentration_to_volumes(
        concentration.to("kilogram / meter ** 3")
    )

    assert concentration.to("gram / liter").magnitude == pytest.approx(
        2.5 * 10.0 / 5.0607
    )
    assert restored == pytest.approx(2.5)
