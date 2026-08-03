import pytest

from fermunits import Q_


def test_firkin_exact_liter_definition() -> None:
    assert Q_(1, "firkin").to("liter").magnitude == pytest.approx(40.91481)


def test_kilderkin_is_two_firkins() -> None:
    assert Q_(1, "kilderkin").to("firkin").magnitude == pytest.approx(2)


def test_imperial_beer_barrel_is_four_firkins() -> None:
    result = Q_(1, "imperial_beer_barrel").to("firkin")
    assert result.magnitude == pytest.approx(4)


def test_pin_cask_is_half_firkin() -> None:
    assert Q_(1, "pin_cask").to("firkin").magnitude == pytest.approx(0.5)


def test_pint_beer_barrel_exact_liter_definition() -> None:
    result = Q_(1, "beer_barrel").to("liter")
    assert result.magnitude == pytest.approx(117.347765304)


def test_brewing_puncheon_equals_72_imperial_gallons() -> None:
    result = Q_(1, "brewing_puncheon").to("imperial_gallon")
    assert result.magnitude == pytest.approx(72)


def test_brewing_butt_equals_108_imperial_gallons() -> None:
    result = Q_(1, "brewing_butt").to("imperial_gallon")
    assert result.magnitude == pytest.approx(108)

def test_wine_hogshead_matches_pint_hogshead() -> None:
    result = Q_(1, "wine_hogshead").to("hogshead")
    assert result.magnitude == pytest.approx(1)


def test_brewing_hogshead_equals_54_imperial_gallons() -> None:
    result = Q_(1, "brewing_hogshead").to("imperial_gallon")
    assert result.magnitude == pytest.approx(54)
