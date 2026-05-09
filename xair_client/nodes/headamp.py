from __future__ import annotations
from typing import override

from ..properties.primitive import BoolProperty, LinearFloatProperty

from ..nodes_base import MixerCollectionNode, MixerNode, MixerNodeFactory


class HeadAmp(MixerNode):
    description = "Settings for the mixer input. Input is assigned to the channel in the channel's config section."

    gain = LinearFloatProperty("gain", -12.0, 60.0, decimals=1, units="dB")
    phantom = BoolProperty("phantom")


class LineHeadAmp(MixerNode):
    description = "Settings for the mixer line input. Input is assigned to the channel in the channel's config section."

    gain = LinearFloatProperty("gain", -12.0, 20.0, decimals=1, units="dB")


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
    def _create_item(self, num: int, path_segment: str):
        disable = False
        if num > self.mixer_model.num_headamp:
            item_type = LineHeadAmp
            if self.mixer_model.line_inputs_fixed_stereo:
                disable = num % 2 == 0
        else:
            item_type = HeadAmp
        result = MixerNodeFactory(self.relative_path(path_segment), item_type).create_node(self)
        if disable:
            result.disabled = True
        return result
