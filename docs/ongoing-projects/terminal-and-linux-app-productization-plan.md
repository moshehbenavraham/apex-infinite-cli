# Terminal and Linux App Productization Plan

## Purpose

Turn Apex Infinite CLI from a source-checkout developer tool into an installable
terminal product and a standalone Linux visual app.

The existing Python CLI remains the workflow engine. The visual wrapper remains
a companion surface over the CLI event stream, not a fork of workflow behavior.

## Current Baseline

- `apex-infinite` already runs the autonomous Apex Spec workflow loop as a
  single Click command with flags such as `--path`, `--start`,
  `--check-provider`, `--event-stream`, and `--machine-output`.
- Package metadata already exposes console scripts for `apex-infinite` and
  `apex-infinite-visual`.
- `apex-infinite-visual` already exists as an optional PySide6/QML source-mode
  wrapper.
- The wrapper launches the Python CLI through the guarded JSONL boundary:
  `apex-infinite --event-stream - --machine-output ...`.
- Visual wrapper dependencies are already isolated behind the `.[visual]`
  optional extra.
- Source-mode wrapper controls already exist for theme, effect intensity, font
  family, font scale, reduced effects, plain fallback, glow, scanlines, flicker,
  and curvature. Persistent wrapper preferences are not implemented.
- Current config lookup is source/local/package oriented: explicit `--config`,
  then `./config.yaml`, source-root `config.yaml` when running from a checkout,
  then packaged `src/apex_infinite/config.yaml`. XDG user config and
  `APEX_INFINITE_CONFIG` are not implemented.
- Interaction history is stored in SQLite at `~/.apex-infinite/history.db`.
- `--check-provider` and `--check-provider-chat` exist as provider-only
  preflight checks. A broader `doctor` command does not exist.
- A platform smoke report is archived at
  `.spec_system/archive/phases/phase_01/platform_smoke_run_report_2026_07_03.md`; it found
  source install, tests, local Ollama preflight, dry-run loops, and wrapper
  source mode mostly healthy, but identified release-blocking runtime issues
  that Phase 01 remediated in the current source. Session 06 reruns the final
  verification matrix and appends release evidence to that report.
- Binary packaging, first-run setup, XDG config, desktop integration,
  clean-machine verification, and release artifacts are not complete.

## Phase 01 Smoke Findings Status

The original 2026-07-03 smoke report remains the historical source for the
release-blocking findings. Current source status:

- Codex invocation compatibility: remediated. The packaged default uses
  `--dangerously-bypass-approvals-and-sandbox`, startup checks configured flags
  against local `codex exec --help`, and docs describe the broad-autonomy
  policy.
- Provider preflight event-stream contract: remediated. Provider preflight
  event names are registered and covered for file and machine-output streams.
- History path normalization: remediated. `--history --path` normalizes the
  project path before querying the SQLite history key.
- Agent config semantics: remediated. `codex.exec_flags` is parsed with
  `shlex`, and `model_reasoning_effort` is passed to Codex as
  `-c model_reasoning_effort="<value>"`.
- Plain-output labels and response previews: remediated. Generic status blocks
  use stable user-facing labels, and `response_summarized.preview` contains a
  bounded preview while preserving secret and display-artifact guards.
- Local smoke environment warning: remediated in docs. The README, operator
  runbook, and troubleshooting guide now recommend an explicit repository
  virtualenv for release smoke runs.

Remaining productization blockers are the broader install and release lanes in
this plan: terminal installation, first-run setup, XDG config resolution,
diagnostics, desktop integration, clean-machine verification, AppImage review,
license notices, checksums, and release artifacts. Final Phase 01 smoke evidence
is recorded in
`.spec_system/archive/phases/phase_01/platform_smoke_run_report_2026_07_03.md`.

## Product Goals

- Operator can install and launch `apex-infinite` as a normal terminal app.
- Operator can configure provider, model, Codex binary, project path, and
  autonomy settings without editing package source files.
- Operator can run a clear diagnostic before starting an unattended workflow.
- Operator can launch a standalone Linux visual wrapper that uses the Python CLI
  as the workflow engine.
- Operator can control wrapper theme, effect intensity, font, scaling, and
  plain fallback without affecting base CLI behavior.
- Developer can package PySide6/Qt Quick/QML wrapper dependencies separately
  from the base CLI installation.
