# FermUnits roadmap

FermUnits is an alpha-stage library for fermentation-industry units,
measurement scales, and reusable conversions built on Pint.

The latest published release is **0.1.3**. This roadmap describes development
priorities after that release. It is intentionally milestone-oriented rather
than tied to speculative release numbers or dates.

`DESIGN.md` defines the architectural boundaries of the project. This roadmap
tracks work within those boundaries.

## Current baseline

The current core includes:

- a shared Pint `UnitRegistry`, typed `Q_` constructor, and public `Quantity` type;
- brewing vessel units with qualified names where plain names are ambiguous;
- gravity-point and SG/Plato calculations;
- wort refractometer correction with an explicit caller-supplied correction
  factor;
- beer color, analytical bitterness, diastatic-power, and carbonation
  conversions;
- chemical equivalents and equivalent concentration;
- calcium-carbonate reporting-basis conversion;
- density-assisted concentration and mass-fraction conversion;
- molar-mass-assisted mass/amount concentration conversion;
- downstream unit-contract coverage for Water Chemistry Engine;
- maintained source-status documentation and an explicit scientific
  verification policy.

Some implemented brewing relationships remain provisional pending stronger
primary-source verification. Implementation status and scientific verification
status are tracked separately.

## Milestone 1 — Draft-system compatibility

**Status: complete in current development**

Make FermUnits a reliable unit boundary for the Draft System Engine without
moving draft-system engineering models into this library.

Implemented work:

- add a draft-system unit-contract test suite covering:
  - absolute temperature and temperature differences;
  - pressure;
  - tubing length and inside diameter;
  - volumetric flow;
  - density and dynamic viscosity;
  - pressure gradient / line restriction;
  - CO2 mass concentration;
  - dimensional-incompatibility failures;
  - explicit US-liquid-unit behavior where US and Imperial measures could be
    confused;
- add quantity-aware carbonation conversion APIs while retaining the existing
  scalar APIs for compatibility;
- document the downstream boundary for gauge versus absolute pressure,
  pressure-gradient representation, and carbonation quantities.

The following remain downstream concerns and are not FermUnits features:

- `psig`/`psia` as artificial units — gauge versus absolute is a pressure
  reference semantic;
- tubing/manufacturer restriction coefficients;
- component-loss tables;
- carbonation-equilibrium pressure models;
- mixed-gas calculations;
- complete draft-system balancing or solver logic.

**Completion criterion:** the Draft System Engine can use FermUnits/Pint for all
v1 quantity parsing, conversion, and dimensional validation without relying on
implicit unit conventions or naked dimensional values at the carbonation
boundary.

## Milestone 2 — Carbonation source verification

**Status: complete for the current development cycle; direct ASBC method-text verification remains pending**

Carbonation is already implemented provisionally and is an important dependency
for draft-system work. Strengthen its source record before treating the
relationship as verified.

Investigate and document:

- the formal definition of one volume of CO2;
- reference temperature and pressure;
- the authoritative ASBC method or table identity and scope;
- any density assumptions or distinctions between physical concentration and
  beverage-industry reporting practice;
- appropriate valid range and reporting precision, if method-defined.

**Completion criterion:** met for the accessible-source review. The current
relationship remains Provisional because authoritative method-text verification
has not yet established the normative reference state and reporting precision.
The unresolved direct ASBC checks remain tracked in `docs/asbc-verification.md`.

## Milestone 3 — Brewing verification backlog

**Status: complete in current development**

Continue converting implemented-but-provisional brewing relationships into
well-sourced, explicitly scoped behavior.

Priority topics include:

- SG and gravity-point conventions;
- SG-to-Plato polynomial provenance, valid range, and reference conditions;
- Plato-to-SG inversion rationale and accuracy;
- Brix, Plato, and Balling distinctions;
- wort refractometer correction provenance and scope;
- hydrometer temperature correction, which remains unimplemented until a
  defensible method is available;
- SRM/EBC method qualification;
- Lovibond approximation provenance and limitations;
- analytical bitterness method semantics;
- Lintner/Windisch-Kolbach conversion;
- remaining brewing vessel definitions and regional meanings.

The goal is not merely more formulas. It is to make the scientific status and
scope of existing functionality increasingly precise.

Completed verification batches in current development:

- gravity/extract measurement semantics and source-status review;
- SRM/EBC, Lovibond, and analytical bitterness source/status review;
- Lintner/Windisch-Kolbach and British brewery-vessel source/status review,
  including the qualified historical `brewing_tun` definition.

All planned implementation/source-verification batches, the whole-M3 internal
review, and the two-pass external scientific/code review are complete. The
resulting corrections clarify unfermented-wort refractometer scope, carbonation
source limitations, Pint vessel aliases/collisions, cask source status, and
method-extract bitterness naming before Milestone 4 begins.

**Completion criterion:** every implemented brewing relationship has a current
maintained source record and an intentional Verified, Provisional, Ambiguous, or
Rejected status, with Pending used for identified but not responsibly
implementable work.

## Milestone 4 — Solution-chemistry semantic boundaries

**Status: complete in current development**

Revisit semantic quantities that go beyond ordinary Pint dimensionality, using
Water Chemistry Engine and FermentationJSON requirements to decide what belongs in
FermUnits versus downstream domain models or serialization schemas.

Audit conclusions for the first M4 pass:

- volume fraction remains an ordinary dimension-one Pint quantity; fraction
  kind and reference conditions remain downstream semantics rather than new
  registry units;
- pH belongs in FermUnits as a small non-Pint `PHValue` semantic type plus
  explicit activity-based transformations, never as a multiplicative Pint unit
  or universal concentration conversion;
