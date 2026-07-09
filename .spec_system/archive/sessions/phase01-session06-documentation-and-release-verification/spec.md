# Session Specification

**Session ID**: `phase01-session06-documentation-and-release-verification`
**Phase**: 01 - Smoke Remediation And Release Hardening
**Status**: Not Started
**Created**: 2026-07-03
**Base Commit**: 2af49cf4b9a07ffa05b8bf1072964b097f6531c4

---

## 1. Session Overview

This session closes Phase 01 by turning the smoke-run environment warning into
operator documentation and rerunning the full release-hardening verification
matrix after Sessions 01 through 05. The earlier sessions fixed Codex invocation
compatibility, provider event schema registration, history path normalization,
plain-output labels, response previews, exec flag parsing, and reasoning-effort
command construction.

The work is next because the phase has one unfinished session and all required
functional remediation sessions are complete. The session should not add product
features. It should make the local smoke setup repeatable, rerun the documented
quality and smoke commands from an explicit repository environment, and record
final pass/fail evidence in the phase smoke report and release notes.

This advances the phase from implementation fixes to release evidence. Any new
release-blocking failure discovered during verification should be recorded with
exact command output and scope, instead of silently expanding this session into a
new feature or broad bug-fix effort.

---

## 2. Objectives

1. Document reliable local smoke setup, including stale activated virtualenv
   detection and an explicit repository virtualenv workflow.
2. Rerun the full local quality suite and package build from a known Python
   environment.
3. Rerun provider, event-stream, history, visual-wrapper, and nested Codex smoke
   scenarios with isolated temporary artifacts.
4. Update final release-hardening evidence so Phase 01 has an auditable
   pass/fail record and no untracked provider substitution.

---

## 3. Prerequisites

### Required Sessions

- [x] `phase01-session01-codex-invocation-compatibility` - Provides the supported Codex execution flag policy and startup compatibility checks.
- [x] `phase01-session02-provider-event-stream-contract` - Provides valid provider preflight lifecycle events for file and machine-output streams.
- [x] `phase01-session03-history-path-normalization` - Provides normalized history lookup behavior for scoped history checks.
- [x] `phase01-session04-output-observability-polish` - Provides user-facing plain labels and response summary preview behavior.
- [x] `phase01-session05-agent-config-semantics` - Provides shell-aware exec flag parsing and active reasoning-effort command construction.

### Required Tools Or Knowledge

- Python 3.10+ with `venv`, `pip`, and local package build support.
- Codex CLI installed on `PATH` or configured through `codex.binary`.
- Local Ollama at `http://localhost:11434/v1` with `qwen2.5-coder:7b-instruct-q4_K_M`, or an equivalent provider substitution recorded in the smoke report.
- Existing smoke source at `.spec_system/PRD/phase_01/platform_smoke_run_report_2026_07_03.md`.
- Existing docs in `README.md`, `docs/operator-runbook.md`, and `docs/troubleshooting.md`.

### Environment Requirements

- Repository root: `/home/aiwithapex/projects/apex-infinite-cli`.
- Use an explicit repository virtualenv such as `.venv` or a named smoke venv,
  not a shell `python` that points to another project.
- Use temporary smoke outputs under `/tmp/apex-infinite-cli-smoke-*` and
  `/tmp/apex-infinite-smoke-*.jsonl`.
- Keep the worktree clean before and after the actual nested Codex smoke.

---

## 4. Scope

### In Scope (MVP)

- Developer can identify when shell `python` resolves to a stale virtualenv from another project.
- Developer can create and invoke an explicit repository virtualenv for smoke runs.
- Maintainer can rerun `pytest`, `black`, `mypy`, `pylint`, `pip-audit`, and package build commands from the chosen Python.
- Maintainer can rerun provider preflight, provider chat preflight, dry-run loop, machine-output JSONL loop, history display, visual wrapper fixture mode, visual wrapper CLI launch mode, and actual nested Codex subprocess smoke.
- Maintainer can record provider substitutions, temporary artifact paths, pass/fail results, and any remaining release blockers in the phase smoke report.
- Operator-facing docs reflect the current supported Codex flag, reasoning-effort behavior, event-stream behavior, and local smoke setup.

### Out Of Scope (Deferred)

- Docker-based Ollama deployment from scratch - Reason: the session verifies with an available provider or records a substitution.
- Nuitka or AppImage binary packaging - Reason: visual-wrapper binary release remains gated outside Phase 01.
- New product features, CLI flags, config precedence changes, or UI redesign - Reason: this session is release verification and documentation.
- Fixing newly discovered release blockers beyond narrow documentation corrections - Reason: a new runtime blocker should be recorded for a follow-up scoped session.
- Privacy retention, purge, dependency locking, or CI scheduling controls - Reason: these remain open security posture items outside the Phase 01 smoke-remediation scope.

