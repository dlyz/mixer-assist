from dataclasses import dataclass
from typing import Iterable, Mapping

from ..nodes.mixer import Mixer


@dataclass
class ChannelStripInputs:
    analog_source: int
    usb_source: int
    use_usb_input: bool


class InputsProfile:
    def __init__(self, mixer: Mixer):
        self.mixer = mixer
        self._channels = {
            num: ChannelStripInputs(c.config.analog_source, c.config.usb_source, c.preamp.use_usb_input)
            for num, c in mixer.channels
        }
        self._fx_returns = {
            num: ChannelStripInputs(0, c.config.usb_source, c.preamp.use_usb_input) for num, c in mixer.fx_returns
        }
        self._aux = ChannelStripInputs(0, mixer.aux_return.config.usb_source, mixer.aux_return.preamp.use_usb_input)

    def restore(self):
        for num, c in self.mixer.channels:
            inputs = self._channels[num]
            c.config.usb_source = inputs.usb_source
            c.preamp.use_usb_input = inputs.use_usb_input
            c.config.analog_source = inputs.analog_source

        for num, c in self.mixer.fx_returns:
            inputs = self._fx_returns[num]
            c.config.usb_source = inputs.usb_source
            c.preamp.use_usb_input = inputs.use_usb_input

        self.mixer.aux_return.config.usb_source = self._aux.usb_source
        self.mixer.aux_return.preamp.use_usb_input = self._aux.use_usb_input

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.restore()

    def disable_inputs(self, *, disable_aux_analog_in: bool = True):
        for num, c in self.mixer.channels:
            c.config.analog_source = 0
            c.preamp.use_usb_input = False
        if disable_aux_analog_in:
            self.mixer.aux_return.preamp.use_usb_input = True

    def disable_selected_inputs(self, *, channels: Iterable[int] | None = None, disable_aux_analog_in: bool = False):
        if channels:
            for num in channels:
                c = self.mixer.channels[num]
                c.config.analog_source = 0
                c.preamp.use_usb_input = False
        if disable_aux_analog_in:
            self.mixer.aux_return.preamp.use_usb_input = True

    def remap_channels(self, new_to_old_map: Mapping[int, int]):
        channels = {**self._channels}
        for new, old in new_to_old_map.items():
            channels[new] = self._channels[old]
        self._channels = channels

    def remap_fxes(self, new_to_old_map: Mapping[int, int]):
        fxes = {**self._channels}
        for new, old in new_to_old_map.items():
            fxes[new] = self._fx_returns[old]
        self._fx_returns = fxes
