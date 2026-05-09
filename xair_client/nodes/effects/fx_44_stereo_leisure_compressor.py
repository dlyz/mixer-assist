# This file is auto-generated with generate_fx_nodes.py. Do not edit manually.

import enum
from enum import IntEnum

from ...nodes_base import MixerNode
from ...properties.primitive import BoolProperty, EnumIntProperty, InvertedBoolProperty, LinearFloatProperty, LogFloatProperty

class CompressorLimiterOptions(IntEnum):
    COMPRESSOR = 0
    LIMITER = 1

class StereoLeisureCompressorFxParams(MixerNode):
    description = 'Stereo Leisure Compressor effect parameters (Compressor category).'

    on = BoolProperty("01")
    gain = LinearFloatProperty("02", 0.0, 100.0, decimals=0)
    peak_reduction = LinearFloatProperty("03", 0.0, 100.0, decimals=0)
    compressor_limiter = EnumIntProperty("04", CompressorLimiterOptions)
    output_gain = LinearFloatProperty("05", -18.0, 6.0, decimals=1, units='dB')

