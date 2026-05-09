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

Good hint about commands is [here](https://behringer.world/wiki/doku.php?id=x-air_osc), but may be not exactly accurate.
Also see xair_api (references/xair_api) as reference (<https://github.com/onyx-and-iris/xair-api-python>), but may be also not accurate or incomplete.
Also there is magical-mixers (references/magical-mixers) library that has [definitions for all the effects](https://github.com/matiasbarrios/magical-mixers/tree/main/src/core/drivers/xair/device/fx/type).

## Philosophy

- Keep the transport layer minimal, explicit, and reliable.
- Keep model definitions declarative and predictable.
- Keep value remapping and validation close to value descriptors.

## Architecture Principles

- `xair_api`: only using for reference
- `xair_client`: our new client
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
