# FermUnits

FermUnits is a Pint-based Python library for units, measurement scales, and
conversions used in brewing, winemaking, cider making, mead making, distilling,
and related fermentation industries.

> **Status:** pre-alpha. Vessel definitions and several brewing gravity
> conversions are implemented. Some formula-based conversions remain
> provisional while their exact ranges, coefficients, and source tables await
> verification against authoritative ASBC material.

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

## Wort refractometer correction

The Brix functions below represent a wort-specific refractometer correction.
They are not general conversions between the Brix and Plato scales.

The correction factor must be supplied explicitly because the appropriate
factor depends on the wort and measurement method and remains pending
authoritative verification.

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

## Design principles

* Pint remains the physical-unit engine.
* FermUnits adds fermentation-industry definitions and domain-specific APIs.
* Ambiguous names such as bare `barrel` are not defined.
* Existing Pint meanings are preserved when they are legitimate.
* Domain-qualified names distinguish conflicting industry meanings.
* Empirical scales and calculations are kept separate from physical units.
* Provisional formulas are labeled clearly.
* Every domain definition and calculation should have a documented source and
  tests.
* Restricted authoritative methods are recorded for later verification rather
  than treated as though their details were directly confirmed.

## Current scope

Implemented physical units include:

* modern British brewery cask units
* modern US beer barrel
* domain-qualified wine and brewing hogsheads
* domain-qualified brewing puncheon and butt

Implemented brewing gravity calculations include:

* specific gravity and gravity points
* provisional specific gravity and degrees Plato conversion
* explicit wort refractometer correction using a caller-supplied factor

Additional wine, distilling, sake, cider, biofuel, and fermentation-process
definitions will be added after their regional, historical, legal, or technical
meanings are documented.
