# Session Specification

**Session ID**: `phase01-session05-agent-config-semantics`
**Phase**: 01 - Smoke Remediation And Release Hardening
**Status**: Not Started
**Created**: 2026-07-03
**Base Commit**: 7673de17d6f44cd9637e66a31d21ff54a3cc6e9c

---

## 1. Session Overview

This session makes Apex Infinite CLI's Codex agent configuration semantics match the command it actually launches. Phase 01 Session 01 restored the supported default Codex autonomy flag and added startup flag validation, but the command path still tokenizes `codex.exec_flags` with basic whitespace splitting and still reads `model_reasoning_effort` without passing it to `codex exec`.

The next release-hardening step is to make quoted Codex options reliable and either make reasoning effort active or remove it from operator-facing configuration. Local Codex help shows `codex exec -c/--config <key=value>` overrides `~/.codex/config.toml`; the local user config already uses `model_reasoning_effort = "xhigh"`, so the plan treats `model_reasoning_effort` as active CLI config and maps it to a `-c model_reasoning_effort="<value>"` override.

This work advances Phase 01 by closing the remaining command-construction smoke finding before final documentation and release verification. It keeps the existing prompt contract, provider preflight behavior, event payload safety, SQLite schema, and subprocess capture semantics intact.

---

## 2. Objectives

1. Replace whitespace splitting of `codex.exec_flags` with shell-aware parsing that preserves quoted option values.
2. Translate valid `model_reasoning_effort` values into the generated `codex exec` command through Codex config override syntax.
3. Fail fast with clear config errors for malformed exec flags or unsupported reasoning-effort values.
4. Update tests and operator docs so packaged config, README examples, dry-run output, and subprocess behavior agree.

---

## 3. Prerequisites

### Required Sessions

- [x] `phase01-session01-codex-invocation-compatibility` - Establishes the supported default Codex invocation flag and startup validation policy.
- [x] `phase01-session02-provider-event-stream-contract` - Keeps provider preflight event output valid while startup behavior is updated.
- [x] `phase01-session03-history-path-normalization` - Keeps history path behavior stable outside this command-construction scope.
- [x] `phase01-session04-output-observability-polish` - Keeps response summary preview behavior stable outside this command-construction scope.

### Required Tools Or Knowledge

- Local `codex exec --help` output showing `-c/--config <key=value>` and the supported `--dangerously-bypass-approvals-and-sandbox` flag.
- Local `~/.codex/config.toml` evidence showing `model_reasoning_effort = "xhigh"` is a Codex config key.
- Existing command construction in `src/apex_infinite/cli.py`.
- Existing subprocess, Click startup, event-stream, renderer, and docs tests under `tests/`.

### Environment Requirements

- Repository root: `/home/aiwithapex/projects/apex-infinite-cli`.
- Codex CLI installed on `PATH` for local help verification.
- Unit tests must avoid launching a real mutating Codex prompt.

---

## 4. Scope

### In Scope (MVP)

- Operator can write quoted `codex.exec_flags` values in YAML and have them passed to `codex exec` as intended.
- Operator can keep `codex.model_reasoning_effort` in config and have it affect the generated Codex command.
- Maintainer can validate malformed `exec_flags` text before launching Codex with schema-validated input and explicit error mapping.
- Maintainer can validate reasoning effort against the allowed values `minimal`, `low`, `medium`, `high`, and `xhigh`.
- Developer can test shell-aware tokenization, startup flag validation, dry-run command rendering, actual command construction, and docs examples without real Codex mutation.
- Operator docs describe quoted exec flags and active reasoning-effort behavior accurately.

### Out Of Scope (Deferred)

- Migrating `codex.exec_flags` from a string to a YAML list - Reason: a shell-aware parser is lower risk and preserves existing config compatibility.
- Adding new CLI flags for reasoning effort - Reason: this session fixes config semantics without expanding the public CLI option surface.
- Prompt contract changes - Reason: command construction can be fixed without editing manager or summarizer prompts.
- SQLite history schema changes - Reason: no persisted data shape changes are required.
- Broader autonomous execution safety gates - Reason: security finding [P00-S02] remains a future scoped control beyond config parsing semantics.

---

## 5. Technical Approach

### Architecture

Keep the change inside the existing CLI boundary in `src/apex_infinite/cli.py`. Replace `str(exec_flags).split()` with a helper that uses `shlex.split()` and raises `CliStartupError` for malformed strings. Reuse that helper from both startup flag validation and `execute_codex()` so validation and real launch use identical tokenization.

