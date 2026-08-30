# Brewing Units and Calculations Reference

This document is the maintained brewing reference for current FermUnits
behavior. It supersedes the original planning inventory retained under
[`legacy/brewing-inventory.txt`](legacy/brewing-inventory.txt).

Implementation status and source-verification status are intentionally separate.
Detailed ASBC/EBC questions are tracked in
[`../asbc-verification.md`](../asbc-verification.md), and shared source records
are defined in [`../sources.md`](../sources.md).

## Physical vessel units

Pint's existing unit names are preserved when they have a legitimate meaning.
FermUnits adds qualified names where brewing terminology would otherwise collide
with Pint or another fermentation domain.

| FermUnits name | Definition | Implementation status | Source status |
|---|---|---|---|
| `us_beer_barrel` | alias of Pint `beer_barrel` = 31 US liquid gallons | Implemented | Pint behavior verified via [SH-PINT-01] |
| `imperial_beer_barrel` | 36 Imperial gallons | Implemented | Domain-source verification pending |
| `pin_cask` | 4.5 Imperial gallons | Implemented | Domain-source verification pending |
| `firkin` | 9 Imperial gallons | Implemented | Domain-source verification pending |
| `kilderkin` | 18 Imperial gallons | Implemented | Domain-source verification pending |
| `brewing_hogshead` | 54 Imperial gallons | Implemented | Domain-source verification pending |
| `brewing_puncheon` | 72 Imperial gallons | Implemented | Domain-source verification pending |
| `brewing_butt` | 108 Imperial gallons | Implemented | Domain-source verification pending |
| `wine_hogshead` | alias of Pint `hogshead` | Implemented for explicit disambiguation | See [wine-units.md](wine-units.md) |

Bare `barrel`, `hogshead`, `puncheon`, and `butt` are not given new universal
brewing meanings when a legitimate Pint or cross-domain meaning would be
changed or obscured.

## Gravity and extract

### Specific gravity and gravity points

Public functions:

- `sg_to_gravity_points`
- `gravity_points_to_sg`

Implemented relationship:

```text
GU = (SG - 1) * 1000
SG = 1 + GU / 1000
```

Specific gravity is treated as a dimensionless ratio. The numeric value does not
encode reference temperature. The gravity-points arithmetic is independently
documented as brewing shorthand by the Canadian Homebrewers Association,
including the example `1.046 = 46` gravity points. [BR-CHA-GU-2021]

FermUnits applies the formula algebraically below SG 1.000 as well, so SG
`0.998` maps to `-2` gravity points. The cited brewing-practice source does not
independently standardize that below-1.000 extension.

Status: **Implemented; the ordinary gravity-points convention is sourced as
brewing shorthand, while the below-1.000 extension, ASBC terminology, and
specific-gravity reference-condition verification remain pending.**

### Specific gravity and degrees Plato

Public functions:

- `sg_to_plato`
- `plato_to_sg`

The current SG-to-Plato polynomial is:

```text
°P = -616.868 + 1111.14(SG) - 630.272(SG²) + 135.997(SG³)
```

`plato_to_sg` numerically inverts that same polynomial rather than using an
independent approximate inverse. This preserves round-trip consistency.

Quek et al. (2019) reproduce the exact implemented coefficients in a
peer-reviewed brewing paper and identify the equation as a formula from the
American Society of Brewing Chemists. [BR-QUEK-2019] This is substantially
stronger support than the legacy inventory provided, but it is still secondary
evidence for the primary ASBC table or method.

Recent JASBC work by Buhl (2024) independently confirms that ASBC extract
tables are used as reference data when evaluating equations relating relative
density and percent-by-mass extract. [BR-BUHL-2024] It does not establish the
provenance of the implemented cubic.

A 1984 JASBC item titled *Statistical Analysis* was identified as a possible
historical lead during this review, but the accessible journal metadata does not
expose the equation or enough article text to establish it as the source of the
coefficients. It therefore remains a verification lead rather than a supporting
source record.

