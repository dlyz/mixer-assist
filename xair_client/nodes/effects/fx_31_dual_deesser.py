# This file is auto-generated with generate_fx_nodes.py. Do not edit manually.

import enum
from enum import IntEnum

from ...nodes_base import MixerNode
from ...properties.primitive import BoolProperty, EnumIntProperty, InvertedBoolProperty, LinearFloatProperty, LogFloatProperty

class DualDeesserFxParams(MixerNode):
    description = 'Dual DeEsser effect parameters (De esser category).'

    a_low_band_reduction = LinearFloatProperty("01", 0.0, 50.0, decimals=0)
    a_high_band_reduction = LinearFloatProperty("02", 0.0, 50.0, decimals=0)
    a_male = BoolProperty("05")
    b_low_band_reduction = LinearFloatProperty("03", 0.0, 50.0, decimals=0)
    b_high_band_reduction = LinearFloatProperty("04", 0.0, 50.0, decimals=0)
    b_male = BoolProperty("06")

