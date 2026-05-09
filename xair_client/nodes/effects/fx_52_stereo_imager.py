# This file is auto-generated with generate_fx_nodes.py. Do not edit manually.

import enum
from enum import IntEnum

from ...nodes_base import MixerNode
from ...properties.primitive import BoolProperty, EnumIntProperty, InvertedBoolProperty, LinearFloatProperty, LogFloatProperty

class StereoImagerFxParams(MixerNode):
    description = 'Stereo Imager effect parameters (Enhancer category).'

    balance = LinearFloatProperty("01", -100.0, 100.0, decimals=0, units='%')
    mono_pan = LinearFloatProperty("02", -100.0, 100.0, decimals=0, units='%')
    stereo_pan = LinearFloatProperty("03", -100.0, 100.0, decimals=0, units='%')
    shelve_gain = LinearFloatProperty("04", 0.0, 12.0, decimals=1, units='dB')
    shelve_frequency = LogFloatProperty("05", 100.0, 1000.0, decimals=0, units='Hz')
    shelve_q = LogFloatProperty("06", 1.0, 10.0, decimals=2)
    output_gain = LinearFloatProperty("07", -12.0, 12.0, decimals=1, units='dB')

