from enum import IntEnum
import textwrap
from typing import override

from ..nodes_base import MixerCollectionNode, MixerNode, MixerNodeFactory

from .returns_common import ReturnStripEq, ReturnStripMix
from .strip_common import (
    SidechainFilterType,
    StripConfig,
    StripDynamics,
    StripGroups,
    StripInsert,
)

from ..properties.codec_type import CodecTypeMixerProperty
from ..properties.sidechain_filter import SidechainKeySource
from ..properties.sources import AnalogSourceProperty, UsbSourceProperty
from ..properties.primitive import (
    BoolProperty,
    EnumIntProperty,
    LinearFloatProperty,
    LogFloatProperty,
)


def get_channel_stereo_link_path(parent: MixerNode):
    """Constructs stereo link path that must be like `/config/chlink/1-2`"""

    assert isinstance(parent, ChannelConfig)
    num_key = f"{Channel.__name__}_num"
    num = parent.context.get(num_key)
    if num is None:
        raise RuntimeError(f"Channel stereo link property requires '{num_key}' to be in the node's context.")

    if num % 2 == 1:
        segment = f"{num}-{num + 1}"
    else:
        segment = f"{num - 1}-{num}"

    return "/config/chlink/" + segment


class ChannelConfig(StripConfig):
    description = "Channel name and color, as well as selected source for the channel (one of analog inputs or usb returns), and stereo-link switch."

    stereo_link = BoolProperty(
        get_channel_stereo_link_path,
        description=textwrap.dedent(
            """
            Links odd-numbered channel as left and even-numbered channel as right components of a stereo-pair.
            This value is synchronized between the channels in the pair.
            When link becomes active, Main LR pan automatically set to -1.0, 1.0 for respective channels, but could be changed afterwards;
            when it becomes inactive, Main LR pan of involved channels must be corrected back manually if needed.
            """
        ),
    )

    analog_source = AnalogSourceProperty(
        "insrc",
        description="Id of analog source (input). To be effective requires use_usb_input to be false in channel's preamp. Gain is in mixer's headamp section.",
    )
    usb_source = UsbSourceProperty(
        "rtnsrc",
        description="Id of usb source. To be effective requires use_usb_input to be true in channel's preamp, and the gain (trim) for usb source is there too.",
    )


class ChannelPreamp(MixerNode):
    description = textwrap.dedent(
        """
        Analog/Usb source switch, usb trim level, low cut and input phase inverter settings.
        The analog source (input) gain is available in mixer's headamps section.
        """
    )

    use_usb_input = BoolProperty(
        "rtnsw",
        description="True if the channel will receive signal from usb return, false - if from analog input. The exact input is set in channel's config section.",
    )
    usb_trim = LinearFloatProperty(
        "rtntrim",
        -18.0,
        18.0,
        decimals=1,
        units="dB",
        description="Usable only if use_usb_input is true.",
    )
    invert_phase = BoolProperty("invert")
    low_cut_on = BoolProperty("hpon")
    low_cut_freq = LogFloatProperty("hpf", 20.0, 400.0, decimals=1, units="Hz")


class ChannelGate(MixerNode):
    class GateMode(IntEnum):
        EXP2 = 0
        EXP3 = 1
        EXP4 = 2
        GATE = 3
        DUCK = 4

    # Main
    enabled = BoolProperty("on")
    mode = EnumIntProperty("mode", GateMode)
    threshold = LinearFloatProperty("thr", -80.0, 0.0, decimals=1, units="dB")
    reduction_range = LinearFloatProperty("range", 3.0, 60.0, decimals=1, units="dB")

    # Envelope
    attack_ms = LinearFloatProperty("attack", 0.0, 120.0, decimals=1, units="ms")
    hold_ms = LogFloatProperty("hold", 0.02, 2000.0, decimals=1, units="ms")
    release_ms = LogFloatProperty("release", 5.0, 4000.0, decimals=1, units="ms")

    # Side chain filter
    sidechain_key_source = CodecTypeMixerProperty("keysrc", SidechainKeySource)
    sidechain_filter_enabled = BoolProperty("filter/on")
    sidechain_filter_type = EnumIntProperty("filter/type", SidechainFilterType)
    sidechain_filter_frequency = LogFloatProperty("filter/f", 20.0, 20000.0, decimals=1, units="Hz")


class ChannelEq(ReturnStripEq):
    description = "Eq for the channel. Low cut (aka HPF) is separate and could be found in channel's preamp section."


class ChannelDynamics(StripDynamics):
    description = "Compressor/expander settings."


class ChannelInsert(StripInsert):
    pass


class ChannelMix(ReturnStripMix):
    pass


class ChannelGroups(StripGroups):
    pass


class Channel(MixerNode):
    description = textwrap.dedent(
        """
        Mixer channel that receives input, processes the signal and sends it to main lr mix and buses.
        Processing sequence in channel strip:
        preamp + low cut -> gate -> insert -> eq -> dynamics (compressor/expander) -> mix.
        """
    )

    config = MixerNodeFactory("config", ChannelConfig)
    preamp = MixerNodeFactory("preamp", ChannelPreamp)
    gate = MixerNodeFactory("gate", ChannelGate)
    insert = MixerNodeFactory("insert", ChannelInsert)
    eq = MixerNodeFactory("eq", ChannelEq)
    dynamics = MixerNodeFactory("dyn", ChannelDynamics)
    mix = MixerNodeFactory("mix", ChannelMix)

    groups = MixerNodeFactory("grp", ChannelGroups)


class Channels(MixerCollectionNode[Channel]):
    description = textwrap.dedent(
        """
        Mixer channel settings.
        Each channel contains its own send levels and tap settings for every bus and FX send — this is the canonical place to configure the full monitor and effects mix, not the bus or FX send strips themselves.
        """
    )
    item_type = Channel

    @override
    def _pre_init(self):
        if self.item_count is None:
            self.item_count = self.mixer_model.num_channels
