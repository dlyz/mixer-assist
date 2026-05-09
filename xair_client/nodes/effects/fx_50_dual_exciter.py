# This file is auto-generated with generate_fx_nodes.py. Do not edit manually.

import enum
from enum import IntEnum

from ...nodes_base import MixerNode
from ...properties.primitive import BoolProperty, EnumIntProperty, InvertedBoolProperty, LinearFloatProperty, LogFloatProperty

class DualExciterFxParams(MixerNode):
    description = 'Dual Exciter effect parameters (Enhancer category).'

    a_tune = LogFloatProperty("01", 1000.0, 10000.0, decimals=0, units='Hz')
    a_peak = LinearFloatProperty("02", 0.0, 100.0, decimals=0, units='%')
    a_zero_fill = LinearFloatProperty("03", 0.0, 100.0, decimals=0, units='%')
    a_timbre = LinearFloatProperty("04", -50.0, 50.0, decimals=0)
    a_harmonics = LinearFloatProperty("05", 0.0, 100.0, decimals=0, units='%')
    a_mix = LinearFloatProperty("06", 0.0, 100.0, decimals=0, units='%')
    a_solo_mode = BoolProperty("07")
    b_tune = LogFloatProperty("08", 1000.0, 10000.0, decimals=0, units='Hz')
    b_peak = LinearFloatProperty("09", 0.0, 100.0, decimals=0, units='%')
    b_zero_fill = LinearFloatProperty("10", 0.0, 100.0, decimals=0, units='%')
    b_timbre = LinearFloatProperty("11", -50.0, 50.0, decimals=0)
    b_harmonics = LinearFloatProperty("12", 0.0, 100.0, decimals=0, units='%')
    b_mix = LinearFloatProperty("13", 0.0, 100.0, decimals=0, units='%')
    b_solo_mode = BoolProperty("14")

