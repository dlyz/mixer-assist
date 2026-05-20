# This file is auto-generated with generate_fx_nodes.py. Do not edit manually.

import enum
from enum import IntEnum

from ...nodes_base import MixerNode
from ...properties.primitive import BoolProperty, EnumIntProperty, InvertedBoolProperty, LinearFloatProperty, LogFloatProperty

class AmbienceFxParams(MixerNode):
    description = 'Ambience effect parameters (Reverb category).'

    pre_delay = LinearFloatProperty("01", 0.0, 200.0, decimals=0, grid_size=101, units='ms')
    decay = LogFloatProperty("02", 0.2, 7.3, decimals=2, grid_size=51, units='s')
    size = LinearFloatProperty("03", 2.0, 100.0, decimals=0, grid_size=50)
    damping = LogFloatProperty("04", 1000.0, 20000.0, decimals=0, grid_size=25, units='Hz')
    diffuse = LinearFloatProperty("05", 1.0, 30.0, decimals=0, grid_size=30)
    level = LinearFloatProperty("06", -12.0, 12.0, decimals=1, grid_size=49, units='dB')
    low_cut = LogFloatProperty("07", 10.0, 500.0, decimals=0, grid_size=51, units='Hz')
    high_cut = LogFloatProperty("08", 200.0, 20000.0, decimals=0, grid_size=51, units='Hz')
    mod = LinearFloatProperty("09", 0.0, 100.0, decimals=0, grid_size=51, units='%')
    tail_gain = LinearFloatProperty("10", 0.0, 100.0, decimals=0, grid_size=51, units='%')

