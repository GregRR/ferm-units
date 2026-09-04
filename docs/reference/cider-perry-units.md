# Cider and Perry Units and Calculations Reference

This document is the maintained cider/perry-domain reference for FermUnits. It
supersedes the planning material retained under
[`legacy/cider-perry-inventory.txt`](legacy/cider-perry-inventory.txt) as the
source of truth for current ownership decisions, implementation status, and
source-verification status.

The Milestone 6 migration does **not** turn the legacy inventory into a feature
checklist. Most cider/perry measurements in that inventory are ordinary physical
quantities, existing FermUnits semantics, analytical reporting conventions, or
application-level classifications rather than new units.

## Migration outcome

The legacy cider/perry inventory is triaged into five ownership classes:

1. **ordinary Pint quantities** — use Pint through FermUnits without adding a
   new alias;
2. **existing FermUnits semantic behavior** — reuse current FermUnits APIs such
   as `PHValue`, gravity points, and solution-chemistry conversions;
3. **method-defined reporting bases** — preserve the analytical method and
   reporting basis rather than treating the label as a universal unit;
4. **application-level classifications and process models** — keep these
   downstream unless a reusable, well-sourced FermUnits semantic API is later
   justified;
5. **pending or rejected legacy formulas** — do not implement unsupported or
   over-generalized relationships.

No new public API is added by this migration slice.

## Sorbitol concentration

Sorbitol concentration is an ordinary mass-per-volume quantity, normally
reported in `g/L`. Peer-reviewed cider work measures residual sorbitol directly
and shows that its behavior can vary with cultivar and fermentation organism.
[CP-SORBITOL-01]

Ownership:

- represent sorbitol concentration with an ordinary FermUnits/Pint quantity, for
  example `Q_(3.0, "g/L")`;
- keep analyte identity (`sorbitol`) as application/report metadata;
- do not add a dedicated `sorbitol_g_per_liter` unit.

Implementation status: **No new FermUnits API required.**

### Legacy sorbitol attenuation correction

The legacy inventory proposes a "true fruit attenuation" equation containing a
fixed `Sorbitol_GU` contribution of roughly 0.0037 specific-gravity points per
`g/L` sorbitol. The maintained sources do not establish that constant as a
universal relationship. Sorbitol concentration and its fermentation behavior are
composition- and organism-dependent, and converting a solute mass concentration
to solution density requires an explicit solution model. [CP-SORBITOL-01]

Status: **Rejected as a universal FermUnits conversion.** A future downstream
process model would need an explicit density/composition basis and validation.

## pH

Cider pH uses the existing FermUnits `PHValue` semantic type. Cornell AgriTech
identifies pH as a routine hard-cider analysis. [CP-CORNELL-ANALYSIS-01]

Ownership:

- use `PHValue` for the pH value itself;
- preserve instrument, calibration, temperature, and sample metadata downstream;
- do not create a cider-specific pH unit.

Implementation status: **Already supported by FermUnits.**

## Titratable acidity as malic acid equivalents

Cornell AgriTech reports cider titratable acidity as `g/L` malic-acid
equivalents using an autotitration endpoint of pH 8.2. [CP-CORNELL-ANALYSIS-01]
Penn State likewise reports titratable malic acid in `g/L` in cider-fruit
chemistry. [CP-PSU-CHEMISTRY-01]

The physical result is a mass concentration, but "as malic acid" is an
**analytical reporting basis**, not a distinct physical dimension. The endpoint
and method belong to the measurement record.

Ownership:

- use ordinary mass concentration for the numeric quantity;
- preserve `as malic acid`, titration endpoint, and method as semantic metadata;
- when a calculation genuinely starts from an equivalent concentration, the
  existing FermUnits solution-chemistry APIs may convert between equivalent and
  mass-concentration bases using explicit molar mass and equivalents-per-mole.

Implementation status: **No cider-specific unit required.**

### Legacy malic/tartaric TA conversion factors

The legacy inventory gives fixed multipliers `1.119` and `0.893` for converting
between malic- and tartaric-acid TA reporting. Those numbers approximate a
change of acid mass basis, but a measured TA value is method-defined. Wine and
cider methods can use different endpoints and procedures, so the factors must
not be presented as a universal conversion between independently measured TA
results.

Status: **Rejected as a universal direct conversion.** If a caller has one
underlying equivalent concentration and merely needs a different mass-equivalent
reporting basis, use the explicit solution-chemistry conversion functions with
the appropriate molar mass and stoichiometric factor instead.

## Phenolics and tannin reporting

Cider fruit chemistry commonly measures tannin or total polyphenols, but the
reported number depends on analytical method and reference standard. Penn State,
for example, reports total polyphenols using the Folin-Ciocalteu method in gallic
acid equivalents. [CP-PSU-CHEMISTRY-01]

Ownership:

- the numeric result may be an ordinary mass concentration or mass fraction;
- analyte class, assay, calibration/reference compound, and reporting basis are
  required semantic metadata;
- do not define a universal `tannin_percent` unit that erases method identity.

Implementation status: **No new FermUnits API required.**

## Long Ashton cider-apple classification

