# ASBC Verification Checklist

This file tracks brewing definitions, formulas, tables, and analytical methods
that require confirmation against original ASBC material.

When an authoritative method is known to exist but is not fully accessible:

* record the method or table name when available;
* distinguish verified details from provisional supporting sources;
* do not imply that restricted content was directly reviewed;
* retain the item until it can be checked against the original ASBC material.

## Gravity and Extract

### Specific gravity

* Status: ASBC verification pending
* Current treatment:

  * specific gravity is represented as a dimensionless density ratio;
  * FermUnits requires a finite value greater than zero;
  * reference temperature is not encoded in the numeric value.
* Confirm:

  * official ASBC definition;
  * reference temperature or temperatures;
  * preferred terminology and notation;
  * whether ASBC distinguishes apparent and true specific gravity in this
    context.

### Gravity points

* Status: brewing shorthand sourced; ASBC terminology verification pending
* Implemented formulas:

  * `GU = (SG - 1) * 1000`
  * `SG = 1 + (GU / 1000)`
* Accessible-source result:

  * Canadian Homebrewers Association guidance defines gravity units as the
    digits after the SG decimal multiplied by 1000 and gives SG `1.046` as
    46 gravity points;
  * this supports the ordinary implemented arithmetic as brewing shorthand but
    does not independently standardize FermUnits' algebraic extension to
    negative points for SG below 1.000 or make gravity points an ASBC
    analytical measurement.
* Confirm:

  * whether ASBC formally defines gravity points;
  * whether gravity points are primarily brewing-industry shorthand rather
    than an ASBC analytical measurement;
  * any recommended terminology or rounding convention.

### Specific gravity to degrees Plato

* Status: exact polynomial independently reproduced with ASBC attribution;
  primary ASBC source and reference-condition verification pending

* Implemented polynomial:

  `°P = -616.868 + 1111.14(SG) - 630.272(SG²) + 135.997(SG³)`

* Accessible-source result:

  * Quek et al. (2019), *Amylase* 3(1):1–18, reproduce the exact implemented
    coefficients and identify the equation as a formula from ASBC;
  * this provides peer-reviewed secondary support for the exact polynomial and
    its ASBC attribution, but it does not identify or expose the primary ASBC
    table or method;
  * Buhl (2024), *Journal of the American Society of Brewing Chemists* 82(3),
    225–237, independently confirms ASBC extract tables as reference data for
    evaluating relative-density/extract equations, but does not establish the
    provenance of this cubic;
  * a 1984 JASBC item titled *Statistical Analysis* (42(3), 138–143; DOI
    `10.1094/ASBCJ-42-0138`) remains a possible historical lead, but accessible
    metadata does not expose the equation or establish that item as its source.

* Current treatment:

  * the function remains explicitly documented as provisional;
  * no ASBC-approved scientific validity range is claimed;
  * SG 1.000 evaluates to approximately `-0.003 °P` because of the rounded
    polynomial coefficients;
  * the result is not silently clamped to zero.

* Still confirm directly:

  * the primary ASBC method/table that defines or tabulates the relationship;
  * whether the 1984 *Statistical Analysis* item is actually part of the
    polynomial's provenance;
  * whether the polynomial or an extract table remains the applicable ASBC
    convention;
  * valid SG range and the complete precision/error qualification;
  * reference temperature and apparent-specific-gravity convention;
  * whether a current ASBC extract table should be preferred over the fitted
    regression for any use case.

### Degrees Plato to specific gravity

* Status: ASBC verification pending
* Current treatment:

  * FermUnits numerically inverts the implemented SG-to-Plato polynomial;
  * this ensures internal round-trip consistency;
  * the numerical search interval is SG 0.5 through 2.0;
  * that interval is an implementation limit, not an ASBC-approved range.
* Rejected formula:

  * the inverse formula originally listed in
    [the legacy brewing inventory](reference/legacy/brewing-inventory.txt) was not
    implemented because it was not numerically consistent with the selected
    SG-to-Plato polynomial.