---

## 5. Technical Approach

### Architecture

Keep implementation limited to documentation and verification artifacts. Add the
local smoke setup guidance to existing operator surfaces instead of creating a
new duplicate guide. Use `README.md` for the concise testing command bundle,
`docs/operator-runbook.md` for repeatable operator procedure, and
`docs/troubleshooting.md` for stale virtualenv diagnosis.

Run verification through an explicit Python executable from the selected smoke
environment. Use temporary home directories and event files to avoid polluting
operator history. Preserve the event-stream and history contracts by checking
for provider lifecycle events, absence of `event_stream_error` during successful
smokes, JSONL-only stdout in machine-output mode, and normalized scoped history
lookups.

Record final results in the existing Phase 01 smoke report. Preserve the
original smoke findings as historical evidence, and add a final verification
section that states which findings are remediated, which provider was used, what
commands were run, and whether any release-blocking failures remain.

### Design Patterns

- Existing documentation surfaces: avoids a parallel smoke guide that can drift.
- Isolated smoke artifacts: keeps local history, event files, and build outputs outside tracked source.
- Evidence-first release notes: records commands and results rather than broad claims.
- Provider substitution ledger: makes local provider differences explicit without blocking planning.
- No feature expansion: separates final verification from future productization work.

---

## 6. Deliverables

### Files To Create

| File | Purpose | Est. Lines |
|------|---------|------------|
| None | No new product files are expected; the session updates existing docs and verification records. | 0 |

### Files To Modify

| File | Changes | Est. Lines |
|------|---------|------------|
| `README.md` | Add or refine concise release smoke setup and quality command guidance. | ~35 |
| `docs/operator-runbook.md` | Add repeatable local release smoke procedure with explicit venv, temp artifacts, and provider substitution handling. | ~80 |
| `docs/troubleshooting.md` | Add stale activated virtualenv diagnosis and remediation guidance. | ~45 |
| `docs/ongoing-projects/terminal-and-linux-app-productization-plan.md` | Sync Phase 01 blocker status or link final smoke evidence after verification. | ~30 |
| `CHANGELOG.md` | Record Phase 01 smoke remediation and final verification under Unreleased. | ~20 |
| `.spec_system/PRD/phase_01/platform_smoke_run_report_2026_07_03.md` | Add final verification matrix, environment, provider substitution notes, and remaining blocker status. | ~140 |

---

## 7. Success Criteria

### Functional Requirements

- [ ] Documentation explains how to detect and avoid a stale activated virtualenv whose `python` points outside this repository.
- [ ] Documentation recommends creating and invoking an explicit repository smoke virtualenv.
- [ ] Final smoke evidence records the exact Python executable, package version, provider, Codex CLI, and temporary artifact paths used.
- [ ] Final smoke evidence records results for quality checks, provider checks, dry-run loop, machine-output JSONL loop, history display, visual wrapper modes, and actual nested Codex subprocess smoke.
- [ ] Provider substitution is recorded if local Ollama is unavailable.
- [ ] Smoke report states whether any Phase 01 release-blocking failures remain.

### Testing Requirements

- [ ] `python -m pytest tests/ -v` passes or any failure is recorded with exact scope.
- [ ] `python -m black --check src tests` passes or any failure is recorded with exact scope.
- [ ] `python -m mypy` passes or any failure is recorded with exact scope.
- [ ] `python -m pylint src tests` passes or any failure is recorded with exact scope.
- [ ] `python -m pip_audit` passes or any vulnerability is recorded with exact scope.
- [ ] `python -m build --outdir /tmp/apex-infinite-cli-smoke-dist` passes or any failure is recorded with exact scope.
- [ ] CLI and wrapper smoke commands complete with expected outputs or documented environment blockers.

### Non-Functional Requirements

- [ ] Smoke commands do not persist provider secrets, Rich markup, ANSI escapes, frame glyphs, or visual tokens into SQLite or JSONL event records.
- [ ] Machine-output stdout remains JSONL-only.
- [ ] Actual nested Codex smoke is non-mutating and the tracked worktree remains clean except for intentional documentation and spec updates.
- [ ] Base CLI verification remains terminal-only and does not require graphical dependencies unless running optional wrapper checks.

### Quality Gates

- [ ] All files ASCII-encoded.
- [ ] Unix LF line endings.
- [ ] Code follows project conventions.
- [ ] No binary screenshots or generated package artifacts are committed.
- [ ] Primary user-facing docs contain current product-facing guidance only.

---

## 8. Implementation Notes

### Working Assumptions

