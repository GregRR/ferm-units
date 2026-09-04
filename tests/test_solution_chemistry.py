import math
import sys
from typing import Any

import pytest
from pint import DimensionalityError, UnitRegistry

from fermunits import (
    PHValue,
    amount_concentration_to_equivalent_concentration,
    amount_to_equivalents,
    caco3_basis_mass_concentration_to_equivalent_concentration,
    create_registry,
    equivalent_concentration_to_amount_concentration,
    equivalent_concentration_to_caco3_basis_mass_concentration,
    equivalent_concentration_to_mass_concentration,
    equivalents_to_amount,
    hydrogen_ion_activity_to_ph,
    mass_concentration_to_equivalent_concentration,
    ph_to_hydrogen_ion_activity,
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
@pytest.mark.parametrize(
    ("source_unit", "target_unit"),
    [
        ("mole", "equivalent"),
        ("equivalent", "mole"),
        ("mole / liter", "equivalent / liter"),
        ("equivalent / liter", "mole / liter"),
    ],
)
def test_direct_chemical_equivalence_context_rejects_invalid_factor(
    registry: UnitRegistry[Any],
    equivalence_factor: float,
    source_unit: str,
    target_unit: str,
) -> None:
    quantity = registry.Quantity(1.0, source_unit)

    with pytest.raises(ValueError):
        quantity.to(
            target_unit,
            "chemical_equivalence",
            equivalence_factor=equivalence_factor,
        )


def test_direct_chemical_equivalence_context_accepts_valid_factor(
    registry: UnitRegistry[Any],
) -> None:
    amount = registry.Quantity(1.0, "millimole / liter")

    equivalents = amount.to(
        "milliequivalent / liter",
        "chemical_equivalence",
        equivalence_factor=2.0,
    )
    restored = equivalents.to(
        "millimole / liter",
        "chemical_equivalence",
        equivalence_factor=2.0,
    )

    assert equivalents.magnitude == pytest.approx(2.0)
    assert restored.magnitude == pytest.approx(1.0)


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
@pytest.mark.parametrize(
    ("source_unit", "target_unit"),
    [
        ("milligram / liter", "milliequivalent / liter"),
        ("milliequivalent / liter", "milligram / liter"),
    ],
)
def test_direct_equivalent_mass_context_rejects_invalid_mass(
    registry: UnitRegistry[Any],
    equivalent_mass: float,
    source_unit: str,
    target_unit: str,
) -> None:
    quantity = registry.Quantity(1.0, source_unit)

    with pytest.raises(ValueError):
        quantity.to(
            target_unit,
            "chemical_equivalent_mass",
            equivalent_mass_grams_per_equivalent=equivalent_mass,
        )


def test_direct_equivalent_mass_context_accepts_valid_mass(
    registry: UnitRegistry[Any],
) -> None:
    concentration = registry.Quantity(50.0, "milligram / liter")

    equivalents = concentration.to(
        "milliequivalent / liter",
        "chemical_equivalent_mass",
        equivalent_mass_grams_per_equivalent=50.0,
    )
    restored = equivalents.to(
        "milligram / liter",
        "chemical_equivalent_mass",
        equivalent_mass_grams_per_equivalent=50.0,
    )

    assert equivalents.magnitude == pytest.approx(1.0)
    assert restored.magnitude == pytest.approx(50.0)


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


def test_ph_value_normalizes_numeric_input() -> None:
    ph = PHValue(7)

    assert ph.value == pytest.approx(7.0)
    assert isinstance(ph.value, float)


@pytest.mark.parametrize("value", [math.nan, math.inf, -math.inf])
def test_ph_value_rejects_nonfinite_value(value: float) -> None:
    with pytest.raises(ValueError, match="pH must be finite"):
        PHValue(value)


def test_ph_value_does_not_support_ordinary_arithmetic() -> None:
    ph = PHValue(7.0)

    with pytest.raises(TypeError):
        _ = ph * 2


@pytest.mark.parametrize(
    ("ph", "expected_activity"),
    [
        (-1.0, 10.0),
        (0.0, 1.0),
        (4.0, 1e-4),
        (7.0, 1e-7),
        (14.0, 1e-14),
    ],
)
def test_ph_to_hydrogen_ion_activity(
    ph: float,
    expected_activity: float,
) -> None:
    assert ph_to_hydrogen_ion_activity(PHValue(ph)) == pytest.approx(
        expected_activity, rel=1e-12, abs=0.0
    )


@pytest.mark.parametrize(
    ("activity", "expected_ph"),
    [
        (10.0, -1.0),
        (1.0, 0.0),
        (1e-4, 4.0),
        (1e-7, 7.0),
        (1e-14, 14.0),
    ],
)
def test_hydrogen_ion_activity_to_ph(
    activity: float,
    expected_ph: float,
) -> None:
    result = hydrogen_ion_activity_to_ph(activity)

    assert isinstance(result, PHValue)
    assert result.value == pytest.approx(expected_ph)


def test_ph_activity_conversion_round_trip() -> None:
    original = PHValue(5.37)
    activity = ph_to_hydrogen_ion_activity(original)

    assert hydrogen_ion_activity_to_ph(activity) == original


@pytest.mark.parametrize("ph", [-400.0, 400.0])
def test_ph_to_activity_rejects_unrepresentable_activity(ph: float) -> None:
    with pytest.raises(ValueError, match="representable hydrogen-ion activity"):
        ph_to_hydrogen_ion_activity(PHValue(ph))


@pytest.mark.parametrize(
    "activity",
    [0.0, -1.0, math.nan, math.inf, -math.inf],
)
def test_activity_to_ph_rejects_invalid_activity(activity: float) -> None:
    with pytest.raises(ValueError):
        hydrogen_ion_activity_to_ph(activity)


@pytest.mark.parametrize(
    ("function", "quantity_unit", "parameter"),
    [
        (amount_to_equivalents, "mole", 2.0),
        (equivalents_to_amount, "equivalent", sys.float_info.min),
        (
            amount_concentration_to_equivalent_concentration,
            "mole / liter",
            2.0,
        ),
        (
            equivalent_concentration_to_amount_concentration,
            "equivalent / liter",
            sys.float_info.min,
        ),
        (
            mass_concentration_to_equivalent_concentration,
            "gram / liter",
            sys.float_info.min,
        ),
        (
            equivalent_concentration_to_mass_concentration,
            "equivalent / liter",
            2.0,
        ),
    ],
)
def test_solution_chemistry_context_helpers_reject_nonfinite_results(
    registry: UnitRegistry[Any],
    function: object,
    quantity_unit: str,
    parameter: float,
) -> None:
    quantity = registry.Quantity(sys.float_info.max, quantity_unit)

    with pytest.raises(ValueError, match="representable finite range"):
        function(quantity, parameter)  # type: ignore[operator]


def test_direct_chemical_context_rejects_nonfinite_result(
    registry: UnitRegistry[Any],
) -> None:
    with pytest.raises(ValueError, match="representable finite range"):
        registry.Quantity(sys.float_info.max, "mole").to(
            "equivalent",
            "chemical_equivalence",
            equivalence_factor=2.0,
        )
