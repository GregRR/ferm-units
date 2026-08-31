"""Static regression checks for solution-chemistry semantic APIs."""

from typing import assert_type

from fermunits import (
    PHValue,
    hydrogen_ion_activity_to_ph,
    ph_to_hydrogen_ion_activity,
)

ph = PHValue(7.0)

assert_type(ph.value, float)
assert_type(ph_to_hydrogen_ion_activity(ph), float)
assert_type(hydrogen_ion_activity_to_ph(1e-7), PHValue)
