"""Terminal doctor entrypoint and shared diagnostic backend tests."""

import json

from click.testing import CliRunner

import apex_infinite.cli as apex_infinite
from apex_infinite.doctor import (
    DOCTOR_FAIL,
    DOCTOR_PASS,
    DOCTOR_WARN,
    DoctorCheck,
    DoctorReport,
    check_event_stream_path,
    check_history_db,
    check_python_version,
    check_spec_system,
    doctor_event_rows,
)
from apex_infinite.events import validate_payload

from .test_cli_options import prepare_cli


def fake_codex_check(binary, **_kwargs):
    from apex_infinite.doctor import DoctorCheck

    return DoctorCheck(
        "codex", "Codex binary", DOCTOR_PASS, f"Found {binary} (codex 1.0 test)."
    )


def failing_codex_check(binary, **_kwargs):
    from apex_infinite.doctor import DoctorCheck

    return DoctorCheck(
        "codex",
        "Codex binary",
        DOCTOR_FAIL,
        f"{binary} was not found on PATH.",
        fix_hint="Install the Codex CLI.",
    )


def invoke_doctor(monkeypatch, tmp_path, extra_args=(), codex_check=fake_codex_check):
    config_path, project_path, captured = prepare_cli(monkeypatch, tmp_path)
    monkeypatch.setattr(apex_infinite, "check_codex_binary", codex_check)
    runner = CliRunner()
    result = runner.invoke(
        apex_infinite.main,
        [
            "--config",
            str(config_path),
            "--path",
            str(project_path),
            "--doctor",
            *extra_args,
        ],
    )
    return result, captured


def test_doctor_all_pass_exits_zero(monkeypatch, tmp_path):
    result, _captured = invoke_doctor(monkeypatch, tmp_path)

    assert result.exit_code == 0
    assert "Doctor" in result.output
    assert "PASS Python version" in result.output
    assert "PASS Provider connectivity" in result.output
    assert "fail" in result.output  # summary counts line


def test_doctor_missing_codex_fails_nonzero_with_fix_hint(monkeypatch, tmp_path):
    result, _captured = invoke_doctor(
        monkeypatch, tmp_path, codex_check=failing_codex_check
    )

    assert result.exit_code == 1
    assert "FAIL Codex binary" in result.output
    assert "Fix: Install the Codex CLI." in result.output


def test_doctor_provider_failure_is_a_fail_row(monkeypatch, tmp_path):
    def failing_preflight(_config, check_completion=False):
        raise apex_infinite.CliStartupError("Provider preflight failed: no route")

    config_path, project_path, _captured = prepare_cli(monkeypatch, tmp_path)
    monkeypatch.setattr(apex_infinite, "check_codex_binary", fake_codex_check)
    monkeypatch.setattr(apex_infinite, "run_provider_preflight", failing_preflight)

    result = CliRunner().invoke(
        apex_infinite.main,
        ["--config", str(config_path), "--path", str(project_path), "--doctor"],
    )

    assert result.exit_code == 1
    assert "FAIL Provider connectivity" in result.output


def test_doctor_skip_provider_check_warns_instead(monkeypatch, tmp_path):
    result, _captured = invoke_doctor(
        monkeypatch, tmp_path, extra_args=["--skip-provider-check"]
    )

    assert result.exit_code == 0
    assert "WARN Provider connectivity" in result.output


def test_doctor_uses_environment_default_project(monkeypatch, tmp_path):
    cwd = tmp_path / "cwd"
    cwd.mkdir()
    monkeypatch.chdir(cwd)
    config_path, project_path, _captured = prepare_cli(monkeypatch, tmp_path)
    monkeypatch.setenv("APEX_INFINITE_DEFAULT_PROJECT", str(project_path))
    monkeypatch.setattr(apex_infinite, "check_codex_binary", fake_codex_check)

    result = CliRunner().invoke(
        apex_infinite.main,
        ["--config", str(config_path), "--doctor", "--skip-provider-check"],
    )

    assert result.exit_code == 0, result.output
    assert "PASS Project path" in result.output
    assert "Project directory exists" in result.output


def test_doctor_machine_output_is_jsonl_only(monkeypatch, tmp_path):
    result, _captured = invoke_doctor(
        monkeypatch,
        tmp_path,
        extra_args=["--event-stream", "-", "--machine-output"],
    )

    assert result.exit_code == 0
    rows = [json.loads(line) for line in result.output.splitlines() if line.strip()]
    event_names = [row["event"] for row in rows]
    assert "doctor_started" in event_names
    assert "doctor_finished" in event_names
    assert event_names.count("doctor_check") >= 8
    finished = rows[event_names.index("doctor_finished")]["payload"]
    assert finished["launch_ready"] is True
    assert "Doctor" not in "".join(
        line for line in result.output.splitlines() if not line.startswith("{")
    )


