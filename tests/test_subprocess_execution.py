"""Subprocess execution compatibility tests."""

import subprocess
from types import SimpleNamespace

import pytest

import apex_infinite.cli as apex_infinite

AGENT_CFG = {
    "binary": "codex",
    "exec_flags": apex_infinite.DEFAULT_CODEX_EXEC_FLAGS,
    "model_reasoning_effort": "high",
}
REASONING_TOKEN = 'model_reasoning_effort="high"'


class CapturingRenderer:
    """Capture renderer calls made by execute_codex()."""

    def __init__(self):
        self.commands = []
        self.responses = []

    def print_codex_command(self, state, snapshot):
        self.commands.append((state, snapshot))

    def print_agent_response(self, output, verbose=False):
        self.responses.append((output, verbose))


class RecordingEmitter:
    """Capture event emissions made by execute_codex()."""

    enabled = True

    def __init__(self):
        self.events = []

    def emit(self, name, payload=None):
        self.events.append((name, dict(payload or {})))

    @property
    def names(self):
        return [name for name, _payload in self.events]


def set_process_result(monkeypatch, stdout="", stderr="", returncode=0):
    """Patch the active process boundary for success/failure tests."""
    captured = {}

    if hasattr(apex_infinite, "run_codex_process"):

        def fake_process(cmd, cwd, timeout):
            captured.update({"cmd": cmd, "cwd": cwd, "timeout": timeout})
            return apex_infinite.CodexProcessResult(
                stdout=stdout,
                stderr=stderr,
                returncode=returncode,
            )

        monkeypatch.setattr(apex_infinite, "run_codex_process", fake_process)
        return captured

    def fake_run(cmd, cwd, capture_output, text, timeout, check):
        captured.update(
            {
                "cmd": cmd,
                "cwd": cwd,
                "capture_output": capture_output,
                "text": text,
                "timeout": timeout,
                "check": check,
            }
        )
        return subprocess.CompletedProcess(
            cmd,
            returncode,
            stdout=stdout,
            stderr=stderr,
        )

    monkeypatch.setattr(apex_infinite.subprocess, "run", fake_run)
    return captured


def set_process_error(monkeypatch, error):
    """Patch the active process boundary to raise an error."""
    captured = {}

    if hasattr(apex_infinite, "run_codex_process"):

        def fake_process(cmd, cwd, timeout):
            captured.update({"cmd": cmd, "cwd": cwd, "timeout": timeout})
            raise error

        monkeypatch.setattr(apex_infinite, "run_codex_process", fake_process)
        return captured

    def fake_run(cmd, cwd, capture_output, text, timeout, check):
        captured.update(
            {
                "cmd": cmd,
                "cwd": cwd,
                "capture_output": capture_output,
                "text": text,
                "timeout": timeout,
                "check": check,
            }
        )
        raise error

    monkeypatch.setattr(apex_infinite.subprocess, "run", fake_run)
    return captured


def test_get_agent_config_uses_supported_default_flag_when_config_omits_codex():
    config = {
        "provider": "ollama",
        "providers": {"ollama": {"model": "test-model"}},
    }

    assert (
        apex_infinite.get_agent_config(config)["exec_flags"]
        == apex_infinite.DEFAULT_CODEX_EXEC_FLAGS
    )


def test_get_codex_exec_flag_tokens_preserves_quoted_values():
    tokens = apex_infinite.get_codex_exec_flag_tokens(
        {
            "exec_flags": (
                "--config 'sandbox_permissions=[\"disk-full-read-access\"]' "
                "--config 'model=\"gpt test\"'"
            )
        }
    )

    assert tokens == (
        "--config",
        'sandbox_permissions=["disk-full-read-access"]',
        "--config",
        'model="gpt test"',
    )


@pytest.mark.parametrize("exec_flags", [None, "", "   "])
def test_get_codex_exec_flag_tokens_allows_empty_values(exec_flags):
    assert apex_infinite.get_codex_exec_flag_tokens({"exec_flags": exec_flags}) == ()


