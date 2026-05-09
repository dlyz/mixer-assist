# This file is auto-generated with generate_fx_nodes.py. Do not edit manually.

import enum
from enum import IntEnum

from ...nodes_base import MixerNode
from ...properties.primitive import BoolProperty, EnumIntProperty, InvertedBoolProperty, LinearFloatProperty, LogFloatProperty

class DualPitchShifterFxParams(MixerNode):
    description = 'Dual Pitch Shifter effect parameters (Pitch category).'

    a_semi = LinearFloatProperty("01", -12.0, 12.0, decimals=0)
    a_cent = LinearFloatProperty("02", -50.0, 50.0, decimals=0)
    a_delay = LogFloatProperty("03", 1.0, 500.0, decimals=1, units='ms')
    a_gain = LinearFloatProperty("04", 0.0, 100.0, decimals=0, units='%')
    a_pan = LinearFloatProperty("05", -100.0, 100.0, decimals=0, units='%')
    mix = LinearFloatProperty("06", 0.0, 100.0, decimals=0, units='%')
    b_semi = LinearFloatProperty("07", -12.0, 12.0, decimals=0)
    b_cent = LinearFloatProperty("08", -50.0, 50.0, decimals=0)
    b_delay = LogFloatProperty("09", 1.0, 500.0, decimals=1, units='ms')
    b_gain = LinearFloatProperty("10", 0.0, 100.0, decimals=0, units='%')
    b_pan = LinearFloatProperty("11", -100.0, 100.0, decimals=0, units='%')
    high_cut = LogFloatProperty("12", 2000.0, 20000.0, decimals=0, units='Hz')

