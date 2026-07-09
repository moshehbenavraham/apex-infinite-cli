# Task Checklist

**Session ID**: `phase01-session04-output-observability-polish`
**Total Tasks**: 18
**Estimated Duration**: 3-4 hours
**Created**: 2026-07-03

---

Legend: `[x]` completed; `[ ]` pending; `[P]` parallelizable; `[SNNMM]` session ref; `TNNN` task ID.

---

## Setup (3 tasks)

- [x] T001 [S0104] Verify Session 04 smoke evidence, dependency completion, and selected preview contract (`.spec_system/PRD/phase_01/session_04_output_observability_polish.md`, `.spec_system/PRD/phase_01/platform_smoke_run_report_2026_07_03.md`)
- [x] T002 [S0104] Inspect current generic status label flow and provider preflight rendering call sites (`src/apex_infinite/ui.py`, `src/apex_infinite/cli.py`)
- [x] T003 [S0104] Inspect current response summary event emitters and existing renderer/event/subprocess test patterns (`src/apex_infinite/events.py`, `tests/test_renderer.py`, `tests/test_subprocess_execution.py`, `tests/test_event_stream.py`)

---

## Foundation (4 tasks)

- [x] T004 [S0104] Add a generic `STATUS` semantic label and keep critical severity labels mapped ahead of generic status fallback (`src/apex_infinite/ui.py`)
- [x] T005 [S0104] Apply the generic status label to `print_status()` and provider preflight plain output without changing error, warning, success, history, decision, prompt, or Codex labels (`src/apex_infinite/ui.py`)
- [x] T006 [S0104] Add bounded safe preview handling for response summary metadata with unsafe preview suppression for ANSI, Rich markup, frame glyph, visual-token, and secret-like content (`src/apex_infinite/events.py`)
- [x] T007 [S0104] Define and use one small nonzero response event preview limit for dry-run, success, timeout, missing-binary, and error response summaries (`src/apex_infinite/cli.py`)

---

## Implementation (7 tasks)

- [x] T008 [S0104] Add renderer tests proving generic plain status and provider preflight output use `STATUS` and never `ACCENT` (`tests/test_renderer.py`)
- [x] T009 [S0104] Add ASCII and compact renderer coverage proving provider preflight status output stays ASCII-only and keeps critical state visible (`tests/test_renderer.py`)
- [x] T010 [S0104] Extend successful provider preflight CLI coverage for `--plain`, `--ascii`, and `--compact` output labels (`tests/test_cli_options.py`)
- [x] T011 [S0104] Extend failed provider preflight CLI coverage so error output remains visible and does not expose internal severity labels (`tests/test_cli_options.py`)
- [x] T012 [S0104] Add subprocess response-summary tests for dry-run, harmless success output, bounded long output, non-zero exit, timeout, missing binary, and generic exception previews (`tests/test_subprocess_execution.py`)
- [x] T013 [S0104] Add event-stream tests proving unsafe preview text is suppressed without `event_stream_error` and without leaking forbidden payload strings (`tests/test_event_stream.py`)
- [x] T014 [S0104] [P] Update event-stream docs and deterministic machine-output transcript samples for the bounded preview contract (`docs/event-stream.md`, `docs/transcripts/machine-output-events.jsonl`)

---

## Testing (4 tasks)

- [x] T015 [S0104] Run focused renderer, CLI, subprocess, and event-stream tests (`python -m pytest tests/test_renderer.py tests/test_cli_options.py tests/test_subprocess_execution.py tests/test_event_stream.py -v`)
- [x] T016 [S0104] Run the full project regression suite (`python -m pytest tests/ -v`)
- [x] T017 [S0104] Run formatter checks for source and test files (`python -m black --check src tests`)
- [x] T018 [S0104] Validate ASCII and LF requirements for changed source, docs, tests, transcript, state, and session artifacts (`src/apex_infinite/ui.py`, `src/apex_infinite/events.py`, `src/apex_infinite/cli.py`, `tests/`, `docs/event-stream.md`, `docs/transcripts/machine-output-events.jsonl`, `.spec_system/specs/phase01-session04-output-observability-polish/`)

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
