# This file is auto-generated with generate_fx_nodes.py. Do not edit manually.

import enum
from enum import IntEnum

from ...nodes_base import MixerNode
from ...properties.primitive import BoolProperty, EnumIntProperty, InvertedBoolProperty, LinearFloatProperty, LogFloatProperty

class FrontRearOptions(IntEnum):
    FRONT = 0
    REAR = 1

class VintageReverbFxParams(MixerNode):
    description = 'Vintage Reverb effect parameters (Reverb category).'

    pre_delay = LinearFloatProperty("01", 0.0, 120.0, decimals=0, units='ms')
    decay = LinearFloatProperty("02", 0.4, 4.5, decimals=2, units='s')
    modulation = LinearFloatProperty("03", 0.0, 100.0, decimals=0, units='%')
    vintage = BoolProperty("04")
    front_rear = EnumIntProperty("05", FrontRearOptions)
    level = LinearFloatProperty("06", -12.0, 12.0, decimals=1, units='dB')
    low_cut = LogFloatProperty("07", 10.0, 500.0, decimals=0, units='Hz')
    high_cut = LogFloatProperty("08", 10000.0, 20000.0, decimals=0, units='Hz')
    low_multiplier = LogFloatProperty("09", 0.5, 2.0, decimals=2)
    high_multiplier = LogFloatProperty("10", 0.25, 1.0, decimals=2)

