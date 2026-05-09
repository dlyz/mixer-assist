import dataclasses


@dataclasses.dataclass(frozen=True)
class MixerModel:
    id: str
    first_name: str
    num_sources: int
    num_headamp: int
    num_dca: int
    num_channels: int
    num_bus: int
    num_fx: int
    num_auxrtn: int = 0
    num_matrix: int = 0
    line_inputs_fixed_stereo: bool = False

    @property
    def name(self):
        return self.first_name + " " + self.id


X32 = MixerModel(
    id="X32",
    first_name="Behringer",
    num_sources=32,
    num_dca=8,
    num_channels=32,
    num_bus=16,
    num_fx=8,
    num_auxrtn=8,
    num_matrix=6,
    num_headamp=127,
)
MR18 = MixerModel(
    id="MR18",
    first_name="Midas",
    num_sources=18,
    num_headamp=16,
    num_dca=4,
    num_channels=16,
    num_bus=6,
    num_fx=4,
    line_inputs_fixed_stereo=True,
)
XR18 = dataclasses.replace(MR18, id="XR18", first_name="Behringer")
XR16 = dataclasses.replace(XR18, id="XR16", num_sources=16, num_bus=4)
MR12 = MixerModel(
    id="MR12",
    first_name="Midas",
    num_sources=12,
    num_headamp=12,
    num_dca=4,
    num_channels=12,
    num_bus=2,
    num_fx=4,
)
XR12 = dataclasses.replace(MR12, id="XR12", first_name="Behringer")

MODELS_BY_ID = {
    X32.id: X32,
    MR18.id: MR18,
    XR18.id: XR18,
    XR16.id: XR16,
    MR12.id: MR12,
    XR12.id: XR12,
}


def get_model(model_id: str) -> MixerModel:
    return MODELS_BY_ID[model_id]