- Developer can publish a Linux AppImage only after license, clean-room,
  generated-bundle, and checksum gates pass.

## Non-Goals

- Do not replace Codex CLI.
- Do not change the Apex Spec workflow contract as part of productization.
- Do not make the base terminal CLI depend on Qt, PySide6, QML, a graphical
  display, pywebview, xterm.js, qmltermwidget, QTermWidget, or PyQt.
- Do not parse Rich output, plain terminal text, SQLite history rows, or ANSI
  captures inside the visual wrapper.
- Do not copy source, QML, shaders, colors, fonts, icons, images, terminal
  emulator code, packaging manifests, or profile data from reference projects.
- Do not ship `.deb`, `.rpm`, Flatpak, or Snap packages before the AppImage path
  has been validated with real operator feedback.

## Architecture Rules

- The Python CLI is the single workflow engine.
- The terminal UI renders human output only.
- SQLite stores raw workflow history only.
- JSONL event streams expose machine-readable lifecycle facts only.
- Every event emitted by the CLI must be registered in the event schema and
  covered by file-stream and stdout-machine-output tests.
- The visual wrapper consumes JSONL events or an importable event API.
- Wrapper settings are visual-only state and must not mutate base CLI config
  unless the operator explicitly changes shared CLI configuration.
- Graphical dependencies stay in optional extras and release packaging lanes.
- Source-mode wrapper success is necessary but not sufficient for binary
  release; generated bundles, license notices, checksums, and clean-machine
  behavior are separate gates.

## Workstream 1: Terminal Product

### Installable Command

Deliver a clean installation path for normal operators.

Work:

- Support and document `pipx install .` from the repo root.
- Verify install from built wheel and sdist, not only editable source installs.
- Add or document a local installer path that creates a dedicated venv and
  exposes `apex-infinite` on the user's shell path.
- Keep editable development install documented separately:
  `python -m pip install -e ".[dev]"`.
- Add install verification commands:
  `apex-infinite --version`, `apex-infinite --help`, and
  `apex-infinite --check-provider`.
- Document uninstall and upgrade behavior for pipx and local-venv installs.

Acceptance:

- A clean Linux user can install the terminal CLI without activating this repo's
  `.venv`.
- `apex-infinite` resolves from the shell after installation.
- `python -m build` artifacts install and expose the same console scripts as
  editable installs.
- The base install does not install PySide6 or require a display server.

### First-Run Configuration

Add a first-run path that removes source-file editing from normal setup.

Work:

- Add a command or startup flow for first-run setup.
- Let the operator choose provider: Ollama, OpenAI, or Grok.
- Let the operator choose or confirm model.
- Let the operator configure Codex binary path.
- Let the operator choose Codex exec flags with clear autonomy warnings.
- Let the operator set a default projects directory and optional default target
  project.
- Write user config to
  `${XDG_CONFIG_HOME:-~/.config}/apex-infinite/config.yaml`.
- Use atomic writes, preserve a backup when overwriting existing user config,
  and set file permissions appropriate for config that may reference secret
  environment variable names.
- Keep package defaults in `src/apex_infinite/config.yaml`.
- Support a non-interactive setup mode for scripts, for example by accepting
  flags and writing only after validation.

Acceptance:

- A new operator can create a valid user config without opening an editor.
- Existing `--config /path/to/config.yaml` behavior still works.
- Missing secrets are referenced as environment variables, not written into
  config by default.
- Re-running setup is idempotent and does not silently discard existing config.

### Config Resolution

Move runtime configuration toward normal Linux conventions while preserving
existing workflows.

Work:

- Define config precedence:
  CLI flags, explicit `--config`, `APEX_INFINITE_CONFIG`, XDG user config,
  local `./config.yaml`, source-root `config.yaml` for checkout development,
  packaged defaults.
- Add `APEX_INFINITE_CONFIG`.
- Add XDG support using `XDG_CONFIG_HOME` when set.
- Keep current local config behavior for repo-based development.
- Add clear startup output showing which config file was used.
- Emit the resolved config source in the event stream without secrets.
- Define `.env` loading precedence explicitly. Current behavior loads cwd
  `.env` first and config-directory `.env` second with override.
- Add tests for all precedence paths.

Acceptance:

