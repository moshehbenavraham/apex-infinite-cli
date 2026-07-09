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

## EXAMPLE Source Reference Map

This map exists to make the design plan traceable. Every path below is
reference-only evidence from the local study tree, not an implementation source
for Apex. Use these anchors to understand what production concerns the
reference app solved, then build Apex-owned code, constants, assets, profiles,
metadata, and release scripts.

### Clean-Room Boundary Anchors

- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/README.md:7-15`
  - Code references: project description, `qmltermwidget` dependency note,
    settings categories.
  - Plan mapping: validates that the reference app is a terminal-emulator-style
    visual product, while Apex must stay a workflow command surface and must not
    vendor `qmltermwidget`.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/PreprocessedTerminal.qml:24-37`
  - Code references: `import QMLTermWidget 2.0`, `QMLTermWidget`,
    `QMLTermSession`, `ShaderEffectSource mainSource`.
  - Plan mapping: reinforces the explicit Apex boundary that the visual wrapper
    must render registered workflow events, not become a general terminal
    emulator widget.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/PreprocessedTerminal.qml:96-128`
  - Code references: `QMLTermWidget`, `textureSize`, `colorScheme`,
    `QMLTermSession`.
  - Plan mapping: useful only as a conceptual reminder that the source surface
    can be captured into render buffers; Apex should capture event rows and
    panels, not terminal emulator state.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/resources.qrc:19-47`
  - Code references: bundled fonts and original reference images/icons.
  - Plan mapping: confirms that fonts and images are asset-heavy release
    concerns; Apex must create or select its own licensed font and image path.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/resources.qrc:51-118`
  - Code references: generated shader blobs, `.qsb` files, bundled font files.
  - Plan mapping: every Apex shader artifact must be generated from Apex-owned
    source and reviewed before release.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/packaging/debian/copyright:1-11`
  - Code references: Debian copyright file, `GPL-3`.
  - Plan mapping: reference material is license-sensitive and must remain
    outside Apex tracked code unless a separate legal decision explicitly
    changes scope.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/packaging/rpm/cool-retro-term.spec:19-25`
  - Code references: `License: GPL-3.0+`.
  - Plan mapping: release metadata can inspire Apex's dependency inventory and
    notices, but not be copied.

### Runtime App And Shell Structure Anchors

- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/main.cpp:65-75`
  - Code references: `--default-settings`, `--workdir`, `-e`, `--fullscreen`,
    `--profile`, `--verbose`.
  - Plan mapping: supports a real visual launcher CLI, but Apex options should
    remain workflow-oriented: project path, dry-run/live-run, doctor, profile,
    and first-run mode.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/main.cpp:86-111`
  - Code references: `QApplication`, application identity, icon, desktop file
    name.
  - Plan mapping: Apex visual needs Linux-native application identity, icon,
    and desktop integration rather than a script-only wrapper.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/main.cpp:101-140`
  - Code references: `QQmlApplicationEngine`, `FileIO`, `FontManager`,
    root context properties, import path registration, `engine.load`.
  - Plan mapping: informs Apex bridge design, but Apex should expose workflow
    state models and actions instead of terminal-widget command properties.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/main.qml:27-45`
  - Code references: `ApplicationSettings`, `TimeManager`,
    `SettingsWindow`, `TerminalWindow`.
  - Plan mapping: supports splitting Apex `Main.qml` into app settings,
    timing/effects, shell, and settings components.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/TerminalWindow.qml:26-52`
  - Code references: `ApplicationWindow`, default dimensions, minimum size,
    fullscreen, menu bar, title.
  - Plan mapping: Apex app shell should be full-window, Linux-native, and
    stable at minimum sizes.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/TerminalWindow.qml:53-125`
  - Code references: `Action` objects for fullscreen, new window, quit,
    settings, copy, paste, zoom, about, tab handling.
  - Plan mapping: Apex command strip should expose real actions as first-class
    UI controls and shortcuts, including run, stop, resume, doctor, profile,
    and zoom/font controls.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/TerminalTabs.qml:41-60`
  - Code references: `addTab()`, `closeTab()`, `ListModel`.
  - Plan mapping: supports modeling repeated shell surfaces cleanly. Apex may
    later use tabs for projects/runs, but the first production target should
    stay one focused workflow surface.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/TerminalTabs.qml:124-154`
  - Code references: `StackLayout`, `Repeater`, `TerminalContainer`.
  - Plan mapping: reinforces decomposition into shell, command surface, run
    console, status rail, signal panel, settings drawer, and effects surface.

### Render Pipeline Anchors

- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/app.pro:34-52`
  - Code references: `qsb`, shader compilation, shader inputs, `QMAKE_EXTRA_COMPILERS`.
  - Plan mapping: Apex shader source needs an explicit build/review pipeline
    before generated artifacts are committed.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/app.pro:57-95`
  - Code references: `RASTER_MODES`, `BINARY_FLAGS`, dynamic shader variant
    targets, static shader variant targets.
  - Plan mapping: supports capability-selected effect variants, but Apex should
    design its own quality tiers and shader module switches.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/ShaderTerminal.qml:26-48`
  - Code references: `dynamicFragmentPath()`, `staticFragmentPath()`,
    `rasterization`, `burnIn`, `frameEnabled`, `chromaColor`, `rgbShift`,
    `bloom`, `screenCurvature`, `frameShininess`.
  - Plan mapping: translates to Apex render capability flags and quality
    profiles without copying names, paths, formulas, or shader constants.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/ShaderTerminal.qml:50-71`
  - Code references: `ShaderEffectSource source`, `BurnInEffect`,
    `bloomSource`, `fontColor`, `backgroundColor`, `virtualResolution`,
    `screenResolution`.
  - Plan mapping: informs Apex scene graph state: event source, effect buffer,
    bloom/glow buffer, profile colors, and viewport/capability sizing.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/ShaderTerminal.qml:72-137`
  - Code references: dynamic `ShaderEffect`, `screenBuffer`, `burnInSource`,
    `frameSource`, `flickering`, `horizontalSync`, `glowingLine`, `jitter`,
    `staticNoise`, `noiseTexture`, `rasterizationIntensity`.
  - Plan mapping: supports the Apex Workstream 5 goal of an original dynamic
    postprocess layer for noise, sync, jitter, persistence, and event pulse.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/ShaderTerminal.qml:139-160`
  - Code references: conditional `Loader`, `TerminalFrame`,
    `ShaderEffectSource`, `hideSource`.
  - Plan mapping: supports optional frame treatment behind capability and
    reduced-effects gates.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/ShaderTerminal.qml:162-200`
  - Code references: static `ShaderEffect`, `bloomSource`, `rgbShift`,
    `screen_brightness`, static `ShaderEffectSource frameBuffer`.
  - Plan mapping: supports separating dynamic event-row effects from final
    presentation composition.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/TerminalContainer.qml:56-82`
  - Code references: `bloomEffectLoader`, `FastBlur`, `bloomSourceLoader`,
    `ShaderEffectSource`.
  - Plan mapping: informs the Apex QML-only Stage 1 glow path before custom
    shaders exist.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/PreprocessedTerminal.qml:268-295`
  - Code references: `kterminalSource`, `textureSize`, `sourceRect`,
    `burnInContainer`, `burnInQuality`.
  - Plan mapping: Apex should use stable texture sizing for event panels and
    effect buffers, with quality controls separated from visual intensity.

