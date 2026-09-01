# Third-party software

## Pint

FermUnits depends on Pint, a Python library for physical quantities and units.
Pint is distributed under the BSD 3-Clause License.

FermUnits uses Pint through Pint's public API and does not copy or modify Pint's
source code. FermUnits re-exports Pint's `Quantity` type through its own public
API so downstream users do not need a separate Pint import solely to use
FermUnits quantities.
