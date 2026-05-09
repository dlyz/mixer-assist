# This file is auto-generated with generate_fx_nodes.py. Do not edit manually.

import enum
from enum import IntEnum

from ...nodes_base import MixerNode
from ...properties.primitive import BoolProperty, EnumIntProperty, InvertedBoolProperty, LinearFloatProperty, LogFloatProperty

class VintageRoomFxParams(MixerNode):
    description = 'Vintage Room effect parameters (Reverb category).'

    rev_delay = LinearFloatProperty("01", 0.0, 200.0, decimals=0, units='ms')
    decay = LogFloatProperty("02", 0.1, 20.0, decimals=2, units='ms')
    size = LinearFloatProperty("03", 2.0, 100.0, decimals=0)
    density = LinearFloatProperty("04", 1.0, 30.0, decimals=0)
    error_level = LinearFloatProperty("05", 0.0, 100.0, decimals=0, units='%')
    level = LinearFloatProperty("06", -12.0, 12.0, decimals=1, units='dB')
    low = LogFloatProperty("07", 0.1, 10.0, decimals=2)
    high = LogFloatProperty("08", 0.1, 10.0, decimals=2)
    low_cut = LogFloatProperty("09", 10.0, 500.0, decimals=0, units='Hz')
    high_cut = LogFloatProperty("10", 200.0, 20000.0, decimals=0, units='Hz')
    er_left_delay = LinearFloatProperty("11", 0.0, 200.0, decimals=0, units='ms')
    er_right_delay = LinearFloatProperty("12", 0.0, 200.0, decimals=0, units='ms')

