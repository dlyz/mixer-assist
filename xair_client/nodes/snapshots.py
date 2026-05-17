from abc import abstractmethod
from dataclasses import dataclass, field
import enum
from typing import Any, ClassVar, Generic, Iterable, Self, TypeVar, override

from ..properties.codec_type import CodecType, CodecTypeMixerProperty

from ..properties.primitive import IntProperty, StringProperty

from ..nodes_base import MixerCollectionNode, MixerNode, MixerNodeFactory, MixerPropDescriptor


SNAPSHOT_SLOTS_COUNT = 64

E = TypeVar("E", bound="_SnapshotRecallEnum")


@dataclass(frozen=True, slots=True)
class _SnapshotRecallGroup(Generic[E]):
    token: str
    items: tuple[E, ...]
    items_set: frozenset[E] = field(init=False, repr=False)

    def __post_init__(self):
        object.__setattr__(self, "items_set", frozenset(self.items))


@dataclass(frozen=True, slots=True)
class _SnapshotRecallNumberedGroup(_SnapshotRecallGroup[E], Generic[E]):
    item_by_number: dict[int, E]


@dataclass(frozen=True, slots=True)
class _SnapshotNumberedItem(Generic[E]):
    prefix: str
    number: int
    width: int
    item: E


class _SnapshotRecallEnum(enum.Enum):
    _item_id_to_item: ClassVar[dict[int, Self]]
    _item_order: ClassVar[dict[Self, int]]
    _groups_by_token: ClassVar[dict[str, _SnapshotRecallGroup[Self]]]
    _groups_by_item: ClassVar[dict[Self, tuple[_SnapshotRecallGroup[Self], ...]]]
    _numbered_item_by_item: ClassVar[dict[Self, _SnapshotNumberedItem[Self]]]

    def __init_subclass__(cls):
        super().__init_subclass__()

        items: tuple[Self, ...] = tuple(cls)
        token_items: dict[str, list[Self]] = {}
        numbered_items_by_prefix: dict[str, list[_SnapshotNumberedItem[Self]]] = {}

        def _parse_numbered_name(name: str):
            left, sep, right = name.rpartition("_")
            if sep != "_" or not right.isdigit():
                return None
            return f"{left}_", int(right), len(right)

        def _iter_prefix_tokens(name: str):
            parts = name.split("_")
            for i in range(1, len(parts)):
                yield "_".join(parts[:i])

        all_items_alias = cls._all_items_alias()
        for item in items:
            token_items.setdefault(all_items_alias, []).append(item)
            token_items.setdefault(item.name, []).append(item)
            for token in _iter_prefix_tokens(item.name):
                token_items.setdefault(token, []).append(item)

            split = _parse_numbered_name(item.name)
            if split is None:
                continue
            prefix, num, width = split
            numbered = _SnapshotNumberedItem(prefix=prefix, number=num, width=width, item=item)
            numbered_items_by_prefix.setdefault(prefix, []).append(numbered)

        cls._scope_name = all_items_alias.lower()
        if cls._scope_name.startswith("all_"):
            cls._scope_name = cls._scope_name[4:]
        cls._item_order = {item: i for i, item in enumerate(items)}
        cls._item_id_to_item = {item.value: item for item in items}
        cls._numbered_item_by_item = {}
        for numbered_items in numbered_items_by_prefix.values():
            for numbered_item in numbered_items:
                cls._numbered_item_by_item[numbered_item.item] = numbered_item

        cls._groups_by_token = {}
        for token, matched in token_items.items():
            numbered_items = numbered_items_by_prefix.get(token, [])
            numbered_items = sorted(numbered_items, key=lambda numbered: numbered.number)
            if numbered_items:
                cls._groups_by_token[token] = _SnapshotRecallNumberedGroup(
                    token=token,
                    items=tuple(matched),
                    item_by_number={numbered.number: numbered.item for numbered in numbered_items},
                )
            else:
                cls._groups_by_token[token] = _SnapshotRecallGroup(token=token, items=tuple(matched))

        cls._groups_by_item = {}
        for item in items:
            groups = [group for group in cls._groups_by_token.values() if item in group.items_set]
            groups.sort(key=lambda group: -len(group.items))
            cls._groups_by_item[item] = tuple(groups)

        cls._groups_by_token["*"] = cls._groups_by_token[all_items_alias]

    @classmethod
    @abstractmethod
    def _all_items_alias(cls) -> str: ...

    @classmethod
    def _range(cls, first_item: "_SnapshotRecallEnum", first: int, last: int):
        return {cls(first_item.value + (i - 1)) for i in range(first, last + 1)}

    @classmethod
    def get_item_for_id(cls, id: int):
        return cls._item_id_to_item.get(id)

    @classmethod
    def get_items_description(cls):
        return " ".join(cls._format_item_names_with_ranges(list(cls)))

    @classmethod
    def _format_item_names_with_ranges(cls, items: list[Self | str]):
        formatted: list[str] = []
        i = 0
        while i < len(items):
            item = items[i]
            if isinstance(item, str):
                formatted.append(item)
                i += 1
                continue

            numbered = cls._numbered_item_by_item.get(item)
            if numbered is None:
                formatted.append(item.name)
                i += 1
                continue

            start_num = numbered.number
            end_num = start_num
            j = i + 1
            while j < len(items):
                next_item = items[j]
                if isinstance(next_item, str):
                    break
                next_numbered = cls._numbered_item_by_item.get(next_item)
                if next_numbered is None:
                    break
                if (
                    next_numbered.prefix != numbered.prefix
                    or next_numbered.width != numbered.width
                    or next_numbered.number != end_num + 1
                ):
                    break
                end_num = next_numbered.number
                j += 1

            if end_num > start_num:
                left = f"{numbered.prefix}{start_num:0{numbered.width}d}"
                right = f"{end_num:0{numbered.width}d}"
                formatted.append(f"{left}..{right}")
            else:
                formatted.append(item.name)
            i = j

        return formatted

    @classmethod
    def parse_items(cls, value: str) -> list[Self]:
        if not value:
            return list()

        def _required_group(prefix: str, original_token: str):
            result = cls._groups_by_token.get(prefix)
            if result is None:
                raise ValueError(f"Unknown {cls._scope_name} snapshot recall scope token: '{original_token}'")
            return result

        selected: list[Self] = list()
        for token in value.split():
            token = token.upper()
            if ".." in token:
                left_token, right_token = token.split("..", 1)
                left_item = cls.__members__.get(left_token)
                if left_item is None:
                    raise ValueError(f"Unknown {cls._scope_name} snapshot recall scope token: '{left_token}'")
                left_numbered = cls._numbered_item_by_item.get(left_item)
                if left_numbered is None:
                    raise ValueError(f"Can not parse range '{token}' because left part does not end with _number.")

                numbered_group = cls._groups_by_token[left_numbered.prefix]
                assert isinstance(numbered_group, _SnapshotRecallNumberedGroup)

                right_item = cls.__members__.get(right_token)
                if right_item is None:
                    right_num = int(right_token)
                    if right_num not in numbered_group.item_by_number:
                        raise ValueError(
                            f"Unknown {cls._scope_name} snapshot recall range right bound number: '{right_num}' for prefix '{left_numbered.prefix}'."
                        )
                else:
                    right_numbered = cls._numbered_item_by_item.get(right_item)
                    if right_numbered is None:
                        raise ValueError(
                            f"Can not parse range '{token}' because right bound '{right_token}' is not a numbered item."
                        )
                    if left_numbered.prefix != right_numbered.prefix:
                        raise ValueError(
                            f"Can not parse range '{token}' because left bound text prefix '{left_numbered.prefix}' doesn't match right bound text prefix '{right_numbered.prefix}'."
                        )
                    right_num = right_numbered.number

                start = min(left_numbered.number, left_numbered.number)
                end = max(left_numbered.number, left_numbered.number)
                for number in range(start, end + 1):
                    item = numbered_group.item_by_number.get(number)
                    if item is None:
                        raise ValueError(
                            f"Can not parse range '{token}' because number '{number}' is not valid for prefix '{left_numbered.prefix}'."
                        )
                    selected.append(item)
            else:
                group = _required_group(token, token)
                selected += group.items

        return selected

    @classmethod
    def format_items(cls, selected: Iterable[Self]):
        remaining = set(selected)
        raw_tokens: list[str | Self] = []
        while remaining:
            first_item = min(remaining, key=lambda item: cls._item_order[item])
            best_group: _SnapshotRecallGroup[Self] | None = None
            for group in cls._groups_by_item[first_item]:
                if group.items_set.issubset(remaining):
                    best_group = group
                    break

            assert best_group is not None
            if len(best_group.items) == 1 and best_group.items[0].name == best_group.token:
                raw_tokens.append(best_group.items[0])
            else:
                raw_tokens.append(best_group.token)

            for item in best_group.items:
                remaining.remove(item)

        return cls._format_item_names_with_ranges(raw_tokens)


