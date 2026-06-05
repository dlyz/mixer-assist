from typing import override

from .eq import ChannelStripEq

from ..strips.config import StripConfig

from .mix import ChannelStripMix

from .sources import StereoUsbSourceProperty
from ..strips.groups import StripGroups
from ..core.primitive_props import BoolProperty, LinearFloatProperty
from ..core.base_types import MixerCollectionNode, MixerNode, MixerNodeFactory


class ReturnStripConfig(StripConfig):
    "Strip name and color, as well as selected usb source for the return."

    usb_source = StereoUsbSourceProperty("rtnsrc")
    "Id of first usb source in a stereo pair. To be effective requires `use_usb_input` to be true in return's `preamp` section."


class ReturnStripPreamp(MixerNode):
    use_usb_input = BoolProperty("rtnsw")

    usb_trim = LinearFloatProperty("rtntrim", -18.0, 18.0, decimals=1, grid_size=145, units="dB")
    "Usable only if `use_usb_input` is true."


class ReturnStrip(MixerNode):
    """
    Return channel strip that receives source signal and sends it to bus strips: main lr, buses and fx sends.
    Processing sequence in return strip:
    preamp -> eq -> mix.
    """

    config = MixerNodeFactory("config", ReturnStripConfig)
    preamp = MixerNodeFactory("preamp", ReturnStripPreamp)
    eq = MixerNodeFactory("eq", ChannelStripEq)
    mix = MixerNodeFactory("mix", ChannelStripMix)

    groups = MixerNodeFactory("grp", StripGroups)


class FxReturnPreamp(ReturnStripPreamp):
    """
    Fx/usb source switch, usb trim level.
    """

    use_usb_input = BoolProperty("rtnsw")
    """True if the return strip will receive signal from a USB return (source set in this strip's `config` section),
    false if it will receive signal from the FX effect assigned to this return slot."""


class FxReturn(ReturnStrip):
    preamp = MixerNodeFactory("preamp", FxReturnPreamp)


class FxReturns(MixerCollectionNode[FxReturn]):
    "FX return channel strips settings."

    item_type = FxReturn
    item_num_width = 1

    @override
    def _pre_init(self):
        if self.item_count is None:
            self.item_count = self.mixer_model.num_fx


class AuxReturnPreamp(ReturnStripPreamp):
    """
    Analog/Usb source switch, usb trim level.
    The physical analog source (input) gain is available in mixer's `headamps` section (fixed line input headamp).
    """

    use_usb_input = BoolProperty("rtnsw")
    """True if the channel strip will receive signal from usb return, false - if from analog input.
    The exact input is set in strip's `config` section."""


class AuxReturn(ReturnStrip):
    """
    AUX Return (AUX Channel) channel strip.
    Can use physical analog line input source or USB source."""

    preamp = MixerNodeFactory("preamp", AuxReturnPreamp)
