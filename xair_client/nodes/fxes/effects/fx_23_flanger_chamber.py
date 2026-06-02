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

class FlangerChamberFxParams(MixerNode):
    description = 'Flanger + Chamber effect parameters (Reverb category).'

    flanger_speed = LogFloatProperty("01", 0.05, 4.0, decimals=2, grid_size=101, units='Hz')
    flanger_depth = LinearFloatProperty("02", 0.0, 100.0, decimals=0, grid_size=21, units='%')
    flanger_delay = LogFloatProperty("03", 0.5, 20.0, decimals=1, grid_size=51, units='ms')
    flanger_phase = LinearFloatProperty("04", 0.0, 180.0, decimals=0, grid_size=37, units='°')
    flanger_feed = LinearFloatProperty("05", -90.0, 90.0, decimals=0, grid_size=37, units='%')
    balance = LinearFloatProperty("06", -100.0, 100.0, decimals=0, grid_size=41, units='%')
    chamber_pre_delay = LinearFloatProperty("07", 0.0, 200.0, decimals=0, grid_size=101, units='ms')
    chamber_decay = LogFloatProperty("08", 0.1, 5.0, decimals=2, grid_size=51, units='s')
    chamber_size = LinearFloatProperty("09", 2.0, 100.0, decimals=0, grid_size=50)
    chamber_damp = LogFloatProperty("10", 1000.0, 20000.0, decimals=0, grid_size=51, units='Hz')
    low_cut = LogFloatProperty("11", 10.0, 500.0, decimals=0, grid_size=51, units='Hz')
    mix = LinearFloatProperty("12", 0.0, 100.0, decimals=0, grid_size=51, units='%')

