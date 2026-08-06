import math
from typing import Any

import pytest
from pint import DimensionalityError, UnitRegistry

from fermunits import (
    amount_concentration_to_equivalent_concentration,
    amount_to_equivalents,
    caco3_basis_mass_concentration_to_equivalent_concentration,
    create_registry,
    equivalent_concentration_to_amount_concentration,
    equivalent_concentration_to_caco3_basis_mass_concentration,
    equivalent_concentration_to_mass_concentration,
    equivalents_to_amount,
    mass_concentration_to_equivalent_concentration,
)


@pytest.fixture
def registry() -> UnitRegistry[Any]:
    """Return an isolated FermUnits registry."""
    return create_registry()


@pytest.mark.parametrize(
    "unit_name",
    [
        "equivalent",
        "eq",
        "milliequivalent",
        "mEq",
        "equivalent / liter",
        "eq / liter",
        "milliequivalent / liter",
        "mEq / liter",
    ],
)
def test_equivalent_units_parse(
    registry: UnitRegistry[Any],
    unit_name: str,
) -> None:
    registry.Unit(unit_name)


def test_milliequivalent_is_one_thousandth_of_equivalent(
    registry: UnitRegistry[Any],
) -> None:
    converted = registry.Quantity(1, "equivalent").to("milliequivalent")

    assert converted.magnitude == pytest.approx(1000.0)


def test_equivalent_is_dimensionally_distinct_from_mole(
    registry: UnitRegistry[Any],
) -> None:
    with pytest.raises(DimensionalityError):
        registry.Quantity(1, "mole").to("equivalent")


@pytest.mark.parametrize(
    ("millimoles", "equivalence_factor", "expected_milliequivalents"),
    [
        (0.0, 1.0, 0.0),
        (1.0, 1.0, 1.0),
        (1.0, 2.0, 2.0),
        (2.5, 3.0, 7.5),
        (1.0, 5.0, 5.0),
    ],
)
def test_amount_to_equivalents(
    registry: UnitRegistry[Any],
    millimoles: float,
    equivalence_factor: float,
    expected_milliequivalents: float,
) -> None:
    amount = registry.Quantity(millimoles, "millimole")

    result = amount_to_equivalents(amount, equivalence_factor)

    assert result.to("milliequivalent").magnitude == pytest.approx(
        expected_milliequivalents
    )


@pytest.mark.parametrize(
    ("milliequivalents", "equivalence_factor", "expected_millimoles"),
    [
        (0.0, 1.0, 0.0),
        (1.0, 1.0, 1.0),
        (2.0, 2.0, 1.0),
        (7.5, 3.0, 2.5),
        (5.0, 5.0, 1.0),
    ],
)
def test_equivalents_to_amount(
    registry: UnitRegistry[Any],
    milliequivalents: float,
    equivalence_factor: float,
    expected_millimoles: float,
) -> None:
    equivalent_amount = registry.Quantity(
        milliequivalents,
        "milliequivalent",
    )

    result = equivalents_to_amount(
        equivalent_amount,
        equivalence_factor,
    )

    assert result.to("millimole").magnitude == pytest.approx(expected_millimoles)


@pytest.mark.parametrize(
    ("millimoles_per_liter", "equivalence_factor", "expected_meq_per_liter"),
    [
        (0.0, 1.0, 0.0),
        (1.0, 1.0, 1.0),
        (1.0, 2.0, 2.0),
        (2.5, 3.0, 7.5),
    ],
)
def test_amount_concentration_to_equivalent_concentration(
    registry: UnitRegistry[Any],
    millimoles_per_liter: float,
    equivalence_factor: float,
    expected_meq_per_liter: float,
) -> None:
    amount_concentration = registry.Quantity(
        millimoles_per_liter,
        "millimole / liter",
    )

    result = amount_concentration_to_equivalent_concentration(
        amount_concentration,
        equivalence_factor,
    )

    assert result.to("milliequivalent / liter").magnitude == pytest.approx(
        expected_meq_per_liter
    )


