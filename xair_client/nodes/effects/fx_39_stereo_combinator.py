# This file is auto-generated with generate_fx_nodes.py. Do not edit manually.

import enum
from enum import IntEnum

from ...nodes_base import MixerNode
from ...properties.primitive import BoolProperty, EnumIntProperty, InvertedBoolProperty, LinearFloatProperty, LogFloatProperty

class BandOptions(IntEnum):
    ALL = 0
    LOW = 1
    LOW_MID = 2
    MID = 3
    HIGH_MID = 4
    HIGH = 5

class GlobalRatioOptions(IntEnum):
    V_1_1 = 0
    V_1_2 = 1
    V_1_3 = 2
    V_1_5 = 3
    V_1_7 = 4
    V_2 = 5
    V_2_5 = 6
    V_3 = 7
    V_3_5 = 8
    V_4 = 9
    V_5 = 10
    V_7 = 11
    V_10 = 12
    LIMIT = 13

    _LABELS = enum.nonmember({
        V_1_1: '1.1',
        V_1_2: '1.2',
        V_1_3: '1.3',
        V_1_5: '1.5',
        V_1_7: '1.7',
        V_2: '2',
        V_2_5: '2.5',
        V_3: '3',
        V_3_5: '3.5',
        V_4: '4',
        V_5: '5',
        V_7: '7',
        V_10: '10',
        LIMIT: 'Limit',
    })

class MetersOptions(IntEnum):
    BAND_GAIN_REDUCTION = 0
    BAND_LEVEL_METERS_PEAK = 1
    AUTOMATIC_SPECTRUM_BALANCE = 2

class StereoCombinatorFxParams(MixerNode):
    description = 'Stereo Combinator effect parameters (Other category).'

    bypass = InvertedBoolProperty("01")
    band = EnumIntProperty("02", BandOptions)
    mix = LinearFloatProperty("03", 0.0, 100.0, decimals=0, units='%')
    attack = LinearFloatProperty("04", 0.0, 19.0, decimals=0)
    release = LogFloatProperty("05", 20.0, 3000.0, decimals=0, units='ms')
    auto_release = BoolProperty("06")
    speed_sbc = LinearFloatProperty("07", 1.0, 10.0, decimals=0)
    sbc = BoolProperty("08")
    x_over = LinearFloatProperty("09", -50.0, 50.0, decimals=0)
    v_48_db = BoolProperty("10")
    global_ratio = EnumIntProperty("11", GlobalRatioOptions)
    trim_threshold = LinearFloatProperty("12", -40.0, 0.0, decimals=1, units='dB')
    trim_gain = LinearFloatProperty("13", -10.0, 10.0, decimals=1, units='dB')
    low_band_threshold = LinearFloatProperty("14", -10.0, 10.0, decimals=1, units='dB')
    low_band_gain = LinearFloatProperty("15", -10.0, 10.0, decimals=1, units='dB')
    low_band_threshold_bypass = BoolProperty("16")
    low_mid_band_threshold = LinearFloatProperty("17", -10.0, 10.0, decimals=1, units='dB')
    low_mid_band_gain = LinearFloatProperty("18", -10.0, 10.0, decimals=1, units='dB')
    low_mid_band_threshold_bypass = BoolProperty("19")
    mid_band_threshold = LinearFloatProperty("20", -10.0, 10.0, decimals=1, units='dB')
    mid_band_gain = LinearFloatProperty("21", -10.0, 10.0, decimals=1, units='dB')
    mid_band_threshold_bypass = BoolProperty("22")
    high_mid_band_threshold = LinearFloatProperty("23", -10.0, 10.0, decimals=1, units='dB')
    high_mid_band_gain = LinearFloatProperty("24", -10.0, 10.0, decimals=1, units='dB')
    high_mid_band_threshold_bypass = BoolProperty("25")
    high_band_threshold = LinearFloatProperty("26", -10.0, 10.0, decimals=1, units='dB')
    high_band_gain = LinearFloatProperty("27", -10.0, 10.0, decimals=1, units='dB')
    high_band_threshold_bypass = BoolProperty("28")
    meters = EnumIntProperty("29", MetersOptions)

