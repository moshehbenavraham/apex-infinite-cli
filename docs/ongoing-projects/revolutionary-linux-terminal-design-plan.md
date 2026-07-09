# Revolutionary Linux Terminal Design Plan

## Purpose

Turn Apex Infinite Visual from a source-mode QML wrapper into a full-production
Linux terminal command surface with maximal visual ambition.

The target is not a simple retro skin. The target is an operator-grade,
event-driven hyperterminal: a dense, legible, reactive Linux app where workflow
state, Codex autonomy, provider health, spec progress, errors, and artifacts
are rendered as a living terminal environment.

This plan inherits the productization rules from
`docs/ongoing-projects/terminal-and-linux-app-productization-plan.md` and adds a
focused design and implementation path for the highest-quality terminal visual
experience.

## Design Mandate

- Build the real product surface, not a demo dashboard.
- Make the first screen the actual command surface.
- Default to the richest production design the machine can support.
- Keep a readable low-effects mode, but do not design the main experience
  around the fallback.
- Make the visual system respond to real workflow facts, not arbitrary
  decoration.
- Preserve the Python CLI as the workflow engine.
- Preserve JSONL events or an importable event API as the wrapper state
  boundary.
- Keep PySide6, QML, shaders, graphical assets, and packaging tools out of the
  base terminal CLI dependency set.
- Treat the local `EXAMPLE/` tree as reference-only study material. Do not copy
  source, QML, shaders, constants, generated shader blobs, images, icons,
  fonts, profiles, manifests, build scripts, terminal-widget code, or package
  metadata.

## Current Baseline

The base productization plan establishes these facts:

- `apex-infinite` is already the Python workflow engine.
- `apex-infinite-visual` already exists as an optional PySide6/QML source-mode
  wrapper.
- The wrapper launches the CLI through:

```text
apex-infinite --event-stream - --machine-output ...
```

- The wrapper already exposes source-mode controls for theme, effect intensity,
  font family, font scale, reduced effects, plain fallback, glow, scanlines,
  flicker, and curvature.
- Wrapper preferences are not yet persisted.
- First-run setup, XDG config, diagnostic UX, desktop integration, AppImage
  packaging, license notices, checksums, and clean-machine release evidence are
  not complete.
- The visual wrapper must not parse Rich output, plain terminal text, SQLite
  history rows, ANSI captures, or terminal-control sequences.

Current implementation shape:

- `src/apex_infinite_visual/settings.py` owns validated theme presets and
  effect settings.
- `src/apex_infinite_visual/main.py` owns the PySide6 bridge, subprocess
  launch, fixture playback, event ingestion, settings updates, and QML-facing
  properties.
- `src/apex_infinite_visual/qml/Main.qml` renders one monolithic application
  window with run controls, status cells, event log, simple glow, scanline,
  flicker, and curvature treatments.
- `tests/test_visual_wrapper_productization.py` and
  `tests/test_visual_wrapper_spike.py` cover the source-mode wrapper boundary.

The gap is not whether a visual wrapper exists. The gap is that the current
surface is still structurally modest: it is a useful dashboard, not the final
extreme Linux terminal experience.

## Reference Study From EXAMPLE

The local reference tree contains `EXAMPLE/cool-retro-term/`. Its value here is
conceptual only.

Relevant observed concepts:

- Qt/QML app structure with a terminal-centered visual surface.
- Shader-heavy rendering with separate dynamic, static, frame, bloom, and
  burn-in style stages.
- Many generated shader variants selected by runtime feature flags.
- A settings model that separates profile, screen, terminal, effects, and
  advanced performance controls.
- Effect categories including bloom, persistence, static noise, jitter, glow
  line, curvature, ambient light, flicker, horizontal sync, RGB shift, frame
  shininess, rasterization modes, texture quality, and effect frame skipping.
- Font controls for source, rendering mode, scale, width, and line spacing.
- Versioned profile save, load, import, and export flows.
- Desktop metadata and package metadata for launcher integration.
- AppImage and desktop packaging scripts exist in the reference project, but
  must not be copied.

Clean-room Apex translation:

