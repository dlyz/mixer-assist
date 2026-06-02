# This file is auto-generated with generate_fx_nodes.py. Do not edit manually.

import enum
from enum import IntEnum

from ...core.base_types import MixerNode
from ...core.primitive_props import (
    BoolProperty,
    EnumIntProperty,
    InvertedBoolProperty,
    LinearFloatProperty,
    LogFloatProperty,
)

class SoundMaxerFxParams(MixerNode):
    description = 'Sound Maxer effect parameters (Enhancer category).'

    a_on = BoolProperty("01")
    a_low_contour = LinearFloatProperty("02", 0.0, 10.0, decimals=1, grid_size=51)
    a_process = LinearFloatProperty("03", 0.0, 10.0, decimals=1, grid_size=51)
    a_gain = LinearFloatProperty("04", -12.0, 12.0, decimals=1, grid_size=49, units='dB')
    b_on = BoolProperty("05")
    b_low_contour = LinearFloatProperty("06", 0.0, 10.0, decimals=1, grid_size=51)
    b_process = LinearFloatProperty("07", 0.0, 10.0, decimals=1, grid_size=51)
    b_gain = LinearFloatProperty("08", -12.0, 12.0, decimals=1, grid_size=49, units='dB')

