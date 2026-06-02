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

class WaveDesignerFxParams(MixerNode):
    description = 'Wave Designer effect parameters (Enhancer category).'

    a_attack = LinearFloatProperty("01", -100.0, 100.0, decimals=0, grid_size=101, units='%')
    a_sustain = LinearFloatProperty("02", -100.0, 100.0, decimals=0, grid_size=101, units='%')
    a_gain = LinearFloatProperty("03", -24.0, 24.0, decimals=1, grid_size=97, units='dB')
    b_attack = LinearFloatProperty("04", -100.0, 100.0, decimals=0, grid_size=101, units='%')
    b_sustain = LinearFloatProperty("05", -100.0, 100.0, decimals=0, grid_size=101, units='%')
    b_gain = LinearFloatProperty("06", -24.0, 24.0, decimals=1, grid_size=97, units='dB')

