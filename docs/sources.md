# Definition sources

Every FermUnits definition must be traceable to a reliable source before it is
considered stable. This file is the project's master source ledger as well as the
project-wide sourcing policy, status vocabulary, and citation guide. Domain
reference files under [`reference/`](reference/) cite these source identifiers and
may repeat claim-specific context or limitations for readability, but every source
actually relied on for a maintained project claim must also have a record here.

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
- Discovery or corroborating material mentioned in an external review does not
  automatically become a project source. If the project adopts that material to
  support a maintained claim or implementation decision, add it to this master
  ledger before citing it from maintained documentation.

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
- URL: https://github.com/hgrecco/pint/blob/0.25.3/pint/default_en.txt
- Accessed: 2026-08-30
- Tier: project-primary source for Pint behavior
- Supports:
  - the exact units and aliases currently supplied by Pint;
  - collision checks for `barrel`, `beer_barrel`, `hogshead`,
    `imperial_barrel`, `imperial_gallon`, and other built-ins in the supported
    Pint 0.25.3 line;
  - preservation of `pH` as the prefixed SI spelling picohenry (`p` pico +
    `H` henry), rather than reassigning that spelling to the chemical pH scale.
- Limitation:
  - does not establish that Pint's historical interpretation is the only
    legitimate industry meaning.

### [SH-JCGM-VIM-01] International Vocabulary of Metrology (VIM), 3rd edition

- Organization: Joint Committee for Guides in Metrology (JCGM)
- Publication: JCGM 200:2012, *International vocabulary of metrology — Basic
  and general concepts and associated terms (VIM)*, 3rd edition
- Online entries: https://jcgm.bipm.org/vim/en/
- Accessed: 2026-08-30
- Tier: 1
- Supports:
  - a measurement result as a quantity value together with other relevant
    information;
  - measurement uncertainty as a non-negative parameter characterizing the
    dispersion of quantity values attributed to a measurand;
  - detection limit as procedure- and error-probability-dependent measurement
    semantics rather than a physical unit;
  - the distinction between a measuring interval/range and a detection limit.

### [SH-PINT-MEASUREMENT-01] Pint 0.25.3 — Using Measurements

- Organization: Pint project
- Source: `docs/advanced/measurement.rst` from Pint 0.25.3
- URL: https://github.com/hgrecco/pint/blob/0.25.3/docs/advanced/measurement.rst
- Accessed: 2026-08-30
- Tier: project-primary source for Pint behavior
- Supports:
  - Pint's optional `Measurement` support when the third-party
    `uncertainties` package is installed;
  - the documented limitation that only linear combinations are currently
    supported.
- Limitation:
  - does not provide FermUnits with a complete metrology/reporting model and is
    not a reason to add `uncertainties` as a FermUnits runtime dependency.

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

## Brewing sources

The records below are the master bibliography for maintained brewing claims.
`docs/reference/brewing-units.md` may repeat these records beside the claims they
support, but this ledger is the canonical project-wide source inventory.

### [BR-CAMRA-CASK-01] Or, does Whitbread know its kil from its firkin?

- Organization: Campaign for Real Ale (CAMRA), South Hants branch
- Publication: *Hop Press*, September 1995
- URL: https://shants.camra.org.uk/hop-press/hop-press40.php
- Accessed: 2026-08-30
- Tier: 4
- Supports:
  - pin as 4.5 gallons, firkin as 9 gallons, kilderkin as 18 gallons,
    brewery barrel as 36 gallons, and hogshead as 54 gallons;
  - the hierarchy of those sizes as multiples/submultiples of the 36-gallon
    brewery barrel;
  - continued British brewing use of the smaller cask names.
- Limitation:
  - does not document the larger historical puncheon, butt, or tun hierarchy.

### [BR-NOTTINGHAM-CASK-01] Volumes or Capacity

- Organization: University of Nottingham, Manuscripts and Special Collections
- URL: https://www.nottingham.ac.uk/manuscriptsandspecialcollections/researchguidance/weightsandmeasures/volumes.aspx
- Accessed: 2026-08-30
- Tier: 7
- Supports:
  - the after-1803 beer/ale hierarchy `4.5 gallons = pin`, `2 pins = firkin`,
    `2 firkins = kilderkin`, `2 kilderkins = barrel`;
  - `1.5 barrels = 54 gallons = hogshead`;
  - `2 barrels = 72 gallons = puncheon`;
  - `2 hogsheads = 108 gallons = butt`;
  - `3 puncheons = 216 gallons = tun`;
  - separation of beer/ale measures from different wine/spirit cask meanings.