@pytest.mark.parametrize(
    ("meq_per_liter", "equivalence_factor", "expected_mmol_per_liter"),
    [
        (0.0, 1.0, 0.0),
        (1.0, 1.0, 1.0),
        (2.0, 2.0, 1.0),
        (7.5, 3.0, 2.5),
    ],
)
def test_equivalent_concentration_to_amount_concentration(
    registry: UnitRegistry[Any],
    meq_per_liter: float,
    equivalence_factor: float,
    expected_mmol_per_liter: float,
) -> None:
    equivalent_concentration = registry.Quantity(
        meq_per_liter,
        "milliequivalent / liter",
    )

    result = equivalent_concentration_to_amount_concentration(
        equivalent_concentration,
        equivalence_factor,
    )

    assert result.to("millimole / liter").magnitude == pytest.approx(
        expected_mmol_per_liter
    )


def test_equivalent_conversion_round_trip(
    registry: UnitRegistry[Any],
) -> None:
    original = registry.Quantity(2.75, "millimole / liter")

    equivalents = amount_concentration_to_equivalent_concentration(
        original,
        equivalence_factor=2.0,
    )
    restored = equivalent_concentration_to_amount_concentration(
        equivalents,
        equivalence_factor=2.0,
    )

    assert restored.to("millimole / liter").magnitude == pytest.approx(2.75)


@pytest.mark.parametrize(
    "equivalence_factor",
    [
        0.0,
        -1.0,
        math.nan,
        math.inf,
        -math.inf,
    ],
)
def test_equivalent_conversions_reject_invalid_factor(
    registry: UnitRegistry[Any],
    equivalence_factor: float,
) -> None:
    amount = registry.Quantity(1, "mole")

    with pytest.raises(ValueError):
        amount_to_equivalents(amount, equivalence_factor)


def test_amount_to_equivalents_rejects_wrong_dimension(
    registry: UnitRegistry[Any],
) -> None:
    with pytest.raises(DimensionalityError):
        amount_to_equivalents(
            registry.Quantity(1, "gram"),
            equivalence_factor=1.0,
        )


def test_concentration_conversion_rejects_wrong_dimension(
    registry: UnitRegistry[Any],
) -> None:
    with pytest.raises(DimensionalityError):
        amount_concentration_to_equivalent_concentration(
            registry.Quantity(1, "gram / liter"),
            equivalence_factor=1.0,
        )


@pytest.mark.parametrize(
    (
        "mass_milligrams_per_liter",
        "equivalent_mass_grams_per_equivalent",
        "expected_meq_per_liter",
    ),
    [
        (0.0, 50.0, 0.0),
        (50.0, 50.0, 1.0),
        (100.0, 50.0, 2.0),
        (75.0, 75.0, 1.0),
    ],
)
def test_mass_concentration_to_equivalent_concentration(
    registry: UnitRegistry[Any],
    mass_milligrams_per_liter: float,
    equivalent_mass_grams_per_equivalent: float,
    expected_meq_per_liter: float,
) -> None:
    mass_concentration = registry.Quantity(
        mass_milligrams_per_liter,
        "milligram / liter",
    )

    result = mass_concentration_to_equivalent_concentration(
        mass_concentration,
        equivalent_mass_grams_per_equivalent,
    )

    assert result.to("milliequivalent / liter").magnitude == pytest.approx(
        expected_meq_per_liter
    )


@pytest.mark.parametrize(
    (
        "meq_per_liter",
        "equivalent_mass_grams_per_equivalent",
        "expected_milligrams_per_liter",
    ),
    [
        (0.0, 50.0, 0.0),
        (1.0, 50.0, 50.0),
        (2.0, 50.0, 100.0),
        (1.0, 75.0, 75.0),
    ],
)
def test_equivalent_concentration_to_mass_concentration(
    registry: UnitRegistry[Any],
    meq_per_liter: float,
    equivalent_mass_grams_per_equivalent: float,
    expected_milligrams_per_liter: float,
) -> None:
    equivalent_concentration = registry.Quantity(
        meq_per_liter,
        "milliequivalent / liter",
    )

    result = equivalent_concentration_to_mass_concentration(
        equivalent_concentration,
        equivalent_mass_grams_per_equivalent,
    )

    assert result.to("milligram / liter").magnitude == pytest.approx(
        expected_milligrams_per_liter
    )


