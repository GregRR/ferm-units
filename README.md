# FermUnits

FermUnits is a Pint-based Python library for units, measurement scales, and
conversions used in brewing, winemaking, cider making, mead making, distilling,
and related fermentation industries.

> **Status:** pre-alpha. The brewing implementation now includes vessel units,
> gravity calculations, color indices, analytical bitterness, diastatic power,
> and carbonation conversions. Some relationships remain provisional pending
> verification against original ASBC or EBC methods and tables.

## Installation for development

```bash
uv sync --dev
```

## Physical-unit example

```python
from fermunits import Q_

cask = Q_(1, "firkin")
print(cask.to("liter"))
```

## Gravity examples

```python
from fermunits import (
    gravity_points_to_sg,
    plato_to_sg,
    sg_to_gravity_points,
    sg_to_plato,
)

points = sg_to_gravity_points(1.050)
specific_gravity = gravity_points_to_sg(points)

plato = sg_to_plato(1.048)
estimated_sg = plato_to_sg(plato)
```

The SG-to-Plato polynomial remains provisional pending verification against
authoritative ASBC extract tables or methods. The inverse function numerically
inverts the same polynomial to preserve internal consistency.

The current numerical inversion interval is an implementation limit rather
than an ASBC-approved scientific range.

## Wort refractometer correction

These functions represent a wort-specific refractometer correction. They are
not general conversions between the Brix and Plato scales.

The correction factor must be supplied explicitly. FermUnits does not assume a
default wort correction factor.

```python
from fermunits import (
    plato_to_wort_refractometer_brix,
    wort_refractometer_brix_to_plato,
)

plato = wort_refractometer_brix_to_plato(
    apparent_brix=12.48,
    wort_correction_factor=1.04,
)

apparent_brix = plato_to_wort_refractometer_brix(
    plato=12.0,
    wort_correction_factor=1.04,
)
```

## Beer color

Modern SRM and EBC color indices can be converted directly.

```python
from fermunits import ebc_to_srm, srm_to_ebc

ebc = srm_to_ebc(10.0)
srm = ebc_to_srm(ebc)
```

Lovibond conversions are explicitly labeled as approximations because the
older visual Lovibond scale is not equivalent to the modern
spectrophotometric SRM and EBC scales.

```python
from fermunits import (
    lovibond_to_srm_approx,
    srm_to_lovibond_approx,
)

srm = lovibond_to_srm_approx(10.0)
lovibond = srm_to_lovibond_approx(srm)
```

## Analytical bitterness

FermUnits implements the coordinated ASBC/EBC-style analytical relationship
between absorbance at 275 nm and bitterness units.

```python
from fermunits import (
    absorbance_275nm_to_bitterness_units,
    bitterness_units_to_absorbance_275nm,
)

bitterness_units = absorbance_275nm_to_bitterness_units(0.5)
absorbance = bitterness_units_to_absorbance_275nm(bitterness_units)
```

Bitterness units are operational analytical results. They are not represented
as an exact concentration of iso-alpha-acids or as a direct measurement of
perceived bitterness.

FermUnits does not currently provide a separate arithmetic conversion between
IBU and EBU because those names refer to coordinated analytical methods rather
than clearly distinct numerical scales.

## Diastatic power

```python
from fermunits import (
    lintner_to_windisch_kolbach,
    windisch_kolbach_to_lintner,
)

windisch_kolbach = lintner_to_windisch_kolbach(60.0)
lintner = windisch_kolbach_to_lintner(windisch_kolbach)
```

The Lintner and Windisch-Kolbach relationship remains provisional pending
verification against the original ASBC and EBC analytical methods.

## Carbonation

```python
from fermunits import (
    co2_grams_per_liter_to_volumes,
    co2_volumes_to_grams_per_liter,
)

grams_per_liter = co2_volumes_to_grams_per_liter(2.5)
volumes = co2_grams_per_liter_to_volumes(grams_per_liter)
```

The current factor is derived from an ASBC-hosted technical source. Its exact
reference temperature, pressure, and relationship to the complete analytical
method remain pending verification.

The same factor is used in both directions to preserve round-trip consistency.

## Hydrometer temperature correction

FermUnits does not currently implement hydrometer temperature correction.

The provisional formula listed in the original project inventory was rejected
because it omitted the hydrometer calibration temperature and produced
physically implausible results.

A correction will not be added until an authoritative method or table can be
implemented with:

* explicit sample temperature;
* explicit hydrometer calibration temperature;
* a defined temperature scale;
* supported temperature and specific-gravity ranges;
* a clearly identified sample matrix.

## Design principles

* Pint remains the physical-unit engine.
* FermUnits adds fermentation-industry definitions and domain-specific APIs.
* Ambiguous names such as bare `barrel` are not defined.
* Existing Pint meanings are preserved when they are legitimate.
* Domain-qualified names distinguish conflicting industry meanings.
* Empirical scales and calculations are kept separate from physical units.
* Approximate and provisional formulas are labeled clearly.
* Input validation rejects nonfinite or physically invalid values.
* Every domain definition and calculation should have a documented source and
  tests.
* Restricted authoritative methods are recorded for later verification rather
  than treated as though their details were directly confirmed.
* Unsupported formulas are rejected rather than implemented merely because
  they appeared in the initial project inventory.

## Current brewing scope

Implemented physical units include:

* modern British brewery cask units;
* modern US beer barrel;
* Imperial beer barrel;
* pin cask;
* firkin;
* kilderkin;
* domain-qualified wine and brewing hogsheads;
* domain-qualified brewing puncheon and butt.

Implemented brewing calculations include:

* specific gravity and gravity points;
* provisional specific gravity and degrees Plato conversion;
* explicit wort refractometer correction with a caller-supplied factor;
* SRM and EBC color-index conversion;
* approximate Lovibond and SRM conversion;
* analytical bitterness units from 275 nm absorbance;
* provisional Lintner and Windisch-Kolbach conversion;
* dissolved CO2 conversion between volumes and grams per liter.

Not yet implemented:

* hydrometer temperature correction;
* generic Brix, Plato, and Balling scale conversion;
* recipe-estimation formulas such as Tinseth or Rager bitterness;
* calculations that require unverified assumptions or inaccessible source
  details.

Additional wine, distilling, sake, cider, biofuel, and fermentation-process
definitions will be added after their regional, historical, legal, or technical
meanings are documented.

## Source verification

Detailed source-status notes and unresolved questions are tracked in:

```text
docs/asbc-verification.md
```

Items remain on that checklist until the original ASBC or EBC method, table,
or publication can be reviewed directly.
