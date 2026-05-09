# This file is auto-generated with generate_fx_nodes.py. Do not edit manually.

import enum
from enum import IntEnum

from ...nodes_base import MixerNode
from ...properties.primitive import BoolProperty, EnumIntProperty, InvertedBoolProperty, LinearFloatProperty, LogFloatProperty

class StereoPitchShifterFxParams(MixerNode):
    description = 'Stereo Pitch Shifter effect parameters (Pitch category).'

    semi = LinearFloatProperty("01", -12.0, 12.0, decimals=0)
    cent = LinearFloatProperty("02", -50.0, 50.0, decimals=0)
    delay = LogFloatProperty("03", 1.0, 500.0, decimals=1, units='ms')
    low_cut = LogFloatProperty("04", 10.0, 500.0, decimals=0, units='Hz')
    high_cut = LogFloatProperty("05", 2000.0, 20000.0, decimals=0, units='Hz')
    mix = LinearFloatProperty("06", 0.0, 100.0, decimals=0, units='%')

