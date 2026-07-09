# Apex Infinite CLI - Product Requirements Document

## Overview

Apex Infinite CLI is a standalone autonomous OpenAI Codex CLI session manager
for Apex Spec System projects. It runs initialized projects through the staged
workflow loop by asking a manager LLM for the next action, executing Codex CLI,
storing history in SQLite, and repeating until the workflow reaches completion
or a safety stop.

The current CLI already supports provider configuration, `codex exec`
subprocess calls, history storage, dry runs, operator interrupts, and
prompt/routing tests. This PRD focuses the standalone package on a polished,
testable operator console while preserving the existing autonomous workflow
contract.

The completed terminal upgrade provides a Rich-based operator console, explicit
plain-output fallbacks, and a raw lifecycle event boundary. The next product
lane is Apex Infinite Hyperterminal: a Linux-native, event-driven visual command
surface that uses the Python CLI as the workflow engine while keeping graphical
dependencies out of the base CLI install.

## Goals

1. Preserve the autonomous Apex Spec workflow loop, including manager decisions, `Next command:` handoffs, Codex execution, history logging, and stop conditions.
2. Improve the interactive operator experience with a cohesive terminal UI that remains readable during long-running autonomous sessions.
3. Add explicit, validated UI configuration and CLI flags for themes, plain output, ASCII output, compact output, and event streaming.
4. Maintain backward compatibility for existing `~/.apex-infinite/history.db` files and prompt/routing behavior.
5. Provide a raw lifecycle event stream that future visual surfaces can consume without scraping terminal output.
6. Promote the standalone Linux visual wrapper into an event-driven
   Hyperterminal command surface without adding graphical dependencies to the
   base CLI.
7. Ship the visual lane with persisted profiles, workflow-aware effects, first-run setup, doctor UX, desktop integration, and clean-room release evidence.

## Non-Goals

- Replacing Codex CLI or changing the Apex Spec staged workflow.
- Rewriting the manager or summarizer prompt contract unless a scoped session explicitly changes prompt behavior and updates tests and docs together.
- Requiring `cool-retro-term`, qmltermwidget, QTermWidget, PyQt, an external terminal emulator, or a graphical display for normal CLI use.
- Copying `cool-retro-term` code, QML, shaders, generated shader blobs, images,
  icons, fonts, resource manifests, profile data, package metadata, terminal
  widget code, or build scripts.
- Migrating or renaming the legacy SQLite `cc_response` column.
- Shipping macOS or Windows visual-wrapper support in this project.
- Turning the visual wrapper into a general-purpose terminal emulator, shell,
  web dashboard, or landing page.
- Broadly rebuilding the root Apex Spec skill package except where CLI integration docs or command routing require it.

## Users and Use Cases

### Primary Users

- **Operator**: Runs Apex Infinite CLI against initialized projects and needs clear progress, errors, history, and safe interruption.
- **Apex Spec maintainer**: Develops and verifies the CLI, command prompts, docs, tests, and release artifacts.
- **Automation environment**: Runs the CLI in dry-run, redirected, non-TTY, CI, log-file, or headless contexts where stable plain output matters.
- **Visual app operator**: Runs the Linux Hyperterminal surface and needs the same workflow control as the CLI with richer state visibility.
- **Visual wrapper developer**: Builds event-derived QML surfaces, profile persistence, effects, packaging, and release verification without depending on Rich output internals.

### Key Use Cases

1. Operator starts or resumes an autonomous Apex Spec workflow for a target project with optional starting command and CEO instruction.
2. Operator runs dry-run mode to confirm provider, model, Codex binary, and generated prompt before executing Codex.
3. Operator monitors a long-running Codex subprocess with clear elapsed-time, timeout, error, and completion states.
4. Operator inspects recent history for a project and expands detail with `--verbose`.
5. Automation runs the CLI with plain or ASCII output and receives deterministic logs without styled control data.
6. Visual wrapper consumes JSONL lifecycle events and renders its own display without scraping terminal frames.
7. Operator launches Apex Infinite Hyperterminal, configures provider/model/project on first run, runs doctor, and starts with a dry run before live operation.
8. Operator saves, duplicates, imports, exports, and resets visual profiles without changing shared CLI config or exposing secrets.

