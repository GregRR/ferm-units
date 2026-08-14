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

* Status: ASBC verification pending
* Implemented formulas:

  * `GU = (SG - 1) * 1000`
  * `SG = 1 + (GU / 1000)`
* Confirm:

  * whether ASBC formally defines gravity points;
  * whether gravity points are primarily brewing-industry shorthand rather
    than an ASBC analytical measurement;
  * any recommended terminology or rounding convention.

### Specific gravity to degrees Plato

* Status: ASBC verification pending

* Implemented provisional polynomial:

  `°P = -616.868 + 1111.14(SG) - 630.272(SG²) + 135.997(SG³)`

* Current treatment:

  * the function is explicitly documented as provisional;
  * no ASBC-approved scientific validity range is claimed;
  * SG 1.000 evaluates to approximately `-0.003 °P` because of the rounded
    polynomial coefficients;
  * the result is not silently clamped to zero.

* Confirm:

  * original source of the polynomial;
  * whether it is endorsed or merely commonly used;
  * valid SG range;
  * expected precision;
  * reference temperature;
  * whether ASBC recommends an official extract table instead.

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

* Status: ASBC verification pending
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

* Status: supporting analytical basis identified
* Implemented relationship:

  * `EBC = SRM * (25 / 12.7)`
  * `SRM = EBC / (25 / 12.7)`
* Current treatment:

  * represented as modern spectrophotometric color-index conversions;
  * values must be finite and nonnegative.
* Confirm against original methods:

  * ASBC Beer-10 method details;
  * EBC method details;
  * wavelength, path length, dilution, turbidity, and reporting conventions;
  * whether the direct scale-factor relationship requires qualifications.

### Lovibond and SRM

* Status: empirical approximation pending primary-source verification
* Implemented provisional approximation:

  * `SRM = 1.3546 * Lovibond - 0.76`
  * inverse calculated algebraically.
* Current treatment:

  * function names include `_approx`;
  * the conversion is not presented as equivalent to the modern SRM/EBC
    spectrophotometric relationship;
  * inputs that would produce a negative SRM result are rejected.
* Confirm:

  * original source of the coefficients;
  * intended material, such as malt, wort, or beer;
  * valid Lovibond range;
  * expected error and precision;
  * whether a different approximation is preferred.

## Beer Bitterness

### Analytical bitterness units

* Status: coordinated ASBC/EBC method relationship identified
* Implemented relationship:

  * `bitterness units = absorbance at 275 nm * 50`
  * inverse calculated algebraically.
* Current treatment:

  * functions use the neutral term `bitterness_units`;
  * the result is described as an operational analytical measurement;
  * FermUnits does not equate the result exactly with iso-alpha-acid
    concentration;
  * FermUnits does not claim that the result directly measures perceived
    bitterness;
  * no separate arithmetic IBU-to-EBU conversion is provided.
* Confirm against original methods:

  * ASBC Beer-23 procedure;
  * EBC Method 9.8 procedure;
  * extraction solvent and sample preparation;
  * path length and absorbance conventions;
  * applicability to dry-hopped beer;
  * official naming and reporting conventions.

## Diastatic Power

### Degrees Lintner and Windisch-Kolbach

* Status: ASBC/EBC verification pending
* Implemented provisional relationships:

  * `°WK = 3.5 * °Lintner - 16`
  * `°Lintner = (°WK + 16) / 3.5`
* Current treatment:

  * negative diastatic-power results are rejected;
  * the relationship is documented as provisional.
* Confirm:

  * original ASBC and EBC method references;
  * whether the relationship is exact, conventional, or approximate;
  * rounding and reporting conventions;
  * valid range;
  * distinction between degrees Lintner and degrees Lovibond, both commonly
    abbreviated with `°L`.

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
