"""Audit proposed FermUnits names against Pint and FermUnits registries."""

from dataclasses import dataclass
from typing import Any

from pint import UnitRegistry
from pint.errors import DimensionalityError, UndefinedUnitError

from fermunits import create_registry

CANDIDATE_UNITS: dict[str, list[str]] = {
    "brewing": [
        "barrel",
        "beer_barrel",
        "us_beer_barrel",
        "imperial_beer_barrel",
        "imperial_barrel",
        "imperial_gallon",
        "UK_gallon",
        "hectoliter",
        "firkin",
        "kilderkin",
        "pin",
        "pin_cask",
        "hogshead",
        "wine_hogshead",
        "brewing_hogshead",
        "puncheon",
        "brewing_puncheon",
        "butt",
        "brewing_butt",
        "tun",
        "brewing_tun",
        "gravity_point",
        "degree_plato",
        "degree_brix",
        "degree_balling",
        "degree_lovibond",
        "SRM",
        "EBC",
        "IBU",
        "EBU",
        "degree_lintner",
        "windisch_kolbach",
        "volume_CO2",
    ],
    "wine": [
        "degree_baume",
        "degree_oechsle",
        "KMW",
        "wine_case",
        "nine_liter_case",
        "barrique",
        "piece",
        "wine_hogshead",
        "wine_puncheon",
        "demi_muid",
        "foudre",
        "stuck",
        "port_pipe",
        "sherry_butt",
        "tun",
        "piccolo",
        "demi_bottle",
        "standard_wine_bottle",
        "magnum",
        "jeroboam",
        "rehoboam",
        "methuselah",
        "salmanazar",
        "balthazar",
        "nebuchadnezzar",
        "melchior",
        "solomon",
        "sovereign",
        "primat",
        "goliath",
        "melchizedek",
        "midas",
    ],
    "distilling": [
        "ABV",
        "ABW",
        "US_proof",
        "UK_proof",
        "degree_Gay_Lussac",
        "proof_gallon",
        "liter_pure_alcohol",
        "litre_absolute_alcohol",
        "wine_gallon",
        "bulk_gallon",
        "bourbon_barrel",
        "whisky_hogshead",
        "quarter_cask",
        "octave_cask",
        "gorda",
    ],
    "sake": [
        "nihonshudo",
        "sake_meter_value",
        "sando",
        "amando",
        "seimaibuai",
        "koku",
        "to",
        "sho",
        "gou",
        "isshobin",
    ],
    "cider_and_perry": [
        "liter_per_metric_tonne",
        "gallon_per_short_ton",
        "tannin_percent",
    ],
    "biofuels": [
        "dry_metric_ton",
        "dry_metric_ton_per_hour",
        "bushel_corn",
        "gram_per_liter_hour",
        "gram_per_gram_hour",
    ],
    "other_fermentation": [
        "CFU",
        "CFU_per_milliliter",
        "percent_lactic_acid",
        "percent_snf",
    ],
    "solution_chemistry": [
        "mole",
        "millimole",
        "micromole",
        "molar",
        "molal",
        "equivalent",
        "milliequivalent",
        "normal",
        "normality",
        "percent",
        "ppm",
        "ppb",
        "ppm_mass",
        "ppb_mass",
        "gram_per_mole",
        "mole_per_liter",
        "millimole_per_liter",
        "equivalent_per_liter",
        "milliequivalent_per_liter",
    ],
}


COMPOUND_EXPRESSIONS: list[str] = [
    "mole / liter",
    "millimole / liter",
    "micromole / liter",
    "mole / kilogram",
    "millimole / kilogram",
    "equivalent / liter",
    "milliequivalent / liter",
    "milliequivalent / kilogram",
    "gram / mole",
    "kilogram / mole",
    "gram / 100 milliliter",
    "liter / kilogram",
    "milliliter / gram",
    "US_liquid_quart / pound",
    "US_liquid_gallon / pound",
    "milliliter / kilogram",
    "gram / kilogram",
    "milliliter / US_liquid_gallon",
    "gram / US_liquid_gallon",
    "gram / hectoliter",
    "pound / us_beer_barrel",
    "ounce / us_beer_barrel",
]


