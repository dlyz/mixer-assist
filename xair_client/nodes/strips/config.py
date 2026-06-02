from enum import IntEnum

from ..core.base_types import MixerNode
from ..core.primitive_props import EnumIntProperty, StringProperty


class StripColor(IntEnum):
    OFF = 0
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4
    MAGENTA = 5
    CYAN = 6
    WHITE = 7
    OFF_INVERTED = 8
    RED_INVERTED = 9
    GREEN_INVERTED = 10
    YELLOW_INVERTED = 11
    BLUE_INVERTED = 12
    MAGENTA_INVERTED = 13
    CYAN_INVERTED = 14
    WHITE_INVERTED = 15


class StripConfig(MixerNode):
    """Strip name and color."""

    name = StringProperty("name", max_len=12)
    color = EnumIntProperty("color", StripColor)