| Reference concept | Apex design translation |
| --- | --- |
| Multi-pass terminal rendering | Independent QML scene graph with explicit event source, state compositor, effect buffer, postprocess pass, and presentation frame |
| Shader feature variants | Original Apex shader modules or QML effects selected by validated capability flags and quality presets |
| Burn-in and persistence | Workflow-aware phosphor trail that reacts to new event rows, active runs, errors, and completed iterations |
| Bloom and glow | Semantic glow around active provider, current spec, current iteration, warning state, and completed gates |
| Scanline and rasterization choices | Apex-owned line, pixel, subpixel, and crisp-modern rendering modes for the operator log |
| Static noise, jitter, sync, RGB shift | Independently implemented effect modules with bounded intensity, reduced-effects disablement, and performance budgets |
| Profile system | Versioned Apex visual profiles stored in XDG config/data locations with import/export and reset |
| Effects FPS and texture quality | Production quality tiers: Cinematic, Balanced, Battery, Low Effects, Plain |
| Desktop metadata | Original Apex `.desktop`, AppStream metadata, icon, categories, launcher actions, and AppImage integration |

Forbidden translation:

- Do not reuse the reference QML component tree.
- Do not reuse reference shader code or constants.
- Do not reuse generated `.qsb` files.
- Do not reuse reference images, icons, fonts, profile JSON, manifests, or
  packaging scripts.
- Do not vendor `qmltermwidget`, QTermWidget, or terminal-emulator code.

## Product Identity

Working product name for this design lane:

```text
Apex Infinite Hyperterminal
```

This name describes the visual mode only. The command names can remain
`apex-infinite` and `apex-infinite-visual` unless a later release explicitly
renames the app.

Experience principles:

- It should feel like a Linux-native command center, not a website in a window.
- It should be information-dense without becoming noisy.
- It should make autonomous runs auditable at a glance.
- It should make dry-run, live-run, stop, resume, doctor, config, provider, and
  model state visible without opening docs.
- It should make errors impossible to miss and easy to diagnose.
- It should feel visually impossible to confuse with a generic admin dashboard.

## Architecture Target

The final visual architecture should be split into independent layers:

```text
Python CLI workflow engine
  -> registered JSONL events / importable event API
  -> visual event adapter
  -> visual state store
  -> QML bridge
  -> scene components
  -> effect pipeline
  -> presentation shell
```

The wrapper must not own workflow decisions. It may own presentation state,
visual preferences, layout state, and explicitly confirmed shared config writes.

### Proposed Python Modules

- `src/apex_infinite_visual/profile_store.py`
  - XDG-backed visual profile persistence.
  - Atomic writes and backup-on-overwrite.
  - Versioned JSON schema.
  - Import/export validation.
- `src/apex_infinite_visual/render_caps.py`
  - Graphics backend detection.
  - Shader availability checks.
  - Offscreen/software backend handling.
  - Quality-tier selection.
- `src/apex_infinite_visual/visual_state.py`
  - Event-derived display state independent from QML.
  - Run health, stage, provider, model, iteration, current spec, task progress,
    error summary, and recent artifact state.
- `src/apex_infinite_visual/doctor.py`
  - Wrapper-facing diagnostic adapter over the CLI doctor path.
  - Display-safe pass, warn, fail summaries.
- `src/apex_infinite_visual/assets.py`
  - Paths for original icons, generated visual assets, and package resources.
  - No dependency on `EXAMPLE/`.

### Proposed QML Structure

Split the current monolithic `Main.qml` into an app shell and reusable
components:

```text
src/apex_infinite_visual/qml/
  Main.qml
  shell/AppShell.qml
  shell/CommandSurface.qml
  shell/StatusRail.qml
  shell/RunConsole.qml
  shell/SpecMap.qml
  shell/SignalPanel.qml
  shell/SettingsDrawer.qml
  controls/ApexButton.qml
  controls/ApexToggle.qml
  controls/ApexSlider.qml
  controls/ApexSegmentedControl.qml
  controls/ApexStatusCell.qml
  effects/EffectSurface.qml
  effects/PhosphorTrail.qml
  effects/ScanlineField.qml
  effects/GlowField.qml
  effects/GlassCurvature.qml
  effects/SignalDistortion.qml
  effects/FrameTreatment.qml
```

The component names above are implementation targets, not borrowed reference
names.

## Information Design

The first viewport should be the operator console. No landing page, no
marketing hero, no explanatory panels.

Primary zones:

- Run Command Strip
  - Project path selector.
  - Start command selector.
  - Dry-run/live-run segmented control.
  - Max iteration stepper.
  - Start, stop, resume, and doctor buttons.
  - Autonomy summary with supported Codex flags and current risk level.