## Requirements

### MVP Requirements

- Operator can configure provider, model, Codex binary, Codex exec flags, and reasoning effort through `config.yaml` and supported CLI overrides.
- Operator can start the autonomous loop with a project path, starting command, CEO instruction, dry-run mode, verbose mode, history mode, and max-iteration safety limit.
- Manager LLM can route known Apex Spec workflow commands from structured JSON output, slash-prefixed command output, or normalized text output.
- Manager LLM can pass unknown output through as raw high-level instructions to Codex CLI.
- CLI can execute `codex exec` with configured flags and preserve stdout, stderr, return code, timeout, missing-binary, and generic-exception behavior.
- CLI can write one SQLite history row per iteration using WAL mode and a normalized project path key.
- CLI can show a compact project history ledger and expand row detail when `--verbose` is used.
- Operator can select built-in UI modes for `auto`, `crt-green`, `crt-amber`, `ibm-dos`, and `plain`.
- Operator can use `--plain`, `--ascii`, `--compact`, and `--theme` overrides without editing config.
- CLI can resolve UI settings with deterministic precedence: CLI flags, environment constraints, config, then built-in defaults.
- CLI can choose plain output by default under `NO_COLOR`, `TERM=dumb`, non-TTY output, redirected output, or non-terminal Console paths.
- CLI can fail fast on invalid theme names or malformed custom theme configuration with clear Click or config errors.
- CLI can render startup, iteration, manager decision, prompt, Codex execution, result, DB log, help, completion, timeout, and error states through centralized renderer helpers.
- CLI can keep ANSI escapes, Rich markup, box glyphs, and styled output out of SQLite history rows.
- Developer can test renderer behavior with injected Rich `Console(record=True, width=...)` objects.
- Developer can verify config parsing, Click flags, prompt routing, subprocess behavior, history rendering, plain mode, `NO_COLOR`, and non-TTY behavior through pytest.
- CLI can emit opt-in line-buffered JSONL lifecycle events to `--event-stream PATH` without changing normal human output.
- Developer can import an event emitter API for tests and visual wrappers.

### Deferred Requirements

- Operator can launch Apex Infinite Hyperterminal as a standalone Linux visual app using the Python CLI as the workflow engine.
- Operator can use a first-run visual setup flow for provider, model, Codex binary, project selection, doctor checks, and dry-run launch.
- Operator can control visual profile, rendering mode, quality tier, effect intensity, font family, font scale, font width, line spacing, reduced effects, and plain fallback without affecting base CLI behavior.
- Operator can save, duplicate, rename, delete, import, export, reset, and automatically reload versioned visual profiles stored under XDG config/state locations.
- Operator can inspect a full-window command surface with run controls, mission state rail, spec map, event core, signal panel, and visual profile drawer.
- Operator can see workflow-aware visual effects triggered by real events such as run start, provider preflight, manager decision, iteration progress, stop, completion, timeout, stderr, and malformed JSONL.
- Developer can split visual wrapper state into a visual event adapter, display state store, QML bridge, reusable scene components, effect pipeline, and presentation shell.
- Developer can add registered CLI lifecycle events for doctor, config, Codex flags, autonomy policy, spec system detection, session resolution, task progress, artifact detection, duration ticks, and wrapper capability resolution.
- Developer can package PySide6/Qt Quick/QML wrapper dependencies as an optional extra separate from base CLI installation.
- Developer can publish original desktop metadata, app icon, AppStream metadata, AppImage artifact, SHA256 checksum, dependency inventory, license notices, and clean-machine release evidence.
- Developer can document pywebview plus xterm.js as a backup only if a future accepted requirement makes a true terminal-emulator viewport mandatory.

