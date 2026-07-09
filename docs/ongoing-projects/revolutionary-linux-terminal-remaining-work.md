# Revolutionary Linux Terminal Remaining Work

This is the standalone remaining-work tracker for the Apex Infinite
Hyperterminal visual release as of the 2026-07-09 audit. It intentionally lists
only open decisions, unfinished work, release gates, and verification still
needed.

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
- [ ] Decide whether the QML profile drawer must expose every backend profile
  operation before release.
  - If yes, add import, export, duplicate, rename, reset, and validation UI.
  - If no, document which operations are backend or bridge-only.
- [ ] Decide whether Workstream 8 terminal CLI polish is complete or still
  needs implementation beyond autonomy-summary and event-boundary updates.
- [ ] For any remaining visual feature that needs new workflow state, decide
  whether to add a registered event instead of adding wrapper assumptions.

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

## Profile Drawer And Persistence Remaining Work

- [ ] Expose profile import in the QML settings drawer if UI parity is required.
- [ ] Expose profile export in the QML settings drawer if UI parity is required.
- [ ] Expose profile duplicate in the QML settings drawer if UI parity is
  required.
- [ ] Expose profile rename in the QML settings drawer if UI parity is
  required.
- [ ] Expose reset-to-built-in/defaults in the QML settings drawer if UI parity
  is required.
- [ ] Show visible validation errors for invalid profile JSON.
  - Invalid profile JSON must not break or mutate shared CLI config.
  - Import/export must validate schema and version.
  - Import/export must reject secrets and provider credentials.
  - Profile names remain ASCII-only for now, matching repo conventions.
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
- [ ] Preserve the planned wrapper storage boundary.
  - Wrapper-only visual profiles:
    `${XDG_CONFIG_HOME:-~/.config}/apex-infinite/visual-profiles.json`
  - Runtime window state:
    `${XDG_STATE_HOME:-~/.local/state}/apex-infinite/visual-state.json`
  - Shared CLI config writes require explicit user confirmation.
- [ ] Preserve the profile schema coverage for any new UI or migration work.
  - Top-level fields: `version`, `name`, `theme_name`, `rendering_mode`,
    `quality_tier`, `effect_intensity`, `font_family`, `font_scale`,
    `font_width`, `line_spacing`, `reduced_effects`, `plain_fallback`.
  - `effects` fields: `glow`, `scanlines`, `flicker`, `curvature`, `bloom`,
    `persistence`, `noise`, `jitter`, `sync`, `chroma`, `ambient_frame`.
  - `layout` fields: density, side rail position, event row height, pinned
    panels.

## Graphical First-Run Remaining Work

- [ ] Build the full graphical first-run shared-config flow.
  - Detect missing shared CLI config.
  - Show provider choices: Ollama, OpenAI, Grok.
  - Let the user enter or confirm model.
  - Let the user select Codex binary.
  - Show detected Codex flag compatibility.
  - Let the user choose projects directory and target project.
  - Run doctor.
  - Show pass, warn, fail results.
  - Offer dry-run as the default first launch.
  - Require explicit confirmation before writing shared CLI config.
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

## Shader Remaining Work

- [ ] Promote shader mode only after deciding it is in release scope.
- [ ] If promoted, wire reviewed compiled shader modules into the QML render
  path.
- [ ] If promoted, add the required compiled shader artifacts to package data.
- [ ] If promoted, keep shader artifacts derived only from Apex-owned source.
- [ ] If promoted, document generated shader artifact review before release.
- [ ] If promoted, implement or wire the full clean-room shader layer.
  - Original postprocess shader for curvature and glass treatment.
  - Original bloom/glow composition.
  - Original procedural noise field.
  - Original chroma/subpixel edge treatment.
  - Original persistence buffer for event-row trails.
  - Original line jitter and sync distortion with bounded intensity.
  - Optional frame/glass treatment behind capability and reduced-effects gates.
- [ ] If promoted, use a typed render-state object derived from profiles,
  capability detection, and workflow events.
- [ ] If promoted, separate dynamic event-row effects from final presentation
  composition.
- [ ] If promoted, keep stable texture sizing for event panels and effect
  buffers.
- [ ] If promoted, keep effect intensity separate from render cost.
- [ ] If promoted, preserve quality-tier frame pacing for Cinematic, Balanced,
  Battery, Low Effects, and Plain.
