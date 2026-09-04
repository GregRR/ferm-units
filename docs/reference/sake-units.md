# Sake Units and Calculations Reference

This document is the maintained sake-domain reference for FermUnits. It
supersedes the planning material retained under
[`legacy/sake-inventory.txt`](legacy/sake-inventory.txt) as the source of truth
for current ownership decisions, implementation status, and source-verification
status.

The Milestone 6 migration does **not** turn the legacy inventory into a feature
checklist. Sake combines an analytical density-derived scale, method-defined
titration indices, ordinary dimensionless production ratios, historical Japanese
capacity measures, packaging conventions, and sensory/classification formulas.
Those categories must remain distinct.

## Migration outcome

The legacy sake inventory is triaged into six ownership classes:

1. **method-defined analytical scales** — Nihonshudo (Sake Meter Value) is a
   density-derived semantic scale with an explicit 15 °C measurement basis;
2. **method-defined titration indices** — sake acidity is defined by a prescribed
   analytical procedure and endpoint rather than by a new physical dimension;
3. **ordinary dimensionless physical quantities** — rice polishing ratio is a
   mass fraction and should use ordinary dimensionless/percent quantities;
4. **historical customary volume measures** — koku, to, sho, and go require
   historical/metrological sourcing and should not be added merely because they
   appear in the legacy inventory;
5. **packaging and application semantics** — an isshobin is a bottle/package
   convention, not a new dimension;
6. **pending or rejected sensory shortcuts** — unsupported legacy sweetness and
   balance formulas are not universal conversions.

No new public API is added by this migration slice.

## Nihonshudo / Sake Meter Value

The National Research Institute of Brewing prescribed sake analysis method
measures sake density/specific gravity at 15 °C. For the vibrating-density-meter
method, density at 15 °C is converted to specific gravity on a `15/4 °C` basis,
and Nihonshudo is calculated as: [SA-NRIB-METHODS-01]

```text
nihonshudo = 1443 / S - 1443
```

where `S` is specific gravity at `15/4 °C`. The inverse relationship is therefore:

```text
S = 1443 / (nihonshudo + 1443)
```

This is a semantic analytical scale, not an ordinary multiplicative Pint unit.
The reference temperatures are part of the meaning and must not be erased.

Ownership:

- a specific-gravity input remains a dimensionless FermUnits/Pint quantity;
- Nihonshudo should be represented as a semantic scalar if a downstream consumer
  later needs it;
- a future reusable API should use explicit conversion functions rather than a
  Pint unit definition;
- measurement method, temperature control, calibration, uncertainty, and sample
  preparation remain measurement metadata.

Implementation status: **Not implemented; source-ready if a real consumer needs
an explicit Nihonshudo API.**

### Sweet/dry interpretation

Nihonshudo is often used as a dryness/sweetness indicator, but the National Tax
Agency cautions that density is affected by both alcohol and dissolved
components and that sweetness/dryness cannot be determined from Nihonshudo
alone. [SA-NTA-SWEETNESS-01]

Status: **Application/sensory interpretation; not a FermUnits unit conversion.**

## Sake acidity / sando

The prescribed sake analysis method defines acidity through titration of a
10 mL sake sample with standardized `N/10` sodium hydroxide. The indicator method
uses a specified mixed indicator; the pH-meter method titrates to pH 7.2. The
reported acidity is the titration volume multiplied by the standardized solution
factor `F`. The method also provides a separate optional conversion for reporting
as succinic acid. [SA-NRIB-METHODS-01]

The legacy inventory's description of `sando` as simply the millilitres of
`0.1 M` NaOH needed for 10 mL of sake is therefore incomplete: reagent
standardization and endpoint definition are part of the analytical result.

Ownership:

- preserve the prescribed method, sample volume, endpoint, titrant basis, and
  standardization factor with the result;
- do not define a universal `sando` multiplicative unit;
- if an application needs the raw titrant volume, represent it as an ordinary
  volume quantity plus method metadata;
- if it needs an acid-equivalent mass concentration, use an explicit reporting
  basis rather than silently treating the acidity index as `g/L`.

Implementation status: **No new FermUnits unit required.** A future semantic
helper would need a concrete downstream use case and explicit method contract.

## Legacy Amando / sweetness-acidity shortcut

The legacy inventory proposes:

```text
amando = nihonshudo / 10 - sando
```

No authoritative source reviewed in this migration establishes that relationship
as a universal sake standard. Current National Tax Agency material uses a
different sweetness/dryness calculation involving Nihonshudo and acidity in
specific reporting contexts. [SA-NTA-SWEETNESS-01]

Status: **Rejected as a universal FermUnits conversion.** If a downstream
application needs a named sensory index, the exact published method and scope
must be identified and represented explicitly.

## Rice polishing ratio / seimaibuai

The National Tax Agency defines rice polishing ratio as the weight percentage of
polished white rice relative to the brown rice from which it was milled.
[SA-NTA-LABEL-01] The same labeling standard uses polishing-ratio thresholds in
several specially designated sake categories, including 70%, 60%, and 50%
criteria depending on category. [SA-NTA-LABEL-01]

This is an ordinary mass fraction:

```text
polishing ratio = polished-rice mass / brown-rice mass
```

Ownership:

- represent the value with an ordinary dimensionless FermUnits/Pint quantity,
  normally displayed as percent;
- keep rice identity, milling method, regulatory classification, rounding, and
  labeling decisions downstream;
- do not create a `seimaibuai` unit alias for `percent`.

Implementation status: **No new FermUnits API required.**