- Mission State Rail
  - Current run status.
  - Stage.
  - Iteration.
  - Provider.
  - Model.
  - Codex binary.
  - Config source.
  - Event stream mode.
  - History DB status.
- Spec Map
  - Detected `.spec_system/` status.
  - Phase/session identity when available.
  - Current command.
  - Task checklist progress when events provide it.
  - Carry-forward warnings and validation status when available.
- Event Core
  - Virtualized event log.
  - Structured rows, not scraped terminal output.
  - Row classes for startup, provider preflight, manager decision, command,
    response, pause, error, stop, completion, and summary.
  - Search, filter, pin, copy, and export controls.
- Signal Panel
  - Provider health.
  - Recent stderr summary.
  - Malformed event count.
  - Runtime duration.
  - Last machine event.
  - Artifact links from safe event payloads only.
- Visual Profile Drawer
  - Theme family.
  - Rendering mode.
  - Effect intensity.
  - Quality tier.
  - Font family, scale, width, and line spacing.
  - Reduced effects.
  - Plain fallback.
  - Save, duplicate, import, export, reset.

## Visual Language

The final design should move beyond the four current presets while keeping the
current names compatible.

### Built-In Profiles

Keep existing compatibility:

- `crt-green`
- `crt-amber`
- `ibm-dos`
- `plain`

Add new Apex-owned profiles:

- `apex-reactor`
  - Deep black base, green-white active signal, red fault charge, high bloom.
- `operator-amber`
  - Amber command surface, warm warning emphasis, low blue content.
- `blueprint-dos`
  - Blue-black base, precise cyan vector lines, crisp pixel grid.
- `whiteout-lab`
  - High-contrast light mode for bright rooms and screenshots.
- `blackbox`
  - Minimal dark mode with restrained effects for long unattended runs.
- `incident-red`
  - Error investigation mode with stronger event classification and fault
    isolation.

These profile names, colors, and constants must be independently designed.

### Rendering Modes

- `modern-crisp`
  - High-readability default when effects are disabled.
- `scanline`
  - Horizontal line treatment.
- `pixel-grid`
  - Cell-grid treatment for log rows and status modules.
- `subpixel`
  - Fine RGB-style edge treatment without copying reference formulas.
- `cinematic`
  - Full postprocess pipeline with curvature, glow, persistence, ambient frame,
    jitter, and event-reactive pulse.

### Event-Reactive Effects

Every major effect should have semantic triggers:

- Run start creates a short surface charge.
- Provider preflight success sends a low-intensity signal sweep.
- Provider preflight failure creates a visible red fault lock.
- New manager decision creates a pulse around the decision panel.
- New iteration adds a soft persistence trail to the event core.
- Operator stop drains glow immediately and freezes final state.
- Successful completion performs a restrained completion sweep.
- Non-zero exit, stderr, malformed JSONL, and timeout use distinct error
  signatures.

This is where the design becomes unique: the terminal should visualize the
workflow, not merely animate.

## Effect Pipeline

Build an original Apex effect pipeline in production stages.

### Stage 1: QML-Only High Design

Deliver a dramatic app without custom shaders first:

- Replace flat rectangles with a structured surface shell.
- Add layered QML items for glow, scanlines, frame treatment, and pulse.
- Add virtualized event rows with typed visual states.
- Add profile persistence.
- Add quality tiers.
- Add reduced-effects and plain fallback enforcement.
- Add screenshot smoke checks.

### Stage 2: Clean-Room Shader Layer

Add original shader assets only after the scene architecture is stable:

- Original postprocess shader for curvature and glass treatment.
- Original bloom/glow composition.
- Original procedural noise field.
- Original chroma/subpixel edge treatment.
- Original persistence buffer for event-row trails.
- Original line jitter and sync distortion with bounded intensity.
- Shader capability probing and automatic fallback.
- Generated shader artifacts reviewed before release.

### Stage 3: Workflow-Aware Rendering

Make visual effects data-driven:

- Bind effect intensity to run state.
- Bind warning and error effects to event severity.
- Bind task progress to spec map density.
- Bind provider health to signal panel.
- Bind autonomy policy to command strip warning level.
- Bind config source and doctor results to launch readiness.

### Stage 4: Production Hardening

Production effects must pass:

- Offscreen smoke launch.
- Software backend fallback.
- Desktop screenshot smoke at common viewports.
- Pixel-level nonblank checks.
- No overlap checks for all built-in profiles.
- Long-run memory checks.
- Reduced-effects verification.
- Plain fallback verification.
- No graphical dependency in base CLI install.

## Terminal CLI Design Lane

The base terminal CLI should also receive a stronger design pass, within its
terminal constraints.

Allowed terminal CLI improvements:

- Rich status hierarchy with clearer labels and compact panels.
- Stronger theme polish for `crt-green`, `crt-amber`, `ibm-dos`, and `plain`.
- Better dry-run/live-run autonomy summary before real runs.
- Progress summaries for max iterations, active command, and current manager
  decision.
- Plain ASCII-safe output for redirected logs and machine-unfriendly terminals.
- No shader, image, GUI, QML, or PySide dependency.

Forbidden terminal CLI changes:

- No ANSI scrape contract.
- No copied retro profiles.
- No graphical dependency.
- No terminal-emulator widget.
- No event-state duplication that belongs in the workflow engine.

## Profile And Persistence Plan

Visual settings should become a production profile system.

Storage:

- Shared CLI config remains at the XDG config path defined by the base
  productization plan.
- Wrapper-only visual settings live under:

```text
${XDG_CONFIG_HOME:-~/.config}/apex-infinite/visual-profiles.json
```

- Runtime window state can live under:

```text
${XDG_STATE_HOME:-~/.local/state}/apex-infinite/visual-state.json
```

Profile schema:

- `version`
- `name`
- `theme_name`
- `rendering_mode`
- `quality_tier`
- `effect_intensity`
- `font_family`
- `font_scale`
- `font_width`
- `line_spacing`
- `reduced_effects`
- `plain_fallback`
- `effects`
  - `glow`
  - `scanlines`
  - `flicker`
  - `curvature`
  - `bloom`
  - `persistence`
  - `noise`
  - `jitter`
  - `sync`
  - `chroma`
  - `ambient_frame`
- `layout`
  - density
  - side rail position
  - event row height
  - pinned panels

Profile operations:

- Save current.
- Duplicate.
- Rename.
- Delete custom.
- Reset built-in.
- Import JSON.
- Export JSON.
- Validate schema and version.
- Reject non-ASCII names for now, matching repo conventions.
- Never write provider secrets.

## Event Stream Expansion

The design should not scrape missing information. If the wrapper needs state,
add registered events to the CLI.

Candidate event additions:

- `doctor_started`
- `doctor_check`
- `doctor_finished`
- `config_resolved`
- `codex_flags_resolved`
- `autonomy_policy_resolved`
- `spec_system_detected`
- `spec_session_resolved`
- `task_progress`
- `artifact_detected`
- `run_duration_tick`
- `wrapper_capabilities_resolved`

Event rules:

- Every new event must be registered in `src/apex_infinite/events.py`.
- Every new event must have file-stream and stdout-machine-output coverage.
- Event payloads must exclude secrets, ANSI escapes, Rich markup, frame glyphs,
  copied reference identifiers, and renderer snapshots.
- Event payloads should expose facts, not visual choices.

## Graphical First-Run Experience

The visual app should be able to onboard a clean user without requiring a
terminal, while still preserving explicit config writes.

Flow:

1. Detect missing shared CLI config.
2. Show provider choices: Ollama, OpenAI, Grok.
3. Let the user enter or confirm model.
4. Let the user select Codex binary.
5. Show detected Codex flag compatibility.
6. Let the user choose projects directory and target project.
7. Run doctor.
8. Show pass, warn, fail results.
9. Offer dry-run as the default first launch.
10. Require explicit confirmation before writing shared CLI config.

The first-run surface should use the same high-design command shell, not a
separate plain wizard that feels like another product.

## Desktop Productization

Ship the visual app like a real Linux application.

Required artifacts:

- Original app icon.
- `.desktop` file.
- AppStream metadata.
- Launcher command for source install and AppImage.
- Launcher action for new visual run.
- Launcher action for doctor.
- Launcher action for safe dry run when feasible.
- AppImage artifact:

```text
apex-infinite-visual-linux-x86_64.AppImage
```

- SHA256 checksum.
- Dependency inventory.
- Qt/PySide6 notices.
- Source/relink or replacement instructions if required by the chosen license
  path.
