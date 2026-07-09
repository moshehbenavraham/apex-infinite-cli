"""First-run setup command and shared-config write tests."""

import os
import stat

import yaml
from click.testing import CliRunner

import apex_infinite.cli as apex_infinite
from apex_infinite.setup_config import (
    SetupValues,
    build_config_payload,
    validate_setup_values,
    write_shared_config,
)

from .test_cli_options import CONFIG_TEXT, prepare_cli


def run_setup(monkeypatch, tmp_path, args, env_config_home=None, input_text=None):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(env_config_home or (tmp_path / "xdg")))
    monkeypatch.delenv("APEX_INFINITE_CONFIG", raising=False)
    runner = CliRunner()
    return runner.invoke(apex_infinite.main, args, input=input_text)


def read_written_config(tmp_path):
    target = tmp_path / "xdg" / "apex-infinite" / "config.yaml"
    assert target.is_file()
    return target, yaml.safe_load(target.read_text(encoding="ascii"))


def test_non_interactive_setup_writes_xdg_config(monkeypatch, tmp_path):
    result = run_setup(
        monkeypatch,
        tmp_path,
        ["--setup-non-interactive", "--provider", "openai", "--model", "gpt-4o-mini"],
    )

    assert result.exit_code == 0, result.output
    target, payload = read_written_config(tmp_path)
    assert payload["provider"] == "openai"
    assert payload["providers"]["openai"]["model"] == "gpt-4o-mini"
    assert payload["codex"]["binary"] == "codex"
    mode = stat.S_IMODE(os.stat(target).st_mode)
    assert mode == 0o600
    parent_mode = stat.S_IMODE(os.stat(target.parent).st_mode)
    assert parent_mode == 0o700
    assert "Next steps" in result.output


def test_setup_written_config_loads_through_load_config(monkeypatch, tmp_path):
    result = run_setup(
        monkeypatch,
        tmp_path,
        ["--setup-non-interactive", "--provider", "grok"],
    )
    assert result.exit_code == 0, result.output
    target, _payload = read_written_config(tmp_path)
    monkeypatch.setenv("XAI_API_KEY", "test-key-value")

    config = apex_infinite.load_config(str(target))

    assert config["provider"] == "grok"
    assert config["providers"]["grok"]["api_key"] == "test-key-value"


def test_setup_never_writes_secret_values(monkeypatch, tmp_path):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-secret-value-should-not-appear")

    result = run_setup(
        monkeypatch,
        tmp_path,
        ["--setup-non-interactive", "--provider", "openai"],
    )

    assert result.exit_code == 0, result.output
    target, payload = read_written_config(tmp_path)
    raw = target.read_text(encoding="ascii")
    assert "sk-secret-value-should-not-appear" not in raw
    assert payload["providers"]["openai"]["api_key"] == "${OPENAI_API_KEY}"


def test_setup_warns_when_provider_key_env_is_missing(monkeypatch, tmp_path):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    result = run_setup(
        monkeypatch,
        tmp_path,
        ["--setup-non-interactive", "--provider", "openai"],
    )

    assert result.exit_code == 0
    assert "OPENAI_API_KEY is not set" in result.output


def test_setup_backs_up_existing_config(monkeypatch, tmp_path):
    first = run_setup(monkeypatch, tmp_path, ["--setup-non-interactive"])
    assert first.exit_code == 0
    second = run_setup(
        monkeypatch, tmp_path, ["--setup-non-interactive", "--provider", "grok"]
    )

    assert second.exit_code == 0
    assert "Previous config preserved" in second.output
    config_dir = tmp_path / "xdg" / "apex-infinite"
    backups = list(config_dir.glob("config.yaml.bak-*"))
    assert len(backups) == 1
    original = yaml.safe_load(backups[0].read_text(encoding="ascii"))
    assert original["provider"] == "ollama"
    _target, payload = read_written_config(tmp_path)
    assert payload["provider"] == "grok"
    assert not list(config_dir.glob(".config.yaml.tmp"))


def test_setup_honors_env_selected_config_target(monkeypatch, tmp_path):
    env_config = tmp_path / "selected" / "config.yaml"
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "xdg"))
    monkeypatch.setenv("APEX_INFINITE_CONFIG", str(env_config))

    result = CliRunner().invoke(apex_infinite.main, ["--setup-non-interactive"])

    assert result.exit_code == 0, result.output
    assert env_config.is_file()
    assert not (tmp_path / "xdg" / "apex-infinite" / "config.yaml").exists()


