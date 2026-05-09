# This file is auto-generated with generate_fx_nodes.py. Do not edit manually.

import enum
from enum import IntEnum

from ...nodes_base import MixerNode
from ...properties.primitive import BoolProperty, EnumIntProperty, InvertedBoolProperty, LinearFloatProperty, LogFloatProperty

class TremoloPannerFxParams(MixerNode):
    description = 'Tremolo / Panner effect parameters (Modulation category).'

    speed = LogFloatProperty("01", 0.05, 5.0, decimals=2, units='Hz')
    phase = LinearFloatProperty("02", 0.0, 180.0, decimals=0, units='°')
    wave = LinearFloatProperty("03", -50.0, 50.0, decimals=0)
    depth = LinearFloatProperty("04", 0.0, 100.0, decimals=0, units='%')
    env_speed = LinearFloatProperty("05", 0.0, 100.0, decimals=0, units='%')
    env_depth = LinearFloatProperty("06", 0.0, 100.0, decimals=0, units='%')
    attack = LogFloatProperty("07", 10.0, 1000.0, decimals=0, units='ms')
    hold = LogFloatProperty("08", 1.0, 2000.0, decimals=0, units='ms')
    release = LogFloatProperty("09", 10.0, 1000.0, decimals=0, units='ms')

