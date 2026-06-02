from ..core.base_types import MixerNode, MixerNodeFactory
from ..core.primitive_props import BoolProperty
from ..strips.eq import StripEqBand


class ChannelStripEq(MixerNode):
    enabled = BoolProperty("on")
    low = MixerNodeFactory("1", StripEqBand)
    lomid = MixerNodeFactory("2", StripEqBand)
    himid = MixerNodeFactory("3", StripEqBand)
    high = MixerNodeFactory("4", StripEqBand)