- Limitation:
  - historical research guidance rather than a current statutory brewery-cask
    standard;
  - the page spans multiple historical measurement systems, so the large-cask
    names are retained as explicitly historical/qualified meanings.

### [BR-UK-WM-1824] Weights and Measures Act 1824 (5 Geo. IV c. 74)

- Organization: Parliament of the United Kingdom
- URL: https://www.legislation.gov.uk/ukpga/1824/74/pdfs/ukpga_18240074_en.pdf
- Accessed: 2026-08-30
- Tier: 1
- Supports:
  - establishment of the Imperial gallon as the standard measure of capacity;
  - application of that common standard to wine, beer, ale, spirits, and other
    liquids;
  - use of parts and multiples of the Imperial gallon after the Act took effect.
- Limitation:
  - does not itself enumerate every brewery-cask multiple used by FermUnits.

### [BR-CHA-GU-2021] Beer Math—Working With Percentages and Gravity Units

- Author: Aaron Brown
- Organization: Canadian Homebrewers Association
- URL: https://canadahomebrews.ca/2021/04/08/beer-math-working-with-percentages-and-gravity-units/
- Accessed: 2026-08-30
- Tier: 4
- Supports:
  - gravity units/points as the digits after the decimal place of specific
    gravity multiplied by 1000;
  - the concrete brewing convention that SG `1.046` corresponds to 46 gravity
    points.
- Limitations:
  - brewing-practice guidance rather than an ASBC analytical method;
  - does not establish a specific-gravity reference temperature or reporting
    precision;
  - does not independently standardize the algebraic extension to negative
    gravity points for SG below 1.000.

### [BR-QUEK-2019] Molecular structure-property relations controlling mashing performance of amylases as a function of barley grain size

- Authors: Wei Ping Quek, Wenwen Yu, Glen P. Fox, Robert G. Gilbert
- Publication: *Amylase*, 3(1), 1–18, 2019
- DOI: https://doi.org/10.1515/amylase-2019-0001
- Accessed: 2026-08-30
- Tier: 5
- Supports:
  - the exact implemented cubic coefficients for conversion from specific
    gravity to degrees Plato;
  - attribution of that equation to the American Society of Brewing Chemists in
    peer-reviewed brewing research.
- Limitations:
  - this is a secondary use of the equation, not the primary ASBC table or
    method;
  - it does not establish the equation's original provenance, normative
    reference conditions, complete validity range, or ASBC reporting precision.

### [BR-BUHL-2024] Physical Equations Relating Extract and Relative Density

- Author: Josh Buhl
- Publication: *Journal of the American Society of Brewing Chemists*, 82(3),
  225–237, 2024
- DOI: https://doi.org/10.1080/03610470.2023.2267947
- Accessed: 2026-08-30
- Tier: 5
- Supports:
  - ASBC extract tables as reference data for evaluating relationships between
    relative density and percent-by-mass extract;
  - continued modern analytical interest in converting between those
    quantities.
- Limitations:
  - does not establish the provenance or coefficients of FermUnits' implemented
    cubic;
  - does not by itself establish the cubic's normative reference conditions,
    validity range, or reporting precision.

### [BR-THESSELING-2019] A Hands-On Guide to Brewing and Analyzing Beer in the Laboratory

- Authors: Florian A. Thesseling, Peter W. Bircham, Stijn Mertens, Karin
  Voordeckers, Kevin J. Verstrepen
- Publication: *Current Protocols in Microbiology*, 54(1), e91, 2019
- DOI: https://doi.org/10.1002/cpmc.91
- PMCID: PMC9286407
- Accessed: 2026-08-30
- Tier: 5
- Supports:
  - degrees Plato as a brewing measure tied to mass percentage of dissolved
    solids in wort;
  - the sucrose-solution reference meaning used to interpret degrees Plato;
  - `EBC = 25 * dilution factor * A430` for spectrophotometric wort/beer color;
  - the rounded modern color relation `SRM = 0.508 * EBC`.
- Limitations:
  - does not establish the provenance, coefficients, or range of FermUnits'
    SG-to-Plato polynomial;
  - does not establish a universal Brix/Plato/Balling conversion rule;
  - gives the rounded SRM/EBC presentation factor rather than primary ASBC/EBC
    method text.

