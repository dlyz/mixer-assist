from typing import override

from ..nodes_base import MixerPropertyPathLike

from .primitive import FloatProperty, LinearFloatProperty


class FaderProperty(FloatProperty):
    def __init__(
        self,
        path_segment: MixerPropertyPathLike,
        *,
        writable: bool = True,
        minimum: float = -90.0,
        maximum: float = 10.0,
        decimals: int = 1,
        description: str | None = None,
    ):
        super().__init__(
            path_segment,
            minimum,
            maximum,
            writable=writable,
            decimals=decimals,
            units="dB",
            extra_constraints=f", {minimum} means -inf",
            description=description,
        )

    @override
    def _do_decode(self, raw_value: float) -> float:
        if raw_value >= 1.0:
            return float(self.maximum)
        elif raw_value >= 0.5:
            return (40.0 * raw_value) - 30.0
        elif raw_value >= 0.25:
            return (80.0 * raw_value) - 50.0
        elif raw_value >= 0.0625:
            return (160.0 * raw_value) - 70.0
        else:
            return (480.0 * raw_value) - 90.0

    @override
    def _do_encode(self, value: float) -> float:
        if value >= -10.0:
            return (value + 30.0) / 40.0
        elif value >= -30.0:
            return (value + 50.0) / 80.0
        elif value >= -60.0:
            return (value + 70.0) / 160.0
        else:
            return (value + 90.0) / 480.0


class PanProperty(LinearFloatProperty):
    def __init__(
        self,
        path_segment: MixerPropertyPathLike = "pan",
        *,
        writable: bool = True,
        description: str | None = None,
    ):
        super().__init__(path_segment, -1.0, 1.0, decimals=2, writable=writable, description=description)
