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
encode reference temperature.

Status: **Implemented; ASBC terminology and reference-condition verification
pending.**

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

Status: **Implemented provisionally; primary source, reference conditions,
scientific validity range, and expected precision remain ASBC verification
pending.**

The numerical SG search interval used by the inverse is an implementation limit,
not an asserted scientific range.

### Brix, Plato, and Balling

FermUnits does not provide a generic Brix-to-Plato conversion and does not
currently provide separate Balling functions. These scales have distinct
historical and analytical contexts and are not treated as interchangeable unit
aliases.

Status: **Not implemented; verification pending.**

Sources: [SH-OIML-01] for Brix instrument context.

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

Status: **Implemented provisionally; ASBC procedure and recommended calibration
practice remain verification pending.**

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

- `co2_volumes_to_grams_per_liter`
- `co2_grams_per_liter_to_volumes`

The current implementation uses one reciprocal factor in both directions:

```text
grams per liter per volume = 10 / 5.0607
```

This is approximately `1.976 g/L` per volume of CO2. The legacy `1.96` and
`0.51` pair is not used because those rounded values are not exact reciprocals.

Status: **Implemented provisionally; exact reference temperature, pressure,
definition of one volume, beverage-density treatment, and complete ASBC method
context remain verification pending.**

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
