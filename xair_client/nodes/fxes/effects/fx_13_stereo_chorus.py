# This file is auto-generated with generate_fx_nodes.py. Do not edit manually.

import enum
from enum import IntEnum

from ...core.base_types import MixerNode
from ...core.primitive_props import (
    BoolProperty,
    EnumIntProperty,
    InvertedBoolProperty,
    LinearFloatProperty,
    LogFloatProperty,
)

class StereoChorusFxParams(MixerNode):
    description = 'Stereo Chorus effect parameters (Modulation category).'

    speed = LogFloatProperty("01", 0.05, 5.0, decimals=2, grid_size=101, units='Hz')
    width_l = LinearFloatProperty("02", 0.0, 100.0, decimals=0, grid_size=21, units='%')
    width_r = LinearFloatProperty("03", 0.0, 100.0, decimals=0, grid_size=21, units='%')
    delay_l = LogFloatProperty("04", 0.5, 50.0, decimals=1, grid_size=51, units='ms')
    delay_r = LogFloatProperty("05", 0.5, 50.0, decimals=1, grid_size=51, units='ms')
    mix = LinearFloatProperty("06", 0.0, 100.0, decimals=0, grid_size=51, units='%')
    low_cut = LogFloatProperty("07", 10.0, 500.0, decimals=0, grid_size=51, units='Hz')
    high_cut = LogFloatProperty("08", 200.0, 20000.0, decimals=0, grid_size=51, units='Hz')
    phase = LinearFloatProperty("09", 0.0, 180.0, decimals=0, grid_size=37, units='°')
    wave = LinearFloatProperty("10", 0.0, 100.0, decimals=0, grid_size=21, units='%')
    spread = LinearFloatProperty("11", 0.0, 100.0, decimals=0, grid_size=21, units='%')

