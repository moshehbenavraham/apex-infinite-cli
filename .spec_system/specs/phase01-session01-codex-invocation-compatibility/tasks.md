# Task Checklist

**Session ID**: `phase01-session01-codex-invocation-compatibility`
**Total Tasks**: 16
**Estimated Duration**: 3-4 hours
**Created**: 2026-07-03

---

Legend: `[x]` completed; `[ ]` pending; `[P]` parallelizable; `[SNNMM]` session ref; `TNNN` task ID.

---

## Setup (3 tasks)

- [x] T001 [S0101] Verify current local Codex CLI help and supported full-auto flag evidence (`codex exec --help`)
- [x] T002 [S0101] Inspect stale flag references in source, docs, transcripts, and tests (`src/apex_infinite/config.yaml`, `src/apex_infinite/cli.py`, `README.md`, `tests/`)
- [x] T003 [S0101] Confirm the startup insertion point for non-dry-run validation before `infinite_loop()` (`src/apex_infinite/cli.py`)

---

## Foundation (4 tasks)

- [x] T004 [S0101] Add a shared default Codex exec flag constant and use it in agent fallback config (`src/apex_infinite/cli.py`)
- [x] T005 [S0101] Implement non-mutating Codex flag compatibility validation against `codex exec --help` with timeout and explicit failure-path handling (`src/apex_infinite/cli.py`)
- [x] T006 [S0101] Wire non-dry-run startup validation after project resolution and before loop startup with machine-output-safe error mapping (`src/apex_infinite/cli.py`)
- [x] T007 [S0101] Update packaged config to the supported Codex execution flag (`src/apex_infinite/config.yaml`)

---

## Implementation (5 tasks)

- [x] T008 [S0101] [P] Update README config sample and real-run policy text (`README.md`)
- [x] T009 [S0101] [P] Update operator startup checklist for target, provider, model, binary, and flag review (`docs/operator-runbook.md`)
- [x] T010 [S0101] [P] Add troubleshooting guidance for stale or rejected Codex exec flags (`docs/troubleshooting.md`)
- [x] T011 [S0101] [P] Refresh the plain dry-run transcript flag output (`docs/transcripts/dry-run-plain.txt`)
- [x] T012 [S0101] Preserve prompt routing, SQLite history shape, event payload safety, and subprocess capture semantics while applying the startup change (`src/apex_infinite/cli.py`)

---

## Testing (4 tasks)

- [x] T013 [S0101] [P] Update subprocess tests for default command construction, accepted flags, stale flags, and missing-binary handling (`tests/test_subprocess_execution.py`)
- [x] T014 [S0101] [P] Add Click startup tests for stale non-dry-run flags and dry-run inspection behavior (`tests/test_cli_options.py`)
- [x] T015 [S0101] Run focused regression checks for the changed boundaries (`python -m pytest tests/test_subprocess_execution.py tests/test_cli_options.py -v`)
- [x] T016 [S0101] Run full quality checks and ASCII/LF verification (`python -m pytest tests/ -v`, `python -m black --check src tests`, `python -m mypy`, `python -m pylint src tests`)

---

## Completion Checklist

- [x] All tasks marked `[x]`
- [x] All tests and checks passing
- [x] All files ASCII-encoded with LF line endings
- [x] implementation-notes.md updated
- [x] Ready for `validate` (creview report generated)

---

## Next Steps

Run the `validate` workflow step.
