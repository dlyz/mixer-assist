# This file is mostly ai-coded with manual crutches

import argparse
import keyword
import re
from pathlib import Path

from fx_js_parser import (
    FxBooleanParameter,
    FxDoubleParameter,
    FxParameter,
    FxSelectParameter,
    FxTypeFile,
    validate_all_fx_type_files,
)


ROOT = Path(__file__).resolve().parents[1]
TYPE_FOLDER = Path(__file__).resolve().parent / "types"
OUTPUT_FOLDER = ROOT / "xair_client" / "nodes" / "effects"


def _split_words(text: str) -> list[str]:
    return [part for part in re.split(r"[^0-9A-Za-z]+", text) if part]


def to_snake_file_name_allow_first_digit(text: str) -> str:
    words = _split_words(text)
    if not words:
        return "value"
    result = "_".join(word.lower() for word in words)
    return result


def to_snake(text: str, digit_prefix: str = "v_") -> str:
    words = _split_words(text)
    if not words:
        return "value"
    result = "_".join(word.lower() for word in words)
    if result[0].isdigit():
        result = f"{digit_prefix}{result}"
    if keyword.iskeyword(result):
        result = f"{result}_value"
    return result


def to_pascal(text: str) -> str:
    words = _split_words(text)
    if not words:
        return "Value"
    result = "".join(word[:1].upper() + word[1:].lower() for word in words)
    if result[0].isdigit():
        result = f"Fx{result}"
    return result


def to_enum_member(text: str, normal_name: str | None, fallback: str) -> tuple[str, str]:
    words = _split_words(normal_name or text)
    result = "_".join(words).upper()
    unsan_words = [part for part in re.split(r"[,\(\)\s]+", text) if part]
    unsan_result = "_".join(unsan_words)
    if not result:
        result = fallback
    if not result or result[0].isdigit():
        result = f"V_{result}"
    if keyword.iskeyword(result.lower()):
        result = f"{result}_VALUE"

    return (result, unsan_result)


def parameter_descriptor(parameter) -> str | None:
    # desc = parameter.name
    return None
    parts: list[str] = []
    if isinstance(parameter, FxDoubleParameter):
        if parameter.style:
            parts.append(f"style: {parameter.style}")
        if parameter.component:
            parts.append(f"component: {parameter.component}")
    if isinstance(parameter, FxSelectParameter):
        if parameter.style:
            parts.append(f"style: {parameter.style}")
    if isinstance(parameter, FxBooleanParameter):
        if parameter.style:
            parts.append(f"style: {parameter.style}")
    return ", ".join(parts)


def render_select_enum(parameter: FxSelectParameter, enum_name: str) -> str:
    lines = [f"class {enum_name}(IntEnum):"]
    require_labels = False
    labels: list[tuple[str, str]] = []
    for option in parameter.options:
        member, label = to_enum_member(option.name, option.normal_name, f"OPTION_{option.id}")
        labels.append((member, label))
        require_labels |= member != label.upper()
        lines.append(f"    {member} = {option.id}")

    if require_labels:
        lines.append("")
        lines.append("    _LABELS = enum.nonmember({")
        for member, label in labels:
            lines.append(f"        {member}: {label!r},")

        lines.append("    })")
    return "\n".join(lines)


def render_parameter(parameter: FxParameter, enum_name: str | None = None, digit_prefix: str = "_v") -> str:
    name = to_snake(parameter.name, digit_prefix=digit_prefix)

    args = [f'"{parameter.number}"']
    if isinstance(parameter, FxDoubleParameter):
        base = "LogFloatProperty" if parameter.scale == "log" else "LinearFloatProperty"
        args.append(str(parameter.minimum))
        args.append(str(parameter.maximum))
        args.append(f"decimals={parameter.precision}")
        if parameter.unit:
            args.append(f"units={parameter.unit!r}")

    elif isinstance(parameter, FxSelectParameter):
        assert enum_name is not None
        base = "EnumIntProperty"
        args.append(enum_name)

    elif isinstance(parameter, FxBooleanParameter):
        base = "InvertedBoolProperty" if parameter.style == "offOn" else "BoolProperty"

    else:
        raise TypeError(f"Unsupported parameter type: {type(parameter)!r}")

    description = parameter_descriptor(parameter)
    if description:
        args.append(f"description={description!r}")
    return f"    {name} = {base}({', '.join(args)})"


