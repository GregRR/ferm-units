# Implemented Relationship Verification Status

This document records the scientific-verification baseline for behavior shipped
in FermUnits 1.0.0. It centralizes the source status recorded in the maintained
domain references so later release and review decisions do not require
reconstructing the implemented surface from several files.

This is not a second source ledger. Bibliographic records remain canonical in
[`sources.md`](sources.md), and claim-specific evidence remains in the maintained
files under [`reference/`](reference/).

## Two different kinds of stability

FermUnits tracks public-API stability separately from scientific verification.
A function name, signature, validation contract, and documented semantics may be
stable while the scientific relationship it exposes remains **Provisional**.
A 1.0 release must not silently upgrade a Provisional scientific relationship to
Verified merely because the API has become stable.

The status vocabulary in [`sources.md`](sources.md) remains authoritative:

- **Verified** means the cited authoritative source directly supports the
  numerical definition, formula, reference conditions, jurisdiction, and
  intended meaning needed by the entry.
- **Provisional** means the relationship may be useful and implemented but one
  or more verification questions remain.
- **Pending**, **Rejected**, and **Ambiguous** retain their project-wide meanings.

For this audit, the **1.0 review disposition** column is narrower:

- **Ready** — no unresolved source issue currently requires 1.0 reviewer action.
- **Retain provisional** — the API is deliberately bounded or explicitly
  approximate; the scientific status must remain visible, but stronger sourcing
  is not currently treated as a release blocker.
- **Reviewed provisional** — the relationship received explicit internal and
  external review for 1.0 and remains intentionally Provisional because the
  unresolved source questions do not invalidate the bounded public semantics.

These dispositions do not change the underlying source status.

## Source-supported shared chemistry

The shared chemistry layer was not a primary 1.0 source risk. Its conversions
use ordinary dimensional arithmetic plus explicit chemical parameters, or a
source-defined semantic relationship whose limitations are retained in the API.

| Implemented behavior | Current source status | 1.0 review disposition | Maintained reference |
|---|---|---|---|
| `equivalent`, `milliequivalent`, amount ↔ equivalents | Implemented from explicit IUPAC equivalence semantics | Ready | [`reference/solution-chemistry.md`](reference/solution-chemistry.md) |
| amount concentration ↔ equivalent concentration | Implemented; explicit equivalence factor required | Ready | [`reference/solution-chemistry.md`](reference/solution-chemistry.md) |
| mass concentration ↔ equivalent concentration | Implemented; explicit equivalent mass required | Ready | [`reference/solution-chemistry.md`](reference/solution-chemistry.md) |
| CaCO3-basis mass concentration ↔ equivalent concentration | Implemented from the conventional EPA 50 mg/mEq reporting factor; USGS uses a more precise molar-mass-derived value in its own calculations | Ready | [`reference/solution-chemistry.md`](reference/solution-chemistry.md) |
| mass concentration ↔ mass fraction | Implemented; explicit solution density required | Ready | [`reference/solution-chemistry.md`](reference/solution-chemistry.md) |
| mass concentration ↔ amount concentration | Implemented; explicit molar mass required | Ready | [`reference/solution-chemistry.md`](reference/solution-chemistry.md) |
| `PHValue` ↔ hydrogen-ion activity | **Verified** mathematical definition only; no operational measurement claim | Ready | [`reference/solution-chemistry.md`](reference/solution-chemistry.md) |

The explicit-parameter rules are part of the public contract. FermUnits does not
infer equivalence factor, equivalent mass, solution density, molar mass, chemical
identity, hydration state, or activity coefficient.

## Brewing vessel definitions

| Implemented behavior | Current source status | 1.0 review disposition | Notes |
|---|---|---|---|
| `us_beer_barrel` | **Verified** Pint behavior | Ready | Qualified FermUnits definition numerically equal to Pint `beer_barrel`. |
| `imperial_beer_barrel` | **Verified** Pint physical value; British brewing terminology **Provisional** | Retain provisional | Qualified FermUnits definition is numerically equal to Pint `imperial_barrel`; it is a distinct unit name, not a canonical Pint alias. |
| `pin_cask`, `firkin`, `kilderkin` | **Provisional** | Reviewed provisional | Current British brewing capacities are sourced, but not at the project's Verified threshold. |
| `brewing_hogshead` | **Provisional** | Reviewed provisional | Qualified brewing name avoids cross-domain ambiguity. |
| `brewing_puncheon`, `brewing_butt`, `brewing_tun` | **Provisional** historical British brewing meaning | Reviewed provisional | Names are qualified; historical source strength remains the open issue. |

