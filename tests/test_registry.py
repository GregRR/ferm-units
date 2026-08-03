from fermunits import create_registry


def test_registry_factory_returns_independent_registries() -> None:
    first = create_registry()
    second = create_registry()

    assert first is not second
    assert first.firkin == second.firkin
