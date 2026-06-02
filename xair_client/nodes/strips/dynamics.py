from enum import IntEnum
from typing import Any, override

from ..core.primitive_props import BoolProperty, EnumIntProperty, LinearFloatProperty, LogFloatProperty
from ..core.codec_type_prop import CodecTypeMixerProperty

from ..core.base_types import (
    MixerNode,
    MixerPropDescriptor,
    MixerProperty,
    MixerPropertyAddressLike,
    MixerPropertyRWMode,
)

from .sidechain_filter import SidechainFilterType, SidechainKeySource


class DynRatioProperty(MixerProperty[float]):
    _ratios: tuple[float, ...] = (1.1, 1.3, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 7.0, 10.0, 20.0, 100.0)

    def __init__(
        self, address_segment: MixerPropertyAddressLike, *, rw_mode: MixerPropertyRWMode = MixerPropertyRWMode.ReadWrite
    ):
        super().__init__(address_segment, rw_mode=rw_mode)
        allowed = ", ".join(str(value) for value in self._ratios)
        self.descriptor = MixerPropDescriptor(
            type="float",
            constraints=f"one of: {allowed}",
            description="Compression ratio x:1.",
        )

    @override
    def parse(self, value: str) -> float:
        return float(value.strip())

    @override
    def decode(self, raw: Any, instance: MixerNode) -> float:
        index = int(raw)
        if not 0 <= index < len(self._ratios):
            raise ValueError(f"ratio raw value must be in range 0..{len(self._ratios) - 1}, got {index}")
        return self._ratios[index]

    @override
    def encode(self, value: float, instance: MixerNode) -> int:
        numeric_value = float(value)
        for index, ratio in enumerate(self._ratios):
            if abs(numeric_value - ratio) < 1e-9:
                return index
        raise ValueError(f"ratio must be one of {self._ratios}, got {numeric_value}")

    @override
    def _make_own_node_descriptor(self, parent: MixerNode) -> MixerPropDescriptor:
        return self.descriptor


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
    "Compressor/expander settings."

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
    sidechain_key_source = None  # keeping to reserve place in property order
    sidechain_filter_enabled = BoolProperty("filter/on")
    sidechain_filter_type = EnumIntProperty("filter/type", SidechainFilterType)
    sidechain_filter_frequency = LogFloatProperty("filter/f", 20.0, 20000.0, decimals=1, grid_size=101, units="Hz")


class StripDynamics(StripDynamicsBase):
    # Side chain filter.
    sidechain_key_source = CodecTypeMixerProperty("keysrc", SidechainKeySource)
