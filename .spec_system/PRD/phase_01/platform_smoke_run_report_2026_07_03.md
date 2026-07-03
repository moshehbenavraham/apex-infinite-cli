# Platform Smoke Run Report - 2026-07-03

## Session Split Plan

### Session 01: Codex Invocation Compatibility

**Objective**: Make default non-dry-run Codex subprocess execution work with the installed Codex CLI and fail early when configured flags are stale.

**Scope**:
- Update packaged `codex.exec_flags` defaults in `src/apex_infinite/config.yaml`.
- Update runtime fallback defaults in `src/apex_infinite/cli.py`.
- Update README examples that still reference the rejected Codex flag.
- Add a startup compatibility check or non-mutating subprocess smoke fixture for `codex exec` flags.
- Document the selected operator policy for the current supported full-auto flag.

**Outputs**:
- Supported default Codex invocation config.
- Regression coverage that catches stale Codex exec flags before the main loop starts.
- README guidance aligned with current Codex CLI behavior.

**Dependencies / Notes**:
- Assumption: the intended replacement is `--dangerously-bypass-approvals-and-sandbox` unless a safer operator-selected policy is chosen during implementation.
- Open question: whether the default should be full-auto out of the box or require explicit operator configuration.

**Acceptance Checks**:
- The default actual nested Codex subprocess smoke no longer fails with `unexpected argument '--dangerously-auto-approve'`.
- Tests or smoke fixtures fail when the configured Codex flags are not accepted by `codex exec`.
- README and packaged defaults no longer mention `--dangerously-auto-approve`.

### Session 02: Provider Event Stream Contract

**Objective**: Restore provider preflight lifecycle events as valid event-stream output for file, stdout, and machine-output consumers.

**Scope**:
- Register `provider_check_started`, `provider_check_failed`, and `provider_check_finished` in the event schema, or rename the emits to approved event names.
- Add tests for `--check-provider --event-stream`.
- Add tests for startup provider preflight with file event streams.
- Add tests for startup provider preflight with `--event-stream - --machine-output`.
- Cover the provider failure path so `provider_check_failed` is validated too.

**Outputs**:
- Event schema and provider preflight emitters with matching event names.
- Regression tests for successful and failed provider preflight event output.

**Dependencies / Notes**:
- None.

**Acceptance Checks**:
- Provider preflight runs no longer emit `event_stream_error` rows for valid lifecycle events.
- Machine-output JSONL remains machine-only and includes valid provider preflight events.
- File event-stream mode persists provider preflight events instead of dropping them.

### Session 03: History Path Normalization

**Objective**: Make history lookups use the same normalized project path shape as normal run logging.

**Scope**:
- Extract or reuse one project-path normalization helper in `src/apex_infinite/cli.py`.
- Apply the helper before history queries and normal loop DB writes.
- Add Click tests that log with one trailing-slash shape and query with the other.
- Verify documented `--history --path` examples work with common shell-expanded paths.

**Outputs**:
- Shared path normalization behavior for run mode and history mode.
- Regression coverage for trailing-slash and no-trailing-slash project paths.

**Dependencies / Notes**:
- None.

**Acceptance Checks**:
- `apex-infinite --history --path /home/aiwithapex/projects/apex-infinite-cli` finds rows logged under `/home/aiwithapex/projects/apex-infinite-cli/`.
- Existing history queries continue to work for already-normalized paths.

### Session 04: Output Observability Polish

**Objective**: Remove confusing plain-output labels and make response summary previews useful or explicitly contracted as redacted.

**Scope**:
- Change generic plain status block labels from internal severity names such as `ACCENT` to a user-facing label such as `STATUS`.
- Add provider preflight plain/ascii/compact renderer coverage.
- Decide whether `response_summarized.preview` should contain a short preview or be documented as intentionally suppressed.
- If previews are intended, replace `summarize_text(..., limit=0)` with a small nonzero limit for dry-run and real Codex response events.
- Add event payload tests for short harmless responses.

**Outputs**:
- Plain output that does not expose internal theme tokens.
- Response summary event behavior that matches its field name and tests.

**Dependencies / Notes**:
- Open question: whether response previews are intentionally redacted for privacy or should show a short preview for observability.

**Acceptance Checks**:
- Provider preflight plain output no longer prints `ACCENT Provider Preflight`.
- A short response such as `APEX_INFINITE_SUBPROCESS_SMOKE_OK` produces a useful preview, or the code/docs clearly define preview suppression.

