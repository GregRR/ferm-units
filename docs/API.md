# FermUnits Public API

This document is the canonical user-facing API reference for FermUnits 0.1.3.
It describes the public names exported by `fermunits`, the FermUnits-specific
unit definitions loaded into its registry, and the Pint functionality available
through the public FermUnits objects.

For the scientific basis, source status, assumptions, and limitations behind a
conversion, follow the links to the domain reference documents. This API page
specifies how to use the library; the reference documents specify why a
relationship exists and how strongly it is supported.

## Import and dependency boundary

Normal downstream use should import unit construction, quantity typing, and
registry access from FermUnits:

```python
from fermunits import Q_, Quantity, ureg
```

Pint is an implementation dependency of FermUnits and is installed transitively.
A downstream application does not need to import or declare Pint merely to use
FermUnits quantities, units, conversions, arithmetic, dimensionality, parsing,
or registry operations.

`Q_` creates real Pint `Quantity` objects, `Quantity` is Pint's generic quantity
type re-exported by FermUnits, and `ureg` is a real Pint `UnitRegistry` containing
Pint's normal unit definitions plus the FermUnits definitions listed below.
FermUnits does not wrap away the public APIs of those objects. Public Pint
methods and properties on `Quantity` and `UnitRegistry` therefore remain
available through the objects imported from FermUnits.

For example:

```python
from fermunits import Q_, Quantity, ureg

volume: Quantity[float] = Q_(5.0, "gallon")
liters = volume.to("liter")
unit = ureg.Unit("milligram / liter")
parsed = ureg.parse_units("kg / m^3")
compatible = ureg.get_compatible_units("liter")
```

The same applies to normal Pint quantity arithmetic, comparison, conversion,
unit simplification, magnitude and unit access, dimensionality inspection, and
other public instance APIs supported by the installed Pint version.

FermUnits intentionally does **not** re-export every top-level class or function
from the `pint` package. If a FermUnits consumer eventually needs a Pint feature
that cannot be reached through the public FermUnits objects, that should be
considered a FermUnits API gap rather than a reason for ordinary downstream code
to begin depending directly on Pint.

FermUnits 0.1.3 supports Pint `>=0.25.3,<0.26`.

## Public package surface

The supported package-level interface is the set of names exported by
`fermunits`. Unless a name is documented here or explicitly exported by the
package, code should treat it as an implementation detail.

### `Q_`

```python
from fermunits import Q_

mass = Q_(10, "gram")
```

The default registry's quantity constructor. It returns genuine Pint quantities
and preserves Pint magnitude typing.

### `Quantity`

```python
from fermunits import Quantity

mass: Quantity[float]
```

Pint's generic `Quantity` type re-exported by FermUnits for downstream type
annotations and runtime use. Consumers should import it from FermUnits rather
than importing `pint.Quantity` solely to type FermUnits quantities.

### `ureg`

```python
from fermunits import ureg

liter = ureg.Unit("liter")
```

The process-wide default FermUnits `UnitRegistry`. It contains Pint's standard
unit definitions plus all FermUnits definitions and registered internal
conversion support.

Applications should normally use this registry so quantities share one registry
identity.

### `create_registry()`

```python
create_registry()
```

Returns a new isolated Pint `UnitRegistry` containing all FermUnits definitions.
This is useful when an application or test deliberately needs registry isolation.

### `__version__`

```python
import fermunits

print(fermunits.__version__)
```

The installed `ferm-units` distribution version. This attribute is available as
package metadata even though it is not part of `fermunits.__all__`.

## Pint functionality available through FermUnits

Because `Q_`, `Quantity`, and `ureg` expose genuine Pint objects, FermUnits
consumers retain Pint's normal object-level functionality. This includes, among
other public Pint APIs supported by the pinned Pint range:

- quantity construction through `Q_` or `ureg.Quantity`;
- unit conversion with methods such as `.to(...)` and `.ito(...)`;
- arithmetic between compatible quantities and scalars;
- compound-unit arithmetic and simplification;
- comparison of compatible quantities;
- `.magnitude`, `.units`, and `.dimensionality` inspection;
- parsing units and quantity expressions through the registry;
- creating `Unit` objects through `ureg.Unit(...)`;
- compatible-unit discovery through the registry;
- registry-level unit lookup and dimensionality operations;
- Pint contexts and other registry behavior reachable through the public
  `UnitRegistry` object.

FermUnits does not duplicate Pint's complete method-by-method documentation.
The installed Pint documentation remains authoritative for the behavior of Pint
object APIs; this document defines how those objects enter the FermUnits public
interface.

FermUnits-specific relationships that carry domain semantics should use the
explicit functions below instead of hiding the relationship inside generic unit
conversion. Examples include pH, Plato/specific-gravity relationships, chemical
equivalents, and carbonation volumes.

## FermUnits unit definitions

`ureg` and registries returned by `create_registry()` include all normal Pint
unit definitions plus the definitions below.

### Solution chemistry

| Name | Alias | Definition |
|---|---|---|
| `equivalent` | `eq` | Base FermUnits chemical-equivalent dimension |
| `milliequivalent` | `mEq` | `1e-3 equivalent` |

Chemical equivalents are intentionally dimensionally distinct from ordinary
amount of substance. Use the explicit solution-chemistry functions below when
converting between moles and equivalents.

### Brewing vessel volumes

| Name | Definition |
|---|---|
| `imperial_beer_barrel` | Pint `imperial_barrel` |
| `kilderkin` | `18 imperial_gallon` |
| `firkin` | `9 imperial_gallon` |
| `pin_cask` | `4.5 imperial_gallon` |
| `wine_hogshead` | Pint `hogshead` |
| `brewing_hogshead` | `54 imperial_gallon` |
| `brewing_puncheon` | `72 imperial_gallon` |
| `brewing_butt` | `108 imperial_gallon` |
| `brewing_tun` | `216 imperial_gallon` |
| `us_beer_barrel` | Pint `beer_barrel` |

Pint's existing `beer_barrel`, `imperial_gallon`, `hogshead`, and other standard
units remain available through the same registry. See
[`reference/brewing-units.md`](reference/brewing-units.md) for sourcing,
historical ambiguity, and naming decisions.

## pH

pH is a logarithmic semantic value, not a Pint unit. FermUnits therefore uses a
small explicit type rather than pretending pH is an ordinary dimensional
quantity.

See [`reference/solution-chemistry.md`](reference/solution-chemistry.md) for the
scientific contract and measurement boundary.

### `PHValue`

```python
PHValue(value: float)
```

Immutable finite numeric value on the pH scale.

```python
from fermunits import PHValue

ph = PHValue(7.0)
```

The constructor normalizes the value to `float` and rejects non-finite values.
FermUnits does not impose an artificial `0 <= pH <= 14` restriction.

### `ph_to_hydrogen_ion_activity()`

```python
ph_to_hydrogen_ion_activity(ph: PHValue) -> float
```

Returns the positive dimensionless hydrogen-ion activity corresponding to pH.
It does not return hydrogen-ion concentration and does not infer an activity
coefficient.

```python
from fermunits import PHValue, ph_to_hydrogen_ion_activity

activity = ph_to_hydrogen_ion_activity(PHValue(7.0))
```

### `hydrogen_ion_activity_to_ph()`

```python
hydrogen_ion_activity_to_ph(hydrogen_ion_activity: float) -> PHValue
```

Returns pH from a positive finite dimensionless hydrogen-ion activity.

```python
from fermunits import hydrogen_ion_activity_to_ph

ph = hydrogen_ion_activity_to_ph(1e-7)
```

## Solution chemistry

The APIs in this section operate on real Pint quantities created from FermUnits.
They keep chemistry-specific semantics explicit rather than encoding them in
ambiguous unit names.

