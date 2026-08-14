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
| Solution chemistry | [`reference/solution-chemistry.md`](reference/solution-chemistry.md) | Active and partly implemented |
| Brewing | [`reference/brewing-units.md`](reference/brewing-units.md) | Active; implementation and verification status reconciled |
| Wine | [`reference/wine-units.md`](reference/wine-units.md) | Current implementation status documented; broader migration pending |
| Distilling | — | Migration pending |
| Sake | — | Migration pending |
| Cider and perry | — | Migration pending |
| Biofuels | — | Migration pending |
| Acid-tier and other fermentation | — | Migration pending |

Historical planning inventories are retained under
[`reference/legacy/`](reference/legacy/) as research context only. They are not
current FermUnits specifications.

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

### [SH-PUBCHEM-CO2-01] PubChem — Carbon Dioxide physical properties

- Organization: National Library of Medicine, National Center for Biotechnology
  Information (PubChem)
- Record: Carbon Dioxide, CID 280
- URL: https://pubchem.ncbi.nlm.nih.gov/compound/280
- Accessed: 2026-08-12
- Tier: 3
- Supports:
  - CO2 gas density of approximately `1.976 g/L` at `0 °C` and `760 mmHg`.
- Limitation:
  - physical-property support only; does not establish the normative
    brewing-industry definition or reporting convention for "volumes of CO2."

### [SH-UF-CO2-01] A Guide to Carbonating Beverages at Small Scale

- Organization: University of Florida IFAS Extension
- Authors: Xuwei Song, Nicholas Wendrick, Charles A. Sims, Andrew MacIntosh
- Publication: FS379
- URL: https://ask.ifas.ufl.edu/publication/FS379
- Accessed: 2026-08-12
- Tier: 6
- Supports:
  - beverage carbonation reported as grams CO2 per liter or volumes of CO2 at
    STP per volume of liquid;
  - the guide's operational conversion `1 vol/vol = 1.96 g/L`.
- Limitation:
  - technical extension guidance rather than an ASBC/EBC analytical standard;
  - the `1.96 g/L` value is the guide's calculation convention and differs
    from the ASBC/EBC-associated approximately `1.976 g/L` factor retained by
    FermUnits.

### [SH-OIV-01] Compendium of International Methods of Wine and Must Analysis

- Organization: International Organisation of Vine and Wine (OIV)
- URL: https://www.oiv.int/standards/compendium-of-international-methods-of-wine-and-must-analysis
- Accessed: 2026-08-03
- Tier: 2
- Supports:
  - authoritative analytical-method structure for wine and must;
  - methods shared with wine, cider, distilling, and other fermented-beverage
    work where applicable.
