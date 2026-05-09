# This file is auto-generated with generate_fx_nodes.py. Do not edit manually.

import enum
from enum import IntEnum

from ...nodes_base import MixerNode
from ...properties.primitive import BoolProperty, EnumIntProperty, InvertedBoolProperty, LinearFloatProperty, LogFloatProperty

class DualGuitarAmpFxParams(MixerNode):
    description = 'Dual Guitar Amp effect parameters (Amp simulation category).'

    a_preamp = LinearFloatProperty("01", 0.0, 10.0, decimals=1)
    a_buzz = LinearFloatProperty("02", 0.0, 10.0, decimals=1)
    a_punch = LinearFloatProperty("03", 0.0, 10.0, decimals=1)
    a_crunch = LinearFloatProperty("04", 0.0, 10.0, decimals=1)
    a_drive = LinearFloatProperty("05", 0.0, 10.0, decimals=1)
    a_level = LinearFloatProperty("06", 0.0, 10.0, decimals=1)
    a_low = LinearFloatProperty("07", 0.0, 10.0, decimals=1)
    a_high = LinearFloatProperty("08", 0.0, 10.0, decimals=1)
    a_cabinet = BoolProperty("09")
    b_preamp = LinearFloatProperty("10", 0.0, 10.0, decimals=1)
    b_buzz = LinearFloatProperty("11", 0.0, 10.0, decimals=1)
    b_punch = LinearFloatProperty("12", 0.0, 10.0, decimals=1)
    b_crunch = LinearFloatProperty("13", 0.0, 10.0, decimals=1)
    b_drive = LinearFloatProperty("14", 0.0, 10.0, decimals=1)
    b_level = LinearFloatProperty("15", 0.0, 10.0, decimals=1)
    b_low = LinearFloatProperty("16", 0.0, 10.0, decimals=1)
    b_high = LinearFloatProperty("17", 0.0, 10.0, decimals=1)
    b_cabinet = BoolProperty("18")

