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

class EdisonEx1FxParams(MixerNode):
    description = 'Edison EX1 effect parameters (Other category).'

    on = BoolProperty("01")
    m_s_input = BoolProperty("02")
    m_s_output = BoolProperty("03")
    stereo_spread = LinearFloatProperty("04", -50.0, 50.0, decimals=0, grid_size=51)
    lmf_spread = LinearFloatProperty("05", -50.0, 50.0, decimals=0, grid_size=51)
    balance = LinearFloatProperty("06", -50.0, 50.0, decimals=0, grid_size=51)
    center_distance = LinearFloatProperty("07", -50.0, 50.0, decimals=0, grid_size=51)
    output_gain = LinearFloatProperty("08", -12.0, 12.0, decimals=1, grid_size=49, units='dB')

