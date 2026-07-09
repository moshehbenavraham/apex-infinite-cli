# Code Review and Repair Report

**Session ID**: `phase01-session04-output-observability-polish`
**Reviewed**: 2026-07-03
**Base Commit**: 7d67d7a78274f951de73575308a2163d1853244d
**Scope**: All changes since the base commit (uncommitted work plus mid-session commits)
**Result**: RESOLVED

## Review Surface

**Files reviewed** (all changes since the base commit):
- `.spec_system/state.json` - tracked-modified
- `docs/event-stream.md` - tracked-modified
- `docs/transcripts/machine-output-events.jsonl` - tracked-modified
- `src/apex_infinite/cli.py` - tracked-modified
- `src/apex_infinite/events.py` - tracked-modified
- `src/apex_infinite/ui.py` - tracked-modified
- `tests/test_cli_options.py` - tracked-modified
- `tests/test_event_stream.py` - tracked-modified
- `tests/test_renderer.py` - tracked-modified
- `tests/test_subprocess_execution.py` - tracked-modified
- `.spec_system/specs/phase01-session04-output-observability-polish/spec.md` - untracked session artifact
- `.spec_system/specs/phase01-session04-output-observability-polish/tasks.md` - untracked session artifact
- `.spec_system/specs/phase01-session04-output-observability-polish/implementation-notes.md` - untracked session artifact
- `.spec_system/specs/phase01-session04-output-observability-polish/code-review.md` - untracked creview report artifact, final self-check only

**Inventory commands**: `git status`, `git log --oneline "$BASE"..HEAD`, `git diff "$BASE"`, `git diff --cached "$BASE"`, `git ls-files --others --exclude-standard`

No mid-session commits were present. `git diff --cached "$BASE"` was empty.

## Findings by Severity

### Critical

None.

### High

None.

### Medium

- `src/apex_infinite/events.py:226` - Response preview safety was checked after truncation, so a secret-like value beginning near the preview boundary could be shortened into a non-matching fragment such as `sk-123456...` and emitted with `preview_suppressed: false`. This violated the session's safety-before-observability contract for response previews. | Fix: validate the normalized response candidate before applying the preview limit, suppressing unsafe response text before any truncation can hide the validator match. Added `tests/test_event_stream.py:321` to cover a secret crossing the preview boundary through the real `EventEmitter`. | Status: FIXED

### Low

- `src/apex_infinite/ui.py:1089` - The changed semantic label resolver tripped the configured pylint `too-many-return-statements` rule. | Fix: kept the same severity/title label precedence but rewrote `_label_for_title()` to use a severity mapping plus one final title-label fallback. | Status: FIXED

## Assumptions and Deliberate Non-Fixes

- The untracked `spec.md`, `tasks.md`, and `implementation-notes.md` files are expected session artifacts. Evidence: `bash .spec_system/scripts/analyze-project.sh --json` resolved `current_session` to `phase01-session04-output-observability-polish`, and the task checklist marks implementation complete and ready for `creview`.
- No unrelated source defects outside the diff surface were investigated or changed. Context from unchanged renderer, event, CLI, visual-wrapper, and test files was read only to judge the changed behavior.
- No deliberate non-fixes remain.

## Behavior Changes

- Unsafe response text is now suppressed before truncation. Observable event behavior changes only for output whose normalized response contains unsafe strings that could otherwise be partially exposed at the preview boundary. Safe short previews, long safe truncation, provider preflight labels, history storage, prompt routing, and subprocess return values remain unchanged.

## Evidence Ledger

Every row names the exact command or targeted inspection used.

| Check | Command or Inspection | Result | Evidence / Blocker |
|-------|-----------------------|--------|--------------------|
| Project state | `bash .spec_system/scripts/analyze-project.sh --json` | PASS | Current session resolved to `phase01-session04-output-observability-polish`; monorepo false. |
| Base resolution | `sed -n 's/^\*\*Base Commit\*\*: *//p' .spec_system/specs/phase01-session04-output-observability-polish/spec.md` plus `git rev-parse --verify --quiet "${BASE}^{commit}"` | PASS | Base commit resolved to `7d67d7a78274f951de73575308a2163d1853244d`. |
| Inventory | `git status`, `git log --oneline "$BASE"..HEAD`, `git diff --name-status "$BASE"`, `git diff --cached "$BASE"`, `git ls-files --others --exclude-standard` | PASS | Ten tracked modified files, three initial untracked session files, no mid-session commits, no staged diff. |
| Finding repro/fix | `PATH="$PWD/.venv/bin:$PATH" python - <<'PY' ... summarize_text(('x' * 110) + ' sk-...', limit=120) ... PY` | PASS | After fix: `preview` is empty and `preview_suppressed` is true. |
| Focused tests | `PATH="$PWD/.venv/bin:$PATH" python -m pytest tests/test_event_stream.py tests/test_subprocess_execution.py -v` | PASS | 53 passed; includes unsafe preview suppression and subprocess summary paths. |
| Renderer/event regression | `PATH="$PWD/.venv/bin:$PATH" python -m pytest tests/test_renderer.py tests/test_event_stream.py -v` | PASS | 44 passed after the label resolver lint reshaping. |
| Full tests | `PATH="$PWD/.venv/bin:$PATH" python -m pytest tests/ -v` | PASS | 274 passed in 11.72s. |
| Linter | `PATH="$PWD/.venv/bin:$PATH" python -m pylint src` | PASS | Rated 10.00/10 after fixing the resolver return-count issue. |
| Formatter | `PATH="$PWD/.venv/bin:$PATH" python -m black --check src tests` | PASS | 25 files would be left unchanged. |
| Type checker | `PATH="$PWD/.venv/bin:$PATH" python -m mypy` | PASS | No issues found in 11 source files. |
| ASCII/LF | `LC_ALL=C grep -nP '[^\x00-\x7F]' [changed files] || true` and `LC_ALL=C grep -nP '\r' [changed files] || true` | PASS | No matches in changed source, docs, tests, transcript, state, and session artifacts. |
| Final diff re-read | `git diff "$BASE"` plus `git ls-files --others --exclude-standard` | PASS | Re-read tracked diff and untracked session artifacts; no remaining review findings. |

## Summary

1. Reviewed 13 implementation/session files plus this report artifact across renderer labels, CLI response summary emitters, event payload validation, tests, docs, transcript samples, and session state.
2. Findings: 0 Critical, 0 High, 1 Medium, 1 Low; all resolved with focused code/test changes.
3. No deliberate non-fixes remain. The only assumption is that the untracked session files are expected Apex Spec session artifacts, supported by project-state analysis.
4. Evidence: focused tests, full tests, black, pylint, mypy, ASCII/LF checks, and final diff re-read all passed.
