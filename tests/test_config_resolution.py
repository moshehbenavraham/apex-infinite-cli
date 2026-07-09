"""Shared config resolution precedence and .env precedence tests."""

import json

from click.testing import CliRunner

import apex_infinite.cli as apex_infinite
from apex_infinite import config_resolution
from apex_infinite.config_resolution import (
    SOURCE_CLI_FLAG,
    SOURCE_CWD,
    SOURCE_ENV,
    SOURCE_PACKAGED,
    SOURCE_SOURCE_ROOT,
    SOURCE_XDG,
    first_run_needed,
    resolve_config,
    user_config_path,
)

from .test_cli_options import CONFIG_TEXT, OLLAMA_ENV_CONFIG_TEXT, clear_ollama_env


def _make_config(path, text=CONFIG_TEXT):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="ascii")
    return path


def _xdg_env(tmp_path, extra=None):
    env = {"XDG_CONFIG_HOME": str(tmp_path / "xdg")}
    if extra:
        env.update(extra)
    return env


def test_explicit_flag_wins_over_everything(tmp_path):
    explicit = _make_config(tmp_path / "explicit" / "config.yaml")
    _make_config(tmp_path / "xdg" / "apex-infinite" / "config.yaml")
    cwd = tmp_path / "cwd"
    _make_config(cwd / "config.yaml")
    env = _xdg_env(tmp_path, {"APEX_INFINITE_CONFIG": str(tmp_path / "other.yaml")})

    resolved = resolve_config(str(explicit), env=env, cwd=cwd)

    assert resolved.source == SOURCE_CLI_FLAG
    assert resolved.path == str(explicit)


def test_env_var_wins_over_xdg_and_cwd(tmp_path):
    env_config = _make_config(tmp_path / "env" / "config.yaml")
    _make_config(tmp_path / "xdg" / "apex-infinite" / "config.yaml")
    cwd = tmp_path / "cwd"
    _make_config(cwd / "config.yaml")
    env = _xdg_env(tmp_path, {"APEX_INFINITE_CONFIG": str(env_config)})

    resolved = resolve_config(None, env=env, cwd=cwd)

    assert resolved.source == SOURCE_ENV
    assert resolved.path == str(env_config)


def test_env_var_is_returned_even_when_missing_for_fail_fast(tmp_path):
    missing = tmp_path / "missing.yaml"
    env = _xdg_env(tmp_path, {"APEX_INFINITE_CONFIG": str(missing)})

    resolved = resolve_config(None, env=env, cwd=tmp_path / "cwd")

    assert resolved.source == SOURCE_ENV
    assert resolved.path == str(missing)
    assert resolved.exists is False


def test_xdg_config_wins_over_cwd(tmp_path):
    xdg_config = _make_config(tmp_path / "xdg" / "apex-infinite" / "config.yaml")
    cwd = tmp_path / "cwd"
    _make_config(cwd / "config.yaml")

    resolved = resolve_config(None, env=_xdg_env(tmp_path), cwd=cwd)

    assert resolved.source == SOURCE_XDG
    assert resolved.path == str(xdg_config)


def test_cwd_config_wins_over_source_root_and_packaged(tmp_path, monkeypatch):
    cwd = tmp_path / "cwd"
    cwd_config = _make_config(cwd / "config.yaml")
    root_config = _make_config(tmp_path / "root" / "config.yaml")
    monkeypatch.setattr(
        config_resolution, "source_root_config_path", lambda: root_config
    )

    resolved = resolve_config(None, env=_xdg_env(tmp_path), cwd=cwd)

    assert resolved.source == SOURCE_CWD
    assert resolved.path == str(cwd_config)


def test_source_root_config_wins_over_packaged(tmp_path, monkeypatch):
    root_config = _make_config(tmp_path / "root" / "config.yaml")
    monkeypatch.setattr(
        config_resolution, "source_root_config_path", lambda: root_config
    )

    resolved = resolve_config(None, env=_xdg_env(tmp_path), cwd=tmp_path / "cwd")

    assert resolved.source == SOURCE_SOURCE_ROOT
    assert resolved.path == str(root_config)


def test_packaged_defaults_are_last_resort(tmp_path, monkeypatch):
    monkeypatch.setattr(config_resolution, "source_root_config_path", lambda: None)

    resolved = resolve_config(None, env=_xdg_env(tmp_path), cwd=tmp_path / "cwd")

    assert resolved.source == SOURCE_PACKAGED
    assert resolved.exists is True


