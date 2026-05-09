# This file is auto-generated with generate_fx_nodes.py. Do not edit manually.

import enum
from enum import IntEnum

from ...nodes_base import MixerNode
from ...properties.primitive import BoolProperty, EnumIntProperty, InvertedBoolProperty, LinearFloatProperty, LogFloatProperty

class StereoEnhancerFxParams(MixerNode):
    description = 'Stereo Enhancer effect parameters (Enhancer category).'

    output_gain = LinearFloatProperty("01", -12.0, 12.0, decimals=1, units='dB')
    spread = LinearFloatProperty("02", 0.0, 100.0, decimals=0, units='%')
    bass_gain = LinearFloatProperty("03", 0.0, 100.0, decimals=0, units='%')
    bass_freq = LinearFloatProperty("04", 1.0, 50.0, decimals=0)
    middle_gain = LinearFloatProperty("05", 0.0, 100.0, decimals=0, units='%')
    middle_q = LinearFloatProperty("06", 1.0, 50.0, decimals=0)
    high_gain = LinearFloatProperty("07", 0.0, 100.0, decimals=0, units='%')
    high_freq = LinearFloatProperty("08", 1.0, 50.0, decimals=0)

