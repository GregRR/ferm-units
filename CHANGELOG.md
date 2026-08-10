# Changelog

All notable changes to FermUnits will be documented in this file.

## Unreleased

### Changed

- Reclassify the project from pre-alpha to alpha in package metadata and the
  README.
- Clarify that the current release is 0.1.1 and that provisional scientific
  relationships remain explicitly source-tracked despite the project maturity
  change.

## 0.1.1 - 2026-08-09

Typing-only maintenance release.

### Fixed

- Preserve Pint's inferred quantity magnitude type through the public `Q_`
  constructor instead of exposing constructed quantities as `Quantity[Any]`.
- Add static regression coverage for `float`, `int`, `Decimal`, and `Fraction`
  quantity magnitudes constructed through `from fermunits import Q_`.

### Notes

- No runtime unit or conversion behavior changed.
- Pint remains constrained to the existing supported `>=0.25,<0.26` range.

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
