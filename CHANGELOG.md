# Changelog

All notable changes to FermUnits will be documented in this file.

## Unreleased

### Removed

- Remove the alpha-only `wine_hogshead` registry alias after the pre-1.0 naming
  audit confirmed that legitimate wine-industry hogshead capacities vary by
  region. Pint's bare `hogshead` remains available unchanged; future wine-specific
  names must be region-qualified.

### Changed

- Close Milestone 6 after migrating and triaging all six legacy domain
  inventories into maintained, source-traceable references. The review found no
  current downstream requirement that justifies adding speculative wine,
  cider/perry, distilling, sake, biofuel, or acid-tier APIs; source-ready
  candidates remain documented for demand-driven future work.
- Complete the sixth Milestone 6 domain migration by triaging the legacy
  acid-tier and other-fermentation inventory into method-defined microbial
  counts and titratable-acidity results, ordinary concentration/fraction
  quantities, downstream food/regulatory semantics, and explicit rejected
  cross-method or dimensionally inconsistent shortcuts without adding
  speculative public API.
- Complete the fifth Milestone 6 domain migration by triaging the legacy biofuel
  inventory into ordinary process-rate quantities, dry-basis and commodity
  metadata, source-supported stoichiometric yield context, and explicit
  rejected/downstream feedstock and plant-efficiency shortcuts without adding
  speculative public API.
- Complete the fourth Milestone 6 domain migration by triaging the legacy sake
  inventory into the source-ready Nihonshudo scale, prescribed acidity method,
  ordinary rice-polishing ratio, pending historical capacity measures, and
  explicit rejected/downstream sensory shortcuts without adding speculative
  public API.
- Complete the third Milestone 6 domain migration by triaging the legacy
  distilling inventory into ordinary physical quantities, jurisdiction-defined
  proof/accounting semantics, authoritative alcoholometry/gauging methods, and
  explicit pending/rejected historical or vessel shortcuts without adding
  speculative public API.
- Complete the second Milestone 6 domain migration by triaging the legacy cider
  and perry inventory into ordinary Pint quantities, existing FermUnits semantic
  behavior, method-defined reporting bases, downstream classification logic, and
  explicit pending/rejected formulas without adding speculative public API.
- Complete the first Milestone 6 domain migration by triaging the legacy wine
  inventory into maintained ownership classes, authoritative source records,
  source-ready regional candidates, and explicit pending/rejected items without
  adding speculative public API.
- Complete the Milestone 4 solution-chemistry semantic-boundary audit by
  documenting electrical conductivity as an ordinary Pint physical quantity,
  keeping reference-temperature and compensation semantics downstream, and
  recording the pH/measurement ownership decisions as complete.
- Extend the Water Chemistry Engine compatibility contract with pH/activity and
  electrical-conductivity coverage without moving application chemistry policy
  into FermUnits.

## 0.1.3 - 2026-08-31

Brewing verification, chemistry hardening, and downstream API release.

### Added

- Export `Quantity` from the package-level FermUnits API so downstream
  applications can use `from fermunits import Q_, Quantity` without importing
  Pint directly.

- Add a small non-Pint `PHValue` semantic type and explicit
  pH-to-hydrogen-ion-activity conversion helpers while preserving the
  distinction between thermodynamic activity and concentration and leaving
  Pint's existing `pH` picohenry spelling untouched.
- Add the qualified `brewing_tun` historical British brewery measure as
  216 Imperial gallons, completing the implemented large-cask hierarchy without
  assigning a universal bare `tun` meaning.
- Add quantity-aware dissolved-CO2 conversions between volumes of CO2 and Pint
  mass-concentration quantities while retaining the original scalar g/L APIs.
- Add a downstream draft-system unit contract covering temperature, pressure,
  length, volumetric flow, density, viscosity, pressure gradient, explicit US
  liquid measures, and the quantity-aware carbonation boundary.

### Changed

