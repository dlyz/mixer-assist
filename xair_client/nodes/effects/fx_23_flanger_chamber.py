# This file is auto-generated with generate_fx_nodes.py. Do not edit manually.

import enum
from enum import IntEnum

from ...nodes_base import MixerNode
from ...properties.primitive import BoolProperty, EnumIntProperty, InvertedBoolProperty, LinearFloatProperty, LogFloatProperty

class FlangerChamberFxParams(MixerNode):
    description = 'Flanger + Chamber effect parameters (Reverb category).'

    flanger_speed = LogFloatProperty("01", 0.05, 4.0, decimals=2, units='Hz')
    flanger_depth = LinearFloatProperty("02", 0.0, 100.0, decimals=0, units='%')
    flanger_delay = LogFloatProperty("03", 0.5, 20.0, decimals=1, units='ms')
    flanger_phase = LinearFloatProperty("04", 0.0, 180.0, decimals=0, units='°')
    flanger_feed = LinearFloatProperty("05", -90.0, 90.0, decimals=0, units='%')
    balance = LinearFloatProperty("06", -100.0, 100.0, decimals=0, units='%')
    chamber_pre_delay = LinearFloatProperty("07", 0.0, 200.0, decimals=0, units='ms')
    chamber_decay = LogFloatProperty("08", 0.1, 5.0, decimals=2, units='s')
    chamber_size = LinearFloatProperty("09", 2.0, 100.0, decimals=0)
    chamber_damp = LogFloatProperty("10", 1000.0, 20000.0, decimals=0, units='Hz')
    low_cut = LogFloatProperty("11", 10.0, 500.0, decimals=0, units='Hz')
    mix = LinearFloatProperty("12", 0.0, 100.0, decimals=0, units='%')

