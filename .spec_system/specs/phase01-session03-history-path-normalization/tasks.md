# Task Checklist

**Session ID**: `phase01-session03-history-path-normalization`
**Total Tasks**: 18
**Estimated Duration**: 3-4 hours
**Created**: 2026-07-03

---

Legend: `[x]` completed; `[ ]` pending; `[P]` parallelizable; `[SNNMM]` session ref; `TNNN` task ID.

---

## Setup (3 tasks)

- [x] T001 [S0103] Verify Phase 01 Session 03 scope, prerequisites, and smoke evidence (`.spec_system/PRD/phase_01/session_03_history_path_normalization.md`, `.spec_system/PRD/phase_01/PRD_phase_01.md`)
- [x] T002 [S0103] Inspect current path normalization, run-mode startup flow, and SQLite history helpers (`src/apex_infinite/cli.py`)
- [x] T003 [S0103] Inspect existing temporary DB and Click history fixtures for reusable regression coverage (`tests/test_cli_options.py`, `tests/test_history_rendering.py`)

---

## Foundation (4 tasks)

- [x] T004 [S0103] Create a shared project-path history-key normalization helper with expanduser, existing-directory validation, and single trailing-slash output (`src/apex_infinite/cli.py`)
- [x] T005 [S0103] Replace run-mode inline path expansion and validation with the shared helper while preserving `project_resolved` event payloads (`src/apex_infinite/cli.py`)
- [x] T006 [S0103] Apply the shared helper before scoped `db_fetch_history()` and `db_show_history()` queries while preserving unscoped global history (`src/apex_infinite/cli.py`)
- [x] T007 [S0103] Confirm the normal loop write path uses the same normalized key before `db_log()` inserts rows with parameterized SQLite statements (`src/apex_infinite/cli.py`)

---

## Implementation (7 tasks)

- [x] T008 [S0103] Add helper-level tests for existing directories with trailing slash, without trailing slash, and expanded path input (`tests/test_cli_options.py`)
- [x] T009 [S0103] Update history-mode Click coverage to expect a normalized path and no loop startup (`tests/test_cli_options.py`)
- [x] T010 [S0103] Add unscoped history-mode Click coverage proving global history still passes `None` to the DB renderer path (`tests/test_cli_options.py`)
- [x] T011 [S0103] Add SQLite regression coverage for a row logged under a trailing-slash key and queried without the trailing slash (`tests/test_history_rendering.py`)
- [x] T012 [S0103] Add SQLite regression coverage for a row logged from no-trailing-slash input and queried with a trailing slash (`tests/test_history_rendering.py`)
- [x] T013 [S0103] Assert raw history rows keep legacy columns and contain no display-only labels, ANSI escapes, Rich markup, or frame glyphs after normalized lookup (`tests/test_history_rendering.py`)
- [x] T014 [S0103] [P] Update history lookup documentation and troubleshooting examples for trailing-slash tolerant scoped reads (`docs/history-db.md`, `docs/operator-runbook.md`, `docs/troubleshooting.md`)

---

## Testing (4 tasks)

- [x] T015 [S0103] Run focused history and Click regression tests (`python -m pytest tests/test_cli_options.py tests/test_history_rendering.py -v`)
- [x] T016 [S0103] Run the full project regression suite (`python -m pytest tests/ -v`)
- [x] T017 [S0103] Run formatter checks for source and test files (`python -m black --check src tests`)
- [x] T018 [S0103] Validate ASCII and LF requirements for changed source, docs, tests, state, and session artifacts (`src/apex_infinite/cli.py`, `tests/test_cli_options.py`, `tests/test_history_rendering.py`, `docs/history-db.md`, `docs/operator-runbook.md`, `docs/troubleshooting.md`, `.spec_system/specs/phase01-session03-history-path-normalization/`)

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
