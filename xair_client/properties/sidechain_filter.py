from dataclasses import dataclass
from enum import Enum
import re
from typing import Any, Self, override

from .codec_type import CodecType
from ..nodes_base import MixerNode, MixerPropDescriptor


class SidechainKeySourceKind(Enum):
    SELF = "self"
    CHANNEL = "channel"
    BUS = "bus"


@dataclass(frozen=True)
class SidechainKeySource(CodecType):
    kind: SidechainKeySourceKind
    number: int | None = None

    def __post_init__(self):
        if self.kind is SidechainKeySourceKind.SELF and self.number is not None:
            raise ValueError("self key source must not have a number")
        if self.kind is not SidechainKeySourceKind.SELF:
            if self.number is None:
                raise ValueError(f"{self.kind.value} key source requires a number")
            if self.number < 1:
                raise ValueError(f"{self.kind.value} key source number must be >= 1, got {self.number}")

    def __str__(self) -> str:
        if self.kind is SidechainKeySourceKind.SELF:
            return "self"
        assert self.number is not None
        prefix = "ch" if self.kind is SidechainKeySourceKind.CHANNEL else "bus"
        return f"{prefix}:{self.number}"

    @classmethod
    @override
    def parse(cls, value: str) -> Self:
        text = value.strip().lower()
        if text == "self":
            return cls(SidechainKeySourceKind.SELF)
        channel_match = re.fullmatch(r"(?:ch|chan|channel)\s*[:#/\-]?\s*(\d+)", text)
        if channel_match is not None:
            return cls(SidechainKeySourceKind.CHANNEL, int(channel_match.group(1)))
        bus_match = re.fullmatch(r"(?:bus)\s*[:#/\-]?\s*(\d+)", text)
        if bus_match is not None:
            return cls(SidechainKeySourceKind.BUS, int(bus_match.group(1)))
        raise ValueError(f"invalid GateKeySource string {value!r}, expected 'self', 'ch:<n>', or 'bus:<n>'")

    @classmethod
    @override
    def decode(cls, raw: Any, instance: MixerNode) -> Self:
        raw_value = int(raw)
        if raw_value == 0:
            return cls(SidechainKeySourceKind.SELF)
        if 1 <= raw_value <= instance.mixer_model.num_channels:
            return cls(SidechainKeySourceKind.CHANNEL, raw_value)
        bus_index = raw_value - instance.mixer_model.num_channels
        if 1 <= bus_index <= instance.mixer_model.num_bus:
            return cls(SidechainKeySourceKind.BUS, bus_index)
        raise ValueError(f"keysrc raw value must map to self/channel/bus for this model, got {raw_value}")

    @override
    def encode(self, instance: MixerNode) -> int:
        if self.kind is SidechainKeySourceKind.SELF:
            return 0
        assert self.number is not None
        if self.kind is SidechainKeySourceKind.CHANNEL:
            if not 1 <= self.number <= instance.mixer_model.num_channels:
                raise ValueError(
                    f"channel key source must be in range 1..{instance.mixer_model.num_channels}, got {self.number}"
                )
            return self.number
        if self.kind is SidechainKeySourceKind.BUS:
            if not 1 <= self.number <= instance.mixer_model.num_bus:
                raise ValueError(
                    f"bus key source must be in range 1..{instance.mixer_model.num_bus}, got {self.number}"
                )
            return instance.mixer_model.num_channels + self.number
        raise ValueError(f"unsupported key source kind {self.kind}")

    @classmethod
    @override
    def make_node_descriptor(cls, parent: MixerNode, writable: bool) -> MixerPropDescriptor:
        return MixerPropDescriptor(
            type="str",
            constraints=f"one of: self, ch:<1..{parent.mixer_model.num_channels}>, bus:<1..{parent.mixer_model.num_bus}>",
        )
