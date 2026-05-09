# This file is auto-generated with generate_fx_nodes.py. Do not edit manually.

import enum
from enum import IntEnum

from ...nodes_base import MixerNode
from ...properties.primitive import BoolProperty, EnumIntProperty, InvertedBoolProperty, LinearFloatProperty, LogFloatProperty

class PrecisionLimiterFxParams(MixerNode):
    description = 'Precision Limiter effect parameters (Compressor category).'

    input_gain = LinearFloatProperty("01", 0.0, 18.0, decimals=1, units='dB')
    output_gain = LinearFloatProperty("02", -18.0, 0.0, decimals=1, units='dB')
    squeeze = LinearFloatProperty("03", 0.0, 100.0, decimals=1, units='%')
    knee = LinearFloatProperty("04", 0.0, 10.0, decimals=0, units='dB')
    attack = LogFloatProperty("05", 0.05, 1.0, decimals=2, units='ms')
    release = LogFloatProperty("06", 20.0, 2000.0, decimals=0, units='ms')
    stereo_link = BoolProperty("07")
    auto_gain = BoolProperty("08")

