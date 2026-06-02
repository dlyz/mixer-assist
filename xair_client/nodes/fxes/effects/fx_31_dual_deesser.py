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

class DualDeesserFxParams(MixerNode):
    description = 'Dual DeEsser effect parameters (De esser category).'

    a_low_band_reduction = LinearFloatProperty("01", 0.0, 50.0, decimals=0, grid_size=51)
    a_high_band_reduction = LinearFloatProperty("02", 0.0, 50.0, decimals=0, grid_size=51)
    a_male = BoolProperty("05")
    b_low_band_reduction = LinearFloatProperty("03", 0.0, 50.0, decimals=0, grid_size=51)
    b_high_band_reduction = LinearFloatProperty("04", 0.0, 50.0, decimals=0, grid_size=51)
    b_male = BoolProperty("06")

