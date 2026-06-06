from ..nodes.channel_strips.mix import ChannelStripMix

from ..nodes.strips.mix import LevelProperty

from ..nodes.mixer import AnyChannelStrip, Mixer


def copy_mix(
    mixer: Mixer,
    source_bus: int,
    target_buses: list[int],
    *,
    channels: list[int] | None = None,
    aux: bool = False,
    fxes: list[int] | None = None,
    relative_to_mix: AnyChannelStrip | ChannelStripMix | None = None,
):
    MIN_SOURCE_REL_LEVEL = 1e-5
    if isinstance(relative_to_mix, ChannelStripMix):
        pass
    elif relative_to_mix is not None:
        relative_to_mix = relative_to_mix.mix

    channel_strips: list[AnyChannelStrip] = [
        *(mixer.channels[c] for c in (channels or [])),
        *([mixer.aux_return] if aux else []),
        *(mixer.fx_returns[i] for i in (fxes or [])),
    ]
    mixes = [c.mix for c in channel_strips]

    if relative_to_mix is not None:
        source_relative_level = LevelProperty.level_to_fader_hight(relative_to_mix.bus_sends[source_bus].level)
        if source_relative_level < MIN_SOURCE_REL_LEVEL:
            raise ValueError("Source reference channel level is -inf")
    else:
        source_relative_level = 0

    source_levels = [mix.bus_sends[source_bus].level for mix in mixes]
    for target_bus in target_buses:
        if relative_to_mix is not None:
            assert not (source_relative_level < MIN_SOURCE_REL_LEVEL)
            multiplier = (
                LevelProperty.level_to_fader_hight(relative_to_mix.bus_sends[target_bus].level) / source_relative_level
            )
        else:
            multiplier = 1.0

        for mix, level in zip(mixes, source_levels):
            new_hight = LevelProperty.level_to_fader_hight(level) * multiplier
            new_level = LevelProperty.fader_hight_to_level(new_hight)
            mix.bus_sends[target_bus].level = LevelProperty.clamp_level(new_level)
