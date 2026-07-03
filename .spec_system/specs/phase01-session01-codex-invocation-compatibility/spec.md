# Session Specification

**Session ID**: `phase01-session01-codex-invocation-compatibility`
**Phase**: 01 - Smoke Remediation And Release Hardening
**Status**: Not Started
**Created**: 2026-07-03
**Base Commit**: 4d25117b2f98a0de78cb3aec58d38120f0990d38

---

## 1. Session Overview

This session restores compatible default `codex exec` subprocess invocation for real, non-dry-run runs of Apex Infinite CLI. The 2026-07-03 smoke report shows the packaged default `--dangerously-auto-approve` is rejected by the installed Codex CLI, while `codex exec --help` exposes `--dangerously-bypass-approvals-and-sandbox` as the current broad-autonomy flag.

The work is first in Phase 01 because the default real subprocess path is release-blocking and later agent configuration semantics depend on the supported invocation policy chosen here. The implementation should update packaged defaults, runtime fallback defaults, operator docs, and tests without changing manager prompt routing, SQLite history storage, event payload safety, or subprocess capture semantics.

---

## 2. Objectives

1. Replace stale default Codex execution flags with the supported current Codex CLI flag in packaged config and runtime fallback behavior.
2. Add a non-mutating compatibility check that fails early when configured `codex.exec_flags` are stale for non-dry-run startup.
3. Document the operator policy for the supported broad-autonomy Codex flag, including dry-run first guidance and target/provider/model review.
4. Add regression coverage that catches stale flags while preserving existing prompt routing, history, and subprocess behavior.

---

## 3. Prerequisites

### Required Sessions

- [x] `phase00-session08-release-verification` - Produced the smoke report that identified the stale default Codex flag.
- [x] `phase01` stubs - `.spec_system/PRD/phase_01/` exists and `analyze-project.sh --json` reports six uncompleted Phase 01 sessions.

### Required Tools Or Knowledge

- Local Codex CLI help output from `codex exec --help`.
- Existing Click startup path, subprocess boundary, and renderer/event error handling in `src/apex_infinite/cli.py`.
- Existing pytest fixtures in `tests/test_subprocess_execution.py` and `tests/test_cli_options.py`.

### Environment Requirements

- Repository root: `/home/aiwithapex/projects/apex-infinite-cli`.
- Codex CLI installed on `PATH` for local help verification.
- Unit tests must avoid launching a real mutating Codex prompt.

---

## 4. Scope

### In Scope (MVP)

- Operator can run packaged non-dry-run defaults against the current Codex CLI without the stale `--dangerously-auto-approve` rejection.
- Operator gets an early startup failure when non-dry-run configuration contains Codex exec flags not accepted by `codex exec --help`.
- Maintainer can update one runtime default source for the selected Codex exec flag and reuse it in fallback config behavior.
- Maintainer can rely on focused tests for command construction, stale flag rejection, and startup behavior.
- Operator documentation names the supported broad-autonomy flag and explains the review/dry-run policy before real runs.

### Out Of Scope (Deferred)

- `exec_flags` shell-aware tokenization or YAML-list migration - Reason: Session 05 owns tokenization hardening.
- `model_reasoning_effort` translation or removal - Reason: Session 05 owns reasoning-effort semantics.
- Provider event schema fixes - Reason: Session 02 owns provider preflight event contract.
- History path normalization - Reason: Session 03 owns SQLite history lookup behavior.
- Broad autonomous execution safety UX beyond the flag policy text and startup compatibility check - Reason: larger safety controls remain an open security follow-up.

---

## 5. Technical Approach

### Architecture

Keep the fix inside the current CLI boundary. Add a small default flag constant and a non-mutating compatibility helper in `src/apex_infinite/cli.py`, use that constant from `get_agent_config()`, and call the compatibility helper during non-dry-run startup after project path resolution and before the autonomous loop begins. The helper should inspect `codex exec --help` rather than launching a real Codex agent prompt.

