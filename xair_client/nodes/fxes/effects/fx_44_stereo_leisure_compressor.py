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

class CompressorLimiterOptions(IntEnum):
    COMPRESSOR = 0
    LIMITER = 1

class StereoLeisureCompressorFxParams(MixerNode):
    description = 'Stereo Leisure Compressor effect parameters (Compressor category).'

    on = BoolProperty("01")
    gain = LinearFloatProperty("02", 0.0, 100.0, decimals=0, grid_size=51)
    peak_reduction = LinearFloatProperty("03", 0.0, 100.0, decimals=0, grid_size=51)
    compressor_limiter = EnumIntProperty("04", CompressorLimiterOptions)
    output_gain = LinearFloatProperty("05", -18.0, 6.0, decimals=1, grid_size=49, units='dB')

