from typing import override

from .bus_strips.main_lr import MainLR

from .snapshots.snapshots import Snapshots

from .core.primitive_props import BoolProperty

from ..client import XAirClient
from .core.base_types import MixerNode, MixerNodeFactory, MixerCollectionNode
from .bus_strips.buses import Buses
from .dca import Dcas
from .channel_strips.channels import Channels
from .bus_strips.fx_sends import FxSends
from .headamp import HeadAmps
from .routing import Routing
from .channel_strips.returns import AuxReturn, FxReturns
from .fxes.fxes import Fxes


class MixerMuteGroup(MixerNode):
    muted = BoolProperty("")


class MixerMuteGroups(MixerCollectionNode[MixerMuteGroup]):
    "Mute groups on/off control (without assignment). You can assign channel/bus to a group in it's own section."

    item_type = MixerMuteGroup
    item_num_width = 1

    @override
    def _pre_init(self):
        if self.item_count is None:
            self.item_count = self.mixer_model.num_groups


class MixerStereoLinkConfig(MixerNode):
    "Global stereo link config (what props are linked between stereo-linked channels)"

    preamp = BoolProperty("preamp")

    eq = BoolProperty("eq")

    dynamics = BoolProperty("dyn")
    "Compressor/expander"

    main_lr_mix = BoolProperty("fdrmute")
    "Fader, mute for Main LR. Mix settings for other buses are always linked. Pan is always independent."


class MixerConfig(MixerNode):
    "Stereo link config"

    stereo_link = MixerNodeFactory("linkcfg", MixerStereoLinkConfig)


class Mixer(MixerNode):
    headamps = MixerNodeFactory("headamp", HeadAmps)

    channels = MixerNodeFactory("ch", Channels)
    aux_return = MixerNodeFactory("rtn/aux", AuxReturn)
    fx_returns = MixerNodeFactory("rtn", FxReturns)

    buses = MixerNodeFactory("bus", Buses)
    fx_sends = MixerNodeFactory("fxsend", FxSends)
    main_lr = MixerNodeFactory("lr", MainLR)

    fxes = MixerNodeFactory("fx", Fxes)
    dcas = MixerNodeFactory("dca", Dcas)
    mute_groups = MixerNodeFactory("config/mute", MixerMuteGroups)
    routing = MixerNodeFactory("routing", Routing)
    config = MixerNodeFactory("config", MixerConfig)
    snapshots = MixerNodeFactory("-snap", Snapshots)

    def all_channel_strips(self):
        for _, c in self.channels:
            yield c
        yield self.aux_return
        for _, c in self.fx_returns:
            yield c

    def all_bus_strips(self):
        for _, c in self.buses:
            yield c
        for _, c in self.fx_sends:
            yield c
        yield self.main_lr

    def __init__(self, client: XAirClient):
        super().__init__(client, "/", description=f"{client.mixer_model.name} mixer parameter tree.")