@pytest.mark.parametrize("exec_flags", [False, 0, []])
def test_get_codex_exec_flag_tokens_rejects_non_string_values(exec_flags):
    with pytest.raises(apex_infinite.CliStartupError) as exc_info:
        apex_infinite.get_codex_exec_flag_tokens({"exec_flags": exec_flags})

    assert str(exc_info.value) == "codex.exec_flags must be a string."


def test_get_codex_exec_flag_tokens_rejects_malformed_quotes():
    with pytest.raises(apex_infinite.CliStartupError) as exc_info:
        apex_infinite.get_codex_exec_flag_tokens({"exec_flags": "--config 'open"})

    assert "Malformed codex.exec_flags" in str(exc_info.value)
    assert "No closing quotation" in str(exc_info.value)


@pytest.mark.parametrize("exec_flags", ["--config", "--model"])
def test_get_codex_exec_flag_tokens_rejects_missing_flag_values(exec_flags):
    with pytest.raises(apex_infinite.CliStartupError) as exc_info:
        apex_infinite.get_codex_exec_flag_tokens({"exec_flags": exec_flags})

    option_name = exec_flags.split()[0]
    assert str(exc_info.value) == (
        f"codex.exec_flags option '{option_name}' requires a value."
    )


@pytest.mark.parametrize("exec_flags", ["--config --model", "--config=missing-key"])
def test_get_codex_exec_flag_tokens_rejects_invalid_config_overrides(exec_flags):
    with pytest.raises(apex_infinite.CliStartupError) as exc_info:
        apex_infinite.get_codex_exec_flag_tokens({"exec_flags": exec_flags})

    assert "requires a key=value value" in str(exc_info.value)


@pytest.mark.parametrize(
    "effort",
    ["minimal", "low", "medium", "high", "xhigh", " XHIGH "],
)
def test_get_codex_reasoning_effort_tokens_accepts_supported_values(effort):
    tokens = apex_infinite.get_codex_reasoning_effort_tokens(
        {"model_reasoning_effort": effort}
    )

    expected = str(effort).strip().lower()
    assert tokens == ("-c", f'model_reasoning_effort="{expected}"')


def test_get_codex_reasoning_effort_tokens_rejects_unsupported_value():
    with pytest.raises(apex_infinite.CliStartupError) as exc_info:
        apex_infinite.get_codex_reasoning_effort_tokens(
            {"model_reasoning_effort": "extreme"}
        )

    assert "Unsupported codex.model_reasoning_effort" in str(exc_info.value)
    assert "minimal, low, medium, high, xhigh" in str(exc_info.value)


def test_validate_codex_exec_flags_accepts_supported_help_flags(monkeypatch):
    captured = {}

    def fake_run(cmd, capture_output, text, timeout, check):
        captured.update(
            {
                "cmd": cmd,
                "capture_output": capture_output,
                "text": text,
                "timeout": timeout,
                "check": check,
            }
        )
        return SimpleNamespace(
            returncode=0,
            stdout=(
                "Options:\n"
                "  -c, --config <key=value>\n"
                "      --dangerously-bypass-approvals-and-sandbox\n"
            ),
            stderr="",
        )

    monkeypatch.setattr(apex_infinite.subprocess, "run", fake_run)

    apex_infinite.validate_codex_exec_flags(
        {
            "binary": "codex",
            "exec_flags": (
                "--dangerously-bypass-approvals-and-sandbox --config model=test"
            ),
        }
    )

    assert captured == {
        "cmd": ["codex", "exec", "--help"],
        "capture_output": True,
        "text": True,
        "timeout": apex_infinite.CODEX_HELP_TIMEOUT,
        "check": False,
    }


def test_validate_codex_exec_flags_skips_config_values_that_look_like_flags(
    monkeypatch,
):
    def fake_run(*_args, **_kwargs):
        return SimpleNamespace(
            returncode=0,
            stdout=(
                "Options:\n"
                "  -c, --config <key=value>\n"
                "  -o, --output-last-message <FILE>\n"
            ),
            stderr="",
        )

    monkeypatch.setattr(apex_infinite.subprocess, "run", fake_run)

    apex_infinite.validate_codex_exec_flags(
        {
            "binary": "codex",
            "exec_flags": "--output-last-message --not-a-flag-value",
            "model_reasoning_effort": "xhigh",
        }
    )