* Confirm:

  * whether ASBC publishes an inverse formula;
  * whether official extract tables should be used instead;
  * valid Plato range;
  * expected precision and rounding.

### Degrees Brix, Plato, and Balling

* Status: modern Plato/Brix semantic boundary supported; historical Balling and
  cross-scale tolerance verification pending
* Accessible-source result:

  * Thesseling et al. (2019), *Current Protocols in Microbiology* 54:e91,
    describes degrees Plato in wort through an equivalent sucrose-solution
    density/mass-percentage meaning;
  * OIML R 142-1 anchors Brix to sucrose mass-fraction/refractometer practice;
  * these sources support retaining distinct scale names rather than defining a
    universal Brix-to-Plato alias or conversion.

* Current treatment:

  * FermUnits does not provide a generic Brix-to-Plato conversion;
  * FermUnits does not currently provide separate Balling functions;
  * wort refractometer correction is represented as a separate,
    application-specific calculation.
* Confirm:

  * formal differences among the Brix, Plato, and Balling scales;
  * accepted conversion tables or approximations;
  * whether Plato and Balling may be treated as equivalent within stated
    tolerances;
  * whether ASBC provides wort-specific refractometer correction guidance.

### Wort refractometer correction

* Status: ASBC verification pending
* Implemented provisional relationships:

  * `corrected Plato = apparent Brix / wort correction factor`
  * `apparent Brix = Plato * wort correction factor`
* Accessible-source review result (2026-08-30):

  * OIML R 142-1 supports treating Brix as a sucrose/refractometer scale whose
    measurement meaning depends on defined instrument and temperature
    conditions;
  * no authoritative source reviewed in this pass justified a universal default
    wort correction factor;
  * the explicit caller-supplied factor therefore remains the conservative API
    boundary.
* Current treatment:

  * the correction factor is required explicitly;
  * FermUnits provides no default factor;
  * the functions are documented as wort-specific corrections rather than
    general scale conversions.
* Confirm:

  * ASBC-recommended correction procedure;
  * whether a standard default factor is ever appropriate;
  * recommended factor range;
  * calibration procedure for determining a wort-specific factor;
  * restrictions for fermented samples containing alcohol.

## Hydrometer Temperature Correction

### General hydrometer correction

* Status: implementation blocked pending authoritative method

* Rejected provisional formula from
  [the legacy brewing inventory](reference/legacy/brewing-inventory.txt):

  `SG_corrected = SG_measured + 0.000004811(T²) - 0.005408(T) + 0.1292`

* Reason for rejection:

  * the formula does not include the hydrometer calibration temperature;
  * hydrometers may be calibrated at different reference temperatures;
  * sample temperature affects both liquid density and hydrometer response;
  * direct evaluation at ordinary brewing temperatures produces implausible
    corrections;
  * the formula lacks a verified source, range, and temperature-unit
    definition.

* Required before implementation:

  * authoritative ASBC method, table, or equation;
  * explicit sample temperature;
  * explicit hydrometer calibration temperature;
  * defined temperature scale;
  * valid temperature and SG ranges;
  * clarity on whether the method is intended for wort, beer, ethanol
    solutions, sucrose solutions, or another matrix.

## Beer Color

### SRM and EBC

* Status: numerical scale relationship strongly supported; full primary method
  text still pending
* Implemented relationship:

  * `EBC = SRM * (25 / 12.7)`
  * `SRM = EBC / (25 / 12.7)`
* Confirmed from accessible sources:

  * ASBC Beer-10A is the current identified spectrophotometric beer-color
    method;
  * Analytica EBC 9.6 is the current identified spectrophotometric beer-color
    method and refers to EBC 8.5;
  * accessible technical material gives 430 nm, a 10 mm cell, `12.7` as the
    ASBC/SRM scale factor, and `25` as the EBC scale factor;
  * peer-reviewed brewing literature independently gives `EBC = 25 * d * A430`
    and the rounded relation `SRM = 0.508 * EBC`.