Status: **Implemented provisionally; the exact polynomial is independently
reproduced in peer-reviewed brewing literature with ASBC attribution, while the
primary ASBC source, reference conditions, scientific validity range, and full
precision qualification remain direct verification items.**

The numerical SG search interval used by the inverse is an implementation limit,
not an asserted scientific range. The inverse itself is a FermUnits numerical
implementation choice: it solves the published forward polynomial rather than
claiming a separately standardized Plato-to-SG equation.

### Brix, Plato, and Balling

FermUnits does not provide a generic Brix-to-Plato conversion and does not
currently provide separate Balling functions. These scales have distinct
historical and analytical contexts and are not treated as interchangeable unit
aliases.

A peer-reviewed laboratory brewing protocol describes degrees Plato as the
mass percentage of dissolved solids in wort by reference to the density of an
equivalent sucrose solution. [BR-THESSELING-2019] OIML guidance separately
anchors Brix to sucrose mass-fraction/refractometer practice. [SH-OIML-01]
These related measurement traditions are enough to support keeping the names
semantically distinct rather than defining a universal arithmetic conversion.

Status: **Not implemented by design; the modern Plato and Brix meanings are
sourced, while historical Balling details and any stated cross-scale tolerance
remain verification pending.**

### Wort refractometer correction

Public functions:

- `wort_refractometer_brix_to_plato`
- `plato_to_wort_refractometer_brix`

Implemented relationship:

```text
corrected Plato = apparent Brix / wort correction factor
apparent Brix = Plato * wort correction factor
```

The wort correction factor is required explicitly. FermUnits does not define a
default correction factor, and these functions are not represented as generic
Brix/Plato scale conversions.

The current M3 review found no authoritative support for a universal wort
correction factor. OIML's Brix treatment is tied to sucrose/refractometer
measurement conditions rather than to a universal wort composition, so the
caller-supplied-factor boundary remains intentionally conservative.

Status: **Implemented provisionally; the explicit-factor API is retained, while
ASBC procedure, calibration practice, and any defensible factor range remain
verification pending.**

Sources: [SH-OIML-01] for refractometer/Brix measurement context.

## Hydrometer temperature correction

FermUnits does not currently implement hydrometer temperature correction.

The formula from the legacy brewing inventory was rejected because it omitted
hydrometer calibration temperature, lacked a verified source and validity range,
and produced implausible corrections under ordinary brewing conditions.

A future API must include explicit sample temperature, hydrometer calibration
temperature, temperature scale, supported SG/temperature range, and sample
matrix.

Status: **Rejected legacy formula; replacement implementation blocked pending an
authoritative method.**

Sources: [SH-NIST-01] for hydrometer calibration and temperature-effect context.


### Gravity and extract sources

#### [BR-CHA-GU-2021] Beer Math—Working With Percentages and Gravity Units

- Author: Aaron Brown
- Organization: Canadian Homebrewers Association
- URL: https://canadahomebrews.ca/2021/04/08/beer-math-working-with-percentages-and-gravity-units/
- Accessed: 2026-08-30
- Tier: 4
- Supports:
  - gravity units/points as the digits after the decimal place of specific
    gravity multiplied by 1000;
  - the concrete brewing convention that SG `1.046` corresponds to 46 gravity
    points.
- Limitations:
  - brewing-practice guidance rather than an ASBC analytical method;
  - does not establish a specific-gravity reference temperature or reporting
    precision;
  - does not independently standardize the algebraic extension to negative
    gravity points for SG below 1.000.

#### [BR-QUEK-2019] Molecular structure-property relations controlling mashing performance of amylases as a function of barley grain size

