# Distilling Units and Calculations Reference

This document is the maintained distilling-domain reference for FermUnits. It
supersedes the planning material retained under
[`legacy/distilling-inventory.txt`](legacy/distilling-inventory.txt) as the
source of truth for current ownership decisions, implementation status, and
source-verification status.

The Milestone 6 migration does **not** turn the legacy inventory into a feature
checklist. Distilling combines ordinary physical quantities with legal proof and
taxation semantics, metrological alcoholometry, table-driven gauging, and highly
variable vessel terminology. Those categories must remain distinct.

## Migration outcome

The legacy distilling inventory is triaged into six ownership classes:

1. **ordinary Pint quantities** — volume, mass, density, temperature, and
   dimension-one fractions remain ordinary Pint/FermUnits quantities;
2. **jurisdiction-defined semantic scales** — proof and related legal alcohol
   strength conventions require their reference temperature and jurisdiction;
3. **legal accounting quantities** — proof gallons and litres of pure alcohol
   are reporting/tax calculations over physical quantities, not universal
   multiplicative units;
4. **metrological/table-driven calculations** — alcoholometry and temperature
   correction depend on authoritative tables, density relationships, and
   measurement conditions;
5. **application/process calculations** — dilution planning, tank management,
   tax reporting, and compliance remain downstream unless a reusable,
   well-sourced semantic transformation is later justified;
6. **pending, ambiguous, or rejected legacy claims** — historical scales and
   vessel-size shortcuts are not implemented without stronger definition and
   scope.

No new public API is added by this migration slice.

## Alcoholic strength by volume

Alcoholic strength by volume is a dimension-one composition quantity, but its
reported value depends on a reference temperature and an alcoholometry system.
OIML R 44 describes volume alcoholometers and specifies a 20 °C reference
condition in accordance with OIML R 22 International Alcoholometric Tables.
[DI-OIML-R22-01] [DI-OIML-R44-01]

Ownership:

- represent the numeric fraction with an ordinary FermUnits/Pint dimensionless
  quantity;
- preserve the reference temperature, method/table, sample basis, uncertainty,
  and reporting precision as measurement metadata;
- do not create a universal `abv` multiplicative unit that silently erases the
  reference condition.

Implementation status: **No new FermUnits API required.**

## U.S. proof

For U.S. distilled-spirits regulation, proof is the ethyl-alcohol content at
60 °F stated as twice the percentage of ethyl alcohol by volume. TTB guidance
therefore gives the familiar relationship `proof = 2 × ABV-percent` within that
legal reference system. [DI-US-TTB-PROOF-01] [DI-US-27CFR-GAUGING-01]

Proof is a semantic scale, not an ordinary physical unit identity. The same
numeric ABV value reported under a different reference-temperature convention
must not be silently treated as U.S. proof without reconciling the measurement
basis.

Ownership:

- keep U.S. proof jurisdiction-qualified and tied to the 60 °F legal basis;
- if a downstream consumer later needs proof conversions, prefer explicit
  semantic functions over a Pint unit alias;
- require the caller or input contract to make the reference basis explicit
  when converting from a measured alcohol-strength result.

Implementation status: **Not implemented; source-ready if a real consumer needs
an explicit U.S.-proof API.**

## Proof gallons

U.S. law defines a proof gallon as one U.S. gallon of liquid at 60 °F containing
50 percent by volume ethyl alcohol of the specified reference density, or the
alcoholic equivalent. TTB guidance calculates proof gallons from bulk gallons
and proof. [DI-US-TTB-PROOF-01] [DI-US-27CFR-GAUGING-01]

For a quantity already expressed as wine gallons at the required basis, the
accounting relationship is:

```text
proof gallons = wine gallons × proof / 100
```

This is a legal alcohol-content accounting quantity, not simply a replacement
name for an ordinary gallon. Real tax/compliance work also depends on TTB gauging
procedures, rounding, obscuration handling, and table use. [DI-US-TTB-GAUGING-01]

Ownership:

- ordinary volume remains a Pint quantity;
- proof is a jurisdiction-defined semantic input;
- proof-gallon calculation belongs in an explicit semantic function if a
  downstream consumer demonstrates a reusable need;
- tax rates, filing rules, and compliance decisions remain downstream.

Implementation status: **Not implemented; no current downstream requirement.**

### Wine gallon / bulk gallon

In the U.S. distilled-spirits regulations, `gallon` or `wine gallon` is the
liquid measure equivalent to 231 cubic inches. That is ordinary U.S. liquid
volume, already represented by Pint/FermUnits. [DI-US-27CFR-GAUGING-01]

Implementation status: **No new alias required.** The legal reporting label
`wine gallon` should remain application/compliance metadata rather than a second
physical gallon definition.

