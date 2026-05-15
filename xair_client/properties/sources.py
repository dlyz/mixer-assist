from typing import Any, override

from ..nodes_base import MixerNode, MixerPropDescriptor, MixerProperty, MixerPropertyPathLike


class AnalogSourceProperty(MixerProperty[int]):
    def __init__(
        self,
        path_segment: MixerPropertyPathLike,
        *,
        writable: bool = True,
        description: str | None = None,
    ):
        super().__init__(path_segment, writable=writable)
        self._description = description

    @override
    def parse(self, value: str) -> int:
        return int(value.strip())

    @override
    def decode(self, raw: Any, instance: MixerNode) -> int:
        raw_value = int(raw)
        n = instance.mixer_model.num_sources
        if not 0 <= raw_value <= n:
            raise ValueError(f"analog source raw value must be in range 0..{n}, got {raw_value}")
        if raw_value == n:
            return 0
        return raw_value + 1

    @override
    def encode(self, value: int, instance: MixerNode) -> int:
        n = instance.mixer_model.num_sources
        if not 0 <= value <= n:
            raise ValueError(f"analog source must be in range 0..{n}, got {value}")
        if value == 0:
            return n
        return value - 1

    @override
    def make_node_descriptor(self, parent: MixerNode) -> MixerPropDescriptor:
        n = parent.mixer_model.num_sources
        return MixerPropDescriptor(
            type="int",
            constraints=f"in range [0, {n}]",
            description=self._description,
        )


class UsbSourceProperty(MixerProperty[int]):
    def __init__(
        self,
        path_segment: MixerPropertyPathLike,
        *,
        writable: bool = True,
        description: str | None = None,
    ):
        super().__init__(path_segment, writable=writable)
        self._description = description

    @override
    def parse(self, value: str) -> int:
        return int(value.strip())

    @override
    def decode(self, raw: Any, instance: MixerNode) -> int:
        raw_value = int(raw)
        n = instance.mixer_model.num_sources
        if not 0 <= raw_value < n:
            raise ValueError(f"usb source raw value must be in range 0..{n - 1}, got {raw_value}")
        return raw_value + 1

    @override
    def encode(self, value: int, instance: MixerNode) -> int:
        n = instance.mixer_model.num_sources
        if not 1 <= value <= n:
            raise ValueError(f"usb source must be in range 1..{n}, got {value}")
        return value - 1

    @override
    def make_node_descriptor(self, parent: MixerNode) -> MixerPropDescriptor:
        n = parent.mixer_model.num_sources
        return MixerPropDescriptor(
            type="int",
            constraints=f"in range [1, {n}]",
            description=self._description,
        )


class StereoUsbSourceProperty(MixerProperty[int]):
    def __init__(
        self,
        path_segment: MixerPropertyPathLike,
        *,
        writable: bool = True,
        description: str | None = None,
    ):
        super().__init__(path_segment, writable=writable)
        self._description = description

    @override
    def parse(self, value: str) -> int:
        return int(value.strip())

    @override
    def decode(self, raw: Any, instance: MixerNode) -> int:
        raw_value = int(raw)
        pair_count = instance.mixer_model.num_sources // 2
        if not 0 <= raw_value < pair_count:
            raise ValueError(f"stereo usb source raw value must be in range 0..{pair_count - 1}, got {raw_value}")
        return raw_value * 2 + 1

    @override
    def encode(self, value: int, instance: MixerNode) -> int:
        n = instance.mixer_model.num_sources
        pair_count = n // 2
        if not 1 <= value <= n:
            raise ValueError(f"stereo usb source must be in range 1..{n}, got {value}")
        if value % 2 == 0:
            raise ValueError(f"stereo usb source must be odd to indicate (x, x+1) stereo pair, got {value}")
        raw_value = (value - 1) // 2
        if raw_value >= pair_count:
            raise ValueError(
                f"stereo usb source must select a complete pair in range 1..{pair_count * 2 - 1}, got {value}"
            )
        return raw_value

    @override
    def make_node_descriptor(self, parent: MixerNode) -> MixerPropDescriptor:
        n = parent.mixer_model.num_sources
        pair_count = n // 2
        max_value = max(1, pair_count * 2 - 1)
        return MixerPropDescriptor(
            type="int",
            constraints=f"odd value X in range [1, {max_value}] points to (X, X+1) stereo pair.",
            description=self._description,
        )