* Current treatment:

  * represented as conversion between already reported modern
    spectrophotometric color indices;
  * the exact ratio `25 / 12.7` is used rather than rounded `1.97`/`0.508`;
  * values must be finite and nonnegative;
  * FermUnits does not implement sample clarification, dilution, turbidity
    assessment, or full Beer-10A/EBC 9.6 procedures.
* Remaining direct verification:

  * inspect current Beer-10A and EBC 9.6/8.5 method text;
  * confirm procedural qualifications for clarification, dilution, turbidity,
    instrument range, and reporting precision.

### Lovibond and SRM

* Status: empirical approximation retained as Provisional
* Implemented provisional approximation:

  * `SRM = 1.3546 * Lovibond - 0.76`
  * inverse calculated algebraically.
* Confirmed from accessible sources:

  * the relationship is widely reproduced in brewing guidance;
  * contemporary malt guidance uses Lovibond, SRM, and EBC in malt color
    reporting and warns that Lovibond and SRM diverge increasingly above pale
    malt colors.
* Current treatment:

  * function names include `_approx`;
  * the approximation is not presented as equivalent to the modern SRM/EBC
    spectrophotometric relationship or as a universal physical conversion;
  * inputs that would produce a negative SRM result are rejected.
* Confirm:

  * primary source of the coefficients;
  * intended material, such as malt, wort, or beer;
  * valid Lovibond range;
  * expected error and precision;
  * whether a different approximation is preferred.

## Beer Bitterness

### Analytical bitterness units

* Status: **Verified** for the Beer-23A numerical reporting factor and
  operational meaning represented by the FermUnits helper; current EBC 9.8
  identity confirmed
* Implemented relationship:

  * `bitterness units = method-extract absorbance at 275 nm * 50`
  * inverse calculated algebraically.
* Confirmed from accessible sources:

  * ASBC Beer-23A is *Beer Bitterness—Bitterness Units (International Method)*;
  * ASBC educational material shows acid/nonpolar liquid-liquid extraction,
    measurement at 275 nm, and the `* 50` reporting factor;
  * that ASBC material explicitly states that one bitterness unit is not one ppm
    iso-alpha-acid;
  * Analytica EBC 9.8 is the current international beer-bitterness method and
    its precision chapter includes dry-hopped beer data;
  * ASBC dry-hop method work demonstrates divergence between IBU and direct
    iso-alpha-acid measurements.
* Current treatment:

  * functions use the neutral term `bitterness_units`;
  * the absorbance argument is documented as the method-derived nonpolar
    extract absorbance, not raw beer absorbance;
  * FermUnits applies the reporting factor but does not implement sample
    preparation or extraction;
  * the result is described as an operational analytical measurement;
  * FermUnits does not equate the result exactly with iso-alpha-acid
    concentration or perceived bitterness;
  * no separate arithmetic IBU-to-EBU conversion is provided.
* Remaining direct verification:

  * inspect the current full Beer-23A and EBC 9.8 procedures;
  * confirm formal cuvette/path-length, blank, extraction-volume, and reporting
    precision requirements before documenting those procedural details as
    normative.

## Diastatic Power

### Degrees Lintner and Windisch-Kolbach

* Status: current ASBC/EBC method identities confirmed; conventional numerical
  relationship independently supported; primary conversion provenance pending
* Implemented provisional relationships:

  * `°WK = 3.5 * °Lintner - 16`
  * `°Lintner = (°WK + 16) / 3.5`
* Accessible-source result:

  * current ASBC material identifies Malt-6 as the diastatic-power method family
    and *The Brewing Science Laboratory* names Malt-6A and Malt-6B procedures;
  * current Analytica EBC 4.12 methods determine combined alpha- and beta-amylase
    activity under standardized reaction conditions;
  * EBC reference-material documentation reports diastatic power in WK on a dry
    matter basis;
  * Rani and Bhardwaj (2021), a peer-reviewed malt-quality review, reproduces
    `Lintner = (WK + 16) / 3.5` and identifies the EBC/WK versus Lintner
    reporting distinction;
  * none of the accessible primary method listings reviewed here exposes the
    provenance, exactness, valid range, or formal method-equivalence meaning of
    the cross-scale formula.
