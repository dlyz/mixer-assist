# This file is auto-generated with generate_fx_nodes.py. Do not edit manually.

import enum
from enum import IntEnum

from ...nodes_base import MixerNode
from ...properties.primitive import BoolProperty, EnumIntProperty, InvertedBoolProperty, LinearFloatProperty, LogFloatProperty

class ARangeOptions(IntEnum):
    LO = 0
    MID = 1
    HI = 2

class BRangeOptions(IntEnum):
    LO = 0
    MID = 1
    HI = 2

class SuboctaverFxParams(MixerNode):
    description = 'Suboctaver effect parameters (Pitch category).'

    a_active = BoolProperty("01")
    a_range = EnumIntProperty("02", ARangeOptions)
    a_direct = LinearFloatProperty("03", 0.0, 100.0, decimals=0, units='%')
    a_octave_1 = LinearFloatProperty("04", 0.0, 100.0, decimals=0, units='%')
    a_octave_2 = LinearFloatProperty("05", 0.0, 100.0, decimals=0, units='%')
    b_active = BoolProperty("06")
    b_range = EnumIntProperty("07", BRangeOptions)
    b_direct = LinearFloatProperty("08", 0.0, 100.0, decimals=0, units='%')
    b_octave_1 = LinearFloatProperty("09", 0.0, 100.0, decimals=0, units='%')
    b_octave_2 = LinearFloatProperty("10", 0.0, 100.0, decimals=0, units='%')

