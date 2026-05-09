# This file is auto-generated with generate_fx_nodes.py. Do not edit manually.

import enum
from enum import IntEnum

from ...nodes_base import MixerNode
from ...properties.primitive import BoolProperty, EnumIntProperty, InvertedBoolProperty, LinearFloatProperty, LogFloatProperty

class StereoGuitarAmpFxParams(MixerNode):
    description = 'Stereo Guitar Amp effect parameters (Amp simulation category).'

    preamp = LinearFloatProperty("01", 0.0, 10.0, decimals=1)
    buzz = LinearFloatProperty("02", 0.0, 10.0, decimals=1)
    punch = LinearFloatProperty("03", 0.0, 10.0, decimals=1)
    crunch = LinearFloatProperty("04", 0.0, 10.0, decimals=1)
    drive = LinearFloatProperty("05", 0.0, 10.0, decimals=1)
    level = LinearFloatProperty("06", 0.0, 10.0, decimals=1)
    low = LinearFloatProperty("07", 0.0, 10.0, decimals=1)
    high = LinearFloatProperty("08", 0.0, 10.0, decimals=1)
    cabinet = BoolProperty("09")