def test_validate_codex_exec_flags_rejects_stale_flag(monkeypatch):
    def fake_run(*_args, **_kwargs):
        return SimpleNamespace(
            returncode=0,
            stdout="Options:\n      --dangerously-bypass-approvals-and-sandbox\n",
            stderr="",
        )

    monkeypatch.setattr(apex_infinite.subprocess, "run", fake_run)

    with pytest.raises(apex_infinite.CliStartupError) as exc_info:
        apex_infinite.validate_codex_exec_flags(
            {"binary": "codex", "exec_flags": "--dangerously-auto-approve"}
        )

    assert "--dangerously-auto-approve" in str(exc_info.value)
    assert "not supported" in str(exc_info.value)


def test_validate_codex_exec_flags_reports_missing_binary(monkeypatch):
    def fake_run(*_args, **_kwargs):
        raise FileNotFoundError()

    monkeypatch.setattr(apex_infinite.subprocess, "run", fake_run)

    with pytest.raises(apex_infinite.CliStartupError) as exc_info:
        apex_infinite.validate_codex_exec_flags(
            {"binary": "missing-codex", "exec_flags": "--some-flag"}
        )

    assert "missing-codex" in str(exc_info.value)
    assert "not found" in str(exc_info.value)


def test_execute_codex_dry_run_returns_existing_command_text(monkeypatch, tmp_path):
    def fail_if_called(*_args, **_kwargs):
        raise AssertionError("dry-run must not launch a subprocess")

    monkeypatch.setattr(apex_infinite.subprocess, "run", fail_if_called)
    monkeypatch.setattr(apex_infinite, "run_codex_process", fail_if_called)
    renderer = CapturingRenderer()

    output = apex_infinite.execute_codex(
        str(tmp_path),
        "Run the apex-spec skill command /implement",
        AGENT_CFG,
        dry_run=True,
        renderer=renderer,
    )

    assert output == "[DRY RUN] Command: Run the apex-spec skill command /implement"
    assert renderer.commands[0][0] == "dry-run"
    assert renderer.commands[0][1].timeout == apex_infinite.COMMAND_TIMEOUT
    assert renderer.commands[0][1].exec_flags == (
        f"{apex_infinite.DEFAULT_CODEX_EXEC_FLAGS} -c '{REASONING_TOKEN}'"
    )


def test_execute_codex_dry_run_emits_events(monkeypatch, tmp_path):
    def fail_if_called(*_args, **_kwargs):
        raise AssertionError("dry-run must not launch a subprocess")

    monkeypatch.setattr(apex_infinite, "run_codex_process", fail_if_called)
    emitter = RecordingEmitter()

    output = apex_infinite.execute_codex(
        str(tmp_path),
        "Run the apex-spec skill command /implement",
        AGENT_CFG,
        dry_run=True,
        event_emitter=emitter,
    )

    assert output == "[DRY RUN] Command: Run the apex-spec skill command /implement"
    assert emitter.names == ["codex_dry_run", "response_summarized"]
    assert emitter.events[0][1]["prompt_length"] == len(
        "Run the apex-spec skill command /implement"
    )
    assert emitter.events[1][1]["source"] == "codex_dry_run"
    assert emitter.events[1][1]["preview"] == output
    assert emitter.events[1][1]["preview_suppressed"] is False


def test_execute_codex_returns_stdout_and_renders_summary(monkeypatch, tmp_path):
    captured = set_process_result(monkeypatch, stdout="agent output\n")
    renderer = CapturingRenderer()

    output = apex_infinite.execute_codex(
        str(tmp_path),
        "prompt",
        AGENT_CFG,
        renderer=renderer,
    )

    assert output == "agent output\n"
    assert captured["cmd"] == [
        "codex",
        "exec",
        "--dangerously-bypass-approvals-and-sandbox",
        "-c",
        REASONING_TOKEN,
        "prompt",
    ]
    assert captured["cwd"] == str(tmp_path)
    assert captured["timeout"] == apex_infinite.COMMAND_TIMEOUT
    assert renderer.commands[0][0] == "start"
    assert renderer.responses == [("agent output\n", False)]


