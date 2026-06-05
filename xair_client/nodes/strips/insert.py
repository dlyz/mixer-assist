from enum import IntEnum

from ..core.base_types import MixerNode
from ..core.primitive_props import BoolProperty, EnumIntProperty


class InsertFxSlot(IntEnum):
    OFF = 0
    FX1A = 1
    FX1B = 2
    FX2A = 3
    FX2B = 4
    FX3A = 5
    FX3B = 6
    FX4A = 7
    FX4B = 8

    @property
    def num(self):
        return -1 if self == InsertFxSlot.OFF else (self.value - 1) // 2 + 1

    @property
    def side(self):
        return -1 if self == InsertFxSlot.OFF else (self.value - 1) % 2

    @staticmethod
    def from_num_side(num: int, side: int):
        if num == -1:
            return InsertFxSlot.OFF
        if not 1 <= num <= 4:
            raise ValueError(f"{num} fx num is invalid for {InsertFxSlot.__name__}")
        if not 0 <= side <= 1:
            raise ValueError(f"{side} fx side is invalid for {InsertFxSlot.__name__}, use 0 for A and 1 for B.")
        return InsertFxSlot(1 + (num - 1) * 2 + side)


class StereoInsertFxSlot(IntEnum):
    OFF = 0
    FX1 = 1
    FX2 = 2
    FX3 = 3
    FX4 = 4

    @property
    def num(self):
        return -1 if self == StereoInsertFxSlot.OFF else self.value

    @staticmethod
    def from_num(num: int):
        if num == -1:
            return StereoInsertFxSlot.OFF
        if not 1 <= num <= 4:
            raise ValueError(f"{num} fx num is invalid for {StereoInsertFxSlot.__name__}")
        return StereoInsertFxSlot(num)


class StripInsert(MixerNode):
    """Effect insert settings."""

    enabled = BoolProperty("on")
    "For insert to take effect it is also required to activate insert mode on fx itself."

    fx_slot = EnumIntProperty("sel", InsertFxSlot)
