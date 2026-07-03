"""Structured logging helpers for local Apex Infinite diagnostics."""

from __future__ import annotations

import datetime as dt
import json
import logging
import math
import sys
import traceback
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

import structlog

LOG_DIR = Path("logs")
DEFAULT_LOG_LEVEL = "INFO"
REDACTED = "[redacted]"
SECRET_KEY_PARTS = (
    "api_key",
    "apikey",
    "authorization",
    "credential",
    "passwd",
    "password",
    "secret",
    "token",
)

JsonScalar = str | int | float | bool | None
JsonValue = JsonScalar | list["JsonValue"] | dict[str, "JsonValue"]


def configure_logging(
    log_dir: str | Path = LOG_DIR,
    level: str = DEFAULT_LOG_LEVEL,
) -> Any:
    """Configure structlog and return the package logger."""
    resolved_log_dir = Path(log_dir)
    resolved_log_dir.mkdir(parents=True, exist_ok=True)
    numeric_level = _numeric_level(level)
    logging.basicConfig(level=numeric_level, format="%(message)s")
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.TimeStamper(fmt="iso", utc=True),
            structlog.processors.add_log_level,
            structlog.processors.JSONRenderer(sort_keys=True),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(numeric_level),
        logger_factory=structlog.PrintLoggerFactory(file=sys.stderr),
        cache_logger_on_first_use=True,
    )
    return structlog.get_logger("apex_infinite").bind(log_dir=str(resolved_log_dir))


def write_last_error(
    error: BaseException,
    *,
    log_dir: str | Path = LOG_DIR,
    context: Mapping[str, object] | None = None,
) -> Path:
    """Write an AI-readable JSON file for the most recent captured error."""
    resolved_log_dir = Path(log_dir)
    resolved_log_dir.mkdir(parents=True, exist_ok=True)
    timestamp = _timestamp()
    payload = {
        "timestamp": timestamp,
        "level": "error",
        "msg": str(error),
        "error": {
            "type": error.__class__.__name__,
            "message": str(error),
            "stack": "".join(
                traceback.format_exception(type(error), error, error.__traceback__)
            ),
        },
        "context": _safe_mapping(context or {}),
    }
    path = resolved_log_dir / f"last_error_{timestamp}.json"
    path.write_text(
        f"{json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True)}\n",
        encoding="ascii",
    )
    return path


def _numeric_level(level: str) -> int:
    numeric_level = getattr(logging, level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Unsupported log level: {level}")
    return numeric_level


def _timestamp() -> str:
    timestamp = dt.datetime.now(dt.timezone.utc).isoformat(timespec="milliseconds")
    return timestamp.replace("+00:00", "Z")


def _safe_mapping(mapping: Mapping[str, object]) -> dict[str, JsonValue]:
    return {
        str(key): REDACTED if _is_secret_key(str(key)) else _safe_json_value(value)
        for key, value in mapping.items()
    }


def _safe_json_value(value: object) -> JsonValue:
    if value is None or isinstance(value, (str, int, bool)):
        return value
    if isinstance(value, float):
        return value if math.isfinite(value) else repr(value)
    if isinstance(value, Mapping):
        return _safe_mapping(value)
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [_safe_json_value(item) for item in value]
    return repr(value)


def _is_secret_key(key: str) -> bool:
    normalized = key.lower().replace("-", "_")
    return any(secret_part in normalized for secret_part in SECRET_KEY_PARTS)
