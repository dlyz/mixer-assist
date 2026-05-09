from enum import IntEnum
from typing import override

from ..properties.fader_pan import FaderProperty, PanProperty

from .strip_common import StripEqBand

from ..nodes_base import MixerCollectionNode, MixerNode, MixerNodeFactory
from ..properties.primitive import BoolProperty, EnumIntProperty, InvertedBoolProperty, LinearFloatProperty


class ReturnStripEq(MixerNode):
    enabled = BoolProperty("on")
    low = MixerNodeFactory("1", StripEqBand)
    lomid = MixerNodeFactory("2", StripEqBand)
    himid = MixerNodeFactory("3", StripEqBand)
    high = MixerNodeFactory("4", StripEqBand)


class ReturnStripBusSend(MixerNode):
    class ReturnStripBusSendTap(IntEnum):
        # 0: Directly after the A/D converter and Digital Trim.
        INPUT = 0

        # 1: After the Input stage but before the EQ.
        # Includes Polarity/Phase and High Pass Filter (HPF) and Gate.
        PRE_EQ = 1

        # 2: After the 4-band EQ but before the Dynamics (Compressor).
        POST_EQ = 2

        # 3: After EQ and Dynamics, but before the Main Channel Fader.
        # Standard for Monitor/IEM mixes.
        PRE_FADER = 3

        # 4: After the Main Channel Fader.
        # Send level changes proportionally with the main mix fader.
        POST_FADER = 4

        # 5: Fixed unity gain (0dB) send.
        # Disables 'level' fader; uses 'send_to_subgroup' as an On/Off toggle.
        SUB_GROUP = 5

    level = FaderProperty("level", description="Channel fader level for the bus. Ignored when tap is SUB_GROUP.")
    pan = PanProperty(
        "pan",
        description="Effective only when current bus and the next one are joined into stereo-pair. Can not be set from even buses.",
    )
    tap = EnumIntProperty(
        "tap",
        ReturnStripBusSendTap,
        description="The stage at which the signal from the channel is sent to the bus. Sequence is: preamp (input) -> low cut -> gate -> insert -> eq -> dynamics (compressor/expander) -> fader.",
    )
    send_to_subgroup = BoolProperty(
        "grpon",
        description="Effective only when tap is set to SUB_GROUP, when bus becomes a subgroup. Determines whether the channel is sent to the bus.",
    )


class ReturnStripBusMix(MixerCollectionNode[ReturnStripBusSend]):
    description = "Mix settings for each individual bus."

    item_type = ReturnStripBusSend

    @override
    def _pre_init(self):
        if self.item_count is None:
            self.item_count = self.mixer_model.num_bus

    @override
    def _create_item(self, num: int, path_segment: str):
        result = super()._create_item(num=num, path_segment=path_segment)
        # pan exists only on odd buses (works when they are paired)
        if num % 2 == 0:
            result.disabled_children_names = result.disabled_children_names.union(["pan"])
        return result


class ReturnStripFxSend(MixerNode):
    class ReturnStripFxSendTap(IntEnum):
        # 0: Directly after the A/D converter and Digital Trim.
        INPUT = 0

        # 1: After the Input stage but before the EQ.
        # Includes Polarity/Phase and High Pass Filter (HPF) and Gate.
        PRE_EQ = 1

        # 2: After the 4-band EQ but before the Dynamics (Compressor).
        POST_EQ = 2

        # 3: After EQ and Dynamics, but before the Main Channel Fader.
        # Standard for Monitor/IEM mixes.
        PRE_FADER = 3

        # 4: After the Main Channel Fader.
        # Send level changes proportionally with the main mix fader.
        POST_FADER = 4

    level = FaderProperty("level", description="Channel fader level for the fx.")
    tap = EnumIntProperty(
        "tap",
        ReturnStripFxSendTap,
        description="The stage at which the signal from the channel is sent to the fx. Sequence is: preamp (input) -> low cut -> gate -> insert -> eq -> dynamics (compressor/expander) -> fader.",
    )
    # it exists, but makes no sense without SUB_GROUP tap
    # send_to_subgroup = BoolValue(
    #     "grpon",
    #     description="Effective only when tap is set to SUB_GROUP, when bus becomes a subgroup. Determines whether the channel is sent to the bus.",
    # )


class ReturnStripFxMix(MixerCollectionNode[ReturnStripFxSend]):
    description = "Mix settings for each individual fx bus."

    item_type = ReturnStripFxSend

    @override
    def _pre_init(self):
        if self.item_count is None:
            self.item_count = self.mixer_model.num_fx
        self.item_path_start = self.mixer_model.num_bus + 1


class ReturnStripMix(MixerNode):
    description = "Global channel mute, main (lr) mix and mixes for each bus and fx sends."

    mute = InvertedBoolProperty("on")
    main_fader = FaderProperty("fader")
    main_pan = LinearFloatProperty("pan", -1.0, 1.0, decimals=2)
    send_to_main = BoolProperty("lr")
    bus_sends = MixerNodeFactory("", ReturnStripBusMix)
    fx_sends = MixerNodeFactory("", ReturnStripFxMix)
