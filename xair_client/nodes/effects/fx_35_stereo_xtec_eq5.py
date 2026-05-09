# This file is auto-generated with generate_fx_nodes.py. Do not edit manually.

import enum
from enum import IntEnum

from ...nodes_base import MixerNode
from ...properties.primitive import BoolProperty, EnumIntProperty, InvertedBoolProperty, LinearFloatProperty, LogFloatProperty

class LowFrequencyOptions(IntEnum):
    V_200_HZ = 0
    V_300_HZ = 1
    V_500_HZ = 2
    V_700_HZ = 3
    V_1_KHZ = 4

    _LABELS = enum.nonmember({
        V_200_HZ: '200_Hz',
        V_300_HZ: '300_Hz',
        V_500_HZ: '500_Hz',
        V_700_HZ: '700_Hz',
        V_1_KHZ: '1_kHz',
    })

class MidFrequencyOptions(IntEnum):
    V_200_HZ = 0
    V_300_HZ = 1
    V_500_HZ = 2
    V_700_HZ = 3
    V_1_KHZ = 4
    V_1_5_KHZ = 5
    V_2_KHZ = 6
    V_3_KHZ = 7
    V_4_KHZ = 8
    V_5_KHZ = 9
    V_7_KHZ = 10

    _LABELS = enum.nonmember({
        V_200_HZ: '200_Hz',
        V_300_HZ: '300_Hz',
        V_500_HZ: '500_Hz',
        V_700_HZ: '700_Hz',
        V_1_KHZ: '1_kHz',
        V_1_5_KHZ: '1.5_kHz',
        V_2_KHZ: '2_kHz',
        V_3_KHZ: '3_kHz',
        V_4_KHZ: '4_kHz',
        V_5_KHZ: '5_kHz',
        V_7_KHZ: '7_kHz',
    })

class HighFrequencyOptions(IntEnum):
    V_1_5_KHZ = 0
    V_2_KHZ = 1
    V_3_KHZ = 2
    V_4_KHZ = 3
    V_5_KHZ = 4

    _LABELS = enum.nonmember({
        V_1_5_KHZ: '1.5_kHz',
        V_2_KHZ: '2_kHz',
        V_3_KHZ: '3_kHz',
        V_4_KHZ: '4_kHz',
        V_5_KHZ: '5_kHz',
    })

class StereoXtecEq5FxParams(MixerNode):
    description = 'Stereo Xtec EQ5 effect parameters (Equalizer category).'

    on = BoolProperty("01")
    gain = LinearFloatProperty("02", -12.0, 12.0, decimals=1, units='dB')
    low_frequency = EnumIntProperty("03", LowFrequencyOptions)
    low_boost = LinearFloatProperty("04", 0.0, 10.0, decimals=1)
    mid_frequency = EnumIntProperty("05", MidFrequencyOptions)
    mid_cut = LinearFloatProperty("06", 0.0, 10.0, decimals=1)
    high_frequency = EnumIntProperty("07", HighFrequencyOptions)
    high_boost = LinearFloatProperty("08", 0.0, 10.0, decimals=1)
    transfer = BoolProperty("09")

