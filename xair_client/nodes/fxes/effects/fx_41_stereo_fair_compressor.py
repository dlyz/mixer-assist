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

class StereoFairCompressorFxParams(MixerNode):
    description = 'Stereo Fair Compressor effect parameters (Compressor category).'

    on = BoolProperty("01")
    gain = LinearFloatProperty("02", -20.0, 0.0, decimals=1, grid_size=41, units='dB')
    threshold = LinearFloatProperty("03", 0.0, 10.0, decimals=1, grid_size=101)
    time = LinearFloatProperty("04", 1.0, 6.0, decimals=0, grid_size=6, units='ms')
    bias = LinearFloatProperty("05", 0.0, 100.0, decimals=0, grid_size=51, units='%')
    output_gain = LinearFloatProperty("06", -18.0, 6.0, decimals=1, grid_size=49, units='dB')
    balance = LinearFloatProperty("07", -100.0, 100.0, decimals=0, grid_size=41, units='%')

