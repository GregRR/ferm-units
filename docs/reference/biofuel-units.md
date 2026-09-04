# Biofuel Units and Calculations Reference

This document is the maintained biofuel-domain reference for FermUnits. It
supersedes the planning material retained under
[`legacy/biofuel-inventory.txt`](legacy/biofuel-inventory.txt) as the source of
truth for current ownership decisions, implementation status, and
source-verification status.

The Milestone 6 migration does **not** turn the legacy inventory into a feature
checklist. Industrial biofuel calculations mix ordinary flow-rate quantities,
dry-basis feedstock metadata, commodity conventions, fermentation performance
metrics, stoichiometric yield calculations, feedstock composition, and
plant-level process models. Those categories must remain distinct.

## Migration outcome

The legacy biofuel inventory is triaged into five ownership classes:

1. **ordinary compound physical quantities** — dry feed rate, volumetric
   productivity, and specific production rate use existing mass, volume, and
   time units;
2. **commodity and dry-basis conventions** — corn bushels and moisture basis are
   feedstock/reporting semantics rather than new physical dimensions;
3. **dimensionless yield coefficients** — mass yield ratios are ordinary
   dimensionless quantities whose reactant/product identities remain semantic
   metadata;
4. **source-supported stoichiometric calculations** — theoretical
   glucose-to-ethanol yield can be documented as reaction context without
   becoming a multiplicative unit;
5. **rejected or downstream process shortcuts** — fixed corn-to-ethanol yields,
   mislabeled starch factors, and underspecified plant-efficiency equations do
   not become universal FermUnits conversions.

No new public API is added by this migration slice.

## Dry feed mass flow

The legacy inventory proposes a named `DMTh` unit for dry metric tons per hour.
The physical dimension is simply mass flow and is already expressible as, for
example:

```python
from fermunits import Q_

feed_rate = Q_(30, "metric_ton / hour")
```

The word *dry* is not part of the physical unit. It specifies what mass basis was
used for the feedstock. Moisture content therefore belongs with the process or
material record rather than in a unit alias.

Ownership:

- use ordinary `metric_ton / hour`, `kg / s`, or another compatible mass-flow
  expression;
- preserve `dry basis`, `as received`, moisture fraction, sampling method, and
  feedstock identity as process metadata;
- do not define `DMTh` as a new FermUnits unit that would silently imply a
  moisture correction.

Implementation status: **No new FermUnits API required.**

## Corn bushel conventions

USDA ERS uses `1 bushel corn = 56 lb` as a statistical conversion factor.
[BF-USDA-ERS-GRAIN-01] USDA NASS guidance pairs 56 lb/bushel with a 15.5%
moisture guideline and explicitly notes that such standards may vary by firm.
[BF-USDA-NASS-MOISTURE-01]

This must not be confused with Pint's physical volume unit `bushel`. A
commodity bushel expressed as a conventional mass proxy is a feedstock/data
convention, not a new dimension.

Ownership:

- preserve Pint's existing `bushel` volume definition;
- represent commodity quantity or conventional mass using ordinary mass values
  plus explicit commodity/basis metadata;
- if a downstream application needs corn-bushel normalization, make the 56 lb
  convention and moisture basis explicit in that application or in a future
  semantic helper;
- never infer dry matter from a bushel count without an explicit moisture model.

Implementation status: **No new FermUnits unit required.**

### Legacy 15% dry-mass conversion

The legacy inventory hard-codes a 15% moisture basis and the factor
`0.02159 metric_ton/bushel`. The maintained USDA guidance instead uses 15.5% as
a corn moisture guideline and warns that the convention may vary.
[BF-USDA-NASS-MOISTURE-01]

Status: **Rejected as a universal FermUnits conversion.** Dry mass should be
calculated from an explicitly stated as-received mass and moisture fraction.

## Volumetric ethanol productivity

Biofuel fermentation literature commonly reports ethanol volumetric
productivity in `g/L/h`. Tang et al. use that exact dimensional form alongside
ethanol yield in `g/g`. [BF-TANG-2015-01]

This is ordinary mass / volume / time dimensionality:

```python
productivity = Q_(1.2, "gram / liter / hour")
```

Ownership:

- let FermUnits/Pint handle the physical quantity and unit conversion;
- preserve product identity, reactor working volume, averaging interval, batch
  versus continuous basis, and process conditions downstream;
- do not add a named `volumetric_ethanol_productivity` unit merely to abbreviate
  a compound expression.

Implementation status: **No new FermUnits API required.**

## Specific production or fermentation rate

A rate written as `g product / g biomass / h` is dimensionally inverse time, but
the numerator and denominator roles carry essential process meaning. Reducing
the value to a bare frequency must not erase whether the normalization basis was
dry cells, total biomass, substrate, catalyst, or another reference mass.

Ownership:

- use an ordinary compatible quantity such as `gram / gram / hour`;
- keep product identity and normalization basis as semantic metadata;
- do not define a new unit whose name promises a particular biological basis.

Implementation status: **No new FermUnits API required.**

## Ethanol yield coefficients

Yield coefficients such as mass ethanol per mass consumed sugar are ordinary
dimensionless ratios. Tang et al. report measured ethanol yields in `g/g` and
identify a conventional theoretical metabolic yield of approximately
`0.51 g ethanol / g consumed sugar` for the studied sugars.
[BF-TANG-2015-01]

