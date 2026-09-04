# Wine Units and Calculations Reference

This document is the maintained wine-domain reference for FermUnits. It
supersedes the original planning material retained under
[`legacy/wine-inventory.txt`](legacy/wine-inventory.txt) as the source of truth
for current implementation status, ownership decisions, candidate names, and
source-verification status.

The Milestone 6 migration does **not** turn the legacy inventory into a feature
checklist. Wine measurements include ordinary physical quantities, analytical
scales, method-defined reporting bases, regional vessel names, and application
semantics. FermUnits should implement only behavior that is reusable across
fermentation software and adequately sourced.

## Migration outcome

The legacy wine inventory has now been triaged into five ownership classes:

1. **ordinary Pint quantities** — use Pint through FermUnits without adding a
   new alias;
2. **existing FermUnits semantic behavior** — reuse the current FermUnits API;
3. **source-ready regional physical-unit candidates** — numerical meanings are
   adequately sourced, but implementation still requires a concrete downstream
   need;
4. **method-defined or application-level semantics** — preserve the reporting
   basis and method context downstream rather than pretending it is a universal
   unit conversion;
5. **pending, ambiguous, or rejected candidates** — do not implement until the
   ambiguity or source gap is resolved.

No new public API is added by this migration slice.

## Wine-vessel naming stabilization

### Former alpha alias: `wine_hogshead`

FermUnits previously defined `wine_hogshead` as an alias of Pint's existing
`hogshead`, whose Pint value is 63 US liquid gallons. That physical Pint meaning
remains available as bare `hogshead` and is verified as Pint behavior via
[SH-PINT-01].

The FermUnits alias has been **removed during pre-1.0 stabilization** because the
name implies a universal wine-industry meaning that the sources do not support.
AWRI documents a legitimate Australian wine-industry hogshead of 300 L, so the
qualifier `wine_` is not sufficient to disambiguate the term.
[WI-AWRI-PACKAGING-01]

Future wine-vessel definitions must use region-qualified names such as
`australian_wine_hogshead` when a concrete downstream need justifies the API.
FermUnits will not silently reinterpret the removed `wine_hogshead` name.

## Must density, extract, sugar, and alcohol

### Density at 20 °C and specific gravity at 20 °C

OIV method `OIV-MA-AS2-01` defines wine/must density at 20 °C as mass per unit
volume and specific gravity as the ratio of sample density at 20 °C to water
density at 20 °C. [WI-OIV-ANALYTICS-01]

Ownership:

- density is an ordinary Pint mass-per-volume quantity;
- specific gravity is an ordinary dimension-one quantity;
- the 20 °C analytical reference condition belongs to the measurement record or
  method context and is not encoded by a new unit name.

Implementation status: **No new FermUnits API required.**

### Brix / refractometric sugar concentration

OIV method `OIV-MA-AS2-02` measures grape-must refractive index at approximately
20 °C and may express the reading as percentage by mass of sucrose before using
method tables to obtain sugar concentration. [WI-OIV-ANALYTICS-01] Shared source
[SH-OIML-01] independently supports Brix as a sucrose mass-fraction scale and
the need for explicit measurement conditions.

Ownership:

- Brix is an analytical scale, not a new multiplicative Pint unit;
- a must refractometer reading must not be represented as chemically identical
  to glucose-plus-fructose concentration;
- temperature correction, instrument calibration, and method-table use remain
  explicit analytical context.

Implementation status: **No wine-specific Brix unit proposed.** Existing
FermUnits brewing refractometer helpers retain their brewing-specific semantics
and do not define a universal wine-must Brix conversion.

### Baumé, Oechsle, and KMW

The legacy inventory records useful research leads for these regional or
historical must scales, but the cross-scale factors in that file are not
promoted into maintained FermUnits behavior.

| Scale | Ownership | Source status | Implementation decision |
|---|---|---|---|
| Baumé | Method-/region-defined density scale | **Pending** exact authoritative wine method, reference conditions, and conversion basis | Do not implement legacy `1.8` rule of thumb |
| Oechsle | Regional must-weight scale | **Pending** authoritative legal/analytical definition and reference conditions | Do not yet expose the legacy SG formula as a wine API |
| KMW / Klosterneuburger Mostwaage | Austrian must scale | **Pending** authoritative Austrian definition and reporting convention | Do not implement legacy `4.86–5` Oechsle approximation |

