# This file is auto-generated with generate_fx_nodes.py. Do not edit manually.

import enum
from enum import IntEnum

from ...nodes_base import MixerNode
from ...properties.primitive import BoolProperty, EnumIntProperty, InvertedBoolProperty, LinearFloatProperty, LogFloatProperty

class GatedReverbFxParams(MixerNode):
    description = 'Gated Reverb effect parameters (Reverb category).'

    pre_delay = LinearFloatProperty("01", 0.0, 200.0, decimals=0, grid_size=101, units='ms')
    decay = LinearFloatProperty("02", 140.0, 1000.0, decimals=0, grid_size=51, units='ms')
    attack = LinearFloatProperty("03", 0.0, 30.0, decimals=0, grid_size=31)
    density = LinearFloatProperty("04", 1.0, 50.0, decimals=0, grid_size=50)
    spread = LinearFloatProperty("05", 0.0, 100.0, decimals=0, grid_size=51)
    level = LinearFloatProperty("06", -12.0, 12.0, decimals=1, grid_size=49, units='dB')
    low_cut = LogFloatProperty("07", 10.0, 500.0, decimals=0, grid_size=51, units='Hz')
    high_shelf_frequency = LogFloatProperty("08", 200.0, 20000.0, decimals=0, grid_size=51, units='Hz')
    high_shelf_gain = LinearFloatProperty("09", -30.0, 0.0, decimals=1, grid_size=61, units='dB')
    diff = LinearFloatProperty("10", 1.0, 30.0, decimals=0, grid_size=30)