## Non-Functional Requirements

- **Performance**: Startup config loading and history rendering for 50 rows must complete in under 2 seconds on a local development machine, excluding network LLM calls and Codex subprocess runtime.
- **Security**: API keys must be loaded from environment-backed config values and must not be printed, written to SQLite history, or emitted in JSONL events in normal operation.
- **Privacy**: SQLite history and JSONL events must store raw workflow facts only; tests must verify 0 Rich markup strings and 0 ANSI escape sequences are stored.
- **Reliability**: Existing prompt/routing tests must remain green, and new subprocess tests must cover success, stderr-only output, non-zero exit, timeout, dry-run, and missing binary paths.
- **Accessibility**: Plain and ASCII modes must avoid non-ASCII frame glyphs and remain readable at 80, 100, and 120 terminal columns.
- **Compatibility**: Existing `~/.apex-infinite/history.db` files must remain readable without migration, and the legacy `cc_response` column must remain intact.
- **Portability**: Base CLI must run on Python 3.10+ with terminal-only dependencies and no graphical runtime dependency.
- **Maintainability**: Renderer, config, event, subprocess, DB, and prompt-routing changes must have focused tests before a session is validated.
- **Visual Performance**: The visual wrapper must target 60fps, limit active animated elements to 3 per viewport region, and provide Balanced, Battery, Low Effects, and Plain fallbacks when shader or graphics capability is insufficient.
- **Visual Release Quality**: Hyperterminal completion requires offscreen smoke launch, desktop screenshot smoke for high/balanced/low/plain profiles, pixel nonblank checks, reduced-effects checks, malformed JSONL checks, clean base install checks, visual extra install checks, and AppImage clean-machine launch checks.
- **Clean Room**: Release verification must confirm 0 tracked `EXAMPLE/` files and no copied reference QML, shaders, generated shader blobs, images, icons, fonts, profiles, manifests, build scripts, terminal-widget code, or package metadata.

## Constraints and Dependencies

- The base CLI runtime is Python 3.10+.
- The base CLI depends on Click, Rich, OpenAI Python SDK, python-dotenv, PyYAML, SQLite from the Python standard library, and Codex CLI.
- Development verification uses pytest, pytest-cov, pytest-mock, black, and pylint.
- The root Apex Spec scripts remain bash + jq only; do not add Python dependencies to root scripts.
- The project uses ASCII-only authored files with Unix LF line endings.
- The repository is standalone; CLI sessions should target the repository root
  rather than a nested package path.
- `EXAMPLE/cool-retro-term` is reference-only and ignored by Git.
- `cool-retro-term` material is GPL-family reference material; product work must use clean-room visual translation only.
- PySide6/Qt Quick/QML is allowed only for an optional Linux visual wrapper path, with LGPLv3/commercial obligations documented.
- PyQt, qmltermwidget, QTermWidget, copied QML, copied shaders, copied
  generated shader blobs, copied assets, copied fonts, copied profile data,
  copied resource manifests, copied package metadata, copied build scripts, and
  copied terminal-emulator code are excluded unless a future explicit decision
  changes scope.
- The CLI must preserve existing prompt contract behavior unless
  `src/apex_infinite/cli.py`, tests, README, and prompt-contract docs are
  updated together.
- Visual wrapper profile files are stored under `${XDG_CONFIG_HOME:-~/.config}/apex-infinite/visual-profiles.json`.
- Visual wrapper runtime window state can be stored under `${XDG_STATE_HOME:-~/.local/state}/apex-infinite/visual-state.json`.
- The first visual binary artifact is `apex-infinite-visual-linux-x86_64.AppImage` with SHA256 checksum and release notices.
- `pyside6-deploy` is evaluated first for visual packaging; direct Nuitka or another path requires documented evidence before use.

