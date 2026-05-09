# This file is auto-generated with generate_fx_nodes.py. Do not edit manually.

import enum
from enum import IntEnum

from ...nodes_base import MixerNode
from ...properties.primitive import BoolProperty, EnumIntProperty, InvertedBoolProperty, LinearFloatProperty, LogFloatProperty

class MSFairCompressorFxParams(MixerNode):
    description = 'M/S Fair Compressor effect parameters (Compressor category).'

    middle_on = BoolProperty("01")
    middle_gain = LinearFloatProperty("02", -20.0, 0.0, decimals=1, units='dB')
    middle_threshold = LinearFloatProperty("03", 0.0, 10.0, decimals=1)
    middle_time = LinearFloatProperty("04", 1.0, 6.0, decimals=0, units='ms')
    middle_bias = LinearFloatProperty("05", 0.0, 100.0, decimals=0, units='%')
    middle_output_gain = LinearFloatProperty("06", -18.0, 6.0, decimals=1, units='dB')
    middle_balance = LinearFloatProperty("07", -100.0, 100.0, decimals=0, units='%')
    sides_gain = LinearFloatProperty("08", -20.0, 0.0, decimals=1, units='dB')
    sides_threshold = LinearFloatProperty("09", 0.0, 10.0, decimals=1)
    sides_time = LinearFloatProperty("10", 1.0, 6.0, decimals=0, units='ms')
    sides_bias = LinearFloatProperty("11", 0.0, 100.0, decimals=0, units='%')
    sides_output_gain = LinearFloatProperty("12", -18.0, 6.0, decimals=1, units='dB')
    sides_balance = LinearFloatProperty("13", -100.0, 100.0, decimals=0, units='%')

