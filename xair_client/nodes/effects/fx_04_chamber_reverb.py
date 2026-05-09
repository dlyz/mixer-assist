# This file is auto-generated with generate_fx_nodes.py. Do not edit manually.

import enum
from enum import IntEnum

from ...nodes_base import MixerNode
from ...properties.primitive import BoolProperty, EnumIntProperty, InvertedBoolProperty, LinearFloatProperty, LogFloatProperty

class ChamberReverbFxParams(MixerNode):
    description = 'Chamber Reverb effect parameters (Reverb category).'

    pre_delay = LinearFloatProperty("01", 0.0, 200.0, decimals=0, units='ms')
    decay = LogFloatProperty("02", 0.3, 29.0, decimals=2, units='s')
    size = LinearFloatProperty("03", 4.0, 76.0, decimals=0, units='m')
    damp = LogFloatProperty("04", 1000.0, 20000.0, decimals=0, units='Hz')
    diffusion = LinearFloatProperty("05", 0.0, 100.0, decimals=0, units='%')
    level = LinearFloatProperty("06", -12.0, 12.0, decimals=1, units='dB')
    low_cut = LogFloatProperty("07", 10.0, 500.0, decimals=0, units='Hz')
    high_cut = LogFloatProperty("08", 200.0, 20000.0, decimals=0, units='Hz')
    bass_multiplier = LogFloatProperty("09", 0.25, 4.0, decimals=2)
    spread = LinearFloatProperty("10", 0.0, 50.0, decimals=0)
    shape = LinearFloatProperty("11", 0.0, 250.0, decimals=0)
    spin = LinearFloatProperty("12", 0.0, 100.0, decimals=0, units='%')
    reflection_left_delay = LinearFloatProperty("13", 0.0, 500.0, decimals=0, units='ms')
    reflection_right_delay = LinearFloatProperty("14", 0.0, 500.0, decimals=0, units='ms')
    reflection_left_gain = LinearFloatProperty("15", 0.0, 100.0, decimals=0, units='%')
    reflection_right_gain = LinearFloatProperty("16", 0.0, 100.0, decimals=0, units='%')