- Authors: Wei Ping Quek, Wenwen Yu, Glen P. Fox, Robert G. Gilbert
- Publication: *Amylase*, 3(1), 1–18, 2019
- DOI: https://doi.org/10.1515/amylase-2019-0001
- Accessed: 2026-08-30
- Tier: 5
- Supports:
  - the exact implemented cubic coefficients for conversion from specific
    gravity to degrees Plato;
  - attribution of that equation to the American Society of Brewing Chemists in
    peer-reviewed brewing research.
- Limitations:
  - this is a secondary use of the equation, not the primary ASBC table or
    method;
  - it does not establish the equation's original provenance, normative
    reference conditions, complete validity range, or ASBC reporting precision.

#### [BR-BUHL-2024] Physical Equations Relating Extract and Relative Density

- Author: Josh Buhl
- Publication: *Journal of the American Society of Brewing Chemists*, 82(3),
  225–237, 2024
- DOI: https://doi.org/10.1080/03610470.2023.2267947
- Accessed: 2026-08-30
- Tier: 5
- Supports:
  - ASBC extract tables as reference data for evaluating relationships between
    relative density and percent-by-mass extract;
  - continued modern analytical interest in converting between those
    quantities.
- Limitations:
  - does not establish the provenance or coefficients of FermUnits' implemented
    cubic;
  - does not by itself establish the cubic's normative reference conditions,
    validity range, or reporting precision.

#### [BR-THESSELING-2019] A Hands-On Guide to Brewing and Analyzing Beer in the Laboratory

- Authors: Florian A. Thesseling, Peter W. Bircham, Stijn Mertens, Karin
  Voordeckers, Kevin J. Verstrepen
- Publication: *Current Protocols in Microbiology*, 54(1), e91, 2019
- DOI: https://doi.org/10.1002/cpmc.91
- PMCID: PMC9286407
- Accessed: 2026-08-30
- Tier: 5
- Supports:
  - degrees Plato as a brewing measure tied to mass percentage of dissolved
    solids in wort;
  - the sucrose-solution reference meaning used to interpret degrees Plato.
- Limitation:
  - does not establish the provenance, coefficients, or range of FermUnits'
    SG-to-Plato polynomial;
  - does not establish a universal Brix/Plato/Balling conversion rule.

## Beer color

### SRM and EBC

Public functions:

- `srm_to_ebc`
- `ebc_to_srm`

Implemented relationship:

```text
EBC = SRM * (25 / 12.7)
SRM = EBC / (25 / 12.7)
```

Status: **Implemented; supporting analytical basis identified, original ASBC
Beer-10 and EBC method details still to be checked directly.**

### Lovibond approximation

Public functions:

- `lovibond_to_srm_approx`
- `srm_to_lovibond_approx`

Implemented relationship:

```text
SRM = 1.3546 * Lovibond - 0.76
```

The inverse is calculated algebraically. Function names include `_approx` because
the visual Lovibond scale is not equivalent to modern spectrophotometric color
indices.

Status: **Implemented provisionally; coefficient provenance, material, range,
and expected error remain verification pending.**

## Analytical bitterness

Public functions:

- `absorbance_275nm_to_bitterness_units`
- `bitterness_units_to_absorbance_275nm`

Implemented relationship:

```text
bitterness units = absorbance at 275 nm * 50
```

The result is represented as an operational analytical measurement. FermUnits
does not define one bitterness unit as an exact concentration of iso-alpha-acid,
does not equate it with perceived bitterness, and does not provide a separate
arithmetic IBU-to-EBU conversion.

Status: **Implemented; coordinated ASBC/EBC relationship identified, direct
method-detail verification pending.**

## Diastatic power

Public functions:

- `lintner_to_windisch_kolbach`
- `windisch_kolbach_to_lintner`

Implemented relationship:

```text
°WK = 3.5 * °Lintner - 16
°Lintner = (°WK + 16) / 3.5
```

Status: **Implemented provisionally; original ASBC/EBC method provenance, range,
and reporting conventions remain verification pending.**