Add a focused helper that normalizes `model_reasoning_effort`, rejects unsupported values, and returns Codex config override tokens in the form `("-c", "model_reasoning_effort=\"xhigh\"")`. Build the final command from `[binary, "exec"]`, parsed exec flag tokens, reasoning-effort override tokens, and the prompt. Keep dry-run rendering and `CodexCommandSnapshot.exec_flags` human-readable while ensuring tests inspect the actual command list.

### Design Patterns

- Single command-token builder: prevents validation and launch from drifting.
- Backward-compatible config string: preserves existing YAML shape while making quoted values safe.
- Config-key override: uses Codex's documented local help path for config overrides rather than adding unsupported bespoke flags.
- Focused regression tests: exercises parsing and command construction through existing subprocess and Click fixtures.
- Error mapping through existing startup paths: keeps machine-output isolation and renderer behavior intact.

---

## 6. Deliverables

### Files To Create

| File | Purpose | Est. Lines |
|------|---------|------------|
| None | No new runtime or test files are expected; the session modifies existing source, docs, and tests. | 0 |

### Files To Modify

| File | Changes | Est. Lines |
|------|---------|------------|
| `src/apex_infinite/cli.py` | Add shell-aware flag parsing, command-token building, reasoning-effort validation, and active Codex config override insertion. | ~120 |
| `src/apex_infinite/config.yaml` | Keep `model_reasoning_effort` as active config and align packaged sample value with supported behavior. | ~5 |
| `README.md` | Document quoted exec flags and active reasoning-effort translation in the config section. | ~35 |
| `docs/operator-runbook.md` | Add runbook guidance for quoted Codex flags and reasoning-effort review before real runs. | ~25 |
| `docs/troubleshooting.md` | Add malformed exec flag and invalid reasoning-effort troubleshooting guidance. | ~25 |
| `docs/transcripts/dry-run-plain.txt` | Refresh dry-run command output if reasoning-effort override changes the visible command. | ~10 |
| `tests/test_subprocess_execution.py` | Cover `shlex.split`, malformed exec flags, reasoning-effort command tokens, and command construction. | ~120 |
| `tests/test_cli_options.py` | Cover startup behavior for quoted flags, malformed flags, invalid reasoning effort, and dry-run command visibility. | ~100 |
| `tests/test_event_stream.py` | Update fixtures or assertions that expect the previous inert config shape. | ~20 |
| `tests/test_operator_console.py` | Update renderer command snapshot expectations if command display now includes reasoning-effort override text. | ~20 |
| `tests/test_renderer.py` | Update renderer fixtures if command snapshots include the active reasoning-effort override. | ~20 |

---

## 7. Success Criteria

### Functional Requirements

- [ ] Quoted `codex.exec_flags` values such as `--config 'sandbox_permissions=["disk-full-read-access"]'` are passed as intended to `codex exec`.
- [ ] Malformed `codex.exec_flags` strings fail before subprocess launch with clear config error text.
- [ ] `model_reasoning_effort` affects the generated `codex exec` command through a Codex config override.
- [ ] Unsupported reasoning-effort values fail before subprocess launch with clear config error text.
- [ ] Existing supported default invocation policy from Session 01 remains unchanged.
- [ ] Prompt routing, SQLite history storage, provider preflight events, and response summary behavior remain unchanged.

### Testing Requirements

- [ ] Unit tests cover shell-aware tokenization, malformed quoted strings, and allowed reasoning-effort values.
- [ ] Unit tests cover `execute_codex()` command construction with quoted flags and reasoning-effort override tokens.
- [ ] Click startup tests cover malformed flags and invalid reasoning effort.
- [ ] Existing subprocess, prompt-routing, renderer, event-stream, and CLI option tests remain green.

### Non-Functional Requirements

- [ ] Command construction uses list arguments and never invokes a shell.
- [ ] Config errors are deterministic and do not include provider secrets or API keys.
- [ ] Durable history rows and JSONL events remain free of ANSI escapes, Rich markup, frame glyphs, and secrets.
- [ ] No database migration or history schema change is introduced.

### Quality Gates

- [ ] All files ASCII-encoded.
- [ ] Unix LF line endings.
- [ ] Code follows project conventions.
- [ ] `python -m pytest tests/test_subprocess_execution.py tests/test_cli_options.py -v` passes.
- [ ] `python -m pytest tests/ -v` passes or unrelated pre-existing failures are documented.
- [ ] `python -m black --check src tests` passes.
- [ ] `python -m mypy` passes.
- [ ] `python -m pylint src tests` passes.

---

## 8. Implementation Notes

### Working Assumptions