## Phases

This system delivers the product via phases. Each phase is implemented via multiple 2-4 hour sessions (12-25 tasks each).

| Phase | Name | Sessions | Status |
|-------|------|----------|--------|
| 00 | Apex Infinite CLI Upgrade | 8 | Complete |
| 01 | Smoke Remediation And Release Hardening | 6 | Complete |
| 02 | Apex Infinite Hyperterminal | 14 | Planned |

## Phase 00: Apex Infinite CLI Upgrade

### Objectives

1. Centralize Rich rendering and UI configuration without changing workflow behavior.
2. Deliver the first complete CRT-inspired terminal operator experience with robust plain-output fallbacks.
3. Improve live subprocess visibility and history readability while preserving captured output semantics.
4. Document and test the UI upgrade, then expose a raw event stream for future wrappers.
5. Spike and productize the optional Linux visual wrapper without adding graphical dependencies to the base CLI.
6. Verify the complete upgrade against compatibility, testing, documentation, release, and clean-room criteria.

### Sessions

Completed session stubs are archived under `.spec_system/archive/phases/phase_00/`.

| Session | Name | Source Theme |
|---------|------|--------------|
| 01 | Config And Renderer Boundary | UI architecture and theme tokens |
| 02 | Rich Operator Console | CRT-inspired operator console |
| 03 | Subprocess And History Visibility | Live execution and better history |
| 04 | Event Stream Boundary | Engine boundary and event stream |
| 05 | Docs Samples And Runbooks | Documentation, samples, and polish |
| 06 | Linux Wrapper Spike | Linux visual wrapper spike |
| 07 | Linux Visual Wrapper Productization | Linux visual wrapper productization |
| 08 | Release Verification | Release verification |

## Phase 01: Smoke Remediation And Release Hardening

### Source

Phase 01 is generated from the archived smoke report at
`.spec_system/archive/phases/phase_01/platform_smoke_run_report_2026_07_03.md`, which
records the 2026-07-03 platform smoke results and the follow-up session split.

### Objectives

1. Restore compatible default Codex subprocess invocation for non-dry-run operation.
2. Make provider preflight lifecycle events valid for event-stream consumers.
3. Normalize history lookup paths before querying SQLite history.
4. Polish plain output labels and response summary preview behavior.
5. Align agent configuration parsing and reasoning-effort documentation with actual subprocess behavior.
6. Add local smoke environment guidance and rerun release verification.

### Sessions

Completed session stubs are archived under `.spec_system/archive/phases/phase_01/`.

| Session | Name | Source Theme |
|---------|------|--------------|
| 01 | Codex Invocation Compatibility | Codex CLI flag compatibility |
| 02 | Provider Event Stream Contract | Provider event schema |
| 03 | History Path Normalization | SQLite history lookup |
| 04 | Output Observability Polish | Plain output and event previews |
| 05 | Agent Config Semantics | Codex config parsing |
| 06 | Documentation And Release Verification | Smoke docs and final verification |

## Phase 02: Apex Infinite Hyperterminal

### Source

Phase 02 is planned from
`docs/ongoing-projects/revolutionary-linux-terminal-design-plan.md`, which
promotes the existing source-mode visual wrapper into a production Linux command
surface.

### Objectives

1. Extract visual state from the QML bridge into event-derived Python models and fixtures.
2. Persist versioned XDG visual profiles with import, export, reset, migration, corruption handling, and safe config boundaries.
3. Redesign the visual app into a full-window command surface with run controls, mission rail, spec map, event core, signal panel, and profile drawer.
4. Add QML-only high-design effects, quality tiers, reduced-effects enforcement, and screenshot smoke checks before custom shader work.
5. Expand CLI events only for facts the wrapper needs, keeping payloads raw, secret-free, and independent from visual choices.
6. Add graphical doctor and first-run setup so a clean Linux user can configure, verify, and start with dry run from the app.
7. Add original clean-room shader effects, desktop metadata, AppImage packaging, license notices, checksums, and clean-machine verification.
8. Finish with a matching terminal CLI polish pass that preserves plain and machine-output contracts.