## Carbonation

Public functions:

- `co2_volumes_to_mass_concentration`
- `co2_mass_concentration_to_volumes`
- `co2_volumes_to_grams_per_liter` (scalar compatibility API)
- `co2_grams_per_liter_to_volumes` (scalar compatibility API)

The quantity-aware APIs return or accept Pint mass-concentration quantities so
physical concentration units remain explicit at downstream engineering
boundaries. The semantic "volumes CO2" value remains a scalar rather than an
ordinary multiplicative Pint unit.

The current implementation uses one reciprocal factor in both directions:

```text
grams per liter per volume = 10 / 5.0607
```

This is approximately `1.976 g/L` per volume of CO2. The legacy `1.96` and
`0.51` pair is not used because those rounded values are not exact reciprocals.

### Accessible-source verification result

The Milestone 2 source review narrowed the remaining uncertainty substantially:

- ASBC materials identify **Beer 13 — Dissolved Carbon Dioxide** as the
  analytical method family for dissolved CO2 in brewery products, and *The
  Brewing Science Laboratory* identifies **Beer 13C** as the
  manometric/volumetric method. [BR-ASBC-BEER13-01]
- ASBC **Fills-1** is a packaging/net-content calculation, not the primary
  dissolved-CO2 analytical method. [BR-ASBC-FILLS1-01]
- Torrent (2006), submitted on behalf of the EBC Analysis Committee, reproduces
  an ASBC-adopted Fills-1 density-correction equation and explicitly identifies
  `k = 506.07 mL/g` as the conversion constant for CO2 in volumes to CO2 by
  weight. [BR-EBC-TORRENT-2006]
- Independent physical data report CO2 gas density of approximately `1.976 g/L`
  at `0 °C` and `760 mmHg`. [SH-PUBCHEM-CO2-01]
- University of Florida beverage guidance defines carbonation in volumes as
  volumes of CO2 at STP per volume of liquid and uses
  `1 vol/vol = 1.96 g/L` as its calculation convention. [SH-UF-CO2-01]

These sources make the current approximately `1.976 g/L` factor physically and
industrially well supported. They do **not**, however, expose enough of the
current applicable ASBC method text to establish that ASBC normatively defines
one reported volume using exactly `0 °C` and `760 mmHg`, or to establish the
official reporting precision. Under FermUnits' verification policy, the
relationship therefore remains **Provisional**, not Verified.

### Density and specific-gravity boundary

The accessible sources also clarify two different uses of density that should
not be conflated:

- converting a standardized gas-volume ratio to physical CO2 mass concentration
  uses the gas reference-state conversion factor;
- converting carbonation to mass percent, or correcting packaged-beer density
  and net contents for dissolved CO2, can additionally involve beverage density
  or specific gravity and CO2 partial molal volume.

FermUnits' direct volumes-to-`g/L` API implements the first relationship. It does
not implement the separate Fills-1/EBC package-density correction model. This is
an implementation interpretation supported by the dimensional and method-scope
separation in the accessible sources; direct ASBC method-text review is still
required before treating the convention as normative.

No beverage-specific validity range is currently imposed on the direct
volumes-to-mass-concentration conversion. Experimental ranges reported for
package-density/partial-molal-volume correction models must not be reused as a
validity range for the simpler reference-state conversion without direct source
support.

### Remaining verification questions

- inspect the applicable current ASBC Beer-13 method text directly;
- inspect the applicable current ASBC Fills-1 text directly;
- confirm the normative reference temperature and pressure for reported
  "volumes of CO2";
- confirm whether ASBC reporting uses the approximately `1.976 g/L`
  relationship, a `1.96 g/L` convention, or another stated precision;
- document any legitimate industry-specific alternative standard states rather
  than silently treating one convention as universal.

Status: **Implemented provisionally; accessible-source review complete. Direct
ASBC method-text verification of reference state and reporting precision remains
pending.**

