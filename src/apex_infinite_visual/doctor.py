"""Wrapper-facing launch diagnostics for the Hyperterminal surface.

The doctor runs display-safe readiness checks and returns pass/warn/fail
rows the QML surface can render directly. The check/report dataclasses and
the display-agnostic checks live in the shared diagnostic backend
(`apex_infinite.doctor`, ADR 0001 #6); this module adds the wrapper-only
PySide6 and display checks. Checks accept injectable dependencies so tests
never touch real providers, Codex, or displays.
"""

from __future__ import annotations

import importlib.util
import os
import shutil
from collections.abc import Callable, Mapping
from dataclasses import dataclass

from apex_infinite.doctor import (
    DOCTOR_FAIL,
    DOCTOR_PASS,
    DOCTOR_WARN,
    DoctorCheck,
    DoctorReport,
    check_codex_binary,
    check_config_resolution,
    check_history_db,
    check_optional_module,
    check_project_path,
    doctor_event_rows,
)

__all__ = [
    "DOCTOR_FAIL",
    "DOCTOR_PASS",
    "DOCTOR_WARN",
    "DoctorCheck",
    "DoctorContext",
    "DoctorReport",
    "doctor_event_rows",
    "run_doctor",
]


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
        check_config_resolution(context.config_path or None, env=context.environ()),
        check_project_path(context.project_path),
        check_codex_binary(context.codex_binary or "codex", which=context.which),
        check_history_db(),
        check_optional_module(
            "PySide6",
            "PySide6 runtime",
            module_available=context.has_module,
            fix_hint="Install the visual extra: pip install 'apex-infinite[visual]'",
        ),
        _check_display(context),
    )
    return DoctorReport(checks=checks)


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
        fix_hint="Run inside a graphical session or set QT_QPA_PLATFORM=offscreen "
        "for smoke tests.",
    )