@dataclass(frozen=True)
class ConversionCheck:
    """A representative conversion to test against both registries."""

    source: str
    target: str


CONVERSION_CHECKS: list[ConversionCheck] = [
    ConversionCheck("1 mole / liter", "millimole / liter"),
    ConversionCheck("1 gram / mole", "kilogram / mole"),
    ConversionCheck("1 liter / kilogram", "milliliter / gram"),
    ConversionCheck("1 US_liquid_quart / pound", "liter / kilogram"),
    ConversionCheck("1 milliliter / US_liquid_gallon", "milliliter / liter"),
    ConversionCheck("1 gram / US_liquid_gallon", "milligram / liter"),
    ConversionCheck("1 pound / us_beer_barrel", "gram / hectoliter"),
]


def unit_status(registry: UnitRegistry[Any], name: str) -> str:
    """Return whether a unit name exists and what it resolves to."""
    try:
        unit = registry.Unit(name)
    except UndefinedUnitError:
        return "NOT FOUND"

    return f"FOUND -> {unit}"


def dimensionality_status(registry: UnitRegistry[Any], expression: str) -> str:
    """Return parsing and dimensionality information for a unit expression."""
    try:
        unit = registry.Unit(expression)
    except UndefinedUnitError:
        return "NOT FOUND"

    return f"FOUND -> {unit}; DIMENSIONALITY: {unit.dimensionality}"


def conversion_status(
    registry: UnitRegistry[Any],
    source: str,
    target: str,
) -> str:
    """Return the result of a representative conversion."""
    try:
        quantity = registry.Quantity(source)
        converted = quantity.to(target)
    except UndefinedUnitError as exc:
        return f"NOT FOUND ({exc})"
    except DimensionalityError as exc:
        return f"INCOMPATIBLE ({exc})"
    except ValueError as exc:
        return f"INVALID ({exc})"

    return f"{quantity} -> {converted}"


def print_candidate_audit(
    pint_registry: UnitRegistry[Any],
    ferm_registry: UnitRegistry[Any],
) -> None:
    """Print named-unit lookup results."""
    for category, names in CANDIDATE_UNITS.items():
        print(f"\n[{category.upper()}]")

        for name in names:
            pint_result = unit_status(pint_registry, name)
            ferm_result = unit_status(ferm_registry, name)

            print(f"{name:<32} PINT: {pint_result:<38} FERMUNITS: {ferm_result}")


def print_compound_expression_audit(
    pint_registry: UnitRegistry[Any],
    ferm_registry: UnitRegistry[Any],
) -> None:
    """Print parsing and dimensionality results for compound expressions."""
    print("\n[SOLUTION_CHEMISTRY_COMPOUND_EXPRESSIONS]")

    for expression in COMPOUND_EXPRESSIONS:
        print(f"\n{expression}")
        print(f"  PINT:      {dimensionality_status(pint_registry, expression)}")
        print(f"  FERMUNITS: {dimensionality_status(ferm_registry, expression)}")


def print_conversion_audit(
    pint_registry: UnitRegistry[Any],
    ferm_registry: UnitRegistry[Any],
) -> None:
    """Print representative conversion results."""
    print("\n[REPRESENTATIVE_CONVERSIONS]")

    for check in CONVERSION_CHECKS:
        print(f"\n{check.source} -> {check.target}")
        print(
            "  PINT:      "
            f"{conversion_status(pint_registry, check.source, check.target)}"
        )
        print(
            "  FERMUNITS: "
            f"{conversion_status(ferm_registry, check.source, check.target)}"
        )


def main() -> None:
    """Run all Pint and FermUnits registry audits."""
    pint_registry: UnitRegistry[Any] = UnitRegistry()
    ferm_registry: UnitRegistry[Any] = create_registry()

    print_candidate_audit(pint_registry, ferm_registry)
    print_compound_expression_audit(pint_registry, ferm_registry)
    print_conversion_audit(pint_registry, ferm_registry)


if __name__ == "__main__":
    main()
