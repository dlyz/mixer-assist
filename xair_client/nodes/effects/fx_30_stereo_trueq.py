# This file is auto-generated with generate_fx_nodes.py. Do not edit manually.

import enum
from enum import IntEnum

from ...nodes_base import MixerNode
from ...properties.primitive import BoolProperty, EnumIntProperty, InvertedBoolProperty, LinearFloatProperty, LogFloatProperty

class StereoTrueqFxParams(MixerNode):
    description = 'Stereo TruEQ effect parameters (Equalizer category).'

    f_20 = LinearFloatProperty("01", -15.0, 15.0, decimals=1, units='dB')
    f_25 = LinearFloatProperty("02", -15.0, 15.0, decimals=1, units='dB')
    f_31_5 = LinearFloatProperty("03", -15.0, 15.0, decimals=1, units='dB')
    f_40 = LinearFloatProperty("04", -15.0, 15.0, decimals=1, units='dB')
    f_50 = LinearFloatProperty("05", -15.0, 15.0, decimals=1, units='dB')
    f_63 = LinearFloatProperty("06", -15.0, 15.0, decimals=1, units='dB')
    f_80 = LinearFloatProperty("07", -15.0, 15.0, decimals=1, units='dB')
    f_100 = LinearFloatProperty("08", -15.0, 15.0, decimals=1, units='dB')
    f_125 = LinearFloatProperty("09", -15.0, 15.0, decimals=1, units='dB')
    f_160 = LinearFloatProperty("10", -15.0, 15.0, decimals=1, units='dB')
    f_200 = LinearFloatProperty("11", -15.0, 15.0, decimals=1, units='dB')
    f_250 = LinearFloatProperty("12", -15.0, 15.0, decimals=1, units='dB')
    f_315 = LinearFloatProperty("13", -15.0, 15.0, decimals=1, units='dB')
    f_400 = LinearFloatProperty("14", -15.0, 15.0, decimals=1, units='dB')
    f_500 = LinearFloatProperty("15", -15.0, 15.0, decimals=1, units='dB')
    f_630 = LinearFloatProperty("16", -15.0, 15.0, decimals=1, units='dB')
    f_800 = LinearFloatProperty("17", -15.0, 15.0, decimals=1, units='dB')
    f_1k = LinearFloatProperty("18", -15.0, 15.0, decimals=1, units='dB')
    f_1k25 = LinearFloatProperty("19", -15.0, 15.0, decimals=1, units='dB')
    f_1k6 = LinearFloatProperty("20", -15.0, 15.0, decimals=1, units='dB')
    f_2k = LinearFloatProperty("21", -15.0, 15.0, decimals=1, units='dB')
    f_2k5 = LinearFloatProperty("22", -15.0, 15.0, decimals=1, units='dB')
    f_3k15 = LinearFloatProperty("23", -15.0, 15.0, decimals=1, units='dB')
    f_4k = LinearFloatProperty("24", -15.0, 15.0, decimals=1, units='dB')
    f_5k = LinearFloatProperty("25", -15.0, 15.0, decimals=1, units='dB')
    f_6k3 = LinearFloatProperty("26", -15.0, 15.0, decimals=1, units='dB')
    f_8k = LinearFloatProperty("27", -15.0, 15.0, decimals=1, units='dB')
    f_10k = LinearFloatProperty("28", -15.0, 15.0, decimals=1, units='dB')
    f_12k5 = LinearFloatProperty("29", -15.0, 15.0, decimals=1, units='dB')
    f_16k = LinearFloatProperty("30", -15.0, 15.0, decimals=1, units='dB')
    f_20k = LinearFloatProperty("31", -15.0, 15.0, decimals=1, units='dB')
    master = LinearFloatProperty("32", -15.0, 15.0, decimals=1, units='dB')

