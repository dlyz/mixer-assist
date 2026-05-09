# This file is auto-generated with generate_fx_nodes.py. Do not edit manually.

import enum
from enum import IntEnum

from ...nodes_base import MixerNode
from ...properties.primitive import BoolProperty, EnumIntProperty, InvertedBoolProperty, LinearFloatProperty, LogFloatProperty

class ModeOptions(IntEnum):
    STEREO_FEED_MODE = 0
    CROSS_FEED_MODE = 1
    MONO_FEED_MODE = 2

class FactorLOptions(IntEnum):
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

class FactorROptions(IntEnum):
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

class StereoDelayFxParams(MixerNode):
    description = 'Stereo Delay effect parameters (Delay category).'

    mix = LinearFloatProperty("01", 0.0, 100.0, decimals=0, units='%')
    time = LinearFloatProperty("02", 1.0, 3000.0, decimals=0, units='ms')
    mode = EnumIntProperty("03", ModeOptions)
    factor_l = EnumIntProperty("04", FactorLOptions)
    factor_r = EnumIntProperty("05", FactorROptions)
    offset_lr = LinearFloatProperty("06", -100.0, 100.0, decimals=0, units='ms')
    low_cut = LogFloatProperty("07", 10.0, 500.0, decimals=0, units='Hz')
    high_cut = LogFloatProperty("08", 200.0, 20000.0, decimals=0, units='Hz')
    feed_low_cut = LogFloatProperty("09", 10.0, 500.0, decimals=0, units='Hz')
    feed_l = LinearFloatProperty("10", 0.0, 100.0, decimals=0, units='%')
    feed_r = LinearFloatProperty("11", 0.0, 100.0, decimals=0, units='%')
    feedback_high_cut = LogFloatProperty("12", 200.0, 20000.0, decimals=0, units='Hz')

