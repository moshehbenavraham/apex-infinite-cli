"""Shared diagnostic backend for the terminal and visual doctors.

This module holds the check/report dataclasses and every display-agnostic
readiness check. It stays standard-library-only so the optional visual
wrapper can import it without terminal rendering or provider dependencies
(ADR 0001 #6). Checks accept injectable callables so tests never touch real
binaries, providers, or displays.
"""

from __future__ import annotations

import os
import shutil
import sys
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from pathlib import Path

from apex_infinite.config_resolution import SOURCE_PACKAGED, resolve_config

DOCTOR_PASS = "pass"
DOCTOR_WARN = "warn"
DOCTOR_FAIL = "fail"

_SEVERITY_ORDER = (DOCTOR_PASS, DOCTOR_WARN, DOCTOR_FAIL)

MIN_PYTHON_VERSION = (3, 10)
VERSION_PROBE_TIMEOUT = 10


@dataclass(frozen=True)
class DoctorCheck:
    """One display-safe diagnostic result row."""

    check_id: str
    label: str
    status: str
    detail: str
    fix_hint: str = ""


@dataclass(frozen=True)
class DoctorReport:
    """Aggregate doctor outcome."""

    checks: tuple[DoctorCheck, ...]

    @property
    def status(self) -> str:
        """Return the worst check status."""
        worst = DOCTOR_PASS
        for check in self.checks:
            if _SEVERITY_ORDER.index(check.status) > _SEVERITY_ORDER.index(worst):
                worst = check.status
        return worst

    @property
    def launch_ready(self) -> bool:
        """Return whether a run can start."""
        return all(check.status != DOCTOR_FAIL for check in self.checks)

    def counts(self) -> dict[str, int]:
        """Return pass/warn/fail counts."""
        result = {DOCTOR_PASS: 0, DOCTOR_WARN: 0, DOCTOR_FAIL: 0}
        for check in self.checks:
            result[check.status] += 1
        return result


def check_python_version(
    version_info: tuple[int, int] | None = None,
) -> DoctorCheck:
    """Check the interpreter meets the supported Python floor."""
    current = version_info if version_info is not None else sys.version_info[:2]
    label = "Python version"
    detail = f"Running Python {current[0]}.{current[1]}."
    if current >= MIN_PYTHON_VERSION:
        return DoctorCheck("python", label, DOCTOR_PASS, detail)
    floor = ".".join(str(part) for part in MIN_PYTHON_VERSION)
    return DoctorCheck(
        "python",
        label,
        DOCTOR_FAIL,
        f"{detail} Python {floor}+ is required.",
        fix_hint=f"Install Python {floor} or newer and reinstall apex-infinite.",
    )


def check_config_resolution(
    explicit_path: str | None = None,
    env: Mapping[str, str] | None = None,
    cwd: Path | None = None,
) -> DoctorCheck:
    """Check the shared config resolution chain."""
    label = "Shared CLI config"
    resolved = resolve_config(explicit_path or None, env=env, cwd=cwd)
    if resolved is None:
        return DoctorCheck(
            "config",
            label,
            DOCTOR_FAIL,
            "No config file was found in the shared resolution chain.",
            fix_hint="Run: apex-infinite --setup",
        )
    if not resolved.exists:
        return DoctorCheck(
            "config",
            label,
            DOCTOR_FAIL,
            f"Selected config ({resolved.source}) was not found: {resolved.path}",
            fix_hint="Fix the --config/APEX_INFINITE_CONFIG path or run: "
            "apex-infinite --setup",
        )
    if resolved.source == SOURCE_PACKAGED:
        return DoctorCheck(
            "config",
            label,
            DOCTOR_WARN,
            "Using packaged defaults; no user-owned config exists yet.",
            fix_hint="Run: apex-infinite --setup",
        )
    return DoctorCheck(
        "config",
        label,
        DOCTOR_PASS,
        f"Resolved {resolved.path} ({resolved.source}).",
    )


def check_codex_binary(
    binary: str = "codex",
    which: Callable[[str], str | None] = shutil.which,
    version_probe: Callable[[str], str] | None = None,
) -> DoctorCheck:
    """Check the configured Codex binary resolves and report its version."""
    label = "Codex binary"
    name = binary or "codex"
    resolved = which(name)
    if not resolved:
        return DoctorCheck(
            "codex",
            label,
            DOCTOR_FAIL,
            f"{name} was not found on PATH.",
            fix_hint="Install the Codex CLI or set codex.binary in config.yaml.",
        )
    if version_probe is None:
        return DoctorCheck("codex", label, DOCTOR_PASS, f"Found {name} on PATH.")
    try:
        version = version_probe(name).strip().splitlines()[0]
    except Exception:  # pylint: disable=broad-exception-caught
        return DoctorCheck(
            "codex",
            label,
            DOCTOR_WARN,
            f"Found {name} on PATH but the version probe failed.",
            fix_hint=f"Run: {name} --version",
        )
    return DoctorCheck("codex", label, DOCTOR_PASS, f"Found {name} ({version}).")