- Existing users with local `./config.yaml` do not break.
- Installed users can rely on `~/.config/apex-infinite/config.yaml`.
- The CLI fails clearly when a selected config is malformed.
- The wrapper and terminal CLI resolve the same shared config for the same
  inputs.

### Doctor Command

Add a diagnostic path that checks readiness before an unattended run.

Work:

- Add a diagnostic entrypoint. If the CLI remains a single Click command, expose
  it as `apex-infinite --doctor`; if the CLI migrates to a Click group, preserve
  all existing root flags and expose `apex-infinite doctor`.
- Check Python version.
- Check Codex CLI availability and version.
- Check configured Codex binary path.
- Check `codex exec --help` against configured `codex.exec_flags`, including
  stale or renamed autonomy flags.
- Check provider name, API key presence, base URL, and model availability.
- Check optional provider chat completion when requested.
- Check target project path.
- Check `.spec_system/` presence when a workflow command requires it.
- Check SQLite history DB path and writeability.
- Check event-stream output path when provided.
- Check visual-wrapper dependencies only when requested.
- Check event-stream schema registration for all startup preflight events.
- Print a concise pass/warn/fail report.

Acceptance:

- The diagnostic exits non-zero for hard blockers.
- The diagnostic distinguishes hard failures from warnings.
- The diagnostic redacts secrets.
- The diagnostic gives exact next commands for common fixes.
- `--check-provider` remains available as a fast provider-only check.

### Runtime Compatibility And Hardening

Fix the current smoke-run blockers that can make an installed CLI appear healthy
while failing in real operation.

Work:

- Replace or version-gate the default Codex autonomy flag.
- Add a real Codex subprocess smoke fixture that can prove command construction
  without mutating the target repository.
- Register provider preflight event names, or rename the emits to existing event
  names, and test provider startup with file event streams and stdout
  machine-output streams.
- Normalize project paths through one shared helper before writing or querying
  history.
- Replace whitespace splitting of `codex.exec_flags` with `shlex.split` or a
  validated list form.
- Decide whether `model_reasoning_effort` is active config. If active, map it to
  current Codex CLI syntax; if inactive, remove it from defaults and docs.
- Replace internal plain-output labels with stable labels such as `STATUS`.
- Make response preview behavior explicit in the event-stream contract.

Acceptance:

- A one-iteration non-dry-run Codex subprocess smoke passes with the packaged
  default config or fails before launch with a precise compatibility message.
- Successful provider preflight does not create `event_stream_error` rows.
- History can be read with or without a trailing slash in `--path`.
- Quoted Codex config flags are tokenized as documented.

### Launcher Ergonomics

Make the terminal app easier and safer to run repeatedly.

Work:

- Add default project selection from config.
- Add a resume-friendly command or documented pattern for last project.
- Add aliases or shortcuts for common starts:
  dry run, resume, history, provider check, and plain log mode.
- Add safer onboarding around broad Codex autonomy flags.
- Avoid naming only one stale Codex flag in user-facing guidance; describe the
  actual configured autonomy policy and whether the installed Codex binary
  supports it.
- Show a prominent autonomy summary before real runs when broad Codex exec flags
  are configured.
- Keep `--dry-run` as the recommended first execution path.

Acceptance:

- A new operator can understand what level of autonomy Codex will have before
  the first real run.
- Repeated runs do not require retyping long project paths.
- Existing direct flags still work for automation.

### Terminal Documentation

Package the real usage loop as product docs, not just reference docs.

Work:

- Add an installation guide.
- Add a first-run guide.
- Add a provider setup guide for Ollama, OpenAI, and Grok.
- Add a safe-run guide:
  dry run, provider check, start command, max iterations, interrupt, history,
  resume.
- Add a troubleshooting section for installed users.
- Maintain troubleshooting guidance for stale activated virtualenvs where
  `python` resolves to another project's venv.
- Add a short "what data is stored where" note covering config and SQLite
  history.
- Link the platform smoke report and keep current remediation status
  synchronized with this plan.

Acceptance:

- A user can install, configure, dry-run, run, interrupt, and inspect history by
  following docs from a clean machine.
- Docs clearly separate base terminal installation from optional visual wrapper
  installation.

## Workstream 2: Linux Visual App

### Wrapper Runtime

Keep the current PySide6/QML wrapper as the selected Linux visual surface.

Work:

