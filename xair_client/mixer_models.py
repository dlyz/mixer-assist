import dataclasses


@dataclasses.dataclass(frozen=True)
class MixerModel:
    id: str
    first_name: str
    num_sources: int
    num_headamp: int
    num_channels: int
    num_aux_outs: int
    num_bus: int
    num_usb: int

    num_fx: int
    num_groups: int
    """Num of dca groups, the same as num of mute groups."""

    line_inputs_fixed_stereo: bool = False

    @property
    def name(self):
        return self.first_name + " " + self.id


MR18 = MixerModel(
    id="MR18",
    first_name="Midas",
    num_sources=18,
    num_headamp=16,
    num_channels=16,
    num_aux_outs=6,
    num_bus=6,
    num_usb=18,
    num_fx=4,
    num_groups=4,
    line_inputs_fixed_stereo=True,
)
XR18 = dataclasses.replace(
    MR18,
    id="XR18",
    first_name="Behringer",
)
XR16 = MixerModel(
    id="XR16",
    first_name="Behringer",
    num_sources=16,
    num_headamp=8,
    num_channels=16,
    num_aux_outs=4,
    num_bus=6,
    num_usb=2,
    num_fx=4,
    num_groups=4,
)
MR12 = dataclasses.replace(
    XR16,
    id="MR12",
    first_name="Midas",
    num_sources=12,
    num_headamp=4,
    num_aux_outs=2,
)
XR12 = dataclasses.replace(MR12, id="XR12", first_name="Behringer")

MODELS_BY_ID = {
    MR18.id: MR18,
    XR18.id: XR18,
    XR16.id: XR16,
    MR12.id: MR12,
    XR12.id: XR12,
}


def get_model(model_id: str) -> MixerModel:
    return MODELS_BY_ID[model_id]