## Litres of pure alcohol

Current UK Alcohol Duty is calculated using litres of pure alcohol in the
product. HMRC examples determine the value from bulk litres and ABV before
applying the duty rate. [DI-UK-HMRC-LPA-01]

The physical result is a volume of ethanol. The phrase *litres of pure alcohol*
is an accounting/reporting basis, not a new dimension.

Ownership:

- represent the numeric result as ordinary litres;
- preserve jurisdiction, alcohol-strength basis, and duty/reporting context
  downstream;
- do not create an `LPA` or `LAA` unit alias merely to rename `liter`.

Implementation status: **No new FermUnits API required.** A future reusable
calculation may be considered only if a consumer needs explicit alcohol-content
accounting semantics.

## Alcoholometry and temperature correction

Alcohol-strength measurements are temperature-sensitive. OIML R 22 provides
international alcoholometric tables relating density, alcoholic strength by
mass, alcoholic strength by volume, and temperature. OIML R 44 specifies
alcoholometers at a 20 °C reference temperature. [DI-OIML-R22-01]
[DI-OIML-R44-01]

For U.S. legal gauging, TTB Table 1 is used to ascertain proof at 60 °F from
corrected hydrometer and thermometer readings, with interpolation when the
readings fall between tabulated values. [DI-US-TTB-GAUGING-01]

### Legacy linear proof-temperature correction

The legacy inventory proposes:

```text
true proof = apparent proof - 0.05 × (temperature °F - 60)
```

That shortcut is not the TTB legal gauging procedure and does not preserve the
nonlinear density/temperature behavior represented by the authoritative tables.

Status: **Rejected as a universal FermUnits conversion and as a substitute for
TTB legal gauging.**

A future alcoholometry API would need an explicit table/model source, supported
range, reference temperature, composition assumptions, interpolation rules, and
validation strategy.

## Dilution and ethanol-water volume contraction

Ethanol-water mixture volumes are not generally additive. A target-strength
calculation therefore cannot assume that adding the component volumes linearly
will produce the final bulk volume.

OIML R 22 provides density/alcohol-strength relationships for ethanol-water
mixtures. TTB's Gauging Manual includes table-driven methods for determining
quantities and, in Table 4, a weight-based procedure for determining water
required to reduce spirits to a target proof. [DI-OIML-R22-01]
[DI-US-TTB-GAUGING-01]

Ownership:

- plain volume and mass units remain Pint quantities;
- a physically rigorous dilution model belongs in FermUnits only if it can be
  defined as a reusable, validated ethanol-water transformation rather than an
  application recipe;
- legal TTB reduction calculations must retain their regulatory table and
  rounding semantics;
- process goals, losses, blend sequencing, and equipment constraints remain
  downstream.

Implementation status: **No generic dilution helper in this migration slice.**

## Historical British proof / Sykes scale

The legacy inventory records British/Sykes proof and fixed conversions such as
`UK proof = ABV × 1.7535`. Historical proof systems are legitimate research
subjects, but the maintained project does not yet have a sufficiently direct
source establishing the exact numerical conversion, temperature basis,
hydrometer definition, and historical scope needed for a stable FermUnits API.

Status: **Pending.** Do not implement the legacy `1.7535` or `0.8767` factors as
universal conversions.

## Gay-Lussac / degree GL

The legacy inventory describes degrees Gay-Lussac as ABV on a 15 °C reference
basis. The maintained OIML sources directly support modern alcoholic strength by
volume and 20 °C alcoholometry, but they do not by themselves establish the
legacy `°GL` label, its historical reference temperature, or all regional uses.

Status: **Pending authoritative historical/jurisdictional verification.** Do not
create a `degree_GL` alias from the legacy description alone.

## Distilling barrels and casks

Barrel names are especially poor candidates for unqualified unit definitions.
The legacy inventory assigns exact capacities to a bourbon barrel, whisky
hogshead, quarter cask, octave cask, and gorda, then derives a fixed conversion
matrix between them.

TTB whisky rules require specified products such as bourbon to be stored in new
charred oak containers, but they do not define bourbon identity by a universal
53 U.S.-gallon barrel capacity. [DI-US-TTB-WHISKY-01]

Ownership:

- do not define bare `bourbon_barrel`, `whisky_hogshead`, `quarter_cask`,
  `octave_cask`, or `gorda` from the legacy capacities without authoritative
  region/trade definitions;
- do not infer exact cask-to-cask ratios from nominal industry sizes;
- preserve ordinary Pint `barrel`/`hogshead` meanings and use qualified names
  only when a real consumer needs a separately sourced distilling definition.

### Legacy 53-gallon bourbon-barrel claim

A 53 U.S.-gallon cask is a common industry size, but the maintained regulatory
source does not make 53 gallons the defining legal capacity of a bourbon barrel.