- Define the Milestone 4 ownership boundary for volume fraction, pH
  differences, reported bounds/ranges, detection and quantitation limits, and
  measurement uncertainty without adding downstream reporting policy to
  FermUnits.
- Incorporate the two-pass external Milestone 3 review by restricting the simple
  wort correction-factor documentation to unfermented wort, clarifying the
  provisional standalone interpretation of Torrent's `506.07 mL/g` carbonation
  constant, downgrading British cask terminology to Provisional where source
  strength does not meet the project-wide Verified bar, and making
  `imperial_beer_barrel` an explicit alias of Pint's `imperial_barrel`.
- Rename the analytical-bitterness input parameter to
  `extract_absorbance_275nm` so keyword use carries the method-extract semantic
  boundary already required by the function documentation.
- Make `docs/sources.md` the master project source ledger and add the maintained
  brewing and solution-chemistry source records, including the external-review
  wort-correction corroboration and upstream Pint compatibility planning source.
- Complete the whole-Milestone-3 internal review by aligning source-status
  vocabulary, expressing the carbonation factor directly from the sourced
  `506.07 mL/g` constant, strengthening bitterness-factor provenance, and
  adding inverse-boundary and vessel-collision regression coverage.
- Complete the planned Milestone 3 verification batches by confirming current
  ASBC/EBC diastatic-power method identities, strengthening the conventional
  Lintner/Windisch-Kolbach source record and low-end limitations, and sourcing
  British brewery cask meanings while keeping larger historical names explicitly
  qualified.
- Continue the Milestone 3 brewing verification pass by confirming current
  ASBC/EBC color and bitterness method identities, strengthening the SRM/EBC
  scale-factor and Beer-23A bitterness-factor source records, clarifying that
  bitterness helpers consume method-derived extract absorbance, and retaining
  the Lovibond relationship as an explicitly provisional approximation.
- Begin the Milestone 3 gravity/extract verification pass by sourcing the
  gravity-points convention, locating peer-reviewed reproduction and ASBC
  attribution for the SG-to-Plato polynomial, clarifying the Plato/Brix
  semantic boundary, and retaining explicit conservative
  refractometer/hydrometer behavior.
- Reclassify the project from pre-alpha to alpha in package metadata and the
  README.
- Clarify that the latest release is 0.1.3 and that provisional scientific
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

- Enforce finite, positive equivalence factors and equivalent masses inside
  the registered Pint context transformations so direct context use cannot
  bypass the validation already performed by the public solution-chemistry
  wrappers.
- Extend Pint collision regression coverage to the built-in `imperial_barrel`
  alias relationship and Pint's bare `pin`/picoinch behavior, and expand the
  collision-audit candidate set so those names are checked explicitly.
- Derive `fermunits.__version__` from installed distribution metadata so it
  cannot drift from the packaged project version.
- Correct the gravity/extract source record so an inaccessible 1984 JASBC item
  is retained only as a verification lead rather than cited as proven
  provenance for the SG-to-Plato coefficients.

## 0.1.2 - 2026-08-28

Python compatibility and release-automation maintenance release.

### Changed

- Incorporate the two-pass external Milestone 3 review by restricting the simple
  wort correction-factor documentation to unfermented wort, clarifying the
  provisional standalone interpretation of Torrent's `506.07 mL/g` carbonation
  constant, downgrading British cask terminology to Provisional where source
  strength does not meet the project-wide Verified bar, and making
  `imperial_beer_barrel` an explicit alias of Pint's `imperial_barrel`.
- Rename the analytical-bitterness input parameter to
  `extract_absorbance_275nm` so keyword use carries the method-extract semantic
  boundary already required by the function documentation.
- Make `docs/sources.md` the master project source ledger and add the maintained
  brewing and solution-chemistry source records, including the external-review
  wort-correction corroboration and upstream Pint compatibility planning source.
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

- Extend Pint collision regression coverage to the built-in `imperial_barrel`
  alias relationship and Pint's bare `pin`/picoinch behavior, and expand the
  collision-audit candidate set so those names are checked explicitly.
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
