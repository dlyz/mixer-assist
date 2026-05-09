# This file is auto-generated with generate_fx_nodes.py. Do not edit manually.

import enum
from enum import IntEnum

from ...nodes_base import MixerNode
from ...properties.primitive import BoolProperty, EnumIntProperty, InvertedBoolProperty, LinearFloatProperty, LogFloatProperty

class ALowFrequencyOptions(IntEnum):
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

class AMidFrequencyOptions(IntEnum):
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

class AHighFrequencyOptions(IntEnum):
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

class BLowFrequencyOptions(IntEnum):
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

class BMidFrequencyOptions(IntEnum):
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

class BHighFrequencyOptions(IntEnum):
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

class DualXtecEq5FxParams(MixerNode):
    description = 'Dual Xtec EQ5 effect parameters (Equalizer category).'

    a_on = BoolProperty("01")
    a_gain = LinearFloatProperty("02", -12.0, 12.0, decimals=1, units='dB')
    a_low_frequency = EnumIntProperty("03", ALowFrequencyOptions)
    a_low_boost = LinearFloatProperty("04", 0.0, 10.0, decimals=1)
    a_mid_frequency = EnumIntProperty("05", AMidFrequencyOptions)
    a_mid_cut = LinearFloatProperty("06", 0.0, 10.0, decimals=1)
    a_high_frequency = EnumIntProperty("07", AHighFrequencyOptions)
    a_high_boost = LinearFloatProperty("08", 0.0, 10.0, decimals=1)
    a_transfer = BoolProperty("09")
    b_on = BoolProperty("10")
    b_gain = LinearFloatProperty("11", -12.0, 12.0, decimals=1, units='dB')
    b_low_frequency = EnumIntProperty("12", BLowFrequencyOptions)
    b_low_boost = LinearFloatProperty("13", 0.0, 10.0, decimals=1)
    b_mid_frequency = EnumIntProperty("14", BMidFrequencyOptions)
    b_mid_cut = LinearFloatProperty("15", 0.0, 10.0, decimals=1)
    b_high_frequency = EnumIntProperty("16", BHighFrequencyOptions)
    b_high_boost = LinearFloatProperty("17", 0.0, 10.0, decimals=1)
    b_transfer = BoolProperty("18")

