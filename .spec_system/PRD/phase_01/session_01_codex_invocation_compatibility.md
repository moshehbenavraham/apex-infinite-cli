# Session 01: Codex Invocation Compatibility

**Session ID**: `phase01-session01-codex-invocation-compatibility`
**Status**: Not Started
**Estimated Tasks**: ~12-25
**Estimated Duration**: 2-4 hours

---

## Objective

Make default non-dry-run Codex subprocess execution work with the installed Codex CLI and fail early when configured flags are stale.

---

## Scope

### In Scope (MVP)

- Update packaged `codex.exec_flags` defaults in `src/apex_infinite/config.yaml`.
- Update runtime fallback defaults in `src/apex_infinite/cli.py`.
- Update README examples that still reference the rejected Codex flag.
- Add a startup compatibility check or non-mutating subprocess smoke fixture for `codex exec` flags.
- Document the selected operator policy for the supported Codex execution flag.
- Preserve existing prompt routing, history storage, and subprocess capture semantics.

### Out of Scope

- Broader autonomous execution safety UX beyond the flag compatibility and policy text needed for this finding.
- `exec_flags` tokenization hardening and reasoning-effort semantics, which are covered by Session 05.
- Full release verification, which is covered by Session 06.

---

## Prerequisites

- [ ] Phase 01 PRD exists and state tracking points at Phase 01.
- [ ] Installed Codex CLI behavior is checked against `codex exec --help`.

---

## Deliverables

1. Supported default Codex invocation config.
2. Runtime fallback and README examples aligned with the supported Codex CLI flag.
3. Compatibility check or non-mutating subprocess smoke coverage for stale flags.
4. Operator-facing policy text for real non-dry-run execution.

---

## Success Criteria

- [ ] The default actual nested Codex subprocess smoke no longer fails with `unexpected argument '--dangerously-auto-approve'`.
- [ ] Tests or smoke fixtures fail when configured Codex flags are not accepted by `codex exec`.
- [ ] README and packaged defaults no longer mention `--dangerously-auto-approve`.
- [ ] No provider secrets, Rich markup, or ANSI escapes are added to durable history or event payloads.