### Carbonation-specific sources

#### [BR-ASBC-BEER13-01] ASBC Beer 13 — Dissolved Carbon Dioxide

- Organization: American Society of Brewing Chemists (ASBC)
- Method index: `https://www.asbcnet.org/Methods/BeerMethods/pages/default.aspx`
- Supporting publication: *The Brewing Science Laboratory*
- URL: `https://www.asbcnet.org/publications/Pages/BSL.aspx`
- Accessed: 2026-08-12
- Tier: 2
- Supports:
  - Beer 13 as the ASBC dissolved-carbon-dioxide method family for brewery
    products;
  - the Beer 13C method name, "Dissolved Carbon Dioxide—Manometric/Volumetric
    Method."
- Limitations:
  - the public method listing and book contents do not expose the complete
    Beer-13 method text;
  - they do not by themselves establish the reference state or numerical
    conversion used by FermUnits.

#### [BR-ASBC-FILLS1-01] ASBC Fills-1 — Total Contents of Bottles and Cans by Calculation from Measured Net Weight

- Organization: American Society of Brewing Chemists (ASBC)
- URL: `https://www.asbcnet.org/Methods/PackagingMethods/pages/default.aspx`
- Accessed: 2026-08-12
- Tier: 2
- Supports:
  - Fills-1 as a packaging/net-content calculation from measured net weight;
  - separation of the Fills-1 packaging role from Beer-13 dissolved-CO2
    analysis.
- Limitation:
  - the complete current Fills-1 equation and its definitions were not publicly
    exposed during this review.

#### [BR-EBC-TORRENT-2006] CO2 correction factor for the net contents of containers

- Author: J. Torrent
- Submitted on behalf of: Analysis Committee of the European Brewery Convention
- Publication: *BrewingScience*, 60(11/12), 3–4, 2006
- URL: `https://brewingscience.de/index.php/brewingscience/article/view/503`
- Accessed: 2026-08-12
- Tier: 4
- Supports:
  - `k = 506.07 mL/g` as the conversion constant for CO2 in volumes to CO2 by
    weight in an equation described as adopted by ASBC;
  - identification of the historical ASBC source as Fills-1/Fills-2 in the
    eighth revised edition (1992);
  - the distinct role of beverage density, specific gravity, residual CO2, and
    CO2 partial molal volume in package-density/net-content corrections.
- Limitation:
  - this is an EBC Analysis Committee technical publication discussing
    packaging correction, not the current ASBC Beer-13 or Fills-1 method text;
  - ranges in the paper concern the density-correction model and must not be
    treated as a validity range for FermUnits' direct volumes-to-`g/L`
    conversion.

## Explicitly superseded legacy claims

The maintained implementation does **not** adopt several claims that appeared in
the original planning inventory:

- no default wort correction factor is assumed;
- no independent De Clerck-style Plato-to-SG formula is used;
- Brix, Plato, and Balling are not generic interchangeable unit aliases;
- no unsupported hydrometer-temperature formula is implemented;
- bitterness units are not defined as an exact iso-alpha-acid mass
  concentration;
- IBU and EBU are not given a synthetic 1:1 conversion API;
- the older Lovibond coefficients `1.35` and `-0.6` are not the current
  implementation;
- the rounded non-reciprocal carbonation pair `1.96` and `0.51` is not used.

## Shared sources used by this reference

- [SH-PINT-01] Pint default unit definitions — defined in
  [`../sources.md`](../sources.md).
- [SH-OIML-01] OIML R 142-1:2025, automated refractometers — defined in
  [`../sources.md`](../sources.md).
- [SH-NIST-01] NBS Circular 555, hydrometer testing — defined in
  [`../sources.md`](../sources.md).

Method-specific brewing verification remains tracked in
[`../asbc-verification.md`](../asbc-verification.md) until the corresponding
primary material can support a stable source record.
