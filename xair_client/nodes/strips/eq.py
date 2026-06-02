from enum import IntEnum

from ..core.base_types import MixerNode
from ..core.primitive_props import EnumIntProperty, InvertedLogFloatProperty, LinearFloatProperty, LogFloatProperty


class EqBandType(IntEnum):
    LCUT = 0
    LSHV = 1
    PEQ = 2
    VEQ = 3
    HSHV = 4
    HCUT = 5


class StripEqBand(MixerNode):
    band_type = EnumIntProperty("type", EqBandType)
    frequency = LogFloatProperty("f", 20.0, 20000.0, decimals=1, grid_size=101, units="Hz")
    gain = LinearFloatProperty("g", -15.0, 15.0, decimals=2, grid_size=121, units="dB")
    quality = InvertedLogFloatProperty("q", 0.3, 10.0, decimals=1, grid_size=72, description="Q factor.")
