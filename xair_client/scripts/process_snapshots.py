from typing import Callable

from ..nodes.mixer import Mixer

from ..nodes.snapshots.snapshots import Snapshot, Snapshots


def process_snapshots(
    mixer: Mixer,
    slots: list[int],
    action: Callable[[int, Snapshot], None],
    save=False,
):
    for num in slots:
        slot = mixer.snapshots.slots[num]
        if not slot.name:
            continue

        original_recall_str = slot._recall_scope_string
        full_recall_str = "+" * len(original_recall_str)
        if original_recall_str != full_recall_str:
            slot._recall_scope_string = full_recall_str

        try:
            Snapshots.load.commit(mixer.snapshots, num)
        finally:
            if original_recall_str != full_recall_str:
                slot._recall_scope_string = original_recall_str

        action(num, slot)

        if save:
            Snapshots.save.commit(mixer.snapshots, num)