* Current treatment:

  * the relationship remains documented as provisional;
  * the functions convert reported numerical scale values, not analytical
    procedures or raw enzyme-activity measurements;
  * negative input values are rejected;
  * forward Lintner values that would produce a negative WK result are rejected;
  * the nonzero intercept means `0 °WK` maps algebraically to about
    `4.57 °Lintner`, so low-end interpretation must not be inferred beyond the
    sourced conventional formula;
  * degrees Lintner remain distinct from degrees Lovibond despite the common
    `°L` abbreviation.
* Still confirm directly:

  * the primary historical or standards source for the Lintner/WK conversion;
  * whether the relationship is defined as exact, conventional, or approximate;
  * whether current ASBC and EBC methods produce results intended to be
    interconverted directly by this equation;
  * dry-matter/reference-basis details on both sides;
  * valid range, rounding, and reporting precision.

## Carbonation

### Volumes of CO2 and physical mass concentration

* Status: **Milestone 2 accessible-source review complete; remains Provisional
  pending direct ASBC method-text verification**
* Implemented relationship:

  * `grams per liter per volume = 10 / 5.0607`
  * approximately `1.976 g/L` per volume of CO2;
  * inverse calculated from the same factor.
* Confirmed from accessible sources:

  * current ASBC materials identify Beer-13 as the dissolved-CO2 analytical
    method family and Beer-13C as a manometric/volumetric method;
  * current ASBC materials identify Fills-1 as a packaging/net-content method,
    so Fills-1 must not be described as the primary dissolved-CO2 analytical
    method;
  * Torrent (2006), submitted on behalf of the EBC Analysis Committee, reports
    an ASBC-adopted Fills-1 equation using `k = 506.07 mL/g` as the conversion
    constant for CO2 in volumes to CO2 by weight;
  * independent physical data give CO2 gas density near `1.976 g/L` at `0 °C`
    and `760 mmHg`;
  * University of Florida beverage guidance defines volumes of CO2 as
    standard-state gas volume per liquid volume and uses `1.96 g/L` as its
    calculation convention.
* Density/specific-gravity interpretation:

  * the direct standardized-gas-volume-to-mass-concentration relationship does
    not require a beverage-density input in the FermUnits API;
  * beverage density/specific gravity and CO2 partial molal volume enter the
    separate package-density, mass-percent, and net-content correction context;
  * FermUnits does not implement that Fills-1/EBC package-correction model.
* Current treatment:

  * one factor is used in both directions to preserve round-trip consistency;
  * the rounded `1.96` and `0.51` pair from
    [the legacy brewing inventory](reference/legacy/brewing-inventory.txt) is
    not used as a reciprocal pair;
  * the more precise ASBC/EBC-associated approximately `1.976 g/L` factor is
    retained while the official ASBC reporting precision remains unresolved;
  * values must be finite and nonnegative;
  * no validity range from partial-molal-volume/package-density studies is
    applied to the direct conversion without source support.
* Still pending direct ASBC verification:

  * inspect the applicable current Beer-13 method text directly;
  * inspect the applicable current Fills-1 method text directly;
  * confirm whether ASBC normatively defines one volume of CO2 at `0 °C` and
    `760 mmHg` (`101.325 kPa`) or another reference state;
  * confirm official rounding/reporting precision;
  * document any legitimate alternative standard states used by other beverage
    industries.

The maintained source records and their limitations are in
[`reference/brewing-units.md`](reference/brewing-units.md), including
`BR-ASBC-BEER13-01`, `BR-ASBC-FILLS1-01`, and `BR-EBC-TORRENT-2006`. Shared
physical and beverage-guidance sources are recorded in [`sources.md`](sources.md)
as `SH-PUBCHEM-CO2-01` and `SH-UF-CO2-01`.
