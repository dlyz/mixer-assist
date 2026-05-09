import abc
import math
from enum import IntEnum
from typing import Any, TypeVar, override
from ..nodes_base import MixerNode, MixerPropDescriptor, MixerProperty


T = TypeVar("T")
E = TypeVar("E", bound=IntEnum)


class SimpleMixerProperty(MixerProperty[T], abc.ABC):
    value_type: type[T]

    def __init__(
        self,
        path_segment: str,
        *,
        writable: bool = True,
        units: str | None = None,
        constraints: str | None = None,
        description: str | None = None,
    ):
        super().__init__(path_segment, writable=writable)
        self.descriptor = MixerPropDescriptor(
            type=self.value_type.__name__,
            units=units,
            constraints=constraints,
            description=description,
        )

    @override
    def make_node_descriptor(self, parent: MixerNode) -> MixerPropDescriptor:
        return self.descriptor

    @override
    def parse(self, value: str) -> T:
        return self.value_type(value)  # pyright: ignore[reportCallIssue]

    @override
    def decode(self, raw: Any, instance: MixerNode) -> T:
        return self.value_type(raw)  # pyright: ignore[reportCallIssue]

    @override
    def encode(self, value: T, instance: MixerNode) -> Any:
        return value


class StringProperty(SimpleMixerProperty[str]):
    value_type = str


class BoolProperty(SimpleMixerProperty[bool]):
    value_type = bool

    @override
    def parse(self, value: str) -> bool:
        text = value.strip().lower()
        if text in {"1", "true", "on", "yes"}:
            return True
        if text in {"0", "false", "off", "no"}:
            return False
        raise ValueError(f"invalid boolean value {value!r}")

    @override
    def decode(self, raw: Any, instance: MixerNode) -> bool:
        return bool(int(raw))

    @override
    def encode(self, value: bool, instance: MixerNode) -> int:
        return 1 if value else 0


class InvertedBoolProperty(BoolProperty):
    @override
    def decode(self, raw: Any, instance: MixerNode) -> bool:
        return not bool(int(raw))

    @override
    def encode(self, value: bool, instance: MixerNode) -> int:
        return 0 if value else 1


class EnumIntProperty(MixerProperty[E]):
    def __init__(
        self,
        path_segment: str,
        enum_type: type[E],
        *,
        writable: bool = True,
        description: str | None = None,
    ):
        super().__init__(path_segment, writable=writable)
        self.enum_type = enum_type

        if hasattr(enum_type, "_LABELS"):
            self.labels: dict[E, str] | None = getattr(enum_type, "_LABELS")
            if not isinstance(self.labels, dict):
                raise ValueError("_LABELS property of the enum class must be a dict[enum_type, str]")
            self.casefold_name_to_value = {label.casefold(): value for value, label in self.labels.items()}
        else:
            self.labels = None
            self.casefold_name_to_value = {member.name.casefold(): member for member in self.enum_type}

        enum_names = ", ".join(self.format_value(member) for member in self.enum_type)
        self.descriptor = MixerPropDescriptor(
            type="enum",
            constraints=f"one of: {enum_names}",
            description=description,
        )

    @override
    def make_node_descriptor(self, parent: MixerNode) -> MixerPropDescriptor:
        return self.descriptor

    @override
    def format_value(self, value: E) -> str:
        if self.labels is not None:
            return self.labels[value]
        else:
            return value.name

    @override
    def parse(self, value: str) -> E:
        text = value.strip()
        member = self.casefold_name_to_value.get(text.casefold())
        if member is None:
            raise ValueError(f"invalid enum value {value!r}, expected {self.descriptor.constraints}")
        return member

    @override
    def decode(self, raw: Any, instance: MixerNode) -> E:
        return self.enum_type(int(raw))

    @override
    def encode(self, value: E, instance: MixerNode) -> int:
        return int(value)


