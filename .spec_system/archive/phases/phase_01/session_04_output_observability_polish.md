# Session 04: Output Observability Polish

**Session ID**: `phase01-session04-output-observability-polish`
**Status**: Not Started
**Estimated Tasks**: ~12-25
**Estimated Duration**: 2-4 hours

---

## Objective

Remove confusing plain-output labels and make response summary previews useful or explicitly contracted as redacted.

---

## Scope

### In Scope (MVP)

- Change generic plain status block labels from internal severity names such as `ACCENT` to a user-facing label such as `STATUS`.
- Add provider preflight plain, ASCII, and compact renderer coverage.
- Decide whether `response_summarized.preview` should contain a short preview or be documented as intentionally suppressed.
- If previews are intended, replace `summarize_text(..., limit=0)` with a small nonzero limit for dry-run and real Codex response events.
- Add event payload tests for short harmless responses.
- Keep previews and labels out of SQLite history unless they are already part of raw agent output.

### Out of Scope

- New theme presets or wrapper visual design.
- Broad renderer refactors not required for the label and preview findings.
- Privacy features beyond the explicit preview contract decision.

---

## Prerequisites

- [ ] Session 02 is complete so provider preflight event tests are stable.
- [ ] Renderer snapshot and event payload test patterns are identified.

---

## Deliverables

1. Plain output that does not expose internal theme or severity tokens.
2. Tested response summary event behavior that matches its field name or documented redaction contract.
3. Renderer tests for provider preflight plain-mode output.

---

## Success Criteria

- [ ] Provider preflight plain output no longer prints `ACCENT Provider Preflight`.
- [ ] A short response such as `APEX_INFINITE_SUBPROCESS_SMOKE_OK` produces a useful preview, or the code/docs clearly define preview suppression.
- [ ] Event and history payloads remain free of Rich markup, ANSI escapes, and frame glyphs.