The legacy inventory states `0.5111 g/g` as an exact absolute thermodynamic
limit. The maintained source does not support that precision or that universal
wording. The value is better treated as a reaction/pathway-specific
stoichiometric reference.

Ownership:

- represent measured yield as an ordinary dimensionless quantity;
- preserve substrate identity, product identity, dry/wet basis, conversion
  extent, and measurement scope as metadata;
- if a future consumer needs a theoretical-yield helper, implement an explicit
  reaction-stoichiometry calculation with named substrates/products rather than
  a unit alias.

Implementation status: **No new FermUnits API required today.**

## Corn-to-ethanol yield per bushel

The legacy inventory claims an exact theoretical value of `2.88 US gal` pure
ethanol per dry corn bushel. USDA ERS instead uses `2.7 gallons ethanol per
bushel` as a standard conversion assumption in its biofuels data products.
[BF-USDA-ERS-BIOFUELS-01] That USDA factor is itself a statistical/data-system
assumption, not a universal theoretical physical conversion.

A corn-to-ethanol yield depends on feedstock composition, moisture basis, starch
or fermentable-carbohydrate fraction, conversion efficiency, coproduct/process
losses, and the basis on which ethanol volume is reported.

Status: **Rejected as a universal FermUnits conversion.** Applications may use
explicit empirical or planning factors when their source and scope are retained.

## Legacy starch factor `0.5678`

The legacy plant-efficiency equation describes `0.5678` as a mass multiplier for
*hydrolysis mass gain when starch converts directly to glucose*. That description
conflates hydrolysis with the subsequent glucose-to-ethanol reaction and is not
supported by a maintained source. Hydrolysis basis, starch composition, water
addition, and ethanol stoichiometry must be represented separately.

Status: **Rejected as documented.** If a downstream process model needs
theoretical ethanol yield from starch, it should use an explicit, sourced
reaction-stoichiometry calculation instead of a magic constant.

## Plant conversion efficiency

The legacy inventory proposes:

```text
Plant Efficiency =
    Actual LPA Yield / (DMTh * Substrate_Starch_Percentage * 0.5678) * 100
```

The numerator is not defined on a basis that is dimensionally commensurate with
the denominator, and the equation mixes product volume, feed mass flow,
composition, and an unsupported constant without specifying ethanol density,
time basis, or whether the actual yield is a rate or a feed-normalized yield.

Status: **Rejected as a universal FermUnits calculation.** A valid plant
efficiency model must define actual and theoretical production on the same basis
and explicitly carry feed composition, time interval, ethanol basis, and any
process losses. That is application/process-model semantics unless a repeated
cross-project use case later justifies a dedicated semantic API.

## Implementation priorities

No biofuel-specific implementation is currently justified by this migration. If
a downstream consumer later needs additional behavior, evaluate it in this
order:

1. reuse ordinary FermUnits/Pint compound quantities for feed rates,
   productivity, and yield ratios;
2. keep dry-basis, feedstock, reactor, and commodity conventions explicit in
   application metadata;
3. add a reusable semantic calculation only when the reaction basis and source
   are explicit and more than one consumer needs it;
4. reject fixed feedstock-yield or plant-efficiency shortcuts that hide
   composition, moisture, or dimensional assumptions.

## Sources

### [BF-USDA-ERS-GRAIN-01] Feed Grains Database — conversion factors

- Organization: U.S. Department of Agriculture, Economic Research Service (ERS)
- URL: https://www.ers.usda.gov/data-products/feed-grains-database/documentation
- Accessed: 2026-09-03
- Source tier: 3
- Supports the USDA statistical convention `1 bushel corn = 56 lb`.

### [BF-USDA-NASS-MOISTURE-01] Standard grain weight and moisture guidance

- Organization: U.S. Department of Agriculture, National Agricultural Statistics
  Service (NASS)
- URL: https://www.nass.usda.gov/Surveys/Guide_to_NASS_Surveys/Prices/Chapter%20Two%20Prices%20Received%20v11%2003092015.pdf
- Accessed: 2026-09-03
- Source tier: 3
- Supports the 56 lb/bushel and 15.5% corn moisture guideline while noting that
  such conventions may vary by firm.

### [BF-USDA-ERS-BIOFUELS-01] USDA biofuel conversion-factor data sources

- Organization: U.S. Department of Agriculture, Economic Research Service (ERS)
- URL: https://www.ers.usda.gov/about-ers/partnerships/strengthening-statistics-through-the-icars/biofuels-data-sources
- Accessed: 2026-09-03
- Source tier: 3
- Supports the USDA statistical biofuel factor `1 bushel corn = 2.7 gallons
  ethanol` and the 56 lb/bushel corn convention.

### [BF-TANG-2015-01] Designer synthetic media for microbial-catalyzed biofuel production

- Authors: X. Tang et al.
- Publication: *Biotechnology for Biofuels* 8 (2015), article 1
- DOI: https://doi.org/10.1186/s13068-014-0179-6
- URL: https://www.osti.gov/servlets/purl/1204436
- Accessed: 2026-09-03
- Source tier: 5
- Supports ethanol productivity in `g/L/h`, ethanol yield in `g/g`, and the
  cited conventional theoretical metabolic yield near `0.51 g/g`.
