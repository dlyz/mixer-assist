# This file is auto-generated with generate_fx_nodes.py. Do not edit manually.

import enum
from enum import IntEnum

from ...nodes_base import MixerNode
from ...properties.primitive import BoolProperty, EnumIntProperty, InvertedBoolProperty, LinearFloatProperty, LogFloatProperty

class EdisonEx1FxParams(MixerNode):
    description = 'Edison EX1 effect parameters (Other category).'

    on = BoolProperty("01")
    m_s_input = BoolProperty("02")
    m_s_output = BoolProperty("03")
    stereo_spread = LinearFloatProperty("04", -50.0, 50.0, decimals=0)
    lmf_spread = LinearFloatProperty("05", -50.0, 50.0, decimals=0)
    balance = LinearFloatProperty("06", -50.0, 50.0, decimals=0)
    center_distance = LinearFloatProperty("07", -50.0, 50.0, decimals=0)
    output_gain = LinearFloatProperty("08", -12.0, 12.0, decimals=1, units='dB')