### Effect And Shader Behavior Anchors

- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/ApplicationSettings.qml:74-102`
  - Code references: `staticNoise`, `screenCurvature`, `glowingLine`,
    `burnIn`, `bloom`, `chromaColor`, `jitter`, `horizontalSync`,
    `flickering`, `rgbShift`, `frameShininess`, `frameSize`, `screenRadius`,
    `frameEnabled`.
  - Plan mapping: validates the plan's effect inventory. Apex implementation
    must bind similar categories to workflow state, not arbitrary decoration.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/SettingsEffectsTab.qml:29-94`
  - Code references: effect controls for bloom, burn-in, static noise, jitter,
    glow line, curvature, ambient light, flickering, horizontal sync, RGB
    shift, and frame shininess.
  - Plan mapping: Apex settings drawer should expose comparable operator
    controls plus reduced/plain fallbacks and semantic event triggers.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/BurnInEffect.qml:24-50`
  - Code references: `Loader`, `effectSource`, `lastUpdate`,
    `burnInFadeTime`, `completelyUpdate()`.
  - Plan mapping: supports an Apex-owned phosphor/persistence model reacting
    to new event rows, iterations, errors, and run completion.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/BurnInEffect.qml:61-128`
  - Code references: recursive `ShaderEffectSource`, terminal paint
    connection, settings-change restart, `burn_in` shader.
  - Plan mapping: Apex persistence must reset cleanly on profile/font/quality
    changes and expose predictable fallbacks.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/TerminalFrame.qml:24-49`
  - Code references: `ShaderEffect`, frame color mix, curvature, frame size,
    radius, viewport size, ambient light, frame shaders.
  - Plan mapping: Apex frame treatment should be a reusable effect component,
    not hard-coded into the main shell.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/shaders/terminal_dynamic.vert:39-49`
  - Code references: time-based brightness, horizontal sync strength,
    distortion scale/frequency.
  - Plan mapping: Apex signal distortion can be event-reactive and bounded by
    quality tier rather than constant idle motion.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/shaders/terminal_dynamic.frag:23-52`
  - Code references: uniforms for time, colors, virtual resolution,
    rasterization intensity, burn-in, static noise, curvature, glow line,
    chroma, jitter, horizontal sync, flickering, frame, bloom.
  - Plan mapping: Apex shader interfaces should have a typed render-state
    object derived from profiles, capability detection, and workflow events.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/shaders/terminal_dynamic.frag:66-117`
  - Code references: rasterization modes for scanline, pixel, and subpixel
    treatments.
  - Plan mapping: supports Apex rendering modes `scanline`, `pixel-grid`,
    `subpixel`, and `modern-crisp`, implemented independently.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/shaders/terminal_dynamic.frag:134-179`
  - Code references: coordinate distortion, procedural noise sampling, jitter,
    glow line, frame mixing, burn-in, rasterization, chroma conversion,
    flickering.
  - Plan mapping: evidence for the staged effect pipeline and verification
    needs: nonblank pixels, reduced effects, performance, and fallback.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/shaders/terminal_static.frag:19-31`
  - Code references: final composition uniforms and bloom source.
  - Plan mapping: supports separating final presentation state from event-log
    state.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/shaders/terminal_static.frag:51-68`
  - Code references: curvature and RGB shift.
  - Plan mapping: Apex chroma/subpixel effects should be optional, bounded,
    and disabled in reduced/plain modes.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/shaders/terminal_static.frag:72-98`
  - Code references: bloom sampling, frame reflection, brightness, noise,
    final color.
  - Plan mapping: supports final composition and frame-lighting design, with
    Apex-owned formulas and constants.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/shaders/burn_in.frag:6-15`
  - Code references: burn-in timing uniforms and source samplers.
  - Plan mapping: Apex persistence needs explicit timing state, not hidden UI
    timers.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/shaders/burn_in.frag:21-36`
  - Code references: accumulated color, previous mask, decay, current mask.
  - Plan mapping: Apex should implement event-row trails clean-room with
    verified decay behavior.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/shaders/terminal_frame.frag:6-16`
  - Code references: frame uniforms for curvature, color, size, radius,
    viewport, ambient light, shininess.
  - Plan mapping: Apex frame effects should be profile-driven and responsive to
    current run severity.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/shaders/terminal_frame.frag:38-79`
  - Code references: frame coordinate distortion, rounded rectangle mask,
    edge softness, glass, frame tint, noise, alpha.
  - Plan mapping: supports original Apex frame/glass treatment with screenshot
    and overlap verification.

