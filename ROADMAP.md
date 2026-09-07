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

**Status: complete**

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
- identified the alpha-only `wine_hogshead` compatibility alias as a pre-1.0
  naming risk because legitimate wine meanings vary by region; the later
  stabilization audit removed that alias rather than assigning it a universal
  wine meaning.

No new public API was added solely because a term appeared in the legacy
inventory.

The second M6 migration slice is complete for cider and perry. It records that
sorbitol concentration, phenolic concentration, pH, and press yield are ordinary
physical quantities or existing FermUnits semantics; keeps titratable-acidity
reporting bases and fruit-classification thresholds as method/application context;
and rejects unsupported legacy attenuation and cross-method acidity shortcuts as
universal conversions. No cider/perry-specific public API was added.

The third M6 migration slice is complete for distilling. It separates ordinary
physical quantities from jurisdiction-defined proof scales, proof-gallon and
pure-alcohol accounting semantics, table-driven alcoholometry/gauging, and
application-level dilution or tax policy. Unsupported linear temperature
corrections and universal cask-size claims remain rejected, pending, or
ambiguous. No distilling-specific public API was added.

The fourth M6 migration slice is complete for sake. It records Nihonshudo as a
15 °C, density-derived semantic scale; sake acidity as a prescribed titration
result rather than a multiplicative unit; rice polishing ratio as an ordinary
dimensionless mass fraction; historical Japanese capacity measures as pending
primary metrology verification; and unsupported sweetness/balance shortcuts as
rejected or downstream semantics. No sake-specific public API was added.

The fifth M6 migration slice is complete for biofuels. It records dry feed rate,
volumetric productivity, specific production rate, and yield coefficients as
ordinary compound or dimensionless quantities whose process roles stay in
metadata; keeps commodity-bushel moisture conventions and feedstock composition
downstream; preserves the conventional glucose-to-ethanol stoichiometric yield
as sourced calculation context rather than a unit; and rejects unsupported
fixed corn-yield, starch-factor, and plant-efficiency shortcuts as universal
conversions. No biofuel-specific public API was added.

The sixth M6 migration slice is complete for acid-tier and other fermentation
processes. It records CFU-based microbial counts as method-defined assay results
over ordinary inverse-volume dimensionality; keeps dairy titratable acidity,
solids-not-fat, vinegar acid strength, and kombucha alcohol compliance semantics
explicit; and rejects unsupported cross-acid shortcuts, volatile-acidity legal
claims, and the dimensionally inconsistent legacy Brix-to-acid ratio as universal
conversions. No acid-tier-specific public API was added.

The M6 closeout review found no concrete downstream requirement that justifies
implementing any of the remaining source-ready domain candidates today. Those
candidates stay documented in the maintained references and can be implemented
later when a consumer needs them, without reopening the migration work itself.
This is the intended outcome of the milestone: domain research is maintained and
source-traceable, while the public API remains demand-driven rather than growing
speculatively.

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

**Completion criterion:** met. All six legacy domain inventories have maintained,
source-traceable references; ownership and naming decisions are recorded; and no
new public API was added without a concrete downstream requirement. Future domain
additions remain demand-driven and must follow the naming and ownership rules in
`DESIGN.md`.

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

The first stabilization slice completed the current registry naming and collision
audit. The alpha-only `wine_hogshead` alias was removed because legitimate wine
meanings are region-dependent; Pint's bare `hogshead` remains unchanged, and any
future wine-specific hogshead must use a region-qualified name. The remaining
current FermUnits registry names are either qualified where collision risk exists
or intentionally preserve a documented domain meaning.

The second stabilization slice establishes a finite-result contract for validated
public conversions. Arithmetic on extreme but finite inputs must either produce a
finite scalar/quantity result or raise `ValueError`; it must not silently return
`inf`/`nan` or expose an implementation-level arithmetic overflow. Coverage now
includes brewing scalar conversions, carbonation, gravity/refractometer helpers,
chemical-equivalence contexts, density-assisted composition, and molar-mass
conversions.

