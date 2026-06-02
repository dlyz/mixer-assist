from typing import override

from ..core.base_types import MixerCollectionNode, MixerNode, MixerNodeFactory
from ..core.primitive_props import (
    BoolProperty,
    LinearFloatProperty,
    LogFloatProperty,
)

from ..strips.insert import StripInsert
from ..strips.config import StripConfig
from ..strips.dynamics import StripDynamics
from ..strips.groups import StripGroups

from .sources import AnalogSourceProperty, UsbSourceProperty
from .gate import ChannelStripGate
from .eq import ChannelStripEq
from .mix import ChannelStripMix


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
    """Channel name and color, as well as selected source for the channel (one of analog inputs or usb returns), and stereo-link switch."""

    stereo_link = BoolProperty(get_channel_stereo_link_path)
    """
    Links odd-numbered channel as left and even-numbered channel as right components of a stereo-pair.
    This value is synchronized between the channels in the pair.
    When link becomes active, Main LR pan automatically set to -1.0, 1.0 for respective channels, but could be changed afterwards;
    when it becomes inactive, Main LR pan of involved channels must be corrected back manually if needed.
    """

    analog_source = AnalogSourceProperty("insrc")
    "Id of analog source (input). 0 to disable. To be effective requires use_usb_input to be false in channel's preamp. Gain is in mixer's headamp section."

    usb_source = UsbSourceProperty("rtnsrc")
    "Id of usb source. To be effective requires use_usb_input to be true in channel's preamp, and the gain (trim) for usb source is there too."


class ChannelPreamp(MixerNode):
    """
    Analog/Usb source switch, usb trim level, low cut and input phase inverter settings.
    The analog source (input) gain is available in mixer's headamps section.
    """

    use_usb_input = BoolProperty("rtnsw")
    "True if the channel will receive signal from usb return, false - if from analog input. The exact input is set in channel's config section."

    usb_trim = LinearFloatProperty("rtntrim", -18.0, 18.0, decimals=1, grid_size=145, units="dB")
    "Usable only if use_usb_input is true."

    invert_phase = BoolProperty("invert")

    low_cut_on = BoolProperty("hpon")

    low_cut_freq = LogFloatProperty("hpf", 20.0, 400.0, decimals=1, grid_size=101, units="Hz")


class ChannelEq(ChannelStripEq):
    "Eq for the channel. Low cut (aka HPF) is separate and could be found in channel's preamp section."


class Channel(MixerNode):
    """
    Mixer channel that receives input, processes the signal and sends it to main lr mix and buses.
    Processing sequence in channel strip:
    preamp + low cut -> gate -> insert -> eq -> dynamics (compressor/expander) -> mix.
    """

    config = MixerNodeFactory("config", ChannelConfig)
    preamp = MixerNodeFactory("preamp", ChannelPreamp)
    gate = MixerNodeFactory("gate", ChannelStripGate)
    insert = MixerNodeFactory("insert", StripInsert)
    eq = MixerNodeFactory("eq", ChannelEq)
    dynamics = MixerNodeFactory("dyn", StripDynamics)
    mix = MixerNodeFactory("mix", ChannelStripMix)

    groups = MixerNodeFactory("grp", StripGroups)


class Channels(MixerCollectionNode[Channel]):
    """
    Mixer channel settings.
    Each channel contains its own send levels and tap settings for every bus and FX send — this is the canonical place to configure the full monitor and effects mix, not the bus or FX send strips themselves.
    """

    item_type = Channel

    @override
    def _pre_init(self):
        if self.item_count is None:
            self.item_count = self.mixer_model.num_channels
