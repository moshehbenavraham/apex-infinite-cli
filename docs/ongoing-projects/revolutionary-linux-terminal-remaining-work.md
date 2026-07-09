# Revolutionary Linux Terminal Remaining Work

This is the standalone remaining-work tracker for Apex Infinite terminal and
Linux visual productization as of the 2026-07-09 audit. It intentionally lists
only open decisions, unfinished work, release gates, and verification still
needed.

Inline `Reference:` bullets identify matching `cool-retro-term` example paths
for conceptual review and clean-room audit only. Do not copy from them, reuse
assets, or make runtime behavior depend on the `EXAMPLE/` tree.

## Open Product Decisions

- [ ] Decide whether command-strip resume is required for release.
  - If yes, implement it as a first-class command-strip action alongside start,
    stop, dry-run/live-run, max iteration, project path, and doctor controls.
  - If no, remove resume from final acceptance language and any release-facing
    workflow claims.
- [ ] Decide whether shader mode is in scope for the source-mode visual
  release.
  - If yes, promote reviewed compiled shader modules into the QML render path
    and package data.
  - If no, keep compiled `.qsb` files ignored and document shader mode as
    deferred.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/ShaderTerminal.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/shaders/`.
- [ ] Decide whether the QML profile drawer must expose every backend profile
  operation before release.
  - If yes, add import, export, duplicate, rename, reset, and validation UI.
  - If no, document which operations are backend or bridge-only.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/SettingsWindow.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/SettingsGeneralTab.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/ApplicationSettings.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/Storage.qml`.
- [ ] Decide whether Workstream 8 terminal CLI polish is complete or still
  needs implementation beyond autonomy-summary and event-boundary updates.
- [ ] For any remaining visual feature that needs new workflow state, decide
  whether to add a registered event instead of adding wrapper assumptions.
- [ ] Decide the terminal doctor entrypoint shape before release.
  - If the root command remains a single Click command, expose doctor as
    `apex-infinite --doctor`.
  - If the CLI becomes a Click group, preserve existing root flags and expose
    doctor as `apex-infinite doctor`.
- [ ] Decide whether the terminal doctor and
  `src/apex_infinite_visual/doctor.py` share a diagnostic backend.
- [ ] Define whether cwd `.env` or config-directory `.env` has precedence, then
  test the selected behavior.
- [ ] Decide the release policy for broad Codex bypass behavior: explicit
  opt-in, narrower default permissions, or accepted-risk documentation.
- [ ] Document public package publishing and rollback policy, or record that it
  remains external/manual.
- [ ] Decide whether to add `docs/CODEOWNERS`; ownership is still an
  organizational decision.

## Visual App Remaining Work

- [ ] Implement command-strip resume if it remains in scope.
  - Resume must be visible without opening docs.
  - Resume must not cause controls to shift or overlap during runs.
  - Resume-facing behavior must remain event-driven and must not scrape Rich,
    ANSI, plain terminal text, SQLite history rows, or terminal-control output.
- [ ] Recheck the first viewport against the final product acceptance language.
  - It must be the usable operator terminal, not a landing page, marketing
    hero, or explanatory screen.
  - It must expose dry-run, live-run, stop, resume if scoped, doctor, config,
    provider, model, project path, and run risk state.
  - Errors must be impossible to miss and easy to diagnose.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/main.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/TerminalWindow.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/TerminalContainer.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/TerminalTabs.qml`.
- [ ] Recheck the command strip details before release.
  - Project path selector.
  - Start command selector.
  - Dry-run/live-run segmented control.
  - Max iteration stepper.
  - Start, stop, resume if scoped, and doctor buttons.
  - Autonomy summary with supported Codex flags and current risk level.
- [ ] Recheck mission-state and launch-readiness details before release.
  - Current run status, stage, iteration, provider, model, Codex binary, config
    source, event stream mode, and history DB status must stay visible.
  - Missing provider, Codex, model, project, and config failures must be
    actionable instead of crash states.
- [ ] Recheck event-core and signal-panel behavior before release.
  - Event rows must remain structured, virtualized, and typed by severity,
    stage, and timestamp.
  - Startup, provider preflight, manager decision, command, response, pause,
    error, stop, completion, and summary rows must remain readable.
  - Search, filter, pin, copy, export, pinned error summary, malformed event
    count, recent stderr summary, runtime duration, last machine event, and
    safe artifact links must remain usable.
- [ ] Recheck spec-map behavior before release.
  - Detected `.spec_system/` status, phase/session identity when available,
    current command, task checklist progress when available, carry-forward
    warnings, and validation status should remain visible from safe event
    payloads.
- [ ] Verify all text fits at minimum and common desktop sizes.
  - Controls, labels, event rows, pinned panels, status cells, and drawer
    content must not overlap or resize unpredictably during runs.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/Components/SizedLabel.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/SimpleSlider.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/CheckableSlider.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/SizeOverlay.qml`.