def test_execute_codex_preserves_quoted_flags_and_reasoning_tokens(
    monkeypatch, tmp_path
):
    agent_cfg = {
        "binary": "codex",
        "exec_flags": (
            "--dangerously-bypass-approvals-and-sandbox "
            "--config 'sandbox_permissions=[\"disk-full-read-access\"]'"
        ),
        "model_reasoning_effort": "xhigh",
    }
    captured = set_process_result(monkeypatch, stdout="agent output\n")

    apex_infinite.execute_codex(str(tmp_path), "prompt", agent_cfg)

    assert captured["cmd"] == [
        "codex",
        "exec",
        "--dangerously-bypass-approvals-and-sandbox",
        "--config",
        'sandbox_permissions=["disk-full-read-access"]',
        "-c",
        'model_reasoning_effort="xhigh"',
        "prompt",
    ]


def test_execute_codex_success_emits_start_finish_and_summary(monkeypatch, tmp_path):
    set_process_result(monkeypatch, stdout="agent output\n")
    emitter = RecordingEmitter()

    output = apex_infinite.execute_codex(
        str(tmp_path),
        "prompt",
        AGENT_CFG,
        event_emitter=emitter,
    )

    assert output == "agent output\n"
    assert emitter.names == [
        "codex_started",
        "codex_finished",
        "response_summarized",
    ]
    assert emitter.events[0][1]["binary"] == "codex"
    assert emitter.events[1][1]["return_code"] == 0
    assert emitter.events[2][1]["has_output"] is True
    assert emitter.events[2][1]["source"] == "codex"
    assert emitter.events[2][1]["preview"] == "agent output"
    assert emitter.events[2][1]["preview_suppressed"] is False


def test_execute_codex_success_summary_preview_is_bounded(monkeypatch, tmp_path):
    long_output = "x" * (apex_infinite.RESPONSE_PREVIEW_LIMIT + 50)
    set_process_result(monkeypatch, stdout=long_output)
    emitter = RecordingEmitter()

    apex_infinite.execute_codex(
        str(tmp_path),
        "prompt",
        AGENT_CFG,
        event_emitter=emitter,
    )

    preview = emitter.events[2][1]["preview"]
    assert len(preview) == apex_infinite.RESPONSE_PREVIEW_LIMIT + 3
    assert preview.endswith("...")
    assert emitter.events[2][1]["preview_suppressed"] is False


def test_execute_codex_renders_running_and_completed_process_state(
    monkeypatch, tmp_path
):
    set_process_result(monkeypatch, stdout="agent output\n")
    renderer = CapturingRenderer()

    apex_infinite.execute_codex(
        str(tmp_path),
        "prompt",
        AGENT_CFG,
        renderer=renderer,
    )

    states = {state: snapshot for state, snapshot in renderer.commands}
    assert states["start"].binary == "codex"
    assert states["start"].project_path == str(tmp_path)
    assert states["start"].timeout == apex_infinite.COMMAND_TIMEOUT
    assert states["start"].process_state == "running"
    assert states["start"].elapsed_seconds == 0
    assert states["complete"].return_code == 0
    assert states["complete"].process_state == "completed"
    assert states["complete"].elapsed_seconds >= 0


def test_execute_codex_uses_stderr_when_success_stdout_is_blank(monkeypatch, tmp_path):
    set_process_result(monkeypatch, stdout="  \n", stderr="stderr response\n")

    output = apex_infinite.execute_codex(str(tmp_path), "prompt", AGENT_CFG)

    assert output == "stderr response\n"


def test_execute_codex_wraps_non_zero_exit(monkeypatch, tmp_path):
    renderer = CapturingRenderer()
    set_process_result(
        monkeypatch,
        stdout="partial stdout",
        stderr="failure stderr",
        returncode=7,
    )

    output = apex_infinite.execute_codex(
        str(tmp_path),
        "prompt",
        AGENT_CFG,
        renderer=renderer,
    )

    assert output == (
        "[ERROR exit code 7]\n" "stdout: partial stdout\n" "stderr: failure stderr"
    )
    assert any(state == "non-zero" for state, _snapshot in renderer.commands)