- [ ] If promoted, verify shader mode is visually richer than QML-only mode.
- [ ] If promoted, verify unsupported graphics environments fall back
  automatically.
- [ ] If promoted, verify chroma/subpixel effects are optional, bounded, and
  disabled in reduced/plain modes.
- [ ] If promoted, verify persistence resets cleanly on profile, font, and
  quality changes.
- [ ] If shader mode is deferred, keep release wording explicit that QML-only
  source mode is the shipped visual path.

## Event-Reactive Effects Remaining Verification

- [ ] Verify run start creates a short surface charge.
- [ ] Verify provider preflight success sends a low-intensity signal sweep.
- [ ] Verify provider preflight failure creates a visible red fault lock.
- [ ] Verify new manager decisions pulse around the decision panel.
- [ ] Verify new iterations add a soft persistence trail to the event core.
- [ ] Verify operator stop drains glow immediately and freezes final state.
- [ ] Verify successful completion performs a restrained completion sweep.
- [ ] Verify non-zero exit, stderr, malformed JSONL, and timeout use distinct
  error signatures.
- [ ] Verify effects bind to run state, event severity, spec-map progress,
  provider health, autonomy policy, config source, and doctor results.

## Desktop And AppImage Remaining Work

- [ ] Build and inspect an AppImage release candidate.
- [ ] Use this artifact name unless the release session explicitly changes it:
  `apex-infinite-visual-linux-x86_64.AppImage`.
- [ ] Evaluate `pyside6-deploy` first for the packaging path.
- [ ] Use direct Nuitka or another packaging path only after documenting why it
  is better for this app.
- [ ] Do not commit generated packaging output unless a release session
  explicitly scopes it.
- [ ] Verify the desktop launcher opens the visual app from an installed build.
- [ ] Verify launcher command coverage for source install and AppImage.
- [ ] Verify launcher action for a new visual run.
- [ ] Verify launcher action for doctor.
- [ ] Verify launcher action for safe dry run when feasible.
- [ ] Verify source install on a clean Linux environment.
- [ ] Verify visual extra install on a clean Linux environment.
- [ ] Verify AppImage launch on a clean Linux environment.
- [ ] Verify the AppImage does not depend on the source checkout or repo
  `.venv`.
- [ ] Verify missing Codex or provider config produces a visual failure state,
  not a crash.
- [ ] Inspect Qt plugins and generated bundle contents.
- [ ] Inspect bundled QML/PySide resources and avoid missing-plugin runtime
  failures.
- [ ] Record deterministic build dirs, version labeling, and clean install
  roots.
- [ ] Record toolchain choices, excluded libraries, Qt plugins, graphics
  backends, and desktop integration dependencies.
- [ ] Publish or record the SHA256 checksum.
- [ ] Record the dependency inventory.
- [ ] Record Qt/PySide6 notices.
- [ ] Record source/relink or replacement instructions if required by the
  chosen license path.
- [ ] Record clean-machine verification evidence.
- [ ] Document source install, AppImage invocation, profile selection, doctor,
  dry-run, live-run, and workdir/project path flags.

## Clean-Room And License Remaining Work

- [ ] Confirm no tracked path starts with `EXAMPLE/`.
- [ ] Confirm no reference QML, shader, generated shader blob, image, icon,
  font, profile, manifest, build script, terminal-widget material, names,
  colors, formulas, constants, or profile JSON is copied.
- [ ] Confirm no generated `.qsb` file from the reference tree is reused.
- [ ] Confirm no reference images, icons, fonts, manifests, or package metadata
  are reused.
- [ ] Confirm `qmltermwidget`, QTermWidget, terminal-emulator code, and related
  terminal-widget dependencies are not vendored.
- [ ] Confirm no GPL-only Qt modules are bundled.
- [ ] Confirm the Qt for Python license path.
- [ ] Confirm AppImage replacement or relink obligations.
- [ ] Include notices and dependency inventory in release artifacts.
- [ ] Verify generated shader artifacts are derived from Apex-owned source if
  shader artifacts are released.
- [ ] Verify original icon and visual assets have documented provenance.
- [ ] Run clean-room text scans for suspicious reference names where feasible.
- [ ] Keep the base CLI free of Qt, PySide6, PyQt, pywebview, xterm.js,
  qmltermwidget, QTermWidget, copied terminal emulators, shaders, fonts, images,
  icons, and graphical startup checks.

