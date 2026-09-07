# Compatibility Policy

This document records the runtime and downstream compatibility contract for
FermUnits 1.x. It complements the public API reference in [`API.md`](API.md) and
the scientific verification baseline in
[`verification-status.md`](verification-status.md).

## Supported Python versions

FermUnits supports Python 3.11, 3.12, 3.13, and 3.14. The CI test matrix runs
the full pytest suite on every supported Python version. Quality gates run on
Python 3.11, the minimum supported version.

Dropping a supported Python version after 1.0 is a compatibility-policy change
and should be documented explicitly in release notes.

## Supported Pint range

FermUnits depends on Pint `>=0.25.3,<0.26`. Pint 0.25.3 is the compatibility
baseline captured by the project lockfile. The upper bound is intentional: a
new Pint feature release may change typing, definitions, parsing, registry
behavior, or object-level APIs that FermUnits deliberately exposes to
downstream consumers.

The supported Pint range must not be widened without rerunning the full
FermUnits suite, static type checks, downstream contract tests, registry
collision checks, and targeted review of any Pint release notes relevant to
FermUnits behavior.

## Downstream import boundary

Normal downstream code should be able to use FermUnits without importing Pint
directly. FermUnits therefore re-exports the Pint types or exceptions that are
part of its maintained downstream contract:

- `Quantity` for quantity annotations and runtime checks;
- `UnitRegistry` for isolated-registry annotations and runtime checks;
- `DimensionalityError` for handling dimensionally invalid conversions.

Quantity construction and registry access remain available through `Q_`,
`ureg`, and `create_registry()`. These are genuine Pint objects, so normal
object-level Pint behavior remains available through the FermUnits boundary
within the supported Pint range. FermUnits does not independently guarantee
every Pint method across unsupported future Pint releases; widening the Pint
range must review object-level compatibility as part of the FermUnits contract.

FermUnits does not re-export Pint wholesale. A Pint symbol should be added to
the FermUnits package surface only when a concrete downstream requirement makes
it part of the supported FermUnits contract. Internal implementation code and
implementation-focused tests may still import Pint directly.

## Maintained downstream contracts

FermUnits currently carries explicit contract suites for two real consumer
classes:

- Water Chemistry Engine: liquid volume, mass, concentration, amount, chemical
  equivalents, density, conductivity, temperature, pH/activity, and the US beer
  barrel boundary;
- draft-system calculations: temperature and temperature differences, pressure,
  length, flow, density, viscosity, pressure gradient, explicit US/Imperial
  volume distinctions, and quantity-aware carbonation.

These contract suites import the public types and errors they need from
`fermunits`, not from Pint. The Water Chemistry Engine contract explicitly
exercises the package-level `Quantity` type used for downstream annotations,
while both suites exercise `UnitRegistry` and `DimensionalityError`. They are
compatibility guarantees for FermUnits;
they are not application implementations and do not transfer application policy
into this library.

## Public package surface

`fermunits.__all__` is an intentional 1.x compatibility surface. A regression
test records the complete current inventory so additions and removals require an
explicit source change rather than occurring accidentally through import
refactoring.

`__version__` remains public package metadata but intentionally sits outside
`__all__`.

## 1.0 compatibility baseline

The 1.0 compatibility audit established that:

- every supported Python version passes the full suite in CI;
- the supported Pint range and upgrade policy are documented;
- maintained downstream contract suites use the FermUnits public boundary;
- the public `__all__` inventory is regression-tested;
- public registry construction and dimension-error handling do not require a
  downstream Pint import.

The release workflow resolves the GitHub release event to one immutable commit
SHA and reuses that SHA for the supported-Python test matrix, quality checks, and
artifact build. The dependency-executing build job remains read-only; a separate
minimal-permission job attaches the already-built distributions to the GitHub
release. Ordinary CI and release quality checks both verify the lockfile.

The workflow performs baseline distribution-content inspection and symmetric
isolated install/import smoke tests for both wheel and source distribution before
publication. Stable GitHub releases publish to production PyPI after those gates;
GitHub prereleases do not publish automatically to production PyPI, though their
verified artifacts may still be attached to the GitHub prerelease.

The project-specific pre-release checklist is a separate final release gate and
may repeat or extend those packaging checks after internal and external review
are complete.