The startup failure path should reuse existing Click/startup error handling so machine-output stdout remains reserved for JSONL and human output stays renderer-owned. Documentation and tests should change with the default so the README, operator runbook, config, and subprocess tests agree.

### Design Patterns

- Single source of default config truth: keeps packaged config and runtime fallback aligned.
- Non-mutating preflight helper: proves flag compatibility without running project-changing Codex instructions.
- Focused regression tests: exercises command construction and startup rejection without real LLM or Codex agent execution.
- Renderer/event-safe error handling: preserves machine-output isolation and raw durable facts.

---

## 6. Deliverables

### Files To Create

| File | Purpose | Est. Lines |
|------|---------|------------|
| None | No new runtime or test files are expected; the session modifies existing source, docs, and tests. | 0 |

### Files To Modify

| File | Changes | Est. Lines |
|------|---------|------------|
| `src/apex_infinite/config.yaml` | Replace packaged stale `codex.exec_flags` default. | ~2 |
| `src/apex_infinite/cli.py` | Add shared default, compatibility helper, and non-dry-run startup validation. | ~80 |
| `README.md` | Update config sample and real-run operator policy. | ~25 |
| `docs/operator-runbook.md` | Clarify startup checklist and dry-run policy for real Codex flags. | ~20 |
| `docs/troubleshooting.md` | Add stale Codex flag troubleshooting guidance. | ~20 |
| `docs/transcripts/dry-run-plain.txt` | Refresh default flag shown in the transcript. | ~5 |
| `tests/test_subprocess_execution.py` | Update command construction expectations and add flag compatibility helper tests. | ~80 |
| `tests/test_cli_options.py` | Add startup validation tests for stale flags and dry-run behavior. | ~80 |

---

## 7. Success Criteria

### Functional Requirements

- [ ] Packaged default `codex.exec_flags` no longer contains `--dangerously-auto-approve`.
- [ ] Runtime fallback defaults no longer produce `--dangerously-auto-approve`.
- [ ] Non-dry-run startup fails before the main loop when configured Codex flags are rejected by local `codex exec --help`.
- [ ] Dry-run remains usable for inspecting configured commands without launching a Codex subprocess.
- [ ] README and runbook explain the selected broad-autonomy policy and tell operators to review target path, provider, model, binary, and flags before real runs.

### Testing Requirements

- [ ] Focused subprocess tests cover accepted and stale Codex exec flags.
- [ ] Click startup tests cover stale flag rejection and dry-run behavior.
- [ ] Existing prompt-routing and subprocess capture tests remain green.

### Non-Functional Requirements

- [ ] Startup compatibility check is non-mutating and bounded.
- [ ] No provider secrets, Rich markup, ANSI escapes, or display-only renderer tokens are written to history or event payloads.
- [ ] Existing SQLite schema and legacy `cc_response` behavior remain unchanged.

### Quality Gates

- [ ] All files ASCII-encoded.
- [ ] Unix LF line endings.
- [ ] Code follows project conventions.
- [ ] `python -m pytest tests/test_subprocess_execution.py tests/test_cli_options.py -v` passes.
- [ ] `python -m pytest tests/ -v` passes or any unrelated pre-existing failures are documented.
- [ ] `python -m black --check src tests` passes.

---

## 8. Implementation Notes

### Working Assumptions

- Supported replacement flag: `--dangerously-bypass-approvals-and-sandbox` is the current compatible broad-autonomy flag. Evidence: local `codex exec --help` lists this flag and not `--dangerously-auto-approve`; the smoke report records a successful nested smoke with this replacement. Planning can proceed because the session's acceptance criteria require a working default or documented policy.
- Compatibility check shape: inspect `codex exec --help` during non-dry-run startup instead of launching a real nested agent prompt. Evidence: the smoke report recommends a startup compatibility check or non-mutating smoke fixture; the CLI must avoid project mutation before the loop. Planning can proceed because help inspection is sufficient to catch the stale default flag.
- Tokenization remains current-behavior scoped: the compatibility helper should align with current command construction and avoid solving quoted flag parsing. Evidence: Session 05 explicitly owns `exec_flags.split()` hardening. Planning can proceed because the stale packaged default is a single long flag.