### [BR-BREWERSFRIEND-WCF-01] How to Determine your Refractometer’s Wort Correction Factor

- Organization: Brewer's Friend
- URL: https://www.brewersfriend.com/how-to-determine-your-refractometers-wort-correction-factor/
- Accessed: 2026-08-30
- Tier: 7
- Supports:
  - the practical convention `WCF = raw refractometer Brix WRI / reference
    hydrometer-derived Brix/Plato`;
  - applying WCF by dividing the raw refractometer reading by the factor;
  - use of unfermented wort only for this simple calibration because alcohol
    changes the refractometer reading.
- Limitations:
  - homebrewing technical guidance rather than an ASBC/EBC analytical standard;
  - does not establish a universal factor, formal validity range, or a
    fermented-sample alcohol-correction model.

### [BR-ASBC-COLOR-01] ASBC Beer 10A — Color—Spectrophotometric Color Method

- Organization: American Society of Brewing Chemists (ASBC)
- Publication: *The Brewing Science Laboratory*, Chapter 15 data sheets
- URL: https://my.asbcnet.org/ASBCStore/Product-Detail.aspx?WebsiteKey=c6851855-80ea-47cf-9f71-647744bd0529&iProductCode=96360
- Accessed: 2026-08-30
- Tier: 2
- Supports:
  - the authoritative method identity `Beer 10A`;
  - its title as the spectrophotometric color method for beer.
- Limitation:
  - the public product page identifies the method but does not expose its full
    procedure or numerical scale-factor details.

### [BR-EBC-COLOR-01] Analytica EBC 9.6 — Colour of Beer: Spectrophotometric Method (IM)

- Organization: European Brewery Convention / Brewers of Europe
- URL: https://brewup.eu/ebc-analytica/beer/colour-of-beer-spectrophotometric-method-im/9.6
- Accessed: 2026-08-30
- Tier: 2
- Supports:
  - the current EBC method identity `9.6`;
  - spectrophotometric determination of beer color;
  - the method's dependency on EBC Method 8.5 for wort color.
- Limitation:
  - the public method page does not expose the full procedure or scale-factor
    equation.

### [BR-BAMFORTH-COLOR-2014] Color Chemistry: Red and White Beer for St. George's Day

- Presenter: Charles W. Bamforth, UC Davis
- Organization: American Chemical Society Webinars
- Date: 2014-04-17
- URL: https://www.acs.org/content/dam/acsorg/acs-webinars/2014/slides/2014-04-17-beer-color.pdf
- Accessed: 2026-08-30
- Tier: 6
- Supports:
  - 430 nm as the color measurement wavelength;
  - `A430 * 12.7` for ASBC/SRM color in a 10 mm cuvette;
  - `A430 * 25` for EBC color;
  - the direct `25 / 12.7` scale-factor relationship used by FermUnits.
- Limitations:
  - expert technical presentation rather than the primary ASBC/EBC method text;
  - does not replace procedural requirements of the formal methods.

### [BR-BYO-MALT-COLOR-01] Understanding Malt COAs

- Organization: Brew Your Own
- URL: https://byo.com/articles/understanding-malt-coas/
- Accessed: 2026-08-30
- Tier: 7
- Supports:
  - contemporary brewing use of Lovibond, SRM, and EBC on malt certificates of
    analysis;
  - the common approximation `Lovibond = (SRM + 0.76) / 1.3546`;
  - the warning that Lovibond and SRM diverge increasingly above pale/base-malt
    colors.
- Limitations:
  - secondary brewing guidance, not primary provenance for the coefficients;
  - does not establish a formal validity range or expected error.

### [BR-ASBC-BEER23-01] ASBC Beer 23A — Beer Bitterness—Bitterness Units (International Method)

- Organization: American Society of Brewing Chemists (ASBC)
- Publication: *The Brewing Science Laboratory*, Chapter 15 data sheets
- URL: https://my.asbcnet.org/ASBCStore/Product-Detail.aspx?WebsiteKey=c6851855-80ea-47cf-9f71-647744bd0529&iProductCode=96360
- Accessed: 2026-08-30
- Tier: 2
- Supports:
  - the authoritative method identity `Beer 23A`;
  - its status as the international bitterness-unit method for beer.
- Limitation:
  - the public product page identifies the method but does not expose the full
    analytical procedure.

### [BR-ASBC-SHELLHAMMER-2016] Beer 23 — International Bitterness Unit

