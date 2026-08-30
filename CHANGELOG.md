# Changelog

All notable changes to FermUnits will be documented in this file.

## Unreleased

### Added

- Add quantity-aware dissolved-CO2 conversions between volumes of CO2 and Pint
  mass-concentration quantities while retaining the original scalar g/L APIs.
- Add a downstream draft-system unit contract covering temperature, pressure,
  length, volumetric flow, density, viscosity, pressure gradient, explicit US
  liquid measures, and the quantity-aware carbonation boundary.

### Changed

- Begin the Milestone 3 gravity/extract verification pass by sourcing the
  gravity-points convention, locating peer-reviewed reproduction and ASBC
  attribution for the SG-to-Plato polynomial, clarifying the Plato/Brix
  semantic boundary, and retaining explicit conservative
  refractometer/hydrometer behavior.
- Reclassify the project from pre-alpha to alpha in package metadata and the
  README.
- Clarify that the latest release is 0.1.2 and that provisional scientific
  relationships remain explicitly source-tracked despite the project maturity
  change.
- Reconcile the README, project metadata, design documentation, source policy,
  and maintained reference indexes.
- Replace stale domain inventories with maintained current-status documents and
  retain the original planning inventories under an explicitly non-normative
  legacy area.
- Align the development Makefile with the locked test, lint, format, type-check,
  and diff verification gate used for releases.
- Add a milestone-oriented project roadmap covering downstream compatibility,
  source verification, semantic boundaries, Python support, and future domain
  expansion.
- Complete the accessible-source carbonation verification pass, distinguish
  ASBC Beer-13 dissolved-CO2 analysis from Fills-1 packaging/net-content
  calculations, document the `506.07 mL/g` source trail and standard-state
  physical support, and retain the conversion as Provisional pending direct
  ASBC method-text verification of reference state and reporting precision.

### Fixed

- Derive `fermunits.__version__` from installed distribution metadata so it
  cannot drift from the packaged project version.
- Correct the gravity/extract source record so an inaccessible 1984 JASBC item
  is retained only as a verification lead rather than cited as proven
  provenance for the SG-to-Plato coefficients.

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
