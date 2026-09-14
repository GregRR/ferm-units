# Brewing Units and Calculations Reference

This document is the maintained brewing reference for current FermUnits
behavior. It supersedes the original planning inventory retained under
[`legacy/brewing-inventory.txt`](legacy/brewing-inventory.txt).

Implementation status and source-verification status are intentionally separate.
Detailed ASBC/EBC questions are tracked in
[`../asbc-verification.md`](../asbc-verification.md). The project-wide master
source ledger is [`../sources.md`](../sources.md); source records may be repeated
here beside the claims they support for local readability.

## Physical vessel units

Pint's existing unit names are preserved when they have a legitimate meaning.
FermUnits adds qualified names where brewing terminology would otherwise collide
with Pint or another fermentation domain.

The modern/traditional British brewery cask family is based on the Imperial
gallon. Current CAMRA material supports the smaller cask capacities, while
University of Nottingham historical guidance records the beer/ale hierarchy
used after 1803 through puncheon, butt, and tun. [BR-CAMRA-CASK-01]
[BR-NOTTINGHAM-CASK-01] The Weights and Measures Act 1824 established the
Imperial gallon as the standard capacity basis for beer and ale; it does not by
itself establish every named cask multiple used below. [BR-UK-WM-1824]

| FermUnits name | Definition | Implementation status | Source status |
|---|---|---|---|
| `us_beer_barrel` | qualified FermUnits definition numerically equal to Pint `beer_barrel` = 31 US liquid gallons | Implemented | **Verified** Pint behavior via [SH-PINT-01] |
| `imperial_beer_barrel` | qualified FermUnits definition numerically equal to Pint `imperial_barrel` = 36 Imperial gallons | Implemented | **Verified** Pint physical value via [SH-PINT-01]; **Provisional** British brewing terminology via [BR-CAMRA-CASK-01] and [BR-NOTTINGHAM-CASK-01] |
| `pin_cask` | 4.5 Imperial gallons | Implemented | **Provisional** British brewing meaning via [BR-CAMRA-CASK-01] and [BR-NOTTINGHAM-CASK-01] |
| `firkin` | 9 Imperial gallons | Implemented | **Provisional** British brewing meaning via [BR-CAMRA-CASK-01] and [BR-NOTTINGHAM-CASK-01] |
| `kilderkin` | 18 Imperial gallons | Implemented | **Provisional** British brewing meaning via [BR-CAMRA-CASK-01] and [BR-NOTTINGHAM-CASK-01] |
| `brewing_hogshead` | 54 Imperial gallons | Implemented | **Provisional** British brewing meaning via [BR-CAMRA-CASK-01] and [BR-NOTTINGHAM-CASK-01] |
| `brewing_puncheon` | 72 Imperial gallons | Implemented | **Provisional** historical British brewing meaning via [BR-NOTTINGHAM-CASK-01] |
| `brewing_butt` | 108 Imperial gallons | Implemented | **Provisional** historical British brewing meaning via [BR-NOTTINGHAM-CASK-01] |
| `brewing_tun` | 216 Imperial gallons | Implemented | **Provisional** historical British brewing meaning via [BR-NOTTINGHAM-CASK-01] |

The qualified `brewing_puncheon`, `brewing_butt`, and `brewing_tun` names are
intentional. The same plain-language cask terms have had different capacities in
wine, spirits, and other regional or historical contexts. The values implemented
here follow the University of Nottingham's **after-1803** beer/ale hierarchy and
are retained as explicitly British/historical brewing meanings rather than
promoted to universal bare aliases.

Bare `barrel`, `hogshead`, `puncheon`, `butt`, and `tun` are not given new
universal brewing meanings when a legitimate Pint or cross-domain meaning would
be changed or obscured.

The former alpha-only `wine_hogshead` alias has been removed because wine usage
is regionally ambiguous. Pint's bare `hogshead` remains available unchanged; see
[the wine reference](wine-units.md) for the pre-1.0 naming decision.

### Vessel sources