class SnapshotRecallStrip(_SnapshotRecallEnum):
    FD_CH_01 = 0
    FD_CH_02 = 1
    FD_CH_03 = 2
    FD_CH_04 = 3
    FD_CH_05 = 4
    FD_CH_06 = 5
    FD_CH_07 = 6
    FD_CH_08 = 7
    FD_CH_09 = 8
    FD_CH_10 = 9
    FD_CH_11 = 10
    FD_CH_12 = 11
    FD_CH_13 = 12
    FD_CH_14 = 13
    FD_CH_15 = 14
    FD_CH_16 = 15
    FD_AUX = 16
    FD_FX_RETURN_1 = 17
    FD_FX_RETURN_2 = 18
    FD_FX_RETURN_3 = 19
    FD_FX_RETURN_4 = 20
    BUS_MBUS_1 = 21
    BUS_MBUS_2 = 22
    BUS_MBUS_3 = 23
    BUS_MBUS_4 = 24
    BUS_MBUS_5 = 25
    BUS_MBUS_6 = 26
    BUS_FX_SEND_1 = 27
    BUS_FX_SEND_2 = 28
    BUS_FX_SEND_3 = 29
    BUS_FX_SEND_4 = 30
    BUS_MAIN_LR = 31

    @override
    @classmethod
    def _all_items_alias(cls):
        return "ALL_STRIPS"

    @classmethod
    def channels(cls, first: int = 1, last: int = 16):
        if first < 1 or last > 16:
            raise ValueError(f"Channels valid range is [1, 16], got [{first}, {last}].")
        return cls._range(cls.FD_CH_01, first, last)

    @classmethod
    def fx_returns(cls, first: int = 1, last: int = 4):
        if first < 1 or last > 4:
            raise ValueError(f"Fx returns valid range is [1, 4], got [{first}, {last}].")
        return cls._range(cls.FD_FX_RETURN_1, first, last)

    @classmethod
    def mix_buses(cls, first: int = 1, last: int = 6):
        if first < 1 or last > 6:
            raise ValueError(f"Mix buses valid range is [1, 6], got [{first}, {last}].")
        return cls._range(cls.BUS_MBUS_1, first, last)

    @classmethod
    def fx_sends(cls, first: int = 1, last: int = 4):
        if first < 1 or last > 4:
            raise ValueError(f"Fx sends valid range is [1, 4], got [{first}, {last}].")
        return cls._range(cls.BUS_FX_SEND_1, first, last)

    @classmethod
    def all_feeds(cls):
        return cls.channels() | {SnapshotRecallStrip.FD_AUX} | cls.fx_returns()

    @classmethod
    def all_buses(cls):
        return cls.mix_buses() | cls.fx_sends() | {SnapshotRecallStrip.BUS_MAIN_LR}

    @classmethod
    def all(cls):
        return cls.all_feeds() | cls.all_buses()


