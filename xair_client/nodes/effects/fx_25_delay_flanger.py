# This file is auto-generated with generate_fx_nodes.py. Do not edit manually.

import enum
from enum import IntEnum

from ...nodes_base import MixerNode
from ...properties.primitive import BoolProperty, EnumIntProperty, InvertedBoolProperty, LinearFloatProperty, LogFloatProperty

class DelayPatternOptions(IntEnum):
    V_1_4 = 0
    V_1_3 = 1
    V_3_8 = 2
    V_1_2 = 3
    V_2_3 = 4
    V_3_4 = 5
    V_1 = 6
    V_1_4X = 7
    V_1_3X = 8
    V_3_8X = 9
    V_1_2X = 10
    V_2_3X = 11
    V_3_4X = 12
    V_1X = 13

    _LABELS = enum.nonmember({
        V_1_4: '1/4',
        V_1_3: '1/3',
        V_3_8: '3/8',
        V_1_2: '1/2',
        V_2_3: '2/3',
        V_3_4: '3/4',
        V_1: '1',
        V_1_4X: '1/4X',
        V_1_3X: '1/3X',
        V_3_8X: '3/8X',
        V_1_2X: '1/2X',
        V_2_3X: '2/3X',
        V_3_4X: '3/4X',
        V_1X: '1X',
    })

class DelayFlangerFxParams(MixerNode):
    description = 'Delay + Flanger effect parameters (Delay category).'

    delay_time = LinearFloatProperty("01", 1.0, 3000.0, decimals=0, units='ms')
    delay_pattern = EnumIntProperty("02", DelayPatternOptions)
    delay_feedback_high_cut = LogFloatProperty("03", 1000.0, 20000.0, decimals=0, units='Hz')
    delay_feedback = LinearFloatProperty("04", 0.0, 100.0, decimals=0, units='%')
    cross_feedback = LinearFloatProperty("05", 0.0, 100.0, decimals=0, units='%')
    balance = LinearFloatProperty("06", -100.0, 100.0, decimals=0, units='%')
    flanger_speed = LogFloatProperty("07", 0.05, 4.0, decimals=2, units='Hz')
    flanger_depth = LinearFloatProperty("08", 0.0, 100.0, decimals=0, units='%')
    flanger_delay = LogFloatProperty("09", 0.5, 50.0, decimals=1, units='ms')
    flanger_phase = LinearFloatProperty("10", 0.0, 180.0, decimals=0, units='°')
    flanger_feedback = LinearFloatProperty("11", -90.0, 90.0, decimals=0, units='%')
    mix = LinearFloatProperty("12", 0.0, 100.0, decimals=0, units='%')

