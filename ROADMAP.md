# FermUnits roadmap

FermUnits is a stable Pint-based library for fermentation-industry units,
measurement scales, and reusable conversions.

The latest published release is **1.0.0**. There is currently **no committed
post-1.0 feature milestone or release feature set**. New functionality is added
when a concrete downstream requirement exposes reusable behavior that belongs in
FermUnits and can be supported with adequate scientific or standards sourcing.

`DESIGN.md` defines the architectural boundaries of the project.
`docs/verification-status.md` tracks the scientific verification status of
implemented relationships, and `CHANGELOG.md` records detailed release history.

## Current development priorities

### Downstream-driven reusable behavior

FermUnits should continue to grow from concrete consumer requirements rather
than speculative unit accumulation.

Current expectations are:

- maintain the public unit and conversion boundary used by Water Chemistry
  Engine and the Draft System Engine;
- add a new unit, semantic type, or conversion only when the behavior is reusable
  beyond one application and clearly belongs in FermUnits;
- keep application policy, equipment models, reporting/provenance models, and
  process-specific calculations downstream;
- preserve Pint behavior when Pint already represents the correct physical unit;
- use explicit qualified names when a domain term has more than one legitimate
  meaning.

A future numbered milestone should be created only when a concrete body of work
is large and coherent enough to justify one. No Milestone 7 is currently pegged.

### Scientific verification

Source verification remains active maintenance even when it does not require a
new public API.

Known follow-up work includes:

- direct authoritative ASBC method-text verification for the implemented
  carbonation relationship, especially its normative reference state and
  reporting precision; unresolved checks remain tracked in
  `docs/asbc-verification.md`;
- hydrometer temperature correction, which remains intentionally unimplemented
  until a defensible authoritative method and scope are available;
- strengthening relationships that remain Provisional in
  `docs/verification-status.md` when better primary evidence becomes available.

An unresolved research item does not block unrelated development.

### Compatibility and maintenance

The current compatibility baseline is Python 3.11 through 3.14 and Pint
`>=0.25.3,<0.26`.

Ongoing maintenance includes:

- preserving the documented 1.x public API and semantics;
- maintaining downstream contract coverage and release-quality gates;
- evaluating future Pint versions deliberately rather than widening the
  supported range automatically;
- revisiting the supported Python matrix when upstream dependencies or concrete
  downstream requirements justify a change.

## Candidate backlog — not scheduled

The maintained domain references contain source-ready or partially researched
candidates that may become useful later. They are **not committed features** and
do not imply a target release.

Candidate areas include:

- regional wine vessel and package units;
- cider and perry;
- distilling;
- sake;
- biofuels;
- other fermentation and acid-tier processes.

Legacy inventories under `docs/reference/legacy/` are research inputs, not a
feature checklist. A term appearing there does not imply that FermUnits should
implement it.

A candidate should become implementation work only when:

1. a concrete downstream consumer needs it;
2. ownership clearly belongs in FermUnits rather than the application or a
   serialization/reporting model;
3. naming is sufficiently unambiguous for a stable public API;
4. the definition or relationship has adequate sourcing and explicit scientific
   status; and
5. the behavior can be covered by tests and public documentation.

## Completed milestones and 1.0 history

The pre-1.0 milestones are complete. They are retained here as a concise record
of how the 1.0 baseline was established rather than as active roadmap items.

### Milestone 1 — Draft-system compatibility

Established FermUnits as the quantity/conversion boundary for the Draft System
Engine, including pressure, temperature, flow, density, viscosity, pressure
gradient, carbonation quantities, dimensional failures, and explicit US-liquid
unit behavior. Draft-system engineering models remain downstream.

### Milestone 2 — Carbonation source verification

Completed the accessible-source review for carbonation and documented the
remaining direct ASBC verification gap. The implemented relationship remains
Provisional where authoritative method text has not established normative
reference conditions or reporting precision.

### Milestone 3 — Brewing verification backlog

Reconciled the implemented brewing relationships with maintained source records
and explicit Verified, Provisional, Ambiguous, Rejected, or Pending status.
Reviews covered gravity/extract semantics, refractometer scope, beer color,
analytical bitterness, diastatic power, carbonation, and brewery-vessel naming.

### Milestone 4 — Solution-chemistry semantic boundaries

Defined which solution-chemistry concerns belong in FermUnits versus downstream
models. The milestone established the `PHValue`/hydrogen-ion-activity boundary,
kept conductivity as an ordinary Pint quantity, retained reported bounds and
uncertainty downstream, and hardened chemical-equivalence context validation.

### Milestone 5 — Python compatibility and adoption

Established Python 3.11 as the supported floor, continuous Python 3.11–3.14 CI,
and the Pint `>=0.25.3,<0.26` compatibility baseline. The maintained downstream
contracts were aligned with FermUnits' public Pint-facing API.

### Milestone 6 — Additional fermentation domains

Migrated the legacy wine, cider/perry, distilling, sake, biofuel, and acid-tier
inventories into maintained source-traceable references. Ownership, naming, and
scientific-status decisions were recorded without adding speculative public API.
Remaining source-ready candidates stay demand-driven.

### 1.0 stabilization and review

The 1.0 cycle completed:

- public API and naming stabilization;
- finite-result and controlled-validation boundaries;
- centralized scientific verification-status documentation;
- maintained downstream compatibility contracts;
- deep internal review and remediation;
- deep external review and remediation;
- release-workflow, artifact-integrity, and publication hardening;
- project-specific pre-release and post-release verification.

FermUnits 1.0.0 therefore marks the supported public API and documented semantics
as intentionally stable for the 1.x series. It does not imply that every
conceivable fermentation-domain unit or calculation has been implemented.

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
