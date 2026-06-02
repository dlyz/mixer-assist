from typing import override

from ..strips.config import StripConfig

from ..strips.mix import HifiFaderProperty

from ..strips.groups import StripGroups
from ..core.primitive_props import InvertedBoolProperty
from ..core.base_types import MixerCollectionNode, MixerNode, MixerNodeFactory


class FxSendConfig(StripConfig):
    pass


class FxSendMix(MixerNode):
    """
    FX send output section.
    Input levels into each FX send are configured in channels and returns mix sections of the mixer.
    """

    mute = InvertedBoolProperty("on")
    fader = HifiFaderProperty("fader")


class FxSendGroup(StripGroups):
    pass


class FxSend(MixerNode):
    "FX send strip with output-level controls."

    config = MixerNodeFactory("config", FxSendConfig)
    mix = MixerNodeFactory("mix", FxSendMix)
    groups = MixerNodeFactory("grp", FxSendGroup)


class FxSends(MixerCollectionNode[FxSend]):
    """Output fx-sends settings. Input per-channel fx-sends settings (channel sends) are a part of mixer's channels mix section."""

    item_type = FxSend
    item_num_width = 1

    @override
    def _pre_init(self):
        if self.item_count is None:
            self.item_count = self.mixer_model.num_fx