def test_doctor_event_rows_suppress_unsafe_fix_hints():
    report = DoctorReport(
        checks=(
            DoctorCheck(
                "pyside6",
                "PySide6 runtime",
                DOCTOR_FAIL,
                "PySide6 is not installed.",
                fix_hint="Install: pip install 'apex-infinite[visual]'",
            ),
        )
    )

    rows = doctor_event_rows(report)

    assert rows[0]["fix_hint"] == ""
    validate_payload(rows[0])


def test_doctor_visual_flag_adds_pyside_row(monkeypatch, tmp_path):
    result, _captured = invoke_doctor(
        monkeypatch, tmp_path, extra_args=["--doctor-visual"]
    )

    assert "PySide6 runtime (visual extra)" in result.output


def test_doctor_visual_requires_doctor(monkeypatch, tmp_path):
    config_path, project_path, _captured = prepare_cli(monkeypatch, tmp_path)

    result = CliRunner().invoke(
        apex_infinite.main,
        ["--config", str(config_path), "--path", str(project_path), "--doctor-visual"],
    )

    assert result.exit_code == 2
    assert "--doctor-visual requires --doctor" in result.output


def test_doctor_rejects_check_provider_combo(monkeypatch, tmp_path):
    config_path, project_path, _captured = prepare_cli(monkeypatch, tmp_path)

    result = CliRunner().invoke(
        apex_infinite.main,
        [
            "--config",
            str(config_path),
            "--path",
            str(project_path),
            "--doctor",
            "--check-provider",
        ],
    )

    assert result.exit_code == 2
    assert "--doctor cannot be combined with --check-provider" in result.output


def test_doctor_malformed_config_reports_parse_failure(monkeypatch, tmp_path):
    project_path = tmp_path / "project"
    project_path.mkdir()
    bad_config = tmp_path / "config.yaml"
    bad_config.write_text("provider: [unclosed\n", encoding="ascii")
    monkeypatch.setattr(apex_infinite, "DB_DIR", tmp_path / "db")
    monkeypatch.setattr(apex_infinite, "DB_PATH", tmp_path / "db" / "history.db")
    monkeypatch.setattr(apex_infinite, "check_codex_binary", fake_codex_check)

    result = CliRunner().invoke(
        apex_infinite.main,
        ["--config", str(bad_config), "--path", str(project_path), "--doctor"],
    )

    assert result.exit_code == 1
    assert "FAIL Config file" in result.output


def test_doctor_redacts_secret_values(monkeypatch, tmp_path):
    result, _captured = invoke_doctor(monkeypatch, tmp_path)

    assert "ollama" in result.output  # provider name shown
    assert "API key is set" in result.output
    # The literal configured key value must never surface.
    assert "api_key: ollama" not in result.output


def test_check_python_version_floor():
    assert check_python_version((3, 10)).status == DOCTOR_PASS
    assert check_python_version((3, 12)).status == DOCTOR_PASS
    failed = check_python_version((3, 9))
    assert failed.status == DOCTOR_FAIL
    assert "3.10" in failed.detail


def test_check_spec_system_states(tmp_path):
    assert check_spec_system("").status == DOCTOR_WARN
    project = tmp_path / "project"
    project.mkdir()
    assert check_spec_system(str(project)).status == DOCTOR_WARN
    (project / ".spec_system").mkdir()
    assert check_spec_system(str(project)).status == DOCTOR_PASS


def test_check_history_db_states(tmp_path):
    existing = tmp_path / "history"
    existing.mkdir()
    assert check_history_db(existing).status == DOCTOR_PASS
    creatable = tmp_path / "new-history"
    assert check_history_db(creatable).status == DOCTOR_PASS
    impossible = tmp_path / "missing-parent" / "history"
    assert check_history_db(impossible).status == DOCTOR_FAIL


def test_check_event_stream_path_states(tmp_path):
    assert check_event_stream_path(None).status == DOCTOR_PASS
    assert check_event_stream_path("-").status == DOCTOR_PASS
    target = tmp_path / "events" / "run.jsonl"
    assert check_event_stream_path(str(target)).status == DOCTOR_PASS