### Profiles, Settings, And Persistence Anchors

- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/ApplicationSettings.qml:27-40`
  - Code references: `version`, `profileVersion`, min/max font scaling,
    burn-in fade time.
  - Plan mapping: Apex profiles need explicit schema versioning and bounded
    ranges.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/ApplicationSettings.qml:42-128`
  - Code references: general settings, performance values, profile settings,
    rasterization constants, font source constants, font aliases.
  - Plan mapping: supports splitting Apex settings into visual profile,
    runtime window state, effect quality, and font controls.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/ApplicationSettings.qml:160-211`
  - Code references: `composeSettingsString()`, `composeProfileObject()`,
    `composeProfileString()`.
  - Plan mapping: Apex profile persistence should serialize a versioned,
    validated object rather than raw QML state.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/ApplicationSettings.qml:213-240`
  - Code references: `loadSettings()`, `storeSettings()`, `_CURRENT_SETTINGS`,
    `_CURRENT_PROFILE`.
  - Plan mapping: Apex should persist last profile and runtime state, but under
    XDG JSON files with atomic writes and corruption backup.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/ApplicationSettings.qml:266-312`
  - Code references: `loadProfileString()` restoring visual and font fields.
  - Plan mapping: Apex profile load must be complete, deterministic, and tested
    against all built-in profile fields.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/ApplicationSettings.qml:314-363`
  - Code references: custom profile storage, `appendCustomProfile()`.
  - Plan mapping: Apex needs custom profile lifecycle operations and tests.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/ApplicationSettings.qml:365-843`
  - Code references: built-in profile `ListModel` entries.
  - Plan mapping: Apex should ship richer built-in profiles, but names, colors,
    constants, and JSON must be Apex-owned.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/ApplicationSettings.qml:853-875`
  - Code references: startup argument handling, default settings, custom
    profile load, `--profile`.
  - Plan mapping: Apex visual profile selection can be CLI-driven, with invalid
    profiles producing visible warnings.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/SettingsWindow.qml:38-73`
  - Code references: tabs `General`, `Terminal`, `Effects`, `Advanced`.
  - Plan mapping: supports Apex settings drawer structure: profile, command,
    terminal text, effects, performance, doctor, and release diagnostics.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/SettingsGeneralTab.qml:25-90`
  - Code references: profile list, save, load, remove.
  - Plan mapping: Apex should support save, duplicate, rename, delete custom,
    reset built-in, and visible validation errors.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/SettingsGeneralTab.qml:96-180`
  - Code references: import/export, JSON parse, `profileVersion`, file read and
    write.
  - Plan mapping: Apex import/export must validate schema, reject secrets, and
    never mutate shared CLI config without explicit confirmation.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/SettingsGeneralTab.qml:185-237`
  - Code references: brightness, contrast, margin, radius, frame size, opacity.
  - Plan mapping: Apex visual profile should include layout density, row
    sizing, frame strength, and brightness/contrast controls.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/Storage.qml:24-88`
  - Code references: `LocalStorage.openDatabaseSync`, settings table, get/set,
    drop.
  - Plan mapping: Apex explicitly chooses XDG JSON with atomic writes instead
    of QML local storage so tests can run without PySide6.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/fileio.cpp:7-37`
  - Code references: `FileIO::write()`, `FileIO::read()`.
  - Plan mapping: Apex import/export should live in Python profile-store code
    with schema validation, not QML file IO.

