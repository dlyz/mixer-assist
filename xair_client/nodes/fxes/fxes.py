from typing import override

from .effects.all import FX_PARAMS_NODE_TYPES_MAP, FxParamsNode, FxType
from ..core.primitive_props import BoolProperty, EnumIntProperty
from ..core.base_types import MixerCollectionNode, MixerNode, MixerNodeFactory


class FxParamsNodeProvider(MixerNodeFactory[FxParamsNode]):
    transient = True

    def __init__(
        self,
        address_segment: str,
        *,
        description_suffix: str | None = None,
    ):
        super().__init__(address_segment, None, description_suffix=description_suffix)

    @override
    def _get_node_type(self, parent: MixerNode):
        if not isinstance(parent, Fx):
            raise ValueError("Fx params node must belong to Fx node")

        type_id = parent.effect_type
        if type_id not in FX_PARAMS_NODE_TYPES_MAP:
            raise ValueError(f"Unsupported effect type '{type_id}'")
        return FX_PARAMS_NODE_TYPES_MAP[type_id]


class Fx(MixerNode):
    """
    FX slot settings. Can operate in either **Insert** or **Send/Return** mode.
    Each effect processor features two inputs and two outputs (labeled A and B).
    Their behavior depends on the selected routing mode and the internal topology of the effect itself.

    Effect topologies are generally divided into two types:
    * **Dual Processing:** Processes inputs A and B completely independently using separate sets of control parameters.
      The signals remain isolated from input to output.
      This essentially allows a single FX slot to function as two independent mono processors.
    * **Stereo Processing:** Treats inputs A and B as Left and Right channels respectively, outputting a processed stereo image to outputs A and B.
    * *Note:* If an effect type does not explicitly state "Dual" or "Stereo" in its name,
      it is typically either a true stereo effect or a dual-input effect with linked parameters (one set of controls for both channels).

    **Insert Mode**

    In Insert mode, the effect is placed directly into the signal chain of a selected channel or bus.
    The output of the effect completely replaces the dry signal at the insert point.

    Using inserts A and B, you can patch a single FX slot into:
    a single mono channel/bus (using just one side);
    two independent mono channels/buses;
    a linked stereo pair of channels/buses.

    * **Dual effects** apply independent parameters (Set A and Set B) to their respective inserts.
      This is ideal for processing one mono source or two separate mono sources with different settings within one slot.
      Could also be used for stereo pair in niche scenarios to achieve different results on left and right channels.
    * **Stereo effects** treat insert A as the Left channel and insert B as the Right channel.
      This is the correct choice for linked stereo pairs.
      Patching single or two unrelated mono channels into a stereo effect is technically possible but usually undesirable.

    **Send/Return Mode**

    In Send/Return mode, the send mix from the channels is routed via a dedicated FX Send bus to the effect processor.
    Because FX Send buses are strictly mono, both inputs A and B always receive the exact same identical signal.
    The processed signal is then returned to the mix through a dedicated stereo FX Return channel.

    * **Dual effects** can be used in this mode to generate different acoustic results for the Left and Right return channels by tweaking parameters A and B independently.
    * **Stereo effects** operate natively in this mode, delivering a traditional stereo ambient field (like reverb or delay) derived from the mono input signal.
    """

    insert_mode = BoolProperty("insert")
    """
    Is fx in an insert mode.
    Have to be enabled and inserted in required channel/bus `config` section in order to be effective.
    """

    effect_type = EnumIntProperty("type", FxType)

    effect_params = FxParamsNodeProvider("par", description_suffix="\nParameter set changes after effect_type change.")


class Fxes(MixerCollectionNode[Fx]):
    item_type = Fx
    item_num_width = 1

    @override
    def _pre_init(self):
        if self.item_count is None:
            self.item_count = self.mixer_model.num_fx
