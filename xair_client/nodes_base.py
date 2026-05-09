from abc import ABC, abstractmethod
import dataclasses
from typing import AbstractSet, Any, Callable, Generic, Iterable, TypeVar, overload, override

from .mixer_models import MixerModel

from .client import XAirClient


@dataclasses.dataclass(frozen=True, kw_only=True)
class MixerNodeDescriptor:
    description: str | None = None


@dataclasses.dataclass(frozen=True)
class MixerPropDescriptor(MixerNodeDescriptor):
    type: str
    units: str | None = None
    constraints: str | None = None


class MixerNode:
    description: str | None = None
    disabled: bool = False
    disabled_children_names: frozenset[str] = frozenset()

    def __init__(
        self,
        client: XAirClient,
        base_path: str,
        *,
        description: str | None = None,
        description_suffix: str | None = None,
    ):
        self._client = client
        self.base_path = base_path
        if description is not None:
            self.description = description
        if description_suffix is not None:
            if self.description:
                self.description = self.description + description_suffix
            else:
                self.description = description_suffix.strip()

    @property
    def mixer_model(self) -> MixerModel:
        return self._client.mixer_model

    def relative_path(self, segment: str) -> str:
        if segment.startswith("/"):
            return segment
        if self.base_path.endswith("/"):
            return f"{self.base_path}{segment}"
        return f"{self.base_path}/{segment}"

    @property
    def children(self) -> Iterable[tuple[str, "MixerNode | MixerPropertyNode"]]:
        all_items = {}

        for cls in reversed(self.__class__.__mro__):
            all_items.update(cls.__dict__)

        for attr_name, member in all_items.items():
            if attr_name in self.disabled_children_names:
                continue

            if isinstance(member, MixerNodeFactory):
                child_node: MixerNode = getattr(self, attr_name)
                if not child_node.disabled:
                    yield (attr_name, child_node)
            elif isinstance(member, MixerProperty):
                yield (attr_name, MixerPropertyNode(self, attr_name, member))

    @property
    def descriptor(self):
        return MixerNodeDescriptor(description=self.description)


N = TypeVar("N", bound="MixerNode")


class MixerCollectionNode(MixerNode, Generic[N]):
    item_type: type[N] | None
    item_start: int = 1
    item_path_start: int | None = None
    item_num_width: int = 2

    def __init__(
        self,
        client: XAirClient,
        base_path: str,
        *,
        item_count: int | None = None,
        **kwargs,
    ):
        super().__init__(client, base_path, **kwargs)

        self.item_count = item_count
        self._pre_init()
        if self.item_count is None:
            raise RuntimeError("item_count must be passed to the init or defined by deriving class")

        num_range = range(self.item_start, self.item_start + self.item_count)
        self._names = [self._create_item_name(num) for num in num_range]

        item_path_start = self.item_path_start if self.item_path_start is not None else self.item_start
        self._path_segments = [
            f"{num:0{self.item_num_width}d}" for num in range(item_path_start, item_path_start + self.item_count)
        ]

        self._items = [self._create_item(num=num, path_segment=ps) for num, ps in zip(num_range, self._path_segments)]

    def _pre_init(self):
        pass

    def _create_item_name(self, num: int):
        return f"{num:0{self.item_num_width}d}"

    def _create_item(self, num: int, path_segment: str):
        if self.item_type is None:
            raise NotImplementedError("Specify item_type or implement custom _create_item.")
        return MixerNodeFactory(self.relative_path(path_segment), self.item_type).create_node(self)

    def __getitem__(self, index: int) -> N:
        first = self.item_start
        last = first + len(self._items) - 1
        if index < self.item_start or index > last:
            raise IndexError(f"index must be in range {self.item_start}..{last}")

        return self._items[index - self.item_start]

    def __len__(self) -> int:
        assert self.item_count is not None
        return self.item_count

    def __contains__(self, item: N):
        return item in self._items

    @property
    @override
    def children(self):
        yield from super().children

        for name, child in zip(self._names, self._items):
            if child.disabled or name in self.disabled_children_names:
                continue
            yield (name, child)


T = TypeVar("T")


