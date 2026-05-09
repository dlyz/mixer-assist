from typing import Any, override

from ..nodes_base import MixerNode, MixerPropDescriptor, MixerProperty


class DynRatioProperty(MixerProperty[float]):
    _ratios: tuple[float, ...] = (1.1, 1.3, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 7.0, 10.0, 20.0, 100.0)

    def __init__(self, path_segment: str, *, writable: bool = True):
        super().__init__(path_segment, writable=writable)
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
    def make_node_descriptor(self, parent: MixerNode) -> MixerPropDescriptor:
        return self.descriptor