## Traditional Japanese capacity measures

The legacy inventory lists `koku`, `to`, `sho`, and `go` as a decimal hierarchy
of historical Japanese capacity measures and gives metric equivalents derived
from the traditional sho. A National Diet Library reference-service record
corroborates the historical hierarchy and approximately `180.39 L` per koku,
while tracing the metric relationship to historical weights-and-measures
sources. [SA-NDL-MEASURES-01]

That source is useful corroboration but is not the primary metrology text. The
migration therefore does not promote the legacy decimal values into stable
FermUnits definitions yet.

Ownership:

- these are genuine historical/customary volume concepts, not sake-only
  chemistry;
- if a real consumer needs them, first verify the exact modern/historical legal
  definition from a primary metrology source and check Pint for naming
  collisions;
- prefer unambiguous names if historical or modern meanings differ;
- do not infer serving-size or packaging semantics from the physical unit alone.

Implementation status: **Pending primary-source metrology verification and a
concrete downstream requirement.**

## Isshobin and other package sizes

Japanese tax statistics and guidance commonly express sake quantities in terms
of 1.8 L bottles. [SA-NTA-PACKAGING-01] A 1.8 L bottle is an ordinary physical
volume plus package identity; it does not require a distinct FermUnits unit.

Ownership:

- use `Q_(1.8, "liter")` for the physical capacity;
- keep `isshobin`, bottle style, nominal fill, and packaging/compliance details
  as application metadata;
- do not define a package name as a universal unit unless a concrete consumer
  later demonstrates that such an alias materially improves interoperability.

Implementation status: **No new FermUnits API required.**

## Implementation priority after migration

The migration identifies only one obviously reusable sake-specific calculation
that is both strongly sourced and plausibly library-shaped: the reversible
Nihonshudo/specific-gravity relationship. Even that should remain unimplemented
until a real FermUnits consumer needs the semantic scale.

If demand appears, the implementation order should be:

1. explicit `specific_gravity_to_nihonshudo()` and inverse functions with the
   `15/4 °C` basis in the contract;
2. only then consider a method-specific sake-acidity helper if an application
   repeatedly needs the prescribed titration calculation;
3. add historical Japanese capacity units only after primary metrology
   verification and collision review.

The legacy Amando formula should not be implemented without a separately
verified published method.

## Sake sources

### [SA-NRIB-METHODS-01] Prescribed analysis methods — sake

- Organization: National Research Institute of Brewing (NRIB)
- Publication: National Tax Agency Prescribed Analysis Methods, Chapter 3,
  `清酒` (sake)
- URL: https://www.nrib.go.jp/bun/pdf/bun/nb03.pdf
- Accessed: 2026-09-03
- Source tier: 2
- Supports:
  - sake specific gravity / Nihonshudo measurement at 15 °C;
  - the `15/4 °C` specific-gravity basis;
  - `nihonshudo = 1443 / S - 1443`;
  - prescribed sake-acidity titration, endpoint, and reporting calculation.

### [SA-NTA-LABEL-01] Manufacturing and quality labeling standard for sake

- Organization: National Tax Agency (Japan)
- Title: `清酒の製法品質表示基準を定める件`
- URL: https://www.nta.go.jp/taxes/sake/hyoji/seishu/kokuji891122/03.htm
- Accessed: 2026-09-03
- Source tier: 1
- Supports:
  - the legal definition of rice polishing ratio;
  - polishing-ratio thresholds used by specially designated sake categories.
- Limitation:
  - category eligibility and labeling compliance are jurisdictional application
    semantics rather than physical-unit definitions.

### [SA-NTA-SWEETNESS-01] Sake Meter Value and sweetness/dryness guidance

- Organization: National Tax Agency (Japan)
- Publication: sake education material on Nihonshudo and sweetness/dryness
- URL: https://www.nta.go.jp/taxes/sake/hambai/moderutekisuto/pdf/r06_07_01.pdf
- Accessed: 2026-09-03
- Source tier: 3
- Supports:
  - Nihonshudo as a sake-specific density scale measured at 15 °C;
  - the `((1 / specific gravity) - 1) × 1443` relationship on the `15/4 °C`
    basis;
  - the limitation that Nihonshudo alone does not determine perceived
    sweetness/dryness.

### [SA-NDL-MEASURES-01] Historical Japanese capacity measures

- Organization: National Diet Library, Collaborative Reference Database
- Title: reference record on `石`, `斗`, `升`, and `合`
- URL: https://crd.ndl.go.jp/reference/entry/reference/show?id=1000076982
- Accessed: 2026-09-03
- Source tier: 7
- Supports:
  - the historical decimal hierarchy of traditional Japanese capacity measures;
  - secondary corroboration of approximately `180.39 L` per koku and the
    historical metric relationship.
- Limitation:
  - secondary reference-service synthesis rather than the primary historical
    weights-and-measures law; exact FermUnits definitions remain pending primary
    verification.

### [SA-NTA-PACKAGING-01] Sake consumption statistics — 1.8 L bottle equivalents

- Organization: National Tax Agency (Japan), Takamatsu Regional Taxation Bureau
- Title: adult per-capita alcohol consumption table
- URL: https://www.nta.go.jp/about/organization/takamatsu/sake/h29/sake_shohi/beppyo_2.htm
- Accessed: 2026-09-03
- Source tier: 3
- Supports:
  - use of 1.8 L bottles as a sake packaging/reporting convention.
- Limitation:
  - does not establish `isshobin` as a physical unit or guarantee one universal
    package specification.
