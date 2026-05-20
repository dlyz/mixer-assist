import abc
from typing import Any, Self, TypeVar, override

from ..nodes_base import MixerNode, MixerPropDescriptor, MixerProperty, MixerPropertyAddressLike, MixerPropertyRWMode


class CodecType(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def parse(cls, value: str) -> Self:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def decode(cls, raw: Any, instance: MixerNode) -> Self:
        raise NotImplementedError

    @abc.abstractmethod
    def encode(self, instance: MixerNode) -> Any:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def make_node_descriptor(cls, parent: MixerNode) -> MixerPropDescriptor:
        raise NotImplementedError


C = TypeVar("C", bound=CodecType)


class CodecTypeMixerProperty(MixerProperty[C]):
    def __init__(
        self,
        address_segment: MixerPropertyAddressLike,
        codec_type: type[C],
        *,
        rw_mode: MixerPropertyRWMode = MixerPropertyRWMode.ReadWrite,
        units: str | None = None,
        constraints: str | None = None,
        description: str | None = None,
    ):
        super().__init__(address_segment, rw_mode=rw_mode)
        self.codec_type = codec_type
        self.units = units
        self.constraints = constraints
        self.description = description

    @override
    def parse(self, value: str) -> C:
        return self.codec_type.parse(value)

    @override
    def decode(self, raw: Any, instance: MixerNode) -> C:
        return self.codec_type.decode(raw, instance)

    @override
    def encode(self, value: C, instance: MixerNode) -> Any:
        return value.encode(instance)

    @override
    def _make_own_node_descriptor(self, parent: MixerNode) -> MixerPropDescriptor:
        type_descriptor = self.codec_type.make_node_descriptor(parent)

        description = self.description
        if not description and self.name:
            description = parent.property_descriptions.get(self.name)
        if not description:
            description = type_descriptor.description

        return MixerPropDescriptor(
            type=type_descriptor.type,
            units=self.units if self.units is not None else type_descriptor.units,
            constraints=self.constraints if self.constraints is not None else type_descriptor.constraints,
            description=description,
        )
