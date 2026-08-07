# Definition sources

Every FermUnits definition must be traceable to a reliable source before it is
considered stable. Domain bibliographies live in the corresponding files under
[`reference/`](reference/). This file defines the project-wide sourcing policy,
status vocabulary, citation conventions, and shared sources.

## Source-quality hierarchy

Prefer sources in this order. A lower-tier source may be used provisionally when
a higher-tier source is inaccessible, but the status must make that limitation
clear.

1. **Law, regulation, and formal standards**
   - statutes, regulations, metrology standards, official legal definitions;
   - examples: eCFR, UK legislation, OIML, BIPM.
2. **Authoritative analytical and industry methods**
   - official methods from ASBC, EBC, OIV, ISO, AOAC, TTB, HMRC, or comparable
     bodies.
3. **Government and national metrology guidance**
   - NIST and equivalent national laboratories or agencies.
4. **Official regional or industry organizations**
   - recognized research institutes, appellation bodies, trade organizations,
     and producer councils such as AWRI, Comité Champagne, BIVB, and the Consejo
     Regulador de Jerez.
5. **Peer-reviewed scientific literature**
   - especially papers that establish or validate an empirical relationship.
6. **Technical books and instrument documentation**
   - useful when the method, calibration, and valid range are explicit.
7. **General secondary references**
   - acceptable as discovery leads or provisional support only; they should not
     be the sole basis for a stable definition when stronger sources exist.

Pint's own definition files are authoritative for what Pint currently defines,
but they are not automatically authoritative for the historical or
industry-specific meaning of a disputed term.

## Required source record

Each source record should include:

- source identifier;
- title;
- issuing organization or author;
- URL, DOI, statute citation, or publication details;
- date accessed;
- source tier;
- the entries or claims it supports;
- any limitations, such as restricted access or indirect support.

## Citation conventions

- Put source identifiers directly in the relevant entry.
- Use domain prefixes such as `BR-` and `WI-`.
- Use `SH-` only for sources shared across domains.
- Do not cite a source for a claim it does not directly support.
- Distinguish a source that proves a method exists from a source that exposes
  the method's detailed equation or table.
- Cite the exact method number when known.
- Retain a stable publication citation even when a URL may later change.
- Record the access date in ISO format: `YYYY-MM-DD`.
- When a webpage changes materially, recheck the supported entries and update
  the access date.

## Status definitions

### Verified

The cited authoritative source directly supports the numerical definition,
formula, reference conditions, jurisdiction, and intended meaning needed by the
entry.

A verified item may still be unimplemented.

### Provisional

The relationship is useful enough to document or implement, but one or more of
the following remains unresolved:

- primary-source confirmation;
- valid range;
- reference temperature or pressure;
- reporting precision;
- method dependence;
- regional scope.

Provisional items must not be presented as stable universal definitions.

### Pending

The project has identified the term or authoritative method, but does not yet
have enough accessible information to define or implement it responsibly.

### Rejected

The project reviewed the proposed definition or formula and intentionally chose
not to use it. Record the reason, such as dimensional inconsistency, missing
reference conditions, implausible results, or an ambiguous name.

### Ambiguous

The plain term has more than one legitimate meaning. Preserve existing
legitimate Pint behavior and use explicit domain- or region-qualified names for
FermUnits definitions.

## Domain reference index

| Domain | File | Notes |
|---|---|---|
| Brewing | [`reference/brewing-units.md`](reference/brewing-units.md) | Revised and sourced |
| Wine | [`reference/wine-units.md`](reference/wine-units.md) | Revised and sourced |
| Distilling | `reference/distilling-units.md` | Migration pending |
| Sake | `reference/sake-units.md` | Migration pending |
| Cider and perry | `reference/cider-perry-units.md` | Migration pending |
| Biofuels | `reference/biofuel-units.md` | Migration pending |
| Acid-tier and other fermentation | `reference/acid-tier-units.md` | Migration pending |

The domain files contain their own bibliographies. Do not duplicate those full
bibliographies here.

## Shared sources

### [SH-SI-01] The International System of Units (SI Brochure)

- Organization: Bureau International des Poids et Mesures (BIPM)
- URL: https://www.bipm.org/en/publications/si-brochure
- Accessed: 2026-08-03
- Tier: 1
- Supports:
  - SI base and derived units;
  - accepted non-SI units used with SI;
  - dimensional anchors used throughout FermUnits.

### [SH-PINT-01] Pint default unit definitions

- Organization: Pint project
- Title: `pint/default_en.txt`
- URL: https://github.com/hgrecco/pint/blob/master/pint/default_en.txt
- Accessed: 2026-08-03
- Tier: project-primary source for Pint behavior
- Supports:
  - the exact units and aliases currently supplied by Pint;
  - collision checks for `beer_barrel`, `hogshead`, `imperial_gallon`, and
    other built-ins.
- Limitation:
  - does not establish that Pint's historical interpretation is the only
    legitimate industry meaning.

### [SH-OIML-01] OIML R 142-1:2025 — Automated refractometers

- Organization: International Organization of Legal Metrology
- URL: https://www.oiml.org/en/files/pdf_r/r142-1-e25.pdf
- Accessed: 2026-08-03
- Tier: 1
- Supports:
  - Brix as a sucrose mass-fraction scale associated with refractometer
    measurement;
  - the need for defined instrument and temperature conditions.
- Limitation:
  - does not make a wort or grape-must refractometer reading chemically
    identical to fermentable sugar concentration.

### [SH-NIST-01] Testing of Hydrometers — NBS Circular 555

- Organization: National Bureau of Standards, now NIST
- Publication: Circular 555, 1954
- URL: https://www.nist.gov/system/files/documents/calibrations/circ555.pdf
- Accessed: 2026-08-03
- Tier: 3
- Supports:
  - hydrometer calibration principles;
  - temperature effects on the liquid and instrument;
  - the need for explicit reference conditions.
- Limitation:
  - not a brewing- or wine-specific correction table.

### [SH-OIV-01] Compendium of International Methods of Wine and Must Analysis

- Organization: International Organisation of Vine and Wine (OIV)
- URL: https://www.oiv.int/standards/compendium-of-international-methods-of-wine-and-must-analysis
- Accessed: 2026-08-03
- Tier: 2
- Supports:
  - authoritative analytical-method structure for wine and must;
  - methods shared with wine, cider, distilling, and other fermented-beverage
    work where applicable.

## Restricted and copyrighted material

Do not commit:

- full ASBC, EBC, ISO, OIV, or other methods when redistribution is restricted;
- copied proprietary tables;
- scans or photographs of copyrighted books or paywalled standards;
- long verbatim passages from technical publications.

Do commit:

- method names and numbers;
- complete bibliographic records;
- concise original summaries;
- implementation decisions and unresolved questions;
- formulas that are independently established and lawfully documented;
- test values derived from redistributable or user-supplied sources.

If a friend or collaborator provides access to a restricted publication, use it
to verify the implementation and record the citation. Do not add the restricted
pages themselves to the repository.
