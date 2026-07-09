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


def make_fake_visual(tmp_path):
    """Create a visual-wrapper double that records its argument vector."""
    bin_dir = tmp_path / "fake bin"
    bin_dir.mkdir(exist_ok=True)
    fake_visual = bin_dir / "apex-infinite-visual"
    fake_visual.write_text(
        """#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path

preflight_calls = Path(os.environ["APEX_PRODUCTION_TEST_CALLS"])
if not preflight_calls.is_file() or not preflight_calls.read_text(encoding="ascii"):
    raise SystemExit(9)

with open(
    os.environ["APEX_PRODUCTION_TEST_VISUAL_CALLS"], "a", encoding="ascii"
) as handle:
    handle.write(json.dumps(sys.argv[1:], ensure_ascii=True) + "\\n")
""",
        encoding="ascii",
    )
    fake_visual.chmod(0o755)
    return fake_visual


def visual_calls_path(cli_calls_path):
    """Return the visual double's recording path for one launcher fixture."""
    return cli_calls_path.parent / "visual-calls.jsonl"


def launcher_env(tmp_path, *, initialized=True):
    """Build an isolated production-launch environment."""
    home = tmp_path / "home"
    home.mkdir()
    project = tmp_path / "project with spaces"
    project.mkdir()
    if initialized:
        (project / ".spec_system").mkdir()
    config = tmp_path / "config with spaces" / "config.yaml"
    config.parent.mkdir()
    config.write_text("provider: test\n", encoding="ascii")
    calls = tmp_path / "cli-calls.jsonl"
    visual_calls = visual_calls_path(calls)
    log_dir = tmp_path / "state with spaces" / "logs"

    env = os.environ.copy()
    for name in (
        "PROJECT",
        "CONFIG",
        "START",
        "MAX_ITERATIONS",
        "LOG_DIR",
        "APEX_INFINITE_CONFIG",
        "APEX_INFINITE_DEFAULT_PROJECT",
        "APEX_PRODUCTION_PATH",
        "APEX_PRODUCTION_CONFIG",
        "APEX_PRODUCTION_LOG_DIR",
        "APEX_PRODUCTION_MAX_ITERATIONS",
        "APEX_PRODUCTION_START_COMMAND",
        "APEX_PRODUCTION_VISUAL",
        "APEX_PRODUCTION_TEST_FAIL_DOCTOR",
        "APEX_PRODUCTION_TEST_VISUAL_CALLS",
    ):
        env.pop(name, None)
    env.update(
        {
            "HOME": str(home),
            "XDG_CONFIG_HOME": str(tmp_path / "xdg"),
            "APEX_PRODUCTION_PATH": str(project),
            "APEX_PRODUCTION_CONFIG": str(config),
            "APEX_PRODUCTION_LOG_DIR": str(log_dir),
            "APEX_PRODUCTION_CLI": str(make_fake_cli(tmp_path)),
            "APEX_PRODUCTION_VISUAL": str(make_fake_visual(tmp_path)),
            "APEX_PRODUCTION_TEST_CALLS": str(calls),
            "APEX_PRODUCTION_TEST_VISUAL_CALLS": str(visual_calls),
        }
    )
    return env, project, config, calls, log_dir


def run_launcher(env, cwd=None):
    """Run the launcher from an isolated cwd without real provider calls."""
    working_dir = Path(cwd) if cwd is not None else Path(env["HOME"]).parent / "cwd"
    working_dir.mkdir(parents=True, exist_ok=True)
    return subprocess.run(
        [str(LAUNCHER)],
        cwd=working_dir,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )


def read_calls(path):
    """Read fake executable argument vectors."""
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="ascii").splitlines()]


def make_initialized_project(tmp_path, name):
    """Create another initialized project for precedence tests."""
    project = tmp_path / name
    project.mkdir(parents=True)
    (project / ".spec_system").mkdir()
    return project


def write_config_default(config, project):
    """Write the minimal launcher config with one default project."""
    config.write_text(
        f'provider: test\ndefaults:\n  project: "{project}"\n',
        encoding="ascii",
    )


def assert_recorded_paths(calls_path, project, config):
    """Assert doctor and visual calls use the same resolved paths."""
    cli_calls = read_calls(calls_path)
    visual_calls = read_calls(visual_calls_path(calls_path))
    assert len(cli_calls) == 1
    assert len(visual_calls) == 1
    for call in (cli_calls[0], visual_calls[0]):
        assert call[call.index("--path") + 1] == str(project)
        assert call[call.index("--config") + 1] == str(config)


def assert_no_calls(calls_path):
    """Assert neither production executable was invoked."""
    assert read_calls(calls_path) == []
    assert read_calls(visual_calls_path(calls_path)) == []


def test_launcher_requires_configured_project(tmp_path):
    env, _project, _config, calls, _log_dir = launcher_env(tmp_path)
    env.pop("APEX_PRODUCTION_PATH")

    result = run_launcher(env)

    assert result.returncode == 2
    assert "project not configured" in result.stderr
    assert "APEX_INFINITE_DEFAULT_PROJECT" in result.stderr
    assert_no_calls(calls)


