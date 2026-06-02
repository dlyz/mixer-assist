from enum import IntEnum

from ..core.base_types import MixerNode, MixerNodeFactory
from ..core.primitive_props import BoolProperty, EnumIntProperty, LinearFloatProperty
from ..strips.eq import StripEqBand


class BusStripEq(MixerNode):
    class EqMode(IntEnum):
        PEQ = 0
        GEQ = 1
        TEQ = 2

    enabled = BoolProperty("on")

    mode = EnumIntProperty("mode", EqMode)
    "For PEQ: only bands in current section are used. For GEQ and TEQ: only bands the bus's graphic EQ section are used."

    low = MixerNodeFactory("1", StripEqBand)
    low2 = MixerNodeFactory("2", StripEqBand)
    lomid = MixerNodeFactory("3", StripEqBand)
    himid = MixerNodeFactory("4", StripEqBand)
    high2 = MixerNodeFactory("5", StripEqBand)
    high = MixerNodeFactory("6", StripEqBand)


class GeqBandProperty(LinearFloatProperty):
    def __init__(self, address_segment: str):
        super().__init__(address_segment, -15.0, 15.0, decimals=1, grid_size=61, units="dB")


class BusStripGraphicEQ(MixerNode):
    "Effective only when equalizer (bus eq) mode is GEQ (Graphic EQ) or TEQ (TruEQ)."

    f_20 = GeqBandProperty("20")
    f_25 = GeqBandProperty("25")
    f_31_5 = GeqBandProperty("31.5")
    f_40 = GeqBandProperty("40")
    f_50 = GeqBandProperty("50")
    f_63 = GeqBandProperty("63")
    f_80 = GeqBandProperty("80")
    f_100 = GeqBandProperty("100")
    f_125 = GeqBandProperty("125")
    f_160 = GeqBandProperty("160")
    f_200 = GeqBandProperty("200")
    f_250 = GeqBandProperty("250")
    f_315 = GeqBandProperty("315")
    f_400 = GeqBandProperty("400")
    f_500 = GeqBandProperty("500")
    f_630 = GeqBandProperty("630")
    f_800 = GeqBandProperty("800")
    f_1k = GeqBandProperty("1k")
    f_1k25 = GeqBandProperty("1k25")
    f_1k6 = GeqBandProperty("1k6")
    f_2k = GeqBandProperty("2k")
    f_2k5 = GeqBandProperty("2k5")
    f_3k15 = GeqBandProperty("3k15")
    f_4k = GeqBandProperty("4k")
    f_5k = GeqBandProperty("5k")
    f_6k3 = GeqBandProperty("6k3")
    f_8k = GeqBandProperty("8k")
    f_10k = GeqBandProperty("10k")
    f_12k5 = GeqBandProperty("12k5")
    f_16k = GeqBandProperty("16k")
    f_20k = GeqBandProperty("20k")
