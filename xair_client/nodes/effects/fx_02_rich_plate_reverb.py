# This file is auto-generated with generate_fx_nodes.py. Do not edit manually.

import enum
from enum import IntEnum

from ...nodes_base import MixerNode
from ...properties.primitive import BoolProperty, EnumIntProperty, InvertedBoolProperty, LinearFloatProperty, LogFloatProperty

class RichPlateReverbFxParams(MixerNode):
    description = 'Rich Plate Reverb effect parameters (Reverb category).'

    pre_delay = LinearFloatProperty("01", 0.0, 200.0, decimals=0, units='ms')
    decay = LogFloatProperty("02", 0.3, 29.0, decimals=2, units='s')
    size = LinearFloatProperty("03", 4.0, 39.0, decimals=0, units='m')
    damp = LogFloatProperty("04", 1000.0, 20000.0, decimals=0, units='Hz')
    diffusion = LinearFloatProperty("05", 0.0, 100.0, decimals=0, units='%')
    level = LinearFloatProperty("06", -12.0, 12.0, decimals=1, units='dB')
    low_cut = LogFloatProperty("07", 10.0, 500.0, decimals=0, units='Hz')
    high_cut = LogFloatProperty("08", 200.0, 20000.0, decimals=0, units='Hz')
    bass_multiplier = LogFloatProperty("09", 0.25, 4.0, decimals=2)
    spread = LinearFloatProperty("10", 0.0, 50.0, decimals=0)
    attack = LinearFloatProperty("11", 0.0, 100.0, decimals=0)
    spin = LinearFloatProperty("12", 0.0, 100.0, decimals=0, units='%')
    echo_left_delay = LinearFloatProperty("13", 0.0, 1200.0, decimals=0, units='ms')
    echo_right_delay = LinearFloatProperty("14", 0.0, 1200.0, decimals=0, units='ms')
    echo_left_feedback = LinearFloatProperty("15", -100.0, 100.0, decimals=0, units='%')
    echo_right_feedback = LinearFloatProperty("16", -100.0, 100.0, decimals=0, units='%')