def test_launcher_uses_yaml_default_project(tmp_path):
    env, project, config, calls, _log_dir = launcher_env(tmp_path)
    env.pop("APEX_PRODUCTION_PATH")
    write_config_default(config, project)

    result = run_launcher(env)

    assert result.returncode == 0, result.stderr
    assert_recorded_paths(calls, project, config)


def test_launcher_uses_cwd_dotenv_default_project(tmp_path):
    env, project, config, calls, _log_dir = launcher_env(tmp_path)
    env.pop("APEX_PRODUCTION_PATH")
    cwd = tmp_path / "isolated cwd"
    cwd.mkdir()
    (cwd / ".env").write_text(
        f'APEX_INFINITE_DEFAULT_PROJECT="{project}"\n', encoding="ascii"
    )

    result = run_launcher(env, cwd=cwd)

    assert result.returncode == 0, result.stderr
    assert_recorded_paths(calls, project, config)


def test_launcher_prefers_config_dotenv_over_cwd_dotenv(tmp_path):
    env, project, config, calls, _log_dir = launcher_env(tmp_path)
    env.pop("APEX_PRODUCTION_PATH")
    cwd_project = make_initialized_project(tmp_path, "cwd project")
    cwd = tmp_path / "isolated cwd"
    cwd.mkdir()
    (cwd / ".env").write_text(
        f'APEX_INFINITE_DEFAULT_PROJECT="{cwd_project}"\n', encoding="ascii"
    )
    (config.parent / ".env").write_text(
        f'APEX_INFINITE_DEFAULT_PROJECT="{project}"\n', encoding="ascii"
    )

    result = run_launcher(env, cwd=cwd)

    assert result.returncode == 0, result.stderr
    assert_recorded_paths(calls, project, config)


def test_launcher_environment_default_wins_yaml_default(tmp_path):
    env, project, config, calls, _log_dir = launcher_env(tmp_path)
    env.pop("APEX_PRODUCTION_PATH")
    yaml_project = make_initialized_project(tmp_path, "yaml project")
    env["APEX_INFINITE_DEFAULT_PROJECT"] = str(project)
    write_config_default(config, yaml_project)

    result = run_launcher(env)

    assert result.returncode == 0, result.stderr
    assert_recorded_paths(calls, project, config)


def test_launcher_project_override_wins_default_sources(tmp_path):
    env, project, config, calls, _log_dir = launcher_env(tmp_path)
    env.pop("APEX_PRODUCTION_PATH")
    env_project = make_initialized_project(tmp_path, "environment project")
    yaml_project = make_initialized_project(tmp_path, "yaml project")
    env["PROJECT"] = str(project)
    env["APEX_INFINITE_DEFAULT_PROJECT"] = str(env_project)
    write_config_default(config, yaml_project)

    result = run_launcher(env)

    assert result.returncode == 0, result.stderr
    assert_recorded_paths(calls, project, config)


def test_launcher_production_path_wins_project_override(tmp_path):
    env, project, config, calls, _log_dir = launcher_env(tmp_path)
    project_override = make_initialized_project(tmp_path, "project override")
    env["PROJECT"] = str(project_override)

    result = run_launcher(env)

    assert result.returncode == 0, result.stderr
    assert_recorded_paths(calls, project, config)


def test_launcher_requires_initialized_project(tmp_path):
    env, project, _config, calls, _log_dir = launcher_env(tmp_path, initialized=False)

    result = run_launcher(env)

    assert result.returncode == 2
    assert f"missing {project}/.spec_system" in result.stderr
    assert_no_calls(calls)


def test_launcher_rejects_uninitialized_yaml_default(tmp_path):
    env, project, config, calls, _log_dir = launcher_env(tmp_path, initialized=False)
    env.pop("APEX_PRODUCTION_PATH")
    write_config_default(config, project)

    result = run_launcher(env)

    assert result.returncode == 2
    assert f"missing {project}/.spec_system" in result.stderr
    assert_no_calls(calls)


def test_launcher_rejects_relative_default_project(tmp_path):
    env, _project, _config, calls, _log_dir = launcher_env(tmp_path)
    env.pop("APEX_PRODUCTION_PATH")
    cwd = tmp_path / "isolated cwd"
    relative_project = Path("relative project")
    make_initialized_project(cwd, str(relative_project))
    env["APEX_INFINITE_DEFAULT_PROJECT"] = str(relative_project)

    result = run_launcher(env, cwd=cwd)

    assert result.returncode == 2
    assert "PROJECT must be an absolute path: relative project" in result.stderr
    assert_no_calls(calls)


def test_launcher_expands_home_in_environment_default(tmp_path):
    env, _project, config, calls, _log_dir = launcher_env(tmp_path)
    env.pop("APEX_PRODUCTION_PATH")
    home_project = make_initialized_project(Path(env["HOME"]), "default project")
    env["APEX_INFINITE_DEFAULT_PROJECT"] = "~/default project"

    result = run_launcher(env)

    assert result.returncode == 0, result.stderr
    assert_recorded_paths(calls, home_project, config)