def test_resolution_returns_none_without_any_candidate(tmp_path, monkeypatch):
    monkeypatch.setattr(config_resolution, "source_root_config_path", lambda: None)
    monkeypatch.setattr(
        config_resolution,
        "packaged_config_path",
        lambda: tmp_path / "absent" / "config.yaml",
    )

    resolved = resolve_config(None, env=_xdg_env(tmp_path), cwd=tmp_path / "cwd")

    assert resolved is None


def test_user_config_path_honors_xdg_config_home(tmp_path):
    env = {"XDG_CONFIG_HOME": str(tmp_path / "custom-xdg")}

    assert user_config_path(env) == (
        tmp_path / "custom-xdg" / "apex-infinite" / "config.yaml"
    )


def test_first_run_needed_true_on_packaged_defaults(tmp_path, monkeypatch):
    monkeypatch.setattr(config_resolution, "source_root_config_path", lambda: None)

    assert first_run_needed(None, env=_xdg_env(tmp_path), cwd=tmp_path / "cwd") is True


def test_first_run_needed_false_with_xdg_config(tmp_path):
    _make_config(tmp_path / "xdg" / "apex-infinite" / "config.yaml")

    assert first_run_needed(None, env=_xdg_env(tmp_path), cwd=tmp_path / "cwd") is False


def test_load_config_prefers_config_directory_env_file(monkeypatch, tmp_path):
    """Config-directory .env overrides cwd .env (ADR 0001 #7)."""
    clear_ollama_env(monkeypatch)
    cwd = tmp_path / "cwd"
    cwd.mkdir()
    monkeypatch.chdir(cwd)
    (cwd / ".env").write_text("OLLAMA_MODEL=cwd-model\n", encoding="ascii")
    config_dir = tmp_path / "cfg"
    config_path = _make_config(config_dir / "config.yaml", OLLAMA_ENV_CONFIG_TEXT)
    (config_dir / ".env").write_text(
        "OLLAMA_MODEL=config-dir-model\n", encoding="ascii"
    )

    config = apex_infinite.load_config(config_path)

    assert config["providers"]["ollama"]["model"] == "config-dir-model"


def test_cwd_env_file_applies_when_config_directory_has_none(monkeypatch, tmp_path):
    clear_ollama_env(monkeypatch)
    cwd = tmp_path / "cwd"
    cwd.mkdir()
    monkeypatch.chdir(cwd)
    (cwd / ".env").write_text("OLLAMA_MODEL=cwd-model\n", encoding="ascii")
    config_path = _make_config(tmp_path / "cfg" / "config.yaml", OLLAMA_ENV_CONFIG_TEXT)

    config = apex_infinite.load_config(config_path)

    assert config["providers"]["ollama"]["model"] == "cwd-model"


def test_cli_emits_config_resolved_event(monkeypatch, tmp_path):
    from .test_cli_options import prepare_cli

    config_path, project_path, _captured = prepare_cli(monkeypatch, tmp_path)
    runner = CliRunner()

    result = runner.invoke(
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
    rows = [json.loads(line) for line in result.output.splitlines() if line.strip()]
    by_name = {row["event"]: row for row in rows}
    assert "config_resolved" in by_name
    payload = by_name["config_resolved"]["payload"]
    assert payload["config_path"] == str(config_path)
    assert payload["source"] == SOURCE_CLI_FLAG
    startup_payload = by_name["startup"]["payload"]
    assert startup_payload["config_source"] == SOURCE_CLI_FLAG


def test_malformed_selected_config_fails_fast(monkeypatch, tmp_path):
    project_path = tmp_path / "project"
    project_path.mkdir()
    bad_config = tmp_path / "config.yaml"
    bad_config.write_text("provider: [unclosed\n", encoding="ascii")
    monkeypatch.setattr(apex_infinite, "DB_DIR", tmp_path / "db")
    monkeypatch.setattr(apex_infinite, "DB_PATH", tmp_path / "db" / "history.db")

    result = CliRunner().invoke(
        apex_infinite.main,
        ["--config", str(bad_config), "--path", str(project_path)],
    )

    assert result.exit_code != 0


def test_missing_env_selected_config_fails_fast(monkeypatch, tmp_path):
    project_path = tmp_path / "project"
    project_path.mkdir()
    monkeypatch.setattr(apex_infinite, "DB_DIR", tmp_path / "db")
    monkeypatch.setattr(apex_infinite, "DB_PATH", tmp_path / "db" / "history.db")
    monkeypatch.setenv("APEX_INFINITE_CONFIG", str(tmp_path / "missing.yaml"))

    result = CliRunner().invoke(
        apex_infinite.main,
        ["--path", str(project_path)],
    )

    assert result.exit_code != 0
    assert "not found" in result.output
