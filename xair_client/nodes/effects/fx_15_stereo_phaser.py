# This file is auto-generated with generate_fx_nodes.py. Do not edit manually.

import enum
from enum import IntEnum

from ...nodes_base import MixerNode
from ...properties.primitive import BoolProperty, EnumIntProperty, InvertedBoolProperty, LinearFloatProperty, LogFloatProperty

class StereoPhaserFxParams(MixerNode):
    description = 'Stereo Phaser effect parameters (Modulation category).'

    speed = LogFloatProperty("01", 0.05, 5.0, decimals=2, units='Hz')
    depth = LinearFloatProperty("02", 0.0, 100.0, decimals=0, units='%')
    resonance = LinearFloatProperty("03", 0.0, 80.0, decimals=0, units='%')
    base = LinearFloatProperty("04", 0.0, 50.0, decimals=0)
    stages = LinearFloatProperty("05", 2.0, 12.0, decimals=0)
    mix = LinearFloatProperty("06", 0.0, 100.0, decimals=0, units='%')
    wave = LinearFloatProperty("07", -50.0, 50.0, decimals=0)
    phase = LinearFloatProperty("08", 0.0, 180.0, decimals=0, units='°')
    env_mod = LinearFloatProperty("09", -100.0, 100.0, decimals=0, units='%')
    attack = LogFloatProperty("10", 10.0, 1000.0, decimals=0, units='ms')
    hold = LogFloatProperty("11", 1.0, 2000.0, decimals=0, units='ms')
    release = LogFloatProperty("12", 10.0, 1000.0, decimals=0, units='ms')

