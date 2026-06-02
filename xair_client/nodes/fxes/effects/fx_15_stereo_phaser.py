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

class StereoPhaserFxParams(MixerNode):
    description = 'Stereo Phaser effect parameters (Modulation category).'

    speed = LogFloatProperty("01", 0.05, 5.0, decimals=2, grid_size=101, units='Hz')
    depth = LinearFloatProperty("02", 0.0, 100.0, decimals=0, grid_size=51, units='%')
    resonance = LinearFloatProperty("03", 0.0, 80.0, decimals=0, grid_size=41, units='%')
    base = LinearFloatProperty("04", 0.0, 50.0, decimals=0, grid_size=26)
    stages = LinearFloatProperty("05", 2.0, 12.0, decimals=0, grid_size=11)
    mix = LinearFloatProperty("06", 0.0, 100.0, decimals=0, grid_size=51, units='%')
    wave = LinearFloatProperty("07", -50.0, 50.0, decimals=0, grid_size=21)
    phase = LinearFloatProperty("08", 0.0, 180.0, decimals=0, grid_size=37, units='°')
    env_mod = LinearFloatProperty("09", -100.0, 100.0, decimals=0, grid_size=41, units='%')
    attack = LogFloatProperty("10", 10.0, 1000.0, decimals=0, grid_size=51, units='ms')
    hold = LogFloatProperty("11", 1.0, 2000.0, decimals=0, grid_size=51, units='ms')
    release = LogFloatProperty("12", 10.0, 1000.0, decimals=0, grid_size=51, units='ms')

