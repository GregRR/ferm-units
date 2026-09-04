# Acid-tier and other-fermentation reference inventory

This maintained reference replaces the legacy planning material in
[`legacy/acid-tier-inventory.txt`](legacy/acid-tier-inventory.txt). It covers
measurements that recur in cultured dairy, vinegar, kombucha, probiotic, and
other acid-driven fermentations. The legacy inventory is research history, not a
current FermUnits specification.

The migration result is intentionally conservative: no acid-tier-specific public
API is currently justified. Most useful quantities are ordinary Pint/FermUnits
concentrations or fractions, while CFU counts and titratable-acidity results carry
method semantics that must not be hidden inside a unit conversion.

## Ownership summary

| Concept | FermUnits ownership | Status |
|---|---|---|
| CFU per volume | ordinary inverse-volume dimensionality plus assay semantics | Method-defined; no new API |
| Dairy titratable acidity as lactic acid | equivalent-basis analytical result | Method-defined; no new API |
| Acetic-acid concentration / vinegar acid strength | ordinary mass concentration plus product/reporting semantics | No new API |
| Lactic ↔ tartaric acidity shortcut | cross-method reporting conversion | Rejected as universal conversion |
| Volatile-acidity legal/SCOBY claim | application/regulatory claim | Rejected as documented |
| Milk solids-not-fat | ordinary mass fraction plus food-property semantics | No new API |
| Brix-to-acid ratio from °Bx and g/L | application index with incompatible stated bases | Rejected as dimensionless formula |

## Colony-forming units per volume

FDA's current Aerobic Plate Count method reports microbial concentrations in
`CFU/mL` and derives the result from observed colonies, dilution, and the volume
of original sample represented by the inoculum. [AT-FDA-BAM-APC-01]

The legacy description calls a CFU an exact count of live, active cells or cell
clusters. That is too strong. A colony-forming unit is an operational result of a
specified culture method; one colony need not map one-to-one to one individual
cell. Medium, incubation conditions, dilution, plating method, and the target
organism all affect what the result means.

Dimensional behavior is straightforward: once the assay result exists, a
concentration reported per milliliter scales as an inverse-volume quantity. But
FermUnits must not erase the assay identity by pretending CFU is simply a count
of physical particles.

Ownership:

- retain CFU identity and analytical method in application/laboratory metadata;
- use ordinary volume conversion when converting a reported `CFU/mL` result to
  another volume denominator;
- do not define CFU as an exact synonym for cells, organisms, or particles;
- add a semantic CFU type only if a concrete downstream consumer needs method-
  aware arithmetic that ordinary quantity metadata cannot safely express.

Implementation status: **No new FermUnits API required.**

## Yogurt live-culture counts

The current U.S. yogurt standard allows an optional “contains live and active
cultures” statement when the product contains at least `10^7 CFU/g` at
manufacture with a reasonable expectation of `10^6 CFU/g` through the assigned
shelf life. The incorporated method is ISO 7889's colony-count technique.
[AT-US-CFR-YOGURT-01]

These are product-labeling thresholds and method-defined microbiological results,
not new units. FermUnits can support ordinary mass or volume denominator
conversion if a future consumer needs it, but threshold policy belongs in the
consumer application or regulatory layer.

## Dairy titratable acidity as lactic acid

ADPI defines dairy titratable acidity as the lactic-acid stoichiometric
equivalent to the amount of standardized sodium hydroxide required to titrate a
sample to a defined endpoint, realized by phenolphthalein color change or the
equivalent pH 8.3 instrument endpoint. [AT-ADPI-TA-01]

That definition is important because “% lactic acid” in this context is a
**reporting basis for a titration result**, not necessarily the measured mass
fraction of molecular lactic acid actually present in the sample. Buffering and
other titratable species contribute to the result.

The current U.S. yogurt standard no longer sets yogurt identity through a
minimum titratable-acidity requirement; it requires pH 4.6 or lower.
[AT-US-CFR-YOGURT-01] Other jurisdictions and analytical programs may still use
titratable acidity, so the reporting basis remains legitimate but must retain its
method context.

Ownership:

- represent a reported percent or mass concentration with ordinary
  FermUnits/Pint quantity behavior when the reporting basis is explicit;
- keep sample preparation, titrant standardization, endpoint, and “as lactic
  acid” semantics with the analytical result;
- use FermUnits' existing equivalents/amount-concentration helpers for explicit
  stoichiometric transformations when the required reaction basis and molar mass
  are supplied;
- do not add a bare `percent_ta_lactic` unit that would hide method semantics.

Implementation status: **No new FermUnits API required.**

## Cross-acid titratable-acidity conversions

The legacy inventory gives fixed relationships:

```text
Tartaric Acid (g/L) = Lactic Acid (g/L) * 0.833
Lactic Acid (g/L) = Tartaric Acid (g/L) * 1.200
```

Those numbers resemble conversions between acid-equivalent reporting bases, but
titratable acidity is not a direct molecular assay and equivalence depends on the
specified reaction or charge relationship. [SC-IUPAC-01] The conversion therefore
cannot be treated as a universal identity between actual lactic-acid and
tartaric-acid concentrations.

Status: **Rejected as a universal FermUnits conversion.** If an application must
translate a titration result between explicitly defined equivalent-mass reporting
bases, it should do so through an explicit stoichiometric/equivalent calculation
whose source, endpoint, and acid basis are retained.

## Acetic-acid concentration and vinegar acid strength