Status: **Rejected as a universal regulatory unit definition.** A future
industry-qualified physical unit would require a source that directly defines
that commercial capacity and a demonstrated downstream need.

### Hogshead, quarter cask, octave, and gorda

The maintained sources in this migration do not establish one universal volume
for these names across whisky, rum, fortified-wine, and historical contexts.
Some overlap with already documented wine terminology further demonstrates the
collision risk.

Status: **Pending/Ambiguous.** No new registry definitions.

## Implementation priorities

No distilling-specific implementation is currently justified by this migration.
If a downstream consumer later needs additional behavior, evaluate it in this
order:

1. reuse ordinary FermUnits/Pint quantities for volume, mass, density,
   temperature, and fraction;
2. add explicit jurisdiction-qualified semantic functions for proof or proof-
   gallon calculations only when their reference conditions and rounding rules
   are part of the API contract;
3. consider alcoholometry/dilution only with an authoritative model or table and
   a clearly defined supported range;
4. keep tax rates, filings, operational blending, equipment, and compliance
   policy downstream;
5. add qualified cask units only when both an authoritative capacity and a real
   consumer need exist.

## Sources

### [DI-US-TTB-PROOF-01] Distilled Spirits FAQs — proof and proof gallons

- Organization: Alcohol and Tobacco Tax and Trade Bureau (TTB)
- URL: https://www.ttb.gov/distilled-spirits/distilled-spirits-faqs/print
- Accessed: 2026-09-03
- Source tier: 2
- Supports U.S. proof as twice ABV and the bulk-gallon/proof-gallon accounting
  relationship.

### [DI-US-27CFR-GAUGING-01] 27 CFR Parts 19 and 30 — distilled spirits and gauging

- Organization: United States Department of the Treasury / TTB
- Citations: 27 CFR § 19.1; 27 CFR Part 30
- URL: https://www.ecfr.gov/current/title-27/chapter-I/subchapter-A/part-30
- Accessed: 2026-09-03
- Source tier: 1
- Supports the legal 60 °F basis for proof, proof-gallon and wine-gallon
  terminology, and the federal gauging framework.

### [DI-US-TTB-GAUGING-01] TTB Gauging Manual and proof interpolation guidance

- Organization: Alcohol and Tobacco Tax and Trade Bureau (TTB)
- URL: https://www.ttb.gov/regulated-commodities/beverage-alcohol/distilled-spirits/laws-regulations-and-public-guidance
- Related guidance: https://www.ttb.gov/regulated-commodities/beverage-alcohol/distilled-spirits/proofing-page-interpolation-table
- Accessed: 2026-09-03
- Source tier: 2
- Supports use of the Gauging Manual tables, temperature correction to 60 °F,
  interpolation, apparent/true proof distinctions, and table-driven quantity
  calculations.

### [DI-OIML-R22-01] OIML R 22 — International Alcoholometric Tables

- Organization: International Organization of Legal Metrology (OIML)
- Publication: OIML R 22, International Alcoholometric Tables
- URL: https://www.oiml.org/en/files/pdf_r/r022-e75.pdf
- Accessed: 2026-09-03
- Source tier: 1
- Supports international density/alcohol-strength relationships for ethanol-
  water mixtures and alcoholometry as a temperature-dependent metrological
  calculation.

### [DI-OIML-R44-01] OIML R 44 — Alcoholometers and alcohol hydrometers

- Organization: International Organization of Legal Metrology (OIML)
- Publication: OIML R 44, Edition 1985 (E)
- URL: https://www.oiml.org/en/files/pdf_r/r044-e85.pdf
- Accessed: 2026-09-03
- Source tier: 1
- Supports percentage alcoholic strength by mass/volume and the 20 °C reference
  condition for OIML alcoholometers.

### [DI-UK-HMRC-LPA-01] Work out how much Alcohol Duty you need to pay

- Organization: HM Revenue & Customs
- URL: https://www.gov.uk/guidance/work-out-how-much-alcohol-duty-you-need-to-pay
- Accessed: 2026-09-03
- Source tier: 1
- Supports current UK duty calculation in litres of pure alcohol and examples
  calculating pure-alcohol litres from bulk litres and ABV.

### [DI-US-TTB-WHISKY-01] TTB whisky guidance — barreling requirements

- Organization: Alcohol and Tobacco Tax and Trade Bureau (TTB)
- Publication: Whisky webinar / distilled-spirits guidance
- URL: https://www.ttb.gov/images/pdfs/whisky-webinar.pdf
- Accessed: 2026-09-03
- Source tier: 2
- Supports new-charred-oak storage requirements for bourbon and related whisky
  classes; does not define a universal 53-gallon legal barrel capacity.
