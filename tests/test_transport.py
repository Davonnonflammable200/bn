from __future__ import annotations

import json
import os
import socketserver
import threading
import uuid
from pathlib import Path

from bn.transport import choose_instance, list_instances, send_request


class _Handler(socketserver.StreamRequestHandler):
    def handle(self):
        payload = json.loads(self.rfile.readline().decode("utf-8"))
        response = {
            "ok": True,
            "result": {
                "op": payload["op"],
                "target": payload.get("target"),
                "params": payload.get("params"),
            },
        }
        self.wfile.write(json.dumps(response).encode("utf-8"))


class _Server(socketserver.ThreadingMixIn, socketserver.UnixStreamServer):
    daemon_threads = True


def test_send_request_uses_registry_and_socket(tmp_path, monkeypatch):
    monkeypatch.setenv("BN_CACHE_DIR", str(tmp_path))
    socket_path = Path("/tmp") / f"bn-test-{os.getpid()}-{uuid.uuid4().hex[:8]}.sock"
    registry_dir = tmp_path / "instances"
    registry_dir.mkdir(parents=True)

    server = _Server(str(socket_path), _Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    (registry_dir / "123.json").write_text(
        json.dumps(
            {
                "pid": 123,
                "socket_path": str(socket_path),
                "plugin_name": "bn_agent_bridge",
                "plugin_version": "0.1.0",
            }
        ),
        encoding="utf-8",
    )

    try:
        instances = list_instances()
        assert len(instances) == 1
        instance = choose_instance(target="123:1:999")
        assert instance.pid == 123

        response = send_request("ping", params={"hello": "world"}, target="123:1:999")
        assert response["result"]["op"] == "ping"
        assert response["result"]["params"] == {"hello": "world"}
    finally:
        server.shutdown()
        server.server_close()


def test_choose_instance_accepts_pid_prefixed_human_selector(tmp_path, monkeypatch):
    monkeypatch.setenv("BN_CACHE_DIR", str(tmp_path))
    registry_dir = tmp_path / "instances"
    registry_dir.mkdir(parents=True)

    socket_path = Path("/tmp") / f"bn-test-{os.getpid()}-{uuid.uuid4().hex[:8]}.sock"
    server = _Server(str(socket_path), _Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    (registry_dir / "456.json").write_text(
        json.dumps(
            {
                "pid": 456,
                "socket_path": str(socket_path),
                "plugin_name": "bn_agent_bridge",
                "plugin_version": "0.1.0",
            }
        ),
        encoding="utf-8",
    )

    try:
        instance = choose_instance(target="456:SnailMail_unwrapped.exe.bndb")
        assert instance.pid == 456
    finally:
        server.shutdown()
        server.server_close()
