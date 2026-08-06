# Solution Chemistry Units and Calculations Reference

This document is the maintained shared solution-chemistry inventory for
FermUnits. It covers physical quantities, composition quantities, conventional
reporting forms, chemical-equivalent calculations, and semantic requirements
used across brewing, wine, cider and perry, sake, distilling, water treatment,
biofuels, and other fermentation-related applications.

A source identifier after an entry points to the bibliography at the bottom of
this file or to a shared source in [`../sources.md`](../sources.md).

## Scope and architectural boundary

Solution chemistry is a shared FermUnits domain rather than a
beverage-specific domain.

This inventory distinguishes among:

- ordinary multiplicative physical units that Pint already supplies;
- FermUnits registry extensions that may be needed for clear, qualified names;
- calculations that require chemical identity, density, molar mass, charge, or
  another explicit parameter;
- analytical or reporting semantics that must not be reduced to a unit alone;
- application-schema concerns that belong primarily in FermentationJSON or a
  downstream engineering application.

FermUnits should perform dimensional conversions and domain calculations
without discarding semantic qualifiers.

## Pint-first rule

Before adding any unit or alias in this domain:

1. review Pint's documentation for the pinned version;
2. review Pint's bundled definitions;
3. verify the pinned local registry;
4. check aliases, dimensionality, and collisions;
5. add a FermUnits definition only when Pint genuinely lacks the needed unit or
   qualified meaning.

Do not create convenience names for compound expressions that Pint already
composes correctly.

## 1. Amount of substance and molar quantities

### Mole

- Pint name: `mole`
- Symbol: `mol`
- FermUnits action: use Pint directly.
- Status: **Confirmed provided by Pint.**
- Sources: [SH-SI-01], [SH-PINT-01]

### Millimole and micromole

- Pint names: `millimole`, `micromole`
- FermUnits action: use Pint directly.
- Status: **Confirmed provided by Pint.**
- Sources: [SH-SI-01], [SH-PINT-01]

### Amount-of-substance concentration

- Pint alias confirmed: `molar`
- Preferred explicit stored forms:
  - `mole / liter`
  - `millimole / liter`
  - `micromole / liter`
- FermUnits action:
  - use Pint directly;
  - do not add aliases such as `mole_per_liter`;
  - require explicit molar mass for mass-concentration conversions.
- Status: **Confirmed composable through Pint.**
- Sources: [SH-IUPAC-GOLD-01], [SH-SI-01], [SH-PINT-01]

### Molality

- Practical unit: `mole / kilogram`.
- Pint audit:
  - `molal` alias not found;
  - `mole / kilogram` is supported directly.
- FermUnits action:
  - use the compound expression;
  - do not add `molal` merely as a convenience alias.
- Status: **Physical quantity supported through Pint; alias deferred.**
- Sources: [SH-IUPAC-GOLD-01], [SH-PINT-01]

### Molar mass

- Practical unit: `gram / mole`.
- SI coherent unit: `kilogram / mole`.
- FermUnits action:
  - use Pint directly;
  - do not add `gram_per_mole`;
  - keep chemical formula and hydration state outside the unit.
- Status: **Confirmed composable through Pint.**
- Sources: [SH-SI-01], [SH-PINT-01]

## 2. Chemical equivalents and equivalent concentration

### Chemical equivalent

- Proposed FermUnits name: `equivalent`
- Proposed alias: `eq`
- Pint audit: not found.
- Architectural rule:
  - no universal conversion between moles and equivalents;
  - conversion requires an explicit equivalence factor.
- Status: **Implementation candidate; authoritative definition and design
  review pending.**
- Sources: [SC-PENDING-01]

### Milliequivalent

- Proposed FermUnits name: `milliequivalent`
- Proposed alias: `mEq`
- Pint audit: not found.
- Definition if `equivalent` is adopted:
  - `1 milliequivalent = 0.001 equivalent`
- Status: **Implementation candidate; depends on equivalent design.**
- Sources: [SC-PENDING-01]

### Normality

- Pint audit:
  - `normal` not found;
  - `normality` not found.
- FermUnits rule:
  - do not add either name until authoritative terminology and reaction-basis
    requirements are resolved.
- Status: **Deferred.**
- Sources: [SC-PENDING-01]

## 3. Composition fractions

### Mass fraction

- Dimensionality: dimension one.
- FermUnits rule:
  - use Pint dimensionless arithmetic;
  - preserve that the basis is mass/mass separately.
- Status: **Physical representation available; semantic API pending.**
- Sources: [SH-IUPAC-GOLD-01], [SH-NIST-SI-01]

### Volume fraction

- Dimensionality: dimension one.
- FermUnits rule:
  - preserve the volume/volume basis;
  - retain reference temperature when material;
  - do not assume additive volumes for non-ideal mixtures.
- Status: **Physical representation available; semantic API pending.**
- Sources: [SH-IUPAC-GOLD-01], [SH-NIST-SI-01]

### Mass-per-volume composition

- Common forms:
  - `gram / liter`
  - `gram / 100 milliliter`
  - percent mass/volume
- Dimensionality: mass per volume.
- FermUnits rule:
  - `% w/v` must remain distinct from mass and volume fractions;
  - use Pint compound expressions rather than adding convenience units.
- Status: **Representable through Pint.**
- Sources: [SH-IUPAC-GOLD-01], [SH-PINT-01]

### Percent

- Pint name: `percent`
- Pint audit: confirmed.
- FermUnits rule:
  - use Pint directly;
  - preserve fraction kind separately.
- Status: **Confirmed provided by Pint; semantic qualification required.**
- Sources: [SH-NIST-SI-01], [SH-PINT-01]

## 4. Parts-per notation

