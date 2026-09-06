from importlib.metadata import version

import pytest

import fermunits
from fermunits import (
    Q_,
    DimensionalityError,
    Quantity,
    UnitRegistry,
    create_registry,
    gravity_points_to_sg,
    plato_to_sg,
    plato_to_wort_refractometer_brix,
    sg_to_gravity_points,
    sg_to_plato,
    wort_refractometer_brix_to_plato,
)


def test_public_all_inventory_is_explicit() -> None:
    expected = {
        "Q_",
        "DimensionalityError",
        "PHValue",
        "Quantity",
        "UnitRegistry",
        "absorbance_275nm_to_bitterness_units",
        "amount_concentration_to_equivalent_concentration",
        "amount_concentration_to_mass_concentration",
        "amount_to_equivalents",
        "bitterness_units_to_absorbance_275nm",
        "caco3_basis_mass_concentration_to_equivalent_concentration",
        "co2_grams_per_liter_to_volumes",
        "co2_mass_concentration_to_volumes",
        "co2_volumes_to_grams_per_liter",
        "co2_volumes_to_mass_concentration",
        "create_registry",
        "ebc_to_srm",
        "equivalent_concentration_to_amount_concentration",
        "equivalent_concentration_to_caco3_basis_mass_concentration",
        "equivalent_concentration_to_mass_concentration",
        "equivalents_to_amount",
        "gravity_points_to_sg",
        "hydrogen_ion_activity_to_ph",
        "lintner_to_windisch_kolbach",
        "lovibond_to_srm_approx",
        "mass_concentration_to_amount_concentration",
        "mass_concentration_to_equivalent_concentration",
        "mass_concentration_to_mass_fraction",
        "mass_fraction_to_mass_concentration",
        "ph_to_hydrogen_ion_activity",
        "plato_to_sg",
        "plato_to_wort_refractometer_brix",
        "sg_to_gravity_points",
        "sg_to_plato",
        "srm_to_ebc",
        "srm_to_lovibond_approx",
        "ureg",
        "windisch_kolbach_to_lintner",
        "wort_refractometer_brix_to_plato",
    }

    assert set(fermunits.__all__) == expected


def test_registry_type_and_dimensionality_error_are_public() -> None:
    registry = create_registry()

    assert isinstance(registry, UnitRegistry)
    with pytest.raises(DimensionalityError):
        registry.Quantity(1.0, "gram").to("liter")


def test_quantity_type_is_available_from_public_api() -> None:
    quantity = Q_(1.0, "gram")

    assert isinstance(quantity, Quantity)


def test_registry_factory_returns_independent_registries() -> None:
    first = create_registry()
    second = create_registry()

    assert first is not second

    first_liters = first.Quantity(1, "firkin").to("liter").magnitude
    second_liters = second.Quantity(1, "firkin").to("liter").magnitude

    assert first_liters == pytest.approx(40.91481)
    assert second_liters == pytest.approx(40.91481)


def test_gravity_functions_are_available_from_public_api() -> None:
    assert sg_to_gravity_points(1.050) == pytest.approx(50.0)
    assert gravity_points_to_sg(50.0) == pytest.approx(1.050)
    assert sg_to_plato(1.048) == pytest.approx(11.9120807562)
    assert plato_to_sg(11.9120807562) == pytest.approx(1.048)
    assert wort_refractometer_brix_to_plato(12.48, 1.04) == pytest.approx(12.0)
    assert plato_to_wort_refractometer_brix(12.0, 1.04) == pytest.approx(12.48)


def test_package_version_matches_distribution_metadata() -> None:
    assert fermunits.__version__ == version("ferm-units")


def test_pint_ph_symbol_remains_picohenry() -> None:
    registry = create_registry()
    converted = registry.Quantity(1.0, "pH").to("henry")

    assert converted.magnitude == pytest.approx(1e-12)