- Preserve lazy PySide6 imports.
- Preserve `.[visual]` as the optional dependency lane.
- Preserve launch through:
  `apex-infinite --event-stream - --machine-output ...`.
- Keep stdout reserved for JSONL events when machine-output mode is active.
- Keep stderr separate and summarize it in wrapper failure state.
- Keep base CLI behavior testable without graphical dependencies.

Acceptance:

- `apex-infinite-visual --launch-cli ...` launches the Python CLI as the engine.
- The wrapper never scrapes Rich panels or plain terminal output.
- The base CLI test suite can run without PySide6 installed.

### Visual Controls

Keep the existing source-mode controls product-facing and add persistence.

Work:

- Preserve existing controls: `crt-green`, `crt-amber`, `ibm-dos`, `plain`,
  effect intensity, font family, font scale, reduced-effects mode, plain
  fallback, and per-effect toggles.
- Add startup loading from persisted wrapper settings.
- Add explicit reset-to-defaults behavior.
- Persist visual preferences in a wrapper-specific config location.
- Ensure wrapper visual settings do not change base CLI config.

Acceptance:

- Operator can change wrapper theme, effects, font, scaling, and fallback from
  the visual app.
- Restarting the wrapper restores visual preferences.
- Base terminal output is unchanged by wrapper visual preferences.

### Visual Effects

Finish and verify graphical effects that Rich cannot faithfully render.

Work:

- Preserve independently designed glow, scanline overlay, screen curvature, and
  subtle flicker already present in source mode.
- Add or explicitly defer phosphor trail or persistence effect with a written
  rationale.
- Add low-effects fallback for unsupported scene graph backends.
- Keep effects disabled or restrained when reduced-effects mode is active.
- Keep all effect code, constants, and assets clean-room.
- Add screenshot or pixel-level smoke checks for desktop and offscreen modes
  where feasible.

Acceptance:

- Visual wrapper can demonstrate glow, curvature, flicker, scanline overlays,
  and the accepted trail/persistence decision.
- Effects are configurable and can be disabled.
- Unsupported graphics environments fall back to a readable low-effects scene.

### Graphical First-Run Setup

Add a visual onboarding path for users who start from the Linux app.

Work:

- Detect missing user config.
- Guide provider selection: Ollama, OpenAI, Grok.
- Guide model selection or entry.
- Guide Codex binary selection.
- Guide project path selection.
- Offer dry-run as the first launch mode.
- Surface diagnostic results inside the wrapper.
- Show the same Codex autonomy summary as the terminal CLI before real runs.
- Write shared CLI configuration only after explicit operator action.

Acceptance:

- A user can launch the visual app on a clean install and reach a dry-run-ready
  configuration without using the terminal.
- The wrapper can open the same target project the terminal CLI would open.
- Config writes are explicit and recoverable.

### Desktop Integration

Make the wrapper feel like a Linux app.

Work:

- Add `.desktop` metadata.
- Add app name, categories, icon, and launcher command.
- Add an application icon created independently for this project.
- Add desktop launch behavior for installed AppImage.
- Add command-line arguments that still allow direct project/start overrides.
- Document where logs, shared config, wrapper preferences, and history live.
- Ensure desktop launches do not assume the source checkout as the current
  working directory.

Acceptance:

- The app appears in a Linux desktop launcher after installation or AppImage
  integration.
- Launching from the desktop reaches the visual app, not a terminal-only
  process.
- CLI overrides remain available for power users.

### AppImage Packaging

Ship the first binary visual-wrapper artifact as an x86_64 Linux AppImage.

Work:

- Build the PySide6/QML wrapper in an isolated packaging workspace.
- Decide and document the packaging path. Evaluate `pyside6-deploy` first; use
  direct Nuitka packaging only if reviewed and documented.
- Ensure the packaged app can launch the installed base CLI module or bundled
  equivalent without relying on this checkout.
- Inspect generated files, collected Qt plugins, and runtime dependencies.
- Wrap the reviewed build as:
  `apex-infinite-visual-linux-x86_64.AppImage`.
- Publish SHA256 checksums.
- Publish source/dev install instructions alongside the binary.
- Do not commit generated packaging output unless explicitly intended as release
  source.

Acceptance:

- The AppImage launches on a clean supported Linux machine.
- The AppImage can run fixture/demo mode.
- The AppImage can launch a real CLI-backed dry run when config and Codex are
  available.
