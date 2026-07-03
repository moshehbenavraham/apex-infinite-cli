# Session 03: History Path Normalization

**Session ID**: `phase01-session03-history-path-normalization`
**Status**: Not Started
**Estimated Tasks**: ~12-25
**Estimated Duration**: 2-4 hours

---

## Objective

Make history lookups use the same normalized project path shape as normal run logging.

---

## Scope

### In Scope (MVP)

- Extract or reuse one project-path normalization helper in `src/apex_infinite/cli.py`.
- Apply the helper before history queries.
- Keep normal loop DB writes using the same normalized path behavior.
- Add Click tests that log with one trailing-slash shape and query with the other.
- Verify documented `--history --path` examples work with common shell-expanded paths.
- Preserve existing `~/.apex-infinite/history.db` readability and the legacy `cc_response` column.

### Out of Scope

- History retention, purge, or redaction controls.
- Database schema migration.
- History display redesign beyond path lookup correctness.

---

## Prerequisites

- [ ] Existing history tests and DB helpers are identified.
- [ ] Temporary DB path strategy is selected for regression tests.

---

## Deliverables

1. Shared path normalization behavior for run mode and history mode.
2. Regression coverage for trailing-slash and no-trailing-slash project paths.
3. Documentation check for history path examples.

---

## Success Criteria

- [ ] `apex-infinite --history --path /home/aiwithapex/projects/apex-infinite-cli` finds rows logged under `/home/aiwithapex/projects/apex-infinite-cli/`.
- [ ] Existing history queries continue to work for already-normalized paths.
- [ ] No SQLite schema migration is required.
- [ ] Raw history rows remain free of display-only formatting artifacts.