The legacy Brix↔Baumé, Brix↔Oechsle, KMW↔Oechsle, Brix↔KMW, and Brix→potential-
alcohol relationships remain **Rejected as universal conversions** until each is
independently sourced with method scope, valid range, and reference conditions.
Potential alcohol is especially unsuitable as a fixed unit conversion because
fermentation yield and completion are process/model assumptions.

### Glucose + fructose, residual sugar, and alcoholic strength

OIV identifies glucose + fructose in g/L and alcoholic strength by volume at
20 °C as standard wine analytical parameters. `OIV-MA-AS312-01` defines
alcoholic strength by volume at 20 °C. [WI-OIV-ANALYTICS-01]

Ownership:

- glucose/fructose and residual-sugar results are ordinary mass-concentration
  quantities once an analytical method has produced the result;
- alcoholic strength by volume is an ordinary dimension-one volume fraction;
- method identity, analyte definition, reference temperature, uncertainty, and
  reporting precision remain downstream measurement metadata.

Implementation status: **No new unit aliases required.**

## Acidity, pH, and sulfur dioxide

OIV's commonly used wine parameters include total acidity, volatile acidity,
pH, and total sulfur dioxide. OIV methods also define free/total sulfur dioxide
and distinguish molecular sulfur dioxide within the free-SO2 equilibrium.
[WI-OIV-ANALYTICS-01]

### pH

Wine pH uses the existing FermUnits semantic boundary:

- `PHValue`
- `ph_to_hydrogen_ion_activity`
- `hydrogen_ion_activity_to_ph`

`OIV-MA-AS313-15` is an operational wine/must measurement method; FermUnits owns
the reusable activity-based pH semantics, while electrode calibration,
temperature, buffers, precision, and laboratory procedure remain downstream.

Implementation status: **Already covered by FermUnits.**

### Total and volatile acidity

OIV method `OIV-MA-AS313-01` defines total acidity by titration, and
`OIV-MA-AS313-02` defines volatile acidity. OIV reporting permits equivalent
concentration and acid-equivalent mass-concentration bases, including mEq/L and
g/L expressed as specified acids. [WI-OIV-ANALYTICS-01]

Ownership:

- `mEq/L` and mass concentration are already supported by FermUnits/Pint;
- the existing equivalent-concentration helpers can perform explicit
  equivalent-mass transformations;
- the reporting phrase *as tartaric acid*, *as sulfuric acid*, or *as acetic
  acid* is semantic metadata and must remain explicit in the calling
  application;
- FermUnits should not infer an acid basis from a bare numeric value.

The legacy acidity factors are therefore retained only as research history.
They should not become wine-specific convenience functions unless a downstream
consumer requires them and the exact equivalent-mass/reporting convention is
made explicit.

### Free, bound, total, and molecular sulfur dioxide

OIV methods `OIV-MA-AS323-04A1`, `OIV-MA-AS323-04A2`, and
`OIV-MA-AS323-04B` define free and total sulfur dioxide and their analytical
relationship. OIV also treats molecular SO2 as dependent on pH, alcoholic
strength, temperature, and equilibrium information. [WI-OIV-ANALYTICS-01]

Ownership:

- reported SO2 concentrations are ordinary mass concentrations such as mg/L;
- `bound = total - free` is downstream domain arithmetic over method-defined
  results, not a new physical unit;
- molecular-SO2 calculation is a possible future explicit reusable calculation,
  but **no fixed-factor conversion is acceptable**.

Implementation status: **No new API in this slice.** Molecular-SO2 calculation
remains **Pending** concrete downstream requirements and a method-complete design.

### Malic and lactic acid

Once determined by an analytical method, malic- and lactic-acid concentrations
are ordinary mass-concentration quantities. OIV provides analytical methods for
both organic-acid analysis and lactic acid. [SH-OIV-01]