# this class is not required, it could be a part of MixerProp
# but we use it so that when we need a field of MixerProp type,
# the type checker won't confuse it with python descriptor.
class MixerPropertyBase(ABC, Generic[T]):
    @abstractmethod
    def parse(self, value: str) -> T:
        raise NotImplementedError

    def format_value(self, value: T) -> str:
        return str(value)

    @abstractmethod
    def decode(self, raw: Any, instance: MixerNode) -> T:
        raise NotImplementedError

    @abstractmethod
    def encode(self, value: T, instance: MixerNode) -> Any:
        raise NotImplementedError

    @abstractmethod
    def make_node_descriptor(self, parent: MixerNode) -> MixerPropDescriptor:
        raise NotImplementedError


class MixerProperty(MixerPropertyBase[T], Generic[T]):
    def __init__(self, path_segment: str, *, writable: bool = True):
        self.path_segment = path_segment
        self.writable = writable
        self.name = path_segment

    def __set_name__(self, owner: type[MixerNode], name: str):
        self.name = name

    @overload
    def __get__(self, instance: None, owner: type[MixerNode]) -> "MixerProperty[T]": ...

    @overload
    def __get__(self, instance: MixerNode, owner: type[MixerNode]) -> T: ...

    def __get__(self, instance: MixerNode | None, owner: type[MixerNode]) -> "MixerProperty[T] | T":
        if instance is None:
            return self
        path = instance.relative_path(self.path_segment)
        if self.name in instance.disabled_children_names:
            raise RuntimeError(
                f"Property '{self.name}' is disabled and probably could not be accessed (internal path: '{path}')."
            )
        raw = instance._client.read(path)
        return self.decode(raw, instance)

    def __set__(self, instance: MixerNode, value: T):
        path = instance.relative_path(self.path_segment)
        if not self.writable:
            raise AttributeError(f"Property '{self.name}' is read-only (internal path: '{path}').")
        if self.name in instance.disabled_children_names:
            raise RuntimeError(
                f"Property '{self.name}' is disabled and probably could not be accessed (internal path: '{path}')."
            )
        encoded = self.encode(value, instance)
        instance._client.write(path, encoded)


@dataclasses.dataclass
class MixerPropertyNode:
    parent: MixerNode
    name: str
    prop: MixerPropertyBase

    @property
    def disabled(self):
        return self.name in self.parent.disabled_children_names

    @property
    def descriptor(self):
        return self.prop.make_node_descriptor(self.parent)

    @property
    def value(self):
        return getattr(self.parent, self.name)

    @value.setter
    def value(self, value):
        setattr(self.parent, self.name, value)

    @property
    def formatted_value(self):
        return self.prop.format_value(self.value)

    @formatted_value.setter
    def formatted_value(self, value: str):
        self.value = self.prop.parse(value)


class MixerNodeFactory(Generic[N]):
    transient = False

    def __init__(
        self,
        path_segment: str,
        node_type: type[N] | None,
        *,
        description: str | None = None,
        description_suffix: str | None = None,
        kwargs: dict[str, Any] | None = None,
        kwargs_factory: Callable[[MixerNode], dict[str, Any]] | None = None,
    ):
        self.path_segment = path_segment
        self.node_type = node_type
        self.description = description
        self.description_suffix = description_suffix
        self.kwargs = kwargs or {}
        self.kwargs_factory = kwargs_factory
        self.name = path_segment

    def __set_name__(self, owner: type[MixerNode], name: str):
        self.name = name

    @overload
    def __get__(self, instance: None, owner: type[MixerNode]) -> "MixerNodeFactory[N]": ...

    @overload
    def __get__(self, instance: MixerNode, owner: type[MixerNode]) -> N: ...

    def __get__(self, instance: MixerNode | None, owner: type[MixerNode]) -> "MixerNodeFactory[N] | N":
        if instance is None:
            return self

        node = self.create_node(instance)
        if not self.transient:
            setattr(instance, self.name, self.create_node(instance))
        return node

    def _get_node_type(self, parent: MixerNode):
        if self.node_type is None:
            raise NotImplementedError("Pass node_type to __init__ or override _get_node_type or create_node")
        return self.node_type

    def create_node(self, parent: MixerNode) -> N:
        node_type = self._get_node_type(parent)

        child_kwargs = {
            "description": self.description,
            "description_suffix": self.description_suffix,
            **self.kwargs,
        }
        if self.kwargs_factory is not None:
            child_kwargs.update(self.kwargs_factory(parent))
        return node_type(parent._client, parent.relative_path(self.path_segment), **child_kwargs)
