from typing import Any, override

from ..nodes_base import MixerNode, MixerPropDescriptor, MixerProperty, MixerPropertyPathLike


class GroupMaskProperty(MixerProperty[str]):
    def __init__(
        self,
        path_segment: MixerPropertyPathLike,
        *,
        writable: bool = True,
        description: str | None = None,
    ):
        super().__init__(path_segment, writable=writable)
        self.description = description

    @override
    def parse(self, value: str) -> str:
        return self._normalize_validate(value, num_groups=None)

    @override
    def decode(self, raw: Any, instance: MixerNode) -> str:
        mask = int(raw)
        width = instance.mixer_model.num_groups
        max_mask = (1 << width) - 1
        if not 0 <= mask <= max_mask:
            raise ValueError(f"{self.name} raw value must be in range 0..{max_mask}, got {mask}")

        return format(mask, f"0{width}b")[::-1]

    @override
    def encode(self, value: str, instance: MixerNode) -> int:
        width = instance.mixer_model.num_groups
        value = self._normalize_validate(value, num_groups=width)
        return int(value[::-1], 2)

    @override
    def make_node_descriptor(self, parent: MixerNode) -> MixerPropDescriptor:
        width = parent.mixer_model.num_groups
        return MixerPropDescriptor(
            type="str",
            constraints=f"{width}-digit binary string (0/1), first digit is the value for the first group.",
            description=self.description,
        )

    def _normalize_validate(self, value: str, num_groups: int | None) -> str:
        text = value.strip()
        if num_groups is not None and len(text) != num_groups:
            raise ValueError(f"{self.name} must contain exactly {num_groups} digits, got {len(text)}")
        if not text:
            raise ValueError(f"{self.name} must not be empty")
        invalid = set(text) - {"0", "1"}
        if invalid:
            raise ValueError(f"{self.name} must contain only '0' and '1', got {value!r}")
        return text
