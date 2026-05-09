import argparse
import atexit
import logging
from fastmcp import FastMCP
from pydantic import BaseModel, ConfigDict, Field

from xair_client.client import XAirConnection
from xair_client.nodes.mixer import Mixer
from xair_client.text_tree_service import MixerTextTreeService

logger = logging.getLogger(__name__)
type PrimitiveValue = str | int | float | bool


def main():
    parser = argparse.ArgumentParser(description="MCP server for XAir mixer tree access.")
    parser.add_argument("--ip", required=True, help="Mixer IP address.")
    parser.add_argument("--port", type=int, default=10024, help="Mixer OSC port.")
    parser.add_argument("--timeout", type=float, default=1.0, help="Read timeout in seconds.")
    args = parser.parse_args()

    client = XAirConnection(ip=args.ip, port=args.port, timeout=args.timeout).connect()
    atexit.register(client.close)
    logger.error("Mixer connected.")
    service = MixerTextTreeService(Mixer(client))
    mcp = build_server(service)
    mcp.run()


DESCRIBE_NODE_TOOL_DESCRIPTION = """
For a path in the mixer parameter tree, returns children nodes with their current values (for children that are leaves i.e. mixer parameters).
Also returns type, units, constraints, and description (if available) for the path-selected node and it's children.

Actual result for the root path (`/`) is:

"""

EXPAND_NODE_TOOL_DESCRIPTION = """
Batch version of the describe_node tool, that does not return descriptions etc, only children names and values.
If the path is a parameter (tree leaf), it's value will be returned.
Useful when you have already discovered available parameters with their types and constraints (using describe-node)
and want to get mixer parameter values without excessive information.
"""

SET_PARAMETERS_TOOL_DESCRIPTION = """
Sets provided values for selected parameters.
You don't have to read parameters manually after setting values: their actual values will be returned as a result of this tool call.
Be sure to consult parameters description (type and constraints) using describe-node before setting any values.
"""


class ParameterInput(BaseModel):
    path: str = Field(description="Path of the parameter in mixer parameter tree.")
    value: PrimitiveValue = Field(description="Value of the parameter to set.")

    model_config = ConfigDict(extra="forbid")


def build_server(service: MixerTextTreeService) -> FastMCP:
    mcp = FastMCP("x-air-mixer", "Gives access to the Behringer/Midas mixer.")

    root_description = service.expand_node("/", verbose=True)

    @mcp.tool(
        name="describe-node",
        description=DESCRIBE_NODE_TOOL_DESCRIPTION + root_description,
    )
    def describe_node(path: str = "/") -> str:
        path = _normalize_path(path)
        return service.expand_node(path, verbose=True)

    @mcp.tool(
        name="expand-node",
        description=EXPAND_NODE_TOOL_DESCRIPTION,
    )
    def expand_node(paths: list[str]) -> str:
        if len(paths) == 0:
            raise ValueError("paths must not be empty")
        blocks: list[str] = []
        for path in paths:
            try:
                path = _normalize_path(path)
                blocks.append(service.expand_node(path, verbose=False))
            except (ValueError, IndexError, AttributeError, TypeError) as exc:
                blocks.append(f"{path}:\n  ERROR: {exc}")
            except Exception:
                logger.exception("Internal error while expanding path %s", path)
                blocks.append(f"{path}:\n  ERROR: internal error while reading path")
        return "\n\n".join(blocks)

    @mcp.tool(
        name="set-parameters",
        description=SET_PARAMETERS_TOOL_DESCRIPTION,
    )
    def set_parameters(parameters: list[ParameterInput]) -> str:
        if len(parameters) == 0:
            raise ValueError("parameters must not be empty")

        lines: list[str] = []
        for assignment in parameters:
            path = assignment.path
            try:
                path = _normalize_path(path)
                lines.append(service.set_parameter(path, str(assignment.value)))
            except (ValueError, IndexError, AttributeError, TypeError) as exc:
                if lines:
                    lines.append("")
                lines.append("PARAMETER ASSIGNMENT INTERRUPTED")
                lines.append(f"FAILED TO SET {path} = {assignment.value}")
                lines.append(f"ERROR: {exc}")
                lines.append(f"SUGGESTION: Use describe-node for {path} to check type and constraints before retrying.")
                return "\n".join(lines)
            except Exception:
                logger.exception("Internal error while applying parameter %s", path)
                if lines:
                    lines.append("")
                lines.append("PARAMETER ASSIGNMENT INTERRUPTED")
                lines.append(f"FAILED TO SET {path} = {assignment.value}")
                lines.append("ERROR: internal error while applying parameter")
                return "\n".join(lines)

        return "\n".join(lines)

    return mcp


def _normalize_path(path: str) -> str:
    if not path:
        raise ValueError("non-empty path is required")
    normalized = path.strip()
    if not normalized:
        raise ValueError("path is required")
    if not normalized.startswith("/"):
        normalized = f"/{normalized}"
    if normalized != "/":
        normalized = normalized.rstrip("/")
    return normalized


if __name__ == "__main__":
    main()
