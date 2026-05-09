from enum import IntEnum
import textwrap
from typing import override

from ..properties.fader_pan import FaderProperty, PanProperty

from .strip_common import (
    StripConfig,
    StripDyn,
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


class BusConfig(StripConfig):
    description = "Bus name and color."


class BusDyn(StripDyn):
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


class BusGroup(StripGroups):
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
    dyn = MixerNodeFactory("dyn", BusDyn)
    mix = MixerNodeFactory("mix", BusMix)
    groups = MixerNodeFactory("grp", BusGroup)


class Buses(MixerCollectionNode[Bus]):
    description = """Output buses settings. Input per-channel bus settings (channel sends) are a part of mixer's channels mix section."""

    item_type = Bus
    item_num_width = 1

    @override
    def _pre_init(self):
        if self.item_count is None:
            self.item_count = self.mixer_model.num_bus


class MainLRMix(MixerNode):
    description = textwrap.dedent(
        """
        Main LR output section.
        To tune channel send mix to main lr see channel's mix section.
        """
    )

    mute = InvertedBoolProperty("on")
    fader = FaderProperty("fader")
    pan = PanProperty("pan")


class MainLRDyn(StripDyn):
    # this is not ideal hack: the property exist in the type, but disabled.
    # kept as is cause not sure it worth branching class hierarchy
    disabled_children_names = StripDyn.disabled_children_names.union(["sidechain_key_source"])


class MainLR(MixerNode):
    config = MixerNodeFactory("config", BusConfig)
    insert = MixerNodeFactory("insert", BusInsert)
    eq = MixerNodeFactory("eq", BusEq)
    # geq = MixerNodeFactory("geq", BusGeq)
    dyn = MixerNodeFactory("dyn", MainLRDyn)
    mix = MixerNodeFactory("mix", MainLRMix)