- Presenter: Thomas H. Shellhammer, Oregon State University
- Event: 2016 World Brewing Congress / ASBC proceedings
- URL: https://www.asbcnet.org/events/archives/2016/proceedings/Documents/W_Hops_Shellhammer.pdf
- Accessed: 2026-08-30
- Tier: 4
- Supports:
  - acidic liquid-liquid extraction of beer bitter compounds into a nonpolar
    solvent before measurement;
  - absorbance measurement at 275 nm;
  - `absorbance at 275 nm * 50 = bitterness units`;
  - explicit distinction between bitterness units and one ppm iso-alpha-acid;
  - contribution of iso-alpha-acids, oxidized hop acids, polyphenols, and other
    compounds to the extracted/absorbing material.
- Limitation:
  - conference educational material rather than the full Beer-23A method text.

### [BR-EBC-BISHOP-1967] The E.B.C. Scale of Bitterness

- Author: L. R. Bishop
- Issuing body: Analysis Committee of the European Brewery Convention
- Publication: *Journal of the Institute of Brewing*, 73(6), 525–527, 1967
- DOI: https://doi.org/10.1002/j.2050-0416.1967.tb03078.x
- Accessed: 2026-08-30
- Tier: 4
- Supports:
  - the coordinated EBC bitterness-unit reporting relationship
    `EBC bitterness units = A275 * 50`;
  - adoption of a common reporting scale across the then-current EBC bitterness
    procedures.
- Limitation:
  - historical EBC Analysis Committee publication; it does not replace the
    complete current Beer-23A or EBC 9.8 analytical procedure.

### [BR-EBC-BITTERNESS-01] Analytica EBC 9.8 — Bitterness of Beer (IM)

- Organization: European Brewery Convention / Brewers of Europe
- URL: https://brewup.eu/ebc-analytica/beer/bitterness-of-beer-im/9.8
- Accessed: 2026-08-30
- Tier: 2
- Supports:
  - the current EBC method identity `9.8`;
  - determination of bitter substances in beer, mainly iso-alpha-acids;
  - the 2020 precision update including collaborative data for dry-hopped beers.
- Limitation:
  - the public method page does not expose the full analytical procedure or the
    numerical reporting equation.

### [BR-ASBC-DRYHOP-2010] Determination of Bitterness Units and Iso-alpha-acid Levels in Dry-Hopped Beers

- Organization: American Society of Brewing Chemists (ASBC)
- Publication: ASBC Technical Committee/Subcommittee Report, 2010
- DOI: https://doi.org/10.1094/ASBCJ-2010-0825-01
- URL: https://www.asbcnet.org/publications/TechReports/2010Technical_Sub_Committee_Reports.pdf
- Accessed: 2026-08-30
- Tier: 2
- Supports:
  - Beer-23 bitterness units as operational measurements distinct from HPLC
    iso-alpha-acid concentration;
  - the observed divergence between IBU and iso-alpha-acid results in dry-hopped
    beer;
  - the need to avoid interpreting IBU as direct sensory bitterness.
- Limitation:
  - focused on comparative method performance in dry-hopped beer, not a
    replacement for the Beer-23A procedure itself.

### [BR-ASBC-MALT6-01] ASBC Malt-6 — Diastatic Power

- Organization: American Society of Brewing Chemists (ASBC)
- Method index: https://www.asbcnet.org/Methods/MaltMethods/pages/default.aspx
- Supporting publication: *The Brewing Science Laboratory*
- URL: https://www.asbcnet.org/publications/Pages/BSL.aspx
- Accessed: 2026-08-30
- Tier: 2
- Supports:
  - Malt-6 as the ASBC diastatic-power method family;
  - Malt-6A and Malt-6B as named ASBC diastatic-power procedures.
- Limitation:
  - the public listings do not expose the full current method text or establish
    the Lintner/Windisch-Kolbach conversion used by FermUnits.

### [BR-EBC-DP-01] Analytica EBC 4.12 — Diastatic Power of Malt

- Organization: European Brewery Convention / Brewers of Europe
- Current method pages:
  - https://brewup.eu/ebc-analytica/malt/diastatic-power-of-malt-by-spectrophotometry-manual-method/4.12.1
  - https://brewup.eu/ebc-analytica/malt/diastatic-power-of-malt-by-segmented-flow-analysis/4.12.2
  - https://brewup.eu/ebc-analytica/malt/diastatic-power-of-malt-by-automated-discrete-analysis/4.12.3
