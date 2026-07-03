# Session Specification

**Session ID**: `phase01-session02-provider-event-stream-contract`
**Phase**: 01 - Smoke Remediation And Release Hardening
**Status**: Complete
**Created**: 2026-07-03
**Base Commit**: 67e1231b9e4aec6efa3c1b2e13b92c578fdcb0e1

---

## 1. Session Overview

This session restores the provider preflight lifecycle event contract for JSONL event-stream consumers. Current startup code already emits `provider_check_started`, `provider_check_failed`, and `provider_check_finished`, but the event registry in `src/apex_infinite/events.py` does not accept those names, so valid provider preflight runs can create `event_stream_error` rows.

The session is next because Phase 01 Session 01 is complete, and the smoke report names the provider event schema mismatch as the remaining event-stream contract bug. Fixing it now stabilizes wrapper and automation consumers before later history, output polish, agent config, and final release verification work.

---

## 2. Objectives

1. Register provider preflight lifecycle event names so existing provider emits are valid JSONL events.
2. Add regression coverage for `--check-provider --event-stream` success and startup provider preflight file-stream success.
3. Add regression coverage for startup provider preflight with `--event-stream - --machine-output` while preserving stdout JSONL isolation.
4. Cover provider preflight failure events so `provider_check_failed` is accepted and does not degrade into `event_stream_error`.

---

## 3. Prerequisites

### Required Sessions

- [x] `phase01-session01-codex-invocation-compatibility` - Restored compatible Codex startup behavior and added startup event patterns used by this session.
- [x] `phase00-session04-event-stream-boundary` - Created the importable JSONL event emitter API and validation boundary.
- [x] `phase00-session08-release-verification` - Produced the smoke report identifying the provider event schema mismatch.

### Required Tools Or Knowledge

- Existing `EventEmitter` validation and event registry in `src/apex_infinite/events.py`.
- Provider preflight emit path in `_run_provider_preflight_or_exit()` in `src/apex_infinite/cli.py`.
- Existing Click and event-stream fixtures in `tests/test_cli_options.py` and `tests/test_event_stream.py`.

### Environment Requirements

- Repository root: `/home/aiwithapex/projects/apex-infinite-cli`.
- Python test environment with pytest available.
- Tests must patch provider preflight calls and avoid requiring a live provider.

---

## 4. Scope

### In Scope (MVP)

- Automation consumer can read provider preflight lifecycle rows from file event streams without `event_stream_error` fallback rows.
- Wrapper consumer can read startup provider preflight rows from stdout JSONL when `--event-stream - --machine-output` is active.
- Maintainer can validate provider preflight success and failure event names through focused tests.
- Operator can run `--check-provider --event-stream PATH` and receive provider lifecycle events without changing human output behavior.
- Documentation consumer can see provider preflight event names in the event-stream contract.

### Out Of Scope (Deferred)

- Provider client redesign - Reason: this session fixes event contract registration only.
- Full OpenAI, Grok, and Ollama matrix testing - Reason: patched provider preflight tests prove the CLI event contract without external services.
- Plain output label polish for provider preflight - Reason: Session 04 owns provider preflight renderer labels and response preview behavior.
- History path normalization - Reason: Session 03 owns SQLite history lookup behavior.
- Agent config parsing and reasoning-effort behavior - Reason: Session 05 owns Codex agent config semantics.

---

## 5. Technical Approach

### Architecture

Keep the runtime behavior narrow and event-contract focused. The provider preflight path in `src/apex_infinite/cli.py` already emits the intended lifecycle names and raw provider facts, so the primary code change should register those names in `src/apex_infinite/events.py`. If tests expose a payload or ordering mismatch, adjust the provider preflight emit path without changing provider client behavior.

Add focused tests at the existing boundaries. Use `EventEmitter` validation tests for the registry, and `CliRunner` tests for `--check-provider`, normal startup preflight, machine-output stdout, and failure paths. Update `docs/event-stream.md` so the documented contract matches the accepted event names.