FDA's vinegar labeling policy describes named vinegars as normally containing at
least `4 g acetic acid / 100 mL` at 20 °C. [AT-FDA-VINEGAR-01] That value is a
product/reporting convention over an ordinary mass concentration. FDA also notes
that no federal vinegar standard of identity has been established under the
Federal Food, Drug, and Cosmetic Act.

Ownership:

- represent acetic-acid concentration with ordinary mass-concentration units;
- keep the analyte identity, analytical method, product type, temperature basis,
  and jurisdiction with the result or application policy;
- do not define “vinegar acidity” as a new physical unit.

Implementation status: **No new FermUnits API required.**

## Volatile acidity and kombucha regulation

The legacy inventory states that volatile acidity is legally required to monitor
SCOBY health and to ensure kombucha does not produce unauthorized alcohol. The
maintained sources do not support that claim.

TTB's U.S. federal kombucha guidance focuses on **alcohol by volume**: if kombucha
reaches 0.5% ABV or more during production, at bottling, or after bottling, the
product is subject to TTB alcohol regulation. TTB discusses direct alcohol
analysis methods for this purpose. [AT-TTB-KOMBUCHA-01]

Volatile acidity can be a legitimate analytical property in some fermented
products, but its method, analyte-equivalent basis, and regulatory meaning are
domain-specific. A generic acetic-acid mass concentration is not automatically a
volatile-acidity measurement, and volatile acidity is not a substitute for ABV.

Status: **Rejected as documented.** No FermUnits conversion should encode the
legacy legal/SCOBY assertion.

## Milk solids-not-fat

The current U.S. yogurt standard requires at least 8.25% milk solids not fat and
incorporates AOAC methods under which milk solids not fat are calculated by
difference between total solids and milkfat. [AT-US-CFR-YOGURT-01]

The physical arithmetic is an ordinary mass fraction:

```text
solids-not-fat fraction = (total solids mass - fat mass) / sample mass
```

The property name and regulatory threshold are food/product semantics rather
than a distinct unit.

Implementation status: **No new FermUnits API required.** A consumer should use
ordinary mass-fraction quantities and retain the measured-property identity and
method alongside the value.

## Brix-to-acid ratio

The legacy inventory proposes:

```text
BAR = °Brix / Total Acidity (g/L)
```

and calls the result dimensionless. As written, that is dimensionally
inconsistent: Brix is a dimension-one sucrose mass-fraction scale, while `g/L`
is mass concentration. [SH-OIML-01] Their quotient is not dimensionless.

Soluble-solids-to-acidity indices can be useful application-level quality or
sensory metrics when both inputs, their reporting bases, and the intended ratio
are explicitly defined. But FermUnits should not canonize an underspecified
“BAR” formula whose units depend on how acidity is reported.

Status: **Rejected as written.** A downstream application may calculate an
explicitly defined ratio after normalizing both inputs to compatible bases.

## Implementation priorities

No acid-tier-specific implementation is currently justified by this migration.
If a downstream consumer later needs additional behavior, evaluate it in this
order:

1. reuse ordinary FermUnits/Pint quantities for mass concentration, mass
   fraction, pH, and denominator-volume conversion;
2. preserve analytical method, analyte/equivalent basis, endpoint, product type,
   and jurisdiction as semantic metadata;
3. use existing solution-chemistry equivalent/amount APIs when a reaction basis
   is explicit rather than introducing fixed cross-acid shortcuts;
4. add a dedicated semantic result type only when a concrete consumer cannot
   safely preserve the required method semantics otherwise.

## Sources

### [AT-FDA-BAM-APC-01] FDA BAM Chapter 3 — Aerobic Plate Count

- Organization: U.S. Food and Drug Administration (FDA)
- URL: https://www.fda.gov/food/laboratory-methods-food/bam-chapter-3-aerobic-plate-count
- Accessed: 2026-09-04
- Source tier: 2
- Supports CFU/mL as a culture-method result derived from colony count, dilution,
  and represented original sample volume.

### [AT-US-CFR-YOGURT-01] 21 CFR 131.200 — Yogurt

- Organization: U.S. Food and Drug Administration (FDA)
- URL: https://www.ecfr.gov/current/title-21/chapter-I/subchapter-B/part-131/subpart-B/section-131.200
- Accessed: 2026-09-04
- Source tier: 1
- Supports current U.S. yogurt pH, milk-solids-not-fat, and live-culture
  provisions and the incorporated analytical methods.

### [AT-ADPI-TA-01] ADPI Analytical Method 007 — Titratable Acidity

- Organization: American Dairy Products Institute (ADPI)
- URL: https://adpi.org/methodsofanalysis/analytical-method-007/
- Accessed: 2026-09-04
- Source tier: 4
- Supports dairy titratable acidity as a method-defined lactic-acid
  stoichiometric equivalent with a defined endpoint.

### [AT-FDA-VINEGAR-01] FDA vinegar definitions and acid-strength policy

- Organization: U.S. Food and Drug Administration (FDA)
- URL: https://www.fda.gov/regulatory-information/search-fda-guidance-documents/cpg-sec-525825-vinegar-definitions-adulteration-vinegar-eels
- Accessed: 2026-09-04
- Source tier: 3
- Supports FDA vinegar labeling-policy guidance using acetic-acid strength at
  20 °C.

### [AT-TTB-KOMBUCHA-01] TTB kombucha alcohol-regulation guidance

- Organization: Alcohol and Tobacco Tax and Trade Bureau (TTB)
- URL: https://www.ttb.gov/regulated-commodities/beverage-alcohol/kombucha
- Accessed: 2026-09-04
- Source tier: 3
- Supports the 0.5% ABV regulatory threshold and the role of alcohol-content
  measurement in U.S. federal kombucha compliance.
