import abc
import logging
import math
from pathlib import Path
import socket
import threading
import time
from typing import Any, overload, override

from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_message_builder import OscMessageBuilder
from pythonosc.osc_server import BlockingOSCUDPServer
from .mixer_models import get_model, MixerModel

logger = logging.getLogger(__name__)


class XAirClientError(Exception):
    """Base error for xair_client transport issues."""


class XAirReadTimeout(XAirClientError):
    """Raised when the mixer does not reply before timeout."""


class XAirCommitConfirmFailed(XAirClientError):
    """Commit operation could not been confirmed."""

    def __init__(self, message: str, actual_value: Any):
        super().__init__(message)
        self.actual_value = actual_value


class XAirProtocolError(XAirClientError):
    """Raised when mixer reply shape is invalid for a read operation."""


class XAirEmptyReplyError(XAirProtocolError):
    pass


class OSCClientServer(BlockingOSCUDPServer):
    def __init__(self, remote_address: tuple[str, int], dispatcher: Dispatcher):
        super().__init__(("", 0), dispatcher, family=socket.AddressFamily.AF_INET)
        self.remote_address = remote_address

    def send_message(self, address: str, values: Any | list[Any] | None):
        builder = OscMessageBuilder(address=address)
        if values is None:
            normalized: list[Any] = []
        elif isinstance(values, list):
            normalized = values
        else:
            normalized = [values]

        logger.debug(f"Sending to    '{address}': {normalized}")

        for value in normalized:
            builder.add_arg(value)

        msg = builder.build()

        self.socket.sendto(msg.dgram, self.remote_address)


class XAirClient(abc.ABC):
    @property
    @abc.abstractmethod
    def mixer_name(self) -> str:
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def mixer_model(self) -> MixerModel:
        raise NotImplementedError()

    @abc.abstractmethod
    def read(self, address: str) -> Any:
        raise NotImplementedError()

    @abc.abstractmethod
    def write(self, address: str, value: Any, *, is_action: bool = False) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def post(self, address: str, value: Any) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def commit(self, address: str, value: Any, *, is_action: bool = False, strict_confirm: bool = True) -> Any:
        """Writes specified value and confirms that it is the actual value for that address at the moment.

        :param strict_confirm: Require strict confirmation that provided value has been applied (raises `XAirCommitConfirmFailed` otherwise).
            When false, the returned actual value might differ from the provided one.
        """
        raise NotImplementedError()

    @overload
    def save_scene(self, target_path: None = None) -> dict[str, Any]: ...
    @overload
    def save_scene(self, target_path: Path | str) -> None: ...
    def save_scene(self, target_path: Path | str | None = None):
        with (Path(__file__).parent / "scene_address_list.txt").open(encoding="utf-8") as addresses_file:
            addresses = addresses_file.read().splitlines()
        values: dict[str, Any] = {}
        for address in addresses:
            values[address] = self.read(address)
        if target_path is None:
            return values
        else:
            import yaml

            with Path(target_path).open("w", encoding="utf-8") as target_file:
                yaml.safe_dump(values, target_file, sort_keys=False)

    @staticmethod
    def read_scene_file(scene: Path | str) -> dict[str, Any]:
        import yaml

        with Path(scene).open(encoding="utf-8") as scene_file:
            return yaml.safe_load(scene_file)

    def load_scene(self, scene: Path | str | dict[str, Any], post_values=False):
        if isinstance(scene, (Path, str)):
            values = self.read_scene_file(scene)
        else:
            values = scene

        for address, value in values.items():
            if post_values:
                self.post(address, value)
            else:
                self.commit(address, value)


