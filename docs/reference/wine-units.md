# Wine Units and Calculations Reference

This document records the **current FermUnits implementation status** for the
wine domain. The broader wine research inventory has not yet been migrated into
the maintained source-record format and is retained under
[`legacy/wine-inventory.txt`](legacy/wine-inventory.txt).

The legacy inventory contains useful research leads for analytical scales,
regional vessels, bottle sizes, vineyard/logistics quantities, and sparkling-
wine measurements. Proposed names or formulas in that file are not public API
commitments.

## Current implemented wine-specific definition

### `wine_hogshead`

- Definition: alias of Pint's existing `hogshead`.
- Pint value: 63 US liquid gallons.
- Purpose: expose an explicit wine-qualified name while preserving Pint's
  existing `hogshead` meaning and allowing FermUnits to define the distinct
  `brewing_hogshead` separately.
- Implementation status: **Implemented.**
- Source status: **Pint behavior verified via [SH-PINT-01]; broader historical
  wine-domain interpretation remains provisional pending migration to an
  authoritative wine source record.**

## Shared analytical foundations

FermUnits already has project-wide sources relevant to future wine work:

- [SH-OIV-01] identifies the OIV Compendium as the authoritative analytical-
  method structure for wine and must.
- [SH-OIML-01] supports Brix/refractometer measurement context and the need for
  explicit instrument and temperature conditions.
- [SH-SI-01] supplies SI dimensional anchors.
- [SH-PINT-01] records the behavior of Pint units and aliases that FermUnits
  must preserve.

These identifiers are defined in [`../sources.md`](../sources.md).

## Migration still pending

Before additional wine-specific names or calculations become maintained
FermUnits definitions, the legacy research needs to be converted into sourced,
qualified entries. Major groups include:

- density and extract scales such as Brix, Baumé, Oechsle, and KMW;
- potential-alcohol estimates;
- acidity, sulfur-dioxide, and other analytical reporting quantities;
- vineyard yield and production/logistics quantities;
- sparkling-wine pressure and dissolved-CO2 semantics;
- regional vessel capacities such as barrique, pièce, foudre, hogshead,
  puncheon, bota, and butt;
- traditional bottle-size names whose capacities can vary by region.

Variable or region-dependent terms must remain qualified rather than receiving a
single universal capacity.

Status: **Broader wine-domain migration pending.**