@pytest.mark.parametrize(
    ("mg_per_liter_as_caco3", "expected_meq_per_liter"),
    [
        (0.0, 0.0),
        (50.0, 1.0),
        (100.0, 2.0),
        (125.0, 2.5),
    ],
)
def test_caco3_basis_mass_concentration_to_equivalent_concentration(
    registry: UnitRegistry[Any],
    mg_per_liter_as_caco3: float,
    expected_meq_per_liter: float,
) -> None:
    reported_concentration = registry.Quantity(
        mg_per_liter_as_caco3,
        "milligram / liter",
    )

    result = caco3_basis_mass_concentration_to_equivalent_concentration(
        reported_concentration
    )

    assert result.to("milliequivalent / liter").magnitude == pytest.approx(
        expected_meq_per_liter
    )


@pytest.mark.parametrize(
    ("meq_per_liter", "expected_mg_per_liter_as_caco3"),
    [
        (0.0, 0.0),
        (1.0, 50.0),
        (2.0, 100.0),
        (2.5, 125.0),
    ],
)
def test_equivalent_concentration_to_caco3_basis_mass_concentration(
    registry: UnitRegistry[Any],
    meq_per_liter: float,
    expected_mg_per_liter_as_caco3: float,
) -> None:
    equivalent_concentration = registry.Quantity(
        meq_per_liter,
        "milliequivalent / liter",
    )

    result = equivalent_concentration_to_caco3_basis_mass_concentration(
        equivalent_concentration
    )

    assert result.to("milligram / liter").magnitude == pytest.approx(
        expected_mg_per_liter_as_caco3
    )


def test_caco3_basis_conversion_accepts_other_mass_concentration_units(
    registry: UnitRegistry[Any],
) -> None:
    reported_concentration = registry.Quantity(
        0.1,
        "gram / liter",
    )

    result = caco3_basis_mass_concentration_to_equivalent_concentration(
        reported_concentration
    )

    assert result.to("milliequivalent / liter").magnitude == pytest.approx(2.0)


def test_caco3_basis_conversion_round_trip(
    registry: UnitRegistry[Any],
) -> None:
    original = registry.Quantity(137.5, "milligram / liter")

    equivalents = caco3_basis_mass_concentration_to_equivalent_concentration(original)
    restored = equivalent_concentration_to_caco3_basis_mass_concentration(equivalents)

    assert restored.to("milligram / liter").magnitude == pytest.approx(137.5)


@pytest.mark.parametrize(
    "equivalent_mass",
    [
        0.0,
        -1.0,
        math.nan,
        math.inf,
        -math.inf,
    ],
)
def test_mass_equivalent_conversions_reject_invalid_equivalent_mass(
    registry: UnitRegistry[Any],
    equivalent_mass: float,
) -> None:
    mass_concentration = registry.Quantity(50, "milligram / liter")

    with pytest.raises(ValueError):
        mass_concentration_to_equivalent_concentration(
            mass_concentration,
            equivalent_mass,
        )


def test_mass_equivalent_conversion_rejects_wrong_dimension(
    registry: UnitRegistry[Any],
) -> None:
    with pytest.raises(DimensionalityError):
        mass_concentration_to_equivalent_concentration(
            registry.Quantity(1, "mole / liter"),
            equivalent_mass_grams_per_equivalent=50.0,
        )


def test_reverse_mass_equivalent_conversion_rejects_wrong_dimension(
    registry: UnitRegistry[Any],
) -> None:
    with pytest.raises(DimensionalityError):
        equivalent_concentration_to_mass_concentration(
            registry.Quantity(1, "mole / liter"),
            equivalent_mass_grams_per_equivalent=50.0,
        )
