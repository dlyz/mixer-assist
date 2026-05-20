from enum import IntEnum
from typing import override

from ..properties.fader_pan import MainFaderProperty, PanProperty

from .strip_common import (
    StereoInsertFxSlot,
    StripConfig,
    StripDynamics,
    StripEqBand,
    StripGroups,
    StripInsert,
)

from ..properties.primitive import (
    BoolProperty,
    EnumIntProperty,
    InvertedBoolProperty,
    LinearFloatProperty,
)
from ..nodes_base import MixerCollectionNode, MixerNode, MixerNodeFactory


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


class BusDynamics(StripDynamics):
    "Bus compressor/expander settings."


class BusInsert(StripInsert):
    pass


class BusEqBand(StripEqBand):
    pass


class BusEq(MixerNode):
    class EqMode(IntEnum):
        PEQ = 0
        GEQ = 1
        TEQ = 2

    enabled = BoolProperty("on")

    mode = EnumIntProperty("mode", EqMode)
    "For PEQ: only bands in current section are used. For GEQ and TEQ: only bands the bus's graphic EQ section are used."

    low = MixerNodeFactory("1", BusEqBand)
    low2 = MixerNodeFactory("2", BusEqBand)
    lomid = MixerNodeFactory("3", BusEqBand)
    himid = MixerNodeFactory("4", BusEqBand)
    high2 = MixerNodeFactory("5", BusEqBand)
    high = MixerNodeFactory("6", BusEqBand)


class GeqBandProperty(LinearFloatProperty):
    def __init__(self, path_segment: str):
        super().__init__(path_segment, -15.0, 15.0, decimals=1, grid_size=61, units="dB")


class BusGraphicEQ(MixerNode):
    "Effective only when equalizer (bus eq) mode is GEQ (Graphic EQ) or TEQ (TruEQ)."

    f_20 = GeqBandProperty("20")
    f_25 = GeqBandProperty("25")
    f_31_5 = GeqBandProperty("31.5")
    f_40 = GeqBandProperty("40")
    f_50 = GeqBandProperty("50")
    f_63 = GeqBandProperty("63")
    f_80 = GeqBandProperty("80")
    f_100 = GeqBandProperty("100")
    f_125 = GeqBandProperty("125")
    f_160 = GeqBandProperty("160")
    f_200 = GeqBandProperty("200")
    f_250 = GeqBandProperty("250")
    f_315 = GeqBandProperty("315")
    f_400 = GeqBandProperty("400")
    f_500 = GeqBandProperty("500")
    f_630 = GeqBandProperty("630")
    f_800 = GeqBandProperty("800")
    f_1k = GeqBandProperty("1k")
    f_1k25 = GeqBandProperty("1k25")
    f_1k6 = GeqBandProperty("1k6")
    f_2k = GeqBandProperty("2k")
    f_2k5 = GeqBandProperty("2k5")
    f_3k15 = GeqBandProperty("3k15")
    f_4k = GeqBandProperty("4k")
    f_5k = GeqBandProperty("5k")
    f_6k3 = GeqBandProperty("6k3")
    f_8k = GeqBandProperty("8k")
    f_10k = GeqBandProperty("10k")
    f_12k5 = GeqBandProperty("12k5")
    f_16k = GeqBandProperty("16k")
    f_20k = GeqBandProperty("20k")


class BusMix(MixerNode):
    """
    Bus output section.
    To tune channel send mix to individual buses see channel's mix section.
    """

    mute = InvertedBoolProperty("on")
    fader = MainFaderProperty("fader")
    send_to_main = BoolProperty("lr")


class BusGroups(StripGroups):
    pass


class Bus(MixerNode):
    """
    Processing sequence in bus strip:
    input -> insert -> eq/geq -> dynamics -> mix.
    """

    config = MixerNodeFactory("config", BusConfig)
    insert = MixerNodeFactory("insert", BusInsert)
    eq = MixerNodeFactory("eq", BusEq)
    graphic_eq = MixerNodeFactory("geq", BusGraphicEQ)
    dynamics = MixerNodeFactory("dyn", BusDynamics)
    mix = MixerNodeFactory("mix", BusMix)

    groups = MixerNodeFactory("grp", BusGroups)


class Buses(MixerCollectionNode[Bus]):
    """Output buses settings. Input per-channel bus settings (channel sends) are a part of mixer's channels mix section."""

    item_type = Bus
    item_num_width = 1

    @override
    def _pre_init(self):
        if self.item_count is None:
            self.item_count = self.mixer_model.num_bus


class MainLRConfig(StripConfig):
    "Main LR strip name and color."


class MainLRInsert(BusInsert):
    fx_slot = EnumIntProperty("sel", StereoInsertFxSlot)


class MainLRDynamics(StripDynamics):
    # this is not ideal hack: the property exist in the type, but disabled.
    # kept as is cause not sure it worth branching class hierarchy
    disabled_children_names = StripDynamics.disabled_children_names.union(["sidechain_key_source"])


class MainLRMix(MixerNode):
    """
    Main LR output section.
    To tune channel send mix to Main LR see channel's mix section.
    """

    mute = InvertedBoolProperty("on")
    fader = MainFaderProperty("fader")
    pan = PanProperty("pan")


class MainLR(MixerNode):
    config = MixerNodeFactory("config", MainLRConfig)
    insert = MixerNodeFactory("insert", MainLRInsert)
    eq = MixerNodeFactory("eq", BusEq)
    graphic_eq = MixerNodeFactory("geq", BusGraphicEQ)
    dynamics = MixerNodeFactory("dyn", MainLRDynamics)
    mix = MixerNodeFactory("mix", MainLRMix)