Implementation status: **No new unit aliases required.**

## Routine winery laboratory and process measurements

| Measurement | FermUnits ownership | Status |
|---|---|---|
| Yeast-assimilable nitrogen (YAN) | Numeric concentration may use ordinary mass concentration; the definition of what contributes to YAN and the `as N` reporting basis are method semantics | Downstream semantic/model concern |
| Turbidity / NTU | Instrument-defined optical result rather than mass concentration | Pending a concrete cross-domain need; do not create a physical-unit identity |
| Dissolved oxygen | Ordinary oxygen mass concentration such as mg/L | Pint quantity; analyte identity remains explicit |
| Headspace oxygen | May be concentration, partial pressure, or mass per package | Downstream reporting/model concern |
| Total package oxygen | Composite package metric whose normalization basis must be explicit | Downstream reporting/model concern |
| Temperature | Ordinary Pint temperature | No new alias required |

The migration intentionally does not invent a universal conversion among the
different headspace/TPO reporting bases.

## Vineyard yield, recovery, and logistics

The legacy inventory's vineyard and cellar logistics expressions are ordinary
compound physical quantities:

- short ton / acre;
- tonne / hectare;
- hectoliter / hectare;
- liter / tonne;
- US gallon / short ton.

Pint already provides the constituent physical units and compound-unit
arithmetic through FermUnits. FermUnits therefore does not add aliases such as
`liter_per_metric_tonne` merely to shorten a valid compound expression.

A nine-liter case is an exact 9 L package-volume convention when explicitly
requested, and AWRI's logistics guidance uses twelve-bottle cases with standard
750 mL bottles. [WI-AWRI-PACKAGING-01] The word `case` itself is not a universal
physical unit, so no bare `wine_case` alias is proposed.

Implementation status: **No new API required without a downstream ergonomics
need.** Recovery from grape mass to wine volume remains a process yield and must
not be inferred from dimensional conversion alone.

## Sparkling-wine measurements

OIV method `OIV-MA-AS314-02` defines sparkling-wine **overpressure** after
temperature stabilization and expresses the result in Pa/kPa. OIV also has
methods for dissolved carbon dioxide as mass concentration. [WI-OIV-ANALYTICS-01]

Ownership:

- pressure is an ordinary Pint quantity;
- overpressure versus absolute pressure is reference semantics, not a separate
  FermUnits unit;
- dissolved CO2 is an ordinary mass concentration once measured;
- FermUnits' beverage-wide carbonation helpers may represent mass concentration
  and the separate `volumes CO2` scale, but they do not provide a universal
  sparkling-wine pressure↔dissolved-CO2 equilibrium model;
- tirage and dosage sugar amounts expressed in g/L are ordinary mass
  concentrations, while process role is downstream metadata.

The legacy pressure-to-dissolved-CO2 idea remains **Rejected as a universal
conversion**. A physically valid model would require explicit temperature,
pressure basis, wine composition, gas-liquid equilibrium assumptions, and any
headspace model.

## Regional vessel capacities

The following capacities are adequately supported as **regional meanings**.
They are source-ready physical-unit candidates, not automatic implementation
commitments.