### Conflict Resolutions

- Security finding [P00-S02] calls for safer autonomous execution controls, while Phase 01 Session 01 must restore a working default non-dry-run invocation. The chosen interpretation is to use the current supported broad-autonomy flag for compatibility, document it clearly as dangerous, and leave broader safety gates to a future scoped session.
- The smoke report leaves open whether the default should be full-auto or operator-selected. The chosen interpretation is that this session should keep the existing unattended-operation product posture but make it compatible and explicit, because the session success criteria require the default nested Codex smoke to stop failing.

### Key Considerations

- Do not edit `MANAGER_SYSTEM_PROMPT`, `SUMMARIZER_SYSTEM_PROMPT`, or `build_codex_prompt()`.
- Preserve stdout, stderr, return code, timeout, dry-run, missing-binary, and generic exception behavior for Codex execution.
- Treat `codex.exec_flags` as security-sensitive operator policy text; never print secrets or provider keys while reporting validation errors.

### Potential Challenges

- Codex help wording can change: keep tests fixture-driven and verify against current local help in manual smoke rather than brittle full help snapshots.
- Non-dry-run startup validation could duplicate missing-binary behavior: route errors through startup handling with clear text while keeping existing execution-time missing-binary tests intact.
- Machine-output mode can be contaminated by human errors: reuse existing `_exit_with_startup_error()` and `_emit_event()` behavior.

### Relevant Considerations

- [P00] **Autonomous execution controls**: The plan adds explicit operator policy text for real runs and keeps the broader safety gate as future work.
- [P00] **Provider and Codex prerequisites**: The compatibility check must not print, store, or emit provider API keys.
- [P00] **Prompt contract coupling**: Prompt routing stays unchanged; this session changes subprocess flags and startup validation only.
- [P00] **Raw durable facts only**: Validation errors must not introduce Rich markup, ANSI escapes, or display-only tokens into history or event payloads.
- [P00] **Machine-output isolation**: Startup validation must keep stdout JSONL-only when `--machine-output` is active.

### Behavioral Quality Focus

Checklist active: Yes

Top behavioral risks for this session:

- Startup validation accidentally launches a real Codex agent instead of help inspection.
- Stale flag failures surface after provider setup or loop startup instead of failing early with explicit error mapping.
- Dry-run and machine-output modes regress while adding the compatibility check.

---

## 9. Testing Strategy

### Unit Tests

- Test default agent config returns the supported flag when config omits `codex.exec_flags`.
- Test compatibility helper accepts the supported local help fixture.
- Test compatibility helper rejects `--dangerously-auto-approve` with clear error text.
- Test `execute_codex()` command construction uses the updated default flag and preserves stdout/stderr behavior.

### Integration Tests

- Use `CliRunner` to verify non-dry-run startup rejects stale configured flags before entering `infinite_loop()`.
- Use `CliRunner` to verify dry-run startup still reaches the loop without launching Codex.
- Verify event-stream or machine-output startup errors do not mix human text into stdout.

### Runtime Verification

- Run `codex exec --help` and confirm the selected flag is present.
- Run focused pytest files for subprocess and CLI startup.
- Run the full pytest suite after focused checks pass.

### Edge Cases

- Missing Codex binary.
- Empty `exec_flags`.
- Stale single long flag.
- Supported flag plus `--skip-provider-check`.
- Machine-output startup error path.

---

## 10. Dependencies

### Other Sessions

- Depends on: `phase00-session08-release-verification`
- Depended by: `phase01-session02-provider-event-stream-contract`, `phase01-session05-agent-config-semantics`, `phase01-session06-documentation-and-release-verification`

---

## Next Steps

Run the `implement` workflow step to begin implementation.
