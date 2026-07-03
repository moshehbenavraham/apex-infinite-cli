# Session Specification

**Session ID**: `phase01-session03-history-path-normalization`
**Phase**: 01 - Smoke Remediation And Release Hardening
**Status**: Not Started
**Created**: 2026-07-03
**Base Commit**: f44d51ba11131f2fab0ccf6d5634e4cdf2518b55

---

## 1. Session Overview

This session makes scoped history reads use the same normalized project path key
as normal run logging. The current CLI normalizes run-mode `--path` after the
history-mode early return, while `db_show_history()` and `db_fetch_history()`
query the exact supplied string. As a result, rows logged under a normalized
trailing-slash key can be missed when the operator queries the same directory
without the trailing slash.

The session is next because Phase 01 Sessions 01 and 02 are complete and the
phase PRD names history lookup normalization as the next smoke remediation
theme. The work is intentionally narrow: preserve the SQLite schema and raw row
contents, centralize path-key normalization, add trailing-slash regression
coverage, and update history docs that describe lookup behavior.

---

## 2. Objectives

1. Add one shared project-path normalization helper for SQLite history keys.
2. Use the helper before scoped history reads and normal run history writes.
3. Add regressions proving trailing-slash and no-trailing-slash path forms find
   the same scoped history rows.
4. Update active history documentation so examples and troubleshooting match
   normalized lookup behavior.

---

## 3. Prerequisites

### Required Sessions

- [x] `phase00-session03-subprocess-and-history-visibility` - Created the
  current history rendering and DB display behavior.
- [x] `phase00-session08-release-verification` - Produced the smoke report that
  identified the history lookup issue.
- [x] `phase01-session01-codex-invocation-compatibility` - Stabilized startup
  and command construction before later release-hardening work.
- [x] `phase01-session02-provider-event-stream-contract` - Stabilized provider
  event streams so this session can focus on history behavior.

### Required Tools Or Knowledge

- Current path validation and normalization code in `src/apex_infinite/cli.py`.
- Current SQLite helpers: `db_init()`, `db_fetch_history()`, `db_log()`, and
  `db_show_history()`.
- Existing Click test fixtures in `tests/test_cli_options.py`.
- Existing temporary DB patch strategy in `tests/test_history_rendering.py`.

### Environment Requirements

- Repository root: `/home/aiwithapex/projects/apex-infinite-cli`.
- Python test environment with pytest available.
- Tests must use temporary project directories and monkeypatched DB paths.

---

## 4. Scope

### In Scope (MVP)

- Operator can query `--history --path /path/to/project` and find rows logged
  under `/path/to/project/`.
- Operator can query `--history --path /path/to/project/` and preserve current
  behavior for already-normalized history rows.
- Normal workflow iterations continue to read and write history with the same
  normalized path key.
- Maintainer can test history path-key behavior without a real provider or
  Codex subprocess.
- Documentation states that trailing slash differences collapse to the same
  history key while symlinked or otherwise different absolute paths do not.

### Out Of Scope (Deferred)

- History retention, purge, or redaction controls - Reason: these remain open
  privacy/security findings outside the smoke-remediation objective.
- SQLite schema migration - Reason: existing `history` rows and the legacy
  `cc_response` column must stay readable as-is.
- Symlink canonicalization or realpath migration - Reason: current docs and
  conventions intentionally avoid treating all equivalent filesystem paths as
  one project identity.
- History display redesign - Reason: Session 04 owns output observability
  polish; this session fixes lookup correctness.
- Prompt routing, provider preflight, or Codex invocation changes - Reason:
  those boundaries are owned by other Phase 01 sessions.

---

## 5. Technical Approach

### Architecture

Add a small helper in `src/apex_infinite/cli.py` that expands `~`, verifies the
directory exists where user-facing CLI paths require that check, strips trailing
slashes, and appends exactly one trailing slash. Replace the inline run-mode
normalization in `main()` with the helper and apply the same helper before
scoped `db_fetch_history()` and `db_show_history()` queries. Global
`--history` without a path should remain unfiltered.

Keep the DB schema unchanged and continue using parameterized SQLite queries.
The helper belongs in `cli.py` for this session because the file already owns
Click path handling, DB helpers, and loop history access; extracting a new DB or
path module would add more surface than this smoke fix requires.