| Candidate FermUnits name | Regional meaning | Capacity | Source status | Implementation status |
|---|---|---:|---|---|
| `bordeaux_barrique` | Bordeaux barrique | 225 L | **Verified** via [WI-BORDEAUX-BARRIQUE-01] and [WI-AWRI-PACKAGING-01] | Candidate; not implemented |
| `burgundy_piece` | Bourgogne pièce | 228 L | **Verified** via [WI-BOURGOGNE-CASKS-01] | Candidate; not implemented |
| `pouilly_fuisse_piece` | Pouilly-Fuissé pièce | 212 L | **Verified** via [WI-BOURGOGNE-CASKS-01] | Candidate; not implemented |
| `burgundy_feuillette` | Côte-d'Or / Saône-et-Loire feuillette | 114 L | **Verified** via [WI-BOURGOGNE-CASKS-01] | Candidate; not implemented |
| `chablis_feuillette` | Chablis feuillette | 132 L | **Verified** via [WI-BOURGOGNE-CASKS-01] | Candidate; not implemented |
| `burgundy_queue` | Bourgogne queue | 456 L | **Verified** via [WI-BOURGOGNE-CASKS-01] | Candidate; not implemented |
| `burgundy_demi_muid` | Bourgogne demi-muid | 600 L | **Verified** via [WI-BOURGOGNE-CASKS-01] | Candidate; not implemented |
| `burgundy_muid` | Bourgogne muid | 1,200 L | **Verified** via [WI-BOURGOGNE-CASKS-01] | Candidate; not implemented |
| `australian_wine_hogshead` | Australian wine-industry hogshead | 300 L | **Verified** via [WI-AWRI-PACKAGING-01] | Candidate; not implemented |
| `australian_wine_puncheon_500` | Australian logistics puncheon | 500 L | **Verified** via [WI-AWRI-PACKAGING-01] | Candidate; not implemented |
| `australian_wine_puncheon_600` | Australian logistics puncheon | 600 L | **Verified** via [WI-AWRI-PACKAGING-01] | Candidate; not implemented |
| `rheinhessen_stueckfass` | Rheinhessen Stückfass | 1,200 L | **Verified** via [WI-RHEINHESSEN-STUECK-01] | Candidate; not implemented |
| `rheinhessen_half_stueckfass` | Rheinhessen Halbstück | 600 L | **Verified** regional base; derived half-size | Candidate; not implemented |
| `rheinhessen_quarter_stueckfass` | Rheinhessen Viertelstück | 300 L | **Verified** regional base; derived quarter-size | Candidate; not implemented |
| `sherry_bota_gorda` | Jerez bota gorda / standard ageing bota | 600 L | **Verified** via [WI-JEREZ-CASKS-01] | Candidate; not implemented |
| `sherry_export_butt` | Jerez export/shipping bota | 500 L | **Verified** via [WI-JEREZ-CASKS-01] | Candidate; not implemented |
| `sherry_receipt_butt` | Jerez bota de recibo | 516 L | **Verified** via [WI-JEREZ-CASKS-01] | Candidate; not implemented |
| `sherry_media_bota` | Jerez media bota | 250 L | **Verified** via [WI-JEREZ-CASKS-01] | Candidate; not implemented |
| `sherry_quarter_bota` | Jerez quarter bota | 125 L | **Verified** via [WI-JEREZ-CASKS-01] | Candidate; not implemented |
| `sherry_octavo` | Jerez octavo | 62.5 L | **Verified** via [WI-JEREZ-CASKS-01] | Candidate; not implemented |

### Vessel meanings that should not become fixed units yet

| Term | Status | Reason |
|---|---|---|
| `wine_hogshead` as a universal wine size | **Ambiguous** | Pint's 63-US-gallon hogshead and AWRI's 300 L Australian hogshead are both legitimate meanings |
| generic `wine_puncheon` | **Ambiguous** | AWRI documents both 500 L and 600 L puncheons |
| generic `piece` / `feuillette` | **Ambiguous** | Bourgogne capacities vary by locality |
| `sherry_bodega_butt` | **Provisional** | Jerez source gives 566 L in a vessel description with average dimensions; fixed-unit treatment needs a specific downstream need and final wording review |
| `sherry_bocoy` | **Ambiguous** | Jerez describes variable shape and approximately 700 L / 40–42 arrobas |
| `foudre` | **Ambiguous** | Vessel class spans variable capacities |
| `port_pipe` | **Pending** | Historical/regional meanings require a stronger maintained source record |
| bare `barrel`, `butt`, `pipe`, `tun`, `cask`, `vat` | **Rejected as universal aliases** | Meanings vary across region, industry, and history |

Operational fill volume is not vessel capacity. In Jerez, a nominal 600 L bota
may intentionally hold about 500 L during biological ageing; FermUnits must not
encode that process fill level as the unit definition. [WI-JEREZ-CASKS-01]

## Wine and Champagne bottle formats