## Profile Drawer And Persistence Remaining Work

- [ ] Expose profile import in the QML settings drawer if UI parity is required.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/SettingsGeneralTab.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/fileio.cpp`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/fileio.h`.
- [ ] Expose profile export in the QML settings drawer if UI parity is required.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/SettingsGeneralTab.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/fileio.cpp`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/fileio.h`.
- [ ] Expose profile duplicate in the QML settings drawer if UI parity is
  required.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/SettingsGeneralTab.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/InsertNameDialog.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/ApplicationSettings.qml`.
- [ ] Expose profile rename in the QML settings drawer if UI parity is
  required.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/InsertNameDialog.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/SettingsGeneralTab.qml`.
- [ ] Expose reset-to-built-in/defaults in the QML settings drawer if UI parity
  is required.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/ApplicationSettings.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/SettingsGeneralTab.qml`.
- [ ] Show visible validation errors for invalid profile JSON.
  - Invalid profile JSON must not break or mutate shared CLI config.
  - Import/export must validate schema and version.
  - Import/export must reject secrets and provider credentials.
  - Profile names remain ASCII-only for now, matching repo conventions.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/SettingsGeneralTab.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/ApplicationSettings.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/fileio.cpp`.
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

- [ ] Build the full graphical first-run shared-config flow.
  - Detect missing shared CLI config.
  - Show provider choices: Ollama, OpenAI, Grok.
  - Let the user enter or confirm model.
  - Let the user select Codex binary.
  - Show detected Codex flag compatibility.
  - Show the same Codex autonomy summary as the terminal CLI before real runs.
  - Let the user choose projects directory and target project.
  - Run doctor.
  - Show pass, warn, fail results.
  - Offer dry-run as the default first launch.
  - Require explicit confirmation before writing shared CLI config.
  - Make config writes recoverable and aligned with the terminal setup command.
- [ ] Keep the first-run flow inside the same high-design command shell.
  - Do not create a separate plain wizard that feels like another product.
- [ ] Preserve the wrapper boundary during first-run work.
  - The wrapper may own presentation state, visual preferences, layout state,
    and explicitly confirmed shared config writes.
  - The wrapper must not own workflow decisions.
- [ ] Verify a clean Linux user can launch the visual app, configure it, run
  doctor, and start a dry run without editing source files.
- [ ] Verify the user can see why live mode is risky before starting it.

## Event Boundary Remaining Work

- [ ] Add new registered events for any missing facts needed by the remaining
  visual, first-run, shader, packaging, or terminal-polish work.
- [ ] Keep every new event registered in `src/apex_infinite/events.py`.
- [ ] Add file-stream coverage for every new event.
- [ ] Add stdout-machine-output coverage for every new event.
- [ ] Keep event payloads factual, not visual.
- [ ] Reject or suppress secrets, ANSI escapes, Rich markup, frame glyphs,
  copied reference identifiers, renderer snapshots, and visual token values in
  event payloads.
- [ ] Use registered events instead of parsing human terminal output whenever
  the wrapper needs more state.

## Logging And Observability Remaining Work

