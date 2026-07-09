# Revolutionary Linux Terminal Remaining Work

This is the standalone remaining-work tracker for Apex Infinite terminal and
Linux visual productization as of the 2026-07-09 audit. It intentionally lists
only open decisions, unfinished work, release gates, and verification still
needed.

Inline `Reference:` bullets identify matching `cool-retro-term` example paths
for conceptual review and clean-room audit only. Do not copy from them, reuse
assets, or make runtime behavior depend on the `EXAMPLE/` tree.

## Open Product Decisions

All open product decisions were closed on 2026-07-09 and recorded in
`docs/adr/0001-release-scope-decisions.md`. Summary:

- [x] Command-strip resume: in scope, minimal form. Resume = re-launch the
  last project/controls through the event-driven launcher; last-run controls
  persist in the wrapper-owned visual-state file. (ADR 0001 #1)
- [x] Shader mode: deferred for this release. `.qsb` stays ignored; QML-only
  source mode is the shipped visual path and release wording must say so.
  (ADR 0001 #2)
- [x] Profile drawer: full parity. Expose import, export, duplicate, rename,
  reset, and validation UI; add missing bridge slots. (ADR 0001 #3)
- [x] Workstream 8 terminal CLI polish: complete; no further polish scoped.
  (ADR 0001 #4)
- [x] New workflow state uses registered events, never wrapper assumptions
  (standing rule reaffirmed; see Event Boundary section). (ADR 0001)
- [x] Terminal doctor entrypoint: `apex-infinite --doctor`; root stays a
  single Click command. (ADR 0001 #5)
- [x] Terminal and visual doctor share a diagnostic backend in
  `src/apex_infinite/doctor.py`; visual adds PySide6/display checks.
  (ADR 0001 #6)
- [x] `.env` precedence: config-directory `.env` overrides cwd `.env`;
  behavior is tested. (ADR 0001 #7)
- [x] Codex bypass policy: accepted-risk documentation plus visible autonomy
  summary, dry-run-first onboarding, and setup-time warning. (ADR 0001 #8)
- [x] Publishing and rollback remain external/manual, recorded in
  `packaging/RELEASE-CHECKLIST.md`. (ADR 0001 #9)
- [x] No `docs/CODEOWNERS`; revisit with a second regular contributor.
  (ADR 0001 #10)

## Visual App Remaining Work

- [x] Implement command-strip resume. (2026-07-09, per ADR 0001 #1: a
  first-class Resume button sits in the command strip next to Start/Stop,
  always present (disabled when no stored run) so controls never shift.
  Last-run controls persist in the wrapper-owned
  `visual-state.json`; resume re-launches through the event-driven
  launcher with no output scraping. Tests:
  `tests/test_hyperterminal_bridge.py` resume suite.)
- [x] Recheck the first viewport against the final product acceptance
  language. (2026-07-09: the first viewport is the operator terminal - the
  command strip with project path, start command, dry-run/live segmented
  control, max-iteration stepper, Start/Resume/Stop/Doctor buttons, and the
  autonomy summary; mission state, event core, spec map, and signal panel
  fill the rest. Errors surface as typed red event rows plus failed run
  health and error pulses; first-run needs render as the setup panel, not
  a crash.)
- [x] Recheck the command strip details before release. (All controls
  present including Resume per ADR 0001 #1; autonomy summary shows mode,
  max iterations, and risk; Codex flag compatibility shows in mission
  state and the first-run panel.)
- [x] Recheck mission-state and launch-readiness details before release.
  (Status rail shows run status, stage, iteration, provider, model, config
  source, Codex flag state, event stream mode, and history DB status;
  missing provider/Codex/model/project/config produce doctor fail rows,
  typed error events, and the first-run panel instead of crashes -
  verified by launch-validation and doctor tests.)
- [x] Recheck event-core and signal-panel behavior before release.
  (Virtualized typed rows with severity/stage/timestamp; search, stage,
  and severity filters; JSON export; malformed event count, stderr
  summary, duration, last event, and safe artifact names in the signal
  panel - covered by bridge and visual-state tests.)
- [x] Recheck spec-map behavior before release. (Detected status,
  phase/session identity, current command, and task progress render from
  registered `spec_system_detected`, `spec_session_resolved`, and
  `task_progress` payloads; covered by tests.)
- [x] Verify all text fits at minimum and common desktop sizes.
  (2026-07-09: window enforces 980x620 minimum; layouts use elide, wrap,
  and bounded panel widths; screenshot smokes at the default viewport for
  high/balanced/low/plain themes pass the nonblank multi-color check.
  Manual spot-check on real desktops remains part of the clean-machine
  session.)

## Profile Drawer And Persistence Remaining Work

Drawer parity completed 2026-07-09 per ADR 0001 #3: the PROFILES section of
`SettingsDrawer.qml` now exposes load, save, delete, duplicate, rename,
reset-built-in, import, and export; the bridge gained `renameProfile` and
`resetProfile` slots. Tests: `tests/test_hyperterminal_bridge.py` profile
suite.

- [x] Expose profile import in the QML settings drawer.
- [x] Expose profile export in the QML settings drawer.
- [x] Expose profile duplicate in the QML settings drawer.
- [x] Expose profile rename in the QML settings drawer.
- [x] Expose reset-to-built-in/defaults in the QML settings drawer.
- [x] Show visible validation errors for invalid profile JSON
  (`profileError` text in the drawer; invalid JSON never touches shared
  CLI config; schema/version validation and secret rejection live in
  `profile_store.py`; profile names remain ASCII-only).
- [ ] Confirm the drawer can cover all release-required profile dimensions.
  - Theme family.
  - Rendering mode.
  - Quality tier.
  - Effect intensity.
  - Font family, scale, width, and line spacing.
  - Reduced effects.
  - Plain fallback.
  - Save, duplicate, rename, delete custom, reset built-in, import, and export
    if those operations stay in release scope.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/SettingsWindow.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/SettingsGeneralTab.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/SettingsTerminalTab.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/SettingsEffectsTab.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/SettingsAdvancedTab.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/ApplicationSettings.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/fontmanager.cpp`.
- [ ] Preserve the planned wrapper storage boundary.
  - Wrapper-only visual profiles:
    `${XDG_CONFIG_HOME:-~/.config}/apex-infinite/visual-profiles.json`
  - Runtime window state:
    `${XDG_STATE_HOME:-~/.local/state}/apex-infinite/visual-state.json`
  - Shared CLI config writes require explicit user confirmation.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/Storage.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/ApplicationSettings.qml`.
- [ ] Preserve the profile schema coverage for any new UI or migration work.
  - Top-level fields: `version`, `name`, `theme_name`, `rendering_mode`,
    `quality_tier`, `effect_intensity`, `font_family`, `font_scale`,
    `font_width`, `line_spacing`, `reduced_effects`, `plain_fallback`.
  - `effects` fields: `glow`, `scanlines`, `flicker`, `curvature`, `bloom`,
    `persistence`, `noise`, `jitter`, `sync`, `chroma`, `ambient_frame`.
  - `layout` fields: density, side rail position, event row height, pinned
    panels.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/ApplicationSettings.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/SettingsTerminalTab.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/SettingsEffectsTab.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/fontmanager.cpp`.

## Graphical First-Run Remaining Work

Implemented 2026-07-09. The first-run panel (`FirstRunBanner.qml`, shown in
the main shell when the shared resolver reports no user-owned config) offers
provider choice (Ollama/OpenAI/Grok), model, Codex binary, projects dir and
default project entry, shows the autonomy warning + summary + Codex flag
state, links Doctor, defaults the first launch to dry-run, and writes shared
config only after an explicit confirmation toggle plus button click. Writes
go through the same `setup_config.write_shared_config` backend as the
terminal `--setup` command (atomic, backup, 0600). Tests:
`tests/test_hyperterminal_bridge.py` first-run/writeSharedConfig suite.

- [x] Build the full graphical first-run shared-config flow.
- [x] Keep the first-run flow inside the same high-design command shell
  (panel within the shell, not a separate wizard window).
- [x] Preserve the wrapper boundary during first-run work (the wrapper only
  writes shared config on explicit confirmation and owns no workflow
  decisions; the write emits a synthetic registered `config_resolved`
  event).
- [ ] Verify a clean Linux user can launch the visual app, configure it, run
  doctor, and start a dry run without editing source files.
  (Needs a clean-machine session; commands documented in
  `packaging/RELEASE-CHECKLIST.md`.)
- [x] Verify the user can see why live mode is risky before starting it
  (autonomy warning text in the first-run panel plus the always-visible
  autonomy summary in the command strip; live mode renders in warning
  color).

## Event Boundary Remaining Work

Updated 2026-07-09. New facts added this pass: `config_resolved` (now
emitted by the CLI with path + source category), `privacy_notice_shown`,
and `history_purged`.

- [x] Add new registered events for the facts needed by this pass
  (`config_resolved` emission, `privacy_notice_shown`, `history_purged`).
- [x] Keep every new event registered in `src/apex_infinite/events.py`.
- [x] Add file-stream coverage for every new event
  (`tests/test_config_resolution.py`, `tests/test_privacy_and_retention.py`).
- [x] Add stdout-machine-output coverage for every new event.
  (`config_resolved` and `history_purged` covered in both modes;
  `privacy_notice_shown` is intentionally absent in machine mode because
  the notice is human-surface-only - the wrapper owns its own notice UI -
  and a test asserts that suppression.)
- [x] Keep event payloads factual, not visual (unchanged validators).
- [x] Reject or suppress secrets, ANSI escapes, Rich markup, frame glyphs,
  copied reference identifiers, renderer snapshots, and visual token values
  in event payloads (unchanged validators cover the new events).
- [x] Use registered events instead of parsing human terminal output
  whenever the wrapper needs more state (wrapper config writes ingest a
  synthetic registered `config_resolved`; resume uses wrapper-owned state,
  not output parsing).

## Logging And Observability Remaining Work

Completed 2026-07-09 per ADR 0001 #11.

- [x] Make logging a high quality product surface. (The durable per-run log
  is the full registered JSONL event stream: structured, timestamped,
  greppable, and exportable; it carries startup, config resolution,
  provider checks, manager decisions, Codex subprocess activity, DB log
  writes, stderr summaries, operator stop, and final outcome. Payload
  safety is enforced by the event schema validators - no secrets, ANSI,
  Rich markup, frame glyphs, or theme tokens. `structlog` diagnostics and
  `write_last_error` remain for wrapper-internal errors.)
- [x] Make full logging the default for the visual app's real CLI path.
  (Every `--launch-cli` run tees its JSONL event stream to
  `${XDG_STATE_HOME:-~/.local/state}/apex-infinite/logs/run-<utc>.jsonl`
  with no extra flags; `--reduced-logging` opts out; `--run-log-dir`
  overrides the location. Retention is until the operator deletes the
  files; the log directory and cleanup are documented in
  `docs/operator-runbook.md` and README.)

## Security And Privacy Productization Remaining Work

Completed 2026-07-09; details recorded in `docs/SECURITY-COMPLIANCE.md`
(P00-S01 through P00-S04 resolved).

- [x] Add local history purge behavior: `apex-infinite --purge-history`
  (all projects or one via `--path`, confirmation-gated, `--yes` for
  scripts, emits the registered `history_purged` event). Retention is
  documented as indefinite-until-purged.
- [x] Add a first-run privacy notice before local history storage and
  provider-bound prompt transfer (`src/apex_infinite/privacy.py`; one-time
  marker under `${XDG_STATE_HOME:-~/.local/state}/apex-infinite/`; emits
  the registered `privacy_notice_shown` event; suppressed in machine mode
  by design because the wrapper owns its own notice UI).
- [x] Document provider-bound prompt traffic (README Data section and the
  first-run notice).
- [x] Warn operators not to include secrets, personal data, or customer
  data in prompts or target-project outputs (README + notice).
- [x] Add recurring CI vulnerability scanning for base, dev, and visual
  dependency lanes (`.github/workflows/security-scan.yml`: weekly schedule,
  dependency-change pushes, manual dispatch).

## Shader Remaining Work

- [ ] Promote shader mode only after deciding it is in release scope.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/ShaderTerminal.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/shaders/`.
- [ ] If promoted, wire reviewed compiled shader modules into the QML render
  path.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/ShaderTerminal.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/resources.qrc`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/shaders/`.
- [ ] If promoted, add the required compiled shader artifacts to package data.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/resources.qrc`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/shaders/`.
- [ ] If promoted, keep shader artifacts derived only from Apex-owned source.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/shaders/`.
- [ ] If promoted, document generated shader artifact review before release.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/shaders/`.
- [ ] If promoted, implement or wire the full clean-room shader layer.
  - Original postprocess shader for curvature and glass treatment.
  - Original bloom/glow composition.
  - Original procedural noise field.
  - Original chroma/subpixel edge treatment.
  - Original persistence buffer for event-row trails.
  - Original line jitter and sync distortion with bounded intensity.
  - Optional frame/glass treatment behind capability and reduced-effects gates.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/ShaderTerminal.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/BurnInEffect.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/TerminalFrame.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/shaders/terminal_dynamic.frag`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/shaders/terminal_static.frag`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/shaders/terminal_frame.frag`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/shaders/burn_in.frag`.
- [ ] If promoted, use a typed render-state object derived from profiles,
  capability detection, and workflow events.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/ApplicationSettings.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/ShaderTerminal.qml`.
- [ ] If promoted, separate dynamic event-row effects from final presentation
  composition.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/ShaderTerminal.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/BurnInEffect.qml`.
- [ ] If promoted, keep stable texture sizing for event panels and effect
  buffers.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/ShaderTerminal.qml`.
- [ ] If promoted, keep effect intensity separate from render cost.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/ApplicationSettings.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/SettingsEffectsTab.qml`.
- [ ] If promoted, preserve quality-tier frame pacing for Cinematic, Balanced,
  Battery, Low Effects, and Plain.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/ApplicationSettings.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/TimeManager.qml`.
- [ ] If promoted, verify shader mode is visually richer than QML-only mode.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/ShaderTerminal.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/PreprocessedTerminal.qml`.
- [ ] If promoted, verify unsupported graphics environments fall back
  automatically.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/ShaderTerminal.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/PreprocessedTerminal.qml`.
- [ ] If promoted, verify chroma/subpixel effects are optional, bounded, and
  disabled in reduced/plain modes.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/ShaderTerminal.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/SettingsTerminalTab.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/shaders/terminal_dynamic.frag`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/shaders/terminal_static.frag`.
- [ ] If promoted, verify persistence resets cleanly on profile, font, and
  quality changes.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/BurnInEffect.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/ApplicationSettings.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/fontmanager.cpp`.
- [ ] If shader mode is deferred, keep release wording explicit that QML-only
  source mode is the shipped visual path.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/PreprocessedTerminal.qml`.

## Event-Reactive Effects Remaining Verification

Verified 2026-07-09 through unit tests on the pulse pipeline
(`tests/test_visual_state.py`, `tests/test_hyperterminal_bridge.py`) and
the QML dispatch in `effects/EffectSurface.qml`, which routes every pulse
name to a distinct visual treatment.

- [x] Verify run start creates a short surface charge (`surface_charge`).
- [x] Verify provider preflight success sends a low-intensity signal sweep
  (`signal_sweep`).
- [x] Verify provider preflight failure creates a visible red fault lock
  (`fault_lock`; also raised by codex flag-check failure).
- [x] Verify new manager decisions pulse around the decision panel
  (`decision_pulse`).
- [x] Verify new iterations add a soft persistence trail to the event core
  (`persistence_trail`).
- [x] Verify operator stop drains glow immediately and freezes final state
  (`glow_drain` on operator stop; store stops mutating after
  `run_stopped`).
- [x] Verify successful completion performs a restrained completion sweep
  (`completion_sweep`).
- [x] Verify non-zero exit, stderr, malformed JSONL, and timeout use a
  distinct error signature (`error_signature` + failed run health; each
  error kind carries its own typed row).
- [x] Verify effects bind to run state, event severity, spec-map progress,
  provider health, autonomy policy, config source, and doctor results
  (pulses bind to run lifecycle and severity; spec progress, provider
  health, autonomy policy, config source, and doctor results drive their
  typed panels and severity coloring from registered events).

## Desktop And AppImage Remaining Work

- [ ] Build and inspect an AppImage release candidate.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/scripts/build-appimage.sh`.
- [ ] Use this artifact name unless the release session explicitly changes it:
  `apex-infinite-visual-linux-x86_64.AppImage`.
- [ ] Evaluate `pyside6-deploy` first for the packaging path.
- [ ] Use direct Nuitka or another packaging path only after documenting why it
  is better for this app.
- [ ] Validate desktop metadata with `desktop-file-validate`.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/cool-retro-term.desktop`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/packaging/rpm/cool-retro-term.spec`.
- [ ] Validate AppStream metadata with `appstreamcli validate`.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/packaging/appdata/cool-retro-term.appdata.xml`.
- [ ] Do not commit generated packaging output unless a release session
  explicitly scopes it.
- [ ] Verify the desktop launcher opens the visual app from an installed build.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/cool-retro-term.desktop`.
- [ ] Confirm desktop launches reach the visual app, not a terminal-only
  process.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/cool-retro-term.desktop`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/main.cpp`.
- [ ] Verify launcher command coverage for source install and AppImage.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/cool-retro-term.desktop`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/cool-retro-term.pro`.
- [ ] Verify launcher action for a new visual run.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/cool-retro-term.desktop`.
- [ ] Verify launcher action for doctor.
- [ ] Verify launcher action for safe dry run when feasible.
- [ ] Confirm command-line project and start-command overrides still work in
  the packaged app.
- [ ] Verify source install on a clean Linux environment.
- [ ] Verify visual extra install on a clean Linux environment.
- [ ] Verify AppImage launch on a clean Linux environment.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/scripts/build-appimage.sh`.
- [ ] Verify the AppImage does not depend on the source checkout or repo
  `.venv`.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/scripts/build-appimage.sh`.
- [ ] Confirm the packaged app launches without relying on this source checkout
  or repo `.venv`.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/scripts/build-appimage.sh`.
- [ ] Verify missing Codex or provider config produces a visual failure state,
  not a crash.
- [ ] Inspect generated files, collected Qt plugins, Python wheels, and runtime
  dependencies.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/scripts/build-appimage.sh`.
- [ ] Inspect Qt plugins and generated bundle contents.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/scripts/build-appimage.sh`.
- [ ] Inspect bundled QML/PySide resources and avoid missing-plugin runtime
  failures.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/scripts/build-appimage.sh`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/resources.qrc`.
- [ ] Record deterministic build dirs, version labeling, and clean install
  roots.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/scripts/build-appimage.sh`.
- [ ] Record toolchain choices, excluded libraries, Qt plugins, graphics
  backends, and desktop integration dependencies.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/scripts/build-appimage.sh`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/cool-retro-term.pro`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/app.pro`.
- [ ] Publish or record the SHA256 checksum.
- [ ] Generate and publish
  `apex-infinite-visual-linux-x86_64.AppImage.sha256`.
- [ ] Verify the checksum with `sha256sum -c`.
- [ ] Record the dependency inventory.
- [ ] Record Qt/PySide6 notices.
- [ ] Record source/relink or replacement instructions if required by the
  chosen license path.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/packaging/debian/copyright`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/gpl-3.0.txt`.
- [ ] Record clean-machine verification evidence.
- [ ] Document source install, AppImage invocation, profile selection, doctor,
  dry-run, live-run, and workdir/project path flags.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/scripts/build-appimage.sh`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/cool-retro-term.desktop`.
- [ ] Publish source/dev install instructions alongside the binary.

## Clean-Room And License Remaining Work

- [ ] Confirm no tracked path starts with `EXAMPLE/`.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/`.
- [ ] Confirm no reference QML, shader, generated shader blob, image, icon,
  font, profile, manifest, build script, terminal-widget material, names,
  colors, formulas, constants, or profile JSON is copied.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/shaders/`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/images/`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/icons/`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/fonts/`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/qmltermwidget/`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/cool-retro-term.desktop`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/scripts/build-appimage.sh`.
- [ ] Confirm no generated `.qsb` file from the reference tree is reused.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/shaders/`.
- [ ] Confirm no reference images, icons, fonts, manifests, or package metadata
  are reused.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/images/`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/icons/`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/fonts/`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/cool-retro-term.desktop`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/packaging/appdata/cool-retro-term.appdata.xml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/packaging/debian/control`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/packaging/rpm/cool-retro-term.spec`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/snap/snapcraft.yaml`.
- [ ] Confirm `qmltermwidget`, QTermWidget, terminal-emulator code, and related
  terminal-widget dependencies are not vendored.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/qmltermwidget/`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/.gitmodules`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/PreprocessedTerminal.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/main.cpp`.
- [ ] Confirm no GPL-only Qt modules are bundled.
- [ ] Confirm the Qt for Python license path.
- [ ] Review the concrete AppImage bundle against the selected Qt for Python
  license path: LGPLv3-compatible or commercial.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/scripts/build-appimage.sh`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/packaging/debian/copyright`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/gpl-3.0.txt`.
- [ ] Confirm AppImage replacement or relink obligations.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/scripts/build-appimage.sh`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/packaging/debian/copyright`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/gpl-3.0.txt`.
- [ ] Verify source availability or relink/replacement instructions against the
  concrete artifact.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/scripts/build-appimage.sh`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/packaging/debian/copyright`.
- [ ] Include notices and dependency inventory in release artifacts.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/packaging/debian/copyright`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/gpl-2.0.txt`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/gpl-3.0.txt`.
- [ ] Verify `packaging/NOTICES.md` matches the generated dependency inventory.
- [ ] Produce and archive a dependency inventory for Python wheels, Qt
  libraries, Qt plugins, and AppImage runtime components.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/scripts/build-appimage.sh`.
- [ ] Verify generated shader artifacts are derived from Apex-owned source if
  shader artifacts are released.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/shaders/`.
- [ ] Verify original icon and visual assets have documented provenance.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/icons/`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/images/`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/fonts/`.
- [ ] Run clean-room text scans for suspicious reference names where feasible.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/`.
- [ ] Keep the base CLI free of Qt, PySide6, PyQt, pywebview, xterm.js,
  qmltermwidget, QTermWidget, copied terminal emulators, shaders, fonts, images,
  icons, and graphical startup checks.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/shaders/`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/fonts/`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/qmltermwidget/`.
- [ ] Block binary release if license, notice, checksum, dependency inventory,
  source/relink, or clean-room evidence is incomplete.

## Terminal CLI Remaining Work

- [x] Confirm whether the terminal CLI polish pass is complete. (Complete,
  ADR 0001 #4; the conditional polish items below are closed with it.)
- [x] Preserve plain ASCII-safe output for redirected logs and
  machine-unfriendly terminals (unchanged; suite passes).
- [x] Preserve redirected output cleanliness (unchanged; suite passes).
- [x] Preserve `--event-stream - --machine-output` as JSONL-only
  (unchanged; new doctor/purge paths covered by machine-output tests).
- [x] Preserve the rule that no shader, image, GUI, QML, or PySide
  dependency enters the base terminal CLI path (new modules
  `config_resolution.py`, `doctor.py`, `setup_config.py`, `privacy.py` are
  stdlib/yaml only; verified by the base-install isolation gate).
- [x] Do not introduce an ANSI scrape contract, copied retro profiles,
  graphical dependencies, a terminal-emulator widget, or duplicated event
  state that belongs in the workflow engine (none introduced).

## Terminal Install And Packaging Remaining Work

Documentation completed 2026-07-09 in `docs/terminal-install.md`;
verification items are tracked in the Final Verification Matrix.

- [ ] Verify base terminal installation from a built wheel in a clean venv.
- [ ] Verify base terminal installation from a built sdist in a clean venv.
- [ ] Verify the base install does not install PySide6, Nuitka, QML assets,
  or require a display server.
- [x] Document `pipx install .` from the repo root, including the expected
  `apex-infinite` command path.
- [x] Document installing from generated wheel and sdist artifacts.
- [x] Document a local installer path that creates a dedicated venv and
  exposes `apex-infinite` on the operator's shell path.
- [x] Document terminal install verification commands:
  `apex-infinite --version`, `--help`, `--doctor`, `--check-provider`.
- [x] Document uninstall and upgrade behavior for pipx and local-venv
  installs (plus data cleanup).
- [ ] Record clean Linux evidence that `apex-infinite` resolves from the
  shell without activating this repo's `.venv`. (Needs a clean machine.)

## Terminal Setup And Shared Config Remaining Work

- [x] Add a terminal first-run setup command. (2026-07-09:
  `apex-infinite --setup` prompts for provider, model, Codex binary, exec
  flags with an explicit autonomy warning, reasoning effort, default
  projects directory, and optional default target project. Backend:
  `src/apex_infinite/setup_config.py`; tests:
  `tests/test_setup_command.py`.)
- [x] Write shared CLI config to
  `${XDG_CONFIG_HOME:-~/.config}/apex-infinite/config.yaml`.
- [x] Write config atomically (temp file + `os.replace`).
- [x] Preserve a backup when overwriting existing user config
  (`config.yaml.bak-<timestamp>`).
- [x] Set conservative permissions (config 0600, config dir 0700).
- [x] Keep package defaults in `src/apex_infinite/config.yaml`.
- [x] Add a non-interactive setup mode (`--setup-non-interactive` plus
  `--codex-binary`, `--codex-exec-flags`, `--reasoning-effort`,
  `--projects-dir`, `--default-project`) that validates flags before
  writing.
- [x] Ensure missing secrets are referenced through environment variables,
  not written into config by default (placeholders like
  `${OPENAI_API_KEY}`; setup warns when the env var is unset).
- [x] Make setup idempotent and prevent silent loss of existing config.
- [x] Implement shared config precedence. (2026-07-09:
  `src/apex_infinite/config_resolution.py`; order: `--config` >
  `APEX_INFINITE_CONFIG` > XDG > `./config.yaml` > source-root > packaged.)
- [x] Add `APEX_INFINITE_CONFIG`. (Returned even when missing so config
  loading fails fast with a clear error.)
- [x] Add XDG config lookup using `XDG_CONFIG_HOME` when set.
- [x] Retain local config compatibility while adding the new precedence chain.
- [x] Centralize config resolution so the terminal CLI, visual wrapper, setup,
  and doctor use the same resolver. (Terminal CLI, visual doctor, and
  first-run detection now import `apex_infinite.config_resolution`.)
- [x] Emit a non-secret `config_resolved` event with the resolved path and
  source category. (Emitted before `config_loaded`.)
- [x] Show the resolved config file and source category in startup output.
  (`StartupSnapshot.config_source` renders in the operator console.)
- [x] Update visual doctor and first-run detection to use the shared resolver.
- [x] Add tests for every config precedence path and malformed selected
  config. (`tests/test_config_resolution.py`; `load_config` now fails fast on
  malformed YAML, non-mapping config, and missing provider/providers keys.)

## Terminal Doctor Remaining Work

Completed 2026-07-09: `apex-infinite --doctor` (plus `--doctor-visual`,
`--skip-provider-check`, `--check-provider-chat` modifiers) with the shared
backend in `src/apex_infinite/doctor.py`; the visual doctor now reuses it.
Tests: `tests/test_terminal_doctor.py`.

- [x] Add a terminal diagnostic entrypoint using the decided CLI shape
  (`apex-infinite --doctor`, ADR 0001 #5).
- [x] Check Python version.
- [x] Check Codex CLI availability and version (`codex --version` probe).
- [x] Check configured Codex binary path.
- [x] Check `codex exec --help` against configured `codex.exec_flags`,
  including stale or renamed autonomy flags (reuses
  `validate_codex_exec_flags`).
- [x] Check provider name, API key presence, base URL, and model
  availability (reuses `run_provider_preflight`).
- [x] Check optional provider chat completion when requested
  (`--check-provider-chat`).
- [x] Check target project path.
- [x] Check `.spec_system/` presence when a workflow command requires it.
- [x] Check SQLite history DB path and writeability.
- [x] Check event-stream output path when provided.
- [x] Check visual-wrapper dependencies only when requested
  (`--doctor-visual`).
- [x] Print concise pass, warn, and fail rows.
- [x] Exit non-zero for hard blockers.
- [x] Redact secrets from all doctor output and events (key presence only;
  event payloads pass the registered-event secret validators).
- [x] Include exact next commands for common fixes (`fix_hint` per row).

## Launcher And Installed-User Documentation Remaining Work

Completed 2026-07-09.

- [x] Add default project selection from config (`defaults.project` and
  `defaults.projects_dir` written by `--setup`, read by the CLI when
  `--path` is omitted).
- [x] Add a resume-friendly command/documented pattern for the last
  project (bare `apex-infinite` with `defaults.project`; documented in
  `docs/terminal-install.md`; visual command-strip Resume).
- [x] Add shortcuts or aliases for common starts (alias block in
  `docs/terminal-install.md`: dry run, resume, history, provider check,
  plain log mode).
- [x] Ensure install, setup, doctor, and visual onboarding docs steer
  first execution through `--dry-run` (README quick start, setup next
  steps, doctor fix hints, first-run panel default, install guide).
- [x] Add installed-user docs for pipx, wheel, sdist, local venv,
  uninstall, and upgrade flows (`docs/terminal-install.md`).
- [x] Add first-run setup docs (README Configuration + install guide).
- [x] Update config docs for XDG and `APEX_INFINITE_CONFIG` resolution
  (README Configuration, install guide, operator runbook).
- [x] Add terminal doctor docs (README Usage/Options, install guide,
  runbook startup checklist).
- [x] Keep provider setup docs synchronized with setup, config
  resolution, and doctor behavior for Ollama, OpenAI, and Grok (setup
  templates mirror packaged config; README provider docs unchanged and
  consistent).

## Production Hardening Remaining Work

- [ ] Test base terminal install on a clean Linux environment.
- [ ] Test wheel install with a clean venv and clean home directory.
- [ ] Test sdist install with a clean venv and clean home directory.
- [ ] Verify offscreen smoke launch.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/main.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/TerminalWindow.qml`.
- [ ] Verify software backend fallback.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/ShaderTerminal.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/PreprocessedTerminal.qml`.
- [ ] Test no-display or unsupported-display behavior.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/ShaderTerminal.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/PreprocessedTerminal.qml`.
- [ ] Verify desktop screenshot smoke at common viewports.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/TerminalWindow.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/TerminalContainer.qml`.
- [ ] Run and archive screenshot smoke evidence for high, balanced, low, and
  plain profiles.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/ApplicationSettings.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/SettingsEffectsTab.qml`.
- [ ] Verify reduced-effects and plain fallback screenshots are readable and
  nonblank.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/PreprocessedTerminal.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/ShaderTerminal.qml`.
- [ ] Verify pixel-level nonblank checks for effect surfaces.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/ShaderTerminal.qml`.
- [ ] Verify no-overlap checks for all built-in profiles.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/ApplicationSettings.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/TerminalContainer.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/SettingsWindow.qml`.
- [ ] Verify long-run memory behavior.
- [ ] Verify reduced-effects behavior.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/SettingsEffectsTab.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/PreprocessedTerminal.qml`.
- [ ] Verify plain fallback behavior.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/PreprocessedTerminal.qml`.
- [ ] Verify low-effects and plain modes are intentionally designed, not broken
  versions of the high-effects mode.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/SettingsEffectsTab.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/PreprocessedTerminal.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/ShaderTerminal.qml`.
- [ ] Verify the app visibly changes between rendering modes.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/SettingsTerminalTab.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/ShaderTerminal.qml`.
- [ ] Verify effects react to run lifecycle events.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/ApplicationSettings.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/ShaderTerminal.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/TimeManager.qml`.
- [ ] Verify graphical dependency absence in the base CLI install.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/shaders/`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/qmltermwidget/`.
- [ ] Test Ollama provider path.
- [ ] Test OpenAI or Grok provider path with redacted credentials.
- [ ] Test a real target project with `.spec_system/`.
- [ ] Test a bounded real Codex subprocess path, not only `--dry-run`.
- [ ] Test `--check-provider` with file event streams and stdout
  machine-output streams in the clean environment.
- [ ] Test history lookup path normalization in the clean environment.
- [ ] Test malformed config, missing Codex CLI, missing provider key, missing
  model, invalid project path, and malformed JSONL event handling.
- [ ] Document all clean-machine results and link the evidence from release
  docs.
- [ ] Confirm no successful smoke run emits event-stream schema errors.

## Final Verification Matrix

- [ ] Rerun and record the full pytest suite.
- [ ] Rerun and record `black --check src tests`.
- [ ] Rerun and record `mypy`.
- [ ] Rerun and record `pylint src/apex_infinite src/apex_infinite_visual`.
- [ ] Rerun and record `.venv/bin/python -m pip_audit`.
- [ ] Rerun and record `.venv/bin/python -m build --outdir
  /tmp/apex-infinite-cli-smoke-dist`.
- [ ] Rerun and record QML lint for every QML file.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/`.
- [ ] Resolve or explicitly record any remaining QML lint warnings.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/`.
- [ ] Rerun and record unit tests for visual state transitions.
- [ ] Rerun and record unit tests for profile schema, persistence, import,
  export, migration, and corruption handling.
- [ ] Rerun and record PySide6 import-laziness checks.
- [ ] Rerun and record offscreen source-mode smoke.
- [ ] Rerun and record malformed JSONL checks.
- [ ] Rerun and record stderr and non-zero subprocess checks.
- [ ] Rerun and record missing PySide6 checks.
- [ ] Rerun and record missing Codex binary checks.
- [ ] Rerun and record missing provider config checks.
- [ ] Rerun and record clean base-install checks proving PySide6 is absent.
- [ ] Rerun and record visual extra source-install checks.
- [ ] Rerun and record AppImage clean-machine launch checks.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/scripts/build-appimage.sh`.
- [ ] Rerun and record `git diff --check`.
- [ ] Rerun and record that no `EXAMPLE/` paths are tracked.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/`.
- [ ] Rerun and record that no `.qsb` artifacts are unintentionally tracked.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/shaders/`.
- [ ] Rerun and record license notice and dependency inventory review.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/packaging/debian/copyright`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/gpl-2.0.txt`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/gpl-3.0.txt`.

## Remaining Session Order

- [ ] Close product-scope decisions for resume, shader mode, profile drawer
  parity, and terminal CLI polish.
- [ ] Finish terminal install packaging, terminal setup, shared config, doctor,
  launcher ergonomics, and installed-user docs.
- [ ] Finish privacy, retention, provider-traffic, and vulnerability-scanning
  productization decisions.
- [ ] Finish QML profile drawer parity if required.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/SettingsWindow.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/SettingsGeneralTab.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/ApplicationSettings.qml`.
- [ ] Implement the full graphical first-run shared-config flow.
- [ ] Promote shader mode or explicitly defer it.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/ShaderTerminal.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/shaders/`.
- [ ] Build and inspect the AppImage release candidate.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/scripts/build-appimage.sh`.
- [ ] Run clean-machine release verification and fix blockers.
- [ ] Run the complete final verification matrix and record results.

## Release Completion Blockers

- [ ] Do not claim completion until `apex-infinite-visual` opens as a
  production Linux command surface, not a prototype dashboard.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/main.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/TerminalWindow.qml`.
- [ ] Do not claim completion until the first screen is the usable operator
  terminal.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/main.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/TerminalContainer.qml`.
- [ ] Do not claim completion until visual profiles, rendering modes, quality
  tiers, and effects persist across launches.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/ApplicationSettings.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/Storage.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/SettingsWindow.qml`.
- [ ] Do not claim completion until effects are visually rich, workflow-aware,
  configurable, and bounded by reduced/plain fallbacks.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/SettingsEffectsTab.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/ShaderTerminal.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/PreprocessedTerminal.qml`.
- [ ] Do not claim completion until the wrapper remains event-driven and does
  not parse human terminal output.
- [ ] Do not claim completion until the base terminal CLI remains free of
  graphical dependencies.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/shaders/`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/qmltermwidget/`.
- [ ] Do not claim completion until base terminal installs work from wheel,
  sdist, pipx, and local-venv paths on clean Linux without this repo `.venv`.
- [ ] Do not claim completion until terminal first-run setup, shared config
  resolution, and terminal doctor are implemented or explicitly deferred with
  release-facing docs.
- [ ] Do not claim completion until the visual app supports first-run setup,
  doctor, dry-run, live-run, stop, and resume-facing workflows or the resume
  scope is explicitly removed.
- [ ] Do not claim completion until the desktop launcher and AppImage work on a
  clean supported Linux machine.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/cool-retro-term.desktop`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/scripts/build-appimage.sh`.
- [ ] Do not claim completion until release artifacts include original assets,
  notices, dependency inventory, and checksums.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/icons/`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/images/`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/packaging/debian/copyright`.
- [ ] Do not claim completion until clean-room evidence proves the `EXAMPLE/`
  tree was used only for conceptual study.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/`.
- [ ] Do not claim completion until terminal CLI polish is implemented or
  explicitly closed without compromising machine-output or plain-output
  contracts.
- [ ] Do not claim completion until local history retention/privacy behavior,
  provider prompt-transfer disclosure, and dependency vulnerability scanning are
  implemented or explicitly accepted as release risks.