A commonly cited Long Ashton Research Station classification divides cider
apples into sweet, sharp, bittersweet, and bittersharp categories using acid and
tannin thresholds. A Cornell historical review gives thresholds of 4.5 g/L acid
and 2.0 g/L tannins and notes continuing use of the scheme.
[CP-CORNELL-LARS-01]

The legacy inventory instead used a 0.18% tannin threshold. That value is not
supported by the maintained source and should not be carried forward.

Ownership:

- this is **classification logic**, not a unit conversion;
- acid and tannin measurement methods/reporting bases must be explicit before a
  classification result is reproducible;
- if a future cider application needs the classifier, implement it downstream
  first or propose a separate FermUnits semantic API with direct primary-source
  verification.

Source status: **Provisional** pending direct review of the original Long Ashton
source and a precise analytical-method contract.

Implementation status: **Downstream; not implemented in FermUnits.**

## Press yield

`L/metric_ton` and `US_liquid_gallon/short_ton` are ordinary volume-per-mass
quantities already expressible through the FermUnits registry. Pint performs the
unit conversion directly, so FermUnits does not need named cider-specific yield
units or a hard-coded conversion factor.

Example:

```python
from fermunits import Q_

yield_value = Q_(700, "liter / metric_ton")
print(yield_value.to("US_liquid_gallon / short_ton"))
```

The legacy fixed factor `4.1725` is a rounded duplicate of ordinary unit
conversion and should not become API. Likewise, the claimed industrial baseline
of 700–750 L/t remains **Pending** because the legacy inventory did not supply an
authoritative source and the value is process/equipment dependent.

Implementation status: **No new FermUnits API required.**

## Legal cider/perry definitions

Government definitions of cider and perry can constrain juice content, alcohol
strength, ingredients, and reference conditions. HMRC's current alcohol-products
guidance is one example. [CP-HMRC-CIDER-01]

These are product-classification and compliance semantics, not physical unit
definitions. FermUnits may represent the underlying quantities, but jurisdiction,
product class, and compliance decisions belong downstream.

Implementation status: **Downstream policy; no FermUnits API.**

## Deferred cider/perry topics

The legacy inventory header mentions sulfur-dioxide management, but it does not
provide a complete cider/perry-specific method or formula. Existing wine and
solution-chemistry references already establish that sulfur reporting and
molecular-speciation calculations require explicit analytical/process context.
No cider-specific sulfur API should be inferred from the legacy heading alone.

## Implementation priorities

No cider/perry-specific implementation is currently justified by this migration.
If a downstream consumer later needs additional behavior, evaluate it in this
order:

1. reuse ordinary FermUnits/Pint quantities and existing semantic APIs;
2. add a reusable semantic calculation only when the method, reporting basis,
   and source are explicit;
3. keep jurisdictional classifications and process models downstream;
4. reject fixed shortcuts that silently erase measurement or composition
   assumptions.

## Sources

### [CP-CORNELL-ANALYSIS-01] Wine and Hard Cider Lab Analysis

- Organization: Cornell AgriTech, Cornell University
- URL: https://cals.cornell.edu/cornell-agritech/our-expertise/craft-beverage-production/craft-beverage-analytical-lab/wine-hard-cider-analyses
- Accessed: 2026-09-03
- Source tier: 4
- Supports cider pH, fermentable sugar, alcohol, and TA reported as malic-acid
  equivalents with the cited pH 8.2 endpoint.

### [CP-PSU-CHEMISTRY-01] Using Mid-Atlantic Processing Fruit in Hard Cider Production

- Organization: Penn State Extension
- URL: https://extension.psu.edu/using-mid-atlantic-processing-fruit-in-hard-cider-production
- Accessed: 2026-09-03
- Source tier: 4
- Supports cider-fruit malic acid, pH, sugar, and method-specific
  tannin/polyphenol reporting.

### [CP-CORNELL-LARS-01] Characterization of Malus genotypes within the USDA-PGRU

- Organization: Cornell University
- URL: https://ecommons.cornell.edu/bitstreams/aac7e7a0-7bdf-4541-939d-70208a5f3046/download
- Accessed: 2026-09-03
- Source tier: 6
- Supports secondary documentation of the Long Ashton category structure and
  4.5 g/L acid / 2.0 g/L tannin thresholds.
- Limitation: original primary source still needs direct review.

### [CP-HMRC-CIDER-01] Alcoholic products technical guide — cider and perry

- Organization: HM Revenue & Customs
- URL: https://www.gov.uk/guidance/alcoholic-products-technical-guide/section-2-alcoholic-products
- Accessed: 2026-09-03
- Source tier: 1
- Supports jurisdiction-specific cider/perry product and ingredient rules.

### [CP-SORBITOL-01] Effect of yeast fermentation on cider chemical composition

- Publication: Food Bioscience (2026), article 108699
- DOI: https://doi.org/10.1016/j.fbio.2026.108699
- URL: https://www.sciencedirect.com/science/article/pii/S2212429226004712
- Accessed: 2026-09-03
- Source tier: 5
- Supports sorbitol as a measured cider constituent and residual sorbitol in the
  studied fermentations; does not establish a universal gravity correction.
