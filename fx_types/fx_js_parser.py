# This file is mostly ai-coded

import json
import re
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
_file_pattern = re.compile(r"export\s+default\s+(\{.*\})\s*;?\s*$", re.S)
_key_pattern = re.compile(r"(^|[,{\[]\s*)([A-Za-z_][A-Za-z0-9_]*)\s*:", re.M)
_trailing_comma_pattern = re.compile(r",(?=\s*[}\]])")
_single_quoted_string_pattern = re.compile(r"'([^'\\]*(?:\\.[^'\\]*)*)'")


def _js_object_to_json_text(source: str) -> str:
    match = _file_pattern.search(source)
    if not match:
        raise ValueError("Could not find export default object")

    text = match.group(1)
    text = _single_quoted_string_pattern.sub(lambda m: json.dumps(m.group(1)), text)
    text = _key_pattern.sub(r'\1"\2":', text)
    text = _trailing_comma_pattern.sub("", text)
    return text


def load_fx_type_file(path: Path) -> FxTypeFile:
    raw = path.read_text(encoding="utf-8")
    json_text = _js_object_to_json_text(raw)
    data = json.loads(json_text)
    return _fx_type_adapter.validate_python(data)


def validate_all_fx_type_files(folder: Path) -> list[FxTypeFile]:
    parsed: list[FxTypeFile] = []
    for path in folder.glob("type*.js"):
        parsed.append(load_fx_type_file(path))
    return sorted(parsed, key=lambda x: x.id)


def main() -> None:
    folder = Path(__file__).resolve().parent / "types"
    parsed = validate_all_fx_type_files(folder)
    print(f"Validated {len(parsed)} FX type files from {folder}")


if __name__ == "__main__":
    main()