### Font And Text Rendering Anchors

- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/SettingsTerminalTab.qml:29-72`
  - Code references: font source controls, rendering mode combo, default,
    scanlines, pixels, sub-pixels, modern.
  - Plan mapping: Apex rendering modes should be visible operator choices and
    must remain readable under all profiles.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/SettingsTerminalTab.qml:76-117`
  - Code references: font list selection, low-resolution vs modern fallback,
    `fontName`.
  - Plan mapping: Apex can use system fonts first and optional curated fonts
    only with clear licenses and provenance.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/SettingsTerminalTab.qml:119-172`
  - Code references: `fontScaling`, `fontWidth`, `lineSpacing`.
  - Plan mapping: Apex profile schema should include font family, scale, width,
    and line spacing as planned.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/SettingsTerminalTab.qml:175-219`
  - Code references: chroma color, saturation color, font/background/frame
    color buttons.
  - Plan mapping: Apex settings should separate semantic palette tokens from
    raw visual colors.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/fontmanager.h:11-24`
  - Code references: `Q_PROPERTY` values for font list, source,
    rasterization, name, scaling, width, line spacing, low-resolution state.
  - Plan mapping: Apex bridge should expose typed properties, not loosely
    parsed strings.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/fontmanager.cpp:27-42`
  - Code references: monospace system font discovery via `QFontDatabase`.
  - Plan mapping: Apex should prefer system monospace discovery before bundling
    any font assets.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/fontmanager.cpp:60-90`
  - Code references: source/rasterization setters updating filtered fonts and
    computed font.
  - Plan mapping: Apex rendering mode changes must update dependent font and
    layout state immediately.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/fontmanager.cpp:197-381`
  - Code references: bundled font registration list.
  - Plan mapping: Apex must not copy bundled fonts, names, or font profile
    choices from the reference tree.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/fontmanager.cpp:426-463`
  - Code references: source and rasterization filtering.
  - Plan mapping: Apex font controls should enforce valid combinations rather
    than allowing broken visual states.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/fontmanager.cpp:465-528`
  - Code references: target pixel height, line spacing, screen scaling, width,
    fallback chain, `terminalFontChanged`.
  - Plan mapping: Apex text rendering needs deterministic sizing so labels,
    event rows, and buttons do not shift or overlap.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/fontmanager.cpp:541-584`
  - Code references: application font loading, family cache, base width
    calculation.
  - Plan mapping: any Apex bundled font path must include provenance, fallback,
    and layout measurement tests.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/fontlistmodel.h:10-21`
  - Code references: `FontEntry` shape.
  - Plan mapping: Apex profile store should use explicit structured data for
    font choices and avoid ad hoc string parsing.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/fontlistmodel.cpp:48-60`
  - Code references: QML roles `name`, `text`, `source`, `baseWidth`,
    `pixelSize`, `lowResolutionFont`, `isSystemFont`, `family`,
    `fallbackName`.
  - Plan mapping: Apex QML models should expose stable roles for all list-based
    controls.

### Timing, Performance, And Quality Anchors

- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/TimeManager.qml:22-45`
  - Code references: `FrameAnimation`, `effectsFrameSkip`, `framesPerUpdate`,
    elapsed time updates.
  - Plan mapping: Apex quality tiers need explicit frame pacing, battery/low
    effects modes, and offscreen fallback behavior.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/SettingsAdvancedTab.qml:72-149`
  - Code references: effects FPS, texture quality, bloom quality, burn-in
    quality.
  - Plan mapping: Apex should separate effect intensity from render cost and
    expose quality tiers: Cinematic, Balanced, Battery, Low Effects, Plain.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/ApplicationSettings.qml:48-53`
  - Code references: `effectsFrameSkip`, `bloomQuality`, `burnInQuality`.
  - Plan mapping: quality defaults should be persisted and validated.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/ShaderTerminal.qml:103-112`
  - Code references: `rasterizationIntensity` and bloom scaling.
  - Plan mapping: Apex effects should degrade gracefully at high pixel density
    and low capability.

### Desktop And Release Packaging Anchors

- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/README.md:22-30`
  - Code references: release artifacts and build documentation expectation.
  - Plan mapping: Apex visual release must include installable artifacts,
    verification notes, and clear build docs.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/cool-retro-term.desktop:1-16`
  - Code references: `.desktop` fields, categories, keywords, desktop action.
  - Plan mapping: Apex needs original desktop metadata with launcher actions
    for visual run, doctor, and safe dry run.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/packaging/appdata/cool-retro-term.appdata.xml:1-40`
  - Code references: AppStream component, metadata license, project license,
    summary, screenshots, release entry.
  - Plan mapping: Apex AppStream metadata must include its own description,
    screenshots, license fields, and release notes.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/app.pro:101-117`
  - Code references: install target and icon install locations.
  - Plan mapping: Apex packaging must install the binary, icon sizes, desktop
    file, AppStream metadata, and notices coherently.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/snap/snapcraft.yaml:1-17`
  - Code references: snap name/version/summary, confinement, app command,
    desktop entry, QML import path.
  - Plan mapping: useful only as packaging category evidence. Apex should not
    copy snap metadata and should prioritize AppImage/source install first.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/snap/snapcraft.yaml:18-70`
  - Code references: desktop helper part, Qt/QML build packages, stage
    packages.
  - Plan mapping: Apex release notes need a dependency inventory for Qt/PySide,
    plugins, graphics backends, and desktop integration.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/scripts/build-appimage.sh:1-33`
  - Code references: build dir, version, qmake check, AppDir creation, install
    targets.
  - Plan mapping: Apex AppImage build needs deterministic build dirs, version
    labeling, clean install roots, and no dependence on a source checkout at
    runtime.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/scripts/build-appimage.sh:37-47`
  - Code references: QML import relocation.
  - Plan mapping: Apex packaging must inspect bundled QML/PySide resources and
    avoid missing-plugin runtime failures.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/scripts/build-appimage.sh:50-82`
  - Code references: `linuxdeploy`, Qt plugin, platform plugins, excluded SQL
    libraries, AppImage output name.
  - Plan mapping: Apex AppImage release must record toolchain choices,
    excluded libraries, Qt plugins, checksum, and clean-machine evidence.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/packaging/debian/control:9-20`
  - Code references: Qt/QML build dependencies and runtime dependencies.
  - Plan mapping: Apex visual extra must keep graphical dependencies optional
    and absent from the base CLI install.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/packaging/rpm/cool-retro-term.spec:34-57`
  - Code references: RPM Qt build/runtime requirements.
  - Plan mapping: supports cross-distro dependency inventory and package
    verification.
