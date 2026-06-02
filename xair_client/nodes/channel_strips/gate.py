from ..core.base_types import MixerNode
from ..core.codec_type_prop import CodecTypeMixerProperty
from ..core.primitive_props import BoolProperty, EnumIntProperty, LinearFloatProperty, LogFloatProperty
from ..strips.sidechain_filter import SidechainFilterType, SidechainKeySource


from enum import IntEnum


class ChannelStripGate(MixerNode):
    class GateMode(IntEnum):
        EXP2 = 0
        EXP3 = 1
        EXP4 = 2
        GATE = 3
        DUCK = 4

    # Main
    enabled = BoolProperty("on")
    mode = EnumIntProperty("mode", GateMode)
    threshold = LinearFloatProperty("thr", -80.0, 0.0, decimals=1, grid_size=161, units="dB")
    reduction_range = LinearFloatProperty("range", 3.0, 60.0, decimals=1, grid_size=58, units="dB")

    # Envelope
    attack_ms = LinearFloatProperty("attack", 0.0, 120.0, decimals=0, grid_size=121, units="ms")
    hold_ms = LogFloatProperty("hold", 0.02, 2000.0, decimals=2, grid_size=101, units="ms")
    release_ms = LogFloatProperty("release", 5.0, 4000.0, decimals=0, grid_size=101, units="ms")

    # Side chain filter
    sidechain_key_source = CodecTypeMixerProperty("keysrc", SidechainKeySource)
    sidechain_filter_enabled = BoolProperty("filter/on")
    sidechain_filter_type = EnumIntProperty("filter/type", SidechainFilterType)
    sidechain_filter_frequency = LogFloatProperty("filter/f", 20.0, 20000.0, decimals=1, grid_size=101, units="Hz")
