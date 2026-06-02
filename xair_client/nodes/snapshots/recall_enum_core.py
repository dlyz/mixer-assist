from dataclasses import dataclass, field

import enum
from abc import abstractmethod
from typing import ClassVar, Generic, Iterable, Self, TypeVar

E = TypeVar("E", bound="_SnapshotRecallEnum")


@dataclass(frozen=True, slots=True)
class _SnapshotNumberedItem(Generic[E]):
    prefix: str
    number: int
    width: int
    item: E


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
