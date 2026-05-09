# This file is auto-generated with generate_fx_nodes.py. Do not edit manually.

import enum
from enum import IntEnum

from ...nodes_base import MixerNode
from ...properties.primitive import BoolProperty, EnumIntProperty, InvertedBoolProperty, LinearFloatProperty, LogFloatProperty

class ARatioOptions(IntEnum):
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

class BRatioOptions(IntEnum):
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

class DualUltimoCompressorFxParams(MixerNode):
    description = 'Dual Ultimo Compressor effect parameters (Compressor category).'

    a_active = BoolProperty("01")
    a_input = LinearFloatProperty("02", -48.0, 0.0, decimals=0, units='dB')
    a_output = LinearFloatProperty("03", -48.0, 0.0, decimals=0, units='dB')
    a_attack = LinearFloatProperty("04", 1.0, 7.0, decimals=1)
    a_release = LinearFloatProperty("05", 1.0, 7.0, decimals=1)
    a_ratio = EnumIntProperty("06", ARatioOptions)
    b_active = BoolProperty("07")
    b_input = LinearFloatProperty("08", -48.0, 0.0, decimals=0, units='dB')
    b_output = LinearFloatProperty("09", -48.0, 0.0, decimals=0, units='dB')
    b_attack = LinearFloatProperty("10", 1.0, 7.0, decimals=1)
    b_release = LinearFloatProperty("11", 1.0, 7.0, decimals=1)
    b_ratio = EnumIntProperty("12", BRatioOptions)

