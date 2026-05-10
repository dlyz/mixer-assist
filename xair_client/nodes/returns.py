import textwrap
from typing import override

from .returns_common import ReturnStripEq, ReturnStripMix

from ..properties.sources import StereoUsbSourceProperty
from .strip_common import StripConfig, StripGroups
from ..properties.primitive import BoolProperty, LinearFloatProperty
from ..nodes_base import MixerCollectionNode, MixerNode, MixerNodeFactory


class ReturnConfig(StripConfig):
    description = "Return-strip name and color, as well as selected usb source for the return."

    usb_source = StereoUsbSourceProperty(
        "rtnsrc",
        description="Id of first usb source in a stereo pair. To be effective requires use_usb_input to be true in return's preamp.",
    )


class ReturnPreamp(MixerNode):
    use_usb_input = BoolProperty("rtnsw")

    usb_trim = LinearFloatProperty(
        "rtntrim",
        -18.0,
        18.0,
        decimals=1,
        units="dB",
        description="Usable only if use_usb_input is true.",
    )


class ReturnEq(ReturnStripEq):
    pass


class ReturnMix(ReturnStripMix):
    pass


class ReturnGroup(StripGroups):
    pass


class Return(MixerNode):
    description = textwrap.dedent(
        """
        Return strip that receives source signal and sends it to main lr mix, buses and fx sends.
        Processing sequence in return strip:
        preamp -> eq -> mix.
        """
    )

    config = MixerNodeFactory("config", ReturnConfig)
    groups = MixerNodeFactory("grp", ReturnGroup)
    preamp = MixerNodeFactory("preamp", ReturnPreamp)
    eq = MixerNodeFactory("eq", ReturnEq)
    mix = MixerNodeFactory("mix", ReturnMix)


class FxReturnPreamp(ReturnPreamp):
    description = textwrap.dedent(
        """
        Fx/usb source switch, usb trim level.
        """
    )

    use_usb_input = BoolProperty(
        "rtnsw",
        description="True if the return strip will receive signal from a USB return (source set in this strip's config section), false if it will receive signal from the FX effect assigned to this return slot.",
    )


class FxReturn(Return):
    preamp = MixerNodeFactory("preamp", FxReturnPreamp)


class FxReturns(MixerCollectionNode[FxReturn]):
    description = "FX return channels settings."

    item_type = FxReturn
    item_num_width = 1

    @override
    def _pre_init(self):
        if self.item_count is None:
            self.item_count = self.mixer_model.num_fx


class AuxReturnPreamp(ReturnPreamp):
    description = textwrap.dedent(
        """
        Analog/Usb source switch, usb trim level.
        The analog source (input) gain is available in mixer's headamps section.
        """
    )

    use_usb_input = BoolProperty(
        "rtnsw",
        description="True if the channel will receive signal from usb return, false - if from analog input. The exact input is set in channel's config section.",
    )


class AuxReturn(Return):
    preamp = MixerNodeFactory("preamp", AuxReturnPreamp)
