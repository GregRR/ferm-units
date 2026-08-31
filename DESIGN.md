# FermUnits Design

## Purpose

FermUnits is the fermentation-domain layer on top of Pint. It provides unit
registry extensions, qualified industry meanings, semantic measurement scales,
and reusable conversions that are broadly useful across fermentation software.

FermUnits is intentionally narrower than a brewing, water-treatment, draft-
system, recipe, or process engine. It should make those applications easier to
build without absorbing their application-specific models.

## Architectural boundary

The project separates responsibilities into four layers:

1. **Pint** owns ordinary physical quantities, units, dimensional analysis,
   prefixes, compound units, and routine unit conversion.
2. **FermUnits** owns fermentation-specific definitions, qualified meanings,
   semantic scales, and reusable conversions whose meaning is broader than one
   downstream application.
3. **Downstream engineering applications** own system models and decisions such
   as water-treatment optimization, draft-system balance, recipe estimation,
   equipment behavior, and process simulation.
4. **Downstream measurement and serialization models** own measurement-result
   semantics such as source-reported precision, qualifiers, bounds and ranges,
   detection and quantitation metadata, uncertainty declarations, provenance,
   and application records.

A feature belongs in FermUnits only when its meaning is reusable across
fermentation applications and does not require an application-specific model.

FermUnits may provide a reusable transformation for a semantic scale when the
scientific definition itself is stable and explicit. It does not thereby own the
laboratory method, uncertainty model, reporting qualifier, or application policy
used to interpret a measurement result on that scale.

## Pint-first registry design

Pint remains the physical-unit engine. FermUnits does not duplicate units that
Pint already represents correctly.

Before adding a registry definition, FermUnits should determine whether Pint
already provides the unit, alias, prefix, or compound expression. A new
FermUnits definition is justified when the fermentation domain needs a meaning
that Pint genuinely lacks or when an explicit qualified name is required to
avoid ambiguity.

Examples:

- `hectoliter`, `psi`, `milligram / liter`, and `mole / liter` are ordinary Pint
  expressions and do not need FermUnits aliases.
- `firkin` and `brewing_hogshead` encode fermentation-industry vessel meanings
  not safely represented by a generic unqualified name.
- `equivalent` is a FermUnits registry extension because chemical equivalents
  require semantics that are not supplied by Pint's default registry.

## Naming and collisions

Existing legitimate Pint meanings are preserved.

When one plain-language term has multiple legitimate meanings, FermUnits uses a
qualified name rather than silently replacing Pint's definition. Bare generic
terms such as `barrel`, `butt`, `puncheon`, or `tun` are not assigned one universal
fermentation meaning when region, industry, or history changes the capacity.

Qualified names should communicate the distinction directly, for example
`brewing_hogshead` versus `wine_hogshead`.

## Physical units versus semantic scales

Not every fermentation measurement should become a Pint unit.

Ordinary multiplicative physical quantities belong in the registry. Analytical
indices, empirical scales, and method-defined measurements are represented by
explicit functions when their meaning depends on a method, reference condition,
or non-linear relationship.

Examples include:

- specific gravity and gravity points;
- degrees Plato and wort refractometer correction;
- SRM, EBC, and approximate Lovibond relationships;
- analytical bitterness units;
- Lintner and Windisch-Kolbach diastatic power;
- volumes of dissolved carbon dioxide.

Function names and documentation should make approximations and method-specific
meanings visible rather than making them look like universal unit identities.

## Explicit physical and chemical parameters

FermUnits does not hide assumptions needed to make a conversion physically or
chemically meaningful.

Conversions that depend on density, molar mass, equivalent mass, charge or
reaction basis, calibration factors, reference conditions, or similar context
must receive that information explicitly unless a definition is genuinely
universal.

Examples include:

- mass concentration to mass fraction requires solution density;
- mass concentration to amount concentration requires molar mass;
- amount to chemical equivalents requires an equivalence factor;
- wort refractometer correction requires a caller-supplied correction factor.

This rule prevents convenient-looking APIs from silently embedding assumptions
that are wrong for some downstream applications.

When an explicit parameter is consumed by a registered Pint context, the context
transformation itself must enforce the same physical validity rules as any
public convenience wrapper. Wrapper validation remains useful defense in
depth, but direct registry/context use must not bypass those invariants.

## Source and scientific status

Implementation status and source-verification status are separate.

A conversion may be useful and tested in software while its scientific
relationship remains provisional. Conversely, a definition may be well sourced
before it is implemented.

The project-wide status vocabulary and source-quality hierarchy are defined in
[`docs/sources.md`](docs/sources.md). Maintained domain inventories live under
[`docs/reference/`](docs/reference/). Brewing relationships awaiting direct
ASBC/EBC confirmation are tracked in
[`docs/asbc-verification.md`](docs/asbc-verification.md).

Unsupported formulas are not implemented merely because they appear in a legacy
inventory or common secondary reference.

## Downstream contracts

FermUnits may include contract tests for downstream applications when those
tests protect the unit boundary without importing the application's model.

For example, the Water Chemistry Engine contract tests confirm that required physical
units parse, convert, and retain the expected dimensionality. The draft-system
contract similarly verifies temperature, temperature differences, pressure,
length, flow, density, viscosity, pressure-gradient, and CO2 mass-concentration
quantities without moving draft-system balance or gas-equilibrium calculations
into FermUnits.

The draft-system boundary intentionally preserves several semantic distinctions:

- gauge versus absolute pressure is metadata about the pressure reference, not a
  separate `psig` or `psia` unit;
- tubing restriction is represented dimensionally as pressure drop per length,
  such as `psi / foot`, not literal force per length;
- explicit US-liquid aliases are preferred where US and Imperial volume names
  could otherwise be confused;
- carbonation may cross the boundary as a Pint mass-concentration quantity,
  while the beverage-industry "volumes CO2" value remains an explicit semantic
  scale handled by FermUnits conversion functions.

These tests are compatibility guarantees for FermUnits behavior, not application
implementations.

## Public API and compatibility

The package-level API in `fermunits.__init__` is the primary supported import
surface. New public functions should be typed, tested, documented, and exported
there intentionally.

Registry aliases require particular care because adding or changing a unit name
can alter parsing globally for every downstream user of the registry.

FermUnits is currently alpha software. Public APIs and domain coverage may still
evolve before 1.0, but changes should preserve clear semantics and avoid silent
reinterpretation of existing names or values.

## Non-goals

FermUnits does not aim to provide complete implementations of:

- recipe formulation or ingredient databases;
- IBU recipe-estimation models such as Tinseth or Rager;
- water-treatment optimization or mash-pH prediction;
- draft-system balancing, equipment-loss models, or gas blending;
- fermentation process control or hardware interfaces;
- a persistence or interchange schema.

Those concerns belong in downstream libraries or applications. FermUnits should
provide the unit-aware building blocks they need.