### Design Patterns

- Single path-key helper: removes drift between run mode, history mode, and DB
  helper call sites.
- Boundary validation: validates operator-supplied paths before querying or
  logging scoped history.
- Parameterized queries: preserves current SQLite injection resistance.
- Temp DB regression tests: proves behavior with real SQLite rows without
  touching the operator's `~/.apex-infinite/history.db`.

---

## 6. Deliverables

### Files To Create

| File | Purpose | Est. Lines |
|------|---------|------------|
| None | No new runtime or test files are expected; this session modifies existing code, tests, and docs. | 0 |

### Files To Modify

| File | Changes | Est. Lines |
|------|---------|------------|
| `src/apex_infinite/cli.py` | Add shared project-path history-key normalization and use it for run mode plus scoped history reads/writes. | ~45 |
| `tests/test_cli_options.py` | Update history-mode Click coverage and add helper/path normalization assertions. | ~55 |
| `tests/test_history_rendering.py` | Add SQLite regressions for trailing-slash and no-trailing-slash history lookups with temporary DB paths. | ~70 |
| `docs/history-db.md` | Clarify that scoped reads and writes use the normalized trailing-slash history key. | ~15 |
| `docs/operator-runbook.md` | Update history inspection and resume guidance for trailing-slash tolerant lookups. | ~10 |
| `docs/troubleshooting.md` | Replace stale exact-key troubleshooting language with normalized trailing-slash guidance. | ~15 |

---

## 7. Success Criteria

### Functional Requirements

- [ ] `db_fetch_history()` finds rows for the same existing directory whether
  the scoped path is supplied with or without a trailing slash.
- [ ] `db_show_history()` finds rows for the same existing directory whether
  the scoped path is supplied with or without a trailing slash.
- [ ] `apex-infinite --history --path /home/aiwithapex/projects/apex-infinite-cli`
  queries the same normalized key as
  `/home/aiwithapex/projects/apex-infinite-cli/`.
- [ ] Normal run-mode history reads and `db_log()` writes keep using the same
  normalized key shape.
- [ ] Unscoped `apex-infinite --history` remains a global history view.
- [ ] No SQLite schema migration is required and the legacy `cc_response`
  column remains unchanged.

### Testing Requirements

- [ ] Helper-level coverage proves `~` expansion, existing-directory
  validation, trailing-slash stripping, and single trailing-slash output.
- [ ] Click coverage proves history mode passes a normalized path into
  `db_show_history()` and does not start the loop.
- [ ] SQLite regression coverage proves trailing-slash and no-trailing-slash
  query forms find the same row.
- [ ] Storage safety coverage proves raw history rows do not gain display-only
  labels, ANSI escapes, Rich markup, frame glyphs, or schema changes.

### Non-Functional Requirements

- [ ] SQLite queries remain parameterized.
- [ ] Lookup normalization does not canonicalize symlinks or migrate stored
  paths.
- [ ] Path errors stay clear and mapped to the existing startup/history CLI
  failure style.
- [ ] Tests avoid live providers, real Codex subprocesses, and the operator's
  real history database.

### Quality Gates

- [ ] All files ASCII-encoded.
- [ ] Unix LF line endings.
- [ ] Code follows project conventions.
- [ ] `python -m pytest tests/test_cli_options.py tests/test_history_rendering.py -v` passes.
- [ ] `python -m pytest tests/ -v` passes or any unrelated pre-existing failures are documented.
- [ ] `python -m black --check src tests` passes.

---

## 8. Implementation Notes

### Working Assumptions

- The shared helper should stay in `src/apex_infinite/cli.py` for this session.
  Evidence: conventions say to extract helpers only when a split lowers risk,
  and the current path handling, DB helper calls, and Click startup flow all
  already live in this module. Planning can proceed because a local helper fixes
  the drift without broad module movement.
- Existing temporary DB tests are the right regression strategy. Evidence:
  `tests/test_cli_options.py` and `tests/test_history_rendering.py` already
  monkeypatch `DB_DIR` and `DB_PATH` and create temporary project directories.
  Planning can proceed without a real provider, real Codex subprocess, or real
  operator history.
