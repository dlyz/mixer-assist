# This file is auto-generated with generate_fx_nodes.py. Do not edit manually.

import enum
from enum import IntEnum

from ...nodes_base import MixerNode
from ...properties.primitive import BoolProperty, EnumIntProperty, InvertedBoolProperty, LinearFloatProperty, LogFloatProperty

class RatioOptions(IntEnum):
    V_4 = 0
    V_8 = 1
    V_12 = 2
    V_20 = 3
    LIMIT = 4

    _LABELS = enum.nonmember({
        V_4: '4',
        V_8: '8',
        V_12: '12',
        V_20: '20',
        LIMIT: 'Limit',
    })

class StereoUltimoCompressorFxParams(MixerNode):
    description = 'Stereo Ultimo Compressor effect parameters (Compressor category).'

    active = BoolProperty("01")
    input = LinearFloatProperty("02", -48.0, 0.0, decimals=0, units='dB')
    output = LinearFloatProperty("03", -48.0, 0.0, decimals=0, units='dB')
    attack = LinearFloatProperty("04", 1.0, 7.0, decimals=1)
    release = LinearFloatProperty("05", 1.0, 7.0, decimals=1)
    ratio = EnumIntProperty("06", RatioOptions)