def test_setup_validation_rejects_bad_provider(monkeypatch, tmp_path):
    result = run_setup(
        monkeypatch,
        tmp_path,
        ["--setup-non-interactive", "--provider", "unknown"],
    )

    assert result.exit_code == 1
    assert "Unknown provider" in result.output
    assert not (tmp_path / "xdg" / "apex-infinite" / "config.yaml").exists()


def test_setup_validation_rejects_missing_projects_dir(monkeypatch, tmp_path):
    result = run_setup(
        monkeypatch,
        tmp_path,
        [
            "--setup-non-interactive",
            "--projects-dir",
            str(tmp_path / "does-not-exist"),
        ],
    )

    assert result.exit_code == 1
    assert "Projects directory not found" in result.output


def test_setup_only_flags_require_setup(monkeypatch, tmp_path):
    result = run_setup(monkeypatch, tmp_path, ["--codex-binary", "codex"])

    assert result.exit_code == 2
    assert "--codex-binary requires --setup" in result.output


def test_setup_rejects_machine_output_combo(monkeypatch, tmp_path):
    result = run_setup(
        monkeypatch,
        tmp_path,
        ["--setup", "--event-stream", "-", "--machine-output"],
    )

    assert result.exit_code == 2
    assert "--setup cannot be combined with" in result.output


def test_interactive_setup_prompts_and_confirms(monkeypatch, tmp_path):
    projects_dir = tmp_path / "projects"
    projects_dir.mkdir()
    input_text = "\n".join(
        [
            "openai",  # provider
            "gpt-4o",  # model
            "codex",  # binary
            "",  # exec flags (default)
            "high",  # reasoning effort
            str(projects_dir),  # projects dir
            "",  # default project (blank)
            "y",  # confirm write
            "",
        ]
    )

    result = run_setup(monkeypatch, tmp_path, ["--setup"], input_text=input_text)

    assert result.exit_code == 0, result.output
    assert "WARNING:" in result.output
    _target, payload = read_written_config(tmp_path)
    assert payload["provider"] == "openai"
    assert payload["codex"]["model_reasoning_effort"] == "high"
    assert payload["defaults"]["projects_dir"] == str(projects_dir)


def test_interactive_setup_blank_projects_dir_skips_missing_home_default(
    monkeypatch, tmp_path
):
    home = tmp_path / "home"
    home.mkdir()
    monkeypatch.setenv("HOME", str(home))
    input_text = "\n".join(
        [
            "",  # provider default
            "",  # model default
            "",  # binary default
            "",  # exec flags default
            "",  # reasoning effort default
            "",  # projects dir skip
            "",  # default project skip
            "y",  # confirm write
            "",
        ]
    )

    result = run_setup(monkeypatch, tmp_path, ["--setup"], input_text=input_text)

    assert result.exit_code == 0, result.output
    _target, payload = read_written_config(tmp_path)
    assert "defaults" not in payload


def test_interactive_setup_abort_writes_nothing(monkeypatch, tmp_path):
    projects_dir = tmp_path / "projects"
    projects_dir.mkdir()
    input_text = "\n".join(
        [
            "ollama",
            "",
            "",
            "",
            "",
            str(projects_dir),
            "",
            "n",  # decline write
            "",
        ]
    )

    result = run_setup(monkeypatch, tmp_path, ["--setup"], input_text=input_text)

    assert result.exit_code == 1
    assert "nothing was written" in result.output
    assert not (tmp_path / "xdg" / "apex-infinite" / "config.yaml").exists()


def test_default_project_from_config_is_used(monkeypatch, tmp_path):
    config_path, project_path, captured = prepare_cli(monkeypatch, tmp_path)
    config_with_defaults = CONFIG_TEXT + (f'defaults:\n  project: "{project_path}"\n')
    config_path.write_text(config_with_defaults, encoding="ascii")

    result = CliRunner().invoke(
        apex_infinite.main,
        ["--config", str(config_path), "--max-iterations", "0"],
    )

    assert result.exit_code == 0, result.output
    assert captured["path"] == f"{project_path}/"


def test_validate_setup_values_unit():
    assert validate_setup_values(SetupValues()) == []
    errors = validate_setup_values(
        SetupValues(provider="nope", model_reasoning_effort="extreme")
    )
    assert len(errors) == 2


def test_build_config_payload_includes_all_providers():
    payload = build_config_payload(SetupValues(provider="ollama"))

    assert set(payload["providers"]) == {"ollama", "openai", "grok"}
    assert payload["ui"]["theme"] == "auto"


def test_write_shared_config_explicit_path(tmp_path):
    target = tmp_path / "custom" / "config.yaml"

    result = write_shared_config(SetupValues(), path=target)

    assert result.path == target
    assert target.is_file()
    assert yaml.safe_load(target.read_text(encoding="ascii"))["provider"] == "ollama"
