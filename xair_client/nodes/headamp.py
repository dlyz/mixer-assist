from typing import override

from ..properties.primitive import BoolProperty, LinearFloatProperty

from ..nodes_base import MixerCollectionNode, MixerNode


class HeadAmp(MixerNode):
    """Settings for the mixer's physical input's preamp.
    CAUTION: changing this parameters may be unsafe. Be sure you know what you are doing.
    Input is assigned to the channel in the channel's config section."""

    gain = LinearFloatProperty("gain", -12.0, 60.0, decimals=1, grid_size=145, units="dB")
    phantom = BoolProperty(
        "phantom",
        description="Whether phantom power is enabled for the input. CAUTION! if incompatible device connected, you can burn it.",
    )


class LineHeadAmp(MixerNode):
    """Settings for the mixer's physical line input.
    Input is assigned to the channel in the channel's config section."""

    gain = LinearFloatProperty("gain", -12.0, 20.0, decimals=1, grid_size=65, units="dB")


class HeadAmps(MixerCollectionNode[HeadAmp | LineHeadAmp]):
    item_type = None

    @override
    def _pre_init(self):
        if self.item_count is None:
            self.item_count = self.mixer_model.num_sources

    @override
    def _create_item_name(self, num: int):
        if num > self.mixer_model.num_headamp:
            if self.mixer_model.line_inputs_fixed_stereo:
                if num % 2 == 1:
                    return f"{super()._create_item_name(num)}-{super()._create_item_name(num + 1)}_line"
                else:
                    return super()._create_item_name(num) + "_line_stub"
            else:
                return super()._create_item_name(num) + "_line"
        else:
            return super()._create_item_name(num)

    @override
    def _create_item(self, num: int, address_segment: str):
        if num > self.mixer_model.num_headamp:
            if self.mixer_model.line_inputs_fixed_stereo and num % 2 == 0:
                return None
            item_type = LineHeadAmp
        else:
            item_type = HeadAmp
        return super()._create_typed_item(item_type, num=num, address_segment=address_segment)
