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

class StereoDeesserFxParams(MixerNode):
    description = 'Stereo DeEsser effect parameters (De esser category).'

    mid_side_process = BoolProperty("06")
    mid_or_stereo_low_band_reduction = LinearFloatProperty("01", 0.0, 50.0, decimals=0, grid_size=51)
    mid_or_stereo_high_band_reduction = LinearFloatProperty("02", 0.0, 50.0, decimals=0, grid_size=51)
    side_low_band_reduction = LinearFloatProperty("03", 0.0, 50.0, decimals=0, grid_size=51)
    side_high_band_reduction = LinearFloatProperty("04", 0.0, 50.0, decimals=0, grid_size=51)
    male = BoolProperty("05")

