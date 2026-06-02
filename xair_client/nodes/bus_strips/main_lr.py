from ..strips.config import StripConfig

from ..core.base_types import MixerNode, MixerNodeFactory
from ..core.primitive_props import EnumIntProperty, InvertedBoolProperty

from ..strips.mix import HifiFaderProperty, PanProperty
from ..strips.dynamics import StripDynamicsBase
from ..strips.insert import StereoInsertFxSlot, StripInsert

from .eq import BusStripEq, BusStripGraphicEQ


class MainLRInsert(StripInsert):
    fx_slot = EnumIntProperty("sel", StereoInsertFxSlot)


class MainLRDynamics(StripDynamicsBase):
    pass


class MainLRMix(MixerNode):
    """
    Main LR output section.
    To tune channel send mix to Main LR see channel's mix section.
    """

    mute = InvertedBoolProperty("on")
    fader = HifiFaderProperty("fader")
    pan = PanProperty("pan")


class MainLR(MixerNode):
    config = MixerNodeFactory("config", StripConfig)
    insert = MixerNodeFactory("insert", MainLRInsert)
    eq = MixerNodeFactory("eq", BusStripEq)
    graphic_eq = MixerNodeFactory("geq", BusStripGraphicEQ)
    dynamics = MixerNodeFactory("dyn", MainLRDynamics)
    mix = MixerNodeFactory("mix", MainLRMix)
