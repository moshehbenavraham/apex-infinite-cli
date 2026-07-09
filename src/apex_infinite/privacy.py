"""First-run privacy notice and local-data disclosure helpers.

The notice is shown once per operator (tracked by an XDG state marker)
before the CLI stores local history or sends provider-bound prompts. The
module stays standard-library-only so the visual wrapper can reuse it.
"""

from __future__ import annotations

import os
from collections.abc import Mapping
from pathlib import Path

STATE_DIR_NAME = "apex-infinite"
MARKER_FILE_NAME = "privacy-notice-shown"

PRIVACY_NOTICE_ROWS: tuple[str, ...] = (
    "Workflow history (manager decisions, Codex output, timestamps, and "
    "project paths) is stored locally in ~/.apex-infinite/history.db.",
    "Prompts sent to the configured LLM provider can include recent "
    "history, the latest agent output, summaries, operator instructions, "
    "and project paths. Treat prompt content as sent to that provider.",
    "Do not include secrets, personal data, or customer data in prompts, "
    "CEO instructions, or target-project output you feed the workflow.",
    "Purge stored history at any time with: apex-infinite --purge-history "
    "(optionally scoped with --path).",
)


def xdg_state_home(env: Mapping[str, str] | None = None) -> Path:
    """Return the XDG state base honoring ``XDG_STATE_HOME`` when set."""
    environ = env if env is not None else os.environ
    base = environ.get("XDG_STATE_HOME", "").strip()
    if base:
        return Path(base).expanduser()
    return Path.home() / ".local" / "state"


def privacy_marker_path(env: Mapping[str, str] | None = None) -> Path:
    """Return the marker recording that the notice was shown."""
    return xdg_state_home(env) / STATE_DIR_NAME / MARKER_FILE_NAME


def privacy_notice_needed(env: Mapping[str, str] | None = None) -> bool:
    """Return whether the first-run privacy notice must be shown."""
    return not privacy_marker_path(env).is_file()


def mark_privacy_notice_shown(env: Mapping[str, str] | None = None) -> Path:
    """Persist the shown marker and return its path."""
    marker = privacy_marker_path(env)
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.write_text("shown\n", encoding="ascii")
    return marker