Comité Champagne publishes a region-specific bottle sequence. These are strong
candidates for qualified physical-unit names if a downstream consumer needs
named package sizes. [WI-CHAMPAGNE-BOTTLES-01]

| Candidate name | Champagne format | Capacity |
|---|---|---:|
| `champagne_quarter` | quart | 200 mL |
| `champagne_half_bottle` | demie | 375 mL |
| `champagne_medium` | medium / pinte | 500 mL |
| `champagne_bottle` | standard bottle | 750 mL |
| `champagne_magnum` | magnum | 1.5 L |
| `champagne_jeroboam` | jeroboam | 3 L |
| `champagne_rehoboam` | rehoboam | 4.5 L |
| `champagne_methuselah` | methuselah | 6 L |
| `champagne_salmanazar` | salmanazar | 9 L |
| `champagne_balthazar` | balthazar | 12 L |
| `champagne_nebuchadnezzar` | nebuchadnezzar | 15 L |
| `champagne_salomon` | salomon | 18 L |
| `champagne_souverain` | souverain | 26.25 L |
| `champagne_primat` | primat | 27 L |
| `champagne_melchizedek` | melchizedek / midas | 30 L |

Implementation status for the entire sequence: **Source-ready; not implemented.**
The region qualifier is intentional. A bare `jeroboam`, for example, must not be
assigned Champagne's 3 L value because the legacy research identifies a
different Bordeaux usage.

The following legacy bottle candidates remain **Pending** rather than being
carried into the source-ready list:

- `wine_split` / piccolo at 187.5 mL;
- still-wine `double_magnum` at 3 L;
- Bordeaux jeroboam at 4.5 L;
- Bordeaux imperial at 6 L.

They need authoritative region-specific source records before implementation.
Bare traditional bottle names should not be promoted when regional meanings
conflict.

## Implementation priority after migration

This migration establishes what is known; it does not create demand by itself.
The next wine implementation slice should be selected only when a real consumer
needs one of these meanings.

If such a need appears, the preferred order is:

1. **source-ready regional physical units** with unambiguous qualified names;
2. **source-ready Champagne bottle formats** when named package sizes are
   actually useful to a consumer;
3. **explicit analytical transformations** only after method scope and required
   parameters are fully designed.

The following are specifically **not** implementation-ready as generic
conversions:

- Baumé/Oechsle/KMW cross-scale shortcuts;
- potential-alcohol estimates;
- molecular-SO2 fixed-factor formulas;
- pressure↔dissolved-CO2 shortcuts;
- generic regional vessel names.

## Wine sources

### [WI-OIV-ANALYTICS-01] OIV wine and must analytical methods

- Organization: International Organisation of Vine and Wine (OIV)
- Publication: *Compendium of International Methods of Wine and Must Analysis*
- Methods used in this migration:
  - `OIV-MA-AS2-01` — Density and specific gravity at 20 °C;
  - `OIV-MA-AS2-02` — Evaluation by refractometry of sugar concentration in
    grape musts;
  - `OIV-MA-AS312-01` — Alcoholic strength by volume;
  - `OIV-MA-AS313-01` — Total acidity;
  - `OIV-MA-AS313-02` — Volatile acidity;
  - `OIV-MA-AS313-15` — pH;
  - `OIV-MA-AS323-04A1`, `04A2`, and `04B` — sulfur dioxide;
  - `OIV-MA-AS314-01` / `OIV-MA-AS314-02` — carbon dioxide and sparkling-wine
    overpressure.
- URL: https://www.oiv.int/standards/compendium-of-international-methods-of-wine-and-must-analysis
- Accessed: 2026-09-03
- Source tier: 2
- Supports:
  - wine/must density and specific-gravity reference conditions;
  - refractometric sucrose-mass-fraction reporting and method context;
  - alcoholic-strength, glucose/fructose, acidity, pH, sulfur-dioxide, CO2, and
    sparkling-wine pressure measurement/reporting bases.
- Limitations:
  - method existence and reporting basis do not make legacy cross-scale rules
    universal unit identities;
  - restricted or lengthy method text is not reproduced in this repository.

### [WI-AWRI-PACKAGING-01] Packaging options