def test_launcher_uses_packaged_config_when_xdg_config_is_absent(tmp_path):
    env, project, _config, calls, _log_dir = launcher_env(tmp_path)
    env.pop("APEX_PRODUCTION_CONFIG")
    packaged_config = REPO_ROOT / "src" / "apex_infinite" / "config.yaml"

    result = run_launcher(env)

    assert result.returncode == 0, result.stderr
    assert_recorded_paths(calls, project, packaged_config)


def test_launcher_explicit_missing_config_fails_fast(tmp_path):
    env, _project, _config, calls, _log_dir = launcher_env(tmp_path)
    missing_config = tmp_path / "missing" / "config.yaml"
    env["APEX_PRODUCTION_CONFIG"] = str(missing_config)

    result = run_launcher(env)

    assert result.returncode == 2
    assert f"config not found: {missing_config}" in result.stderr
    assert_no_calls(calls)


def test_launcher_fails_when_visual_executable_is_missing(tmp_path):
    env, _project, _config, calls, _log_dir = launcher_env(tmp_path)
    missing_visual = tmp_path / "missing" / "apex-infinite-visual"
    env["APEX_PRODUCTION_VISUAL"] = str(missing_visual)

    result = run_launcher(env)

    assert result.returncode == 2
    assert f"visual executable not found: {missing_visual}" in result.stderr
    assert_no_calls(calls)


@pytest.mark.parametrize("value", ["0", "-1", "many"])
def test_launcher_rejects_invalid_iteration_limit(tmp_path, value):
    env, _project, _config, calls, _log_dir = launcher_env(tmp_path)
    env["APEX_PRODUCTION_MAX_ITERATIONS"] = value

    result = run_launcher(env)

    assert result.returncode == 2
    assert "MAX_ITERATIONS must be a positive integer" in result.stderr
    assert_no_calls(calls)


@pytest.mark.parametrize(
    ("start_value", "expected_start"),
    [(None, ""), ("plansession", "plansession")],
)
def test_launcher_gates_then_opens_live_visual(tmp_path, start_value, expected_start):
    env, project, config, calls_path, log_dir = launcher_env(tmp_path)
    env["APEX_PRODUCTION_MAX_ITERATIONS"] = "12"
    if start_value is not None:
        env["APEX_PRODUCTION_START_COMMAND"] = start_value

    result = run_launcher(env)

    assert result.returncode == 0, result.stderr
    cli_calls = read_calls(calls_path)
    visual_calls = read_calls(visual_calls_path(calls_path))
    assert len(cli_calls) == 1
    assert len(visual_calls) == 1
    doctor = cli_calls[0]
    visual = visual_calls[0]

    assert doctor[doctor.index("--config") + 1] == str(config)
    assert doctor[doctor.index("--path") + 1] == str(project)
    assert "--doctor" in doctor
    assert "--doctor-visual" in doctor
    assert "--check-provider-chat" in doctor

    assert visual[visual.index("--config") + 1] == str(config)
    assert visual[visual.index("--path") + 1] == str(project)
    assert visual[visual.index("--max-iterations") + 1] == "12"
    assert visual[visual.index("--start-command") + 1] == expected_start
    assert visual[visual.index("--run-log-dir") + 1] == str(log_dir)
    assert "--launch-cli" in visual
    assert "--require-initialized-project" in visual
    assert "--no-restore-profile" in visual
    assert "--dry-run" not in visual
    assert "--reduced-logging" not in visual

    preflight_log = Path(doctor[doctor.index("--event-stream") + 1])
    assert preflight_log.parent == log_dir
    assert preflight_log.name.startswith("preflight-")
    assert preflight_log.stat().st_mode & 0o777 == 0o600
    assert log_dir.is_dir()


def test_launcher_stops_when_doctor_fails(tmp_path):
    env, _project, _config, calls_path, _log_dir = launcher_env(tmp_path)
    env["APEX_PRODUCTION_TEST_FAIL_DOCTOR"] = "1"

    result = run_launcher(env)

    assert result.returncode == 2
    assert "visual console was not started" in result.stderr
    calls = read_calls(calls_path)
    assert len(calls) == 1
    assert "--doctor" in calls[0]
    assert "--doctor-visual" in calls[0]
    assert read_calls(visual_calls_path(calls_path)) == []


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
    cli_calls = read_calls(calls_path)
    visual_calls = read_calls(visual_calls_path(calls_path))
    assert len(cli_calls) == 1
    assert len(visual_calls) == 1
    visual = visual_calls[0]
    assert visual[visual.index("--path") + 1] == str(project)
    assert visual[visual.index("--config") + 1] == str(config)
    assert visual[visual.index("--start-command") + 1] == "validate"
    assert visual[visual.index("--max-iterations") + 1] == "3"
    assert visual[visual.index("--run-log-dir") + 1] == str(log_dir)
    assert "--launch-cli" in visual
