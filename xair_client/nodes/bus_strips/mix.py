from ..strips.mix import FaderProperty

from ..core.primitive_props import InvertedBoolProperty

from ..core.base_types import MixerNode


class BusStripMix(MixerNode):
    """
    Bus strip output mix section.
    To tune channel strip send mix to individual bus strips see channel strip's `mix` section.
    """

    mute = InvertedBoolProperty("on")
    fader = FaderProperty("fader")
