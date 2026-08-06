# Definition sources

Before adding any FermUnits unit definition or alias, verify the pinned Pint version’s 
documentation, bundled definitions, and registry behavior.

- Use Pint’s definition directly when it already has the correct meaning.
- Preserve Pint’s definition when its meaning is legitimate but conflicts with a 
  fermentation-domain meaning; add an explicit qualified FermUnits name instead.
- Add calculations or semantic metadata—not a duplicate unit—when Pint already represents 
  the physical dimensions but not the domain meaning.
- Add a FermUnits definition only when Pint genuinely lacks the required unit or qualified
  meaning.

Every FermUnits definition must be traceable to a reliable source. Before a
unit is considered stable, this file should record:

- the unit's exact definition;
- jurisdiction or industry;
- modern, historical, customary, or legal status;
- source title and issuing organization;
- source URL or publication details;
- date accessed;
- accepted aliases and rejected ambiguous aliases.

## Initial vessel definitions

The numerical definitions currently included are provisional pending a formal
source review. They are suitable for establishing and testing the package
architecture, but should not be declared stable until primary or authoritative
industry sources are cited here.

