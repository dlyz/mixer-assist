# converter from js format of magical-mixers into a yaml

import ast
import json
import re
from pathlib import Path

import yaml


SOURCE_DIR = Path(__file__).with_name("js_types")
OUTPUT_DIR = Path(__file__).with_name("types")


def normalize_source(text: str) -> str:
    lines: list[str] = []
    for line in text.splitlines():
        stripped = line.lstrip()
        if stripped.startswith("//"):
            continue
        if stripped.startswith("export default "):
            line = line.replace("export default ", "", 1)
        if stripped == "};":
            lines.append("}")
            continue
        lines.append(line)

    normalized = "\n".join(lines)
    normalized = re.sub(
        r"(?m)(^|[{\[,]\s*)([A-Za-z_][A-Za-z0-9_]*)\s*:",
        r'\1"\2":',
        normalized,
    )
    normalized = re.sub(
        r"'([^'\\]*(?:\\.[^'\\]*)*)'",
        lambda match: json.dumps(ast.literal_eval(match.group(0))),
        normalized,
    )
    normalized = re.sub(r",(\s*[}\]])", r"\1", normalized)
    return normalized


def parse_fx_type(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    return json.loads(normalize_source(text))


def dump_yaml(data: object) -> str:
    return yaml.safe_dump(data, sort_keys=False, allow_unicode=True)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    converted = 0
    for path in sorted(SOURCE_DIR.glob("type*.js")):
        data = parse_fx_type(path)
        output_path = OUTPUT_DIR / f"{path.stem}.yaml"
        output_path.write_text(dump_yaml(data), encoding="utf-8")
        converted += 1

    print(f"Converted {converted} files to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
