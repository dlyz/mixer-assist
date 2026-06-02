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

class ReverseReverbFxParams(MixerNode):
    description = 'Reverse Reverb effect parameters (Reverb category).'

    pre_delay = LinearFloatProperty("01", 0.0, 200.0, decimals=0, grid_size=101, units='ms')
    decay = LinearFloatProperty("02", 140.0, 1000.0, decimals=0, grid_size=51, units='ms')
    rise = LinearFloatProperty("03", 0.0, 50.0, decimals=0, grid_size=51)
    diff = LinearFloatProperty("04", 1.0, 30.0, decimals=0, grid_size=30)
    spread = LinearFloatProperty("05", 0.0, 100.0, decimals=0, grid_size=51)
    level = LinearFloatProperty("06", -12.0, 12.0, decimals=1, grid_size=49, units='dB')
    low_cut = LogFloatProperty("07", 10.0, 500.0, decimals=0, grid_size=51, units='Hz')
    high_shelf_frequency = LogFloatProperty("08", 200.0, 20000.0, decimals=0, grid_size=51, units='Hz')
    high_shelf_gain = LinearFloatProperty("09", -30.0, 0.0, decimals=1, grid_size=61, units='dB')