class XAirConnection(XAirClient):
    """Minimal OSC transport wrapper for X AIR style mixers."""

    def __init__(
        self,
        ip: str,
        port: int = 10024,
        timeout: float = 1.0,
        commit_on_write: bool = True,
        commit_confirm_timeout: float | None = 10.0,
        commit_confirm_attempts: int = 20,
        action_commit_timeout: float = 2.5,
    ):
        if not ip:
            raise ValueError("ip is required")
        if commit_confirm_attempts < 1:
            raise ValueError("commit_confirm_attempts must be at least 1")

        self.ip = ip
        self.port = port
        self.timeout = timeout
        self.commit_on_write = commit_on_write
        self.commit_confirm_timeout = commit_confirm_timeout or timeout
        self.commit_confirm_attempts = commit_confirm_attempts
        self.action_commit_timeout = action_commit_timeout

        dispatcher = Dispatcher()
        dispatcher.set_default_handler(self._on_message)

        self._server = OSCClientServer((self.ip, self.port), dispatcher)
        self._worker: threading.Thread | None = None

        self._query_lock = threading.Lock()
        self._response_cv = threading.Condition()
        self._expected_path: str | None = None
        self._expected_payload: tuple[Any, ...] | None = None
        self._mixer_model = None

    @property
    @override
    def mixer_name(self):
        if self._mixer_name is None:
            raise RuntimeError("Connection has not been established yet")
        return self._mixer_name

    @property
    @override
    def mixer_model(self):
        if self._mixer_model is None:
            raise RuntimeError("Connection has not been established yet")
        return self._mixer_model

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()

    def connect(self):
        if not self._worker or not self._worker.is_alive():
            self._worker = threading.Thread(target=self._server.serve_forever, daemon=True)
            self._worker.start()

        try:
            if not self._mixer_model:
                self._mixer_name, self._mixer_model = self._x_info()
        except Exception:
            self.close()
            raise

        return self

    def close(self):
        self._server.shutdown()

    @override
    def read(self, address: str) -> Any:
        address = self._normalize_address(address)
        deadline = time.monotonic() + self.timeout

        with self._query_lock:
            with self._response_cv:
                self._expected_path = address
                self._expected_payload = None

            self._server.send_message(address, None)

            with self._response_cv:
                while self._expected_payload is None:
                    remaining = deadline - time.monotonic()
                    if remaining <= 0:
                        self._expected_path = None
                        raise XAirReadTimeout(f"timeout reading {address}")
                    self._response_cv.wait(remaining)

                payload = self._expected_payload
                self._expected_path = None
                self._expected_payload = None

        if payload is None:
            raise XAirProtocolError(f"internal error: missing payload for {address}")
        if len(payload) == 0:
            raise XAirEmptyReplyError(f"empty reply for {address}")
        if len(payload) == 1:
            return payload[0]
        return payload

    @override
    def write(self, address: str, value: Any, *, is_action: bool = False):
        if self.commit_on_write:
            self.commit(address, value, is_action=is_action)
        else:
            self.post(address, value)

    @override
    def post(self, address: str, value: Any):
        """Fire and forget write"""
        address = self._normalize_address(address)
        self._server.send_message(address, value)

    @override
    def commit(self, address: str, value: Any, *, strict_confirm: bool = True, is_action: bool = False):
        """Write with confirmation"""
        address = self._normalize_address(address)
        self._server.send_message(address, value)

        if is_action:
            self.read(address)
            time.sleep(self.action_commit_timeout)
            self.read(address)
            return None

        # This is a polling strategy.
        # It is quite reliable, most writes will be available on first or second read.
        # The slower the network, the less attempts are required.
        # There are two problems with polling:
        # - the value must be acceptable by mixer as provided:
        #   if the mixer will correct incoming value, we could not match the actual value to the provided one
        # - if after the wright, but before the first read someone changes this value
        #   we could never see our change, only the actual value from the other change
        # Alternatives:
        # - Return actual value even if it's not matched to the provided (instead of exception).
        # - Subscription. Doesn't solve the first problem, complex impl, not necessary less load on the system.
        #   Less chances of race condition, but still may theoretically drop some data.

        deadline = time.monotonic() + self.commit_confirm_timeout

        actual = None
        timeout = 0.010
        assert self.commit_confirm_attempts > 0
        for attempt in range(0, self.commit_confirm_attempts):
            try:
                actual = self.read(address)
                if _value_equal(value, actual):
                    return actual

            except XAirEmptyReplyError as ex:
                if actual is None:
                    actual = ex

            remaining = deadline - time.monotonic()
            if remaining <= timeout:
                break

            # this should be rare
            if attempt >= 1:
                time.sleep(timeout)
                timeout *= 2

        error = actual if isinstance(actual, Exception) else None

        if strict_confirm:
            raise XAirCommitConfirmFailed(
                f"Could not confirm value write to '{address}'", actual_value=actual
            ) from error
        elif error:
            raise error
        else:
            return actual

    def _on_message(self, address: str, *args):
        with self._response_cv:
            logger.debug(f"Received from '{address}': {args}")
            if self._expected_path == address:
                self._expected_payload = tuple(args)
                self._response_cv.notify_all()

    def _x_info(self) -> tuple[str, MixerModel]:
        info = self.read("/xinfo")
        if not isinstance(info, tuple) or len(info) != 4:
            raise XAirProtocolError(f"invalid /xinfo response: {info!r}")
        ip, mixer_name, model_id, firmware_version = info
        try:
            return mixer_name, get_model(model_id)
        except KeyError as exc:
            raise XAirProtocolError(f"unsupported mixer model id: {model_id}") from exc

    @staticmethod
    def _normalize_address(address: str) -> str:
        if not address:
            raise ValueError("address is required")
        return address if address.startswith("/") else f"/{address}"


def _value_equal(expected: Any, actual: Any):
    if isinstance(expected, (list, tuple)):
        if not isinstance(actual, (list, tuple)):
            raise RuntimeError(
                f"Types of expected and actual x-air protocol values do not match: {type(expected)} != {type(actual)}"
            )
        if len(expected) != len(actual):
            raise RuntimeError(
                f"Expected and actual x-air protocol values have different lengths: {len(expected)} != {len(actual)}"
            )
        return all(_value_equal(e, a) for e, a in zip(expected, actual))

    if type(expected) is not type(actual):
        raise RuntimeError(
            f"Types of expected and actual x-air protocol values do not match: {type(expected)} != {type(actual)}"
        )

    if isinstance(expected, (str, int)):
        return expected == actual
    elif isinstance(expected, float):
        if math.isnan(expected) and math.isnan(actual):
            return True
        return abs(expected - actual) < 1e-5

    raise NotImplementedError(f"Type {type(expected)} is not supported as x-air protocol value.")
