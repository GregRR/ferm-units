# FermUnits

FermUnits is a Pint-based Python library for units, measurement scales, and
conversions used in brewing, winemaking, cider making, mead making, and
distilling.

> **Status:** pre-alpha. The initial release focuses on unambiguous physical
> volume units. Formula-based scales and process calculations will be added
> separately and only with documented sources and tests.

## Installation for development

```bash
uv sync --dev
```

## Example

```python
from fermunits import Q_

cask = Q_(1, "firkin")
print(cask.to("liter"))
```

## Design principles

- Pint remains the physical-unit engine.
- FermUnits adds fermentation-industry definitions and domain-specific APIs.
- Ambiguous names such as bare `barrel` are not defined.
- Empirical scales and calculations are kept separate from physical units.
- Every domain definition should have a documented source and a test.

## Initial scope

The first milestone includes modern British brewery cask units and the modern
US beer barrel. Wine and distilling vessel units will be added after their
regional, historical, and legal meanings are documented.
