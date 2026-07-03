# Session 06: Documentation And Release Verification

**Session ID**: `phase01-session06-documentation-and-release-verification`
**Status**: Not Started
**Estimated Tasks**: ~12-25
**Estimated Duration**: 2-4 hours

---

## Objective

Capture environment guidance and rerun the full release smoke suite after the functional fixes land.

---

## Scope

### In Scope (MVP)

- Add local development troubleshooting guidance for stale activated virtualenvs where `python` points outside the repository.
- Recommend creating and invoking an explicit repository virtualenv for smoke runs.
- Rerun pytest, black, mypy, pylint, pip-audit, and package build.
- Rerun provider preflight, provider chat preflight, dry-run loop, machine-output JSONL loop, history display, visual wrapper fixture mode, visual wrapper CLI launch mode, and actual nested Codex subprocess smoke.
- Update the smoke report or release notes with final verification results.
- Record any provider substitution if local Ollama is unavailable.

### Out of Scope

- Docker-based Ollama deployment from scratch.
- Nuitka binary packaging for the visual wrapper.
- New product features beyond smoke remediation verification.

---

## Prerequisites

- [ ] Sessions 01 through 05 are complete.
- [ ] Local provider availability is confirmed or an equivalent verification provider is selected.
- [ ] Release smoke commands and temporary artifact paths are prepared.

---

## Deliverables

1. Developer documentation for reliable local smoke setup.
2. Final quality and smoke verification evidence.
3. Updated smoke report or release note entry showing remediated findings.

---

## Success Criteria

- [ ] The quality suite remains green after the fixes.
- [ ] The actual nested Codex subprocess smoke passes with the shipped default or documented required config.
- [ ] Provider preflight and machine-output JSONL runs have no provider event-stream contract errors.
- [ ] The smoke report records no remaining release-blocking failures from the Phase 01 findings.