- Clean-machine verification report.

Packaging decision:

- Evaluate `pyside6-deploy` first.
- Use direct Nuitka or another path only after documenting why it is better for
  this app.
- Do not commit generated packaging output unless a release session explicitly
  scopes it.

## Clean-Room And License Gates

Before any binary or visual asset release:

- Confirm no tracked path starts with `EXAMPLE/`.
- Confirm no reference QML, shader, generated shader blob, image, icon, font,
  profile, manifest, build script, or terminal-widget material is copied.
- Confirm no GPL-only Qt modules are bundled.
- Confirm Qt for Python license path.
- Confirm AppImage replacement/relink obligations.
- Include notices and dependency inventory.
- Verify generated shader artifacts are derived from Apex-owned source.
- Verify original icon and visual assets have documented provenance.
- Run clean-room text scans for suspicious reference names where feasible.

## Implementation Workstreams

### Workstream 1: Visual State Foundation

Work:

- Extract display state from the QML bridge into a Python `visual_state` model.
- Keep QML as a consumer of properties and invokable actions.
- Add event-derived state for run health, provider/model, config source, Codex
  flags, current stage, iteration, recent errors, and last manager decision.
- Define missing event payloads before adding wrapper-specific assumptions.
- Add tests for visual state transitions from JSONL fixtures.

Acceptance:

- QML does not parse raw JSONL.
- Python tests can verify display state without PySide6.
- Wrapper state remains derived from registered events and explicit wrapper
  controls.

### Workstream 2: Profile Persistence

Work:

- Add XDG-backed wrapper profile store.
- Persist current visual preferences on explicit save and app close.
- Load last profile on startup.
- Add reset-to-defaults.
- Add import/export for custom profiles.
- Add schema versioning and migration stubs.
- Add corruption handling with backup preservation.

Acceptance:

- Restarting the app restores visual choices.
- Invalid profile JSON fails visibly without breaking shared CLI config.
- Base CLI behavior is unchanged.

### Workstream 3: App Shell Redesign

Work:

- Split `Main.qml` into shell, controls, status, event log, settings, and
  effects components.
- Build a full-window command surface with stable responsive dimensions.
- Replace generic dashboard rhythm with a dense terminal command-center layout.
- Add virtualized event rows with typed severity, stage, and timestamp display.
- Add event filters and pinned error summary.
- Add start, stop, dry-run/live-run, max iteration, project path, and doctor
  controls in the command strip.
- Ensure all text fits at minimum and common desktop sizes.

Acceptance:

- First screen is the usable app.
- No page section exists only to explain the product.
- Event log remains readable under every built-in profile.
- Controls do not shift or overlap during runs.

### Workstream 4: QML High-Design Effects

Work:

- Add layered QML effects for glow, scanline field, frame treatment, pulse, and
  event-row persistence.
- Add event-reactive animation triggers.
- Add rendering modes and quality tiers.
- Add reduced-effects enforcement.
- Add plain fallback enforcement.
- Add offscreen smoke and screenshot checks.

Acceptance:

- The app visibly changes between rendering modes.
- Effects react to run lifecycle events.
- Low-effects and plain modes are intentionally designed, not broken versions
  of the high-effects mode.

### Workstream 5: Clean-Room Shader Pipeline

Work:

- Create original shader source files only after Workstream 4 stabilizes.
- Add shader build/review commands if generated artifacts are needed.
- Add capability detection and fallback paths.
- Add original curvature, glow, procedural noise, persistence, and chroma
  modules.
- Add performance tiers and frame pacing controls.
- Record provenance for all shader code and generated outputs.

Acceptance:

- Shader mode is visually richer than QML-only mode.
- Unsupported graphics environments fall back automatically.
- Generated shader artifacts are reviewed and documented before release.
- No reference shader material appears in tracked files.

### Workstream 6: Graphical Doctor And First Run

Work:

- Add CLI doctor if not already implemented by the terminal productization lane.
- Surface doctor results in the visual app.
- Add first-run shared config flow.
- Add explicit config write confirmation.
- Show autonomy policy before live runs.
- Keep dry-run as the first-run default.

Acceptance:

- A clean Linux user can launch the visual app, configure it, run doctor, and
  start a dry run without editing source files.
- The user can see why live mode is risky before starting it.
- Missing provider, Codex, model, project, and config failures are actionable.