### Session 05: Agent Config Semantics

**Objective**: Make Codex agent configuration parsing and documented reasoning-effort behavior match actual subprocess invocation behavior.

**Scope**:
- Replace `exec_flags.split()` with shell-aware parsing via `shlex.split`, or migrate `exec_flags` to a validated YAML list.
- Add tests for quoted Codex options such as config overrides with spaces or quotes.
- Decide whether `model_reasoning_effort` should be translated into current Codex CLI config syntax.
- Implement the reasoning-effort translation or remove the inert setting from config and docs.
- Update config validation and README examples to match the chosen behavior.

**Outputs**:
- Robust exec flag tokenization or validated list-based config.
- Clear, tested behavior for `model_reasoning_effort`.
- Documentation that no longer describes inert configuration.

**Dependencies / Notes**:
- Depends on Session 01 if that session changes the supported default invocation policy.
- Open question: whether current Codex CLI exposes the desired reasoning-effort setting through stable command-line or config syntax.

**Acceptance Checks**:
- Quoted exec flag values are passed to the Codex subprocess as intended.
- `model_reasoning_effort` either affects the generated Codex command or is absent from shipped config and docs.

### Session 06: Documentation And Release Verification

**Objective**: Capture environment guidance and rerun the full release smoke suite after the functional fixes land.

**Scope**:
- Add local development troubleshooting guidance for stale activated virtualenvs where `python` points outside the repository.
- Recommend creating and invoking an explicit repository virtualenv for smoke runs.
- Rerun the documented quality suite: pytest, black, mypy, pylint, pip-audit, and package build.
- Rerun provider preflight, provider chat preflight, dry-run loop, machine-output JSONL loop, history display, visual wrapper fixture mode, visual wrapper CLI launch mode, and actual nested Codex subprocess smoke.
- Update this smoke report or the appropriate release notes with final verification results.

**Outputs**:
- Developer documentation for reliable local smoke setup.
- Final verification evidence after all smoke-run findings are addressed.

**Dependencies / Notes**:
- Depends on Sessions 01 through 05 for final end-to-end verification.
- Assumption: local Ollama remains available at `http://localhost:11434/v1` with `qwen2.5-coder:7b-instruct-q4_K_M`, or an equivalent documented provider is substituted.

**Acceptance Checks**:
- The quality suite remains green after the fixes.
- The actual nested Codex subprocess smoke passes with the shipped default or documented required config.
- The smoke report records no remaining release-blocking failures from the findings listed below.

## Summary

Smoke result: mostly healthy, with two functional issues found.

The install, test suite, formatter, type checker, linter, dependency audit,
package build, local Ollama provider preflight, bounded dry-run loop, visual
wrapper fixture mode, and visual wrapper guarded CLI launch all passed.

The default non-dry-run Codex subprocess path fails with the installed Codex
CLI because the packaged default `codex.exec_flags` value is no longer
accepted. A temporary config using the current Codex full-auto flag allowed the
same nested subprocess smoke to complete successfully.

The event stream also has a contract bug: provider preflight emits provider
event names that are not registered in the event schema.

## Environment

- Repository: `/home/aiwithapex/projects/apex-infinite-cli`
- Package version under test: `2.0.3`
- Python used for isolated smoke: `/tmp/apex-infinite-cli-smoke-venv/bin/python`
- Python version: `3.12.3`
- Codex CLI: `codex-cli 0.142.5`
- Local provider: Ollama at `http://localhost:11434/v1`
- Ollama model: `qwen2.5-coder:7b-instruct-q4_K_M`
- Temporary smoke artifacts:
  - `/tmp/apex-infinite-cli-smoke-venv`
  - `/tmp/apex-infinite-cli-smoke-dist`
  - `/tmp/apex-infinite-smoke-events.jsonl`
  - `/tmp/apex-infinite-smoke-real-codex-events.jsonl`
  - `/tmp/apex-infinite-smoke-current-codex-events.jsonl`
  - `/tmp/apex-infinite-cli-smoke-home*`

## Scope

Covered:

- Editable install with dev and visual extras.
- CLI version/help startup.
- Local Ollama provider model and chat preflight.
- One-iteration CLI dry-run loop with event stream and temporary history DB.
- One-iteration CLI machine-output JSONL loop.
- One-iteration actual nested Codex subprocess smoke.
- History display.
- Optional PySide6 visual wrapper in offscreen fixture mode.
- Optional PySide6 visual wrapper in offscreen real CLI launch mode.
- Pytest, black, mypy, pylint, pip-audit, and package build.