- Local Ollama remains the default smoke provider: the original Phase 01 report used Ollama at `http://localhost:11434/v1` with `qwen2.5-coder:7b-instruct-q4_K_M`, and README/runbook docs already describe local Ollama preflight. Planning can proceed because the session explicitly records an equivalent provider substitution if local Ollama is unavailable.
- The phase smoke report should be updated instead of replaced: it is the durable source for the original findings and the session stub names it as the release verification record. Planning can proceed because adding a final verification section preserves historical evidence while documenting remediation.
- Documentation updates belong in existing docs: `README.md`, `docs/operator-runbook.md`, and `docs/troubleshooting.md` already cover testing, operation, and failures. Planning can proceed because targeted additions reduce drift versus a new guide.

### Conflict Resolutions

- The smoke report contains historical failures while Sessions 01 through 05 are now complete. The chosen interpretation is to keep the original findings intact and append final remediation evidence with dates, commands, and current status.
- The session stub allows updating either the smoke report or release notes. The chosen interpretation is to update the smoke report as the authoritative evidence record and add a concise `CHANGELOG.md` note so release readers can find the verification result.

### Key Considerations

- Do not print, store, or emit provider API keys or full provider config maps.
- Keep wrapper verification in source/offscreen mode only; binary/AppImage gates remain deferred.
- Keep temporary smoke outputs under `/tmp` and avoid committing build outputs or JSONL smoke artifacts.
- Use explicit Python paths from the smoke environment for every quality command.
- If a smoke step is blocked by provider availability, record the blocker and the selected substitution instead of treating it as an undocumented pass.

### Potential Challenges

- Local provider unavailable: use an equivalent configured provider and record the provider name, model, and reason for substitution.
- Optional PySide6 missing: install `.[visual]` in the smoke venv or record wrapper smoke as environment-blocked with exact import or platform error.
- Actual nested Codex smoke could try to modify the repo: use a no-edit prompt, bounded one-iteration run, temporary artifacts, and `git status --short` before and after.
- Long-running checks can hide stale Python usage: include `sys.executable` and `python -m pip --version` evidence in the final report.

### Relevant Considerations

- [P00] **Provider and Codex prerequisites**: Provider availability, provider keys, and Codex CLI are runtime prerequisites; verification must not expose secrets.
- [P00] **Autonomous execution controls**: Real nested Codex smoke must make target path, provider, model, and execution flags explicit before launch.
- [P00] **Raw durable facts only**: SQLite rows and JSONL events must not contain Rich markup, ANSI escapes, frame glyphs, visual tokens, secrets, or copied-reference identifiers.
- [P00] **Machine-output isolation**: `--event-stream - --machine-output` must keep stdout reserved for JSONL only.
- [P00] **Event stream is the wrapper contract**: Wrapper smoke should consume the guarded JSONL boundary rather than Rich/plain human output.
- [P00] **Binary release gate**: Source/offscreen wrapper verification does not approve AppImage or binary publication.

---

## 9. Testing Strategy

### Unit Tests

- Run the full pytest suite with the selected smoke Python.
- Include the opt-in live Ollama test only when local Ollama is available and explicitly enabled.
- Record any skipped, xfailed, or environment-blocked tests in the final smoke report.

### Integration Tests

- Run provider model preflight and provider chat preflight.
- Run the dry-run loop with a file event stream and verify no provider event-stream contract errors appear.
- Run the machine-output JSONL loop and verify stdout contains JSONL events only.
- Run scoped history lookup with trailing-slash and no-trailing-slash path forms.
- Run visual wrapper fixture mode and visual wrapper CLI launch mode with `QT_QPA_PLATFORM=offscreen`.
- Run the actual nested Codex subprocess smoke with a no-edit prompt and bounded one-iteration execution.

### Runtime Verification

- Record `python --version`, `python -c 'import sys; print(sys.executable)'`, `python -m pip --version`, `codex --version`, `apex-infinite --version`, and `apex-infinite --help`.
- Run `python -m black --check src tests`.
- Run `python -m mypy`.
- Run `python -m pylint src tests`.
- Run `python -m pip_audit`.
- Run `python -m build --outdir /tmp/apex-infinite-cli-smoke-dist`.
- Run `git status --short` before and after the actual nested Codex smoke.

### Edge Cases

- Shell `python` resolves outside this repository.
- Provider is unavailable but an equivalent configured provider is available.
- Event stream path is unwritable or stale from a previous run.
- Machine-output mode is accidentally run without `--event-stream`.
- History path is supplied with and without a trailing slash.
- Optional wrapper dependencies are unavailable or the display backend is headless.
- Actual Codex subprocess exits non-zero or times out.

---

## 10. Dependencies

### Other Sessions

- Depends on: `phase01-session01-codex-invocation-compatibility`, `phase01-session02-provider-event-stream-contract`, `phase01-session03-history-path-normalization`, `phase01-session04-output-observability-polish`, `phase01-session05-agent-config-semantics`
- Depended by: Phase transition `audit`

---

## Next Steps

Run the `implement` workflow step to begin implementation.
