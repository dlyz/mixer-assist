from abc import ABC, abstractmethod
import dataclasses
import enum
from typing import Any, Callable, Generic, Iterable, Mapping, Protocol, TypeVar, overload, override

from frozendict import frozendict

from ...attribure_docs import get_class_attribute_docs

from ...mixer_models import MixerModel

from ...client import XAirClient


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
    property_descriptions: frozendict[str, str] = frozendict()

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        if cls.description is None:
            if cls.__doc__:
                class_doc = cls.__doc__.strip()
                if class_doc:
                    cls.description = class_doc

        attr_docs = get_class_attribute_docs(cls)
        attr_docs.update(cls.property_descriptions)
        cls.property_descriptions = frozendict(attr_docs)

    def __init__(
        self,
        client: XAirClient,
        base_address: str,
        context: frozendict = frozendict(),
        *,
        description: str | None = None,
        description_suffix: str | None = None,
    ):
        self.client = client
        if base_address.endswith("/"):
            base_address = base_address[:-1]
        self.base_address = base_address
        self.context = context
        self.disabled_properties: frozenset[str] = frozenset()

        if description is not None:
            self.description = description

        if description_suffix is not None:
            if self.description:
                self.description = self.description + description_suffix
            else:
                self.description = description_suffix.strip()

    @property
    def mixer_model(self) -> MixerModel:
        return self.client.mixer_model

    def relative_address(self, segment: str) -> str:
        if not segment:
            return self.base_address
        if segment.startswith("/"):
            return segment
        return f"{self.base_address}/{segment}"

    @property
    def children(self) -> Iterable[tuple[str, "MixerNode | MixerPropertyNode"]]:
        all_items: dict[str, Any] = {}

        for cls in reversed(self.__class__.__mro__):
            all_items.update(cls.__dict__)

        for attr_name, member in all_items.items():
            if attr_name.startswith("_"):
                continue

            if isinstance(member, MixerNodeFactory):
                child_node: MixerNode = getattr(self, attr_name)
                yield (attr_name, child_node)
            elif isinstance(member, MixerProperty):
                if attr_name not in self.disabled_properties:
                    yield (attr_name, member.make_node(self))

    @property
    def descriptor(self):
        return MixerNodeDescriptor(description=self.description)

    def to_dict(self):
        result: dict[str, Any] = {}
        for name, child in self.children:
            if isinstance(child, MixerPropertyNode):
                result[name] = child.value
            else:
                result[name] = child.to_dict()
        return result

    def validate_dict(self, values: Mapping[str, Any]):
        if not isinstance(values, Mapping):
            raise ValueError(
                f"Value of type '{type(values)}' is invalid for '{self.__class__}' node. Mapping expected."
            )
        children = dict(self.children)
        for name, value in values.items():
            child = children.get(name)
            if child is None:
                raise ValueError(f"Child '{name}' not found in '{self.__class__}'.")
            elif isinstance(child, MixerPropertyNode):
                child.prop.encode(value, child.parent)
            else:
                child.validate_dict(value)

    def set_values_from_dict(self, values: Mapping[str, Any]):
        self.validate_dict(values)
        for name, child in self.children:
            if name in values:
                value = values[name]
                if isinstance(child, MixerPropertyNode):
                    child.value = value
                else:
                    child.set_values_from_dict(value)


N = TypeVar("N", bound="MixerNode", covariant=True)
NInternal = TypeVar("NInternal", bound="MixerNode")


