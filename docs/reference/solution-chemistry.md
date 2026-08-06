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
- FermUnits registry extensions needed for clear, qualified meanings;
- calculations that require chemical identity, density, molar mass, charge, or
  another explicit parameter;
- analytical or reporting semantics that must not be reduced to a unit alone;
- application-schema concerns that belong primarily in FermentationJSON or a
  downstream engineering application.

FermUnits performs dimensional conversions and reusable domain calculations
without claiming ownership of the full chemical model.

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
- Sources: [SH-SI-01], [SH-PINT-01]

### Molality

- Practical unit: `mole / kilogram`.
- Pint audit:
  - `molal` alias not found;
  - `mole / kilogram` is supported directly.
- FermUnits action:
  - use the compound expression;
  - do not add `molal` merely as a convenience alias.
- Status: **Physical quantity supported through Pint; alias deferred.**
- Sources: [SH-PINT-01]

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

- FermUnits name: `equivalent`
- Alias: `eq`
- Pint audit: not found.
- FermUnits representation:
  - separate `[chemical_equivalent]` dimension;
  - no direct conversion to amount of substance;
  - conversion requires an explicit equivalence factor.
- Public functions:
  - `amount_to_equivalents`
  - `equivalents_to_amount`
  - `amount_concentration_to_equivalent_concentration`
  - `equivalent_concentration_to_amount_concentration`
- Status: **Implemented.**
- Sources: [SC-IUPAC-01]

### Milliequivalent

- FermUnits name: `milliequivalent`
- Alias: `mEq`
- Definition:
  - `1 milliequivalent = 0.001 equivalent`
- Equivalent concentration is composed normally through Pint:
  - `equivalent / liter`
  - `milliequivalent / liter`
- Status: **Implemented.**
- Sources: [SC-IUPAC-01], [SC-EPA-01]

### Equivalence factor

- Meaning: equivalents per mole for the stated entity and reaction or charge
  convention.
- FermUnits rule:
  - must be supplied explicitly;
  - must be finite and greater than zero;
  - is never guessed from a unit string.
- Status: **Implemented as a required calculation parameter.**
- Sources: [SC-IUPAC-01]

### Equivalent mass

- Meaning: grams per equivalent for the stated chemical entity, reaction, or
  reporting basis.
- Public functions:
  - `mass_concentration_to_equivalent_concentration`
  - `equivalent_concentration_to_mass_concentration`
- FermUnits rule:
  - equivalent mass must be supplied explicitly;
  - the value must be finite and greater than zero;
  - chemical identity and reporting basis remain application semantics.
- Status: **Implemented.**
- Sources: [SC-IUPAC-01]

### Normality

- Pint audit:
  - `normal` not found;
  - `normality` not found.
- FermUnits rule:
  - do not add either name;
  - use explicit equivalent concentration such as `mEq/L`;
  - retain the reaction basis separately.
- Status: **Deferred intentionally.**
- Sources: [SC-IUPAC-01]

## 3. Composition fractions

### Mass fraction

- Dimensionality: dimension one.
- FermUnits rule:
  - use Pint dimensionless arithmetic;
  - preserve that the basis is mass/mass separately.
- Status: **Physical representation and density-assisted conversion implemented.**

### Volume fraction

- Dimensionality: dimension one.
- FermUnits rule:
  - preserve the volume/volume basis;
  - retain reference temperature when material;
  - do not assume additive volumes for non-ideal mixtures.
- Status: **Physical representation available; semantic API pending.**

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

### Percent

- Pint name: `percent`
- Pint audit: confirmed.
- FermUnits rule:
  - use Pint directly;
  - preserve fraction kind separately.
- Status: **Confirmed provided by Pint; semantic qualification required.**
- Sources: [SH-PINT-01]

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
- Sources: [SH-PINT-01], [SH-SI-01]

### Canonical mass-fraction forms

Use explicit ratios:

- `milligram / kilogram` for a mass fraction of `10^-6`;
- `microgram / kilogram` for a mass fraction of `10^-9`.

FermUnits does not add:

- `ppm_mass`;
- `ppb`;
- `ppb_mass`.

A source value reported as `ppm` or `ppb` may retain that label as reported
metadata, but canonical chemistry data should state the ratio basis explicitly.

Status: **Representation decision complete.**

Sources: [SH-SI-01]

## 5. Density-assisted concentration conversions

### Mass fraction and mass concentration

Public functions:

- `mass_concentration_to_mass_fraction`
- `mass_fraction_to_mass_concentration`

Rules:

- solution density is required explicitly;
- density must be finite, positive, and dimensionally mass per volume;
- no silent `1 kilogram / liter` approximation is made;
- mass fractions may be expressed explicitly as `milligram / kilogram`,
  `microgram / kilogram`, or another compatible mass ratio;
- density reference temperature remains application metadata.

Status: **Implemented.**

### Mass concentration and amount concentration

