# Session Specification

**Session ID**: `phase01-session04-output-observability-polish`
**Phase**: 01 - Smoke Remediation And Release Hardening
**Status**: Not Started
**Created**: 2026-07-03
**Base Commit**: 7d67d7a78274f951de73575308a2163d1853244d

---

## 1. Session Overview

This session removes two low-severity smoke-run observability defects from the
operator and event-stream surfaces. Plain provider preflight output currently
falls back to the internal severity token `ACCENT`, and response summary events
currently emit `preview: "..."` for every Codex response because call sites pass
`limit=0` into `summarize_text()`.

The session is next because Phase 01 Sessions 01 through 03 are complete, and
Session 04 depends on the provider event-stream contract stabilized in Session
02. The work is intentionally narrow: add a stable user-facing status label for
generic plain output, make response summaries useful for harmless short output,
document the preview contract, and preserve the rule that SQLite history and
JSONL events do not contain Rich markup, ANSI escapes, frame glyphs, visual
tokens, or secrets.

---

## 2. Objectives

1. Replace generic plain-output severity leakage with a stable operator-facing
   status label.
2. Make `response_summarized.preview` useful for harmless short dry-run and
   Codex outputs.
3. Preserve event payload safety by bounding previews and suppressing unsafe
   preview text without failing the event stream.
4. Update focused renderer, event, subprocess, CLI, and documentation coverage
   for the chosen output contract.

---

## 3. Prerequisites

### Required Sessions

- [x] `phase00-session02-rich-operator-console` - Created the current renderer
  facade and plain/ascii/compact output behavior.
- [x] `phase00-session04-event-stream-boundary` - Created the JSONL event
  emitter and response summary event surface.
- [x] `phase01-session01-codex-invocation-compatibility` - Stabilized default
  Codex command construction before later response-summary work.
- [x] `phase01-session02-provider-event-stream-contract` - Registered provider
  preflight event names and added provider event regression coverage.
- [x] `phase01-session03-history-path-normalization` - Completed the preceding
  release-hardening session and preserved raw history behavior.

### Required Tools Or Knowledge

- Current renderer label flow in `src/apex_infinite/ui.py`.
- Current event validation and summary helper behavior in
  `src/apex_infinite/events.py`.
- Current Codex execution response event call sites in
  `src/apex_infinite/cli.py`.
- Existing renderer, provider preflight, event-stream, and subprocess tests in
  `tests/`.

### Environment Requirements

- Repository root: `/home/aiwithapex/projects/apex-infinite-cli`.
- Python test environment with pytest available.
- Tests must avoid live provider calls and real Codex subprocesses by using the
  existing monkeypatch and fake-emitter fixtures.

---

## 4. Scope

### In Scope (MVP)

- Operator can run provider preflight in plain/ascii/compact modes without
  seeing internal labels such as `ACCENT`.
- Operator-facing generic status blocks use stable product labels such as
  `STATUS` while critical states keep their existing semantic labels.
- Event-stream consumers receive a bounded useful
  `response_summarized.preview` for short harmless dry-run and Codex outputs.
- Event-stream consumers receive a clear suppressed-preview contract when a
  response preview would violate payload safety rules.
- Maintainers can verify that response preview changes do not write styled
  output, display-only labels, or preview text into SQLite history rows.
- Documentation and deterministic JSONL transcript samples describe the
  implemented preview behavior.

### Out Of Scope (Deferred)

- New theme presets or wrapper visual redesign - Reason: this session polishes
  existing product surfaces only.
- Broad renderer refactors - Reason: the smoke finding is label fallback
  behavior, not renderer architecture.
- Full privacy redaction, retention, or purge controls - Reason: those remain
  open security/compliance findings beyond this release-hardening slice.
- Codex `exec_flags` parsing or `model_reasoning_effort` semantics - Reason:
  Session 05 owns agent configuration semantics.
- SQLite schema changes - Reason: history compatibility and raw durable facts
  must remain unchanged.

---

## 5. Technical Approach

### Architecture

Add a generic semantic status label in `src/apex_infinite/ui.py` and route
plain generic status blocks through it instead of falling back to
`severity.upper()`. This can be done by adding `STATUS` to the semantic label
set and mapping generic status titles, including provider preflight, to that
label while leaving error, warning, success, history, decision, prompt, and
Codex-specific labels untouched.

For response summary events, keep the summary data in the event boundary rather
than the renderer. Update `summarize_text()` or a small helper near it so
bounded previews remain safe for JSONL payload validation. The implementation
should emit useful previews for harmless text such as
`APEX_INFINITE_SUBPROCESS_SMOKE_OK`, but suppress or replace unsafe preview
strings that contain ANSI escapes, Rich markup, frame glyphs, visual tokens, or
secret-like values. Then replace the `limit=0` response summary call sites in
`src/apex_infinite/cli.py` with one small nonzero response-preview limit.

### Design Patterns

- Semantic label vocabulary: product-facing labels come from one renderer
  mapping instead of internal style names.