#### [BR-CAMRA-CASK-01] Or, does Whitbread know its kil from its firkin?

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

#### [BR-NOTTINGHAM-CASK-01] Volumes or Capacity

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

#### [BR-UK-WM-1824] Weights and Measures Act 1824 (5 Geo. IV c. 74)

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

## Gravity and extract

### Specific gravity and gravity points

Public functions:

- `sg_to_gravity_points`
- `gravity_points_to_sg`

Implemented relationship:

```text
GU = (SG - 1) * 1000
SG = 1 + GU / 1000
```

Specific gravity is treated as a dimensionless ratio. The numeric value does not
encode reference temperature. The gravity-points arithmetic is independently
documented as brewing shorthand by the Canadian Homebrewers Association,
including the example `1.046 = 46` gravity points. [BR-CHA-GU-2021]

FermUnits applies the formula algebraically below SG 1.000 as well, so SG
`0.998` maps to `-2` gravity points. The cited brewing-practice source does not
independently standardize that below-1.000 extension.

Status: **Provisional.** Implemented. The ordinary gravity-points convention is
sourced as brewing shorthand, while the below-1.000 extension, ASBC terminology,
and specific-gravity reference-condition verification remain pending.

### Specific gravity and degrees Plato

Public functions:

- `sg_to_plato`
- `plato_to_sg`

The current SG-to-Plato polynomial is:

```text
°P = -616.868 + 1111.14(SG) - 630.272(SG²) + 135.997(SG³)
```

`plato_to_sg` numerically inverts that same polynomial rather than using an
independent approximate inverse. This preserves round-trip consistency.

Quek et al. (2019) reproduce the exact implemented coefficients in a
peer-reviewed brewing paper and identify the equation as a formula from the
American Society of Brewing Chemists. [BR-QUEK-2019] This is substantially
stronger support than the legacy inventory provided, but it is still secondary
evidence for the primary ASBC table or method.

Recent JASBC work by Buhl (2024) independently confirms that ASBC extract
tables are used as reference data when evaluating equations relating relative
density and percent-by-mass extract. [BR-BUHL-2024] It does not establish the
provenance of the implemented cubic.

A 1984 JASBC item titled *Statistical Analysis* was identified as a possible
historical lead during this review, but the accessible journal metadata does not
expose the equation or enough article text to establish it as the source of the
coefficients. It therefore remains a verification lead rather than a supporting
source record.

Status: **Provisional.** Implemented. The exact polynomial is independently
reproduced in peer-reviewed brewing literature with ASBC attribution, while the
primary ASBC source, reference conditions, scientific validity range, and full
precision qualification remain direct verification items.

The numerical SG search interval used by the inverse is an implementation limit,
not an asserted scientific range. The inverse itself is a FermUnits numerical
implementation choice: it solves the published forward polynomial rather than
claiming a separately standardized Plato-to-SG equation.

### Brix, Plato, and Balling

FermUnits does not provide a generic Brix-to-Plato conversion and does not
currently provide separate Balling functions. These scales have distinct
historical and analytical contexts and are not treated as interchangeable unit
aliases.

A peer-reviewed laboratory brewing protocol describes degrees Plato as the
mass percentage of dissolved solids in wort by reference to the density of an
equivalent sucrose solution. [BR-THESSELING-2019] OIML guidance separately
anchors Brix to sucrose mass-fraction/refractometer practice. [SH-OIML-01]
These related measurement traditions are enough to support keeping the names
semantically distinct rather than defining a universal arithmetic conversion.

Status: **Pending** for any generic cross-scale conversion; not implemented by
design. The modern Plato and Brix meanings are sourced, while historical Balling
details and any stated cross-scale tolerance remain verification pending.

### Wort refractometer correction

Public functions:

- `wort_refractometer_brix_to_plato`
- `plato_to_wort_refractometer_brix`

Implemented relationship:

```text
corrected Plato = apparent Brix / wort correction factor
apparent Brix = Plato * wort correction factor
```