- `model_reasoning_effort` should remain active config: local `codex exec --help` documents `-c/--config <key=value>` as a runtime override of `~/.codex/config.toml`, and local `~/.codex/config.toml` contains `model_reasoning_effort = "xhigh"`. Planning can proceed because this uses Codex's generic config override path and will be covered by command-construction tests.
- `exec_flags` should remain a YAML string for this session: the packaged config, README, tests, and existing user guidance already use a string, and the session stub allows `shlex.split` as the lower-risk option. Planning can proceed because `shlex.split` fixes quoted values without a config migration.

### Conflict Resolutions

- The session stub allows either implementing reasoning-effort translation or removing the inert setting. The chosen interpretation is to implement translation because local Codex config evidence supports `model_reasoning_effort` as a config key and the CLI help supports `-c` runtime overrides.
- The session stub allows either `shlex.split` or YAML-list migration. The chosen interpretation is `shlex.split` because it is backward-compatible with current packaged and user config while directly fixing the quoted-option bug.

### Key Considerations

- Do not edit `MANAGER_SYSTEM_PROMPT`, `SUMMARIZER_SYSTEM_PROMPT`, or `build_codex_prompt()`.
- Preserve stdout, stderr, return code, timeout, dry-run, missing-binary, and generic exception behavior for Codex execution.
- Keep Session 01's supported default `--dangerously-bypass-approvals-and-sandbox` policy unchanged.
- Keep command arguments as a list and do not introduce `shell=True`.
- Avoid emitting provider keys, environment-expanded secrets, or full config maps in errors or events.

### Potential Challenges

- `shlex.split` can reject malformed user config that previously reached subprocess launch: map this to a clear `CliStartupError` before launch.
- Reasoning-effort override quoting must survive both command execution and dry-run display: test actual command tokens and renderer output separately.
- Startup flag validation extracts option names from tokens: ensure `-c model_reasoning_effort="xhigh"` does not make validation reject config values as flags.

### Relevant Considerations

- [P00] **Prompt contract coupling**: Prompt routing stays unchanged; this session changes command construction only.
- [P00] **Autonomous execution controls**: The plan preserves the existing autonomy flag policy but makes the generated command explicit and testable before real runs.
- [P00] **Provider and Codex prerequisites**: Codex binary and config syntax remain runtime prerequisites; never print or emit provider API keys.
- [P00] **Raw durable facts only**: No Rich markup, ANSI escapes, visual tokens, or secrets should enter history or event payloads.
- [P00] **Machine-output isolation**: Startup/config failures must preserve JSONL-only stdout when `--machine-output` is active.

### Behavioral Quality Focus

Checklist active: Yes

Top behavioral risks for this session:

- Malformed config reaches `subprocess.Popen` instead of failing through the existing startup error boundary.
- Validation and launch build different command tokens for the same config.
- Reasoning-effort override accidentally changes prompt routing, event payloads, or durable history facts.

---

## 9. Testing Strategy

### Unit Tests

- Test `get_codex_exec_flag_tokens()` preserves quoted values with `shlex.split`.
- Test malformed quotes raise `CliStartupError` with a clear message.
- Test reasoning-effort helper accepts `minimal`, `low`, `medium`, `high`, and `xhigh`.
- Test invalid reasoning-effort values raise `CliStartupError`.
- Test `execute_codex()` passes quoted `--config` values and `-c model_reasoning_effort="xhigh"` as separate command tokens.

### Integration Tests

- Use `CliRunner` to verify malformed `codex.exec_flags` stops non-dry-run startup before the loop.
- Use `CliRunner` to verify invalid `model_reasoning_effort` stops startup before the loop.
- Use `CliRunner` to verify dry-run output shows the effective command with quoted flags and reasoning effort without launching Codex.
- Verify event-stream machine-output startup errors remain JSONL-only when config validation fails.

### Runtime Verification

- Run `codex exec --help` and confirm `-c/--config <key=value>` remains available.
- Run focused pytest files for subprocess and CLI startup.
- Run the full pytest suite after focused checks pass.
- Run black, mypy, and pylint checks.

### Edge Cases

- Empty `exec_flags`.
- Supported single long flag from Session 01.
- Quoted `--config` value containing spaces.
- Quoted `--config` value containing TOML list syntax.
- Unterminated quote in `exec_flags`.
- Missing or empty `model_reasoning_effort`.
- Unsupported reasoning effort such as `extreme`.

---

## 10. Dependencies

### Other Sessions

- Depends on: `phase01-session01-codex-invocation-compatibility`, `phase01-session02-provider-event-stream-contract`, `phase01-session03-history-path-normalization`, `phase01-session04-output-observability-polish`
- Depended by: `phase01-session06-documentation-and-release-verification`

---

## Next Steps

Run the `implement` workflow step to begin implementation.