class FloatProperty(MixerProperty[float]):
    def __init__(
        self,
        path_segment: str,
        minimum: float,
        maximum: float,
        *,
        writable: bool = True,
        decimals: int | None = None,
        units: str | None = None,
        extra_constraints: str = "",
        description: str | None = None,
    ):
        if minimum >= maximum:
            raise ValueError(f"minimum must be less than maximum, got {minimum} >= {maximum}")
        super().__init__(path_segment, writable=writable)
        self.minimum = minimum
        self.maximum = maximum
        self.decimals = decimals
        self.descriptor = MixerPropDescriptor(
            type="float",
            units=units,
            constraints=self.make_range_constraints(minimum, maximum, decimals=decimals) + extra_constraints,
            description=description,
        )

    @override
    def make_node_descriptor(self, parent: MixerNode) -> MixerPropDescriptor:
        return self.descriptor

    @override
    def parse(self, value: str) -> float:
        return float(value.strip())

    @override
    def format_value(self, value: float) -> str:
        return format(value, f".{self.decimals}f")

    @override
    def decode(self, raw: Any, instance: MixerNode) -> float:
        raw_value = float(raw)
        if not 0.0 <= raw_value <= 1.0:
            raise ValueError(f"{self.name} raw value must be in range 0.0..1.0, got {raw_value}")
        value = self._do_decode(raw_value)
        if self.decimals is not None:
            return smart_round(value, self.decimals)
        return value

    @abc.abstractmethod
    def _do_decode(self, raw_value: float) -> float:
        raise NotImplementedError()

    @override
    def encode(self, value: float, instance: MixerNode) -> float:
        numeric_value = float(value)
        if not self.minimum <= numeric_value <= self.maximum:
            raise ValueError(f"{self.name} must be in range {self.minimum}..{self.maximum}, got {numeric_value}")
        return self._do_encode(numeric_value)

    @abc.abstractmethod
    def _do_encode(self, value: float) -> float:
        raise NotImplementedError()

    @staticmethod
    def make_range_constraints(minimum: float, maximum: float, decimals: int | None = None):
        if decimals is not None:
            return f"in range [{minimum:.{decimals}f}, {maximum:.{decimals}f}]"
        else:
            return f"in range [{minimum}, {maximum}]"


def smart_round(value: float, decimals: int):
    if decimals < 4:
        # rounding to 4 digits to turn 0.574999988079071... into 0.5750
        value = round(value, 4)

        from decimal import Decimal, ROUND_HALF_UP

        # float to string to remove error
        d = Decimal(str(value))

        precision = Decimal("10") ** -decimals
        return float(d.quantize(precision, rounding=ROUND_HALF_UP))
    else:
        return round(value, decimals)


class LinearFloatProperty(FloatProperty):
    @override
    def _do_decode(self, raw_value: float) -> float:
        return self.minimum + (self.maximum - self.minimum) * raw_value

    @override
    def _do_encode(self, value: float) -> float:
        return (value - self.minimum) / (self.maximum - self.minimum)


class LogFloatProperty(FloatProperty):
    def __init__(
        self,
        path_segment: str,
        minimum: float,
        maximum: float,
        *,
        writable: bool = True,
        decimals: int | None = None,
        units: str | None = None,
        description: str | None = None,
    ):
        if minimum <= 0 or maximum <= 0:
            raise ValueError(f"log range values must be positive, got {minimum}..{maximum}")
        super().__init__(
            path_segment,
            minimum,
            maximum,
            writable=writable,
            decimals=decimals,
            units=units,
            description=description,
        )
        self._scale = math.log(self.maximum / self.minimum)

    @override
    def _do_decode(self, raw_value: float) -> float:
        return self.minimum * math.exp(self._scale * raw_value)

    @override
    def _do_encode(self, value: float) -> float:
        return math.log(value / self.minimum) / self._scale


class InvertedLogFloatProperty(LogFloatProperty):
    @override
    def _do_decode(self, raw_value: float) -> float:
        return self.minimum * math.exp(self._scale * (1.0 - raw_value))

    @override
    def _do_encode(self, value: float) -> float:
        return 1.0 - (math.log(value / self.minimum) / self._scale)
