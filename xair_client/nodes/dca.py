from typing import override

from .strips.mix import FaderProperty

from .core.base_types import MixerCollectionNode, MixerNode, MixerNodeFactory
from .core.primitive_props import InvertedBoolProperty
from .strips.config import StripConfig


class DcaConfig(StripConfig):
    pass


class Dca(MixerNode):
    "DCA group state."

    config = MixerNodeFactory("config", DcaConfig)
    mute = InvertedBoolProperty("on")
    fader = FaderProperty("fader")


class Dcas(MixerCollectionNode[Dca]):
    "DCA groups control (without assignment). You can assign channel/bus to a group in it's own section."

    item_type = Dca
    item_num_width = 1

    @override
    def _pre_init(self):
        if self.item_count is None:
            self.item_count = self.mixer_model.num_groups