class SnapshotRecallParameter(_SnapshotRecallEnum):
    SOURCE = 40
    INPUT = 41
    CONFIG = 42  # TODO: does in include gate? low cut? insert? automix, dca, mute groups?
    EQ = 43
    DYNAMICS = 44
    FADER_PAN = (
        55  # TODO: this probably SEND_MAIN_LR for feeds and master fader for buses. so should it be in sends section?
    )
    MUTE = 56
    SEND_BUS_1 = 45
    SEND_BUS_2 = 46
    SEND_BUS_3 = 47
    SEND_BUS_4 = 48
    SEND_BUS_5 = 49
    SEND_BUS_6 = 50
    SEND_FX_1 = 51
    SEND_FX_2 = 52
    SEND_FX_3 = 53
    SEND_FX_4 = 54

    @override
    @classmethod
    def _all_items_alias(cls):
        return "ALL_PARAMS"

    @classmethod
    def send_buses(cls, first: int = 1, last: int = 6):
        if first < 1 or last > 6:
            raise ValueError(f"Send to mix buses valid range is [1, 6], got [{first}, {last}].")
        return cls._range(cls.SEND_BUS_1, first, last)

    @classmethod
    def send_fxes(cls, first: int = 1, last: int = 4):
        if first < 1 or last > 4:
            raise ValueError(f"Send to fxes valid range is [1, 4], got [{first}, {last}].")
        return cls._range(cls.SEND_FX_1, first, last)

    @classmethod
    def all_sends(cls):
        return cls.send_buses() | cls.send_fxes()

    @classmethod
    def all(cls):
        return {
            cls.SOURCE,
            cls.INPUT,
            cls.CONFIG,
            cls.EQ,
            cls.DYNAMICS,
            cls.FADER_PAN,
            cls.MUTE,
        } | cls.all_sends()


