"""Structured logging configuration tests."""

import json

from apex_infinite.logging_config import configure_logging, write_last_error


def test_configure_logging_creates_log_directory(tmp_path):
    logger = configure_logging(tmp_path)

    logger.info("audit_logger_initialized", check="observability")

    assert tmp_path.exists()


def test_write_last_error_creates_ai_readable_json(tmp_path):
    try:
        raise RuntimeError("audit validation failed")
    except RuntimeError as exc:
        path = write_last_error(
            exc,
            log_dir=tmp_path,
            context={
                "stage": "audit",
                "api_key": "secret-value",
                "details": {"attempt": 1, "items": ["formatter", "tests"]},
            },
        )

    payload = json.loads(path.read_text(encoding="ascii"))

    assert path.name.startswith("last_error_")
    assert payload["level"] == "error"
    assert payload["msg"] == "audit validation failed"
    assert payload["error"]["type"] == "RuntimeError"
    assert "RuntimeError: audit validation failed" in payload["error"]["stack"]
    assert payload["context"] == {
        "api_key": "[redacted]",
        "details": {"attempt": 1, "items": ["formatter", "tests"]},
        "stage": "audit",
    }
