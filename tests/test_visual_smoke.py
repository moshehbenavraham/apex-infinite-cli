"""Offscreen smoke tests for the real Hyperterminal QML surface."""

import importlib.util
import os
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.skipif(
    importlib.util.find_spec("PySide6") is None,
    reason="PySide6 is not installed",
)

REPO_ROOT = Path(__file__).resolve().parent.parent
SMOKE_SCRIPT = REPO_ROOT / "scripts" / "visual_screenshot_smoke.py"


def offscreen_env(tmp_path):
    """Return an isolated offscreen Qt environment."""
    env = dict(os.environ)
    env["QT_QPA_PLATFORM"] = "offscreen"
    env["QT_QUICK_BACKEND"] = "software"
    env["XDG_CONFIG_HOME"] = str(tmp_path / "cfg")
    env["XDG_STATE_HOME"] = str(tmp_path / "state")
    return env


def test_offscreen_launch_exits_clean(tmp_path):
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "apex_infinite_visual",
            "--dry-run",
            "--auto-close-ms",
            "1400",
            "--path",
            str(tmp_path),
            "--no-restore-profile",
        ],
        env=offscreen_env(tmp_path),
        capture_output=True,
        text=True,
        timeout=90,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert ".qml" not in result.stderr


@pytest.mark.parametrize("theme", ["apex-reactor", "crt-green", "plain"])
def test_offscreen_screenshot_is_nonblank(tmp_path, theme):
    out = tmp_path / f"smoke-{theme}.png"
    result = subprocess.run(
        [
            sys.executable,
            str(SMOKE_SCRIPT),
            "--theme",
            theme,
            "--out",
            str(out),
        ],
        env=offscreen_env(tmp_path),
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )

    assert result.returncode == 0, result.stderr + result.stdout
    assert "SMOKE OK" in result.stdout
    assert out.exists() and out.stat().st_size > 1000