Not covered:

- A long autonomous multi-iteration workflow that lets the manager LLM choose
  follow-up commands after a real Codex response. The smoke runs were bounded
  to one iteration to avoid changing the repository.
- Grok and OpenAI remote provider checks. Local Ollama was available and used.
- Nuitka binary packaging for the visual wrapper.
- Docker-based Ollama deployment from scratch. Existing local Ollama was used.

## Smoke Matrix

| Area | Command or action | Result | Notes |
| --- | --- | --- | --- |
| Install | `python -m venv /tmp/apex-infinite-cli-smoke-venv` and `pip install -e ".[dev,visual]"` | PASS | Installed base, dev, and visual extras. |
| CLI version | `apex-infinite --version` | PASS | Returned `apex-infinite, version 2.0.3`. |
| CLI help | `apex-infinite --help` | PASS | Options rendered as documented. |
| Provider preflight | `apex-infinite --provider ollama --check-provider` | PASS | 1 model visible. |
| Provider chat preflight | `apex-infinite --provider ollama --check-provider --check-provider-chat` | PASS | Tiny chat completion passed. |
| Ollama helper | `./scripts/check-ollama.sh --chat` | PASS | Provider preflight and chat passed. |
| Unit/integration tests | `python -m pytest tests/ -v` | PASS | 236 passed, including live Ollama check. |
| Formatting | `python -m black --check .` | PASS | 25 files unchanged. |
| Type checking | `python -m mypy` | PASS | No issues in 11 source files. |
| Linting | `python -m pylint src tests` | PASS | Rated 10.00/10. |
| Dependency audit | `python -m pip_audit` | PASS | No known dependency vulnerabilities. Local package skipped because it is not on PyPI. |
| Build | `python -m build --outdir /tmp/apex-infinite-cli-smoke-dist` | PASS | Built sdist and wheel. |
| CLI dry-run loop | `apex-infinite --start plansession --dry-run --max-iterations 1` | PASS WITH ISSUE | Loop completed, but provider events were rejected by event stream. |
| Machine JSONL loop | `apex-infinite --event-stream - --machine-output --start plansession --dry-run --max-iterations 1` | PASS WITH ISSUE | JSONL stayed machine-only but contained provider `event_stream_error` rows. |
| History display | `apex-infinite --history --path ...` | PASS WITH ISSUE | Exact trailing-slash path found the row; no trailing slash returned no records. |
| Visual fixture | `QT_QPA_PLATFORM=offscreen apex-infinite-visual --dry-run --auto-close-ms 900` | PASS | Exited 0. |
| Visual real CLI launch | `QT_QPA_PLATFORM=offscreen apex-infinite-visual --launch-cli --dry-run --max-iterations 1` | PASS | Exited 0. |
| Actual nested Codex with default config | One-iteration no-edit subprocess smoke | FAIL | Codex rejected `--dangerously-auto-approve`. |
| Actual nested Codex with temporary current flag | Same smoke with `--dangerously-bypass-approvals-and-sandbox` | PASS | Returned `APEX_INFINITE_SUBPROCESS_SMOKE_OK`; worktree unchanged. |

## Findings

### 1. Default Codex exec flag is incompatible with installed Codex CLI

Severity: high / release-blocking for non-dry-run operation.

Evidence:

- Default config uses `exec_flags: "--dangerously-auto-approve"` at
  `src/apex_infinite/config.yaml:7`.
- README documents the same flag at `README.md:111`.
- Runtime fallback default also uses the same value at
  `src/apex_infinite/cli.py:916`.
- Installed Codex CLI is `codex-cli 0.142.5`.
- Actual nested subprocess smoke failed with exit code 2:
  `error: unexpected argument '--dangerously-auto-approve' found`.
- `codex exec --help` lists `--dangerously-bypass-approvals-and-sandbox` and
  `--dangerously-bypass-hook-trust`, not `--dangerously-auto-approve`.
- With a temporary config replacing the flag with
  `--dangerously-bypass-approvals-and-sandbox`, the same smoke completed and
  returned `APEX_INFINITE_SUBPROCESS_SMOKE_OK`.

Impact:

- The platform can install and pass dry-run tests while real autonomous Codex
  execution fails immediately out of the box.
- The optional visual wrapper launch path can appear healthy in dry-run mode
  while inheriting the same failure for real execution.

Recommended fix:

- Update packaged config, README examples, and runtime defaults to a supported
  Codex CLI flag or a documented operator-selected policy.
- Add a startup compatibility check for `codex exec --help` or a small
  subprocess smoke fixture so stale flags fail before the main loop starts.
- Consider making the safe default explicit in docs because the current
  equivalent full-auto flag is more dangerous than the old name suggests.

### 2. Provider preflight event names are not registered in the event stream

Severity: high for event-stream consumers.

Evidence:

- `_run_provider_preflight_or_exit()` emits `provider_check_started`,
  `provider_check_failed`, and `provider_check_finished` at
  `src/apex_infinite/cli.py:846`, `src/apex_infinite/cli.py:866`, and
  `src/apex_infinite/cli.py:886`.
- `EVENT_NAMES` in `src/apex_infinite/events.py:16` through
  `src/apex_infinite/events.py:58` does not include those three event names.
- Bounded dry-run loop with a file event stream printed:
  `Event stream error: invalid event name: 'provider_check_started'`.
- Machine-output JSONL contained `event_stream_error` rows for
  `provider_check_started` and `provider_check_finished`.
- File event-stream mode did not persist provider preflight events; it only
  printed human-facing event stream errors.

Impact:

- Automation and the visual wrapper cannot rely on provider preflight lifecycle
  events.
- Machine-output consumers receive error events during otherwise successful
  startup.
- Human file event-stream runs silently lose provider check events while still
  exiting 0.

Recommended fix:

- Add the provider preflight event names to `EVENT_NAMES`, or rename the emits
  to already-approved event names.
- Add tests for `--check-provider --event-stream`, startup preflight with file
  event streams, and startup preflight with `--event-stream - --machine-output`.
- Include the failure path too, because `provider_check_failed` is also
  currently unregistered.

### 3. `--history --path` does not normalize the project path before querying

Severity: medium.

Evidence:

- History mode returns before project path expansion/validation/normalization:
  `src/apex_infinite/cli.py:2252` through `src/apex_infinite/cli.py:2255`.
- Normal loop DB keys are normalized later at `src/apex_infinite/cli.py:2305`
  through `src/apex_infinite/cli.py:2316`.
- After the smoke loop logged a row for
  `/home/aiwithapex/projects/apex-infinite-cli/`, this command returned no
  records:
  `apex-infinite --history --path /home/aiwithapex/projects/apex-infinite-cli`
- The same command with a trailing slash found the row:
  `apex-infinite --history --path /home/aiwithapex/projects/apex-infinite-cli/`

Impact:

- The documented `--history --path ~/projects/my-app/` form works only when
  callers pass the exact normalized DB key.
- Operators can falsely conclude there is no history.

Recommended fix:

- Share one project-path normalization helper between run mode, history mode,
  and DB fetches.
- Add a Click test that logs with one path shape and reads history with the
  other.

### 4. Current shell `python` points at another project's virtualenv

Severity: medium environment warning, not a repository code bug.

Evidence:

- `python --version` returned `Python 3.12.3`, but `python -m pip --version`
  failed with:
  `/home/aiwithapex/projects/roaring-lion/backend/.venv/bin/python: No module named pip`.
- `sys.executable` for `python` was
  `/home/aiwithapex/projects/roaring-lion/backend/.venv/bin/python`.
- `python3 -m pip --version` worked from system Python.

Impact:

- The README install command `python -m pip install -e .` fails in this shell
  even though `python3` is usable.
- Operators may accidentally test or run the package against dependencies from
  an unrelated project.

Recommended fix:

- For local smoke/development docs, recommend creating an explicit repo venv
  and invoking that venv's Python.
- Consider adding a troubleshooting note for stale activated virtualenvs.

### 5. Plain status output uses `ACCENT` as a visible label

Severity: low.

Evidence:

- Provider preflight in plain/ascii/compact mode printed:
  `ACCENT Provider Preflight`.
- `print_status()` calls `print_block()` without a semantic label at
  `src/apex_infinite/ui.py:715` through `src/apex_infinite/ui.py:719`.
- `_print_plain_block()` falls back to `severity.upper()` at
  `src/apex_infinite/ui.py:918`.