class MixerCollectionNode(MixerNode, Generic[N]):
    item_type: type[N] | None
    item_start: int = 1
    item_path_start: int | None = None
    item_num_width: int = 2
    item_count: int | None = None

    def __init__(
        self,
        client: XAirClient,
        base_address: str,
        context: frozendict = frozendict(),
        *,
        item_count: int | None = None,
        **kwargs,
    ):
        super().__init__(client, base_address, context, **kwargs)

        if item_count is not None:
            self.item_count = item_count
        self._pre_init()
        if self.item_count is None:
            raise RuntimeError("item_count must be passed to the init or defined by deriving class")

        num_range = range(self.item_start, self.item_start + self.item_count)
        names = [self._create_item_name(num) for num in num_range]

        item_path_start = self.item_path_start if self.item_path_start is not None else self.item_start
        address_segments = [
            f"{num:0{self.item_num_width}d}" for num in range(item_path_start, item_path_start + self.item_count)
        ]

        items = [self._create_item(num=num, address_segment=ps) for num, ps in zip(num_range, address_segments)]
        self._items = [i for i in items if i is not None]
        self._nums = tuple(num for i, num in zip(items, num_range) if i is not None)
        self._names = [name for i, name in zip(items, names) if i is not None]

    def _pre_init(self):
        pass

    def _create_item_name(self, num: int):
        return f"{num:0{self.item_num_width}d}"

    def _create_item_context(self, item_type: type[NInternal], num: int):
        return self.context.set(f"{item_type.__name__}_num", num)

    def _create_item_context_factory(self, item_type: type[NInternal], num: int) -> Callable[[MixerNode], frozendict]:
        return lambda _: self._create_item_context(item_type, num)

    def _create_typed_item(self, item_type: type[NInternal], num: int, address_segment: str) -> NInternal | None:
        return MixerNodeFactory(
            self.relative_address(address_segment),
            item_type,
            context_factory=self._create_item_context_factory(item_type, num),
        ).create_node(self)

    def _create_item(self, num: int, address_segment: str):
        if self.item_type is None:
            raise NotImplementedError(f"Specify item_type or implement custom {self._create_item.__name__}")

        return self._create_typed_item(self.item_type, num=num, address_segment=address_segment)

    def __getitem__(self, num_or_name: int | str) -> N:
        if isinstance(num_or_name, int):
            item_idx = self._nums.index(num_or_name)
        else:
            item_idx = self._names.index(num_or_name)
        return self._items[item_idx]

    def __contains__(self, item):
        return item in self._items

    def __iter__(self):
        return zip(self._nums, self._items)

    @property
    def item_numbers(self) -> Iterable[int]:
        return self._nums

    @property
    @override
    def children(self):
        yield from super().children

        for name, child in zip(self._names, self._items):
            yield (name, child)


T = TypeVar("T")


class MixerPropertyRWMode(enum.Enum):
    ReadWrite = (0,)
    ReadOnly = (1,)
    WriteOnly = (2,)


# this class is not required, it could be a part of MixerProp
# but we use it so that when we need a field of MixerProp type,
# the type checker won't confuse it with python descriptor.
class MixerPropertyBase(ABC, Generic[T]):
    @property
    @abstractmethod
    def rw_mode(self) -> MixerPropertyRWMode:
        raise NotImplementedError

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


class MixerPropertyAddressProvider(Protocol):
    def __call__(self, parent: MixerNode, /) -> str: ...


type MixerPropertyAddressLike = str | MixerPropertyAddressProvider


