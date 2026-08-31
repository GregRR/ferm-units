# FermUnits

FermUnits is a Pint-based Python library for units, measurement scales, and
conversions used in brewing, winemaking, cider making, mead making, distilling,
and related fermentation industries.

> **Project status:** alpha. **Latest release:** 0.1.2. FermUnits has a released,
> tested core covering brewing units and calculations plus shared
> solution-chemistry conversions for downstream fermentation-engineering work.
> Public APIs and domain coverage may still evolve before 1.0. Relationships
> awaiting primary-source verification remain explicitly provisional and are
> tracked in the project documentation.

## Installation and development

FermUnits requires Python 3.11 or later and currently supports Pint
`>=0.25.3,<0.26`.

Install the latest release from PyPI:

```bash
pip install ferm-units
```

For a development checkout:

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

The quantity-aware APIs keep physical CO2 mass concentration explicit for
unit-aware downstream applications:

```python
from fermunits import (
    Q_,
    co2_mass_concentration_to_volumes,
    co2_volumes_to_mass_concentration,
)

concentration = co2_volumes_to_mass_concentration(2.5)
kilograms_per_cubic_meter = concentration.to("kilogram / meter ** 3")
volumes = co2_mass_concentration_to_volumes(Q_(4.94, "gram / liter"))
```

The original scalar grams-per-liter APIs remain available for compatibility:

```python
from fermunits import (
    co2_grams_per_liter_to_volumes,
    co2_volumes_to_grams_per_liter,
)

grams_per_liter = co2_volumes_to_grams_per_liter(2.5)
volumes = co2_grams_per_liter_to_volumes(grams_per_liter)
```

The current factor is supported by an EBC Analysis Committee publication that
reports an ASBC-adopted packaging equation using `506.07 mL/g` as the
conversion constant between CO2 volumes and CO2 by weight. Independent
physical data place CO2 gas density at approximately `1.976 g/L` at 0 °C and
760 mmHg, while University of Florida IFAS beverage guidance describes
volumes of CO2 as standard-state gas volume per liquid volume and uses a rounded
`1.96 g/L` convention. Direct review of the applicable ASBC Beer-13 and Fills-1
method text is still needed to establish the normative reference state and
reporting precision, so the FermUnits relationship remains provisional.

The same factor is used in both directions to preserve round-trip consistency.
Gauge versus absolute pressure, carbonation-equilibrium pressure, gas blends,
and draft-system balancing are downstream engineering semantics rather than
FermUnits unit definitions.

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

## Solution chemistry and water treatment

FermUnits also provides shared solution-chemistry conversions intended for
water-treatment and other fermentation engineering applications. These APIs
keep chemical semantics explicit rather than hiding them inside ambiguous unit
labels.

Chemical-equivalent concentration uses FermUnits' separate `equivalent`
dimension. Converting from amount concentration requires an explicit
equivalence factor:

```python
from fermunits import Q_, amount_concentration_to_equivalent_concentration

calcium = Q_(1.0, "millimole / liter")
charge_equivalents = amount_concentration_to_equivalent_concentration(
    calcium,
    equivalence_factor=2.0,
)
```

For conventional water-analysis reporting, FermUnits implements the relationship
`50 mg/L as CaCO3 = 1 mEq/L`. The `as CaCO3` reporting basis remains application
metadata; it is not encoded as though calcium carbonate were necessarily the
dissolved analyte.

```python
from fermunits import (
    Q_,
    caco3_basis_mass_concentration_to_equivalent_concentration,
)

alkalinity_as_caco3 = Q_(100.0, "milligram / liter")
alkalinity = caco3_basis_mass_concentration_to_equivalent_concentration(
    alkalinity_as_caco3
)
```

Mass concentration and mass fraction are not treated as interchangeable. A
conversion such as `mg/L` to `mg/kg` requires explicit solution density:

```python
from fermunits import Q_, mass_concentration_to_mass_fraction

concentration = Q_(100.0, "milligram / liter")
density = Q_(1.05, "kilogram / liter")
mass_fraction = mass_concentration_to_mass_fraction(concentration, density)
```

Likewise, conversion between mass concentration and amount concentration
requires an explicit molar mass supplied as a Pint quantity:

```python
from fermunits import Q_, mass_concentration_to_amount_concentration

sodium_chloride = Q_(58.44, "milligram / liter")
molar_mass = Q_(58.44, "gram / mole")
amount_concentration = mass_concentration_to_amount_concentration(
    sodium_chloride,
    molar_mass,
)
```

FermUnits preserves Pint's generic `ppm` unit, but canonical chemistry data
should use an explicit ratio such as `mg/kg` or `microgram / kilogram` when the intended basis
is mass fraction. FermUnits does not define a generic `ppb` alias.

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
* Scientific verification status is tracked separately from implementation
  status.
* Unsupported formulas are rejected rather than implemented merely because
  they appeared in an early project inventory.

## Current brewing scope

Implemented physical units include:

* British brewery cask units, including current-use and historical large-cask
  measures;
* modern US beer barrel;
* Imperial beer barrel;
* pin cask;
* firkin;
* kilderkin;
* domain-qualified wine and brewing hogsheads;
* domain-qualified brewing puncheon, butt, and tun.

Implemented brewing calculations include:

* specific gravity and gravity points;
* provisional specific gravity and degrees Plato conversion;
* explicit wort refractometer correction with a caller-supplied factor;
* SRM and EBC color-index conversion;
* approximate Lovibond and SRM conversion;
* analytical bitterness units from 275 nm absorbance;
* provisional Lintner and Windisch-Kolbach conversion;
* dissolved CO2 conversion between volumes and physical mass concentration,
  with scalar grams-per-liter compatibility APIs.

Not yet implemented:

* hydrometer temperature correction;
* generic Brix, Plato, and Balling scale conversion;
* recipe-estimation formulas such as Tinseth or Rager bitterness;
* calculations that require unverified assumptions or inaccessible source
  details.

Additional wine, distilling, sake, cider, biofuel, and fermentation-process
definitions will be added after their regional, historical, legal, or technical
meanings are documented.

## Design and source verification

The architectural boundary between Pint, FermUnits, and downstream engineering
applications is documented in [`DESIGN.md`](DESIGN.md). Development priorities
and milestone sequencing are tracked in [`ROADMAP.md`](ROADMAP.md).

Project-wide source status and citation conventions are documented in
[`docs/sources.md`](docs/sources.md). Maintained domain inventories live under
[`docs/reference/`](docs/reference/), and unresolved ASBC/EBC verification work
is tracked in [`docs/asbc-verification.md`](docs/asbc-verification.md).

## License

FermUnits is distributed under the MIT License. See [`LICENSE`](LICENSE).

