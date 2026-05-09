# This file is auto-generated with generate_fx_nodes.py. Do not edit manually.

import enum
from enum import IntEnum

from ...nodes_base import MixerNode
from ...properties.primitive import BoolProperty, EnumIntProperty, InvertedBoolProperty, LinearFloatProperty, LogFloatProperty

class SlowFastOptions(IntEnum):
    SLOW = 0
    FAST = 1

class RotarySpeakerFxParams(MixerNode):
    description = 'Rotary Speaker effect parameters (Modulation category).'

    low_speed = LogFloatProperty("01", 0.1, 4.0, decimals=2, units='Hz')
    high_speed = LogFloatProperty("02", 2.0, 10.0, decimals=2, units='Hz')
    acceleration = LinearFloatProperty("03", 0.0, 100.0, decimals=0, units='%')
    distance = LinearFloatProperty("04", 0.0, 100.0, decimals=0, units='%')
    balance = LinearFloatProperty("05", -100.0, 100.0, decimals=0, units='%')
    mix = LinearFloatProperty("06", 0.0, 100.0, decimals=0, units='%')
    stop = BoolProperty("07")
    slow_fast = EnumIntProperty("08", SlowFastOptions)