The wort correction factor is required explicitly. FermUnits does not define a
default correction factor, and these functions are not represented as generic
Brix/Plato scale conversions.

The current M3 review found no authoritative support for a universal wort
correction factor. OIML's Brix treatment is tied to sucrose/refractometer
measurement conditions rather than to a universal wort composition, so the
caller-supplied-factor boundary remains intentionally conservative.

Brewer's Friend independently documents the same practical convention used by
FermUnits: determine the factor from paired unfermented-wort readings as raw
refractometer Brix WRI divided by a hydrometer-derived reference Brix/Plato value,
then divide the raw refractometer reading by that factor. It also explicitly
warns that this simple calibration is for **unfermented wort only** because
alcohol changes the refractometer response. [BR-BREWERSFRIEND-WCF-01]

Status: **Provisional.** Implemented with an explicit caller-supplied factor for
unfermented wort. ASBC procedure, calibration practice, and any defensible
factor range remain verification pending. FermUnits does not implement a
fermented-sample/alcohol refractometer correction model.

Sources: [SH-OIML-01] for refractometer/Brix measurement context and
[BR-BREWERSFRIEND-WCF-01] for corroborating brewing-practice convention and the
unfermented-wort restriction.

## Hydrometer temperature correction

FermUnits does not currently implement hydrometer temperature correction.

The formula from the legacy brewing inventory was rejected because it omitted
hydrometer calibration temperature, lacked a verified source and validity range,
and produced implausible corrections under ordinary brewing conditions.

A future API must include explicit sample temperature, hydrometer calibration
temperature, temperature scale, supported SG/temperature range, and sample
matrix.

Status: **Rejected** for the legacy formula. Replacement status: **Pending** an
authoritative method; no replacement is implemented.

Sources: [SH-NIST-01] for hydrometer calibration and temperature-effect context.


### Gravity and extract sources

#### [BR-CHA-GU-2021] Beer Math—Working With Percentages and Gravity Units

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

#### [BR-QUEK-2019] Molecular structure-property relations controlling mashing performance of amylases as a function of barley grain size

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

#### [BR-BUHL-2024] Physical Equations Relating Extract and Relative Density

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

#### [BR-THESSELING-2019] A Hands-On Guide to Brewing and Analyzing Beer in the Laboratory

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

#### [BR-BREWERSFRIEND-WCF-01] How to Determine your Refractometer’s Wort Correction Factor

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

## Beer color

### SRM and EBC

Public functions:

- `srm_to_ebc`
- `ebc_to_srm`

Implemented relationship:

```text
EBC = SRM * (25 / 12.7)
SRM = EBC / (25 / 12.7)
```

ASBC publicly identifies Beer-10A as its spectrophotometric beer-color method,
and Analytica EBC identifies 9.6 as the current spectrophotometric beer-color
method. [BR-ASBC-COLOR-01] [BR-EBC-COLOR-01] A technical presentation by
Charlie Bamforth gives the corresponding 430 nm scale factors for a 10 mm cell
as `12.7` for ASBC/SRM and `25` for EBC; a peer-reviewed brewing protocol
independently gives `EBC = 25 * dilution * A430` and the rounded relation
`SRM = 0.508 * EBC`. [BR-BAMFORTH-COLOR-2014] [BR-THESSELING-2019]

FermUnits uses the exact ratio of the stated scale factors rather than the
rounded `1.97`/`0.508` presentation values. These helpers convert already
reported modern color indices. They do not implement the sample clarification,
dilution, turbidity assessment, or other procedural requirements of Beer-10A
or EBC 9.6/8.5, and a single-wavelength index is not a complete description of
perceived beer color.

Status: **Provisional.** Implemented. The numerical scale-factor relationship is
strongly supported by accessible technical and peer-reviewed sources and the
current ASBC/EBC method identities are confirmed, but the complete primary
method text has not been directly verified for all procedural qualifications.

### Lovibond approximation

Public functions:

- `lovibond_to_srm_approx`
- `srm_to_lovibond_approx`

Implemented relationship:

```text
SRM = 1.3546 * Lovibond - 0.76
```

The inverse is calculated algebraically. The relationship is commonly reproduced
in brewing guidance, including for malt color reporting, but the current review
did not locate a primary source that establishes the coefficients, material
scope, valid range, or expected error. [BR-BYO-MALT-COLOR-01] Function names
therefore retain `_approx`. The relationship must not be treated as a general
physical conversion between arbitrary Lovibond-tintometer measurements and
modern spectrophotometric SRM/EBC measurements.

Status: **Provisional.** Implemented as an explicitly named approximation. The
relationship is well established in secondary brewing practice, while primary
coefficient provenance, material scope, range, and expected error remain
verification pending.

## Analytical bitterness

Public functions:

- `absorbance_275nm_to_bitterness_units`
- `bitterness_units_to_absorbance_275nm`

Implemented relationship:

```text
bitterness units = method-extract absorbance at 275 nm * 50
```

ASBC publicly identifies Beer-23A as *Beer Bitterness—Bitterness Units
(International Method)*. An ASBC conference presentation shows the Beer-23
liquid-liquid extraction context and states `A275 * 50 = bitterness units`, while
explicitly warning that the result is not one ppm of iso-alpha-acid.
[BR-ASBC-BEER23-01] [BR-ASBC-SHELLHAMMER-2016] An EBC Analysis Committee
publication also directly established the coordinated `A275 * 50` EBC bitterness
reporting factor in 1967. [BR-EBC-BISHOP-1967] Analytica EBC identifies 9.8 as
its current international beer-bitterness method and notes that its precision
chapter now includes dry-hopped beers. [BR-EBC-BITTERNESS-01]

The FermUnits helper therefore accepts the absorbance of the method-derived
nonpolar extract, not raw beer absorbance. It applies only the reporting factor
and does not implement acidification, extraction, phase separation, cuvette, or
other sample-preparation requirements. The result remains an operational
analytical measurement: ASBC dry-hop work shows why IBU values must not be
collapsed into exact iso-alpha-acid concentration or sensory bitterness.
[BR-ASBC-DRYHOP-2010]

FermUnits does not provide a synthetic arithmetic IBU-to-EBU conversion.

Status: **Provisional.** Implemented. The historical `A275 * 50` reporting
factor and operational bitterness-unit meaning are directly supported, and the
current Beer-23A/EBC 9.8 method identities are confirmed. Direct verification of
the complete current methods and their procedural conditions remains pending.

### Beer color and bitterness sources

#### [BR-ASBC-COLOR-01] ASBC Beer 10A — Color—Spectrophotometric Color Method

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

#### [BR-EBC-COLOR-01] Analytica EBC 9.6 — Colour of Beer: Spectrophotometric Method (IM)

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

#### [BR-BAMFORTH-COLOR-2014] Color Chemistry: Red and White Beer for St. George's Day

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

#### [BR-BYO-MALT-COLOR-01] Understanding Malt COAs

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

#### [BR-ASBC-BEER23-01] ASBC Beer 23A — Beer Bitterness—Bitterness Units (International Method)

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

#### [BR-ASBC-SHELLHAMMER-2016] Beer 23 — International Bitterness Unit

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

#### [BR-EBC-BISHOP-1967] The E.B.C. Scale of Bitterness

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

#### [BR-EBC-BITTERNESS-01] Analytica EBC 9.8 — Bitterness of Beer (IM)

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

#### [BR-ASBC-DRYHOP-2010] Determination of Bitterness Units and Iso-alpha-acid Levels in Dry-Hopped Beers

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

## Diastatic power

Public functions:

- `lintner_to_windisch_kolbach`
- `windisch_kolbach_to_lintner`

Implemented conventional relationship:

```text
°WK = 3.5 * °Lintner - 16
°Lintner = (°WK + 16) / 3.5
```