- [ ] Make logging a very high quality product surface, not a debugging
  afterthought.
  - Logs must be structured, timestamped, searchable, exportable, and useful
    for both operators and future AI agents diagnosing a run.
  - Logs must clearly connect visual events, CLI lifecycle events, provider
    checks, manager decisions, Codex subprocess activity, SQLite history writes,
    stderr summaries, user actions, and final run outcome.
  - Logs must preserve enough detail to reconstruct what happened without
    requiring screenshots or manual terminal transcript copying.
  - Logs must stay safe by default: no provider keys, secrets, ANSI escapes,
    Rich markup, frame glyphs, theme token values, or copied reference
    identifiers.
- [ ] Make full logging the default setting for the visual app and real CLI
  wrapper path.
  - A normal live visual run should produce durable logs without requiring the
    operator to discover and pass extra flags.
  - The default should include the full structured event stream and enough
    diagnostic context for post-run review.
  - Provide an explicit reduced/private logging mode only for operators who
    intentionally want less retained data.
  - Document retention location, export path, privacy boundaries, and cleanup
    or purge behavior before release.

## Security And Privacy Productization Remaining Work

- [ ] Add local history purge, retention, or redaction behavior, or document an
  accepted local-data risk before broader distribution.
- [ ] Add a first-run privacy notice before local history storage and
  provider-bound prompt transfer.
- [ ] Document provider-bound prompt traffic.
  - Recent history, latest agent output, summaries, operator instructions, and
    project paths can be sent to the configured LLM provider.
- [ ] Warn operators not to include secrets, personal data, or customer data in
  prompts or target-project outputs.
- [ ] Add dependency locking or recurring CI/scheduled vulnerability scanning
  for base, dev, and visual dependency lanes.

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

- [ ] Verify run start creates a short surface charge.
- [ ] Verify provider preflight success sends a low-intensity signal sweep.
- [ ] Verify provider preflight failure creates a visible red fault lock.
- [ ] Verify new manager decisions pulse around the decision panel.
- [ ] Verify new iterations add a soft persistence trail to the event core.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/BurnInEffect.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/ShaderTerminal.qml`.
- [ ] Verify operator stop drains glow immediately and freezes final state.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/SettingsEffectsTab.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/ShaderTerminal.qml`.
- [ ] Verify successful completion performs a restrained completion sweep.
- [ ] Verify non-zero exit, stderr, malformed JSONL, and timeout use distinct
  error signatures.
- [ ] Verify effects bind to run state, event severity, spec-map progress,
  provider health, autonomy policy, config source, and doctor results.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/ApplicationSettings.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/ShaderTerminal.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/TimeManager.qml`.

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

- [ ] Confirm whether the terminal CLI polish pass is complete.
- [ ] If not complete, improve Rich status hierarchy with clearer labels and
  compact panels.
- [ ] If not complete, polish terminal themes for `crt-green`, `crt-amber`,
  `ibm-dos`, and `plain`.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/ApplicationSettings.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/SettingsTerminalTab.qml`.
- [ ] If not complete, improve progress summaries for max iterations, active
  command, and current manager decision.
- [ ] If not complete, improve compact progress and diagnostic summaries.
- [ ] Preserve plain ASCII-safe output for redirected logs and
  machine-unfriendly terminals.