- Supporting reference-malt guidance: https://brewup.eu/document/download/270
- Accessed: 2026-08-30
- Tier: 2
- Supports:
  - the current EBC 4.12 diastatic-power method family;
  - determination of combined alpha- and beta-amylase activity under
    standardized reaction conditions;
  - use of Windisch-Kolbach reporting for EBC malt diastatic power in EBC
    reference-material documentation.
- Limitation:
  - the public method pages do not expose the complete numerical definition of
    the WK reporting scale or the Lintner/WK cross-scale conversion.

### [BR-RANI-DP-2021] Quality attributes for barley malt: “The backbone of beer”

- Authors: Heena Rani and Rachana D. Bhardwaj
- Publication: *Journal of Food Science*, 86(8), 3322-3340, 2021
- DOI: https://doi.org/10.1111/1750-3841.15858
- URL: https://ift.onlinelibrary.wiley.com/doi/10.1111/1750-3841.15858
- Accessed: 2026-08-30
- Tier: 5
- Supports:
  - use of Windisch-Kolbach units for EBC diastatic-power reporting and degrees
    Lintner in another established brewing-analysis tradition;
  - the numerical relationship `Lintner = (WK + 16) / 3.5`, algebraically
    equivalent to the FermUnits pair.
- Limitation:
  - peer-reviewed secondary support rather than the primary historical or
    current standards text establishing the conversion;
  - does not establish a formal valid range or cross-method equivalence claim.

### [BR-ASBC-BEER13-01] ASBC Beer 13 — Dissolved Carbon Dioxide

- Organization: American Society of Brewing Chemists (ASBC)
- Method index: `https://www.asbcnet.org/Methods/BeerMethods/pages/default.aspx`
- Supporting publication: *The Brewing Science Laboratory*
- URL: `https://www.asbcnet.org/publications/Pages/BSL.aspx`
- Accessed: 2026-08-12
- Tier: 2
- Supports:
  - Beer 13 as the ASBC dissolved-carbon-dioxide method family for brewery
    products;
  - the Beer 13C method name, "Dissolved Carbon Dioxide—Manometric/Volumetric
    Method."
- Limitations:
  - the public method listing and book contents do not expose the complete
    Beer-13 method text;
  - they do not by themselves establish the reference state or numerical
    conversion used by FermUnits.

### [BR-ASBC-FILLS1-01] ASBC Fills-1 — Total Contents of Bottles and Cans by Calculation from Measured Net Weight

- Organization: American Society of Brewing Chemists (ASBC)
- URL: `https://www.asbcnet.org/Methods/PackagingMethods/pages/default.aspx`
- Accessed: 2026-08-12
- Tier: 2
- Supports:
  - Fills-1 as a packaging/net-content calculation from measured net weight;
  - separation of the Fills-1 packaging role from Beer-13 dissolved-CO2
    analysis.
- Limitation:
  - the complete current Fills-1 equation and its definitions were not publicly
    exposed during this review.

### [BR-EBC-TORRENT-2006] CO2 correction factor for the net contents of containers

- Author: J. Torrent
- Submitted on behalf of: Analysis Committee of the European Brewery Convention
- Publication: *BrewingScience*, 60(11/12), 3–4, 2006
- URL: `https://brewingscience.de/index.php/brewingscience/article/view/503`
- Accessed: 2026-08-30
- Tier: 4
- Supports:
  - `k = 506.07 mL/g` as the conversion constant for CO2 in volumes to CO2 by
    weight in an equation described as adopted by ASBC;
  - identification of the historical ASBC source as Fills-1/Fills-2 in the
    eighth revised edition (1992);
  - the distinct role of beverage density, specific gravity, residual CO2, and
    CO2 partial molal volume in package-density/net-content corrections.
- Limitations:
  - this is an EBC Analysis Committee technical publication discussing
    packaging correction, not the current ASBC Beer-13 or Fills-1 method text;
  - `k` appears inside a multi-variable package-density equation with separate
    CO2 partial-molal-volume, residual-CO2, and beer-density terms;
  - the paper does not state the reference temperature or pressure for
    `k = 506.07 mL/g`;
  - ranges in the paper concern the density-correction model and must not be
    treated as a validity range for FermUnits' direct volumes-to-`g/L`
    conversion.

## Solution-chemistry sources

The records below are the master bibliography for maintained solution-chemistry
claims.

### [SC-IUPAC-01] Equivalent entity

