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

    @property
    def num(self):
        return -1 if self == InsertFxSlot.OFF else (self.value - 1) // 2 + 1

    @property
    def side(self):
        return -1 if self == InsertFxSlot.OFF else (self.value - 1) % 2

    @staticmethod
    def from_num_side(num: int, side: int):
        if num == -1:
            return InsertFxSlot.OFF
        if not 1 <= num <= 4:
            raise ValueError(f"{num} fx num is invalid for {InsertFxSlot.__name__}")
        if not 0 <= side <= 1:
            raise ValueError(f"{side} fx side is invalid for {InsertFxSlot.__name__}, use 0 for A and 1 for B.")
        return InsertFxSlot(1 + (num - 1) * 2 + side)


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
    frequency = LogFloatProperty("f", 20.0, 20000.0, decimals=1, grid_size=101, units="Hz")
    gain = LinearFloatProperty("g", -15.0, 15.0, decimals=2, grid_size=121, units="dB")
    quality = InvertedLogFloatProperty("q", 0.3, 10.0, decimals=1, grid_size=72, description="Q factor.")


class DynMode(IntEnum):
    COMP = 0
    EXP = 1


class DynDetector(IntEnum):
    PEAK = 0
    RMS = 1


class DynEnvelope(IntEnum):
    LIN = 0
    LOG = 1


class StripDynamicsBase(MixerNode):
    # Main.
    enabled = BoolProperty("on")
    mode = EnumIntProperty("mode", DynMode)
    threshold = LinearFloatProperty("thr", -60.0, 0.0, decimals=1, grid_size=121, units="dB")
    ratio = DynRatioProperty("ratio")
    knee = LinearFloatProperty("knee", 0.0, 5.0, decimals=0, grid_size=6, units="dB")
    makeup_gain = LinearFloatProperty("mgain", 0.0, 24.0, decimals=2, grid_size=49, units="dB")
    mix_percent = LinearFloatProperty("mix", 0.0, 100.0, decimals=0, grid_size=51, units="%")
    auto_time = BoolProperty("auto")

    # Envelope.
    detector = EnumIntProperty("det", DynDetector)
    envelope = EnumIntProperty("env", DynEnvelope)
    attack_ms = LinearFloatProperty("attack", 0.0, 120.0, decimals=0, grid_size=121, units="ms")
    hold_ms = LogFloatProperty("hold", 0.02, 2000.0, decimals=2, grid_size=101, units="ms")
    release_ms = LogFloatProperty("release", 5.0, 4000.0, decimals=0, grid_size=101, units="ms")

    # Side chain filter.
    sidechain_key_source = None
    sidechain_filter_enabled = BoolProperty("filter/on")
    sidechain_filter_type = EnumIntProperty("filter/type", SidechainFilterType)
    sidechain_filter_frequency = LogFloatProperty("filter/f", 20.0, 20000.0, decimals=1, grid_size=101, units="Hz")


class StripDynamics(StripDynamicsBase):
    # Side chain filter.
    sidechain_key_source = CodecTypeMixerProperty("keysrc", SidechainKeySource)


class StripGroups(MixerNode):
    "DCA and mute groups assignment"

    dca = GroupMaskProperty("dca")
    "DCA assignment bit sting."

    mute = GroupMaskProperty("mute")
    "Mute-group assignment bit string."
