# Changelog

All notable changes to FermUnits will be documented in this file.

## 0.1.0 - 2026-08-06

Initial pre-alpha distributable release.

### Added

- Pint-based FermUnits registry and `Q_` quantity constructor.
- Fermentation-specific vessel definitions with qualified names where Pint
  names are ambiguous or represent a different legitimate meaning.
- Brewing gravity, color, bitterness, diastatic-power, carbonation, and
  refractometer calculations.
- Chemical-equivalent units and explicit mole/equivalent conversions.
- Equivalent-concentration conversions using explicit equivalent mass.
- Conventional calcium-carbonate reporting conversion for water analysis.
- Density-assisted mass-concentration/mass-fraction conversions.
- Molar-mass-assisted mass-concentration/amount-concentration conversions.
- Water-treatment downstream unit-contract tests.
- Source-verification policy and domain reference documentation.

### Notes

- FermUnits remains pre-alpha.
- Relationships that still require authoritative ASBC or EBC verification are
  documented as provisional rather than presented as stable universal
  definitions.