- Organization: International Union of Pure and Applied Chemistry
- Source: IUPAC Gold Book, “equivalent entity”
- URL: https://goldbook.iupac.org/terms/view/E02192
- Accessed: 2026-08-06
- Source tier: 2
- Supports:
  - equivalence depends on the specified reaction or charge relationship;
  - equivalents must not be treated as universally interchangeable with
    moles without an explicit factor.

### [SC-IUPAC-PH-01] pH

- Organization: International Union of Pure and Applied Chemistry
- Source: IUPAC Gold Book, “pH”
- DOI: https://doi.org/10.1351/goldbook.P04524
- URL: https://goldbook.iupac.org/terms/view/P04524
- Accessed: 2026-08-30
- Source tier: 2
- Supports:
  - the definition of pH as the negative base-10 logarithm of hydrogen-ion
    activity;
  - the dimensionless standard-state activity formulation;
  - the qualification that single-ion activity is not independently measurable
    and the thermodynamic definition is therefore notional.

### [SC-IUPAC-PH-02] Measurement of pH: Definition, standards, and procedures

- Organization: International Union of Pure and Applied Chemistry
- Authors: R. P. Buck, S. Rondinini, A. K. Covington, F. G. K. Baucke,
  C. M. A. Brett, M. F. Camões, M. J. T. Milton, T. Mussini, R. Naumann,
  K. W. Pratt, P. Spitzer, and G. S. Wilson
- Publication: *Pure and Applied Chemistry* 74(11), 2169–2200 (2002)
- DOI: https://doi.org/10.1351/pac200274112169
- URL: https://publications.iupac.org/pac/74/11/2169/index.html
- Accessed: 2026-08-30
- Source tier: 2
- Supports:
  - the conventional/metrological status of pH and its activity-based
    definition;
  - the distinction between defining pH and operationally realizing pH
    measurements and standards.

### [SC-IUPAC-FRACTION-01] Volume fraction and fraction terminology

- Organization: International Union of Pure and Applied Chemistry
- Sources: IUPAC Gold Book, “volume fraction” and “fraction”
- DOIs:
  - https://doi.org/10.1351/goldbook.V06643
  - https://doi.org/10.1351/goldbook.F02494
- URL: https://goldbook.iupac.org/terms/view/V06643
- Accessed: 2026-08-30
- Source tier: 2
- Supports:
  - volume fraction as the volume of a constituent divided by the sum of
    constituent volumes before mixing;
  - mass, volume, and amount fractions as distinct kinds of dimension-one
    composition quantities.

### [SC-EPA-01] Methods for Chemical Analysis of Water and Wastes

- Organization: United States Environmental Protection Agency
- Methods:
  - 130.2, Hardness, Total (Titrimetric, EDTA)
  - 310.1, Alkalinity (Titrimetric, pH 4.5)
- URL: https://nepis.epa.gov/Exe/ZyPURL.cgi?Dockey=30000Q10.TXT
- Accessed: 2026-08-06
- Source tier: 2
- Supports:
  - hardness and alkalinity reporting in `mg/L as CaCO3`;
  - the conventional factor of `50,000` in titration formulas;
  - the equivalent relationship `50 mg/L as CaCO3 = 1 mEq/L`.

### [SC-USGS-01] Alkalinity and Acid Neutralizing Capacity

- Organization: United States Geological Survey
- Publication: National Field Manual, Chapter A6.6
- URL: https://pubs.usgs.gov/twri/twri9a6/twri9a_6.6.pdf
- Accessed: 2026-08-06
- Source tier: 3
- Supports:
  - alkalinity as a chemical property rather than a dissolved CaCO3
    concentration;
  - reporting alkalinity in equivalent concentration and as CaCO3.
- Note:
  - some USGS calculations use a more precise molar-mass-derived factor near
    `50.044 mg/mEq`; FermUnits uses the conventional EPA water-reporting factor
    of exactly `50 mg/mEq` for this API.

## Dependency-planning sources

### [SH-PINT-CHANGES-01] Pint unreleased change log

- Organization: Pint project
- Title: `CHANGES`
- URL: https://github.com/hgrecco/pint/blob/master/CHANGES
- Accessed: 2026-08-30
- Tier: project-primary source for upstream release planning
- Supports:
  - the current unreleased Pint 0.26 development note that Python 3.11 support is
    planned to be dropped in favor of Python 3.14.
- Limitation:
  - describes an unreleased upstream version and may change before Pint 0.26 is
    published; FermUnits must recheck the released metadata before changing its
    compatibility policy.