The removed alpha-only `wine_hogshead` alias is not part of this audit because it
is no longer implemented. Pint's bare `hogshead` remains Pint-owned behavior.

## Brewing calculations

| Implemented relationship | Current source status | 1.0 review disposition | Main unresolved point |
|---|---|---|---|
| specific gravity ↔ gravity points | **Provisional** | Retain provisional | Ordinary brewing shorthand is sourced; below-1.000 extension and reference-condition terminology remain unverified. |
| specific gravity ↔ degrees Plato | **Provisional** | Reviewed provisional | Exact cubic is reproduced in peer-reviewed brewing literature with ASBC attribution, but primary ASBC provenance, reference conditions, range, and precision remain unverified. |
| apparent wort Brix ↔ Plato with caller-supplied correction factor | **Provisional** | Retain provisional | API is explicitly limited to unfermented wort and requires the factor from the caller; ASBC calibration procedure and factor range remain unverified. |
| SRM ↔ EBC reported color indices | **Provisional** | Reviewed provisional | Numerical scale-factor relationship is strongly corroborated, but complete primary ASBC/EBC procedural qualification has not been directly verified. |
| Lovibond ↔ SRM approximation | **Provisional** | Retain provisional | Public names explicitly include `_approx`; primary coefficient provenance, material scope, range, and error remain unverified. |
| A275 extract absorbance ↔ bitterness units | **Provisional** | Reviewed provisional | Historical numerical factor is implemented; complete current method text and procedural conditions remain unverified. |
| Lintner ↔ Windisch-Kolbach diastatic power | **Provisional** | Reviewed provisional | Conventional relationship is sourced; primary formula provenance, exactness, range, and method-equivalence scope remain unverified. |
| volumes of CO2 ↔ CO2 mass concentration | **Provisional** | Reviewed provisional | Physical/industry evidence supports the magnitude, but the normative ASBC reference state and reporting precision remain unverified. |

The corresponding detailed evidence, limitations, and unresolved questions remain
in [`reference/brewing-units.md`](reference/brewing-units.md). This table does
not replace those records.

## What is not a 1.0 source blocker

The following categories do not require implementation or source promotion merely
to satisfy the 1.0 baseline or continue normal 1.x maintenance:

- unimplemented candidates from wine, cider/perry, distilling, sake, biofuel,
  and acid-tier references;
- rejected legacy formulas;
- ordinary Pint units and arithmetic that FermUnits does not redefine;
- downstream reporting, regulatory, recipe, or engineering semantics that the
  maintained references intentionally keep outside FermUnits.

Milestone 6 established that additional domain APIs remain demand-driven. The
1.x compatibility contract does not turn those research inventories back into a
feature checklist.

## External review outcome

The 1.0 external review gave explicit attention to these implemented
Provisional areas:

1. British brewing cask capacities and historical naming support.
2. The SG ↔ Plato cubic and its reference conditions/range.
3. The SRM ↔ EBC scale-factor relationship and procedural scope.
4. The A275 analytical-bitterness factor and method scope.
5. The Lintner ↔ Windisch-Kolbach relationship and method-equivalence wording.
6. The volumes-of-CO2 reference state and reporting precision.

The review question is not simply whether each formula is familiar or commonly
used. It is whether FermUnits' exact public semantics, qualifications, and source
status are defensible for a stable 1.0 API.

The internal and external reviews found no release blocker in these bounded
relationships and retained their Provisional scientific status for 1.0. Stronger
sources may justify a future upgrade to Verified, but scientific status should
only be upgraded when the project-wide Verified criteria are met. Any future
change to a stable public semantic contract must follow the 1.x compatibility
policy.