ASBC currently identifies Malt-6 as its diastatic-power method family, while
Analytica EBC 4.12 measures the combined activity of alpha- and beta-amylase of
malt under standardized reaction conditions. [BR-ASBC-MALT6-01]
[BR-EBC-DP-01] A peer-reviewed malt-quality review independently reproduces the
implemented Lintner/Windisch-Kolbach conversion and describes the two reporting
scales as related by `Lintner = (WK + 16) / 3.5`. [BR-RANI-DP-2021]

The conversion is therefore well established as a conventional reporting-scale
relationship, but FermUnits does not claim that applying it converts a result
from one analytical procedure into the result that would have been obtained by
running the other procedure. Direct primary provenance for the cross-scale
formula, its formal exactness, valid range, dry-matter basis, and reporting
precision remains unavailable in the sources reviewed here.

The nonzero intercept also makes the low end important: the conventional formula
maps `0 °WK` to about `4.57 °Lintner`, while smaller Lintner values would produce
negative WK values. FermUnits rejects forward conversions that would produce a
negative reported value rather than silently extending the relationship into
that physically meaningless region.

Status: **Provisional.** Implemented. Current ASBC/EBC method identities and the
conventional numerical relationship are sourced, while primary formula
provenance, method-equivalence scope, range, and reporting conventions remain
verification pending.

### Diastatic-power sources

#### [BR-ASBC-MALT6-01] ASBC Malt-6 — Diastatic Power

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

#### [BR-EBC-DP-01] Analytica EBC 4.12 — Diastatic Power of Malt

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

#### [BR-RANI-DP-2021] Quality attributes for barley malt: “The backbone of beer”

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

## Carbonation

Public functions:

- `co2_volumes_to_mass_concentration`
- `co2_mass_concentration_to_volumes`
- `co2_volumes_to_grams_per_liter` (scalar compatibility API)
- `co2_grams_per_liter_to_volumes` (scalar compatibility API)

The scalar compatibility pair is an intentional supported 1.x API, not a
pending deprecation. New unit-aware code should still prefer the quantity-aware
pair when physical concentration participates in larger calculations.

The quantity-aware APIs return or accept Pint mass-concentration quantities so
physical concentration units remain explicit at downstream engineering
boundaries. The semantic "volumes CO2" value remains a scalar rather than an
ordinary multiplicative Pint unit.

### Verified reference-state definition

For this API, one volume of CO2 means one volume of CO2 gas at `273.15 K` and
`101.325 kPa` per equal volume of beverage. Speers and MacIntosh identify those
conditions explicitly as the STP basis of the ASBC Beer-13 chart.
[BR-SPEERS-MACINTOSH-2013]

The implementation uses one reciprocal factor in both directions:

```text
milliliters of CO2 at the reference state per gram = 506.07
grams per liter per volume = 1000 / 506.07
```

The result is approximately `1.976011 g/L` per volume of CO2. Torrent (2006),
submitted on behalf of the EBC Analysis Committee, reports `506.07 mL/g` as the
conversion constant for CO2 in volumes to CO2 by weight in an ASBC-adopted
packaging equation. [BR-EBC-TORRENT-2006] Independent physical-property data
report CO2 gas density of approximately `1.976 g/L` at `0 °C` and `760 mmHg`,
the same reference state. [SH-PUBCHEM-CO2-01] University of Florida beverage
guidance also uses volumes of CO2 at STP per liquid volume across carbonated
beverage categories, with a rounded `1.96 g/L` convention. [SH-UF-CO2-01]

Taken together, the beer-specific reference-state definition, the brewing-
industry conversion constant, and independent physical-property value directly
support the FermUnits conversion semantics and numerical factor. The direct
volumes-to-mass-concentration relationship is therefore **Verified**.

Official ASBC display rounding is not part of the FermUnits conversion
contract: these functions convert the underlying reference-state quantity and
do not prescribe an analytical method's reported number of decimal places.

### Equilibrium-solubility boundary

The verified reference-state conversion must not be confused with a model that
predicts how much CO2 will be dissolved in beer at a given temperature and
pressure.

