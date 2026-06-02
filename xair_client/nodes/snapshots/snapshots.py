from ..core.base_types import MixerCollectionNode, MixerNode, MixerNodeFactory, MixerPropertyRWMode
from ..core.primitive_props import IntProperty, StringProperty
from ..core.codec_type_prop import CodecTypeMixerProperty

from .recall_scopes import SnapshotRecallScope, SNAPSHOT_RECALL_SCOPES_COUNT


SNAPSHOT_SLOTS_COUNT = 64


class Snapshot(MixerNode):
    name = StringProperty("name", max_len=31)

    _recall_scope_string = StringProperty(
        "scope",
        min_len=SNAPSHOT_RECALL_SCOPES_COUNT,
        max_len=SNAPSHOT_RECALL_SCOPES_COUNT,
    )
    "String of +/- for each recall option. Consider using recall_scope instead"

    recall_scope = CodecTypeMixerProperty("scope", SnapshotRecallScope)


class SnapshotSlots(MixerCollectionNode[Snapshot]):
    item_type = Snapshot
    item_count = SNAPSHOT_SLOTS_COUNT
    item_num_width = 2


class Snapshots(MixerNode):
    slots = MixerNodeFactory("", SnapshotSlots)

    # this is just an index, selected in the UI, and useless in the API
    # could actually be used to inspect "working" snapshot, but not reliably
    # current_index = IntProperty("index", 1, SNAPSHOT_SLOTS_COUNT)

    load = IntProperty("load", 1, SNAPSHOT_SLOTS_COUNT, rw_mode=MixerPropertyRWMode.WriteOnly)
    """Setting a snapshot slot number to this property will lead to loading the snapshot into the mixer state.
    Reading this property is useless."""

    name_to_save = StringProperty("name", max_len=31)
    """Set it only before saving the snapshot. To read the name of particular snapshot see slots."""

    save = IntProperty("save", 1, SNAPSHOT_SLOTS_COUNT, rw_mode=MixerPropertyRWMode.WriteOnly)
    """Setting a snapshot slot number to this property will lead to saving current mixer state to that slot using snapshot name from `name_to_save`.
    Reading this property is useless."""

    delete = IntProperty("delete", 1, SNAPSHOT_SLOTS_COUNT, rw_mode=MixerPropertyRWMode.WriteOnly)
    """Setting a snapshot slot number to this property will lead to deleting snapshot from this slot and clearing the slot.
    Reading this property is useless."""
