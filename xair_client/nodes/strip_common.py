from enum import IntEnum

from ..properties.codec_type import CodecTypeMixerProperty

from ..properties.sidechain_filter import SidechainKeySource

from ..properties.groups import GroupMaskProperty

from ..properties.dynamics import DynRatioProperty
from ..properties.primitive import (
    BoolProperty,
    EnumIntProperty,
    InvertedLogFloatProperty,
    LinearFloatProperty,
    LogFloatProperty,
    StringProperty,
)
from ..nodes_base import MixerNode


class StripColor(IntEnum):
    OFF = 0
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4
    MAGENTA = 5
    CYAN = 6
    WHITE = 7
    OFF_INVERTED = 8
    RED_INVERTED = 9
    GREEN_INVERTED = 10
    YELLOW_INVERTED = 11
    BLUE_INVERTED = 12
    MAGENTA_INVERTED = 13
    CYAN_INVERTED = 14
    WHITE_INVERTED = 15


class StripConfig(MixerNode):
    """Strip name and color."""

    name = StringProperty("name", max_len=12)
    color = EnumIntProperty("color", StripColor)


class InsertFxSlot(IntEnum):
    OFF = 0
    FX1A = 1
    FX1B = 2
    FX2A = 3
    FX2B = 4
    FX3A = 5
    FX3B = 6
    FX4A = 7
    FX4B = 8


class StereoInsertFxSlot(IntEnum):
    OFF = 0
    FX1 = 1
    FX2 = 2
    FX3 = 3
    FX4 = 4


class StripInsert(MixerNode):
    enabled = BoolProperty("on")
    "For insert to take effect it is also required to activate insert mode on fx itself."

    fx_slot = EnumIntProperty("sel", InsertFxSlot)


class SidechainFilterType(IntEnum):
    LC6 = 0
    LC12 = 1
    HC6 = 2
    HC12 = 3
    BW_1_0 = 4
    BW_2_0 = 5
    BW_3_0 = 6
    BW_5_0 = 7
    BW_10_0 = 8


class EqBandType(IntEnum):
    LCUT = 0
    LSHV = 1
    PEQ = 2
    VEQ = 3
    HSHV = 4
    HCUT = 5


class StripEqBand(MixerNode):
    band_type = EnumIntProperty("type", EqBandType)
    frequency = LogFloatProperty("f", 20.0, 20000.0, decimals=1, units="Hz")
    gain = LinearFloatProperty("g", -15.0, 15.0, decimals=1, units="dB")
    quality = InvertedLogFloatProperty("q", 0.3, 10.0, decimals=1, description="Q factor.")


class DynMode(IntEnum):
    COMP = 0
    EXP = 1


class DynDetector(IntEnum):
    PEAK = 0
    RMS = 1


class DynEnvelope(IntEnum):
    LIN = 0
    LOG = 1


class StripDynamics(MixerNode):
    # Main.
    enabled = BoolProperty("on")
    mode = EnumIntProperty("mode", DynMode)
    threshold = LinearFloatProperty("thr", -60.0, 0.0, decimals=1, units="dB")
    ratio = DynRatioProperty("ratio")
    knee = LinearFloatProperty("knee", 0.0, 5.0, decimals=0, units="dB")
    makeup_gain = LinearFloatProperty("mgain", 0.0, 24.0, decimals=1, units="dB")
    mix_percent = LinearFloatProperty("mix", 0.0, 100.0, decimals=0, units="%")
    auto_time = BoolProperty("auto")

    # Envelope.
    detector = EnumIntProperty("det", DynDetector)
    envelope = EnumIntProperty("env", DynEnvelope)
    attack_ms = LinearFloatProperty("attack", 0.0, 120.0, decimals=1, units="ms")
    hold_ms = LogFloatProperty("hold", 0.02, 2000.0, decimals=1, units="ms")
    release_ms = LogFloatProperty("release", 5.0, 4000.0, decimals=1, units="ms")

    # Side chain filter.
    sidechain_key_source = CodecTypeMixerProperty("keysrc", SidechainKeySource)
    sidechain_filter_enabled = BoolProperty("filter/on")
    sidechain_filter_type = EnumIntProperty("filter/type", SidechainFilterType)
    sidechain_filter_frequency = LogFloatProperty("filter/f", 20.0, 20000.0, decimals=1, units="Hz")


class StripGroups(MixerNode):
    "DCA and mute groups assignment"

    dca = GroupMaskProperty("dca")
    "DCA assignment bit sting."

    mute = GroupMaskProperty("mute")
    "Mute-group assignment bit string."
