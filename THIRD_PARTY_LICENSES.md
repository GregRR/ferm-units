# Third-party software

## Pint

FermUnits depends on Pint, a Python library for physical quantities and units.
Pint is distributed under the BSD 3-Clause License.

FermUnits uses Pint through Pint's public API and does not copy or modify Pint's
source code. FermUnits deliberately re-exports Pint's `Quantity`, `UnitRegistry`,
and `DimensionalityError` through its public API so maintained downstream code
can construct and type quantities and registries, and handle dimensionality
errors, without a separate Pint import solely for those supported boundaries.
