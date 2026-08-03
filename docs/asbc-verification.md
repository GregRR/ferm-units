# ASBC Verification Checklist

Items in this file are believed to have an authoritative ASBC method, table,
definition, or publication behind them, but have not yet been fully verified
against the original ASBC material.

## Gravity and Extract

### Specific gravity

- Status: ASBC verification pending
- Confirm:
  - official definition
  - reference temperature or temperatures
  - preferred terminology and notation
- Provisional treatment:
  - dimensionless density ratio
  - reference temperature must be recorded where measurement precision matters

### Gravity points

- Status: ASBC verification pending
- Provisional formulas:
  - `GU = (SG - 1) * 1000`
  - `SG = 1 + (GU / 1000)`
- Confirm:
  - whether ASBC formally defines gravity points
  - whether this is primarily an industry shorthand rather than an ASBC method

### Specific gravity to degrees Plato

- Status: ASBC verification pending
- Provisional polynomial:

  `°P = -616.868 + 1111.14(SG) - 630.272(SG²) + 135.997(SG³)`

- Confirm:
  - original ASBC source
  - valid SG range
  - expected precision
  - reference temperature
  - whether ASBC recommends tables instead of this polynomial

### Degrees Plato to specific gravity

- Status: ASBC verification pending
- Do not use the formula currently listed in `All Units.txt`.
- Provisional implementation plan:
  - numerically invert the selected SG-to-Plato polynomial
- Confirm:
  - whether ASBC publishes an inverse formula
  - whether official extract tables should be used instead
  - valid Plato range and expected precision

### Degrees Brix, Plato, and Balling

- Status: ASBC verification pending
- Confirm:
  - formal differences among the three scales
  - accepted conversion tables or approximations
  - whether any may be treated as equivalent within stated tolerances
  - refractometer wort-correction guidance
