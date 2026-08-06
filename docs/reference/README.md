# FermUnits Reference Inventories

This directory contains the maintained technical inventories used to plan,
implement, test, and review FermUnits definitions and domain-specific
calculations.

The reference files are not merely wish lists. Each entry should state what the
term means, where it is used, whether it is a physical unit or a method-defined
scale, how FermUnits intends to represent it, and which sources support the
claim.

## Files

| Domain | Reference file | Current state |
|---|---|---|
| Solution chemistry | [solution-chemistry.md](solution-chemistry.md) | Active and partly implemented |
| Brewing | [brewing-units.md](brewing-units.md) | Revised and sourced |
| Wine | [wine-units.md](wine-units.md) | Revised and sourced |
| Distilling | `distilling-units.md` | Migration pending |
| Sake | `sake-units.md` | Migration pending |
| Cider and perry | `cider-perry-units.md` | Migration pending |
| Biofuels | `biofuel-units.md` | Migration pending |
| Acid-tier and other fermentation | `acid-tier-units.md` | Migration pending |

The domain files are the maintained source documents. A combined project-wide
inventory may be generated from them, but it should not be edited independently.

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

Source identifiers point to the bibliography at the bottom of the same domain
file or to a shared source recorded in [`../sources.md`](../sources.md).

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

Examples:

```text
Sources: [WI-OIV-01], [SH-OIML-01]
Status: Verified physical definition; analytical application provisional.
```

A source identifier must be defined exactly once. Domain-specific sources belong
in the bibliography of that domain file. Sources used across multiple domains
belong in `docs/sources.md`.

## Status vocabulary

Use the status terms defined in [`../sources.md`](../sources.md). In brief:

- **Verified** — the cited authoritative source directly supports the claim.
- **Provisional** — useful and implemented or proposed, but not yet supported
  strongly enough to be stable.
- **Pending** — research or restricted-source review is still required.
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

## Copyright and restricted methods

Do not commit full copyrighted methods, restricted tables, scans, or substantial
verbatim extracts unless the project has permission to redistribute them.

It is appropriate to record:

- method titles and identifiers;
- bibliographic citations;
- URLs;
- concise original summaries;
- formulas or definitions that may lawfully be recorded;
- notes describing what still needs verification.

When a restricted authoritative method is known to exist, mark the item pending
and use the strongest accessible supporting source without claiming that the
restricted text was reviewed.
