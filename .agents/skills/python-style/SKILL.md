---
name: python-style
description: Apply universal Python engineering conventions with `uv` tooling and Pylance/Pyright-friendly typing: modern union syntax, strong descriptor typing with overloads, clear separation of declarative domain models from imperative infrastructure, and explicit validation/remapping at boundaries.
---

# Python Style (uv + Pyright)

Apply these rules when writing or modifying Python code.

## Tooling

- Run Python via `uv`; do not invoke `python` directly.
- Examples:
  - `uv run python -m py_compile ...`
  - `uv run python -m pytest ...`
  - `uv run python -m <module>`

## Typing Rules

- Use modern unions: `A | B` and `T | None`.
- Do not use `typing.Optional` or `typing.Union`.
- Use concrete return/value types where practical.
- Do not use `from __future__ import annotations`, current python version doesn't need it.

## Flow rules

- Use if-else instead if-break and if-continue and if-return when if and else statements are kind of same level of logic. When it is a shortcut, return/break/continue is preferred instead of introducing nested branch for the normal case.

## Descriptor Rules (Pyright/Pylance)

- For descriptors, implement `@overload` for `__get__`:
  - class access returns descriptor type
  - instance access returns value type
- Avoid explicit type annotations on descriptor-backed class attributes; let descriptor typing drive inference.
- Prefer strongly typed descriptor subclasses for value semantics (bool/enum/custom mapped int).

