# This file is auto-generated with generate_fx_nodes.py. Do not edit manually.

import enum
from enum import IntEnum

from ...nodes_base import MixerNode
from ...properties.primitive import BoolProperty, EnumIntProperty, InvertedBoolProperty, LinearFloatProperty, LogFloatProperty

class StereoExciterFxParams(MixerNode):
    description = 'Stereo Exciter effect parameters (Enhancer category).'

    tune = LogFloatProperty("01", 1000.0, 10000.0, decimals=0, units='Hz')
    peak = LinearFloatProperty("02", 0.0, 100.0, decimals=0, units='%')
    zero_fill = LinearFloatProperty("03", 0.0, 100.0, decimals=0, units='%')
    timbre = LinearFloatProperty("04", -50.0, 50.0, decimals=0)
    harmonics = LinearFloatProperty("05", 0.0, 100.0, decimals=0, units='%')
    mix = LinearFloatProperty("06", 0.0, 100.0, decimals=0, units='%')
    solo_mode = BoolProperty("07")