### Design Patterns

- Registry-first event validation: keeps event names explicit and importable for tests and wrappers.
- Existing fixture reuse: patches provider preflight calls instead of depending on a live local model.
- Machine-output isolation: verifies stdout remains JSONL-only when `--machine-output` is active.
- Contract documentation with tests: event names are added to docs and regression tests together.

---

## 6. Deliverables

### Files To Create

| File | Purpose | Est. Lines |
|------|---------|------------|
| None | No new runtime or test files are expected; this session modifies existing source, docs, and tests. | 0 |

### Files To Modify

| File | Changes | Est. Lines |
|------|---------|------------|
| `src/apex_infinite/events.py` | Register provider preflight event names in the stable event-name set. | ~5 |
| `src/apex_infinite/cli.py` | Preserve or adjust provider preflight emit payloads only if tests expose a contract mismatch. | ~20 |
| `docs/event-stream.md` | Document provider preflight event names in the startup and configuration event list. | ~10 |
| `tests/test_event_stream.py` | Add registry coverage for provider preflight event names. | ~20 |
| `tests/test_cli_options.py` | Add Click regression tests for provider preflight file streams, stdout machine output, and failure events. | ~120 |
| `tests/test_provider_preflight.py` | Add focused direct preflight failure or success event coverage if CLI tests leave a gap. | ~40 |

---

## 7. Success Criteria

### Functional Requirements

- [ ] `provider_check_started`, `provider_check_failed`, and `provider_check_finished` are accepted by the event schema.
- [ ] `--check-provider --event-stream PATH` writes provider preflight events and no `event_stream_error` rows.
- [ ] Normal startup provider preflight with `--event-stream PATH` writes provider preflight events before loop startup.
- [ ] Normal startup provider preflight with `--event-stream - --machine-output` emits JSONL-only stdout including provider preflight events.
- [ ] Provider preflight failures emit `provider_check_failed` plus the startup `error` event without an invalid-event fallback.

### Testing Requirements

- [ ] Event emitter tests cover the provider preflight event-name registry.
- [ ] Click tests cover `--check-provider` file event-stream success.
- [ ] Click tests cover startup file event-stream success and machine-output stdout success.
- [ ] Click tests cover provider preflight failure event output.
- [ ] Existing provider preflight, event-stream, and CLI option tests remain green.

### Non-Functional Requirements

- [ ] Event payloads contain raw operational facts only and no API keys or provider config maps.
- [ ] Machine-output mode keeps human rendering, terminal bells, and notifications off stdout.
- [ ] JSONL remains ASCII-safe and line-buffered.
- [ ] No SQLite schema, history row, prompt-routing, or subprocess capture behavior changes.

### Quality Gates

- [ ] All files ASCII-encoded.
- [ ] Unix LF line endings.
- [ ] Code follows project conventions.
- [ ] `python -m pytest tests/test_event_stream.py tests/test_cli_options.py tests/test_provider_preflight.py -v` passes.
- [ ] `python -m pytest tests/ -v` passes or any unrelated pre-existing failures are documented.
- [ ] `python -m black --check src tests` passes.

---

## 8. Implementation Notes

### Working Assumptions

- Registering provider event names is safer than renaming emits. Evidence: `_run_provider_preflight_or_exit()` already emits `provider_check_started`, `provider_check_failed`, and `provider_check_finished`, the smoke report names these exact events, and the ongoing product plan references the same names. Planning can proceed because the mismatch is between existing emits and the registry, not between two competing runtime designs.
- Patched provider preflight tests are sufficient for the contract fix. Evidence: existing `tests/test_cli_options.py` already patches `run_provider_preflight()` for startup wiring and `tests/test_provider_preflight.py` separately covers provider-client behavior. Planning can proceed without a live provider because this session tests event validity and output isolation.
- Updating `docs/event-stream.md` is required even though the session stub emphasizes code and tests. Evidence: the event-stream contract document lists accepted names for consumers, and Session 01 updated it when new startup events were added. Planning can proceed because a small docs update keeps consumer-facing contract text aligned.

