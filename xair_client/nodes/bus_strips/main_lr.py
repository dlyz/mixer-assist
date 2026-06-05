from .mix import BusStripMix

from ..strips.config import StripConfig

from ..core.base_types import MixerNode, MixerNodeFactory
from ..core.primitive_props import EnumIntProperty

from ..strips.mix import PanProperty
from ..strips.dynamics import StripDynamicsBase
from ..strips.insert import StereoInsertFxSlot, StripInsert

from .eq import BusStripEq, BusStripGraphicEQ


class MainLRInsert(StripInsert):
    fx_slot = EnumIntProperty("sel", StereoInsertFxSlot)


class MainLRDynamics(StripDynamicsBase):
    pass


class MainLRMix(BusStripMix):
    pan = PanProperty("pan")


class MainLR(MixerNode):
    """
    Main LR bus strip settings.
    Channel strip send mix to the Main is configured in that channel strip's `mix` section.
    """

    config = MixerNodeFactory("config", StripConfig)
    insert = MixerNodeFactory("insert", MainLRInsert)
    eq = MixerNodeFactory("eq", BusStripEq)
    graphic_eq = MixerNodeFactory("geq", BusStripGraphicEQ)
    dynamics = MixerNodeFactory("dyn", MainLRDynamics)
    mix = MixerNodeFactory("mix", MainLRMix)
