from typing import Any, Iterable, override

from ..core.base_types import MixerNode, MixerPropDescriptor
from ..core.codec_type_prop import CodecType
from .recall_enum_core import _SnapshotRecallEnum


class SnapshotRecallStrip(_SnapshotRecallEnum):
    CS_CH_01 = 0
    CS_CH_02 = 1
    CS_CH_03 = 2
    CS_CH_04 = 3
    CS_CH_05 = 4
    CS_CH_06 = 5
    CS_CH_07 = 6
    CS_CH_08 = 7
    CS_CH_09 = 8
    CS_CH_10 = 9
    CS_CH_11 = 10
    CS_CH_12 = 11
    CS_CH_13 = 12
    CS_CH_14 = 13
    CS_CH_15 = 14
    CS_CH_16 = 15
    CS_AUX = 16
    CS_FX_RETURN_1 = 17
    CS_FX_RETURN_2 = 18
    CS_FX_RETURN_3 = 19
    CS_FX_RETURN_4 = 20
    BS_BUS_1 = 21
    BS_BUS_2 = 22
    BS_BUS_3 = 23
    BS_BUS_4 = 24
    BS_BUS_5 = 25
    BS_BUS_6 = 26
    BS_FX_SEND_1 = 27
    BS_FX_SEND_2 = 28
    BS_FX_SEND_3 = 29
    BS_FX_SEND_4 = 30
    BS_MAIN_LR = 31

    @override
    @classmethod
    def _all_items_alias(cls):
        return "ALL_STRIPS"

    @classmethod
    def channels(cls, first: int = 1, last: int = 16):
        if first < 1 or last > 16:
            raise ValueError(f"Channels valid range is [1, 16], got [{first}, {last}].")
        return cls._range(cls.CS_CH_01, first, last)

    @classmethod
    def fx_returns(cls, first: int = 1, last: int = 4):
        if first < 1 or last > 4:
            raise ValueError(f"Fx returns valid range is [1, 4], got [{first}, {last}].")
        return cls._range(cls.CS_FX_RETURN_1, first, last)

    @classmethod
    def buses(cls, first: int = 1, last: int = 6):
        if first < 1 or last > 6:
            raise ValueError(f"Buses valid range is [1, 6], got [{first}, {last}].")
        return cls._range(cls.BS_BUS_1, first, last)

    @classmethod
    def fx_sends(cls, first: int = 1, last: int = 4):
        if first < 1 or last > 4:
            raise ValueError(f"Fx sends valid range is [1, 4], got [{first}, {last}].")
        return cls._range(cls.BS_FX_SEND_1, first, last)

    @classmethod
    def channel_strips(cls):
        return cls.channels() | {SnapshotRecallStrip.CS_AUX} | cls.fx_returns()

    @classmethod
    def bus_strips(cls):
        return cls.buses() | cls.fx_sends() | {SnapshotRecallStrip.BS_MAIN_LR}

    @classmethod
    def all(cls):
        return cls.channel_strips() | cls.bus_strips()


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


RECALL_SCOPE_DESCRIPTION = f"""
Scope that will be applied to the mixer state during the snapshot loading. Doesn't impact saving, save is always complete.

Format is `<strips> | <params> | <globals>` with exactly three `|`-separated sections, that could be empty.
Each section consists of space-separated scope elements of corresponding kind (see full list below).
Prefixes of these elements could also be used (that followed by _ in the original name) to include whole prefixed group, for example `CS` will include all channel strips, `CS_CH` will include all channels.
Ranges also could be used for numbered elements using `..` separator, for example `CS_CH_05..12`.
And for each element kind (each section) there is a special group name, that includes all the elements of this kind: {SnapshotRecallStrip._all_items_alias()}, {SnapshotRecallParameter._all_items_alias()}, {SnapshotRecallGlobalSetting._all_items_alias()}

For each strip in <strips> only selected <params> will be loaded, so the result is a cartesian multiplication.
<globals> are on their own and don't depend on <strips> or <params>.

Strip elements: {SnapshotRecallStrip.get_items_description()}
Parameter elements: {SnapshotRecallParameter.get_items_description()}
Global elements: {SnapshotRecallGlobalSetting.get_items_description()}
"""
SNAPSHOT_RECALL_SCOPES_COUNT = 59


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
    def make_node_descriptor(cls, parent: MixerNode):
        return MixerPropDescriptor(type="str", description=RECALL_SCOPE_DESCRIPTION)
