# 0001. Release Scope Decisions For The Terminal And Visual Productization

**Status:** Accepted
**Date:** 2026-07-09

## Context

The 2026-07-09 audit tracker
(`docs/ongoing-projects/revolutionary-linux-terminal-remaining-work.md`)
lists open product decisions that block release-facing work. Each decision
below closes one tracker item. The base CLI must stay terminal-only, the
wrapper must stay event-driven, and all visual work must remain clean-room.

## Decisions

### 1. Command-strip resume is in scope, in its honest minimal form

The workflow engine already resumes naturally: history lives in SQLite and
the manager summarizes it on every run, so "resume" means re-launching the
CLI against the same project with the same controls. The wrapper therefore:

- persists the last run controls (project path, start command, max
  iterations, dry-run mode) in the wrapper-owned runtime state file
  (`${XDG_STATE_HOME:-~/.local/state}/apex-infinite/visual-state.json`),
- exposes a first-class `Resume` command-strip action that restores those
  controls and starts a run through the existing event-driven launcher.

No Rich/ANSI/SQLite scraping is added; resume state is wrapper presentation
state, not workflow state.

### 2. Shader mode is deferred for the source-mode visual release

Compiled `.qsb` modules stay ignored and out of package data. The shipped
visual path is QML-only source mode (Qt Quick effects layered in
`src/apex_infinite_visual/qml/effects/`). The clean-room shader sources in
`src/apex_infinite_visual/shaders/` remain in-tree for a future release but
are not wired into the render path. Release wording must state that
QML-only source mode is the shipped visual path.

### 3. The QML profile drawer gets full profile-operation parity

`ProfileStore` already implements save, load, delete, duplicate, rename,
reset-to-built-in, import, and export with schema validation and secret
rejection. The drawer exposes all of them; the bridge gains the two
missing slots (`renameProfile`, `resetProfile`). Validation errors surface
through the existing `profileError` UI text. Profile names remain
ASCII-only.

### 4. Workstream 8 terminal CLI polish is complete

The terminal renderer already ships status hierarchy, themes
(`crt-green`, `crt-amber`, `ibm-dos`, `plain`), progress summaries, the
autonomy summary, compact mode, plain/ASCII fallbacks, and machine-output
separation. No further polish is scoped for this release; remaining
terminal work is setup/doctor/config resolution (decisions 5-7).

### 5. The terminal doctor entrypoint is `apex-infinite --doctor`

The root command remains a single Click command; doctor is exposed as a
flag, like `--check-provider` and `--history`. If the CLI ever becomes a
Click group, `apex-infinite doctor` must alias the same backend.

### 6. Terminal and visual doctor share a diagnostic backend

The shared backend lives in the base package (`apex_infinite/doctor.py`):
check/report dataclasses plus display-agnostic checks (config, project,
Codex binary, history DB). The visual doctor imports those and adds
wrapper-only checks (PySide6, display). The base CLI never imports the
visual package.

### 7. Config-directory `.env` takes precedence over cwd `.env`

`load_config()` loads cwd `.env` first and then the config-directory
`.env` with `override=True`, so values stored beside the selected config
file win. This existing behavior is now the documented and tested
contract.

### 8. Broad Codex bypass ships as documented accepted risk

`codex.exec_flags` defaults stay unchanged
(`--dangerously-bypass-approvals-and-sandbox`) because the product is an
autonomous workflow runner. Mitigations that must stay in place:

- the autonomy summary is always visible before real runs (terminal and
  wrapper),
- onboarding and setup steer the first execution through `--dry-run`,
- the setup command prints an explicit autonomy warning before writing
  exec flags,
- `docs/SECURITY-COMPLIANCE.md` documents the accepted risk.

### 9. Package publishing and rollback remain external/manual

There is no automated publish pipeline. Publishing to an index and rolling
back a bad release are manual operator actions recorded in
`packaging/RELEASE-CHECKLIST.md`. Artifacts are versioned by
`pyproject.toml`; rollback is "publish the previous version / delete the
bad artifact where the channel allows it".

### 10. No `docs/CODEOWNERS` file is added

The repository has a single maintainer; ownership routing adds process
without value today. Revisit when a second regular contributor lands.

### 11. Full logging is the default for the visual wrapper's real CLI path

When the wrapper launches the real CLI, it tees the validated JSONL event
stream it already consumes to a durable per-run log under
`${XDG_STATE_HOME:-~/.local/state}/apex-infinite/logs/`. A
`--reduced-logging` wrapper flag opts out for operators who want less
retained data. Retention, export, and purge behavior are documented in
`docs/operator-runbook.md`. Payload safety is inherited from the event
schema (no secrets, ANSI, Rich markup, frame glyphs, or theme tokens).

## Consequences

- `apex-infinite --doctor`, `apex-infinite --setup`, shared config
  resolution (`APEX_INFINITE_CONFIG`, XDG), history purge, and the privacy
  notice are implementation work items, tracked in
  `docs/ongoing-projects/revolutionary-linux-terminal-remaining-work.md`.
- Release wording anywhere shader mode is mentioned must say "deferred".
- Tests must cover: `.env` precedence, config resolution order, doctor
  checks, setup writes (atomic + backup + permissions), profile drawer
  slots, resume-control persistence, and wrapper log teeing.