- Bounded event preview: response summaries expose concise raw facts without
  dumping full agent output.
- Safety-before-observability: unsafe preview text is explicitly suppressed
  rather than causing `event_stream_error` or leaking secrets.
- Focused regression coverage: tests target label semantics, event payloads,
  and fake subprocess outputs without live providers or real Codex execution.

---

## 6. Deliverables

### Files To Create

| File | Purpose | Est. Lines |
|------|---------|------------|
| None | No new runtime or test files are expected; this session modifies existing code, tests, docs, and transcript fixtures. | 0 |

### Files To Modify

| File | Changes | Est. Lines |
|------|---------|------------|
| `src/apex_infinite/ui.py` | Add a generic `STATUS` semantic label and apply it to plain generic status output, including provider preflight. | ~25 |
| `src/apex_infinite/events.py` | Make response preview metadata bounded and safe when preview text would fail payload validation. | ~35 |
| `src/apex_infinite/cli.py` | Replace zero-length response summary preview limits with a small shared nonzero limit for dry-run, success, timeout, missing-binary, and error response summaries. | ~25 |
| `tests/test_renderer.py` | Add renderer-level coverage for generic status and provider preflight plain/ascii/compact labels without `ACCENT`. | ~45 |
| `tests/test_cli_options.py` | Extend provider preflight CLI coverage for plain/ascii/compact output and failure labels. | ~45 |
| `tests/test_subprocess_execution.py` | Add fake Codex response event assertions for harmless previews, bounded truncation, and error-path summaries. | ~60 |
| `tests/test_event_stream.py` | Add event-stream safety coverage proving unsafe previews are suppressed without `event_stream_error`. | ~45 |
| `docs/event-stream.md` | Document the bounded response preview contract and suppressed-preview behavior. | ~25 |
| `docs/transcripts/machine-output-events.jsonl` | Refresh deterministic sample output so `response_summarized.preview` is useful instead of always `...`. | ~5 |

---

## 7. Success Criteria

### Functional Requirements

- [ ] Plain provider preflight output no longer prints `ACCENT Provider Preflight`.
- [ ] Plain generic status output prints a stable user-facing label such as
  `STATUS`.
- [ ] ASCII and compact provider preflight output remains ASCII-only and keeps
  the same user-facing status label.
- [ ] A short harmless response such as `APEX_INFINITE_SUBPROCESS_SMOKE_OK`
  produces a useful `response_summarized.preview`.
- [ ] Dry-run response summaries produce a useful bounded preview instead of
  `...`.
- [ ] Unsafe response preview text is suppressed or replaced according to the
  documented contract without emitting `event_stream_error`.
- [ ] SQLite history rows remain raw workflow facts and do not gain preview
  text, renderer labels, ANSI escapes, Rich markup, frame glyphs, or visual
  tokens.

### Testing Requirements

- [ ] Renderer tests cover generic plain status labels and provider preflight
  labels at product-supported output modes.
- [ ] CLI tests cover successful and failed provider preflight plain output
  without internal severity labels.
- [ ] Subprocess tests cover dry-run, successful Codex output, non-zero exit,
  timeout, missing binary, and generic exception response summaries.
- [ ] Event-stream tests cover harmless short previews, bounded truncation, and
  unsafe preview suppression.
- [ ] Documentation and transcript fixture changes match the implemented event
  payload contract.

### Non-Functional Requirements

- [ ] Response previews are bounded to a small deterministic maximum.
- [ ] Event payload validation still rejects ANSI escapes, Rich markup, frame
  glyphs, visual tokens, and secret-like values.
- [ ] No provider secrets, API keys, or personal data examples are introduced
  into docs, tests, transcripts, history rows, or event fixtures.
- [ ] Machine-output JSONL remains machine-only and does not mix with human
  output.

### Quality Gates

- [ ] All files ASCII-encoded.
- [ ] Unix LF line endings.
- [ ] Code follows project conventions.
- [ ] Primary user-facing surfaces contain product-facing copy only.
- [ ] `python -m pytest tests/test_renderer.py tests/test_cli_options.py tests/test_subprocess_execution.py tests/test_event_stream.py -v` passes.
- [ ] `python -m pytest tests/ -v` passes or any unrelated pre-existing failures are documented.
- [ ] `python -m black --check src tests` passes.

---

## 8. Implementation Notes

### Working Assumptions

- Response previews should become useful bounded previews rather than remain
  intentionally redacted. Evidence: the event field is named `preview`, the
  Phase 01 smoke report recommends a small nonzero limit, and `PRD_UX.md`
  defines the event stream as a lifecycle-fact boundary for wrappers and tests.
  Planning can proceed because previews can be bounded, validated, documented,
  and kept out of SQLite history.
