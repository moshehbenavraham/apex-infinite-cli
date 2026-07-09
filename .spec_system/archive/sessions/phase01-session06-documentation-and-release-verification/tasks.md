# Task Checklist

**Session ID**: `phase01-session06-documentation-and-release-verification`
**Total Tasks**: 20
**Estimated Duration**: 3-4 hours
**Created**: 2026-07-03

---

Legend: `[x]` completed; `[ ]` pending; `[P]` parallelizable; `[SNNMM]` session ref; `TNNN` task ID.

---

## Setup (4 tasks)

- [x] T001 [S0106] Verify phase prerequisites, base commit, and clean starting worktree (`.spec_system/PRD/phase_01/PRD_phase_01.md`, `git status --short`)
- [x] T002 [S0106] Create or refresh an explicit smoke virtualenv and install dev plus visual extras (`.venv`, `python -m pip install -e ".[dev,visual]"`)
- [x] T003 [S0106] Verify local provider and Codex prerequisites or record provider substitution evidence (`scripts/check-ollama.sh`, `codex exec --help`)
- [x] T004 [S0106] Prepare isolated smoke artifact paths and temporary home directories (`/tmp/apex-infinite-cli-smoke-*`, `/tmp/apex-infinite-smoke-*.jsonl`)

## Foundation (5 tasks)

- [x] T005 [S0106] [P] Add stale virtualenv diagnosis and explicit repository venv remediation guidance (`docs/troubleshooting.md`)
- [x] T006 [S0106] [P] Add repeatable local release smoke procedure with temp artifacts and provider substitution handling (`docs/operator-runbook.md`)
- [x] T007 [S0106] [P] Update concise release smoke setup and quality command guidance (`README.md`)
- [x] T008 [S0106] [P] Sync Phase 01 blocker status or final smoke evidence link in the productization plan (`docs/ongoing-projects/terminal-and-linux-app-productization-plan.md`)
- [x] T009 [S0106] Record Phase 01 smoke remediation and final verification note under Unreleased (`CHANGELOG.md`)

## Testing (9 tasks)

- [x] T010 [S0106] Run the full pytest suite from the selected smoke Python (`python -m pytest tests/ -v`)
- [x] T011 [S0106] Run formatter, type checker, and linter checks (`python -m black --check src tests`, `python -m mypy`, `python -m pylint src tests`)
- [x] T012 [S0106] Run dependency audit and package build with temporary output (`python -m pip_audit`, `python -m build --outdir /tmp/apex-infinite-cli-smoke-dist`)
- [x] T013 [S0106] Run provider model preflight, provider chat preflight, and Ollama helper or documented substitute (`apex-infinite --check-provider`, `scripts/check-ollama.sh --chat`)
- [x] T014 [S0106] Run dry-run loop with file event stream and verify no provider event-stream contract errors (`/tmp/apex-infinite-smoke-events.jsonl`)
- [x] T015 [S0106] Run machine-output JSONL loop and verify stdout is JSONL-only (`apex-infinite --event-stream - --machine-output`)
- [x] T016 [S0106] Run history display verification for trailing-slash and no-slash scoped paths (`apex-infinite --history --path /home/aiwithapex/projects/apex-infinite-cli`)
- [x] T017 [S0106] Run visual wrapper fixture and CLI launch offscreen smokes (`QT_QPA_PLATFORM=offscreen apex-infinite-visual`)
- [x] T018 [S0106] Run actual nested Codex subprocess smoke with a no-edit prompt and verify worktree cleanliness (`git status --short`, `/tmp/apex-infinite-smoke-real-codex-events.jsonl`)

## Completion (2 tasks)

- [x] T019 [S0106] Update final smoke matrix, remediation status, command evidence, and provider substitution notes (`.spec_system/PRD/phase_01/platform_smoke_run_report_2026_07_03.md`)
- [x] T020 [S0106] Validate ASCII and LF requirements and record implementation evidence (`.spec_system/specs/phase01-session06-documentation-and-release-verification/implementation-notes.md`)

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
