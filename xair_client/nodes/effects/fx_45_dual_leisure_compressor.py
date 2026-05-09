# This file is auto-generated with generate_fx_nodes.py. Do not edit manually.

import enum
from enum import IntEnum

from ...nodes_base import MixerNode
from ...properties.primitive import BoolProperty, EnumIntProperty, InvertedBoolProperty, LinearFloatProperty, LogFloatProperty

class ACompressorLimiterOptions(IntEnum):
    COMPRESSOR = 0
    LIMITER = 1

class BCompressorLimiterOptions(IntEnum):
    COMPRESSOR = 0
    LIMITER = 1

class DualLeisureCompressorFxParams(MixerNode):
    description = 'Dual Leisure Compressor effect parameters (Compressor category).'

    a_on = BoolProperty("01")
    a_gain = LinearFloatProperty("02", 0.0, 100.0, decimals=0)
    a_peak_reduction = LinearFloatProperty("03", 0.0, 100.0, decimals=0)
    a_compressor_limiter = EnumIntProperty("04", ACompressorLimiterOptions)
    a_output_gain = LinearFloatProperty("05", -18.0, 6.0, decimals=1, units='dB')
    b_on = BoolProperty("06")
    b_gain = LinearFloatProperty("07", 0.0, 100.0, decimals=0)
    b_peak_reduction = LinearFloatProperty("08", 0.0, 100.0, decimals=0)
    b_compressor_limiter = EnumIntProperty("09", BCompressorLimiterOptions)
    b_output_gain = LinearFloatProperty("10", -18.0, 6.0, decimals=1, units='dB')