def render_fx_file(spec: FxTypeFile) -> tuple[str, str]:
    class_name = f"{to_pascal(spec.name)}FxParams"
    lines: list[str] = [
        "# This file is auto-generated with generate_fx_nodes.py. Do not edit manually.",
        "",
        "import enum",
        "from enum import IntEnum",
        "",
        "from ...nodes_base import MixerNode",
        "from ...properties.primitive import BoolProperty, EnumIntProperty, InvertedBoolProperty, LinearFloatProperty, LogFloatProperty",
        "",
    ]

    select_parameters = [p for p in spec.parameters if isinstance(p, FxSelectParameter)]
    enum_names: dict[int, str] = {}
    for index, parameter in enumerate(select_parameters):
        enum_name = f"{to_pascal(parameter.name)}Options"
        enum_names[id(parameter)] = enum_name
        lines.append(render_select_enum(parameter, enum_name))
        lines.append("")

    lines.append(f"class {class_name}(MixerNode):")
    lines.append(f"    description = {f'{spec.name} effect parameters ({spec.category} category).'!r}")
    lines.append("")

    for parameter in spec.parameters:
        enum_name = enum_names.get(id(parameter))
        digit_prefix = "f_" if spec.category == "Equalizer" else "v_"
        lines.append(render_parameter(parameter, enum_name, digit_prefix=digit_prefix))

    lines.append("")
    file_name = f"fx_{spec.id:02d}_{to_snake_file_name_allow_first_digit(spec.name)}.py"
    return file_name, "\n".join(lines)


def render_all_file(specs: list[FxTypeFile]) -> str:
    lines: list[str] = [
        "# This file is auto-generated with generate_fx_nodes.py. Do not edit manually.",
        "",
        "from enum import IntEnum",
        "from typing import TypeAlias",
    ]

    for spec in specs:
        class_name = f"{to_pascal(spec.name)}FxParams"
        file_name = f"fx_{spec.id:02d}_{to_snake_file_name_allow_first_digit(spec.name)}"
        lines.append(f"from .{file_name} import {class_name}")

    lines.extend(
        [
            "",
            "FxParamsNode: TypeAlias = (",
        ]
    )

    for index, spec in enumerate(specs):
        class_name = f"{to_pascal(spec.name)}FxParams"
        suffix = " |" if index < len(specs) - 1 else ""
        lines.append(f"    {class_name}{suffix}")

    lines.extend(
        [
            ")",
            "",
            "class FxType(IntEnum):",
        ]
    )

    used_members: set[str] = set()
    for spec in specs:
        member = to_pascal(spec.name)
        base = member
        suffix = 2
        while member in used_members:
            member = f"{base}{suffix}"
            suffix += 1
        used_members.add(member)
        lines.append(f"    {member} = {spec.id}")

    lines.extend(
        [
            "",
            "FX_PARAMS_NODE_TYPES_MAP: dict[FxType, type[FxParamsNode]] = {",
        ]
    )

    for spec in specs:
        member = to_pascal(spec.name)
        class_name = f"{to_pascal(spec.name)}FxParams"
        lines.append(f"    FxType.{member}: {class_name},")

    lines.append("}")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate FX parameter node classes from magical-mixers type definitions."
    )
    parser.add_argument("--write", action="store_true", help="Write generated files to disk (default action).")
    args = parser.parse_args()

    if not args.write:
        args.write = True

    specs = validate_all_fx_type_files(TYPE_FOLDER)
    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

    for spec in specs:
        file_name, content = render_fx_file(spec)
        (OUTPUT_FOLDER / file_name).write_text(content + "\n", encoding="utf-8")

    (OUTPUT_FOLDER / "all.py").write_text(render_all_file(specs) + "\n", encoding="utf-8")

    print(f"Generated {len(specs)} FX node files in {OUTPUT_FOLDER}")


if __name__ == "__main__":
    main()
