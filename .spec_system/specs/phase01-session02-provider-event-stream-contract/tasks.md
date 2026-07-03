# Task Checklist

**Session ID**: `phase01-session02-provider-event-stream-contract`
**Total Tasks**: 17
**Estimated Duration**: 3-4 hours
**Created**: 2026-07-03

---

Legend: `[x]` completed; `[ ]` pending; `[P]` parallelizable; `[SNNMM]` session ref; `TNNN` task ID.

---

## Setup (3 tasks)

- [x] T001 [S0102] Verify Session 01 completion and provider event contract failure evidence (`.spec_system/specs/phase01-session01-codex-invocation-compatibility/validation.md`, `.spec_system/PRD/phase_01/platform_smoke_run_report_2026_07_03.md`)
- [x] T002 [S0102] Inspect provider preflight event emits and event-name validation boundaries (`src/apex_infinite/cli.py`, `src/apex_infinite/events.py`)
- [x] T003 [S0102] Inspect existing event-stream and Click test fixtures for reusable provider preflight patches (`tests/test_event_stream.py`, `tests/test_cli_options.py`, `tests/test_provider_preflight.py`)

---

## Foundation (4 tasks)

- [x] T004 [S0102] Register provider preflight lifecycle names in the stable event-name registry (`src/apex_infinite/events.py`)
- [x] T005 [S0102] Confirm provider preflight started, failed, and finished payloads contain only raw provider facts and no secrets (`src/apex_infinite/cli.py`)
- [x] T006 [S0102] Update the event-stream contract with provider preflight event names and startup semantics (`docs/event-stream.md`)
- [x] T007 [S0102] Add event-name registry coverage for all provider preflight lifecycle events (`tests/test_event_stream.py`)

---

## Implementation (6 tasks)

- [x] T008 [S0102] Add `--check-provider --event-stream PATH` success coverage with valid provider events and no invalid-event fallback (`tests/test_cli_options.py`)
- [x] T009 [S0102] Add normal startup file event-stream coverage for successful provider preflight before loop startup (`tests/test_cli_options.py`)
- [x] T010 [S0102] Add normal startup stdout machine-output coverage for provider preflight with JSONL-only stdout and no human rendering (`tests/test_cli_options.py`)
- [x] T011 [S0102] Add provider preflight failure file-stream coverage for `provider_check_failed` and startup `error` events (`tests/test_cli_options.py`)
- [x] T012 [S0102] Add provider preflight failure machine-output coverage when needed to prove failure JSONL remains machine-only (`tests/test_cli_options.py`)
- [x] T013 [S0102] Preserve check-provider early-return behavior, startup loop entry behavior, prompt routing, SQLite history shape, and subprocess semantics while applying fixes (`src/apex_infinite/cli.py`)

---

## Testing (4 tasks)

- [x] T014 [S0102] [P] Run focused event-stream and provider preflight regression tests (`python -m pytest tests/test_event_stream.py tests/test_cli_options.py tests/test_provider_preflight.py -v`)
- [x] T015 [S0102] Run full project regression tests (`python -m pytest tests/ -v`)
- [x] T016 [S0102] Run formatter check for changed Python files (`python -m black --check src tests`)
- [x] T017 [S0102] Validate ASCII and LF requirements for changed source, docs, tests, and session artifacts (`src/apex_infinite/events.py`, `src/apex_infinite/cli.py`, `docs/event-stream.md`, `tests/test_event_stream.py`, `tests/test_cli_options.py`, `.spec_system/specs/phase01-session02-provider-event-stream-contract/`)

---

## Completion Checklist

- [x] All tasks marked `[x]`
- [x] All tests and checks passing
- [x] All files ASCII-encoded with LF line endings
- [x] implementation-notes.md updated
- [x] Ready for `creview` (next step in the implement -> creview -> validate sequence)

---

## Next Steps

Run the `creview` workflow step.
