from typing import override

from ..core.base_types import MixerPropertyAddressLike, MixerPropertyRWMode

from ..core.primitive_props import FloatProperty, LinearFloatProperty


class FaderProperty(FloatProperty):
    MINIMUM = -90.0
    MAXIMUM = 10.0

    @staticmethod
    def clamp_level(level: float):
        return min(max(level, FaderProperty.MINIMUM), FaderProperty.MAXIMUM)

    @staticmethod
    def level_to_fader_hight(level: float):
        return max(0, level - FaderProperty.MINIMUM)

    def __init__(
        self,
        address_segment: MixerPropertyAddressLike,
        *,
        rw_mode: MixerPropertyRWMode = MixerPropertyRWMode.ReadWrite,
        grid_size: int = 161,
        description: str | None = None,
    ):
        super().__init__(
            address_segment,
            minimum=self.MINIMUM,
            maximum=self.MAXIMUM,
            rw_mode=rw_mode,
            decimals=1,
            grid_size=grid_size,
            units="dB",
            extra_constraints=f", {self.MINIMUM} means -inf",
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


class HifiFaderProperty(FaderProperty):
    def __init__(
        self,
        address_segment: MixerPropertyAddressLike,
        *,
        rw_mode: MixerPropertyRWMode = MixerPropertyRWMode.ReadWrite,
        description: str | None = None,
    ):
        super().__init__(address_segment, rw_mode=rw_mode, grid_size=1024, description=description)


class PanProperty(LinearFloatProperty):
    def __init__(
        self,
        address_segment: MixerPropertyAddressLike = "pan",
        *,
        rw_mode: MixerPropertyRWMode = MixerPropertyRWMode.ReadWrite,
        description: str | None = None,
    ):
        super().__init__(
            address_segment,
            -1.0,
            1.0,
            decimals=2,
            grid_size=101,
            rw_mode=rw_mode,
            description=description,
        )