class MixerProperty(MixerPropertyBase[T], Generic[T]):
    def __init__(
        self, address_segment: MixerPropertyAddressLike, *, rw_mode: MixerPropertyRWMode = MixerPropertyRWMode.ReadWrite
    ):
        if isinstance(address_segment, str):
            self.address_provider: MixerPropertyAddressProvider = lambda parent: parent.relative_address(
                address_segment
            )
        else:
            self.address_provider = address_segment

        self._rw_mode = rw_mode
        self.name = None

    @property
    @override
    def rw_mode(self):
        return self._rw_mode

    def __set_name__(self, owner: type[MixerNode], name: str):
        self.name = name

    @override
    def make_node_descriptor(self, parent: MixerNode) -> MixerPropDescriptor:
        d = self._make_own_node_descriptor(parent)
        if not d.description and self.name:
            descr_from_parent = parent.property_descriptions.get(self.name)
            if descr_from_parent:
                d = dataclasses.replace(d, description=descr_from_parent)
        return d

    def make_node(self, parent: MixerNode):
        if self.name is None:
            raise RuntimeError("Descriptor have to belong to a class in order to create a node.")
        return MixerPropertyNode(parent, self.name, self)

    @abstractmethod
    def _make_own_node_descriptor(self, parent: MixerNode) -> MixerPropDescriptor:
        raise NotImplementedError

    @overload
    def __get__(self, instance: None, owner: type[MixerNode]) -> "MixerProperty[T]": ...

    @overload
    def __get__(self, instance: MixerNode, owner: type[MixerNode]) -> T: ...

    def __get__(self, instance: MixerNode | None, owner: type[MixerNode]) -> "MixerProperty[T] | T":
        if instance is None:
            return self
        address = self.address_provider(instance)
        if self.name in instance.disabled_properties:
            raise RuntimeError(
                f"Property '{self.name}' is disabled and probably could not be accessed (internal path: '{address}')."
            )
        raw = instance.client.read(address)
        return self.decode(raw, instance)

    def __set__(self, instance: MixerNode, value: T):
        address, encoded = self._validate_write(instance, value)
        instance.client.write(address, encoded, is_action=(self.rw_mode == MixerPropertyRWMode.WriteOnly))

    def commit(self, instance: MixerNode, value: T, *, strict_confirm: bool = True):
        address, encoded = self._validate_write(instance, value)
        result = instance.client.commit(
            address,
            encoded,
            strict_confirm=strict_confirm,
            is_action=(self.rw_mode == MixerPropertyRWMode.WriteOnly),
        )
        return self.decode(result, instance)

    def _validate_write(self, instance: MixerNode, value: T):
        address = self.address_provider(instance)
        if self.rw_mode == MixerPropertyRWMode.ReadOnly:
            raise AttributeError(f"Property '{self.name}' is read-only (osc address: '{address}').")
        if self.name in instance.disabled_properties:
            raise RuntimeError(
                f"Property '{self.name}' is disabled and probably could not be accessed (osc address: '{address}')."
            )
        return address, self.encode(value, instance)


@dataclasses.dataclass
class MixerPropertyNode:
    parent: MixerNode
    name: str
    prop: MixerPropertyBase

    @property
    def disabled(self):
        return self.name in self.parent.disabled_properties

    @property
    def descriptor(self):
        return self.prop.make_node_descriptor(self.parent)

    @property
    def value(self):
        return getattr(self.parent, self.name)

    @value.setter
    def value(self, value):
        setattr(self.parent, self.name, value)

    def commit_value(self, value, *, strict_confirm: bool = True):
        assert isinstance(self.prop, MixerProperty)
        return self.prop.commit(self.parent, value, strict_confirm=strict_confirm)

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
        address_segment: str,
        node_type: type[N] | None,
        *,
        context_factory: Callable[[MixerNode], frozendict] | None = None,
        description: str | None = None,
        description_suffix: str | None = None,
        kwargs: dict[str, Any] | None = None,
        kwargs_factory: Callable[[MixerNode], dict[str, Any]] | None = None,
    ):
        self.address_segment = address_segment
        self.node_type = node_type
        self.context_factory = context_factory
        self.description = description
        self.description_suffix = description_suffix
        self.kwargs = kwargs or {}
        self.kwargs_factory = kwargs_factory
        self.name = address_segment

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

    def _get_node_context(self, parent: MixerNode):
        if self.context_factory is not None:
            return self.context_factory(parent)
        else:
            return parent.context

    def create_node(self, parent: MixerNode) -> N:
        node_type = self._get_node_type(parent)
        context = self._get_node_context(parent)

        child_kwargs = {
            "description": self.description,
            "description_suffix": self.description_suffix,
            **self.kwargs,
        }
        if self.kwargs_factory is not None:
            child_kwargs.update(self.kwargs_factory(parent))
        return node_type(
            client=parent.client,
            base_address=parent.relative_address(self.address_segment),
            context=context,
            **child_kwargs,
        )
