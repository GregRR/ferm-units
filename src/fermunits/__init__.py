"""Fermentation-industry units and conversions built on Pint."""

from importlib.metadata import (
    PackageNotFoundError,
)
from importlib.metadata import (
    version as _distribution_version,
)

from fermunits.bitterness import (
    absorbance_275nm_to_bitterness_units,
    bitterness_units_to_absorbance_275nm,
)
from fermunits.carbonation import (
    co2_grams_per_liter_to_volumes,
    co2_mass_concentration_to_volumes,
    co2_volumes_to_grams_per_liter,
    co2_volumes_to_mass_concentration,
)
from fermunits.color import (
    ebc_to_srm,
    lovibond_to_srm_approx,
    srm_to_ebc,
    srm_to_lovibond_approx,
)
from fermunits.diastatic import (
    lintner_to_windisch_kolbach,
    windisch_kolbach_to_lintner,
)
from fermunits.gravity import (
    gravity_points_to_sg,
    plato_to_sg,
    plato_to_wort_refractometer_brix,
    sg_to_gravity_points,
    sg_to_plato,
    wort_refractometer_brix_to_plato,
)
from fermunits.registry import Q_, create_registry, ureg
from fermunits.solution_chemistry import (
    amount_concentration_to_equivalent_concentration,
    amount_concentration_to_mass_concentration,
    amount_to_equivalents,
    caco3_basis_mass_concentration_to_equivalent_concentration,
    equivalent_concentration_to_amount_concentration,
    equivalent_concentration_to_caco3_basis_mass_concentration,
    equivalent_concentration_to_mass_concentration,
    equivalents_to_amount,
    mass_concentration_to_amount_concentration,
    mass_concentration_to_equivalent_concentration,
    mass_concentration_to_mass_fraction,
    mass_fraction_to_mass_concentration,
)

__all__ = [
    "Q_",
    "absorbance_275nm_to_bitterness_units",
    "amount_concentration_to_equivalent_concentration",
    "amount_concentration_to_mass_concentration",
    "amount_to_equivalents",
    "bitterness_units_to_absorbance_275nm",
    "caco3_basis_mass_concentration_to_equivalent_concentration",
    "co2_grams_per_liter_to_volumes",
    "co2_mass_concentration_to_volumes",
    "co2_volumes_to_grams_per_liter",
    "co2_volumes_to_mass_concentration",
    "create_registry",
    "ebc_to_srm",
    "equivalent_concentration_to_amount_concentration",
    "equivalent_concentration_to_caco3_basis_mass_concentration",
    "equivalent_concentration_to_mass_concentration",
    "equivalents_to_amount",
    "gravity_points_to_sg",
    "lintner_to_windisch_kolbach",
    "lovibond_to_srm_approx",
    "mass_concentration_to_amount_concentration",
    "mass_concentration_to_equivalent_concentration",
    "mass_concentration_to_mass_fraction",
    "mass_fraction_to_mass_concentration",
    "plato_to_sg",
    "plato_to_wort_refractometer_brix",
    "sg_to_gravity_points",
    "sg_to_plato",
    "srm_to_ebc",
    "srm_to_lovibond_approx",
    "ureg",
    "windisch_kolbach_to_lintner",
    "wort_refractometer_brix_to_plato",
]

try:
    __version__ = _distribution_version("ferm-units")
except PackageNotFoundError:
    __version__ = "0+unknown"
