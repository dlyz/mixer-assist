from enum import IntEnum
from typing import override

from ..strips.mix import FaderProperty, HifiFaderProperty, PanProperty


from ..core.base_types import MixerCollectionNode, MixerNode, MixerNodeFactory
from ..core.primitive_props import BoolProperty, EnumIntProperty, InvertedBoolProperty


class ChannelStripBusSend(MixerNode):
    class Tap(IntEnum):
        """The stage at which the signal from the channel is sent to the bus.
        Sequence is: preamp (input) -> low cut -> gate -> insert -> eq -> dynamics (compressor/expander) -> main fader.
        """

        INPUT = 0
        """Directly after the A/D converter or Digital Trim (for USB input)."""

        PRE_EQ = 1
        """After the Input stage but before the EQ.
        Includes Polarity/Phase, Low cut (High Pass Filter) and Gate."""

        POST_EQ = 2
        """After the EQ but before the Dynamics (Compressor/Expander)."""

        PRE_FADER = 3
        """After EQ and Dynamics, but before the Main Channel Fader.
        Standard for Monitor/IEM mixes."""

        POST_FADER = 4
        """After the Main Channel Fader.
        Send level changes proportionally with the main mix fader."""

        SUB_GROUP = 5
        """Fixed unity gain (0dB) send.
        Disables 'level' fader; uses 'send_to_subgroup' as an On/Off toggle."""

    level = FaderProperty("level")
    "Channel fader level for the bus. Ignored when tap is SUB_GROUP."

    pan = PanProperty("pan")
    """Effective only when current bus and the next one are joined into a stereo-pair.
    The pan value set on the odd bus applies to the signal within that pair; pan can not be accessed from even buses."""

    tap = EnumIntProperty("tap", Tap)

    send_to_subgroup = BoolProperty("grpon")
    """Effective only when tap is set to SUB_GROUP.
    When a bus is used as a subgroup, this flag determines whether this channel is routed into it."""


class ChannelStripBusMix(MixerCollectionNode[ChannelStripBusSend]):
    "Mix settings for each individual bus."

    item_type = ChannelStripBusSend

    @override
    def _pre_init(self):
        if self.item_count is None:
            self.item_count = self.mixer_model.num_bus

    @override
    def _create_item(self, num: int, address_segment: str):
        result = super()._create_item(num=num, address_segment=address_segment)
        assert result
        # pan exists only on odd buses (works when they are paired)
        if num % 2 == 0:
            result.disabled_properties = result.disabled_properties.union(["pan"])
        return result


class ChannelStripFxSend(MixerNode):
    class Tap(IntEnum):
        """The stage at which the signal from the channel is sent to the fx.
        Sequence is: preamp (input) -> low cut -> gate -> insert -> eq -> dynamics (compressor/expander) -> main fader.
        """

        INPUT = 0
        """Directly after the A/D converter or Digital Trim (for USB input)."""

        PRE_EQ = 1
        """After the Input stage but before the EQ.
        Includes Polarity/Phase, Low cut (High Pass Filter) and Gate."""

        POST_EQ = 2
        """After the EQ but before the Dynamics (Compressor/Expander)."""

        PRE_FADER = 3
        """After EQ and Dynamics, but before the Main Channel Fader.
        Standard for Monitor/IEM mixes."""

        POST_FADER = 4
        """After the Main Channel Fader.
        Send level changes proportionally with the main mix fader."""

    level = FaderProperty("level")
    "Channel fader level for the fx."

    tap = EnumIntProperty("tap", Tap)

    # it exists, but makes no sense without SUB_GROUP tap
    # send_to_subgroup = BoolValue("grpon")
    # "Effective only when tap is set to SUB_GROUP, when bus becomes a subgroup. Determines whether the channel is sent to the bus."


class ChannelStripFxMix(MixerCollectionNode[ChannelStripFxSend]):
    "Mix settings for each individual fx bus."

    item_type = ChannelStripFxSend

    @override
    def _pre_init(self):
        if self.item_count is None:
            self.item_count = self.mixer_model.num_fx
        self.item_path_start = self.mixer_model.num_bus + 1


class ChannelStripMix(MixerNode):
    "Global channel mute and mixes for all bus strips: main (lr), buses, fx sends."

    mute = InvertedBoolProperty("on")
    main_fader = HifiFaderProperty("fader")
    main_pan = PanProperty("pan")
    send_to_main = BoolProperty("lr")
    bus_sends = MixerNodeFactory("", ChannelStripBusMix)
    fx_sends = MixerNodeFactory("", ChannelStripFxMix)