The third stabilization slice centralizes the source-verification audit for every
implemented semantic relationship in `docs/verification-status.md`. It separates
API stability from scientific verification, records which implemented behavior is
ready as documented, and identifies the remaining Provisional relationships that
deserve explicit external-review attention before 1.0. Unimplemented M6 research
candidates remain outside this stabilization requirement.

The fourth stabilization slice closes the downstream compatibility audit. Python
3.11 through 3.14 remain the supported runtime matrix, Pint remains constrained to
`>=0.25.3,<0.26`, and the upgrade policy is documented in
`docs/compatibility.md`. `UnitRegistry` and `DimensionalityError` join `Quantity`
as deliberate Pint re-exports required by maintained downstream contracts, so the
Water Chemistry Engine and draft-system contract suites no longer import Pint
directly. The package-level `__all__` inventory is regression-tested to prevent
accidental public-surface drift.

After these focused stabilization slices, the project enters a deep internal
pre-1.0 review. Findings from that review should be resolved before the repository
is handed to an external reviewer. The first internal-review fix batch closes a
finite-result validation hole where mathematically finite integers or quantity
magnitudes outside Python float range could leak raw `OverflowError` before the
documented `ValueError` boundary was reached.

The second internal-review fix batch hardens release automation. The publish
workflow reruns the full Python 3.11-3.14 test matrix and all quality gates
against the exact release tag before release artifacts may be built or published
to PyPI, so publishing cannot rely only on an earlier CI run. GitHub Actions
dependencies used by CI and publishing are pinned to immutable commits.

The third internal-review fix batch reduces direct release-toolchain drift. CI
and publishing use an explicit uv version, the Hatchling build backend is
pinned, and release metadata validation uses an explicit Twine version rather
than resolving a different top-level tool version at release time.
The same packaging pass also reconciles stale third-party and API wording with
the intentional Pint re-export boundary.

The fourth internal-review fix batch closes a remaining finite-result boundary in
context-backed solution-chemistry helpers. Pint performs ordinary target-unit
scaling after a context transformation, so the public helpers now validate the
fully converted return quantity as well as the transformation itself.

The fifth internal-review fix batch hardens distribution integrity. Release builds
ignore any local uv source overrides, inspect wheel and source-distribution
contents for required runtime and license resources, and smoke-test both built
artifacts in isolated environments before they can be attached or published.
Packaging metadata also explicitly declares the MIT license file using the
current standardized license-file field.

The deep external review found no release blocker and identified a focused
pre-1.0 remediation list. The first external-review fix batch addresses the
high-priority public-boundary findings: carbonation can return quantities in an
explicit isolated registry, solution-chemistry wrapper and raw-context validation
share one controlled `ValueError` boundary, the intentional public `Quantity`
re-export is exercised by a maintained downstream contract, shared `ureg`
mutability is documented, and local review working material is ignored.

The second external-review fix batch reconciles documentation/source integrity and
downstream compatibility coverage. Unimplemented regional wine-vessel
candidates remain Provisional under the strict verification threshold; pH
verification is explicitly limited to the mathematical activity definition;
Pint-derived barrel names are described as distinct qualified definitions rather
than canonical aliases; the scalar carbonation pair is retained for 1.x; and the
maintained consumer contracts cover the remaining general equivalence and scalar
carbonation boundaries. Historical 0.1.2 changelog duplication is corrected.

The third external-review fix batch closes the remaining release-engineering
hardening findings. The release event commit is resolved once and passed as an
immutable SHA to every checkout, ordinary CI verifies the lockfile, build jobs
remain read-only while a separate minimal-permission job attaches release
assets, and wheel/source-distribution smoke tests exercise the same packaged
runtime and license resources.

The project-specific pre-release checklist is run only after both internal and
external review findings are closed.

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
