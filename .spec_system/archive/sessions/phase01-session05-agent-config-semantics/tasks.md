# Task Checklist

**Session ID**: `phase01-session05-agent-config-semantics`
**Total Tasks**: 18
**Estimated Duration**: 3-4 hours
**Created**: 2026-07-03

---

Legend: `[x]` completed; `[ ]` pending; `[P]` parallelizable; `[SNNMM]` session ref; `TNNN` task ID.

---

## Setup (3 tasks)

- [x] T001 [S0105] Verify local Codex help and current config-key evidence for reasoning effort (`codex exec --help`, `/home/aiwithapex/.codex/config.toml`)
- [x] T002 [S0105] Inspect existing command construction, flag validation, and docs references (`src/apex_infinite/cli.py`, `README.md`, `docs/operator-runbook.md`, `docs/troubleshooting.md`)
- [x] T003 [S0105] Confirm existing tests and fixtures that reference `exec_flags` and `model_reasoning_effort` (`tests/test_subprocess_execution.py`, `tests/test_cli_options.py`, `tests/test_event_stream.py`, `tests/test_renderer.py`, `tests/test_operator_console.py`)

## Foundation (4 tasks)

- [x] T004 [S0105] Add shell-aware exec flag parsing helper with malformed-input error mapping (`src/apex_infinite/cli.py`)
- [x] T005 [S0105] Add reasoning-effort normalization and Codex config override token helper with schema-validated input and explicit error mapping (`src/apex_infinite/cli.py`)
- [x] T006 [S0105] Create a shared command-token builder used by validation and launch paths without shell invocation (`src/apex_infinite/cli.py`)
- [x] T007 [S0105] Update startup validation to use shared parsed tokens and avoid rejecting `-c` values as unsupported flags (`src/apex_infinite/cli.py`)

## Implementation (6 tasks)

- [x] T008 [S0105] Wire `execute_codex()` to launch with parsed exec flags plus reasoning-effort override tokens while preserving stdout, stderr, timeout, and error semantics (`src/apex_infinite/cli.py`)
- [x] T009 [S0105] Update dry-run command rendering and command snapshots to show the effective Codex command clearly without secrets (`src/apex_infinite/cli.py`, `src/apex_infinite/ui.py`)
- [x] T010 [S0105] Align packaged config comments and defaults with active reasoning-effort behavior (`src/apex_infinite/config.yaml`)
- [x] T011 [S0105] Update README configuration guidance for quoted exec flags and active reasoning-effort override behavior (`README.md`)
- [x] T012 [S0105] Update runbook and troubleshooting guidance for malformed exec flags, invalid reasoning effort, and real-run review (`docs/operator-runbook.md`, `docs/troubleshooting.md`)
- [x] T013 [S0105] Refresh dry-run transcript or documented command examples affected by reasoning-effort command rendering (`docs/transcripts/dry-run-plain.txt`)

## Testing (5 tasks)

- [x] T014 [S0105] Write subprocess unit tests for shell-aware tokenization, malformed flags, reasoning-effort validation, and command construction (`tests/test_subprocess_execution.py`)
- [x] T015 [S0105] Write Click startup tests for quoted flags, malformed flags, invalid reasoning effort, and dry-run visibility (`tests/test_cli_options.py`)
- [x] T016 [S0105] Update event-stream, renderer, and operator-console fixtures affected by effective command rendering (`tests/test_event_stream.py`, `tests/test_renderer.py`, `tests/test_operator_console.py`)
- [x] T017 [S0105] Run focused and full automated checks (`python -m pytest tests/test_subprocess_execution.py tests/test_cli_options.py -v`, `python -m pytest tests/ -v`, `python -m black --check src tests`, `python -m mypy`, `python -m pylint src tests`)
- [x] T018 [S0105] Validate ASCII and LF requirements for changed files and record implementation evidence (`src/apex_infinite/cli.py`, `src/apex_infinite/config.yaml`, `README.md`, `docs/operator-runbook.md`, `docs/troubleshooting.md`, `docs/transcripts/dry-run-plain.txt`, `tests/`)

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
