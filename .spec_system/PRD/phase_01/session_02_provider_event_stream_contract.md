# Session 02: Provider Event Stream Contract

**Session ID**: `phase01-session02-provider-event-stream-contract`
**Status**: Not Started
**Estimated Tasks**: ~12-25
**Estimated Duration**: 2-4 hours

---

## Objective

Restore provider preflight lifecycle events as valid event-stream output for file, stdout, and machine-output consumers.

---

## Scope

### In Scope (MVP)

- Register `provider_check_started`, `provider_check_failed`, and `provider_check_finished` in the event schema, or rename provider preflight emits to existing approved event names.
- Add tests for `--check-provider --event-stream`.
- Add tests for startup provider preflight with file event streams.
- Add tests for startup provider preflight with `--event-stream - --machine-output`.
- Cover the provider failure path so failed preflight events are valid too.
- Preserve machine-output isolation and line-buffered JSONL behavior.

### Out of Scope

- Provider client redesign.
- Wrapper UI changes beyond preserving the event contract it consumes.
- Full provider matrix testing for OpenAI or Grok unless needed to prove the event contract.

---

## Prerequisites

- [ ] Session 01 is complete or confirmed not to affect provider preflight startup behavior.
- [ ] Existing event schema and emitter tests are identified.

---

## Deliverables

1. Event schema and provider preflight emitters with matching event names.
2. Regression tests for successful and failed provider preflight event output.
3. Machine-output JSONL coverage proving no human text is mixed into stdout.

---

## Success Criteria

- [ ] Provider preflight runs no longer emit `event_stream_error` rows for valid lifecycle events.
- [ ] Machine-output JSONL remains machine-only and includes valid provider preflight events.
- [ ] File event-stream mode persists provider preflight events instead of dropping them.
- [ ] Failure-path provider preflight events are accepted by the schema.