- `_label_for_title()` does not map generic provider/status titles at
  `src/apex_infinite/ui.py:1088` through `src/apex_infinite/ui.py:1103`.

Impact:

- Plain logs are understandable but look like internal theme/severity tokens
  are leaking into operator output.

Recommended fix:

- Give generic status blocks a stable user-facing label such as `STATUS`.
- Add provider preflight plain-mode output to renderer tests.

### 6. `exec_flags.split()` is fragile for quoted Codex options

Severity: low / hardening improvement.

Evidence:

- Command construction uses `*exec_flags.split()` at
  `src/apex_infinite/cli.py:1298`.
- Current Codex supports config overrides such as
  `-c model="..."` and other values where shell-style quoting is common.

Impact:

- A documented or operator-provided `exec_flags` string containing quoted
  values can be split incorrectly.

Recommended fix:

- Use `shlex.split(exec_flags)` for string config, or accept `exec_flags` as a
  YAML list and validate each token.

### 7. `model_reasoning_effort` is configured but not passed to Codex

Severity: low / documentation and behavior mismatch.

Evidence:

- Config contains `model_reasoning_effort: "xhigh"` at
  `src/apex_infinite/config.yaml:8`.
- README tells users to adjust `model_reasoning_effort` at `README.md:112` and
  `README.md:136`.
- Code reads the setting in `get_agent_config()` at
  `src/apex_infinite/cli.py:913` through `src/apex_infinite/cli.py:920`.
- Command construction only uses `binary`, `exec_flags`, and `prompt` at
  `src/apex_infinite/cli.py:1298`.

Impact:

- Operators may believe reasoning effort is being applied when it is currently
  inert.

Recommended fix:

- Either translate the setting to the current Codex CLI config syntax or remove
  it from config/docs until supported.

### 8. `response_summarized.preview` is always `...`

Severity: low / observability improvement.

Evidence:

- Dry-run and real Codex response events call `summarize_text(output, limit=0)`
  at `src/apex_infinite/cli.py:1263` and `src/apex_infinite/cli.py:1380`.
- The successful nested Codex smoke output was
  `APEX_INFINITE_SUBPROCESS_SMOKE_OK`, but the event payload preview was
  `...`.

Impact:

- Event-stream consumers get length and line count but no useful preview, even
  for harmless short responses.

Recommended fix:

- Use a small nonzero preview limit, or rename the field/contract if response
  previews are intentionally suppressed.

## Verification Evidence

Passing checks:

```text
pytest: 236 passed in 11.53s
black: All done; 25 files would be left unchanged.
mypy: Success: no issues found in 11 source files
pylint: 10.00/10
pip-audit: No known vulnerabilities found
build: Successfully built apex_infinite_cli-2.0.3.tar.gz and apex_infinite_cli-2.0.3-py3-none-any.whl
visual fixture offscreen: exit 0
visual real CLI launch offscreen: exit 0
provider preflight: passed via models endpoint; 1 models visible
provider chat preflight: passed via models plus chat completion; 1 models visible
```

Nested Codex default-config failure:

```text
Return code: 2
error: unexpected argument '--dangerously-auto-approve' found
tip: a similar argument exists: '--dangerously-bypass-hook-trust'
```

Nested Codex temporary-current-flag success:

```text
Flags: --dangerously-bypass-approvals-and-sandbox
Return code: 0
Output: APEX_INFINITE_SUBPROCESS_SMOKE_OK
```

Event-stream provider event failure:

```text
Event stream error: invalid event name: 'provider_check_started'
Event stream error: invalid event name: 'provider_check_finished'
```

Worktree verification after nested Codex smoke:

```text
git status --short
?? docs/ongoing-projects/
```

The only repository change from this smoke run is this report file. The
existing `docs/ongoing-projects/terminal-and-linux-app-productization-plan.md`
was already present in the untracked directory before this report was added.

## Suggested Fix Order

1. Replace or version-gate the default Codex exec flag, then add a real
   subprocess smoke test that cannot mutate the repo.
2. Register or rename provider preflight event names and add event-stream tests
   for provider startup.
3. Normalize history paths before querying.
4. Clean up plain status labels.
5. Replace `exec_flags.split()` with robust token parsing or list config.
6. Decide whether `model_reasoning_effort` should be implemented or removed
   from docs/config.
7. Decide whether response previews should be useful or intentionally redacted.
