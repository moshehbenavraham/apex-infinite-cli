"""Wrapper-facing launch diagnostics for the Hyperterminal surface.

The doctor runs display-safe readiness checks and returns pass/warn/fail
rows the QML surface can render directly. Checks accept injectable
dependencies so tests never touch real providers, Codex, or displays.
"""

from __future__ import annotations

import importlib.util
import os
import shutil
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from pathlib import Path

DOCTOR_PASS = "pass"
DOCTOR_WARN = "warn"
DOCTOR_FAIL = "fail"

_SEVERITY_ORDER = (DOCTOR_PASS, DOCTOR_WARN, DOCTOR_FAIL)


@dataclass(frozen=True)
class DoctorCheck:
    """One display-safe diagnostic result row."""

    check_id: str
    label: str
    status: str
    detail: str


@dataclass(frozen=True)
class DoctorReport:
    """Aggregate doctor outcome for the visual surface."""

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


@dataclass(frozen=True)
class DoctorContext:  # pylint: disable=too-many-instance-attributes
    """Injectable dependencies for doctor checks."""

    project_path: str = ""
    config_path: str = ""
    codex_binary: str = "codex"
    env: Mapping[str, str] | None = None
    which: Callable[[str], str | None] = shutil.which
    module_available: Callable[[str], bool] | None = None

    def environ(self) -> Mapping[str, str]:
        """Return the effective environment mapping."""
        return self.env if self.env is not None else os.environ

    def has_module(self, name: str) -> bool:
        """Return whether an optional module can be imported."""
        if self.module_available is not None:
            return self.module_available(name)
        return importlib.util.find_spec(name) is not None


def run_doctor(context: DoctorContext) -> DoctorReport:
    """Run every launch-readiness check."""
    checks = (
        _check_config(context),
        _check_project(context),
        _check_codex(context),
        _check_history_dir(),
        _check_pyside6(context),
        _check_display(context),
    )
    return DoctorReport(checks=checks)


def doctor_event_rows(report: DoctorReport) -> list[dict[str, object]]:
    """Return registered-event payloads for each doctor check."""
    return [
        {
            "check_id": check.check_id,
            "label": check.label,
            "status": check.status,
            "detail": check.detail,
        }
        for check in report.checks
    ]


def _check_config(context: DoctorContext) -> DoctorCheck:
    label = "Shared CLI config"
    candidates = []
    if context.config_path:
        candidates.append(Path(os.path.expanduser(context.config_path)))
    else:
        candidates.append(Path.cwd() / "config.yaml")
    for candidate in candidates:
        if candidate.is_file():
            return DoctorCheck("config", label, DOCTOR_PASS, f"Found {candidate.name}.")
    if context.config_path:
        return DoctorCheck(
            "config", label, DOCTOR_FAIL, "Configured config file was not found."
        )
    return DoctorCheck(
        "config",
        label,
        DOCTOR_WARN,
        "No local config.yaml; the packaged default will be used.",
    )


def _check_project(context: DoctorContext) -> DoctorCheck:
    label = "Project path"
    if not context.project_path:
        return DoctorCheck("project", label, DOCTOR_WARN, "No project selected yet.")
    path = Path(os.path.expanduser(context.project_path))
    if path.is_dir():
        detail = "Project directory exists."
        if (path / ".spec_system").is_dir():
            detail = "Project directory exists with an Apex Spec system."
        return DoctorCheck("project", label, DOCTOR_PASS, detail)
    return DoctorCheck(
        "project", label, DOCTOR_FAIL, "Project directory was not found."
    )


def _check_codex(context: DoctorContext) -> DoctorCheck:
    label = "Codex binary"
    binary = context.codex_binary or "codex"
    resolved = context.which(binary)
    if resolved:
        return DoctorCheck("codex", label, DOCTOR_PASS, f"Found {binary} on PATH.")
    return DoctorCheck("codex", label, DOCTOR_FAIL, f"{binary} was not found on PATH.")


def _check_history_dir() -> DoctorCheck:
    label = "History database"
    history_dir = Path.home() / ".apex-infinite"
    if history_dir.is_dir():
        if os.access(history_dir, os.W_OK):
            return DoctorCheck(
                "history", label, DOCTOR_PASS, "History directory is writable."
            )
        return DoctorCheck(
            "history", label, DOCTOR_FAIL, "History directory is not writable."
        )
    return DoctorCheck(
        "history",
        label,
        DOCTOR_WARN,
        "History directory will be created on first run.",
    )


def _check_pyside6(context: DoctorContext) -> DoctorCheck:
    label = "PySide6 runtime"
    if context.has_module("PySide6"):
        return DoctorCheck("pyside6", label, DOCTOR_PASS, "PySide6 is installed.")
    return DoctorCheck(
        "pyside6",
        label,
        DOCTOR_FAIL,
        "PySide6 is not installed. Install the visual extra.",
    )


def _check_display(context: DoctorContext) -> DoctorCheck:
    label = "Display backend"
    env = context.environ()
    platform = env.get("QT_QPA_PLATFORM", "").strip()
    if platform in {"offscreen", "minimal"}:
        return DoctorCheck(
            "display", label, DOCTOR_WARN, f"Qt platform forced to {platform}."
        )
    if env.get("WAYLAND_DISPLAY") or env.get("DISPLAY"):
        return DoctorCheck(
            "display", label, DOCTOR_PASS, "A display server is available."
        )
    return DoctorCheck(
        "display",
        label,
        DOCTOR_FAIL,
        "No DISPLAY or WAYLAND_DISPLAY environment was found.",
    )