- The AppImage fails gracefully when Codex or provider config is missing.
- The release includes a SHA256 checksum.

### License And Release Gates

Do not publish a binary until legal and clean-room gates are satisfied.

Work:

- Confirm Qt for Python license path: LGPLv3-compatible or commercial.
- Include required Qt/PySide6 notices.
- Confirm no GPL-only Qt modules are bundled.
- Confirm AppImage packaging does not block replacement or relink rights.
- Provide source availability or relink/replacement instructions if required.
- Include dependency inventory or SBOM-style bundle manifest for Python wheels,
  Qt libraries, Qt plugins, and AppImage runtime components.
- Confirm no copied reference source, QML, shaders, shader constants, shader
  blobs, images, icons, fonts, profile data, resource manifests, build scripts,
  terminal-emulator code, qmltermwidget, or QTermWidget material is tracked.
- Record the generated bundle inventory.

Acceptance:

- A release reviewer can inspect license notices, dependency inventory,
  checksum, and clean-room evidence.
- The binary release is blocked if license or clean-room evidence is incomplete.

### Clean Linux Verification

Test outside the development checkout before calling the app productized.

Work:

- Test base terminal install on a clean Linux environment.
- Test wheel and sdist installs in a clean venv with a clean home directory.
- Test visual extra source install on a clean Linux environment.
- Test AppImage launch without source checkout assumptions.
- Test no-display or unsupported-display behavior.
- Test Ollama provider path.
- Test OpenAI or Grok provider path with redacted credentials.
- Test a real target project with `.spec_system/`.
- Test a bounded real Codex subprocess path, not only `--dry-run`.
- Test `--check-provider` with file event streams and stdout machine-output
  streams.
- Test history lookup path normalization.
- Test malformed config, missing Codex CLI, missing provider key, missing model,
  invalid project path, and malformed JSONL event handling.

Acceptance:

- Clean-machine results are documented.
- Failures produce actionable messages.
- AppImage behavior does not depend on this repo's `.venv`.
- No successful smoke run emits event-stream schema errors.

## Backup Path: pywebview Plus xterm.js

The selected wrapper path does not require a terminal-emulator viewport. It
renders lifecycle events and captured output through native QML models/views.

Document pywebview plus xterm.js as a backup only if a future accepted
requirement needs one of these:

- Interactive shell behavior.
- PTY support.
- curses-like application rendering.
- Raw ANSI terminal fidelity.
- Full terminal copy/paste semantics beyond an event log viewport.

If that requirement appears, run a separate spike before changing architecture.
The backup path must remain optional, license-reviewed, clean-room, and isolated
from the base terminal CLI.

## Recommended Build Order

1. Preserve Phase 01 smoke-remediation evidence and keep the release smoke
   matrix green.
2. Terminal install and config conventions.
3. First-run setup and diagnostic command or flag.
4. Terminal launcher ergonomics and user docs.
5. Visual wrapper persistence and graphical first-run setup.
6. Visual effects completion and low-effects fallback.
7. Desktop metadata and icon.
8. Isolated AppImage packaging.
9. License, clean-room, checksum, and clean Linux release verification.

This order fixes known runtime blockers first, gets the terminal product usable,
then makes the visual wrapper installable, then turns the wrapper into a
releasable Linux app.

## Definition Of Done

The productization effort is done when:

- A clean Linux user can install and run `apex-infinite` as a terminal command.
- A clean Linux user can configure provider/model/Codex/project without editing
  package source files.
- The diagnostic entrypoint catches the common blockers before an unattended run.
- Default Codex exec configuration is compatible with the supported Codex CLI or
  fails before launch with an actionable diagnostic.
- Event streams do not emit schema errors during successful startup or provider
  preflight.
- Terminal docs cover install, first run, dry run, real run, interrupt, history,
  resume, and troubleshooting.
- A clean Linux user can launch `apex-infinite-visual` as a standalone app.
- The visual app uses the Python CLI as its workflow engine.
- The visual app controls theme, effects, font, scaling, and fallback without
  changing base CLI behavior.
- PySide6/QML remains optional and separate from the base CLI install.
- The AppImage launches on a clean supported Linux machine.
- The release includes license notices, dependency inventory, clean-room
  evidence, and SHA256 checksums.
