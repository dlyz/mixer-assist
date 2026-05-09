# This file is auto-generated with generate_fx_nodes.py. Do not edit manually.

import enum
from enum import IntEnum

from ...nodes_base import MixerNode
from ...properties.primitive import BoolProperty, EnumIntProperty, InvertedBoolProperty, LinearFloatProperty, LogFloatProperty

class LowFrequencyOptions(IntEnum):
    V_20_HZ = 0
    V_30_HZ = 1
    V_60_HZ = 2
    V_100_HZ = 3

    _LABELS = enum.nonmember({
        V_20_HZ: '20_Hz',
        V_30_HZ: '30_Hz',
        V_60_HZ: '60_Hz',
        V_100_HZ: '100_Hz',
    })

class HighFrequencyOptions(IntEnum):
    V_3_KHZ = 0
    V_4_KHZ = 1
    V_5_KHZ = 2
    V_8_KHZ = 3
    V_10_KHZ = 4
    V_12_KHZ = 5
    V_16_KHZ = 6

    _LABELS = enum.nonmember({
        V_3_KHZ: '3_kHz',
        V_4_KHZ: '4_kHz',
        V_5_KHZ: '5_kHz',
        V_8_KHZ: '8_kHz',
        V_10_KHZ: '10_kHz',
        V_12_KHZ: '12_kHz',
        V_16_KHZ: '16_kHz',
    })

class AttenuationSelectorOptions(IntEnum):
    V_5_KHZ = 0
    V_10_KHZ = 1
    V_20_KHZ = 2

    _LABELS = enum.nonmember({
        V_5_KHZ: '5_kHz',
        V_10_KHZ: '10_kHz',
        V_20_KHZ: '20_kHz',
    })

class StereoXtecEq1FxParams(MixerNode):
    description = 'Stereo Xtec EQ1 effect parameters (Equalizer category).'

    on = BoolProperty("01")
    gain = LinearFloatProperty("02", -12.0, 12.0, decimals=1, units='dB')
    low_boost = LinearFloatProperty("03", 0.0, 10.0, decimals=1)
    low_frequency = EnumIntProperty("04", LowFrequencyOptions)
    low_attenuation = LinearFloatProperty("05", 0.0, 10.0, decimals=1)
    high_bandwidth = LinearFloatProperty("06", 0.0, 10.0, decimals=1)
    high_boost = LinearFloatProperty("07", 0.0, 10.0, decimals=1)
    high_frequency = EnumIntProperty("08", HighFrequencyOptions)
    high_attenuation = LinearFloatProperty("09", 0.0, 10.0, decimals=1)
    attenuation_selector = EnumIntProperty("10", AttenuationSelectorOptions)
    transfer = BoolProperty("11")

