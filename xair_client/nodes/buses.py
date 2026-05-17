from enum import IntEnum
import textwrap
from typing import override

from ..properties.fader_pan import FaderProperty, PanProperty

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
    description = "Bus strip name and color. Also bus stereo-link switch."

    stereo_link = BoolProperty(
        get_bus_stereo_link_path,
        description=textwrap.dedent(
            """
            Links odd-numbered bus as left and even-numbered bus as right components of a stereo-pair.
            This value is synchronized between the buses in the pair.
            When link becomes active, Main LR pan automatically set to -1.0, 1.0 for respective buses, but could be changed afterwards;
            when it becomes inactive, Main LR pan of involved buses must be corrected back manually if needed.
            """
        ),
    )


class BusDynamics(StripDynamics):
    description = "Bus compressor/expander settings."


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
    mode = EnumIntProperty(
        "mode",
        EqMode,
        description="For PEQ: only bands in current section are used. For GEQ and TEQ: only bands the bus's graphic EQ section are used.",
    )

    low = MixerNodeFactory("1", BusEqBand)
    low2 = MixerNodeFactory("2", BusEqBand)
    lomid = MixerNodeFactory("3", BusEqBand)
    himid = MixerNodeFactory("4", BusEqBand)
    high2 = MixerNodeFactory("5", BusEqBand)
    high = MixerNodeFactory("6", BusEqBand)


class BusGraphicEQ(MixerNode):
    description = "Effective only when equalizer (bus eq) mode is GEQ (Graphic EQ) or TEQ (TruEQ)."

    f_20 = LinearFloatProperty("20", -15.0, 15.0, decimals=1, units="dB")
    f_25 = LinearFloatProperty("25", -15.0, 15.0, decimals=1, units="dB")
    f_31_5 = LinearFloatProperty("31.5", -15.0, 15.0, decimals=1, units="dB")
    f_40 = LinearFloatProperty("40", -15.0, 15.0, decimals=1, units="dB")
    f_50 = LinearFloatProperty("50", -15.0, 15.0, decimals=1, units="dB")
    f_63 = LinearFloatProperty("63", -15.0, 15.0, decimals=1, units="dB")
    f_80 = LinearFloatProperty("80", -15.0, 15.0, decimals=1, units="dB")
    f_100 = LinearFloatProperty("100", -15.0, 15.0, decimals=1, units="dB")
    f_125 = LinearFloatProperty("125", -15.0, 15.0, decimals=1, units="dB")
    f_160 = LinearFloatProperty("160", -15.0, 15.0, decimals=1, units="dB")
    f_200 = LinearFloatProperty("200", -15.0, 15.0, decimals=1, units="dB")
    f_250 = LinearFloatProperty("250", -15.0, 15.0, decimals=1, units="dB")
    f_315 = LinearFloatProperty("315", -15.0, 15.0, decimals=1, units="dB")
    f_400 = LinearFloatProperty("400", -15.0, 15.0, decimals=1, units="dB")
    f_500 = LinearFloatProperty("500", -15.0, 15.0, decimals=1, units="dB")
    f_630 = LinearFloatProperty("630", -15.0, 15.0, decimals=1, units="dB")
    f_800 = LinearFloatProperty("800", -15.0, 15.0, decimals=1, units="dB")
    f_1k = LinearFloatProperty("1k", -15.0, 15.0, decimals=1, units="dB")
    f_1k25 = LinearFloatProperty("1k25", -15.0, 15.0, decimals=1, units="dB")
    f_1k6 = LinearFloatProperty("1k6", -15.0, 15.0, decimals=1, units="dB")
    f_2k = LinearFloatProperty("2k", -15.0, 15.0, decimals=1, units="dB")
    f_2k5 = LinearFloatProperty("2k5", -15.0, 15.0, decimals=1, units="dB")
    f_3k15 = LinearFloatProperty("3k15", -15.0, 15.0, decimals=1, units="dB")
    f_4k = LinearFloatProperty("4k", -15.0, 15.0, decimals=1, units="dB")
    f_5k = LinearFloatProperty("5k", -15.0, 15.0, decimals=1, units="dB")
    f_6k3 = LinearFloatProperty("6k3", -15.0, 15.0, decimals=1, units="dB")
    f_8k = LinearFloatProperty("8k", -15.0, 15.0, decimals=1, units="dB")
    f_10k = LinearFloatProperty("10k", -15.0, 15.0, decimals=1, units="dB")
    f_12k5 = LinearFloatProperty("12k5", -15.0, 15.0, decimals=1, units="dB")
    f_16k = LinearFloatProperty("16k", -15.0, 15.0, decimals=1, units="dB")
    f_20k = LinearFloatProperty("20k", -15.0, 15.0, decimals=1, units="dB")


class BusMix(MixerNode):
    description = textwrap.dedent(
        """
        Bus output section.
        To tune channel send mix to individual buses see channel's mix section.
        """
    )

    mute = InvertedBoolProperty("on")
    fader = FaderProperty("fader")
    send_to_main = BoolProperty("lr")


class BusGroups(StripGroups):
    pass


class Bus(MixerNode):
    description = textwrap.dedent(
        """
        Processing sequence in bus strip:
        input -> insert -> eq/geq -> dynamics -> mix.
        """
    )

    config = MixerNodeFactory("config", BusConfig)
    insert = MixerNodeFactory("insert", BusInsert)
    eq = MixerNodeFactory("eq", BusEq)
    graphic_eq = MixerNodeFactory("geq", BusGraphicEQ)
    dynamics = MixerNodeFactory("dyn", BusDynamics)
    mix = MixerNodeFactory("mix", BusMix)

    groups = MixerNodeFactory("grp", BusGroups)


class Buses(MixerCollectionNode[Bus]):
    description = """Output buses settings. Input per-channel bus settings (channel sends) are a part of mixer's channels mix section."""

    item_type = Bus
    item_num_width = 1

    @override
    def _pre_init(self):
        if self.item_count is None:
            self.item_count = self.mixer_model.num_bus


class MainLRConfig(StripConfig):
    description = "Main LR strip name and color."


class MainLRInsert(BusInsert):
    fx_slot = EnumIntProperty("sel", StereoInsertFxSlot)


class MainLRDynamics(StripDynamics):
    # this is not ideal hack: the property exist in the type, but disabled.
    # kept as is cause not sure it worth branching class hierarchy
    disabled_children_names = StripDynamics.disabled_children_names.union(["sidechain_key_source"])


class MainLRMix(MixerNode):
    description = textwrap.dedent(
        """
        Main LR output section.
        To tune channel send mix to Main LR see channel's mix section.
        """
    )

    mute = InvertedBoolProperty("on")
    fader = FaderProperty("fader")
    pan = PanProperty("pan")


class MainLR(MixerNode):
    config = MixerNodeFactory("config", MainLRConfig)
    insert = MixerNodeFactory("insert", MainLRInsert)
    eq = MixerNodeFactory("eq", BusEq)
    graphic_eq = MixerNodeFactory("geq", BusGraphicEQ)
    dynamics = MixerNodeFactory("dyn", MainLRDynamics)
    mix = MixerNodeFactory("mix", MainLRMix)