- Required input: explicit molar mass.
- FermUnits rule:
  - molar mass must match chemical identity and hydration state;
  - hydration state is not a unit.
- Status: **Planned calculation.**

### Volume fraction and mass fraction

- May require constituent density, mixture density, temperature, and
  non-ideal mixing data.
- FermUnits rule: no universal one-step conversion.
- Status: **Deferred.**

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
- preserve reporting basis as explicit application metadata;
- do not imply that “as CaCO3” means actual dissolved calcium carbonate;
- add calculations only when the conversion basis is explicit and sourced.

### Calcium-carbonate equivalent basis

Public functions:

- `caco3_basis_mass_concentration_to_equivalent_concentration`
- `equivalent_concentration_to_caco3_basis_mass_concentration`

Implemented convention:

- `50 mg/L as CaCO3 = 1 mEq/L`;
- equivalently, `50 g as CaCO3 per equivalent`.

This is the conventional water-analysis reporting factor used by EPA
alkalinity and hardness methods. The returned mass concentration does not
carry “as CaCO3” inside the Pint unit; the calling water model must retain that
reporting basis explicitly.

Status: **Implemented for CaCO3-basis conversion.**

Sources: [SC-EPA-01], [SC-USGS-01]

## 7. pH and logarithmic quantities

### pH

- Representation: validated semantic value, not a multiplicative Pint unit.
- Arithmetic rule:
  - do not blend or average pH using generic linear-quantity operations;
  - activity conversions must be explicit.
- Status: **Documented; implementation pending.**

### pH interval

- Needed for buffering capacity expressed per pH-unit change.
- FermUnits rule:
  - distinguish absolute pH from a pH difference;
  - do not model this as division by an absolute pH reading.
- Status: **Pending semantic design.**

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

## 9. Boundary with FermentationJSON and water engines

- FermentationJSON requires a canonical quantity.
- FermentationJSON allows an optional reported quantity and strongly recommends
  it for imported or user-entered data.
- FermUnits provides conversion behavior and reusable semantics, but does not
  own the complete serialized document model.
- A water-treatment engine owns chemical identity, ion charge, analyte,
  quantity kind, and reporting basis.
- FermUnits does not infer alkalinity or hardness from a mass-concentration
  value alone.
- Status: **Project architecture decision.**

## 10. Implementation summary

Implemented FermUnits units:

- `equivalent`
- `milliequivalent`
- aliases `eq` and `mEq`

Implemented calculations:

- amount of substance to and from equivalent amount;
- amount concentration to and from equivalent concentration;
- mass concentration to and from equivalent concentration using an explicit
  equivalent mass;
- CaCO3-basis mass concentration to and from equivalent concentration;
- mass concentration to and from mass fraction using explicit solution density.

Representation decisions:

- use explicit `mg/kg` instead of a qualified `ppm_mass` unit;
- use explicit `µg/kg` instead of defining `ppb`;
- preserve source `ppm` and `ppb` labels only as reported metadata with an
  explicit basis.

Deferred:

- `normal`
- `normality`
- `molal` convenience alias
- pH semantic type
- general mass/amount concentration conversion
- general reported-quantity wrapper

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

### [SC-IUPAC-01] Equivalent entity

- Organization: International Union of Pure and Applied Chemistry
- Source: IUPAC Gold Book, “equivalent entity”
- URL: https://goldbook.iupac.org/terms/view/E02192
- Accessed: 2026-08-06
- Source tier: 2
- Supports:
  - equivalence depends on the specified reaction or charge relationship;
  - equivalents must not be treated as universally interchangeable with
    moles without an explicit factor.

### [SC-EPA-01] Methods for Chemical Analysis of Water and Wastes

- Organization: United States Environmental Protection Agency
- Methods:
  - 130.2, Hardness, Total (Titrimetric, EDTA)
  - 310.1, Alkalinity (Titrimetric, pH 4.5)
- URL: https://nepis.epa.gov/Exe/ZyPURL.cgi?Dockey=30000Q10.TXT
- Accessed: 2026-08-06
- Source tier: 2
- Supports:
  - hardness and alkalinity reporting in `mg/L as CaCO3`;
  - the conventional factor of `50,000` in titration formulas;
  - the equivalent relationship `50 mg/L as CaCO3 = 1 mEq/L`.

### [SC-USGS-01] Alkalinity and Acid Neutralizing Capacity

- Organization: United States Geological Survey
- Publication: National Field Manual, Chapter A6.6
- URL: https://pubs.usgs.gov/twri/twri9a6/twri9a_6.6.pdf
- Accessed: 2026-08-06
- Source tier: 3
- Supports:
  - alkalinity as a chemical property rather than a dissolved CaCO3
    concentration;
  - reporting alkalinity in equivalent concentration and as CaCO3.
- Note:
  - some USGS calculations use a more precise molar-mass-derived factor near
    `50.044 mg/mEq`; FermUnits uses the conventional EPA water-reporting factor
    of exactly `50 mg/mEq` for this API.
