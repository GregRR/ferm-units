import pytest

from fermunits import create_registry


def test_registry_factory_returns_independent_registries() -> None:
    first = create_registry()
    second = create_registry()

    assert first is not second

    first_liters = first.Quantity(1, "firkin").to("liter").magnitude
    second_liters = second.Quantity(1, "firkin").to("liter").magnitude

    assert first_liters == pytest.approx(40.91481)
    assert second_liters == pytest.approx(40.91481)
    