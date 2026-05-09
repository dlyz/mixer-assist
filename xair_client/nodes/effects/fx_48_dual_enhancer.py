# This file is auto-generated with generate_fx_nodes.py. Do not edit manually.

import enum
from enum import IntEnum

from ...nodes_base import MixerNode
from ...properties.primitive import BoolProperty, EnumIntProperty, InvertedBoolProperty, LinearFloatProperty, LogFloatProperty

class DualEnhancerFxParams(MixerNode):
    description = 'Dual Enhancer effect parameters (Enhancer category).'

    a_output_gain = LinearFloatProperty("01", -12.0, 12.0, decimals=1, units='dB')
    a_bass_gain = LinearFloatProperty("02", 0.0, 100.0, decimals=0, units='%')
    a_bass_freq = LinearFloatProperty("03", 1.0, 50.0, decimals=0)
    a_middle_gain = LinearFloatProperty("04", 0.0, 100.0, decimals=0, units='%')
    a_middle_q = LinearFloatProperty("05", 1.0, 50.0, decimals=0)
    a_high_gain = LinearFloatProperty("06", 0.0, 100.0, decimals=0, units='%')
    a_high_freq = LinearFloatProperty("07", 1.0, 50.0, decimals=0)
    a_solo_mode = BoolProperty("08")
    b_output_gain = LinearFloatProperty("09", -12.0, 12.0, decimals=1, units='dB')
    b_bass_gain = LinearFloatProperty("10", 0.0, 100.0, decimals=0, units='%')
    b_bass_freq = LinearFloatProperty("11", 1.0, 50.0, decimals=0)
    b_middle_gain = LinearFloatProperty("12", 0.0, 100.0, decimals=0, units='%')
    b_middle_q = LinearFloatProperty("13", 1.0, 50.0, decimals=0)
    b_high_gain = LinearFloatProperty("14", 0.0, 100.0, decimals=0, units='%')
    b_high_freq = LinearFloatProperty("15", 1.0, 50.0, decimals=0)
    b_solo_mode = BoolProperty("16")

