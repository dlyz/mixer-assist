# This file is auto-generated with generate_fx_nodes.py. Do not edit manually.

import enum
from enum import IntEnum

from ...nodes_base import MixerNode
from ...properties.primitive import BoolProperty, EnumIntProperty, InvertedBoolProperty, LinearFloatProperty, LogFloatProperty

class DimensionalChorusFxParams(MixerNode):
    description = 'Dimensional Chorus effect parameters (Modulation category).'

    power = BoolProperty("01")
    stereo = BoolProperty("02")
    dry = BoolProperty("03")
    mode_1 = BoolProperty("04")
    mode_2 = BoolProperty("05")
    mode_3 = BoolProperty("06")
    mode_4 = BoolProperty("07")

