from typing import override


from ..core.primitive_props import (
    BoolProperty,
    InvertedBoolProperty,
)
from ..core.base_types import MixerCollectionNode, MixerNode, MixerNodeFactory

from ..strips.insert import StripInsert
from ..strips.config import StripConfig
from ..strips.dynamics import StripDynamics
from ..strips.mix import HifiFaderProperty
from ..strips.groups import StripGroups
from .eq import BusStripGraphicEQ, BusStripEq


def get_bus_stereo_link_path(parent: MixerNode):
    """Constructs stereo link path that must be like `/config/buslink/1-2`"""

    assert isinstance(parent, BusConfig)
    num_key = f"{Bus.__name__}_num"
    num = parent.context.get(num_key)
    if num is None:
        raise RuntimeError(f"Bus stereo link property requires '{num_key}' to be in the node's context.")

    if num % 2 == 1:
        segment = f"{num}-{num + 1}"
    else:
        segment = f"{num - 1}-{num}"

    return "/config/buslink/" + segment


class BusConfig(StripConfig):
    "Bus strip name and color. Also bus stereo-link switch."

    stereo_link = BoolProperty(get_bus_stereo_link_path)
    """
    Links odd-numbered bus as left and even-numbered bus as right components of a stereo-pair.
    This value is synchronized between the buses in the pair.
    When link becomes active, Main LR pan automatically set to -1.0, 1.0 for respective buses, but could be changed afterwards;
    when it becomes inactive, Main LR pan of involved buses must be corrected back manually if needed.
    """


class BusMix(MixerNode):
    """
    Bus output section.
    To tune channel send mix to individual buses see channel's mix section.
    """

    mute = InvertedBoolProperty("on")
    fader = HifiFaderProperty("fader")
    send_to_main = BoolProperty("lr")


class Bus(MixerNode):
    """
    Processing sequence in bus strip:
    input -> insert -> eq/geq -> dynamics -> mix.
    """

    config = MixerNodeFactory("config", BusConfig)
    insert = MixerNodeFactory("insert", StripInsert)
    eq = MixerNodeFactory("eq", BusStripEq)
    graphic_eq = MixerNodeFactory("geq", BusStripGraphicEQ)
    dynamics = MixerNodeFactory("dyn", StripDynamics)
    mix = MixerNodeFactory("mix", BusMix)

    groups = MixerNodeFactory("grp", StripGroups)


class Buses(MixerCollectionNode[Bus]):
    """Output buses settings. Input per-channel bus settings (channel sends) are a part of mixer's channels mix section."""

    item_type = Bus
    item_num_width = 1

    @override
    def _pre_init(self):
        if self.item_count is None:
            self.item_count = self.mixer_model.num_bus
