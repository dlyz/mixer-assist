from typing import Iterable, Mapping

from ..nodes.mixer import AnyStrip, Mixer
from ..nodes.core.base_types import MixerCollectionNode


class StripCollectionMutesProfile:
    def __init__(self, strips: MixerCollectionNode[AnyStrip]):
        self.strips = strips
        self._mutes = {num: strip.mix.mute for num, strip in strips}

    def restore(self):
        for num, strip in self.strips:
            strip.mix.mute = self._mutes[num]

    def mute(self, items: Iterable[int] | None = None):
        if items is None:
            for num, strip in self.strips:
                strip.mix.mute = True
        else:
            for num in items:
                self.strips[num].mix.mute = True

    def remap(self, new_to_old_map: Mapping[int, int]):
        mutes = {**self._mutes}
        for new, old in new_to_old_map.items():
            mutes[new] = self._mutes[old]
        self._mutes = mutes


class StripMuteProfile:
    def __init__(self, strip: AnyStrip):
        self.strip = strip
        self._mute = strip.mix.mute

    def restore(self):
        self.strip.mix.mute = self._mute

    def mute(self):
        self.strip.mix.mute = True


class MutesProfile:
    def __init__(self, mixer: Mixer):
        self.mixer = mixer

        self._channels = StripCollectionMutesProfile(mixer.channels)
        self._aux_return = StripMuteProfile(mixer.aux_return)
        self._fx_returns = StripCollectionMutesProfile(mixer.fx_returns)
        self._buses = StripCollectionMutesProfile(mixer.buses)
        self._fx_sends = StripCollectionMutesProfile(mixer.fx_sends)
        self._main_lr = StripMuteProfile(mixer.main_lr)

        self._mutes: list[StripCollectionMutesProfile | StripMuteProfile] = [
            self._channels,
            self._aux_return,
            self._fx_returns,
            self._buses,
            self._fx_sends,
            self._main_lr,
        ]

    def restore(self):
        for mute in self._mutes:
            mute.restore()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.restore()

    def mute(self):
        for mute in self._mutes:
            mute.mute()

    def mute_selected(
        self,
        *,
        channels: Iterable[int] | None = None,
        aux_return: bool = False,
        fx_returns: Iterable[int] | None = None,
        buses: Iterable[int] | None = None,
        fx_sends: Iterable[int] | None = None,
        main_lr: bool = False,
    ):
        if channels:
            self._channels.mute(channels)
        if aux_return:
            self._aux_return.mute()
        if fx_returns:
            self._fx_returns.mute(fx_returns)
        if buses:
            self._buses.mute(buses)
        if fx_sends:
            self._fx_sends.mute(fx_sends)
        if main_lr:
            self._main_lr.mute()

    def remap_channels(self, new_to_old_map: Mapping[int, int]):
        self._channels.remap(new_to_old_map)

    def remap_fxes(self, new_to_old_map: Mapping[int, int]):
        self._fx_returns.remap(new_to_old_map)
        self._fx_sends.remap(new_to_old_map)

    def remap_buses(self, new_to_old_map: Mapping[int, int]):
        self._buses.remap(new_to_old_map)
