# Changelog

All notable changes to FermUnits will be documented in this file.

## 0.1.2 - 2026-08-28

Python compatibility and release-automation maintenance release.

### Changed

- Lower the supported Python floor from 3.14 to 3.11 and test Python 3.11,
  3.12, 3.13, and 3.14 in CI.
- Require Pint `>=0.25.3,<0.26`, retaining the fixes required by FermUnits.
- Align Ruff and mypy compatibility targets with the Python 3.11 support floor.
- Publish GitHub releases to PyPI through Trusted Publishing.

### Notes

- No runtime unit or conversion behavior changed.

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
