# PRD Phase 01: Smoke Remediation And Release Hardening

**Status**: In Progress
**Sessions**: 6 (initial estimate)
**Estimated Duration**: 3-6 days

**Progress**: 4/6 sessions (67%)

---

## Overview

Phase 01 turns the 2026-07-03 platform smoke-run findings into a release-hardening track. The phase fixes the default Codex invocation failure, restores provider preflight event-stream contracts, normalizes history lookup paths, polishes operator-visible output, aligns agent configuration semantics with actual subprocess behavior, and reruns release verification with explicit local environment guidance.

The full source smoke report is preserved at
`.spec_system/PRD/phase_01/platform_smoke_run_report_2026_07_03.md`.

---

## Progress Tracker

| Session | Name | Status | Est. Tasks | Validated |
|---------|------|--------|------------|-----------|
| 01 | Codex Invocation Compatibility | Complete | ~12-25 | 2026-07-03 |
| 02 | Provider Event Stream Contract | Complete | ~12-25 | 2026-07-03 |
| 03 | History Path Normalization | Complete | ~12-25 | 2026-07-03 |
| 04 | Output Observability Polish | Complete | ~12-25 | 2026-07-03 |
| 05 | Agent Config Semantics | Not Started | ~12-25 | - |
| 06 | Documentation And Release Verification | Not Started | ~12-25 | - |

---

## Completed Sessions

- 2026-07-03 - Session 01: Codex Invocation Compatibility
- 2026-07-03 - Session 02: Provider Event Stream Contract
- 2026-07-03 - Session 03: History Path Normalization
- 2026-07-03 - Session 04: Output Observability Polish

---

## Upcoming Sessions

- Session 05: Agent Config Semantics
- Session 06: Documentation And Release Verification

---

## Objectives

1. Restore out-of-the-box non-dry-run Codex subprocess compatibility.
2. Make provider preflight events valid and reliable for file, stdout, machine-output, and wrapper consumers.
3. Remove path-shape surprises from history lookup behavior.
4. Improve plain-output and response-summary observability without polluting durable records.
5. Align Codex agent configuration parsing and documentation with actual command construction.
6. Document local smoke-run environment requirements and rerun release verification.

---

## Prerequisites

- Phase 00 completed.
- The smoke-run report exists at
  `.spec_system/PRD/phase_01/platform_smoke_run_report_2026_07_03.md`.
- Existing Phase 00 compatibility constraints remain in force: prompt routing, history schema, raw event payloads, and optional wrapper boundaries must not regress.

---

## Planning Assumptions And Resolutions

### Working Assumptions

- Phase 01 is the correct next phase: `analyze-project.sh --json` reports Phase 00 complete with no candidate sessions, and the supplied smoke-run report contains a six-session `Session Split Plan` plus release-blocking findings. The user invoked `phasebuild` with that report, so it is safe to use the report as the next phase source.
- The initial session count is six: the smoke-run split defines six implementation-oriented sessions that each have one objective and can be expanded into 12-25 tasks during `plansession`.
- Session 01 should run first: the default Codex exec flag blocks real non-dry-run operation and influences later agent config semantics.
- Session 06 should run last: final verification depends on the functional fixes from Sessions 01 through 05.
- Local Ollama remains the default verification provider unless plansession records an equivalent provider substitution.

### Conflict Resolutions

- Master PRD and state tracking previously indicated only completed Phase 00, while the smoke-run report records new release-hardening work. The chosen interpretation is that the master PRD and state were stale because the report was created after Phase 00 release verification. This phasebuild reconciles them by adding Phase 01 to the master PRD and advancing `current_phase` to 1.
- The smoke report calls the current Codex replacement flag dangerous while also recommending it as a compatibility fix. The chosen interpretation is to make Session 01 decide and document the supported operator policy, rather than hard-code the final safety posture in the phase stub.
- The smoke report includes one environment warning that is not a repository code bug. The chosen interpretation is to handle it in Session 06 documentation and verification, not as a standalone code-fix session.

---

## Technical Considerations

### Architecture

- Keep subprocess, provider preflight, event, renderer, history, and config changes focused and covered by Click or unit tests.
- Preserve the raw lifecycle event boundary for wrappers and automation.
- Keep durable SQLite rows and JSONL events free of Rich markup, ANSI escapes, frame glyphs, secrets, and display-only renderer text.
- Extract helpers from `src/apex_infinite/cli.py` only when the split reduces risk and has focused coverage.

### Technologies

- Python 3.10+
- Click
- Rich
- SQLite
- PyYAML and python-dotenv
- OpenAI-compatible provider client
- Codex CLI
- pytest, black, mypy, pylint, pip-audit, and build tooling
- Optional PySide6 visual wrapper smoke checks

### Risks

- Codex flag changes can widen autonomous execution permissions: mitigate with explicit docs, startup checks, and operator-facing policy text.
- Event-name changes can break wrapper or automation consumers: mitigate with schema tests and machine-output JSONL coverage.
- History path normalization can accidentally break existing databases: mitigate with tests for both trailing-slash and no-trailing-slash keys.
- Response previews can expose sensitive output: mitigate by deciding preview semantics explicitly and testing the chosen contract.
- Final verification can depend on local provider availability: mitigate by documenting provider substitution evidence when needed.

### Relevant Considerations

- [P00] **Autonomous execution controls**: Session 01 must make target path, provider, model, and execution flags explicit before real non-dry-run loops.
- [P00] **Provider and Codex prerequisites**: Sessions 01, 02, and 06 must avoid printing, storing, or emitting provider secrets.
- [P00] **History compatibility**: Session 03 must preserve the legacy history schema and normalized project path key behavior.
- [P00] **Raw durable facts only**: Sessions 02, 04, and 06 must keep durable event and history payloads free of display artifacts.
- [P00] **Machine-output isolation**: Session 02 must keep stdout JSONL isolated under `--machine-output`.
- [P00] **Event stream is the wrapper contract**: Session 02 changes must preserve wrapper-facing lifecycle event semantics.
- [P00] **Semantic labels over color**: Session 04 should use stable labels instead of internal color or severity tokens.
- [P00] **JSONL events**: Session 02 should keep event names importable and payload types validated.

---

## Success Criteria

Phase complete when:
- [ ] All 6 sessions completed
- [ ] Default or documented Codex subprocess invocation passes a non-mutating real smoke
- [ ] Provider preflight emits valid lifecycle events without event-stream errors
- [ ] History lookup works for equivalent trailing-slash and no-trailing-slash project paths
- [ ] Plain output no longer leaks internal labels such as `ACCENT`
- [ ] Agent config docs and behavior match actual command construction
- [ ] Final quality and smoke verification evidence is recorded

---

## Dependencies

### Depends On

- Phase 00: Apex Infinite CLI Upgrade

### Enables

- Release candidate cleanup after smoke-run remediation
- Future privacy, dependency governance, and broader autonomous execution-control phases