def test_execute_codex_non_zero_emits_error_and_preserves_text(monkeypatch, tmp_path):
    set_process_result(
        monkeypatch,
        stdout="partial stdout",
        stderr="failure stderr",
        returncode=7,
    )
    emitter = RecordingEmitter()

    output = apex_infinite.execute_codex(
        str(tmp_path),
        "prompt",
        AGENT_CFG,
        event_emitter=emitter,
    )

    assert output == (
        "[ERROR exit code 7]\n" "stdout: partial stdout\n" "stderr: failure stderr"
    )
    assert emitter.names == [
        "codex_started",
        "codex_error",
        "response_summarized",
    ]
    assert emitter.events[1][1]["error_type"] == "non_zero_exit"
    assert emitter.events[1][1]["return_code"] == 7
    assert emitter.events[2][1]["source"] == "codex"
    assert "[ERROR exit code 7]" in emitter.events[2][1]["preview"]
    assert "failure stderr" in emitter.events[2][1]["preview"]
    assert emitter.events[2][1]["preview_suppressed"] is False


def test_execute_codex_timeout_text_is_stable(monkeypatch, tmp_path):
    renderer = CapturingRenderer()
    set_process_error(
        monkeypatch,
        subprocess.TimeoutExpired(["codex", "exec"], apex_infinite.COMMAND_TIMEOUT),
    )

    output = apex_infinite.execute_codex(
        str(tmp_path),
        "prompt",
        AGENT_CFG,
        renderer=renderer,
    )

    assert output == (
        f"[TIMEOUT] Codex command timed out after {apex_infinite.COMMAND_TIMEOUT}s"
    )
    assert any(state == "timeout" for state, _snapshot in renderer.commands)


def test_execute_codex_timeout_emits_timeout_event(monkeypatch, tmp_path):
    set_process_error(
        monkeypatch,
        subprocess.TimeoutExpired(["codex", "exec"], apex_infinite.COMMAND_TIMEOUT),
    )
    emitter = RecordingEmitter()

    output = apex_infinite.execute_codex(
        str(tmp_path),
        "prompt",
        AGENT_CFG,
        event_emitter=emitter,
    )

    assert output == (
        f"[TIMEOUT] Codex command timed out after {apex_infinite.COMMAND_TIMEOUT}s"
    )
    assert emitter.names == [
        "codex_started",
        "codex_timeout",
        "response_summarized",
    ]
    assert emitter.events[1][1]["timeout_seconds"] == apex_infinite.COMMAND_TIMEOUT
    assert emitter.events[2][1]["source"] == "codex_timeout"
    assert emitter.events[2][1]["preview"] == output
    assert emitter.events[2][1]["preview_suppressed"] is False


def test_execute_codex_missing_binary_text_is_stable(monkeypatch, tmp_path):
    renderer = CapturingRenderer()
    set_process_error(monkeypatch, FileNotFoundError())

    output = apex_infinite.execute_codex(
        str(tmp_path),
        "prompt",
        AGENT_CFG,
        renderer=renderer,
    )

    assert output == "[ERROR] 'codex' command not found. Is Codex CLI installed?"
    assert any(state == "missing" for state, _snapshot in renderer.commands)


def test_execute_codex_missing_binary_emits_error_event(monkeypatch, tmp_path):
    set_process_error(monkeypatch, FileNotFoundError())
    emitter = RecordingEmitter()

    output = apex_infinite.execute_codex(
        str(tmp_path),
        "prompt",
        AGENT_CFG,
        event_emitter=emitter,
    )

    assert output == "[ERROR] 'codex' command not found. Is Codex CLI installed?"
    assert emitter.names == [
        "codex_started",
        "codex_error",
        "response_summarized",
    ]
    assert emitter.events[1][1]["error_type"] == "missing_binary"
    assert emitter.events[2][1]["source"] == "codex_missing"
    assert emitter.events[2][1]["preview"] == output
    assert emitter.events[2][1]["preview_suppressed"] is False


