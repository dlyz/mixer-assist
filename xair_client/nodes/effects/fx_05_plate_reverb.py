# This file is auto-generated with generate_fx_nodes.py. Do not edit manually.

import enum
from enum import IntEnum

from ...nodes_base import MixerNode
from ...properties.primitive import BoolProperty, EnumIntProperty, InvertedBoolProperty, LinearFloatProperty, LogFloatProperty

class PlateReverbFxParams(MixerNode):
    description = 'Plate Reverb effect parameters (Reverb category).'

    pre_delay = LinearFloatProperty("01", 0.0, 200.0, decimals=0, units='ms')
    decay = LogFloatProperty("02", 0.5, 10.0, decimals=2, units='ms')
    size = LinearFloatProperty("03", 2.0, 100.0, decimals=0)
    damp = LogFloatProperty("04", 1000.0, 20000.0, decimals=0, units='Hz')
    diffuse = LinearFloatProperty("05", 1.0, 30.0, decimals=0)
    level = LinearFloatProperty("06", -12.0, 12.0, decimals=1, units='dB')
    low_cut = LogFloatProperty("07", 10.0, 500.0, decimals=0, units='Hz')
    high_cut = LogFloatProperty("08", 200.0, 20000.0, decimals=0, units='Hz')
    bass_multiplier = LogFloatProperty("09", 0.5, 2.0, decimals=2)
    x_over = LogFloatProperty("10", 10.0, 500.0, decimals=0, units='Hz')
    modulation_depth = LinearFloatProperty("11", 1.0, 50.0, decimals=0)
    modulation_speed = LinearFloatProperty("12", 0.0, 100.0, decimals=0)