def check_project_path(project_path: str) -> DoctorCheck:
    """Check the target project directory."""
    label = "Project path"
    if not project_path:
        return DoctorCheck(
            "project",
            label,
            DOCTOR_WARN,
            "No project selected yet.",
            fix_hint="Pass --path /path/to/project",
        )
    path = Path(os.path.expanduser(project_path))
    if path.is_dir():
        return DoctorCheck("project", label, DOCTOR_PASS, "Project directory exists.")
    return DoctorCheck(
        "project",
        label,
        DOCTOR_FAIL,
        "Project directory was not found.",
        fix_hint="Pass --path with an existing project directory.",
    )


def check_spec_system(project_path: str) -> DoctorCheck:
    """Check for an Apex Spec system in the target project."""
    label = "Apex Spec system"
    if not project_path:
        return DoctorCheck(
            "spec_system", label, DOCTOR_WARN, "No project selected yet."
        )
    path = Path(os.path.expanduser(project_path))
    if (path / ".spec_system").is_dir():
        return DoctorCheck(
            "spec_system", label, DOCTOR_PASS, "Found .spec_system in the project."
        )
    return DoctorCheck(
        "spec_system",
        label,
        DOCTOR_WARN,
        "No .spec_system directory; workflow commands that need it will "
        "initialize or fail clearly.",
        fix_hint="Start with: apex-infinite --start initspec --dry-run",
    )


def check_history_db(db_dir: Path | None = None) -> DoctorCheck:
    """Check the SQLite history directory is usable."""
    label = "History database"
    history_dir = db_dir if db_dir is not None else Path.home() / ".apex-infinite"
    if history_dir.is_dir():
        if os.access(history_dir, os.W_OK):
            return DoctorCheck(
                "history", label, DOCTOR_PASS, "History directory is writable."
            )
        return DoctorCheck(
            "history",
            label,
            DOCTOR_FAIL,
            "History directory is not writable.",
            fix_hint=f"Run: chmod u+w {history_dir}",
        )
    parent = history_dir.parent
    if parent.is_dir() and os.access(parent, os.W_OK):
        return DoctorCheck(
            "history",
            label,
            DOCTOR_PASS,
            "History directory will be created on first run.",
        )
    return DoctorCheck(
        "history",
        label,
        DOCTOR_FAIL,
        "History directory cannot be created.",
        fix_hint=f"Ensure {parent} exists and is writable.",
    )


def check_event_stream_path(event_stream: str | None) -> DoctorCheck:
    """Check the requested event-stream output target."""
    label = "Event stream"
    if not event_stream:
        return DoctorCheck(
            "event_stream", label, DOCTOR_PASS, "Event stream is disabled."
        )
    if event_stream == "-":
        return DoctorCheck(
            "event_stream",
            label,
            DOCTOR_PASS,
            "Event stream writes JSONL to stdout (machine output).",
        )
    target = Path(os.path.expanduser(event_stream))
    probe_dir = target.parent if str(target.parent) else Path.cwd()
    if probe_dir.is_dir() and not os.access(probe_dir, os.W_OK):
        return DoctorCheck(
            "event_stream",
            label,
            DOCTOR_FAIL,
            f"Event stream directory is not writable: {probe_dir}",
            fix_hint="Choose a writable --event-stream path.",
        )
    return DoctorCheck(
        "event_stream", label, DOCTOR_PASS, f"Event stream file target: {target}"
    )


def check_optional_module(
    module_name: str,
    label: str,
    module_available: Callable[[str], bool] | None = None,
    fix_hint: str = "",
) -> DoctorCheck:
    """Check an optional dependency without importing it."""
    if module_available is None:
        import importlib.util  # pylint: disable=import-outside-toplevel

        def module_available(name: str) -> bool:
            return importlib.util.find_spec(name) is not None

    if module_available(module_name):
        return DoctorCheck(
            module_name.lower(), label, DOCTOR_PASS, f"{module_name} is installed."
        )
    return DoctorCheck(
        module_name.lower(),
        label,
        DOCTOR_FAIL,
        f"{module_name} is not installed.",
        fix_hint=fix_hint or f"Install the extra that provides {module_name}.",
    )


def doctor_event_rows(report: DoctorReport) -> list[dict[str, object]]:
    """Return registered-event payloads for each doctor check."""
    return [
        {
            "check_id": check.check_id,
            "label": _event_safe_text(check.label),
            "status": check.status,
            "detail": _event_safe_text(check.detail),
            "fix_hint": _event_safe_text(check.fix_hint),
        }
        for check in report.checks
    ]


def _event_safe_text(value: str) -> str:
    """Return event-safe text, suppressing unsafe display-only content."""
    if not value:
        return ""
    from apex_infinite.events import (  # pylint: disable=import-outside-toplevel
        EventStreamError,
        validate_payload,
    )

    try:
        validate_payload({"text": value})
    except EventStreamError:
        return ""
    return value