See [`reference/solution-chemistry.md`](reference/solution-chemistry.md) for the
full semantic model, source record, reporting-basis rules, and downstream
boundaries.

### Amount and chemical equivalents

#### `amount_to_equivalents()`

```python
amount_to_equivalents(
    amount: Quantity,
    equivalence_factor: float,
) -> Quantity
```

Converts amount of substance to chemical-equivalent amount using an explicit,
positive equivalence factor in equivalents per mole.

#### `equivalents_to_amount()`

```python
equivalents_to_amount(
    equivalent_amount: Quantity,
    equivalence_factor: float,
) -> Quantity
```

Converts chemical-equivalent amount back to amount of substance using the
explicit equivalence factor.

### Amount concentration and equivalent concentration

#### `amount_concentration_to_equivalent_concentration()`

```python
amount_concentration_to_equivalent_concentration(
    amount_concentration: Quantity,
    equivalence_factor: float,
) -> Quantity
```

Converts amount concentration such as `millimole / liter` to equivalent
concentration using an explicit equivalence factor.

#### `equivalent_concentration_to_amount_concentration()`

```python
equivalent_concentration_to_amount_concentration(
    equivalent_concentration: Quantity,
    equivalence_factor: float,
) -> Quantity
```

Performs the inverse conversion.

### Mass concentration and equivalent concentration

#### `mass_concentration_to_equivalent_concentration()`

```python
mass_concentration_to_equivalent_concentration(
    mass_concentration: Quantity,
    equivalent_mass_grams_per_equivalent: float,
) -> Quantity
```

Converts mass concentration to equivalent concentration using an explicit
positive equivalent mass in grams per equivalent.

#### `equivalent_concentration_to_mass_concentration()`

```python
equivalent_concentration_to_mass_concentration(
    equivalent_concentration: Quantity,
    equivalent_mass_grams_per_equivalent: float,
) -> Quantity
```

Performs the inverse conversion using the same explicit equivalent-mass
semantics.

### CaCO3 reporting basis

#### `caco3_basis_mass_concentration_to_equivalent_concentration()`

```python
caco3_basis_mass_concentration_to_equivalent_concentration(
    mass_concentration_as_caco3: Quantity,
) -> Quantity
```

Converts a conventional water-analysis mass concentration reported *as CaCO3*
to equivalent concentration using `50 mg/L as CaCO3 = 1 mEq/L`.

The returned quantity does not imply that dissolved calcium carbonate is the
analyte. The `as CaCO3` reporting basis remains application metadata.

#### `equivalent_concentration_to_caco3_basis_mass_concentration()`

```python
equivalent_concentration_to_caco3_basis_mass_concentration(
    equivalent_concentration: Quantity,
) -> Quantity
```

Converts equivalent concentration to a mass-concentration value on the CaCO3
reporting basis. The calling application remains responsible for preserving the
`as CaCO3` metadata.

### Mass concentration and mass fraction

#### `mass_concentration_to_mass_fraction()`

```python
mass_concentration_to_mass_fraction(
    mass_concentration: Quantity,
    solution_density: Quantity,
) -> Quantity
```

Converts mass-per-volume concentration to a dimensionless mass fraction using
an explicit positive finite solution density.

#### `mass_fraction_to_mass_concentration()`

```python
mass_fraction_to_mass_concentration(
    mass_fraction: Quantity,
    solution_density: Quantity,
) -> Quantity
```

Converts a dimensionless mass fraction to mass-per-volume concentration using
an explicit positive finite solution density.

### Mass concentration and amount concentration

#### `mass_concentration_to_amount_concentration()`

```python
mass_concentration_to_amount_concentration(
    mass_concentration: Quantity,
    molar_mass: Quantity,
) -> Quantity
```

Converts mass concentration to amount concentration using an explicit positive
finite molar mass.

