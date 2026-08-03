"""Check whether candidate FermUnits names already exist in Pint."""

from pint import UnitRegistry
from pint.errors import UndefinedUnitError


CANDIDATE_UNITS = [
    "beer_barrel",
    "US_beer_barrel",
    "imperial_beer_barrel",
    "imperial_gallon",
    "UK_gallon",
    "firkin",
    "kilderkin",
    "pin",
    "pin_cask",
    "hogshead",
    "puncheon",
    "butt",
]


def main() -> None:
    registry = UnitRegistry()

    for name in CANDIDATE_UNITS:
        try:
            unit = registry.Unit(name)
            print(f"{name:<24} FOUND     -> {unit}")
        except UndefinedUnitError:
            print(f"{name:<24} NOT FOUND")


if __name__ == "__main__":
    main()
