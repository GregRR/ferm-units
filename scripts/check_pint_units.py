"""Audit proposed FermUnits names against Pint and FermUnits registries."""

from typing import Any

from pint import UnitRegistry
from pint.errors import UndefinedUnitError

from fermunits import create_registry

CANDIDATE_UNITS: dict[str, list[str]] = {
    "brewing": [
        "beer_barrel",
        "us_beer_barrel",
        "imperial_beer_barrel",
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
}


def unit_status(registry: UnitRegistry[Any], name: str) -> str:
    """Return whether a unit name exists and what it resolves to."""
    try:
        unit = registry.Unit(name)
        return f"FOUND -> {unit}"
    except UndefinedUnitError:
        return "NOT FOUND"


def main() -> None:
    pint_registry: UnitRegistry[Any] = UnitRegistry()
    ferm_registry: UnitRegistry[Any] = create_registry()

    for category, names in CANDIDATE_UNITS.items():
        print(f"\n[{category.upper()}]")

        for name in names:
            pint_result = unit_status(pint_registry, name)
            ferm_result = unit_status(ferm_registry, name)

            print(
                f"{name:<28} "
                f"PINT: {pint_result:<28} "
                f"FERMUNITS: {ferm_result}"
            )


if __name__ == "__main__":
    main()