- Source:
  `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/packaging/debian/cool-retro-term.1:15-43`
  - Code references: user-facing command options in man page.
  - Plan mapping: Apex visual packaging should document source install,
    AppImage invocation, profile selection, doctor, dry-run, live-run, and
    workdir/project path flags.

### Apex Design-To-Reference Traceability

| Apex plan item | Reference anchors |
| --- | --- |
| Preserve event-wrapper boundary | `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/README.md:11`, `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/PreprocessedTerminal.qml:24-37`, `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/PreprocessedTerminal.qml:96-128` |
| Split `Main.qml` into app shell/components | `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/main.qml:27-45`, `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/TerminalWindow.qml:26-52`, `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/TerminalTabs.qml:124-154` |
| Multi-stage render/effect pipeline | `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/ShaderTerminal.qml:72-200`, `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/app.pro:57-95`, `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/resources.qrc:51-112` |
| Event-row persistence/phosphor trail | `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/BurnInEffect.qml:24-128`, `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/shaders/burn_in.frag:21-36`, `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/shaders/terminal_dynamic.frag:161-166` |
| Bloom/glow/ambient frame | `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/TerminalContainer.qml:56-82`, `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/TerminalFrame.qml:24-49`, `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/shaders/terminal_static.frag:72-98` |
| Scanline/pixel/subpixel rendering modes | `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/ApplicationSettings.qml:104-110`, `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/SettingsTerminalTab.qml:56-72`, `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/shaders/terminal_dynamic.frag:66-117` |
| Profile persistence/import/export | `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/ApplicationSettings.qml:160-363`, `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/SettingsGeneralTab.qml:25-180`, `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/Storage.qml:24-88` |
| Font controls and stable text layout | `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/SettingsTerminalTab.qml:29-172`, `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/fontmanager.cpp:426-528`, `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/fontlistmodel.cpp:48-60` |
| Quality tiers and performance pacing | `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/TimeManager.qml:22-45`, `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/SettingsAdvancedTab.qml:72-149`, `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/ApplicationSettings.qml:48-53` |
| Desktop/AppImage release lane | `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/cool-retro-term.desktop:1-16`, `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/packaging/appdata/cool-retro-term.appdata.xml:1-40`, `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/scripts/build-appimage.sh:1-82` |
| Clean-room license gates | `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/packaging/debian/copyright:1-11`, `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/packaging/rpm/cool-retro-term.spec:19-25`, `/home/aiwithapex/projects/apex-infinite-cli/EXAMPLE/cool-retro-term/app/qml/resources.qrc:19-118` |

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