Speers and MacIntosh show that the historical Beer-13 pressure/temperature chart
represents a "standard beer" and that alcohol and extract can affect CO2
solubility. [BR-SPEERS-MACINTOSH-2013] Later peer-reviewed work continues to
treat beer or beverage CO2 solubility as composition-dependent:

- Liger-Belair and Cilindre report that usual theoretical solubility models do
  not account for the full compositional range of modern beer and obtain a
  lager-specific Henry coefficient using composition-aware treatment.
  [BR-LIGER-BELAIR-CILINDRE-2021]
- Guadalupe-Daqui et al. use the Speers-and-MacIntosh composition-aware
  relationship in brewing-fermentation research and recalculate CO2 saturation
  from temperature, sugar, ethanol, and pressure. [BR-GUADALUPE-DAQUI-2023]
- Liger-Belair's later critical review synthesizes sparkling-beverage
  solubility models around the combined effects of temperature, sugar, and
  ethanol. [SH-LIGER-BELAIR-2025]

FermUnits therefore does **not** encode the Beer-13 pressure/temperature chart,
a universal Henry coefficient for beer, or any pressure-to-dissolved-CO2
shortcut. Those are downstream model semantics that require composition and
model-scope decisions beyond a unit/reporting conversion.

### Density and specific-gravity boundary

Torrent's Fills-1-family equation uses `k = 506.07 mL/g` alongside separate
beverage-density/specific-gravity, residual-CO2, and CO2 partial-molal-volume
terms for package-density/net-content correction. FermUnits uses `k` only for
the reference-state volumes-to-mass-concentration conversion; it does not
implement those separate package-correction terms. [BR-EBC-TORRENT-2006]

Those density terms must not be imported into the direct reference-state
conversion, and experimental ranges reported for package-density or
partial-molal-volume models must not be treated as a validity range for this
conversion.

Status: **Verified.** Implemented.

### Carbonation-specific sources

#### [BR-SPEERS-MACINTOSH-2013] Carbon Dioxide Solubility in Beer

- Authors: R. Alex Speers and Andrew MacIntosh
- Publication: *Journal of the American Society of Brewing Chemists*, 71(4),
  242–247, 2013
- DOI: `10.1094/ASBCJ-2013-1008-01`
- URL: `https://doi.org/10.1094/ASBCJ-2013-1008-01`
- Accessed: 2026-09-14
- Tier: 5 — peer-reviewed original research and analysis
- Supports:
  - Beer-13 volumes of CO2 as reference-state gas volume at `273.15 K` and
    `101.325 kPa` per volume of beer;
  - separation of that reporting definition from equilibrium-solubility
    modeling;
  - composition dependence of beer CO2 solubility and limitations of a
    pressure/temperature-only "standard beer" model.
- Limitations:
  - does not reproduce the complete current Beer-13 method text;
  - does not itself state the `506.07 mL/g` factor used by FermUnits;
  - the evaluated composition-aware model remains model-scoped rather than a
    universal equilibrium law.

#### [BR-LIGER-BELAIR-CILINDRE-2021] How Many CO2 Bubbles in a Glass of Beer?

- Authors: Gérard Liger-Belair and Clara Cilindre
- Publication: *ACS Omega*, 6(14), 9672–9679, 2021
- DOI: `10.1021/acsomega.1c00256`
- URL: `https://doi.org/10.1021/acsomega.1c00256`
- Accessed: 2026-09-14
- Tier: 5 — peer-reviewed original research
- Supports:
  - later beer-specific thermodynamic treatment of composition-dependent CO2
    solubility;
  - approximate `2.4 g/(L * bar)` Henry coefficient at `6 °C` for the lager
    studied;
  - reported agreement of its composition-aware estimate with the main model
    discussed by Speers and MacIntosh.
- Limitation:
  - one commercial lager does not establish a universal beer-equilibrium model.

#### [BR-GUADALUPE-DAQUI-2023] The effect of CO2 concentration on yeast fermentation

