"""Production-like local launcher tests."""

import json
import os
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
LAUNCHER = REPO_ROOT / "scripts" / "run-production.sh"


def make_fake_cli(tmp_path):
    """Create a CLI double that records each argument vector as JSON."""
    bin_dir = tmp_path / "fake bin"
    bin_dir.mkdir()
    fake_cli = bin_dir / "apex-infinite"
    fake_cli.write_text(
        """#!/usr/bin/env python3
import json
import os
import sys

with open(os.environ["APEX_PRODUCTION_TEST_CALLS"], "a", encoding="ascii") as handle:
    handle.write(json.dumps(sys.argv[1:], ensure_ascii=True) + "\\n")

event_path = sys.argv[sys.argv.index("--event-stream") + 1]
with open(event_path, "w", encoding="ascii") as handle:
    handle.write("{}\\n")

if "--doctor" in sys.argv and os.environ.get("APEX_PRODUCTION_TEST_FAIL_DOCTOR"):
    raise SystemExit(7)
""",
        encoding="ascii",
    )
    fake_cli.chmod(0o755)
    return fake_cli


def launcher_env(tmp_path, *, initialized=True):
    """Build an isolated production-launch environment."""
    project = tmp_path / "project with spaces"
    project.mkdir()
    if initialized:
        (project / ".spec_system").mkdir()
    config = tmp_path / "config with spaces" / "config.yaml"
    config.parent.mkdir()
    config.write_text("provider: test\n", encoding="ascii")
    calls = tmp_path / "calls.jsonl"
    log_dir = tmp_path / "state with spaces" / "logs"

    env = os.environ.copy()
    for name in (
        "PROJECT",
        "CONFIG",
        "START",
        "MAX_ITERATIONS",
        "LOG_DIR",
        "APEX_INFINITE_CONFIG",
        "APEX_PRODUCTION_START_COMMAND",
    ):
        env.pop(name, None)
    env.update(
        {
            "HOME": str(tmp_path / "home"),
            "APEX_PRODUCTION_PATH": str(project),
            "APEX_PRODUCTION_CONFIG": str(config),
            "APEX_PRODUCTION_LOG_DIR": str(log_dir),
            "APEX_PRODUCTION_CLI": str(make_fake_cli(tmp_path)),
            "APEX_PRODUCTION_TEST_CALLS": str(calls),
        }
    )
    return env, project, config, calls, log_dir


def run_launcher(env):
    """Run the launcher without contacting a real provider or Codex."""
    return subprocess.run(
        [str(LAUNCHER)],
        cwd=REPO_ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )


def read_calls(path):
    """Read fake CLI argument vectors."""
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="ascii").splitlines()]


def test_launcher_requires_explicit_project(tmp_path):
    env, _project, _config, calls, _log_dir = launcher_env(tmp_path)
    env.pop("APEX_PRODUCTION_PATH")

    result = run_launcher(env)

    assert result.returncode == 2
    assert "set PROJECT=/absolute/path" in result.stderr
    assert read_calls(calls) == []


def test_launcher_requires_initialized_project(tmp_path):
    env, project, _config, calls, _log_dir = launcher_env(tmp_path, initialized=False)

    result = run_launcher(env)

    assert result.returncode == 2
    assert f"missing {project}/.spec_system" in result.stderr
    assert read_calls(calls) == []


@pytest.mark.parametrize("value", ["0", "-1", "many"])
def test_launcher_rejects_invalid_iteration_limit(tmp_path, value):
    env, _project, _config, calls, _log_dir = launcher_env(tmp_path)
    env["APEX_PRODUCTION_MAX_ITERATIONS"] = value

    result = run_launcher(env)

    assert result.returncode == 2
    assert "MAX_ITERATIONS must be a positive integer" in result.stderr
    assert read_calls(calls) == []


@pytest.mark.parametrize(
    ("start_value", "expected_start"),
    [(None, None), ("plansession", "plansession")],
)
def test_launcher_gates_then_starts_live_run(tmp_path, start_value, expected_start):
    env, project, config, calls_path, log_dir = launcher_env(tmp_path)
    env["APEX_PRODUCTION_MAX_ITERATIONS"] = "12"
    if start_value is not None:
        env["APEX_PRODUCTION_START_COMMAND"] = start_value

    result = run_launcher(env)

    assert result.returncode == 0, result.stderr
    calls = read_calls(calls_path)
    assert len(calls) == 2
    doctor, live = calls

    assert doctor[doctor.index("--config") + 1] == str(config)
    assert doctor[doctor.index("--path") + 1] == str(project)
    assert "--doctor" in doctor
    assert "--check-provider-chat" in doctor

    assert live[live.index("--config") + 1] == str(config)
    assert live[live.index("--path") + 1] == str(project)
    assert live[live.index("--max-iterations") + 1] == "12"
    assert "--check-provider-chat" in live
    assert "--dry-run" not in live
    assert "--skip-provider-check" not in live
    assert "--machine-output" not in live

    if expected_start is None:
        assert "--start" not in live
    else:
        assert live[live.index("--start") + 1] == expected_start

    preflight_log = Path(doctor[doctor.index("--event-stream") + 1])
    run_log = Path(live[live.index("--event-stream") + 1])
    assert preflight_log.parent == log_dir
    assert preflight_log.name.startswith("preflight-")
    assert run_log.parent == log_dir
    assert run_log.name.startswith("run-")
    assert preflight_log != run_log
    assert preflight_log.stat().st_mode & 0o777 == 0o600
    assert run_log.stat().st_mode & 0o777 == 0o600
    assert log_dir.is_dir()


def test_launcher_stops_when_doctor_fails(tmp_path):
    env, _project, _config, calls_path, _log_dir = launcher_env(tmp_path)
    env["APEX_PRODUCTION_TEST_FAIL_DOCTOR"] = "1"

    result = run_launcher(env)

    assert result.returncode == 2
    assert "live run was not started" in result.stderr
    calls = read_calls(calls_path)
    assert len(calls) == 1
    assert "--doctor" in calls[0]


def test_makefile_exposes_production_launcher():
    makefile = (REPO_ROOT / "Makefile").read_text(encoding="ascii")
    manifest = (REPO_ROOT / "MANIFEST.in").read_text(encoding="ascii")

    assert ".PHONY: production " in makefile
    assert "production:\n\t@./scripts/run-production.sh\n" in makefile
    assert "include Makefile\n" in manifest


def test_make_target_exports_production_variables(tmp_path):
    env, project, config, calls_path, log_dir = launcher_env(tmp_path)
    for name in (
        "APEX_PRODUCTION_PATH",
        "APEX_PRODUCTION_CONFIG",
        "APEX_PRODUCTION_LOG_DIR",
    ):
        env.pop(name)

    result = subprocess.run(
        [
            "make",
            "-s",
            "production",
            f"PROJECT={project}",
            f"CONFIG={config}",
            "START=validate",
            "MAX_ITERATIONS=3",
            f"LOG_DIR={log_dir}",
        ],
        cwd=REPO_ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    calls = read_calls(calls_path)
    assert len(calls) == 2
    live = calls[1]
    assert live[live.index("--path") + 1] == str(project)
    assert live[live.index("--config") + 1] == str(config)
    assert live[live.index("--start") + 1] == "validate"
    assert live[live.index("--max-iterations") + 1] == "3"
    assert Path(live[live.index("--event-stream") + 1]).parent == log_dir