- Generic status labels should be solved in the renderer vocabulary, not by
  hard-coding provider preflight strings in CLI flow. Evidence:
  `print_status()` already routes human output through `ApexRenderer`, and the
  smoke finding points at `_print_plain_block()` falling back to
  `severity.upper()`. Planning can proceed because the change is display-only
  and does not affect manager prompts, event names, or storage.
- The active documentation surfaces for this contract are
  `docs/event-stream.md` and `docs/transcripts/machine-output-events.jsonl`.
  Evidence: `docs/event-stream.md` owns event names and payload examples, and
  the transcript fixture currently shows `response_summarized.preview` as
  `...`. Planning can proceed without rewriting archived smoke reports or broad
  README sections.

### Conflict Resolutions

- The Session 04 stub allows either useful previews or documented suppression.
  The chosen interpretation is useful bounded previews for safe text, with
  explicit suppression only when preview text violates event payload safety
  rules. This best matches the field name, smoke evidence, and wrapper/event
  observability goals while respecting security constraints.
- Privacy/security findings warn against leaking secrets, while the smoke report
  asks for better response observability. The chosen interpretation is to keep
  previews small, validated, and absent from SQLite, and to suppress unsafe
  preview text instead of disabling all preview usefulness.
- UI surface guidance bans implementation diagnostics in primary product
  surfaces, while provider preflight is operational telemetry. The chosen
  interpretation is that `STATUS Provider Preflight` is product-facing
  operator state, while renderer internals such as `ACCENT` remain banned from
  normal product output.

### Key Considerations

- Do not change prompt routing, manager prompt text, history schema, provider
  event names, machine-output isolation, or Codex command semantics.
- Keep response preview code close to the event payload boundary so future
  wrappers inherit the same safe contract.
- Debug surface required: none. Tests and transcript fixtures provide the
  diagnostic evidence for this session.

### Potential Challenges

- Unsafe preview strings can trip event validation once previews become
  non-empty. Mitigation: add explicit tests for unsafe preview suppression and
  avoid falling back to event-stream errors for expected unsafe content.
- Plain label changes can accidentally relabel critical errors as generic
  status. Mitigation: keep severity-specific mappings for error, warning,
  success, timeout, stop, and Codex states ahead of generic status fallback.
- Updating transcript fixtures can drift from runtime behavior. Mitigation:
  derive the sample from the same event contract and verify ASCII JSONL shape.

### Relevant Considerations

- [P00] **Raw durable facts only**: Response previews and status labels must not
  put Rich markup, ANSI escapes, frame glyphs, visual tokens, or secrets into
  SQLite history or JSONL events.
- [P00] **Machine-output isolation**: JSONL to stdout remains valid only under
  `--machine-output`; no human status labels can appear in machine stdout.
- [P00] **Semantic labels over color**: Use stable text labels such as
  `STATUS`, `ERROR`, and `STOP` instead of exposing style tokens.
- [P00] **JSONL events**: Event names and payloads remain importable,
  primitive, validated, and line-buffered.
- [P00] **Provider and Codex prerequisites**: Tests and docs must not print,
  store, or emit API keys or provider secrets.

### Behavioral Quality Focus

Checklist active: Yes
Top behavioral risks for this session:
- Plain product surfaces can expose internal renderer vocabulary instead of
  operator-facing labels.
- Event preview changes can leak unsafe response content or cause summary
  events to fail validation.
- Event-stream consumers and wrapper fixtures can drift if docs, transcripts,
  and runtime payloads do not move together.

---

## 9. Testing Strategy

### Unit Tests

- Renderer tests for `print_status()` and provider preflight label behavior in
  plain, ASCII, and compact output.
- Event helper tests for useful harmless previews, bounded truncation, empty
  output, and unsafe preview suppression.
- Subprocess execution tests for all `response_summarized` sources emitted by
  fake Codex success and failure paths.

### Integration Tests

- Click tests for `--check-provider --plain`, `--check-provider --ascii`,
  `--check-provider --compact`, and provider failure output.
- Event-stream dry-run tests that read JSONL rows and assert
  `response_summarized.preview` matches the documented bounded contract.

### Runtime Verification

- Run focused tests:
  `python -m pytest tests/test_renderer.py tests/test_cli_options.py tests/test_subprocess_execution.py tests/test_event_stream.py -v`.
- Run full regression suite: `python -m pytest tests/ -v`.
- Run formatter check: `python -m black --check src tests`.

### Edge Cases

- Empty response output keeps `has_output: false` and a non-misleading preview.
- Long response output is truncated deterministically.
- Response output containing ANSI escapes, Rich markup, frame glyphs, visual
  tokens, or secret-like values does not leak through `preview`.
- Provider preflight failures still show visible error text and do not downgrade
  to generic status labels.
- Machine-output mode does not print human labels to stdout.

---

## 10. Dependencies

### Other Sessions

- Depends on: `phase01-session02-provider-event-stream-contract`,
  `phase01-session03-history-path-normalization`.
- Depended by: `phase01-session06-documentation-and-release-verification`.

---

## Next Steps

Run the `implement` workflow step to begin implementation.
