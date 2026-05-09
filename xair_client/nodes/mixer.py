from ..client import XAirClient
from ..nodes_base import MixerNode, MixerNodeFactory
from .buses import Buses, MainLR
from .dca import Dcas
from .channels import Channels
from .fx_sends import FxSends
from .headamp import HeadAmps
from .returns import AuxReturn, FxReturns
from .fx import Fxes


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

    def __init__(self, client: XAirClient):
        super().__init__(client, "/", description=f"{client.mixer_model.name} mixer parameter tree.")