- electrical conductivity remains an ordinary Pint conductance-per-length
  quantity (for example `microsiemens / centimeter`); reference-temperature,
  compensation, calibration, and reporting semantics remain downstream;
- a pH difference is logarithmic and does not require a new Pint unit or
  FermUnits type at present;
- reported bounds, ranges, nondetects, detection/quantitation limits, and
  uncertainty belong to downstream measurement/serialization models, while
  their numeric thresholds remain ordinary Pint quantities;
- FermUnits does not resolve bounded or uncertain measurements to scalar values
  and does not add a general uncertainty-propagation framework.

Do not duplicate FermentationJSON's reporting/provenance model or embed
water-treatment calculation policy in FermUnits merely for convenience.

External review identified one preflight defect in the existing solution-chemistry
foundation: direct use of FermUnits' registered Pint equivalence contexts could
bypass wrapper-level validation for nonpositive or nonfinite conversion factors.
The preflight fix now enforces those invariants inside the context transformation
layer as well, retains wrapper validation as defense in depth, and adds direct-context
regression coverage in both directions before any new Milestone 4 contexts are added.

The closeout pass adds downstream contract coverage for the `PHValue`/hydrogen-ion
activity boundary and for electrical conductivity as an ordinary Pint quantity.
No additional semantic wrapper, conductivity unit alias, or water-treatment policy
is required in FermUnits.

**Completion criterion:** met. Ownership of each audited semantic concern is
documented, and only the reusable unit/conversion behavior that clearly belongs
in FermUnits is implemented.

## Milestone 5 — Python compatibility and adoption

**Status: complete in 0.1.2**

FermUnits 0.1.2 established Python 3.11 as the deliberate minimum supported
version and added continuous coverage through Python 3.14.

Completed work:

- lower `requires-python` from `>=3.14` to `>=3.11`;
- continuously test Python 3.11, 3.12, 3.13, and 3.14 in CI;
- align Ruff and mypy compatibility targets with Python 3.11;
- require Pint `>=0.25.3,<0.26`, whose supported Python floor is also 3.11;
- verify the published 0.1.2 artifact installs and imports under Python 3.11.

Upstream Pint's current **unreleased** 0.26 change log says Python 3.11 support is
planned to be dropped in favor of Python 3.14. [SH-PINT-CHANGES-01] FermUnits
therefore keeps the existing `<0.26` ceiling and will re-evaluate the actual
released Pint 0.26 metadata rather than changing policy based on an unreleased
plan.

**Completion criterion:** met. The minimum supported Python version is
deliberate, CI-enforced, and no higher than necessary for the current
implementation and supported Pint line.

## Milestone 6 — Additional fermentation domains

**Status: in progress; wine and cider/perry reference migrations complete**

Migrate legacy research into maintained domain references and add functionality
when there is a concrete downstream need and adequate sourcing.

The first M6 migration slice is complete for wine. The legacy wine inventory has
been triaged into maintained ownership classes that distinguish ordinary Pint
quantities, existing FermUnits semantic behavior, source-ready regional physical
units, downstream analytical/reporting semantics, and candidates that remain
pending, ambiguous, or rejected. The migration also:

- records authoritative OIV analytical-method/reporting bases without promoting
  method-specific relationships into universal unit conversions;
- identifies source-ready regional vessel and Champagne-package capacities while
  leaving them unimplemented until a real consumer needs the named unit;
- rejects legacy shortcut formulas as universal conversions where method scope,
  reference conditions, or process assumptions are not adequately defined;
- flags the existing `wine_hogshead` compatibility alias for pre-1.0 naming
  review because legitimate wine meanings vary by region.

No new public API was added solely because a term appeared in the legacy
inventory.

The second M6 migration slice is complete for cider and perry. It records that
sorbitol concentration, phenolic concentration, pH, and press yield are ordinary
physical quantities or existing FermUnits semantics; keeps titratable-acidity
reporting bases and fruit-classification thresholds as method/application context;
and rejects unsupported legacy attenuation and cross-method acidity shortcuts as
universal conversions. No cider/perry-specific public API was added.

Candidate domains include:

- wine;
- cider and perry;
- distilling;
- sake;
- biofuels;
- other fermentation and acid-tier processes.

Legacy inventories under `docs/reference/legacy/` are research inputs, not a
feature checklist. A term appearing there does not imply that FermUnits should
implement it.

**Completion criterion:** additions are demand-driven, source-traceable, and
consistent with the naming and ownership rules in `DESIGN.md`.

## Pre-1.0 stabilization

Before a 1.0 release, review the project as a whole for:

- public API consistency and naming stability;
- registry aliases and collision behavior;
- source-verification status of implemented relationships;
- downstream contract coverage;
- supported Python/Pint compatibility policy;
- documentation completeness and internal consistency;
- deprecation policy for any alpha-era APIs that need adjustment;
- extreme finite-input handling, so arithmetic overflow cannot silently produce
  nonfinite outputs where a public conversion promises validated numeric behavior.

A 1.0 release should indicate that the supported public API and documented
semantics are intentionally stable, not that every conceivable fermentation
domain has been implemented.

## Roadmap principles

- Prefer concrete downstream requirements over speculative unit accumulation.
- Preserve Pint behavior when it already represents the correct physical unit.
- Qualify ambiguous domain terms instead of silently redefining legitimate
  existing names.
- Keep empirical and analytical scales explicit rather than pretending they are
  universal multiplicative units.
- Keep implementation status separate from source-verification status.
- Do not block unrelated development merely because one research item awaits
  access to an authoritative source.
- Revisit this roadmap when downstream projects expose new reusable unit or
  conversion requirements.
