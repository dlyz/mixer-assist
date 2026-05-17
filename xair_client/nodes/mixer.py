from typing import override

from .snapshots import Snapshots

from ..properties.primitive import BoolProperty

from ..client import XAirClient
from ..nodes_base import MixerNode, MixerNodeFactory, MixerCollectionNode
from .buses import Buses, MainLR
from .dca import Dcas
from .channels import Channels
from .fx_sends import FxSends
from .headamp import HeadAmps
from .routing import Routing
from .returns import AuxReturn, FxReturns
from .fx import Fxes


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
    fx_returns = MixerNodeFactory("rtn", FxReturns)
    aux_return = MixerNodeFactory("rtn/aux", AuxReturn)
    buses = MixerNodeFactory("bus", Buses)
    fx_sends = MixerNodeFactory("fxsend", FxSends)
    main_lr = MixerNodeFactory("lr", MainLR)

    fx = MixerNodeFactory("fx", Fxes)
    dcas = MixerNodeFactory("dca", Dcas)
    mute_groups = MixerNodeFactory("config/mute", MixerMuteGroups)
    routing = MixerNodeFactory("routing", Routing)
    config = MixerNodeFactory("config", MixerConfig)
    snapshots = MixerNodeFactory("-snap", Snapshots)

    def __init__(self, client: XAirClient):
        super().__init__(client, "/", description=f"{client.mixer_model.name} mixer parameter tree.")
