import argparse
import os
from pathlib import Path
import sys
from dotenv import load_dotenv


from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.document import Document
from prompt_toolkit.history import FileHistory
from prompt_toolkit.formatted_text import HTML

from xair_client.client import XAirConnection
from xair_client.nodes.mixer import Mixer
from xair_client.text_tree_service import MixerTextTreeService
from xair_client.nodes_base import MixerPropertyNode


class TreePathCompleter(Completer):
    def __init__(self, tree_service: MixerTextTreeService, get_current_path):
        self._tree_service = tree_service
        self._get_current_path = get_current_path

    def get_completions(self, document: Document, complete_event):
        path_text = _extract_path_text_for_completion(document.text_before_cursor)
        if not path_text:
            return

        parent_path, last_segment = _split_before_last_path_segment(path_text)
        try:
            absolute_parent_path = _resolve_path(parent_path, self._get_current_path())
            node = self._tree_service.resolve_node(absolute_parent_path)
        except ValueError:
            return

        if isinstance(node, MixerPropertyNode):
            return

        for child_name, _ in node.children:
            if child_name.startswith(last_segment):
                yield Completion(child_name, start_position=-len(last_segment))


class ReplHistory(FileHistory):
    def __init__(self, filename: str, get_current_path):
        super().__init__(filename)
        self._get_current_path = get_current_path

    def append_string(self, string: str) -> None:
        entry = self._normalize_for_history(string)
        if entry is None:
            return
        super().append_string(entry)

    def _normalize_for_history(self, string: str) -> str | None:
        text = string.strip()
        if not text:
            return None

        command = text.split(maxsplit=1)[0].lower()
        if command in {"ls", "ds"}:
            return None
        if command in {"exit", "quit", ":q"}:
            return None
        if command in {"raw"}:
            return text

        set_cmd_args = [s.strip() for s in text.split("=", maxsplit=1)]
        if len(set_cmd_args) > 1:
            raw_path, value = set_cmd_args
            absolute_path = _resolve_path(raw_path, self._get_current_path()) if raw_path else self._get_current_path()
            return f"{absolute_path} = {value}"

        return _resolve_path(text, self._get_current_path())


def _split_before_last_path_segment(path: str) -> tuple[str, str]:
    if "/" not in path:
        return "", path
    parent, _, last = path.rpartition("/")
    if not parent:
        return "/", last
    return parent, last


def _extract_path_text_for_completion(text: str) -> str:
    stripped = text.lstrip()
    if stripped.startswith("ls"):
        remainder = stripped[2:]
        if not remainder:
            return ""
        return remainder.strip()

    if "=" in text:
        return text.split("=", 1)[0].strip()

    return text.strip()


def _split_segments(path: str) -> list[str]:
    return [segment for segment in path.split("/") if segment and segment != "."]


def _join_absolute(segments: list[str]) -> str:
    if not segments:
        return "/"
    return "/" + "/".join(segments)


def _resolve_path(path: str, current_path: str) -> str:
    if not path:
        return current_path

    if path.startswith("/"):
        base_segments: list[str] = []
    else:
        base_segments = _split_segments(current_path)

    for segment in path.split("/"):
        if not segment or segment == ".":
            continue
        if segment == "..":
            if base_segments:
                base_segments.pop()
            continue
        base_segments.append(segment)

    return _join_absolute(base_segments)


def main():
    ip_from_env = os.getenv("MIXER_IP") or None

    parser = argparse.ArgumentParser(description="MCP server for XAir mixer tree access.")
    parser.add_argument("--ip", required=(ip_from_env is None), default=ip_from_env, help="Mixer IP address.")
    parser.add_argument("--port", type=int, default=10024, help="Mixer OSC port.")
    parser.add_argument("--timeout", type=float, default=1.0, help="Read timeout in seconds.")

    args = parser.parse_args()

    with XAirConnection(ip=args.ip, port=args.port, timeout=args.timeout) as client:
        print(f"Connected to {args.ip}, mixer: {client.mixer_name}, model: {client.mixer_model.name}")

        mixer = Mixer(client)
        service = MixerTextTreeService(mixer)
        current_path = "/"
        history_path = Path(__file__).resolve().with_name(".mixer_assist_history")
        session = PromptSession(
            history=ReplHistory(str(history_path), lambda: current_path),
            auto_suggest=AutoSuggestFromHistory(),
            completer=TreePathCompleter(service, lambda: current_path),
            complete_while_typing=True,
        )

        while True:
            try:
                line: str = session.prompt(HTML(f"<yellow>{current_path}></yellow> ")).strip()
            except KeyboardInterrupt:
                print("^C")
                continue
            except EOFError:
                print()
                break

            if not line:
                continue
            if line.lower() in {"exit", "quit", ":q"}:
                break

            try:
                command_split = line.split(maxsplit=1)
                command = command_split[0].lower()
                command_args = command_split[1].strip() if len(command_split) > 1 else ""

                if command == "raw":
                    raw_path = command_args
                    result = client.read(raw_path.split()[0], raw_path.split()[1:])
                    print(f"raw {raw_path} = {result}")
                else:
                    if command in {"ls", "ds"}:
                        raw_path = command_args
                        target_path = _resolve_path(raw_path, current_path) if raw_path else current_path
                        print(service.expand_node(target_path, verbose=line[0] == "d"))
                        continue

                    set_cmd_args = [s.strip() for s in line.split("=", maxsplit=1)]
                    if len(set_cmd_args) > 1:
                        raw_path, value = set_cmd_args

                        target_path = _resolve_path(raw_path, current_path) if raw_path else current_path

                        if not isinstance(service.resolve_node(target_path), MixerPropertyNode):
                            raise ValueError(f"path is not a mixer parameter: '{target_path}'")

                        print(service.set_parameter(target_path, value))
                        continue

                    target_path = _resolve_path(line, current_path)
                    service.resolve_node(target_path)
                    current_path = target_path

                    print(service.expand_node(target_path, verbose=False))

            except Exception as exc:
                print(f"error: {exc}")


if __name__ == "__main__":
    load_dotenv()
    main()