class SnapshotRecallGlobalSetting(_SnapshotRecallEnum):
    DCA_1 = 32
    DCA_2 = 33
    DCA_3 = 34
    DCA_4 = 35
    FXSLOT_1 = 36
    FXSLOT_2 = 37
    FXSLOT_3 = 38
    FXSLOT_4 = 39
    MIXER_IN_OUT = 57  # TODO: is it both input and output routing?
    MIXER_CONFIG = 58  # TODO: what is this exactly? probably audio and monitoring config

    @override
    @classmethod
    def _all_items_alias(cls):
        return "ALL_GLOBALS"

    @classmethod
    def dcas(cls, first: int = 1, last: int = 4):
        if first < 1 or last > 4:
            raise ValueError(f"Dca valid range is [1, 4], got [{first}, {last}].")
        return cls._range(cls.DCA_1, first, last)

    @classmethod
    def fx_slots(cls, first: int = 1, last: int = 4):
        if first < 1 or last > 4:
            raise ValueError(f"Fx slots valid range is [1, 4], got [{first}, {last}].")
        return cls._range(cls.FXSLOT_1, first, last)

    @classmethod
    def all(cls):
        return cls.dcas() | cls.fx_slots() | {cls.MIXER_IN_OUT, cls.MIXER_CONFIG}


SNAPSHOT_RECALL_SCOPES_COUNT = 59

RECALL_SCOPE_DESCRIPTION = f"""
Scope that will be applied to the mixer state during the snapshot loading. Doesn't impact saving, save is always complete.

Format is `<strips> | <params> | <globals>` with exactly three `|`-separated sections, that could be empty.
Each section consists of space-separated scope elements of corresponding kind (see full list below).
Prefixes of these elements could also be used (that followed by _ in the original name) to include whole prefixed group, for example `FD` will include all feeds, `FD_CH` will include all channels.
Ranges also could be used for numbered elements using `..` separator, for example `FD_CH_05..12`.
And for each element kind (each section) there is a special group name, that includes all the elements of this kind: {SnapshotRecallStrip._all_items_alias()}, {SnapshotRecallParameter._all_items_alias()}, {SnapshotRecallGlobalSetting._all_items_alias()}

For each strip in <strips> only selected <params> will be loaded, so the result is a cartesian multiplication.
<globals> are on their own and don't depend on <strips> or <params>.

Strip elements: {SnapshotRecallStrip.get_items_description()}
Parameter elements: {SnapshotRecallParameter.get_items_description()}
Global elements: {SnapshotRecallGlobalSetting.get_items_description()}
"""