- [ ] Preserve redirected output cleanliness.
- [ ] Preserve `--event-stream - --machine-output` as JSONL-only.
- [ ] Preserve the rule that no shader, image, GUI, QML, or PySide dependency
  enters the base terminal CLI path.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/shaders/`.
- [ ] Do not introduce an ANSI scrape contract, copied retro profiles,
  graphical dependencies, a terminal-emulator widget, or duplicated event state
  that belongs in the workflow engine.
  - Reference:
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/ApplicationSettings.qml`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/qmltermwidget/`,
    `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/PreprocessedTerminal.qml`.

## Terminal Install And Packaging Remaining Work

- [ ] Verify base terminal installation from a built wheel in a clean venv.
- [ ] Verify base terminal installation from a built sdist in a clean venv.
- [ ] Verify the base install does not install PySide6, Nuitka, QML assets, or
  require a display server.
- [ ] Document `pipx install .` from the repo root, including the expected
  `apex-infinite` command path.
- [ ] Document installing from generated wheel and sdist artifacts.
- [ ] Add or document a local installer path that creates a dedicated venv and
  exposes `apex-infinite` on the operator's shell path.
- [ ] Document terminal install verification commands:
  `apex-infinite --version`, `apex-infinite --help`, and
  `apex-infinite --check-provider`.
- [ ] Document uninstall and upgrade behavior for pipx and local-venv installs.
- [ ] Record clean Linux evidence that `apex-infinite` resolves from the shell
  without activating this repo's `.venv`.

## Terminal Setup And Shared Config Remaining Work

- [ ] Add a terminal first-run setup command or startup flow.
  - Let the operator choose provider: Ollama, OpenAI, or Grok.
  - Let the operator choose or confirm the model.
  - Let the operator configure the Codex binary path.
  - Let the operator configure Codex exec flags with clear autonomy warnings.
  - Let the operator set a default projects directory.
  - Let the operator optionally set a default target project.
- [ ] Write shared CLI config to
  `${XDG_CONFIG_HOME:-~/.config}/apex-infinite/config.yaml`.
- [ ] Write config atomically.
- [ ] Preserve a backup when overwriting existing user config.
- [ ] Set conservative permissions for config files that may reference secret
  environment variable names.
- [ ] Keep package defaults in `src/apex_infinite/config.yaml`.
- [ ] Add a non-interactive setup mode for scripts that validates flags before
  writing config.
- [ ] Ensure missing secrets are referenced through environment variables, not
  written into config by default.
- [ ] Make setup idempotent and prevent silent loss of existing config.
- [ ] Implement shared config precedence.
  - CLI flags.
  - Explicit `--config`.
  - `APEX_INFINITE_CONFIG`.
  - XDG user config.
  - Local `./config.yaml`.
  - Source-root `config.yaml` for checkout development.
  - Packaged defaults.
- [ ] Add `APEX_INFINITE_CONFIG`.
- [ ] Add XDG config lookup using `XDG_CONFIG_HOME` when set.
- [ ] Retain local config compatibility while adding the new precedence chain.
- [ ] Centralize config resolution so the terminal CLI, visual wrapper, setup,
  and doctor use the same resolver.
- [ ] Emit a non-secret `config_resolved` or equivalent event that includes the
  resolved path and source category.
- [ ] Show the resolved config file and source category in startup output.
- [ ] Update visual doctor and first-run detection to use the shared resolver
  instead of checking only an explicit path or cwd `config.yaml`.
- [ ] Add tests for every config precedence path and malformed selected config.

## Terminal Doctor Remaining Work

- [ ] Add a terminal diagnostic entrypoint using the decided CLI shape.
- [ ] Check Python version.
- [ ] Check Codex CLI availability and version.
- [ ] Check configured Codex binary path.
- [ ] Check `codex exec --help` against configured `codex.exec_flags`,
  including stale or renamed autonomy flags.
- [ ] Check provider name, API key presence, base URL, and model availability.
- [ ] Check optional provider chat completion when requested.
- [ ] Check target project path.
- [ ] Check `.spec_system/` presence when a workflow command requires it.
- [ ] Check SQLite history DB path and writeability.
- [ ] Check event-stream output path when provided.
- [ ] Check visual-wrapper dependencies only when requested.
- [ ] Print concise pass, warn, and fail rows.
- [ ] Exit non-zero for hard blockers.
- [ ] Redact secrets from all doctor output and events.
- [ ] Include exact next commands for common fixes.

## Launcher And Installed-User Documentation Remaining Work

- [ ] Add default project selection from config.
- [ ] Add a resume-friendly command or documented pattern for the last project.
- [ ] Add shortcuts or aliases for common starts: dry run, resume, history,
  provider check, and plain log mode.
- [ ] Ensure install, setup, doctor, and visual onboarding docs steer first
  execution through `--dry-run`.
- [ ] Add installed-user docs for pipx, wheel, sdist, local venv, uninstall, and
  upgrade flows.
- [ ] Add first-run setup docs after the setup command exists.
- [ ] Update config docs after XDG and `APEX_INFINITE_CONFIG` resolution exist.
- [ ] Add terminal doctor docs after the doctor entrypoint exists.
- [ ] Keep provider setup docs synchronized with setup, config resolution, and
  doctor behavior for Ollama, OpenAI, and Grok.

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
