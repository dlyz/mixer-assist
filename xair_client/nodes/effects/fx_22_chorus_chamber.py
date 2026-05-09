# This file is auto-generated with generate_fx_nodes.py. Do not edit manually.

import enum
from enum import IntEnum

from ...nodes_base import MixerNode
from ...properties.primitive import BoolProperty, EnumIntProperty, InvertedBoolProperty, LinearFloatProperty, LogFloatProperty

class ChorusChamberFxParams(MixerNode):
    description = 'Chorus + Chamber effect parameters (Reverb category).'

    chorus_speed = LogFloatProperty("01", 0.05, 4.0, decimals=2, units='Hz')
    chorus_depth = LinearFloatProperty("02", 0.0, 100.0, decimals=0, units='%')
    chorus_delay = LogFloatProperty("03", 0.5, 50.0, decimals=1, units='ms')
    chorus_phase = LinearFloatProperty("04", 0.0, 180.0, decimals=0, units='°')
    chorus_wave = LinearFloatProperty("05", 0.0, 100.0, decimals=0, units='%')
    balance = LinearFloatProperty("06", -100.0, 100.0, decimals=0, units='%')
    chamber_pre_delay = LinearFloatProperty("07", 0.0, 200.0, decimals=0, units='ms')
    chamber_decay = LogFloatProperty("08", 0.1, 5.0, decimals=2, units='s')
    chamber_size = LinearFloatProperty("09", 2.0, 100.0, decimals=0)
    chamber_damp = LogFloatProperty("10", 1000.0, 20000.0, decimals=0, units='Hz')
    low_cut = LogFloatProperty("11", 10.0, 500.0, decimals=0, units='Hz')
    mix = LinearFloatProperty("12", 0.0, 100.0, decimals=0, units='%')

