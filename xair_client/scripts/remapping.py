from collections import Counter
from typing import Iterable

from .inputs_profile import InputsProfile
from ..nodes.core.base_types import MixerCollectionNode, MixerNode
from ..nodes.mixer import Mixer
from .mutes_profile import MutesProfile
from ..nodes.strips.insert import InsertFxSlot, StereoInsertFxSlot
from ..nodes.strips.insert import StripInsert


def remap_channels(
    mixer: Mixer,
    new_to_old_map: dict[int, int],
    with_sources: bool = False,
    with_headamps: bool = True,
):
    with MutesProfile(mixer) as mutes:
        mutes.mute_selected(channels=new_to_old_map.keys())

        with InputsProfile(mixer) as inputs:
            if with_headamps and not with_sources:
                # TODO: phantom safety, line headamps has no phantom

                headamps = CollectionState(mixer.headamps)
                headamps_map, target_input_dupes = to_dict_and_key_dupes(
                    [
                        (mixer.channels[new].config.analog_source, mixer.channels[old].config.analog_source)
                        for new, old in new_to_old_map.items()
                    ]
                )
                if target_input_dupes:
                    raise ValueError(
                        f"Can not remap headamps due to following target analog inputs have multiple sources: {target_input_dupes}"
                    )

                def apply_headamps():
                    headamps.remap_values(headamps_map).apply_values()

                _apply_headamps = apply_headamps
            else:
                _apply_headamps = None

            inputs.disable_selected_inputs(channels=new_to_old_map.keys())

            states = CollectionState(mixer.channels)
            states.remap_values(new_to_old_map).apply_values()

            if with_sources:
                inputs.remap_channels(new_to_old_map)

            if _apply_headamps:
                _apply_headamps()

        mutes.remap_channels(new_to_old_map)


def remap_fxes(mixer: Mixer, new_to_old_slots: dict[int, int]):
    old_to_new_slots = {old: new for new, old in new_to_old_slots.items()}

    with MutesProfile(mixer) as mutes:
        mutes.mute()

        fx_states = [
            CollectionState(mixer.fxes),
            *(CollectionState(channel.mix.fx_sends) for _, channel in mixer.channels),
            CollectionState(mixer.aux_return.mix.fx_sends),
            CollectionState(mixer.fx_returns),
            CollectionState(mixer.fx_sends),
        ]

        # doing manually to pass validation
        fx_types = {num: fx.effect_type for num, fx in mixer.fxes}
        for new_num, old_num in new_to_old_slots.items():
            mixer.fxes[new_num].effect_type = fx_types[old_num]

        for state in fx_states:
            state.remap_values(new_to_old_slots).apply_values()

        mutes.remap_fxes(new_to_old_slots)

        def remap_insert(insert: StripInsert):
            slot = insert.fx_slot
            if slot == InsertFxSlot.OFF:
                return
            if slot.num not in old_to_new_slots:
                return
            num = old_to_new_slots[slot.num]
            insert.fx_slot = InsertFxSlot.from_num_side(num, slot.side)

        for _, channel in mixer.channels:
            remap_insert(channel.insert)
        for _, bus in mixer.buses:
            remap_insert(bus.insert)

        main_ins = mixer.main_lr.insert
        main_ins_slot = main_ins.fx_slot
        if main_ins_slot != StereoInsertFxSlot.OFF and main_ins_slot in old_to_new_slots:
            main_ins.fx_slot = StereoInsertFxSlot.from_num(old_to_new_slots[main_ins_slot])


class CollectionState:
    def __init__(self, node: MixerCollectionNode, values: dict[int, dict] | None = None):
        self._node: MixerCollectionNode[MixerNode] = node
        self._values = values if values is not None else {num: item.to_dict() for num, item in self._node}

    def remap_values(self, new_to_old: dict[int, int]):
        new_values = dict(self._values)
        for new, old in new_to_old.items():
            new_values[new] = self._values[old]
        return CollectionState(self._node, new_values)

    def apply_values(self):
        for num, value in self._values.items():
            self._node[num].set_values_from_dict(value)


def to_dict_and_key_dupes[K, V](pairs: Iterable[tuple[K, V]]):
    key_counts = Counter(key for key, _ in pairs)
    duplicates = [key for key, count in key_counts.items() if count > 1]
    return dict(pairs), duplicates
