# This file is auto-generated with generate_fx_nodes.py. Do not edit manually.

import enum
from enum import IntEnum

from ...nodes_base import MixerNode
from ...properties.primitive import BoolProperty, EnumIntProperty, InvertedBoolProperty, LinearFloatProperty, LogFloatProperty

class DualFairCompressorFxParams(MixerNode):
    description = 'Dual Fair Compressor effect parameters (Compressor category).'

    a_on = BoolProperty("01")
    a_gain = LinearFloatProperty("02", -20.0, 0.0, decimals=1, grid_size=41, units='dB')
    a_threshold = LinearFloatProperty("03", 0.0, 10.0, decimals=1, grid_size=101)
    a_time = LinearFloatProperty("04", 1.0, 6.0, decimals=0, grid_size=6, units='ms')
    a_bias = LinearFloatProperty("05", 0.0, 100.0, decimals=0, grid_size=51, units='%')
    a_output_gain = LinearFloatProperty("06", -18.0, 6.0, decimals=1, grid_size=49, units='dB')
    a_balance = LinearFloatProperty("07", -100.0, 100.0, decimals=0, grid_size=41, units='%')
    a_on = BoolProperty("08")
    b_gain = LinearFloatProperty("09", -20.0, 0.0, decimals=1, grid_size=41, units='dB')
    b_threshold = LinearFloatProperty("10", 0.0, 10.0, decimals=1, grid_size=101)
    b_time = LinearFloatProperty("11", 1.0, 6.0, decimals=0, grid_size=6, units='ms')
    b_bias = LinearFloatProperty("12", 0.0, 100.0, decimals=0, grid_size=51, units='%')
    b_output_gain = LinearFloatProperty("13", -18.0, 6.0, decimals=1, grid_size=49, units='dB')
    b_balance = LinearFloatProperty("14", -100.0, 100.0, decimals=0, grid_size=41, units='%')

