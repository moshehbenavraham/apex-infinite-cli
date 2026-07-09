"""First-run privacy notice and history purge tests."""

import json

from click.testing import CliRunner

import apex_infinite.cli as apex_infinite
from apex_infinite.privacy import (
    mark_privacy_notice_shown,
    privacy_marker_path,
    privacy_notice_needed,
)

from .test_cli_options import jsonl_rows, prepare_cli


def remove_notice_marker(tmp_path):
    marker = tmp_path / "xdg-state" / "apex-infinite" / "privacy-notice-shown"
    if marker.exists():
        marker.unlink()


def test_privacy_marker_roundtrip(monkeypatch, tmp_path):
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))

    assert privacy_notice_needed() is True
    marker = mark_privacy_notice_shown()
    assert marker == privacy_marker_path()
    assert privacy_notice_needed() is False


def test_first_run_shows_privacy_notice_once(monkeypatch, tmp_path):
    config_path, project_path, _captured = prepare_cli(monkeypatch, tmp_path)
    remove_notice_marker(tmp_path)
    args = [
        "--config",
        str(config_path),
        "--path",
        str(project_path),
        "--max-iterations",
        "0",
    ]

    first = CliRunner().invoke(apex_infinite.main, args)
    second = CliRunner().invoke(apex_infinite.main, args)

    assert first.exit_code == 0, first.output
    assert "Privacy Notice" in first.output
    assert "history.db" in first.output
    assert second.exit_code == 0
    assert "Privacy Notice" not in second.output


def test_privacy_notice_event_reaches_file_stream(monkeypatch, tmp_path):
    config_path, project_path, _captured = prepare_cli(monkeypatch, tmp_path)
    remove_notice_marker(tmp_path)
    event_path = tmp_path / "events.jsonl"

    result = CliRunner().invoke(
        apex_infinite.main,
        [
            "--config",
            str(config_path),
            "--path",
            str(project_path),
            "--event-stream",
            str(event_path),
            "--max-iterations",
            "0",
        ],
    )

    assert result.exit_code == 0, result.output
    rows = jsonl_rows(event_path.read_text(encoding="ascii"))
    by_name = {row["event"]: row for row in rows}
    assert by_name["privacy_notice_shown"]["payload"] == {"first_run": True}


def test_machine_output_suppresses_privacy_notice(monkeypatch, tmp_path):
    config_path, project_path, _captured = prepare_cli(monkeypatch, tmp_path)
    remove_notice_marker(tmp_path)

    result = CliRunner().invoke(
        apex_infinite.main,
        [
            "--config",
            str(config_path),
            "--path",
            str(project_path),
            "--event-stream",
            "-",
            "--machine-output",
            "--max-iterations",
            "0",
        ],
    )

    assert result.exit_code == 0
    event_names = [row["event"] for row in jsonl_rows(result.output)]
    assert "privacy_notice_shown" not in event_names
    assert "Privacy Notice" not in result.output


def seed_history(tmp_path, monkeypatch, projects):
    """Create a history DB with one row per project path."""
    config_path, project_path, captured = prepare_cli(monkeypatch, tmp_path)
    apex_infinite.db_init()
    for project in projects:
        apex_infinite.db_log(project, "response", "implement", "reason")
    return config_path, project_path, captured


def test_purge_history_all_rows(monkeypatch, tmp_path):
    config_path, _project_path, _captured = seed_history(
        tmp_path, monkeypatch, ["/tmp/a/", "/tmp/b/"]
    )

    result = CliRunner().invoke(
        apex_infinite.main,
        ["--config", str(config_path), "--purge-history", "--yes"],
    )

    assert result.exit_code == 0, result.output
    assert "Deleted 2 history row(s)" in result.output
    assert apex_infinite.db_purge_history() == 0  # nothing left


def test_purge_history_scoped_to_project(monkeypatch, tmp_path):
    config_path, project_path, _captured = seed_history(
        tmp_path, monkeypatch, ["/tmp/other/"]
    )
    apex_infinite.db_log(f"{project_path}/", "response", "implement", "reason")

    result = CliRunner().invoke(
        apex_infinite.main,
        [
            "--config",
            str(config_path),
            "--purge-history",
            "--yes",
            "--path",
            str(project_path),
        ],
    )

    assert result.exit_code == 0, result.output
    assert "Deleted 1 history row(s)" in result.output


def test_purge_history_confirmation_declined(monkeypatch, tmp_path):
    config_path, _project_path, _captured = seed_history(
        tmp_path, monkeypatch, ["/tmp/a/"]
    )

    result = CliRunner().invoke(
        apex_infinite.main,
        ["--config", str(config_path), "--purge-history"],
        input="n\n",
    )

    assert result.exit_code == 1
    assert "nothing was deleted" in result.output


def test_purge_history_machine_output_requires_yes(monkeypatch, tmp_path):
    config_path, _project_path, _captured = prepare_cli(monkeypatch, tmp_path)

    result = CliRunner().invoke(
        apex_infinite.main,
        [
            "--config",
            str(config_path),
            "--purge-history",
            "--event-stream",
            "-",
            "--machine-output",
        ],
    )

    assert result.exit_code == 2
    assert "requires --yes" in result.output


def test_purge_history_emits_event_on_stdout_stream(monkeypatch, tmp_path):
    config_path, _project_path, _captured = seed_history(
        tmp_path, monkeypatch, ["/tmp/a/"]
    )

    result = CliRunner().invoke(
        apex_infinite.main,
        [
            "--config",
            str(config_path),
            "--purge-history",
            "--yes",
            "--event-stream",
            "-",
            "--machine-output",
        ],
    )

    assert result.exit_code == 0, result.output
    rows = [json.loads(line) for line in result.output.splitlines() if line.strip()]
    by_name = {row["event"]: row for row in rows}
    assert by_name["history_purged"]["payload"]["deleted_rows"] == 1


def test_purge_history_emits_event_on_file_stream(monkeypatch, tmp_path):
    config_path, _project_path, _captured = seed_history(
        tmp_path, monkeypatch, ["/tmp/a/"]
    )
    event_path = tmp_path / "purge-events.jsonl"

    result = CliRunner().invoke(
        apex_infinite.main,
        [
            "--config",
            str(config_path),
            "--purge-history",
            "--yes",
            "--event-stream",
            str(event_path),
        ],
    )

    assert result.exit_code == 0, result.output
    rows = jsonl_rows(event_path.read_text(encoding="ascii"))
    by_name = {row["event"]: row for row in rows}
    assert by_name["history_purged"]["payload"]["deleted_rows"] == 1


def test_purge_history_rejects_history_combo(monkeypatch, tmp_path):
    config_path, _project_path, _captured = prepare_cli(monkeypatch, tmp_path)

    result = CliRunner().invoke(
        apex_infinite.main,
        ["--config", str(config_path), "--purge-history", "--history"],
    )

    assert result.exit_code == 2
    assert "--purge-history cannot be combined with --history" in result.output
