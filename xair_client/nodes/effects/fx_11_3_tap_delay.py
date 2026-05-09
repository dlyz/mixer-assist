# This file is auto-generated with generate_fx_nodes.py. Do not edit manually.

import enum
from enum import IntEnum

from ...nodes_base import MixerNode
from ...properties.primitive import BoolProperty, EnumIntProperty, InvertedBoolProperty, LinearFloatProperty, LogFloatProperty

class FactorAOptions(IntEnum):
    V_1_4 = 0
    V_3_8 = 1
    V_1_2 = 2
    V_2_3 = 3
    V_1 = 4
    V_4_3 = 5
    V_3_2 = 6
    V_2 = 7
    V_3 = 8

    _LABELS = enum.nonmember({
        V_1_4: '1/4',
        V_3_8: '3/8',
        V_1_2: '1/2',
        V_2_3: '2/3',
        V_1: '1',
        V_4_3: '4/3',
        V_3_2: '3/2',
        V_2: '2',
        V_3: '3',
    })

class FactorBOptions(IntEnum):
    V_1_4 = 0
    V_3_8 = 1
    V_1_2 = 2
    V_2_3 = 3
    V_1 = 4
    V_4_3 = 5
    V_3_2 = 6
    V_2 = 7
    V_3 = 8

    _LABELS = enum.nonmember({
        V_1_4: '1/4',
        V_3_8: '3/8',
        V_1_2: '1/2',
        V_2_3: '2/3',
        V_1: '1',
        V_4_3: '4/3',
        V_3_2: '3/2',
        V_2: '2',
        V_3: '3',
    })

class Fx3TapDelayFxParams(MixerNode):
    description = '3-Tap Delay effect parameters (Delay category).'

    time = LinearFloatProperty("01", 1.0, 3000.0, decimals=0, units='ms')
    gain_base = LinearFloatProperty("02", 0.0, 100.0, decimals=0, units='%')
    pan_base = LinearFloatProperty("03", -100.0, 100.0, decimals=0, units='%')
    feed = LinearFloatProperty("04", 0.0, 100.0, decimals=0, units='%')
    low_cut = LogFloatProperty("05", 10.0, 500.0, decimals=0, units='Hz')
    high_cut = LogFloatProperty("06", 200.0, 20000.0, decimals=0, units='Hz')
    factor_a = EnumIntProperty("07", FactorAOptions)
    gain_a = LinearFloatProperty("08", 0.0, 100.0, decimals=0, units='%')
    pan_a = LinearFloatProperty("09", -100.0, 100.0, decimals=0, units='%')
    factor_b = EnumIntProperty("10", FactorBOptions)
    gain_b = LinearFloatProperty("11", 0.0, 100.0, decimals=0, units='%')
    pan_b = LinearFloatProperty("12", -100.0, 100.0, decimals=0, units='%')
    cross_feedback = BoolProperty("13")
    mono = BoolProperty("14")
    dry = BoolProperty("15")