#### `amount_concentration_to_mass_concentration()`

```python
amount_concentration_to_mass_concentration(
    amount_concentration: Quantity,
    molar_mass: Quantity,
) -> Quantity
```

Performs the inverse conversion using an explicit molar mass.

## Gravity and extract

See [`reference/brewing-units.md`](reference/brewing-units.md) for source status,
validity notes, and the distinction between physical scales and empirical
relationships.

### `sg_to_gravity_points()`

```python
sg_to_gravity_points(specific_gravity: float) -> float
```

Converts specific gravity to algebraic gravity points relative to SG 1.000.

### `gravity_points_to_sg()`

```python
gravity_points_to_sg(gravity_points: float) -> float
```

Converts algebraic gravity points back to specific gravity.

### `sg_to_plato()`

```python
sg_to_plato(specific_gravity: float) -> float
```

Estimates degrees Plato from specific gravity using the project's documented
relationship.

### `plato_to_sg()`

```python
plato_to_sg(plato: float) -> float
```

Numerically inverts the same SG-to-Plato relationship. The current numerical
inversion interval is an implementation limit, not an asserted analytical
method range.

## Wort refractometer correction

These functions are for **unfermented wort only**. They are not general Brix ↔
Plato conversions and must not be applied unchanged after alcohol is present.
The wort correction factor is always explicit; FermUnits does not supply a
default.

### `wort_refractometer_brix_to_plato()`

```python
wort_refractometer_brix_to_plato(
    apparent_brix: float,
    wort_correction_factor: float,
) -> float
```

Corrects an apparent wort refractometer Brix reading to estimated degrees Plato.
The correction factor must be positive and finite.

### `plato_to_wort_refractometer_brix()`

```python
plato_to_wort_refractometer_brix(
    plato: float,
    wort_correction_factor: float,
) -> float
```

Inverse of the unfermented-wort correction above.

## Beer color

See [`reference/brewing-units.md`](reference/brewing-units.md) for analytical
method qualification and the status of the Lovibond approximations.

### `srm_to_ebc()`

```python
srm_to_ebc(srm: float) -> float
```

Converts a modern method-derived ASBC SRM index to EBC.

### `ebc_to_srm()`

```python
ebc_to_srm(ebc: float) -> float
```

Converts a modern method-derived EBC color index to ASBC SRM.

### `lovibond_to_srm_approx()`

```python
lovibond_to_srm_approx(lovibond: float) -> float
```

Approximates SRM from degrees Lovibond. The function name deliberately marks
this as an approximation rather than an exact scale identity.

### `srm_to_lovibond_approx()`

```python
srm_to_lovibond_approx(srm: float) -> float
```

Approximate inverse of the Lovibond-to-SRM relationship.

## Analytical bitterness

See [`reference/brewing-units.md`](reference/brewing-units.md) for the
ASBC/EBC-style analytical basis and method limitations.

### `absorbance_275nm_to_bitterness_units()`

```python
absorbance_275nm_to_bitterness_units(
    extract_absorbance_275nm: float,
) -> float
```

Calculates method-derived beer bitterness units from 275 nm extract absorbance.
Bitterness units are operational analytical results, not an exact concentration
of iso-alpha-acids and not a direct sensory bitterness scale.

### `bitterness_units_to_absorbance_275nm()`

```python
bitterness_units_to_absorbance_275nm(
    bitterness_units: float,
) -> float
```

Inverse numerical relationship for method-derived 275 nm extract absorbance.

## Diastatic power

See [`reference/brewing-units.md`](reference/brewing-units.md) for source status.

### `lintner_to_windisch_kolbach()`

```python
lintner_to_windisch_kolbach(lintner: float) -> float
```

Converts a reported degrees-Lintner value to Windisch-Kolbach units.

### `windisch_kolbach_to_lintner()`

```python
windisch_kolbach_to_lintner(windisch_kolbach: float) -> float
```