class SnapshotRecallScope(CodecType):
    def __init__(
        self,
        strips: Iterable[SnapshotRecallStrip],
        parameters: Iterable[SnapshotRecallParameter],
        globals: Iterable[SnapshotRecallGlobalSetting],
    ):
        self.strips = frozenset(strips)
        self.parameters = frozenset(parameters)
        self.globals = frozenset(globals)

    @classmethod
    def parse(cls, value: str):
        sections = [section.strip() for section in value.split("|")]
        if len(sections) != 3:
            raise ValueError(
                "Snapshot recall scope must contain exactly three `|`-separated sections: for strips, parameters and globals."
            )

        strips = SnapshotRecallStrip.parse_items(sections[0])
        parameters = SnapshotRecallParameter.parse_items(sections[1])
        globals_ = SnapshotRecallGlobalSetting.parse_items(sections[2])

        return cls(strips, parameters, globals_)

    @override
    def __str__(self):
        strips = " ".join(SnapshotRecallStrip.format_items(self.strips))
        parameters = " ".join(SnapshotRecallParameter.format_items(self.parameters))
        globals_ = " ".join(SnapshotRecallGlobalSetting.format_items(self.globals))

        return f"{strips} | {parameters} | {globals_}"

    @override
    def encode(self, instance: MixerNode):
        result = [0] * SNAPSHOT_RECALL_SCOPES_COUNT
        for i in self.strips | self.parameters | self.globals:
            result[i.value] = True

        return "".join("+" if item else "-" for item in result)

    @classmethod
    def decode(cls, raw: Any, instance: MixerNode):
        raw = str(raw)
        if len(raw) != SNAPSHOT_RECALL_SCOPES_COUNT:
            raise ValueError(
                f"Snapshot recall flag string len must be exactly {SNAPSHOT_RECALL_SCOPES_COUNT}, got {len(raw)}"
            )

        strips: list[SnapshotRecallStrip] = []
        parameters: list[SnapshotRecallParameter] = []
        globals: list[SnapshotRecallGlobalSetting] = []
        for i, c in enumerate(raw):
            if c != "+":
                continue

            if (item := SnapshotRecallStrip._item_id_to_item.get(i)) is not None:
                strips.append(item)
            elif (item := SnapshotRecallParameter._item_id_to_item.get(i)) is not None:
                parameters.append(item)
            else:
                assert SnapshotRecallGlobalSetting._item_id_to_item.get(i)
                globals.append(SnapshotRecallGlobalSetting(i))

        return cls(strips, parameters, globals)

    @classmethod
    def make_node_descriptor(cls, parent: MixerNode, writable: bool):
        return MixerPropDescriptor(type="str", description=RECALL_SCOPE_DESCRIPTION)


class Snapshot(MixerNode):
    name = StringProperty("name", max_len=31)
    _recall_scope_string = StringProperty(
        "scope",
        min_len=SNAPSHOT_RECALL_SCOPES_COUNT,
        max_len=SNAPSHOT_RECALL_SCOPES_COUNT,
        description="String of +/- for each recall option.",
    )
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

    load = IntProperty(
        "load",
        1,
        SNAPSHOT_SLOTS_COUNT,
        description="Setting a snapshot slot number to this property will lead to loading the snapshot into the mixer state. Reading this property is useless.",
    )  # non-readable

    name_to_save = StringProperty(
        "name",
        max_len=31,
        description="Set it only before saving the snapshot. To read the name of particular snapshot see slots.",
    )
    save = IntProperty(
        "save",
        1,
        SNAPSHOT_SLOTS_COUNT,
        description="Setting a snapshot slot number to this property will lead to saving current mixer state to that slot using snapshot name from `name_to_save`. Reading this property is useless.",
    )  # non-readable

    delete = IntProperty(
        "delete",
        1,
        SNAPSHOT_SLOTS_COUNT,
        description="Setting a snapshot slot number to this property will lead to deleting snapshot from this slot and clearing the slot. Reading this property is useless.",
    )  # non-readable