### Sessions

Planned session stubs are defined by `phasebuild`.

| Session | Name | Source Theme |
|---------|------|--------------|
| 01 | Visual State Model | Event-derived display state and fixtures |
| 02 | Visual Profile Persistence | XDG profiles, import/export, corruption handling |
| 03 | QML Shell Components | Split reusable command-surface components |
| 04 | Command Surface Redesign | Event log, status rail, run command strip |
| 05 | QML High-Design Effects | Glow, scanlines, frame treatment, quality tiers |
| 06 | Event-Reactive Motion | Lifecycle-triggered effects and fallback checks |
| 07 | CLI Event Expansion | Missing machine-readable workflow facts |
| 08 | Graphical Doctor And First Run | Config setup, doctor, dry-run default |
| 09 | Shader Pipeline Spike | Original shaders and capability detection |
| 10 | Shader Production Promotion | Accepted effects, fallbacks, tests |
| 11 | Desktop Metadata And Icon | Original icon, desktop file, AppStream draft |
| 12 | AppImage Release Candidate | Build, inspect, checksum, notices |
| 13 | Clean Linux Verification | Clean-machine launch and blocker fixes |
| 14 | Terminal CLI Polish | Matching Rich theme and docs pass |

## Technical Stack

- Python 3.10+ - base CLI runtime and standard library support.
- Click - command-line parser and validation layer.
- Rich - terminal rendering, panels, tables, status, and testable recorded consoles.
- SQLite WAL - local interaction history at `~/.apex-infinite/history.db`.
- OpenAI-compatible API client - manager and summarizer LLM calls.
- python-dotenv and PyYAML - environment expansion and YAML config loading.
- Codex CLI - autonomous agent execution through `codex exec`.
- pytest, pytest-mock, pytest-cov - automated verification.
- black and pylint - formatting and linting for Python code.
- PySide6 with Qt Quick/QML - optional Linux Hyperterminal visual app path.
- QML scene components - command surface, status rail, event core, spec map, signal panel, settings drawer, controls, and effects.
- Qt Quick ShaderEffect - optional clean-room shader effects when capability detection and fallbacks pass.
- XDG config/state files - visual profile persistence and runtime window state.
- AppImage packaging - first binary visual wrapper release artifact.

## Success Criteria

- [x] Existing prompt/routing behavior remains compatible and covered by tests.
- [x] CLI users can enable `auto`, `crt-green`, `crt-amber`, `ibm-dos`, and `plain` themes.
- [x] CLI users can disable styling with `--plain` and avoid non-ASCII glyphs with `--ascii`.
- [x] Plain output is selected automatically for constrained terminal environments unless explicitly overridden.
- [x] History display is readable without horizontal scrolling at 80 columns.
- [x] SQLite history rows remain raw and backward compatible with existing databases.
- [x] JSONL event stream emits raw lifecycle facts without Rich markup.
- [x] README and deep-dive docs describe UI flags, config, event stream, and troubleshooting.
- [x] No reference source, QML, shader, generated shader blob, image, icon,
  font, resource manifest, package metadata, build script, terminal-widget
  code, or literal profile data is copied into the CLI.
- [x] Optional Linux wrapper path has documented dependency, license, packaging, and interface boundaries.
- [ ] Apex Infinite Hyperterminal opens as the first screen of the visual app, not a dashboard or landing page.
- [ ] Visual state is derived from registered events or explicit wrapper controls, not raw JSONL parsing in QML or Rich output scraping.
- [ ] Visual profiles, rendering modes, quality tiers, and effect preferences persist across launches.
- [ ] Workflow-aware visual effects react to real lifecycle events while reduced-effects and plain fallback modes remain usable.
- [ ] Graphical first-run setup and doctor let a clean Linux user configure and start with dry run without editing source files.
- [ ] Desktop launcher and AppImage work on a clean supported Linux machine with checksum, notices, inventory, and clean-room evidence.
- [ ] Terminal CLI polish preserves `--event-stream - --machine-output`, redirected output, and plain-output contracts.

