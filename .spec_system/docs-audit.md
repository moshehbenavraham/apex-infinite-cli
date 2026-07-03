# Documentation Audit Report

**Date**: 2026-07-03
**Project**: Apex Infinite CLI
**Audit Mode**: Standalone repository link and reference cleanup

## Summary

| Category | Required | Found | Status |
|----------|----------|-------|--------|
| Root files | 5 | 5 | PASS |
| Package docs | 8 | 8 | PASS |
| Transcript fixtures | 3 | 3 | PASS |
| Spec-system docs | 5 | 5 | PASS |
| CI docs | 0 | 0 | N/A |

Root files are `README.md`, `CHANGELOG.md`, `LICENSE`, `pyproject.toml`, and
`.env.example`. Package docs are under `docs/`. The repository is a standalone
Python package and does not currently include CI workflows, ADRs, or the broader
Apex Spec System plugin source tree.

## Audit Scope

The repository was rearranged from a nested `./` subproject into
a standalone package. This audit checks that `.spec_system` references the
current root layout:

- Base CLI package: `src/apex_infinite/`
- Visual wrapper package: `src/apex_infinite_visual/`
- Tests: `tests/`
- Documentation: `README.md` and `docs/`
- Example reference tree: `EXAMPLE/cool-retro-term/`

## Current Documentation

| File | Purpose | Status |
|------|---------|--------|
| `README.md` | Primary install, configuration, usage, event stream, history, and wrapper guide | Current |
| `docs/event-stream.md` | JSONL event stream contract | Current |
| `docs/history-db.md` | SQLite history behavior and compatibility notes | Current |
| `docs/operator-runbook.md` | Operator workflows and run guidance | Current |
| `docs/prompt-contract.md` | Manager routing and prompt behavior | Current |
| `docs/troubleshooting.md` | CLI, provider, event-stream, and wrapper recovery notes | Current |
| `docs/visual-wrapper-boundary.md` | Clean-room and optional wrapper boundary | Current |
| `docs/visual-wrapper-productization.md` | Source-mode visual wrapper productization guide | Current |
| `docs/visual-wrapper-spike.md` | Visual wrapper spike record | Current |
| `docs/transcripts/README_transcripts.md` | Transcript fixture index | Current |

## Spec-System Files

| File | Purpose | Status |
|------|---------|--------|
| `.spec_system/PRD/PRD.md` | Product requirements | Updated for standalone repo |
| `.spec_system/PRD/PRD_UX.md` | UX requirements | Updated for packaged entrypoints |
| `.spec_system/CONVENTIONS.md` | Current implementation conventions | Updated for root paths |
| `.spec_system/CONSIDERATIONS.md` | Institutional memory | Updated for `src/` paths |
| `.spec_system/SECURITY-COMPLIANCE.md` | Security posture and open findings | Updated for root paths |

## Reference Fixes

| Previous Reference | Current Reference |
|--------------------|-------------------|
| `src/apex_infinite/cli.py` | `src/apex_infinite/cli.py` |
| `src/apex_infinite/ui.py` | `src/apex_infinite/ui.py` |
| `src/apex_infinite/events.py` | `src/apex_infinite/events.py` |
| `src/apex_infinite_visual/` | `src/apex_infinite_visual/` |
| `README.md` | `README.md` |
| `docs/` | `docs/` |
| `tests/` | `tests/` |
| Old parent-checkout `EXAMPLE/` links | `EXAMPLE/` |

## Remaining Notes

Archived Phase 00 session files are historical records. Their file and command
references have been normalized to current standalone paths where a current
equivalent exists, while preserving the session content and acceptance evidence.

No CI workflow documents are listed because this standalone copy has no workflow
directory. Until CI is added, release checks remain local:
`python -m pytest tests/ -v`, formatter/linter checks from `pyproject.toml`,
event-stream smoke checks, and optional wrapper smoke checks.
