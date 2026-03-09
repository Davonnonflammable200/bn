from __future__ import annotations

import json
import tempfile
from pathlib import Path

import tiktoken

from bn.output import write_output


TOKENIZER = "o200k_base"


def _token_count(text: str) -> int:
    return len(tiktoken.get_encoding(TOKENIZER).encode(text))


def test_write_output_renders_small_payload_without_spill(tmp_path, monkeypatch):
    monkeypatch.setenv("BN_CACHE_DIR", str(tmp_path))

    rendered = write_output({"ok": True}, fmt="json", out_path=None, stem="small")

    payload = json.loads(rendered)
    assert payload["ok"] is True


def test_write_output_spills_large_payload(tmp_path, monkeypatch):
    monkeypatch.setenv("BN_CACHE_DIR", str(tmp_path))

    rendered = write_output(
        {"data": "x" * 100_000},
        fmt="json",
        out_path=None,
        stem="large",
        spill_threshold=256,
    )

    envelope = json.loads(rendered)
    artifact_root = tempfile.gettempdir()
    assert envelope["artifact_path"].startswith(artifact_root)
    artifact_text = Path(envelope["artifact_path"]).read_text()
    assert envelope["tokenizer"] == TOKENIZER
    assert envelope["tokens"] == _token_count(artifact_text)


def test_write_output_spills_text_payload_with_txt_suffix(tmp_path, monkeypatch):
    monkeypatch.setenv("BN_CACHE_DIR", str(tmp_path))

    rendered = write_output(
        "x" * 100_000,
        fmt="text",
        out_path=None,
        stem="large-text",
        spill_threshold=256,
    )

    envelope = json.loads(rendered)
    assert envelope["artifact_path"].endswith(".txt")


def test_write_output_reports_exact_tokens_for_explicit_out_path(tmp_path, monkeypatch):
    monkeypatch.setenv("BN_CACHE_DIR", str(tmp_path))

    out_path = tmp_path / "artifacts" / "payload.json"
    rendered = write_output(
        {"message": "token-aware output"},
        fmt="json",
        out_path=out_path,
        stem="explicit-out",
    )

    envelope = json.loads(rendered)
    artifact_text = out_path.read_text()
    assert envelope["artifact_path"] == str(out_path)
    assert envelope["tokenizer"] == TOKENIZER
    assert envelope["tokens"] == _token_count(artifact_text)
