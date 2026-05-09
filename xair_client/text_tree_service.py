from .nodes_base import MixerCollectionNode, MixerNode, MixerPropertyNode

from .nodes.mixer import Mixer


class MixerTextTreeService:
    def __init__(self, mixer: Mixer):
        self._mixer = mixer

    def resolve_node(self, path: str) -> MixerNode | MixerPropertyNode:
        segments = [segment for segment in path.split("/") if segment]

        current: MixerNode = self._mixer
        for idx, segment in enumerate(segments):
            is_last = idx == len(segments) - 1
            child = next((child for name, child in current.children if name == segment), None)
            if child is None:
                raise ValueError(f"path not found: '{'/' + '/'.join(segments[: idx + 1])}'")
            if is_last:
                return child
            if isinstance(child, MixerPropertyNode):
                raise ValueError(
                    f"path not found: '{'/' + '/'.join(segments[: idx + 2])}', leaf mixer property is available at {'/' + '/'.join(segments[: idx + 1])}"
                )
            current = child
        return current

    def expand_node(self, path: str, verbose: bool) -> str:
        node = self.resolve_node(path)
        if isinstance(node, MixerPropertyNode):
            return path + "\n".join(_print_value(node, "  ", verbose=verbose))

        container = node if isinstance(node, MixerCollectionNode) else None

        lines: list[str] = [f"{path}:" + "\n".join(_print_value(node, "", verbose=verbose))]
        for child_name, child in node.children:
            # suppressing description for collection items because they all repeat the same.
            actual_verbose = verbose and (container is None or child not in container)
            lines.append(f"  - {child_name}" + "\n".join(_print_value(child, "    ", verbose=actual_verbose)))
        return "\n".join(lines)

    def set_parameter(self, path: str, value: str):
        node = self.resolve_node(path)
        if not isinstance(node, MixerPropertyNode):
            raise ValueError(f"path is not a mixer parameter, but intermediate node: '{path}'")

        node.formatted_value = value
        return f"{path} = {node.formatted_value}"


def _print_value(node: MixerNode | MixerPropertyNode, indent: str, verbose: bool):
    lines: list[str] = []
    if isinstance(node, MixerPropertyNode):
        descriptor = node.descriptor
        lines.append(" = " + node.formatted_value)
        if verbose:
            parts: list[str] = []
            if descriptor.type:
                parts.append(descriptor.type)
            if descriptor.units:
                parts.append(f"in {descriptor.units}")
            if descriptor.constraints:
                parts.append(descriptor.constraints)
            descriptor_line = ", ".join(parts)
            if descriptor_line:
                lines.append(f"{indent}{descriptor_line}")
    else:
        descriptor = node.descriptor
        lines.append("")

    if verbose and descriptor.description:
        lines.extend(f"{indent}{line}" for line in descriptor.description.strip().splitlines())
    return lines