- Documentation updates should focus on active history docs, not archived smoke
  or planning documents. Evidence: `docs/history-db.md`,
  `docs/operator-runbook.md`, and `docs/troubleshooting.md` are the user-facing
  contract surfaces for history lookup behavior. Planning can proceed without
  rewriting archived or ongoing planning notes.

### Conflict Resolutions

- `docs/history-db.md` already says writes normalize trailing slashes, while
  Phase 01 Session 03 says reads currently do not use the same normalization.
  The chosen interpretation is to preserve the documented write key and extend
  scoped reads to use that same key.
- `docs/troubleshooting.md` currently advises that `--history --path` can miss
  rows because the exact normalized string differs. The chosen interpretation is
  to make trailing-slash differences non-issues while preserving the existing
  warning that symlinked or otherwise different absolute paths remain distinct.

### Key Considerations

- Preserve existing `~/.apex-infinite/history.db` readability.
- Preserve the legacy `cc_response` column and avoid all schema migrations.
- Keep history rows raw; display labels and summaries remain renderer-only.
- Avoid prompt, provider, event-stream, subprocess, and renderer changes except
  where tests require path lookup assertions.
- Do not use this session to address retention, purge, redaction, or provider
  transfer disclosure findings.

### Potential Challenges

- Validating a path inside low-level DB helpers could surprise direct tests:
  use temporary existing directories and keep errors explicit.
- Global `--history` must not accidentally become scoped or require a project
  path: keep `path=None` as a separate branch.
- Docs must not imply all filesystem aliases collapse: state that trailing slash
  forms match, while symlink and alternate absolute paths remain distinct.

### Relevant Considerations

- [P00] **History compatibility**: Preserve legacy history schema, normalized
  project path keys, and the `cc_response` column.
- [P00] **Raw durable facts only**: Do not persist Rich markup, ANSI escapes,
  display labels, truncation text, or frame glyphs.
- [P00] **History retention gap**: Do not add purge, retention, or redaction in
  this smoke-fix session; record it as deferred.
- [P00] **SQLite**: Use temporary DB paths or monkeypatched `DB_DIR` and
  `DB_PATH` in tests, and cover sparse legacy rows when relevant.
- [P00] **Prompt contract coupling**: Do not edit manager or summarizer prompt
  behavior for a history lookup fix.

### Behavioral Quality Focus

Checklist active: Yes

Top behavioral risks for this session:

- Scoped history reads still miss valid rows because only one call site is
  normalized.
- User-supplied history paths produce unclear errors or accidentally query a
  different project key.
- DB helper tests touch the real operator history database instead of isolated
  temporary paths.

---

## 9. Testing Strategy

### Unit Tests

- Test the path-key helper with an existing temp directory, both trailing-slash
  forms, and an expanded path form where practical.
- Test invalid path behavior maps to the same error style as existing startup
  path validation.

### Integration Tests

- Use `CliRunner` to run `--history --path <project-without-slash>` with a
  patched `db_show_history()` and assert the normalized trailing-slash path is
  passed.
- Use temporary SQLite DB paths to log a row and query it with the opposite
  trailing-slash shape through `db_fetch_history()`.
- Use a recorded renderer and temporary SQLite DB to prove `db_show_history()`
  renders the row when queried with the opposite trailing-slash shape.
- Confirm unscoped `--history` still calls `db_show_history(None, ...)`.

### Runtime Verification

- Run focused tests:
  `python -m pytest tests/test_cli_options.py tests/test_history_rendering.py -v`.
- Run full project tests: `python -m pytest tests/ -v`.
- Run formatter check: `python -m black --check src tests`.

### Edge Cases

- Query path without trailing slash for a row logged under a trailing-slash key.
- Query path with trailing slash for a row logged after no-trailing-slash input.
- Empty/global history mode without `--path`.
- Missing project path passed to scoped history mode.
- Existing normalized history rows with the legacy `cc_response` column.

---

## 10. Dependencies

### Other Sessions

- Depends on: `phase01-session01-codex-invocation-compatibility`,
  `phase01-session02-provider-event-stream-contract`
- Depended by: `phase01-session04-output-observability-polish`,
  `phase01-session05-agent-config-semantics`,
  `phase01-session06-documentation-and-release-verification`

---

## Next Steps

Run the `implement` workflow step to begin implementation.