def test_execute_codex_generic_exception_text_is_stable(monkeypatch, tmp_path):
    renderer = CapturingRenderer()
    set_process_error(monkeypatch, RuntimeError("boom"))

    output = apex_infinite.execute_codex(
        str(tmp_path),
        "prompt",
        AGENT_CFG,
        renderer=renderer,
    )

    assert output == "[ERROR] Failed to execute codex: boom"
    assert any(state == "error" for state, _snapshot in renderer.commands)


def test_execute_codex_generic_exception_emits_error_event(monkeypatch, tmp_path):
    set_process_error(monkeypatch, RuntimeError("boom"))
    emitter = RecordingEmitter()

    output = apex_infinite.execute_codex(
        str(tmp_path),
        "prompt",
        AGENT_CFG,
        event_emitter=emitter,
    )

    assert output == "[ERROR] Failed to execute codex: boom"
    assert emitter.names == [
        "codex_started",
        "codex_error",
        "response_summarized",
    ]
    assert emitter.events[1][1]["error_type"] == "RuntimeError"
    assert emitter.events[2][1]["source"] == "codex_error"
    assert emitter.events[2][1]["preview"] == output
    assert emitter.events[2][1]["preview_suppressed"] is False


def test_execute_codex_verbose_flag_reaches_response_renderer(monkeypatch, tmp_path):
    renderer = CapturingRenderer()
    set_process_result(monkeypatch, stdout="full response")

    output = apex_infinite.execute_codex(
        str(tmp_path),
        "prompt",
        AGENT_CFG,
        verbose=True,
        renderer=renderer,
    )

    assert output == "full response"
    assert renderer.responses == [("full response", True)]


def test_run_codex_process_terminates_child_on_timeout(monkeypatch):
    class TimeoutThenExitProcess:
        """Fake process that exits after terminate and pipe drain."""

        returncode = None

        def __init__(self):
            self.communicate_timeouts = []
            self.terminated = False
            self.killed = False

        def communicate(self, timeout=None):
            self.communicate_timeouts.append(timeout)
            if len(self.communicate_timeouts) == 1:
                raise subprocess.TimeoutExpired(["codex"], timeout)
            self.returncode = -15
            return "partial stdout", "partial stderr"

        def terminate(self):
            self.terminated = True

        def kill(self):
            self.killed = True

    process = TimeoutThenExitProcess()
    monkeypatch.setattr(
        apex_infinite.subprocess,
        "Popen",
        lambda *_args, **_kwargs: process,
    )

    with pytest.raises(subprocess.TimeoutExpired) as exc_info:
        apex_infinite.run_codex_process(["codex", "exec"], str("/tmp"), 30)

    assert process.terminated is True
    assert process.killed is False
    assert process.communicate_timeouts == [30, apex_infinite.PROCESS_CLEANUP_TIMEOUT]
    assert exc_info.value.output == "partial stdout"
    assert exc_info.value.stderr == "partial stderr"


def test_run_codex_process_kills_child_if_terminate_does_not_exit(monkeypatch):
    class TimeoutUntilKillProcess:
        """Fake process that requires kill after terminate timeout."""

        returncode = None

        def __init__(self):
            self.communicate_timeouts = []
            self.terminated = False
            self.killed = False

        def communicate(self, timeout=None):
            self.communicate_timeouts.append(timeout)
            if len(self.communicate_timeouts) < 3:
                raise subprocess.TimeoutExpired(["codex"], timeout)
            self.returncode = -9
            return "killed stdout", "killed stderr"

        def terminate(self):
            self.terminated = True

        def kill(self):
            self.killed = True

    process = TimeoutUntilKillProcess()
    monkeypatch.setattr(
        apex_infinite.subprocess,
        "Popen",
        lambda *_args, **_kwargs: process,
    )

    with pytest.raises(subprocess.TimeoutExpired) as exc_info:
        apex_infinite.run_codex_process(["codex", "exec"], str("/tmp"), 30)

    assert process.terminated is True
    assert process.killed is True
    assert process.communicate_timeouts == [
        30,
        apex_infinite.PROCESS_CLEANUP_TIMEOUT,
        None,
    ]
    assert exc_info.value.output == "killed stdout"
    assert exc_info.value.stderr == "killed stderr"
