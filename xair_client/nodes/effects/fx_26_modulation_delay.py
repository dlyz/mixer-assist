# This file is auto-generated with generate_fx_nodes.py. Do not edit manually.

import enum
from enum import IntEnum

from ...nodes_base import MixerNode
from ...properties.primitive import BoolProperty, EnumIntProperty, InvertedBoolProperty, LinearFloatProperty, LogFloatProperty

class PatternOptions(IntEnum):
    DELAY = 0
    V_1_2 = 1
    V_2_3 = 2
    V_3_2 = 3

    _LABELS = enum.nonmember({
        DELAY: 'Delay',
        V_1_2: '1/2',
        V_2_3: '2/3',
        V_3_2: '3/2',
    })

class TypeOptions(IntEnum):
    AMBIENCE = 0
    CLUB = 1
    HALL = 2

class ModulationDelayFxParams(MixerNode):
    description = 'Modulation Delay effect parameters (Delay category).'

    time = LinearFloatProperty("01", 1.0, 3000.0, decimals=0, units='ms')
    pattern = EnumIntProperty("02", PatternOptions)
    feedback = LinearFloatProperty("03", 0.0, 100.0, decimals=0, units='%')
    low_cut = LogFloatProperty("04", 10.0, 500.0, decimals=0, units='Hz')
    high_cut = LogFloatProperty("05", 200.0, 20000.0, decimals=0, units='Hz')
    depth = LinearFloatProperty("06", 0.0, 100.0, decimals=0, units='%')
    rate = LogFloatProperty("07", 0.05, 10.0, decimals=2, units='Hz')
    ser = BoolProperty("08")
    type = EnumIntProperty("09", TypeOptions)
    decay = LinearFloatProperty("10", 1.0, 10.0, decimals=1, units='s')
    high_damp = LogFloatProperty("11", 1000.0, 20000.0, decimals=0, units='Hz')
    balance = LinearFloatProperty("12", -100.0, 100.0, decimals=0, units='%')
    mix = LinearFloatProperty("13", 0.0, 100.0, decimals=0, units='%')

