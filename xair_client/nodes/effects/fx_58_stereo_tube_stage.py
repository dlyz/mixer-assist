# This file is auto-generated with generate_fx_nodes.py. Do not edit manually.

import enum
from enum import IntEnum

from ...nodes_base import MixerNode
from ...properties.primitive import BoolProperty, EnumIntProperty, InvertedBoolProperty, LinearFloatProperty, LogFloatProperty

class StereoTubeStageFxParams(MixerNode):
    description = 'Stereo Tube Stage effect parameters (Amp simulation category).'

    drive = LinearFloatProperty("01", 0.0, 100.0, decimals=0, units='%')
    even = LinearFloatProperty("02", 0.0, 50.0, decimals=0, units='%')
    odd = LinearFloatProperty("03", 0.0, 50.0, decimals=0, units='%')
    gain = LinearFloatProperty("04", -12.0, 12.0, decimals=1, units='dB')
    low_cut = LogFloatProperty("05", 20.0, 200.0, decimals=0, units='Hz')
    high_cut = LogFloatProperty("06", 4000.0, 20000.0, decimals=0, units='Hz')
    bass_gain = LinearFloatProperty("07", -12.0, 12.0, decimals=1, units='dB')
    bass_frequency = LogFloatProperty("08", 50.0, 400.0, decimals=0, units='Hz')
    treble_gain = LinearFloatProperty("09", -12.0, 12.0, decimals=1, units='dB')
    treble_frequency = LogFloatProperty("10", 1000.0, 10000.0, decimals=0, units='Hz')

