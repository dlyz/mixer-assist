from typing import override

from ..properties.fader_pan import FaderProperty

from ..nodes_base import MixerCollectionNode, MixerNode, MixerNodeFactory
from ..properties.primitive import InvertedBoolProperty
from .strip_common import StripConfig


class DcaConfig(StripConfig):
    pass


class Dca(MixerNode):
    description = "DCA group state."

    config = MixerNodeFactory("config", DcaConfig)
    mute = InvertedBoolProperty("on")
    fader = FaderProperty("fader")


class Dcas(MixerCollectionNode[Dca]):
    description = "DCA groups control (without assignment). You can assign channel/bus to a group in it's own section."

    item_type = Dca
    item_num_width = 1

    @override
    def _pre_init(self):
        if self.item_count is None:
            self.item_count = self.mixer_model.num_groups
