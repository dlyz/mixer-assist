from typing import override

from .effects.all import FX_PARAMS_NODE_TYPES_MAP, FxParamsNode, FxType
from ..properties.primitive import BoolProperty, EnumIntProperty
from ..nodes_base import MixerCollectionNode, MixerNode, MixerNodeFactory


class FxParamsNodeProvider(MixerNodeFactory[FxParamsNode]):
    transient = True

    def __init__(
        self,
        path_segment: str,
        *,
        description_suffix: str | None = None,
    ):
        super().__init__(path_segment, None, description_suffix=description_suffix)

    @override
    def _get_node_type(self, parent: MixerNode):
        if not isinstance(parent, Fx):
            raise ValueError("Fx params node must belong to Fx node")

        type_id = parent.effect_type
        if type_id not in FX_PARAMS_NODE_TYPES_MAP:
            raise ValueError(f"Unsupported effect type '{type_id}'")
        return FX_PARAMS_NODE_TYPES_MAP[type_id]


class Fx(MixerNode):
    "FX effect settings"

    insert_mode = BoolProperty("insert")
    "Is fx in an insert mode. Channels and buses to insert fx to are configured in insert sections of these channels and buses."

    effect_type = EnumIntProperty("type", FxType)

    effect_params = FxParamsNodeProvider("par", description_suffix="\nParameter set changes when effect_type changes.")


class Fxes(MixerCollectionNode[Fx]):
    item_type = Fx
    item_num_width = 1

    @override
    def _pre_init(self):
        if self.item_count is None:
            self.item_count = self.mixer_model.num_fx
