# FermUnits Reference Inventories

This directory contains the maintained technical inventories used to describe
FermUnits definitions, domain-specific calculations, implementation status, and
source-verification status.

The maintained files are not wish lists. Entries distinguish current public
behavior from proposed work and identify whether a term is a physical unit, a
method-defined scale, a reusable calculation, or application-level semantics
that belong outside FermUnits.

## Files

| Domain | Reference file | Current state |
|---|---|---|
| Solution chemistry | [solution-chemistry.md](solution-chemistry.md) | Active and partly implemented |
| Brewing | [brewing-units.md](brewing-units.md) | Active; current implementation reconciled |
| Wine | [wine-units.md](wine-units.md) | Legacy migration triaged; source-ready candidates and ownership boundaries documented |
| Distilling | [distilling-units.md](distilling-units.md) | Legacy migration triaged; legal/metrological ownership boundaries documented |
| Sake | [sake-units.md](sake-units.md) | Legacy migration triaged; analytical and historical-unit ownership boundaries documented |
| Cider and perry | [cider-perry-units.md](cider-perry-units.md) | Legacy migration triaged; ownership boundaries documented |
| Biofuels | [biofuel-units.md](biofuel-units.md) | Legacy migration triaged; process-rate and feedstock ownership boundaries documented |
| Acid-tier and other fermentation | [acid-tier-units.md](acid-tier-units.md) | Legacy migration triaged; microbiological, acidity, and food-process ownership boundaries documented |

The maintained domain files are the source documents for current FermUnits
behavior and planned definitions. All six legacy Milestone 6 domain inventories
have now been migrated and triaged into these maintained references. A
project-wide inventory may be generated from them, but should not be maintained
independently.

## Legacy research inventories

The original planning inventories are retained in [`legacy/`](legacy/). They may
contain superseded formulas, unsupported assumptions, provisional names, or
research leads that were never implemented. They are preserved for historical
context and future source investigation, not as normative FermUnits
documentation.

## Required entry fields

Every stable or proposed entry should identify, as applicable:

- the preferred FermUnits name;
- accepted aliases;
- rejected or ambiguous aliases;
- the exact numerical definition or calculation;
- dimensionality and reference conditions;
- jurisdiction, region, industry, or analytical method;
- modern, historical, customary, legal, or provisional status;
- implementation status;
- one or more source identifiers.

Source identifiers always have a canonical record in the master ledger at
[`../sources.md`](../sources.md). Domain files may repeat claim-specific source
context or limitations beside the entries they support.

## Source identifiers

Domain source identifiers use a short prefix:

- `SC-` — shared solution chemistry
- `BR-` — brewing
- `WI-` — wine
- `DI-` — distilling
- `SA-` — sake
- `CP-` — cider and perry
- `BF-` — biofuels
- `AT-` — acid-tier and other fermentation
- `SH-` — shared project sources

Example:

```text
Sources: [SC-IUPAC-01], [SH-SI-01]
Status: Verified physical definition; analytical application provisional.
```

Every source used by maintained documentation must be defined in
[`../sources.md`](../sources.md). A domain reference may repeat the same source
record or a claim-specific subset for readability, but the identifier and
bibliographic facts must remain consistent with the master ledger.

## Status vocabulary

Use the status terms defined in [`../sources.md`](../sources.md). In brief:

- **Verified** — the cited authoritative source directly supports the claim.
- **Provisional** — useful and implemented or proposed, but not yet supported
  strongly enough to be stable.
- **Pending** — further source verification is still required.
- **Rejected** — reviewed and intentionally not used.
- **Ambiguous** — the unqualified name has multiple legitimate meanings.

Implementation and source status are separate. A function may be implemented
while its scientific relationship remains provisional.

## Naming rules

- Preserve legitimate Pint definitions.
- Add domain-qualified names when a plain term has multiple legitimate meanings.
- Do not assign a universal value to a variable regional or historical term.
- Keep analytical scales and empirical calculations separate from ordinary
  multiplicative physical units.
- Record aliases that were considered and rejected.
