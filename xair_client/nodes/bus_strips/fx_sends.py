from typing import override

from .mix import BusStripMix

from ..strips.config import StripConfig

from ..strips.groups import StripGroups
from ..core.base_types import MixerCollectionNode, MixerNode, MixerNodeFactory


class FxSend(MixerNode):
    "FX Send bus strip with output-level controls."

    config = MixerNodeFactory("config", StripConfig)
    mix = MixerNodeFactory("mix", BusStripMix)

    groups = MixerNodeFactory("grp", StripGroups)


class FxSends(MixerCollectionNode[FxSend]):
    """
    FX Send bus strip settings.
    Channel strip send mix to these FX Sends is configured in that channel strip's `mix` section.
    """

    item_type = FxSend
    item_num_width = 1

    @override
    def _pre_init(self):
        if self.item_count is None:
            self.item_count = self.mixer_model.num_fx
