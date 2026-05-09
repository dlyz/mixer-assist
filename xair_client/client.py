import abc
import socket
import threading
import time
from typing import Any, override

from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_message_builder import OscMessageBuilder
from pythonosc.osc_server import BlockingOSCUDPServer
from .mixer_models import get_model, MixerModel


class XAirClientError(Exception):
    """Base error for xair_client transport issues."""


class XAirReadTimeout(XAirClientError):
    """Raised when the mixer does not reply before timeout."""


class XAirProtocolError(XAirClientError):
    """Raised when mixer reply shape is invalid for a read operation."""


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
    def read(self, path: str) -> Any:
        raise NotImplementedError()

    @abc.abstractmethod
    def write(self, path: str, value: Any):
        raise NotImplementedError()


class XAirConnection(XAirClient):
    """Minimal OSC transport wrapper for X AIR style mixers."""

    def __init__(
        self,
        ip: str,
        port: int = 10024,
        timeout: float = 1.0,
    ):
        if not ip:
            raise ValueError("ip is required")

        self.ip = ip
        self.port = port
        self.timeout = timeout

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
    def read(self, path: str) -> Any:
        path = self._normalize_path(path)
        deadline = time.monotonic() + self.timeout

        with self._query_lock:
            with self._response_cv:
                self._expected_path = path
                self._expected_payload = None

            self._server.send_message(path, None)

            with self._response_cv:
                while self._expected_payload is None:
                    remaining = deadline - time.monotonic()
                    if remaining <= 0:
                        self._expected_path = None
                        raise XAirReadTimeout(f"timeout reading {path}")
                    self._response_cv.wait(remaining)

                payload = self._expected_payload
                self._expected_path = None
                self._expected_payload = None

        if payload is None:
            raise XAirProtocolError(f"internal error: missing payload for {path}")
        if len(payload) == 0:
            raise XAirProtocolError(f"empty reply for {path}")
        if len(payload) == 1:
            return payload[0]
        return payload

    @override
    def write(self, path: str, value: Any):
        path = self._normalize_path(path)
        self._server.send_message(path, value)

    def _on_message(self, address: str, *args):
        with self._response_cv:
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
    def _normalize_path(path: str) -> str:
        if not path:
            raise ValueError("path is required")
        return path if path.startswith("/") else f"/{path}"