### Workstream 7: Desktop And AppImage Release

Work:

- Add original icon.
- Add `.desktop` and AppStream metadata.
- Package the visual extra in an isolated workspace.
- Inspect Qt plugins and generated bundle contents.
- Build AppImage.
- Publish checksum.
- Verify source install, visual extra install, and AppImage on a clean Linux
  environment.

Acceptance:

- Desktop launcher opens the visual app.
- AppImage does not depend on the source checkout or repo `.venv`.
- Missing Codex/provider config produces a visual failure state, not a crash.
- Release artifacts include notices, inventory, and checksum.

### Workstream 8: Terminal CLI Polish

Work:

- Improve Rich terminal themes and status hierarchy.
- Add clearer autonomy summary before live runs.
- Add compact progress and diagnostic summaries.
- Preserve plain and machine-output behavior.
- Keep all graphical dependencies out of the base install.

Acceptance:

- The terminal CLI feels intentionally designed when run in an interactive
  terminal.
- Redirected output remains clean.
- `--event-stream - --machine-output` remains JSONL-only.

## Recommended Build Order

1. Visual state foundation.
2. Profile persistence.
3. App shell redesign.
4. QML high-design effects.
5. Event stream expansion for missing facts.
6. Graphical doctor and first-run setup.
7. Clean-room shader pipeline.
8. Desktop metadata and original icon.
9. AppImage packaging and license gates.
10. Clean Linux release verification.
11. Terminal CLI polish pass.

This order gets the product architecture right before adding expensive shader
work, then turns the visual system into a releasable Linux app.

## Suggested Session Split

Each session should stay within the Apex Spec target of 2-4 hours and 12-25
tasks.

| Session | Objective |
| --- | --- |
| S01 | Extract visual state model and add event fixture coverage |
| S02 | Add XDG visual profile persistence and import/export |
| S03 | Split QML shell into reusable command-surface components |
| S04 | Redesign event log, status rail, and run command strip |
| S05 | Add QML-only high-design effects and quality tiers |
| S06 | Add event-reactive animation triggers and reduced/plain verification |
| S07 | Add missing CLI events needed by the visual state model |
| S08 | Add graphical doctor and first-run config flow |
| S09 | Add original shader pipeline spike and capability detection |
| S10 | Promote accepted shader effects to production with fallback tests |
| S11 | Add desktop metadata, icon, and AppStream draft |
| S12 | Build and inspect AppImage release candidate |
| S13 | Run clean-machine release verification and fix blockers |
| S14 | Polish terminal CLI themes and docs |

## Verification Matrix

Required checks before claiming the design lane is complete:

- Unit tests for visual state transitions.
- Unit tests for profile schema, persistence, import, export, migration, and
  corruption handling.
- PySide6 import-laziness test.
- QML lint for every QML file.
- Offscreen source-mode smoke.
- Desktop screenshot smoke for high, balanced, low, and plain profiles.
- Pixel nonblank check for effect surface.
- Reduced-effects check.
- Plain fallback check.
- Malformed JSONL check.
- Stderr and non-zero subprocess check.
- Missing PySide6 check.
- Missing Codex binary check.
- Missing provider config check.
- Clean base install check proving PySide6 is absent.
- Visual extra source install check.
- AppImage clean-machine launch check.
- `git diff --check`.
- `git ls-files | grep '^EXAMPLE/'` must return no tracked files.
- License notice and dependency inventory review.

## Definition Of Done

This design effort is complete when:

- `apex-infinite-visual` opens as a production Linux command surface, not a
  prototype dashboard.
- The first screen is the usable operator terminal.
- Visual profiles, rendering modes, quality tiers, and effects persist across
  launches.
- Effects are visually rich, workflow-aware, configurable, and bounded by
  reduced/plain fallbacks.
- The wrapper remains event-driven and does not parse human terminal output.
- The base terminal CLI remains free of graphical dependencies.
- The visual app supports first-run setup, doctor, dry-run, live-run, stop, and
  resume-facing workflows.
- The desktop launcher and AppImage work on a clean supported Linux machine.
- Release artifacts include original assets, notices, dependency inventory, and
  checksums.
- Clean-room evidence proves the `EXAMPLE/` tree was used only for conceptual
  study.
- The terminal CLI receives a matching polish pass without compromising
  machine-output or plain-output contracts.
