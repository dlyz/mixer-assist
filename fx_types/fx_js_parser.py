# This file is mostly ai-coded

import json
import yaml
from pathlib import Path
from typing import Annotated, Literal, TypeAlias, Union

from pydantic import BaseModel, ConfigDict, Field, TypeAdapter


class FxSelectOption(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: int
    name: str
    normal_name: str | None = None


class FxParameterBase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: int
    number: str
    name: str


class FxDoubleParameter(FxParameterBase):
    type: Literal["double"]
    precision: int
    minimum: float
    maximum: float
    unit: str
    scale: Literal["linear", "log"]
    oscType: Literal["fractional"]
    style: Literal["tap"] | None = None
    component: Literal["knob"] | None = None
    grid_size: int


class FxSelectParameter(FxParameterBase):
    type: Literal["select"]
    options: list[FxSelectOption]
    style: Literal["toggle"] | None = None


class FxBooleanParameter(FxParameterBase):
    type: Literal["boolean"]
    style: Literal["onOff", "offOn", "toggle"]


FxParameter: TypeAlias = Annotated[
    Union[FxDoubleParameter, FxSelectParameter, FxBooleanParameter],
    Field(discriminator="type"),
]


class FxTypeFile(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: int
    name: str
    category: str
    parameters: list[FxParameter]


_fx_type_adapter = TypeAdapter(FxTypeFile)


def load_fx_type_file(path: Path) -> FxTypeFile:
    with path.open(encoding="utf-8") as stream:
        data = yaml.safe_load(stream)
    return _fx_type_adapter.validate_python(data)


def validate_all_fx_type_files(folder: Path) -> list[FxTypeFile]:
    parsed: list[FxTypeFile] = []
    for path in folder.glob("type*.yaml"):
        parsed.append(load_fx_type_file(path))
    return sorted(parsed, key=lambda x: x.id)


def main() -> None:
    folder = Path(__file__).resolve().parent / "types"
    parsed = validate_all_fx_type_files(folder)
    print(f"Validated {len(parsed)} FX type files from {folder}")


if __name__ == "__main__":
    main()