- Organization: Australian Wine Research Institute (AWRI)
- URL: https://www.awri.com.au/industry_support/winemaking_resources/storage-and-packaging/packaging-operations/packaging-options/
- Accessed: 2026-09-03
- Source tier: 4
- Supports:
  - Bordeaux barrique at 225 L;
  - Burgundy barrique at 228 L;
  - Australian wine-industry hogshead at 300 L;
  - 500 L and 600 L puncheons;
  - twelve-bottle case logistics based on standard 750 mL bottles.
- Limitation:
  - logistics guidance does not establish one universal historical meaning for
    `hogshead`, `puncheon`, `barrique`, or `case` outside the stated context.

### [WI-BORDEAUX-BARRIQUE-01] L'art de faire du vin : l'élevage

- Organization: Conseil Interprofessionnel du Vin de Bordeaux (CIVB)
- URL: https://www.bordeaux.com/fr/savoir-faire/elevage/
- Accessed: 2026-09-03
- Source tier: 4
- Supports:
  - 225 L as the Bordeaux barrique capacity in current regional wine practice.

### [WI-BOURGOGNE-CASKS-01] The secrets of a well-aged wine

- Organization: Bourgogne Wine Board (BIVB)
- URL: https://www.bourgogne-wines.com/wine-and-terroir/our-natural-assets/vinification-and-ageing/ageing-the-wine/the-secrets-of-a-well-aged-wine,2488,9273.html
- Accessed: 2026-09-03
- Source tier: 4
- Supports:
  - 228 L Bourgogne pièce;
  - 212 L Pouilly-Fuissé pièce;
  - 114 L Bourgogne feuillette and 132 L Chablis feuillette;
  - 456 L queue;
  - 600 L demi-muid;
  - 1,200 L muid.
- Limitation:
  - these are explicitly regional meanings and must not be generalized to bare
    `piece`, `feuillette`, or `muid` aliases across wine regions.

### [WI-RHEINHESSEN-STUECK-01] “Stück” — Rheinhessen Wine Dictionary

- Organization: Rheinhessen regional wine portal
- URL: https://www.rheinhessen.de/en/en-stueck
- Accessed: 2026-09-03
- Source tier: 4
- Supports:
  - Stückfass as a widespread Rheinhessen wine measure of 1,200 L;
  - regional use of half-Stück and quarter-Stück forms.
- Limitation:
  - the source states the base capacity and names the fractional forms; 600 L
    and 300 L are arithmetic derivations from the named half/quarter forms.

### [WI-JEREZ-CASKS-01] Sherry cask cooperage and glossary

- Organization: Consejo Regulador de las Denominaciones de Origen Jerez-Xérès-
  Sherry, Manzanilla-Sanlúcar de Barrameda y Vinagre de Jerez
- URLs:
  - https://www.sherry.wine/sherry-cask/sherrycask-the-cooperage
  - https://www.sherry.wine/sherry-cask/sherrycask-the-cooperage/glosario
- Accessed: 2026-09-03
- Source tier: 4
- Supports:
  - 600 L bota gorda / standard Jerez ageing bota;
  - 500 L export bota;
  - 516 L receipt bota;
  - 566 L bodega-butt description;
  - 250 L media bota, 125 L quarter bota, and 62.5 L octavo;
  - bocoy as variable in shape and around 700 L;
  - operational practice of partially filling ageing botas.
- Limitation:
  - cooperage dimensions can vary;
  - `bota` and `bocoy` are not universal fixed-capacity terms without the
    specific Jerez subtype/context.

### [WI-CHAMPAGNE-BOTTLES-01] Champagne bottle sizes

- Organization: Comité Champagne
- URL: https://www.champagne.fr/en/champagne-frequently-asked-questions
- Accessed: 2026-09-03
- Source tier: 4
- Supports:
  - the Champagne-specific sequence from 200 mL quarter through 30 L
    Melchizedek/Midas, including the capacities recorded above.
- Limitation:
  - bottle names used in other wine regions can carry different capacities;
    this source supports Champagne-qualified meanings only.
