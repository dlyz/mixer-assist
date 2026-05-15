from enum import IntEnum

from typing import override

from ..nodes_base import MixerCollectionNode, MixerNode, MixerNodeFactory
from ..properties.primitive import EnumIntProperty


# TODO: constraints on enum values depending on the mixer model


class RoutingTap(IntEnum):
    """The stage at which the signal from the channel (or analog input) is sent to the routed out.
    Sequence is: preamp (input) -> low cut -> gate -> insert -> eq -> dynamics (compressor/expander) -> main fader."""

    ANALOG_IN = 0
    """From analog input with preamp (after the A/D converter).
    Ignores analog input to channel assignment, takes raw signal from the physical input."""
    ANALOG_IN_WITH_MUTE = 1

    CHANNEL_IN = 2
    """Directly after the A/D converter or Digital Trim (for USB input).
    Considers whatever source for the channel is selected: one of analog inputs or USB."""
    CHANNEL_IN_WITH_MUTE = 3

    PRE_EQ = 4
    """After the Input stage but before the EQ.
    Includes Polarity/Phase, Low cut (High Pass Filter) Gate and inserted effect if any."""
    PRE_EQ_WITH_MUTE = 5

    POST_EQ = 6
    """After the EQ but before the Dynamics (Compressor/Expander)."""
    POST_EQ_WITH_MUTE = 7

    PRE_FADER = 8
    """After EQ and Dynamics, but before the Main Channel Fader."""
    PRE_FADER_WITH_MUTE = 9

    POST_FADER = 10
    """After the Main Channel Fader.
    Send level changes proportionally with the main mix fader."""


class RoutingUsbSource(IntEnum):
    CH_01 = 0
    CH_02 = 1
    CH_03 = 2
    CH_04 = 3
    CH_05 = 4
    CH_06 = 5
    CH_07 = 6
    CH_08 = 7
    CH_09 = 8
    CH_10 = 9
    CH_11 = 10
    CH_12 = 11
    CH_13 = 12
    CH_14 = 13
    CH_15 = 14
    CH_16 = 15
    AUX_L = 16
    AUX_R = 17
    FX_1L = 18
    FX_1R = 19
    FX_2L = 20
    FX_2R = 21
    FX_3L = 22
    FX_3R = 23
    FX_4L = 24
    FX_4R = 25
    BUS_1 = 26
    BUS_2 = 27
    BUS_3 = 28
    BUS_4 = 29
    BUS_5 = 30
    BUS_6 = 31
    FX_SEND_1 = 32
    FX_SEND_2 = 33
    FX_SEND_3 = 34
    FX_SEND_4 = 35
    MAIN_L = 36
    MAIN_R = 37


class RoutingInputSource(IntEnum):
    CH_01 = 0
    CH_02 = 1
    CH_03 = 2
    CH_04 = 3
    CH_05 = 4
    CH_06 = 5
    CH_07 = 6
    CH_08 = 7
    CH_09 = 8
    CH_10 = 9
    CH_11 = 10
    CH_12 = 11
    CH_13 = 12
    CH_14 = 13
    CH_15 = 14
    CH_16 = 15
    AUX_L = 16
    AUX_R = 17
    FX_1L = 18
    FX_1R = 19
    FX_2L = 20
    FX_2R = 21
    FX_3L = 22
    FX_3R = 23
    FX_4L = 24
    FX_4R = 25
    BUS_1 = 26
    BUS_2 = 27
    BUS_3 = 28
    BUS_4 = 29
    BUS_5 = 30
    BUS_6 = 31
    FX_SEND_1 = 32
    FX_SEND_2 = 33
    FX_SEND_3 = 34
    FX_SEND_4 = 35
    MAIN_L = 36
    MAIN_R = 37
    USB_01 = 38
    USB_02 = 39
    USB_03 = 40
    USB_04 = 41
    USB_05 = 42
    USB_06 = 43
    USB_07 = 44
    USB_08 = 45
    USB_09 = 46
    USB_10 = 47
    USB_11 = 48
    USB_12 = 49
    USB_13 = 50
    USB_14 = 51
    USB_15 = 52
    USB_16 = 53
    USB_17 = 54
    USB_18 = 55


class RoutingMainSource(IntEnum):
    MAIN_LR = 0
    MONITOR = 1
    USB_01_02 = 2
    USB_03_04 = 3
    USB_05_06 = 4
    USB_07_08 = 5
    USB_09_10 = 6
    USB_11_12 = 7
    USB_13_14 = 8
    USB_15_16 = 9
    USB_17_18 = 10


class RoutingOut(MixerNode):
    tap = EnumIntProperty("pos", RoutingTap)
    source = EnumIntProperty("src", RoutingInputSource)


class RoutingUsbOut(MixerNode):
    tap = EnumIntProperty("pos", RoutingTap)
    source = EnumIntProperty("src", RoutingUsbSource)


class RoutingAuxOuts(MixerCollectionNode[RoutingOut]):
    description = "Aux out routing taps and sources."
    item_type = RoutingOut
    item_num_width = 2

    @override
    def _pre_init(self):
        if self.item_count is None:
            self.item_count = self.mixer_model.num_aux_outs


class RoutingUltranetOuts(MixerCollectionNode[RoutingOut]):
    description = "Ultranet out routing taps and sources."
    item_type = RoutingOut
    item_num_width = 2

    @override
    def _pre_init(self):
        if self.item_count is None:
            self.item_count = 16


class RoutingUsbOuts(MixerCollectionNode[RoutingUsbOut]):
    description = "USB out routing taps and sources."
    item_type = RoutingUsbOut
    item_num_width = 2

    @override
    def _pre_init(self):
        if self.item_count is None:
            self.item_count = self.mixer_model.num_usb


class RoutingMainOut(MixerNode):
    source = EnumIntProperty("src", RoutingMainSource)


class Routing(MixerNode):
    description = "Routing taps and sources for following outs: aux, main, phones, usb, ultranet."

    aux = MixerNodeFactory("aux", RoutingAuxOuts)
    main = MixerNodeFactory("main/01", RoutingMainOut, description="Main out routing source")
    phones = MixerNodeFactory("main/02", RoutingMainOut, description="Phones out routing source")
    usb = MixerNodeFactory("usb", RoutingUsbOuts)
    ultranet = MixerNodeFactory("p16", RoutingUltranetOuts)
