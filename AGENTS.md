# AGENTS.md

## Project Goals

- Build a mixer wrapper that targets MCP usage with a predictable tree-shaped model:
  - A read/list flow that navigates node paths naturally.
  - A write flow that applies validated path/value updates.
  - Consistent value semantics at leaves (human-facing values, protocol remapping hidden internally).
- Build a Python library that is pleasant to use directly in scripts:
  - Strong static typing with Pylance/Pyright-friendly descriptors and overloads.
  - Reliable IntelliSense/autocomplete across mixer nodes and properties.
  - Explicit, maintainable models unlike the dynamic-style ergonomics issues seen in `xair_api`.

## Protocol

Good list of commands is [here](https://behringer.world/wiki/doku.php?id=x-air_osc), but may be not exactly accurate. Use it when asked to add some not-yet-implemented commands.
Also see xair_api (references/xair_api) as reference (<https://github.com/onyx-and-iris/xair-api-python>), but may be also not accurate or incomplete.

## Philosophy

- Keep the transport layer minimal, explicit, and reliable.
- Keep model definitions declarative and predictable.
- Keep value remapping and validation close to value descriptors.

## Architecture Principles

- `xair_api`: only using for reference
- `xair_client`: our new client library
- `xair_client/client.py`:
  - OSC transport, request/response correlation, model detection.
- `xair_client/mixer_models.py`:
  - Mixer model definitions and lookup.
- `xair_client/nodes.py`:
  - Base node/value/descriptor infrastructure and tree description behavior.
- `xair_client/model/*`:
  - Declarative mixer domain structure only (channels, mixer root, etc.).
- `xair_client/mixer_values.py`:
  - Typed value adapters (bool, enum).

## Data Modeling Rules

- External API should expose human-friendly values where practical.
- Raw OSC index/value conventions should be hidden inside descriptors.
- Validate all writes before sending to mixer.
- Model-dependent constraints should come from `XAirClient.model`.
- Do not use unconstrained `IntValue` for protocol-coded fields (mode/slot/type/position/etc.); use `EnumIntValue` or another constrained value adapter with explicit semantics.

## Coding style and python

Apply these rules when writing or modifying Python code.

### Tooling

- Run Python via `uv`; do not invoke `python` directly.
- Examples:
  - `uv run python -m py_compile ...`
  - `uv run python -m pytest ...`
  - `uv run python -m <module>`

### Typing Rules

- Use modern unions: `A | B` and `T | None`.
- Do not use `typing.Optional` or `typing.Union`.
- Use concrete return/value types where practical.
- Do not use `from __future__ import annotations`, current python version doesn't need it.
- Use `@override` decorator for overridden class members

### Code flow rules

- Use if-else instead if-break and if-continue and if-return when `if` and `else` statements are kind of same level of logic. When it is a shortcut, return/break/continue is preferred instead of introducing nested branch for the "normal" case.

### Descriptor Rules (Pyright/Pylance)

- For descriptors, implement `@overload` for `__get__`:
  - class access returns descriptor type
  - instance access returns value type
- Avoid explicit type annotations on descriptor-backed class attributes; let descriptor typing drive inference.
- Prefer strongly typed descriptor subclasses for value semantics (bool/enum/custom mapped int).