### Generic ppm

- Pint name: `ppm`
- Pint audit: confirmed.
- FermUnits rule:
  - preserve Pint's unit;
  - do not redefine or replace it;
  - avoid unqualified `ppm` in saved chemistry data unless basis metadata is
    present.
- Status: **Confirmed provided by Pint; qualified use required.**
- Sources: [SH-PINT-01], [SH-NIST-SI-01]

### Parts per million by mass

- Candidate FermUnits name: `ppm_mass`
- Intended exact relationship:
  - mass fraction of `10^-6`;
  - equivalently `1 milligram / kilogram`.
- Pint audit: qualified name not found.
- FermUnits rule:
  - decide whether this is a unit alias or Pint `ppm` plus required metadata;
  - do not implement before that semantic decision.
- Status: **Semantic design candidate.**
- Sources: [SH-NIST-SI-01], [SC-PENDING-02]

### Parts per billion by mass

- Candidate FermUnits name: `ppb_mass`
- Intended exact relationship:
  - mass fraction of `10^-9`;
  - equivalently `1 microgram / kilogram`.
- Pint audit:
  - generic `ppb` not found;
  - qualified `ppb_mass` not found.
- Status: **Semantic design candidate.**
- Sources: [SH-NIST-SI-01], [SC-PENDING-02]

## 5. Density-assisted concentration conversions

### Mass fraction and mass concentration

- Required input: explicit solution density.
- FermUnits rule:
  - do not silently assume `1 kilogram / liter`;
  - preserve density reference temperature where known.
- Status: **Planned calculation.**
- Sources: [SH-IUPAC-GOLD-01], [SC-PENDING-03]

### Mass concentration and amount concentration

- Required input: explicit molar mass.
- FermUnits rule:
  - molar mass must match chemical identity and hydration state;
  - hydration state is not a unit.
- Status: **Planned calculation.**
- Sources: [SH-IUPAC-GOLD-01], [SC-PENDING-03]

### Volume fraction and mass fraction

- May require constituent density, mixture density, temperature, and
  non-ideal mixing data.
- FermUnits rule: no universal one-step conversion.
- Status: **Deferred.**
- Sources: [SC-PENDING-03]

## 6. Reporting bases

Examples include:

- alkalinity as calcium carbonate;
- hardness as calcium carbonate;
- titratable acidity as tartaric acid;
- titratable acidity as malic acid;
- volatile acidity as acetic acid;
- concentration as elemental nitrogen or phosphorus.

FermUnits rule:

- preserve the ordinary physical quantity;
- preserve reporting basis as explicit metadata;
- do not imply that “as CaCO3” means actual dissolved calcium carbonate;
- add calculations only when the conversion basis is explicit and sourced.

Status: **Architectural requirement accepted; API pending.**

Sources: [SH-OIV-01], [SC-PENDING-04]

## 7. pH and logarithmic quantities

### pH

- Representation: validated semantic value, not a multiplicative Pint unit.
- Arithmetic rule:
  - do not blend or average pH using generic linear-quantity operations;
  - activity conversions must be explicit.
- Status: **Documented; implementation pending.**
- Sources: [SH-OIV-01], [SC-PENDING-05]

### pH interval

- Needed for buffering capacity expressed per pH-unit change.
- FermUnits rule:
  - distinguish absolute pH from a pH difference;
  - do not model this as division by an absolute pH reading.
- Status: **Pending semantic design.**
- Sources: [SC-PENDING-05]

## 8. Measurement qualifiers, bounds, and uncertainty

Required qualifiers include:

- exact;
- approximate;
- less than;
- less than or equal;
- greater than;
- greater than or equal;
- interval or range;
- uncertainty;
- stated statistic;
- detection or quantitation limit.

FermUnits requirement:

- conversion changes value and unit;
- conversion preserves the qualifier;
- interval endpoints convert independently;
- uncertainty converts with the quantity;
- a bound never becomes an unqualified exact value.

Example invariant:

```text
< 10 milligram/liter -> < 0.010 gram/liter
```

Status: **Requirement accepted; API pending.**

Sources: [SC-PENDING-06]

## 9. Boundary with FermentationJSON

- FermentationJSON requires a canonical quantity.
- FermentationJSON allows an optional reported quantity and strongly recommends
  it for imported or user-entered data.
- FermUnits provides conversion behavior and reusable semantics, but does not
  own the complete serialized document model.
- Status: **Project architecture decision.**

## 10. Current implementation candidates

A missing Pint name is only an implementation candidate.

Candidates requiring further review:

- `equivalent`
- `milliequivalent`

Semantic candidates requiring a representation decision:

- `ppm_mass`
- `ppb_mass`

Deferred:

- `normal`
- `normality`
- `molal` convenience alias

No FermUnits definition needed:

- `mole`
- `millimole`
- `micromole`
- `molar`
- `percent`
- `ppm`
- `mole / liter`
- `millimole / liter`
- `micromole / liter`
- `mole / kilogram`
- `millimole / kilogram`
- `gram / mole`
- `kilogram / mole`

## 11. Solution-chemistry bibliography

### [SC-PENDING-01] Chemical equivalents and normality

- Status: pending authoritative terminology and metrology review.

### [SC-PENDING-02] Qualified parts-per notation

- Status: pending final source and representation review.

### [SC-PENDING-03] Composition conversion equations

- Status: pending implementation-source review.

### [SC-PENDING-04] Reporting-basis semantics

- Status: pending cross-domain design and source review.

### [SC-PENDING-05] pH and pH intervals

- Status: pending authoritative definition and API design.

### [SC-PENDING-06] Bounds, detection limits, and uncertainty

- Status: pending metrology-source review.