### Conflict Resolutions

- The session stub allows either registering provider events or renaming provider emits to approved names. The chosen interpretation is to register the existing `provider_check_*` names because they are semantically precise, already emitted by `src/apex_infinite/cli.py`, and already cited by the smoke follow-up plan.
- The Phase 01 smoke split says Session 02 has no dependencies, while the session stub notes Session 01 should be complete or confirmed not to affect provider startup behavior. The chosen interpretation is to plan Session 02 after Session 01 because `analyze-project.sh --json` reports Session 01 complete and its startup changes shape the nearby event-stream tests.

### Key Considerations

- Keep provider API keys out of event payloads, history rows, logs, and docs.
- Preserve event side-channel behavior; wrappers must consume JSONL events instead of scraping terminal output.
- Do not change prompt routing, manager prompts, SQLite history shape, or Codex subprocess behavior.
- Keep `--event-stream - --machine-output` stdout reserved for JSONL only.

### Potential Challenges

- Event ordering can differ between `--check-provider` mode and normal startup: write assertions around required subsequences instead of brittle full-run sequences where unrelated startup events can legitimately appear.
- Failure-path startup exits can bypass loop fixtures: assert the event file/stdout rows and captured loop absence explicitly.
- Event payload validation may reject unsafe strings from provider exceptions: keep failure messages explicit but free of secrets and renderer markup.

### Relevant Considerations

- [P00] **Raw durable facts only**: Provider event payloads must stay free of ANSI escapes, Rich markup, frame glyphs, display tokens, and secrets.
- [P00] **Machine-output isolation**: Stdout JSONL must not mix with Rich or plain human output when machine-output mode is active.
- [P00] **Provider and Codex prerequisites**: Provider API keys and provider availability are runtime prerequisites; tests must not print or emit secrets.
- [P00] **Event stream is the wrapper contract**: Visual surfaces consume provider lifecycle facts from events, not human output.
- [P00] **Guarded machine stdout**: `--event-stream -` remains valid only with `--machine-output`.

### Behavioral Quality Focus

Checklist active: Yes

Top behavioral risks for this session:

- Existing provider preflight emits continue to produce invalid event fallbacks because registry coverage is incomplete.
- Provider failure events leak sensitive provider configuration or produce unsafe payload strings.
- Machine-output startup paths mix human text with JSONL while adding provider event tests.

---

## 9. Testing Strategy

### Unit Tests

- Test `EventEmitter.emit()` accepts `provider_check_started`, `provider_check_failed`, and `provider_check_finished`.
- Test provider preflight failure payloads stay JSON-safe and avoid API keys if direct preflight helper coverage is needed.

### Integration Tests

- Use `CliRunner` to run `--check-provider --event-stream PATH --plain` with patched provider success and assert provider events are persisted.
- Use `CliRunner` to run normal startup with `--event-stream PATH --max-iterations 0` and assert provider events appear without `event_stream_error`.
- Use `CliRunner` to run normal startup with `--event-stream - --machine-output --max-iterations 0` and assert stdout parses as JSONL only and includes provider events.
- Use `CliRunner` to run provider failure with an event stream and assert `provider_check_failed` and `error` are emitted before exit.

### Runtime Verification

- Run focused pytest files for event stream, CLI options, and provider preflight.
- Run full pytest after focused checks pass.
- Run `python -m black --check src tests`.

### Edge Cases

- `--check-provider` mode without a project path.
- Provider preflight failure before loop startup.
- File event stream with normal human output still enabled.
- Stdout event stream with machine-output isolation.
- Provider exception messages that must remain JSON-safe.

---

## 10. Dependencies

### Other Sessions

- Depends on: `phase01-session01-codex-invocation-compatibility`
- Depended by: `phase01-session04-output-observability-polish`, `phase01-session06-documentation-and-release-verification`

---

## Next Steps

Run the `implement` workflow step to begin implementation.