- Authors: Mario Guadalupe-Daqui, Renee M. Goodrich-Schneider, Paul J. Sarnoski,
  John C. Carriglio, Charles A. Sims, Brian J. Pearson, and Andrew J. MacIntosh
- Publication: *Journal of Industrial Microbiology and Biotechnology*, 50(1),
  kuad001, 2023
- DOI: `10.1093/jimb/kuad001`
- URL: `https://doi.org/10.1093/jimb/kuad001`
- Accessed: 2026-09-14
- Tier: 5 — peer-reviewed original research
- Supports:
  - later quantitative use of the Speers-and-MacIntosh composition-aware
    solubility relationship;
  - dissolved-CO2 saturation treatment using temperature, sugar, ethanol, and
    pressure.
- Limitation:
  - uses rather than independently revalidates every coefficient of the cited
    solubility relationship.

#### [SH-LIGER-BELAIR-2025] Carbon Dioxide Solubility in Sugar and Water–Ethanol Solutions for Applications to Sparkling Drinks

- Author: Gérard Liger-Belair
- Publication: *ACS Food Science & Technology*, 5(1), 36–49, 2025
- DOI: `10.1021/acsfoodscitech.4c00854`
- URL: `https://doi.org/10.1021/acsfoodscitech.4c00854`
- Accessed: 2026-09-14
- Tier: 5 — peer-reviewed critical review
- Supports:
  - later synthesis of sparkling-beverage CO2-solubility models around the
    combined effects of temperature, sugar, and ethanol.
- Limitation:
  - corroborating review evidence rather than a replacement for primary work.

#### [BR-ASBC-BEER13-01] ASBC Beer 13 — Dissolved Carbon Dioxide

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
- Limitation:
  - the public listing does not expose the complete method text; the
    reference-state definition used by FermUnits is instead directly supported
    by [BR-SPEERS-MACINTOSH-2013].

#### [BR-ASBC-FILLS1-01] ASBC Fills-1 — Total Contents of Bottles and Cans by Calculation from Measured Net Weight

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

#### [BR-EBC-TORRENT-2006] CO2 correction factor for the net contents of containers

- Author: J. Torrent
- Submitted on behalf of: Analysis Committee of the European Brewery Convention
- Publication: *BrewingScience*, 60(11/12), 3–4, 2006
- Published: 2006-12-20
- URL: `https://brewingscience.de/index.php/brewingscience/article/view/503`
- Accessed: 2026-09-07
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
  - the paper does not itself state the reference temperature or pressure for
    `k = 506.07 mL/g`; that reference-state meaning is supplied by the separate
    Beer-13 evidence in [BR-SPEERS-MACINTOSH-2013];
  - ranges in the paper concern the density-correction model and must not be
    treated as a validity range for FermUnits' direct volumes-to-`g/L`
    conversion.

## Explicitly superseded legacy claims

The maintained implementation does **not** adopt several claims that appeared in
the original planning inventory:

- no default wort correction factor is assumed;
- no independent De Clerck-style Plato-to-SG formula is used;
- Brix, Plato, and Balling are not generic interchangeable unit aliases;
- no unsupported hydrometer-temperature formula is implemented;
- bitterness units are not defined as an exact iso-alpha-acid mass
  concentration;
- IBU and EBU are not given a synthetic 1:1 conversion API;
- the older Lovibond coefficients `1.35` and `-0.6` are not the current
  implementation;
- the rounded non-reciprocal carbonation pair `1.96` and `0.51` is not used.

## Shared sources used by this reference

- [SH-PINT-01] Pint default unit definitions — defined in
  [`../sources.md`](../sources.md).
- [SH-OIML-01] OIML R 142-1:2025, automated refractometers — defined in
  [`../sources.md`](../sources.md).
- [SH-NIST-01] NBS Circular 555, hydrometer testing — defined in
  [`../sources.md`](../sources.md).

Method-specific brewing verification and remaining provenance questions are
tracked in [`../asbc-verification.md`](../asbc-verification.md). Additional
method text may refine method history or reporting details without automatically
overriding claim-appropriate peer-reviewed evidence.