## Risks

- **Retro styling reduces readability**: Keep contrast high, effects low by default, and provide `--plain`, `--ascii`, and compact modes.
- **Terminal compatibility varies**: Respect `NO_COLOR`, `TERM=dumb`, non-TTY output, redirected output, and common terminal widths.
- **Styled output pollutes durable records**: Store raw workflow data only and test for 0 ANSI or Rich markup in SQLite and event payloads.
- **Live subprocess display changes behavior**: Preserve current stdout, stderr, return code, timeout, and verbose semantics with subprocess tests.
- **Dependency creep slows base CLI use**: Finish Rich milestones first and keep wrapper dependencies optional.
- **GPL contamination concerns**: Use `cool-retro-term` only as visual reference and document no-copy boundaries.
- **Wrapper diverges from CLI behavior**: Keep one workflow engine and make the wrapper a display/runtime shell over JSONL events.
- **Visual complexity hides workflow state**: Make the first viewport the actual command surface, keep event log readable, and bind effects to workflow facts rather than decoration.
- **Shader work overruns core UX**: Complete QML-only high design, profile persistence, and command-surface architecture before custom shader promotion.
- **Graphics capability varies across Linux systems**: Probe shader and scene graph support, then fall back automatically to low-effects or plain modes.
- **Profile persistence corrupts user state**: Use versioned schemas, atomic writes, backup-on-overwrite, migration stubs, and visible corruption recovery.
- **Desktop packaging bundles inappropriate dependencies**: Inspect Qt plugins and generated bundle contents, document license path, and verify no GPL-only Qt modules are bundled.
- **CLI entry point becomes harder to maintain**: Split renderer, config,
  event, DB, or subprocess helpers when that lowers risk versus extending
  `src/apex_infinite/cli.py`.

## Assumptions

- The master PRD scope is Apex Infinite CLI development in this standalone
  repository. The Phase 00 PRD plus session stubs contain the folded CLI upgrade
  plan.
- The repository should be treated as a single standalone package rooted at this
  directory.
- Apex Infinite Hyperterminal is the visual lane name, not a command rename. The command names remain `apex-infinite` and `apex-infinite-visual` unless a future release explicitly changes them.
- Prompt routing should remain stable during UI work: `docs/prompt-contract.md`
  and the upgrade plan both require prompt changes to be made only with matching
  tests and docs.
- `cool-retro-term` is inspiration only: the upgrade and Hyperterminal plans record GPL/license boundaries and forbid copying source, shader, asset, font, profile, manifest, build, terminal-widget, or package metadata.

### Conflict Resolutions

- The repo is no longer a subproject inside a larger workspace. The chosen
  interpretation is single-repo planning with sessions scoped to the standalone
  repository root.
- Visual direction references `cool-retro-term`, while license boundaries forbid copying. The chosen interpretation is clean-room visual translation: use concepts such as terminal mood, status hierarchy, and effect categories while creating independent tokens, code, docs, and assets.
- The older PRD treated the Linux wrapper as exploratory, while the Hyperterminal plan makes it a planned product lane. The chosen interpretation is to add Phase 02 while preserving completed Phase 00 and Phase 01 records.

## Open Decisions

1. Decide which QML-only effects earn promotion into original shader effects after command-surface architecture and capability detection are stable.
2. Decide whether `pyside6-deploy` remains the packaging path after inspecting generated bundle contents; document evidence before using direct Nuitka or another approach.
3. Decide final original icon and asset provenance before desktop metadata and AppImage release.
