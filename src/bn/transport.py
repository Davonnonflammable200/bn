from __future__ import annotations

import json
import socket
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .paths import registry_dir


class BridgeError(RuntimeError):
    pass


@dataclass(slots=True)
class BridgeInstance:
    pid: int
    socket_path: Path
    registry_path: Path
    plugin_name: str
    plugin_version: str
    started_at: str | None
    meta: dict[str, Any]

    @property
    def label(self) -> str:
        return f"{self.pid}:{self.plugin_version}"


def _load_instance(path: Path) -> BridgeInstance | None:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        socket_path = Path(payload["socket_path"])
        pid = int(payload["pid"])
    except (OSError, ValueError, KeyError, json.JSONDecodeError):
        return None

    if not socket_path.exists():
        return None

    return BridgeInstance(
        pid=pid,
        socket_path=socket_path,
        registry_path=path,
        plugin_name=str(payload.get("plugin_name", "bn_agent_bridge")),
        plugin_version=str(payload.get("plugin_version", "0")),
        started_at=payload.get("started_at"),
        meta=payload,
    )


def list_instances() -> list[BridgeInstance]:
    root = registry_dir()
    if not root.exists():
        return []

    instances: list[BridgeInstance] = []
    for path in sorted(root.glob("*.json")):
        instance = _load_instance(path)
        if instance is not None:
            instances.append(instance)
    return instances


def choose_instance(
    *,
    instance_pid: int | None = None,
    target: str | None = None,
) -> BridgeInstance:
    instances = list_instances()
    if not instances:
        raise BridgeError("No running Binary Ninja bridge instances found")

    if target and target != "active":
        try:
            target_pid = int(target.split(":", 1)[0])
        except ValueError:
            target_pid = None
        if target_pid is not None:
            instance_pid = target_pid

    if instance_pid is not None:
        for instance in instances:
            if instance.pid == instance_pid:
                return instance
        raise BridgeError(f"No running Binary Ninja bridge instance for pid {instance_pid}")

    if len(instances) == 1:
        return instances[0]

    raise BridgeError(
        "Multiple Binary Ninja bridge instances are running; pass --instance or use a full target id"
    )


def send_request(
    op: str,
    *,
    params: dict[str, Any] | None = None,
    target: str | None = None,
    instance_pid: int | None = None,
    timeout: float = 30.0,
) -> dict[str, Any]:
    instance = choose_instance(instance_pid=instance_pid, target=target)
    payload: dict[str, Any] = {
        "id": str(uuid.uuid4()),
        "op": op,
        "params": params or {},
    }
    if target is not None:
        payload["target"] = target

    encoded = (json.dumps(payload) + "\n").encode("utf-8")

    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        sock.connect(str(instance.socket_path))
        sock.sendall(encoded)
        sock.shutdown(socket.SHUT_WR)
        chunks: list[bytes] = []
        while True:
            chunk = sock.recv(65536)
            if not chunk:
                break
            chunks.append(chunk)

    if not chunks:
        raise BridgeError("Binary Ninja bridge returned an empty response")

    try:
        response = json.loads(b"".join(chunks).decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise BridgeError("Binary Ninja bridge returned invalid JSON") from exc

    if not isinstance(response, dict):
        raise BridgeError("Binary Ninja bridge returned a malformed response")

    if response.get("ok"):
        return response

    error = response.get("error") or "Unknown Binary Ninja bridge error"
    raise BridgeError(str(error))
