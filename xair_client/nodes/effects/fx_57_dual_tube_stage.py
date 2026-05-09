# This file is auto-generated with generate_fx_nodes.py. Do not edit manually.

import enum
from enum import IntEnum

from ...nodes_base import MixerNode
from ...properties.primitive import BoolProperty, EnumIntProperty, InvertedBoolProperty, LinearFloatProperty, LogFloatProperty

class DualTubeStageFxParams(MixerNode):
    description = 'Dual Tube Stage effect parameters (Amp simulation category).'

    a_drive = LinearFloatProperty("01", 0.0, 100.0, decimals=0, units='%')
    a_even = LinearFloatProperty("02", 0.0, 50.0, decimals=0, units='%')
    a_odd = LinearFloatProperty("03", 0.0, 50.0, decimals=0, units='%')
    a_gain = LinearFloatProperty("04", -12.0, 12.0, decimals=1, units='dB')
    a_low_cut = LogFloatProperty("05", 20.0, 200.0, decimals=0, units='Hz')
    a_high_cut = LogFloatProperty("06", 4000.0, 20000.0, decimals=0, units='Hz')
    a_bass_gain = LinearFloatProperty("07", -12.0, 12.0, decimals=1, units='dB')
    a_bass_frequency = LogFloatProperty("08", 50.0, 400.0, decimals=0, units='Hz')
    a_treble_gain = LinearFloatProperty("09", -12.0, 12.0, decimals=1, units='dB')
    a_treble_frequency = LogFloatProperty("10", 1000.0, 10000.0, decimals=0, units='Hz')
    b_drive = LinearFloatProperty("11", 0.0, 100.0, decimals=0, units='%')
    b_even = LinearFloatProperty("12", 0.0, 50.0, decimals=0, units='%')
    b_odd = LinearFloatProperty("13", 0.0, 50.0, decimals=0, units='%')
    b_gain = LinearFloatProperty("14", -12.0, 12.0, decimals=1, units='dB')
    b_low_cut = LogFloatProperty("15", 20.0, 200.0, decimals=0, units='Hz')
    b_high_cut = LogFloatProperty("16", 4000.0, 20000.0, decimals=0, units='Hz')
    b_bass_gain = LinearFloatProperty("17", -12.0, 12.0, decimals=1, units='dB')
    b_bass_frequency = LogFloatProperty("18", 50.0, 400.0, decimals=0, units='Hz')
    b_treble_gain = LinearFloatProperty("19", -12.0, 12.0, decimals=1, units='dB')
    b_treble_frequency = LogFloatProperty("20", 1000.0, 10000.0, decimals=0, units='Hz')

