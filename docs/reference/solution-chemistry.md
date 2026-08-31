# Solution Chemistry Units and Calculations Reference

This document is the maintained shared solution-chemistry inventory for
FermUnits. It covers physical quantities, composition quantities, conventional
reporting forms, chemical-equivalent calculations, and semantic requirements
used across brewing, wine, cider and perry, sake, distilling, water treatment,
biofuels, and other fermentation-related applications.

Every source identifier used here has a master bibliographic record in
[`../sources.md`](../sources.md). Claim-specific context may also be repeated
below when it helps explain the solution-chemistry decision.

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
  - is never guessed from a unit string;
  - the registered `chemical_equivalence` Pint context enforces the same
    validation when used directly, so callers cannot bypass the invariant
    by skipping the convenience functions.
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
  - chemical identity and reporting basis remain application semantics;
  - the registered `chemical_equivalent_mass` Pint context enforces the
    same validation when used directly.
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
- IUPAC definition: constituent volume divided by the sum of constituent
  volumes before mixing. [SC-IUPAC-FRACTION-01]
- FermUnits rule:
  - use Pint dimensionless arithmetic and Pint's existing `percent` unit;
  - do not add a `percent_by_volume`, `% v/v`, or similar registry alias;
  - preserve the fact that a value is a volume fraction in downstream quantity
    metadata because Pint dimensionality cannot distinguish mass, amount, and
    volume fractions;
  - retain reference conditions when a domain method requires them;
  - do not infer a mass fraction or final-mixture composition from volume
    fraction without an explicit physical model.
- Status: **Representation decision complete; no FermUnits semantic API
  required.**
- Sources: [SC-IUPAC-FRACTION-01], [SH-PINT-01]

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

Public functions:

- `mass_concentration_to_amount_concentration`
- `amount_concentration_to_mass_concentration`

Rules:

- molar mass is required explicitly as a Pint quantity;
- molar mass must be finite, positive, and dimensionally mass per amount of
  substance;
- molar mass must match the chemical identity and hydration state of the
  concentration being converted;
- hydration state is not encoded in the unit;
- FermUnits does not infer chemical identity or choose a molar mass from an
  analyte name.

Status: **Implemented.**

Sources: [SH-SI-01]

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

IUPAC defines pH as the negative base-10 logarithm of hydrogen-ion activity.
The definition is explicitly activity-based, not a hydrogen-ion concentration
identity, and IUPAC also notes the special metrological difficulty of assigning
single-ion activity. [SC-IUPAC-PH-01] [SC-IUPAC-PH-02]

FermUnits representation:

- `PHValue` is a small immutable semantic type for a finite numeric pH scale
  value; it is not a Pint quantity and does not define ordinary quantity
  arithmetic;
- `ph_to_hydrogen_ion_activity` accepts `PHValue` and returns the dimensionless
  activity appearing in the pH definition;
- `hydrogen_ion_activity_to_ph` performs the inverse definition and returns a
  `PHValue`;
- neither function converts between activity and concentration or infers an
  activity coefficient;
- FermUnits does not impose a 0-through-14 validation rule; it validates
  finiteness and floating-point representability rather than inventing a
  universal scientific range;
- Pint's existing `pH` unit spelling is preserved: with `p` as the pico prefix
  and `H` as henry, `pH` is picohenry in the supported Pint registry.
  [SH-PINT-01]

Status: **Verified definition; implemented as a semantic value type plus
explicit activity conversion functions.**

### pH difference

A difference between two pH values is a difference on a logarithmic scale. It
must not be represented as a multiplicative Pint unit or confused with a linear
change in hydrogen-ion concentration or activity. Buffer-capacity and similar
models may use an explicitly named numeric pH difference downstream. FermUnits
does not currently need a separate `delta_pH` type.

Status: **Boundary decision complete; no separate API required.**

## 8. Measurement results, bounds, detection limits, and uncertainty

Bounds, intervals, source-reported qualifiers, detection/quantitation limits,
and measurement uncertainty describe a measurement result or analytical
procedure rather than a new physical unit. The VIM treats a measurement result
as a quantity value together with relevant information, defines measurement
uncertainty as a parameter characterizing dispersion, and defines detection
limit in terms of a specified measurement procedure and error probabilities.
[SH-JCGM-VIM-01]

FermUnits rule:

- do not add a general reported-quantity, bounded-quantity, nondetect, LOD, LOQ,
  or uncertainty wrapper;
- keep exact/approximate, `<`, `<=`, `>`, `>=`, interval/range, nondetect,
  reporting-limit, LOD/LOQ, stated-statistic, and provenance semantics in the
  downstream measurement or serialization model;
- keep any numeric threshold itself as an ordinary Pint quantity so the
  downstream model can convert it without changing its qualifier or meaning;
- never resolve a bound, range, or nondetect to a scalar value inside FermUnits;
- do not add an uncertainty-propagation framework. Pint already offers optional
  `Measurement` integration when the third-party `uncertainties` package is
  installed, but its documented scope is limited and FermUnits does not require
  that dependency. [SH-PINT-MEASUREMENT-01]

The expected downstream invariant remains, for example, that converting a
reported `< 10 mg/L` threshold to `g/L` yields `< 0.010 g/L`; the `<` semantic is
owned by the wrapper, while Pint/FermUnits owns the quantity conversion.

Status: **Boundary decision complete; no FermUnits wrapper API required.**

## 9. Boundary with FermentationJSON and water engines

- FermentationJSON requires a canonical quantity.
- FermentationJSON allows an optional reported quantity and strongly recommends
  it for imported or user-entered data.
- FermUnits provides conversion behavior and reusable semantics, but does not
  own the complete serialized document model.
- Water Chemistry Engine owns chemical identity, ion charge, analyte,
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
- mass concentration to and from mass fraction using explicit solution density;
- mass concentration to and from amount concentration using explicit molar
  mass;
- `PHValue` representation plus pH to and from dimensionless hydrogen-ion
  activity, without concentration or activity-coefficient inference.

Representation decisions:

- use explicit `mg/kg` instead of a qualified `ppm_mass` unit;
- use explicit `µg/kg` instead of defining `ppb`;
- preserve source `ppm` and `ppb` labels only as reported metadata with an
  explicit basis.

Deferred:

- `normal`
- `normality`
- `molal` convenience alias

Explicitly downstream rather than deferred FermUnits APIs:

- general reported-quantity wrappers for bounds, ranges, nondetects, and
  source qualifiers;
- detection/reporting/quantitation-limit semantics;
- measurement-uncertainty models and propagation policy;
- domain policy for resolving any of those values to a scalar.

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