## Terminal CLI Remaining Work

- [ ] Confirm whether the terminal CLI polish pass is complete.
- [ ] If not complete, improve Rich status hierarchy with clearer labels and
  compact panels.
- [ ] If not complete, polish terminal themes for `crt-green`, `crt-amber`,
  `ibm-dos`, and `plain`.
- [ ] If not complete, improve progress summaries for max iterations, active
  command, and current manager decision.
- [ ] If not complete, improve compact progress and diagnostic summaries.
- [ ] Preserve plain ASCII-safe output for redirected logs and
  machine-unfriendly terminals.
- [ ] Preserve redirected output cleanliness.
- [ ] Preserve `--event-stream - --machine-output` as JSONL-only.
- [ ] Preserve the rule that no shader, image, GUI, QML, or PySide dependency
  enters the base terminal CLI path.
- [ ] Do not introduce an ANSI scrape contract, copied retro profiles,
  graphical dependencies, a terminal-emulator widget, or duplicated event state
  that belongs in the workflow engine.

## Production Hardening Remaining Work

- [ ] Verify offscreen smoke launch.
- [ ] Verify software backend fallback.
- [ ] Verify desktop screenshot smoke at common viewports.
- [ ] Verify desktop screenshot smoke for high, balanced, low, and plain
  profiles.
- [ ] Verify pixel-level nonblank checks for effect surfaces.
- [ ] Verify no-overlap checks for all built-in profiles.
- [ ] Verify long-run memory behavior.
- [ ] Verify reduced-effects behavior.
- [ ] Verify plain fallback behavior.
- [ ] Verify low-effects and plain modes are intentionally designed, not broken
  versions of the high-effects mode.
- [ ] Verify the app visibly changes between rendering modes.
- [ ] Verify effects react to run lifecycle events.
- [ ] Verify graphical dependency absence in the base CLI install.

## Final Verification Matrix

- [ ] Rerun and record the full pytest suite.
- [ ] Rerun and record `black --check src tests`.
- [ ] Rerun and record `mypy`.
- [ ] Rerun and record `pylint src/apex_infinite src/apex_infinite_visual`.
- [ ] Rerun and record QML lint for every QML file.
- [ ] Resolve or explicitly record any remaining QML lint warnings.
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
- [ ] Rerun and record `git diff --check`.
- [ ] Rerun and record that no `EXAMPLE/` paths are tracked.
- [ ] Rerun and record that no `.qsb` artifacts are unintentionally tracked.
- [ ] Rerun and record license notice and dependency inventory review.

## Remaining Session Order

- [ ] Close product-scope decisions for resume, shader mode, profile drawer
  parity, and terminal CLI polish.
- [ ] Finish QML profile drawer parity if required.
- [ ] Implement the full graphical first-run shared-config flow.
- [ ] Promote shader mode or explicitly defer it.
- [ ] Build and inspect the AppImage release candidate.
- [ ] Run clean-machine release verification and fix blockers.
- [ ] Run the complete final verification matrix and record results.

## Release Completion Blockers

- [ ] Do not claim completion until `apex-infinite-visual` opens as a
  production Linux command surface, not a prototype dashboard.
- [ ] Do not claim completion until the first screen is the usable operator
  terminal.
- [ ] Do not claim completion until visual profiles, rendering modes, quality
  tiers, and effects persist across launches.
- [ ] Do not claim completion until effects are visually rich, workflow-aware,
  configurable, and bounded by reduced/plain fallbacks.
- [ ] Do not claim completion until the wrapper remains event-driven and does
  not parse human terminal output.
- [ ] Do not claim completion until the base terminal CLI remains free of
  graphical dependencies.
- [ ] Do not claim completion until the visual app supports first-run setup,
  doctor, dry-run, live-run, stop, and resume-facing workflows or the resume
  scope is explicitly removed.
- [ ] Do not claim completion until the desktop launcher and AppImage work on a
  clean supported Linux machine.
- [ ] Do not claim completion until release artifacts include original assets,
  notices, dependency inventory, and checksums.
- [ ] Do not claim completion until clean-room evidence proves the `EXAMPLE/`
  tree was used only for conceptual study.
- [ ] Do not claim completion until terminal CLI polish is implemented or
  explicitly closed without compromising machine-output or plain-output
  contracts.