Converts a reported Windisch-Kolbach value to degrees Lintner.

## Carbonation

See [`reference/brewing-units.md`](reference/brewing-units.md) for the current
verification status and reference-state limitations.

The quantity-aware APIs are preferred when physical concentration is part of a
larger unit-aware calculation.

### `co2_volumes_to_mass_concentration()`

```python
co2_volumes_to_mass_concentration(co2_volumes: float) -> Quantity
```

Converts volumes of dissolved CO2 to a FermUnits/Pint mass-concentration
quantity.

### `co2_mass_concentration_to_volumes()`

```python
co2_mass_concentration_to_volumes(
    mass_concentration: Quantity,
) -> float
```

Converts a compatible dissolved-CO2 mass concentration to volumes of CO2.

### `co2_volumes_to_grams_per_liter()`

```python
co2_volumes_to_grams_per_liter(co2_volumes: float) -> float
```

Compatibility scalar API returning dissolved CO2 in grams per liter.

### `co2_grams_per_liter_to_volumes()`

```python
co2_grams_per_liter_to_volumes(grams_per_liter: float) -> float
```

Compatibility scalar API converting grams per liter to volumes of CO2.

## Complete exported-name inventory

FermUnits 0.1.3 exports the following 37 names from `fermunits`:

```text
PHValue
Q_
Quantity
absorbance_275nm_to_bitterness_units
amount_concentration_to_equivalent_concentration
amount_concentration_to_mass_concentration
amount_to_equivalents
bitterness_units_to_absorbance_275nm
caco3_basis_mass_concentration_to_equivalent_concentration
co2_grams_per_liter_to_volumes
co2_mass_concentration_to_volumes
co2_volumes_to_grams_per_liter
co2_volumes_to_mass_concentration
create_registry
ebc_to_srm
equivalent_concentration_to_amount_concentration
equivalent_concentration_to_caco3_basis_mass_concentration
equivalent_concentration_to_mass_concentration
equivalents_to_amount
gravity_points_to_sg
hydrogen_ion_activity_to_ph
lintner_to_windisch_kolbach
lovibond_to_srm_approx
mass_concentration_to_amount_concentration
mass_concentration_to_equivalent_concentration
mass_concentration_to_mass_fraction
mass_fraction_to_mass_concentration
ph_to_hydrogen_ion_activity
plato_to_sg
plato_to_wort_refractometer_brix
sg_to_gravity_points
sg_to_plato
srm_to_ebc
srm_to_lovibond_approx
ureg
windisch_kolbach_to_lintner
wort_refractometer_brix_to_plato
```

## Validation and errors

FermUnits generally validates semantic parameters before applying a relationship.
Depending on the API, invalid inputs may raise `ValueError`; incompatible unit
conversion uses Pint's normal error behavior. Examples of explicitly validated
conditions include finite pH values, positive hydrogen-ion activity, positive
solution density, positive molar mass, positive equivalence factors, and positive
equivalent mass.

Callers should not rely on private constants, private context names, internal
modules, or implementation-only helpers beginning with an underscore.

## Scientific and design references

- [`reference/brewing-units.md`](reference/brewing-units.md) — brewing units,
  calculations, verification status, and bibliographic records.
- [`reference/solution-chemistry.md`](reference/solution-chemistry.md) — solution
  chemistry, chemical-equivalent semantics, composition, density, molar mass,
  reporting bases, pH, and measurement boundaries.
- [`reference/wine-units.md`](reference/wine-units.md) — current wine-specific
  definitions and pending migration work.
- [`sources.md`](sources.md) — project-wide source hierarchy, citation rules, and
  source ledger.
- [`../DESIGN.md`](../DESIGN.md) — architectural decisions and the FermUnits/Pint
  dependency boundary.

This Markdown reference is intended to remain the single API inventory until the
project's fuller generated/user documentation is published on GitHub Pages.
