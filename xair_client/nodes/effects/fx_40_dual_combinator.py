# This file is auto-generated with generate_fx_nodes.py. Do not edit manually.

import enum
from enum import IntEnum

from ...nodes_base import MixerNode
from ...properties.primitive import BoolProperty, EnumIntProperty, InvertedBoolProperty, LinearFloatProperty, LogFloatProperty

class ABandOptions(IntEnum):
    ALL = 0
    LOW = 1
    LOW_MID = 2
    MID = 3
    HIGH_MID = 4
    HIGH = 5

class AGlobalRatioOptions(IntEnum):
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

class AMetersOptions(IntEnum):
    BAND_GAIN_REDUCTION = 0
    BAND_LEVEL_METERS_PEAK = 1
    AUTOMATIC_SPECTRUM_BALANCE = 2

class BBandOptions(IntEnum):
    ALL = 0
    LOW = 1
    LOW_MID = 2
    MID = 3
    HIGH_MID = 4
    HIGH = 5

class BGlobalRatioOptions(IntEnum):
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

class BMetersOptions(IntEnum):
    BAND_GAIN_REDUCTION = 0
    BAND_LEVEL_METERS_PEAK = 1
    AUTOMATIC_SPECTRUM_BALANCE = 2

class DualCombinatorFxParams(MixerNode):
    description = 'Dual Combinator effect parameters (Other category).'

    a_bypass = InvertedBoolProperty("01")
    a_band = EnumIntProperty("02", ABandOptions)
    a_mix = LinearFloatProperty("03", 0.0, 100.0, decimals=0, units='%')
    a_attack = LinearFloatProperty("04", 0.0, 19.0, decimals=0)
    a_release = LogFloatProperty("05", 20.0, 3000.0, decimals=0, units='ms')
    a_auto_release = BoolProperty("06")
    a_speed_sbc = LinearFloatProperty("07", 1.0, 10.0, decimals=0)
    a_sbc = BoolProperty("08")
    a_x_over = LinearFloatProperty("09", -50.0, 50.0, decimals=0)
    a_48_db = BoolProperty("10")
    a_global_ratio = EnumIntProperty("11", AGlobalRatioOptions)
    a_trim_threshold = LinearFloatProperty("12", -40.0, 0.0, decimals=1, units='dB')
    a_trim_gain = LinearFloatProperty("13", -10.0, 10.0, decimals=1, units='dB')
    a_low_band_threshold = LinearFloatProperty("14", -10.0, 10.0, decimals=1, units='dB')
    a_low_band_gain = LinearFloatProperty("15", -10.0, 10.0, decimals=1, units='dB')
    a_low_band_threshold_bypass = BoolProperty("16")
    a_low_mid_band_threshold = LinearFloatProperty("17", -10.0, 10.0, decimals=1, units='dB')
    a_low_mid_band_gain = LinearFloatProperty("18", -10.0, 10.0, decimals=1, units='dB')
    a_low_mid_band_threshold_bypass = BoolProperty("19")
    a_mid_band_threshold = LinearFloatProperty("20", -10.0, 10.0, decimals=1, units='dB')
    a_mid_band_gain = LinearFloatProperty("21", -10.0, 10.0, decimals=1, units='dB')
    a_mid_band_threshold_bypass = BoolProperty("22")
    a_high_mid_band_threshold = LinearFloatProperty("23", -10.0, 10.0, decimals=1, units='dB')
    a_high_mid_band_gain = LinearFloatProperty("24", -10.0, 10.0, decimals=1, units='dB')
    a_high_mid_band_threshold_bypass = BoolProperty("25")
    a_high_band_threshold = LinearFloatProperty("26", -10.0, 10.0, decimals=1, units='dB')
    a_high_band_gain = LinearFloatProperty("27", -10.0, 10.0, decimals=1, units='dB')
    a_high_band_threshold_bypass = BoolProperty("28")
    a_meters = EnumIntProperty("29", AMetersOptions)
    b_bypass = InvertedBoolProperty("30")
    b_band = EnumIntProperty("31", BBandOptions)
    b_mix = LinearFloatProperty("32", 0.0, 100.0, decimals=0, units='%')
    b_attack = LinearFloatProperty("33", 0.0, 19.0, decimals=0)
    b_release = LogFloatProperty("34", 20.0, 3000.0, decimals=0, units='ms')
    b_auto_release = BoolProperty("35")
    b_speed_sbc = LinearFloatProperty("36", 1.0, 10.0, decimals=0)
    b_sbc = BoolProperty("37")
    b_x_over = LinearFloatProperty("38", -50.0, 50.0, decimals=0)
    b_48_db = BoolProperty("39")
    b_global_ratio = EnumIntProperty("40", BGlobalRatioOptions)
    b_trim_threshold = LinearFloatProperty("41", -40.0, 0.0, decimals=1, units='dB')
    b_trim_gain = LinearFloatProperty("42", -10.0, 10.0, decimals=1, units='dB')
    b_low_band_threshold = LinearFloatProperty("43", -10.0, 10.0, decimals=1, units='dB')
    b_low_band_gain = LinearFloatProperty("44", -10.0, 10.0, decimals=1, units='dB')
    b_low_band_threshold_bypass = BoolProperty("45")
    b_low_mid_band_threshold = LinearFloatProperty("46", -10.0, 10.0, decimals=1, units='dB')
    b_low_mid_band_gain = LinearFloatProperty("47", -10.0, 10.0, decimals=1, units='dB')
    b_low_mid_band_threshold_bypass = BoolProperty("48")
    b_mid_band_threshold = LinearFloatProperty("49", -10.0, 10.0, decimals=1, units='dB')
    b_mid_band_gain = LinearFloatProperty("50", -10.0, 10.0, decimals=1, units='dB')
    b_mid_band_threshold_bypass = BoolProperty("51")
    b_high_mid_band_threshold = LinearFloatProperty("52", -10.0, 10.0, decimals=1, units='dB')
    b_high_mid_band_gain = LinearFloatProperty("53", -10.0, 10.0, decimals=1, units='dB')
    b_high_mid_band_threshold_bypass = BoolProperty("54")
    b_high_band_threshold = LinearFloatProperty("55", -10.0, 10.0, decimals=1, units='dB')
    b_high_band_gain = LinearFloatProperty("56", -10.0, 10.0, decimals=1, units='dB')
    b_high_band_threshold_bypass = BoolProperty("57")
    b_meters = EnumIntProperty("58", BMetersOptions)

