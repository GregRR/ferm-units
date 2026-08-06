# FermUnits Reference Inventories

This directory contains the maintained technical inventories used to plan,
implement, test, and review FermUnits definitions, calculations, analytical
scales, and semantic quantity types.

These files are not merely wish lists. Each entry should state what the term
means, where it is used, whether it is a physical unit or a method-defined
quantity, how FermUnits intends to represent it, and which sources support the
claim.

## Files

| Domain | Reference file | Current state |
|---|---|---|
| Brewing | [brewing-units.md](brewing-units.md) | Revised and sourced |
| Wine | [wine-units.md](wine-units.md) | Revised and sourced |
| Distilling | `distilling-units.md` | Migration pending |
| Sake | `sake-units.md` | Migration pending |
| Cider and perry | `cider-perry-units.md` | Migration pending |
| Biofuels | `biofuel-units.md` | Migration pending |
| Acid-tier and other fermentation | `acid-tier-units.md` | Migration pending |
| Solution chemistry | [solution-chemistry.md](solution-chemistry.md) | Initial maintained inventory |

The domain files are the maintained source documents. A combined project-wide
inventory may be generated from them, but it should not be edited independently.

## Required entry fields

Every stable or proposed entry should identify, as applicable:

- the preferred FermUnits name;
- accepted aliases;
- rejected or ambiguous aliases;
- the exact numerical definition or calculation;
- dimensionality and reference conditions;
- jurisdiction, region, industry, analytical method, or reporting basis;
- modern, historical, customary, legal, provisional, or semantic status;
- implementation status;
- one or more source identifiers;
- relevant Pint behavior and the resulting FermUnits decision.

Source identifiers point to the bibliography at the bottom of the same domain
file or to a shared source recorded in [`../sources.md`](../sources.md).

## Source identifiers

Domain source identifiers use a short prefix:

- `BR-` — brewing
- `WI-` — wine
- `DI-` — distilling
- `SA-` — sake
- `CP-` — cider and perry
- `BF-` — biofuels
- `AT-` — acid-tier and other fermentation
- `SC-` — solution chemistry
- `SH-` — shared project sources

## Status vocabulary

Use the status terms defined in [`../sources.md`](../sources.md):

- **Verified**
- **Provisional**
- **Pending**
- **Rejected**
- **Ambiguous**

Implementation status and source status are separate.

## Pint-first extension policy

Before adding any FermUnits unit definition or alias:

1. Review the Pint documentation for the pinned project version.
2. Review Pint's bundled unit definitions.
3. Verify the behavior of the pinned local registry.
4. Check aliases, dimensionality, and naming collisions.
5. Decide whether the Pint meaning is correct for the FermUnits use case.

Apply these rules:

- Use Pint directly when Pint already provides the correct unit and meaning.
- Do not duplicate a Pint unit under a FermUnits name solely for convenience.
- Do not create named aliases for compound expressions that Pint already
  composes correctly, such as `gram / mole` or `millimole / liter`.
- Preserve a legitimate Pint definition when a fermentation-domain meaning
  conflicts with it.
- Add an explicit domain- or region-qualified FermUnits name when a collision
  must be resolved.
- Add calculations or semantic metadata, rather than a duplicate unit, when
  Pint already represents the physical dimensions but not the analytical or
  chemical meaning.
- Add a FermUnits definition only when Pint genuinely lacks the required unit
  or qualified meaning.
- Treat a unit's absence from the local Pint registry as an implementation
  candidate, not as automatic justification for adding it.

Record the Pint result and FermUnits decision in the relevant reference entry.

## Naming rules

- Preserve legitimate Pint definitions.
- Add domain-qualified names when a plain term has multiple legitimate meanings.
- Do not assign a universal value to a variable regional or historical term.
- Keep analytical scales and empirical calculations separate from ordinary
  multiplicative physical units.
- Keep reporting bases, chemical identity, hydration state, and analytical
  method separate from the unit when they are not part of the dimensionality.
- Record aliases that were considered and rejected.
- Prefer explicit stored unit identifiers over locale-dependent interpretation.

## Physical units, calculations, and semantic quantities

Reference entries should distinguish among:

- **physical units**
- **compound units**
- **analytical scales**
- **calculations**
- **reporting bases**
- **semantic quantities**

A numerically valid unit conversion must not discard the scientific meaning of
the original value.

## Copyright and restricted methods

Do not commit full copyrighted methods, restricted tables, scans, or substantial
verbatim extracts unless the project has permission to redistribute them.

It is appropriate to record method titles and identifiers, bibliographic
citations, concise original summaries, lawful formulas or definitions, and
notes describing what still needs verification.
