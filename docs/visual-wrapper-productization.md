# Apex Infinite CLI Visual Wrapper Productization

## Status

The optional Linux source visual mode is the Apex Infinite Hyperterminal
surface. It is a PySide6/QML command surface over the base CLI workflow engine,
not a separate workflow engine and not a terminal-emulator viewport.

Source mode is implemented and verified through focused wrapper tests. The
repository includes original desktop metadata, AppStream metadata, icon assets,
shader sources, notices, a release checklist, and an AppImage build script.
Clean-machine AppImage launch evidence is still a release-session gate.

The base terminal CLI remains the workflow engine. The wrapper launches that
CLI with the guarded event-stream command and renders lifecycle state from
JSONL events:

```text
apex-infinite --event-stream - --machine-output ...
```

The wrapper must not parse Rich output, plain terminal text, SQLite history
rows, ANSI captures, or reference terminal frames.

The first viewport is the operator command surface. It is composed from the run
command strip, mission state rail, spec map, event core, signal panel, visual
profile drawer, and effect surface.

## Source Setup

Install the base CLI first:

```bash
cd apex-infinite-cli
python -m pip install -e .
```

Install the optional visual wrapper only when running the Linux visual mode:

```bash
python -m pip install -e ".[visual]"
```

The `visual` extra includes PySide6 and packaging review tooling in the
optional lane. The base CLI install stays free of Qt, PySide6, QML, graphical
display requirements, Nuitka, AppImage tooling, and wrapper assets.

## Run Commands

Fixture-backed source visual mode:

```bash
cd apex-infinite-cli
apex-infinite-visual --dry-run --max-iterations 1
```

Launch the real CLI subprocess from the wrapper:

```bash
apex-infinite-visual \
  --launch-cli \
  --path ~/projects/my-app/ \
  --start-command implement \
  --dry-run \
  --max-iterations 1
```

Use the productized visual settings from the command line:

```bash
apex-infinite-visual \
  --theme crt-amber \
  --effect-intensity 55 \
  --font-family "monospace" \
  --font-scale 1.05 \
  --reduced-effects \
  --plain-fallback
```

Headless smoke check:

```bash
QT_QPA_PLATFORM=offscreen apex-infinite-visual \
  --dry-run --max-iterations 1 --auto-close-ms 300
```

The wrapper sets `QT_QUICK_BACKEND=software` automatically when
`QT_QPA_PLATFORM=offscreen`.

## Settings

The Python settings model owns productized visual settings. QML consumes
settings through the bridge; normal QML rendering must not own duplicated
preset, schema, or fallback logic.

- `crt-green`, `crt-amber`, `ibm-dos`, and `plain` presets.
- Hyperterminal profiles: `apex-reactor`, `operator-amber`,
  `blueprint-dos`, `whiteout-lab`, `blackbox`, and `incident-red`.
- Rendering modes: `modern-crisp`, `scanline`, `pixel-grid`, `subpixel`, and
  `cinematic`.
- Quality tiers: `cinematic`, `balanced`, `battery`, `low-effects`, and
  `plain`.
- Effect intensity from 0 to 100.
- Effect toggles for glow, scanlines, flicker, curvature, bloom, persistence,
  noise, jitter, sync, chroma, and ambient frame.
- Font family as non-empty ASCII text.
- Font scale from 0.8 to 1.4.
- Font width from 0.8 to 1.25.
- Line spacing from 0.9 to 1.6.
- Reduced effects, which disables optional effects.
- Plain fallback, which switches to the plain preset and disables effects.

Plain fallback and reduced effects are hard fallbacks, not aesthetic profiles.
They must keep state visible through text, color, simple layout, and stable
status panels.

## Profile Persistence

Visual profiles are wrapper-only presentation state. They never contain
provider secrets and never touch shared CLI config without explicit user
confirmation.

Storage locations:

```text
${XDG_CONFIG_HOME:-~/.config}/apex-infinite/visual-profiles.json
${XDG_STATE_HOME:-~/.local/state}/apex-infinite/visual-state.json
```

Profile storage is JSON, ASCII-written, versioned, atomically persisted, and
backed up on corruption. Built-in profiles are derived from the Python settings
presets; custom profiles live in the XDG profile file.

Schema version 1 profile fields:

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

Known `effects` keys are `glow`, `scanlines`, `flicker`, `curvature`, `bloom`,
`persistence`, `noise`, `jitter`, `sync`, `chroma`, and `ambient_frame`.

Supported backend operations are save current, set last profile, duplicate,
rename, delete custom, reset built-in, import JSON, and export JSON. Profile
names are non-empty ASCII text up to 64 characters and cannot contain path
separators or control characters. Import rejects unsupported versions,
unknown effect keys, invalid settings values, and secret-looking fields.

The current QML drawer exposes save, load, and delete. Import, export,
duplicate, rename, and reset are backend/bridge capabilities that need drawer
controls if UI parity is required for release.

## Render Capabilities And Effects

Render capability detection is PySide6-free and runs before Qt imports. It
uses environment facts such as `QT_QPA_PLATFORM`, `QT_QUICK_BACKEND`,
`LIBGL_ALWAYS_SOFTWARE`, available compiled shader artifacts, and
`APEX_INFINITE_VISUAL_TIER`.

Capability output is event-safe and may be emitted as
`wrapper_capabilities_resolved`. The payload reports platform, backend,
offscreen state, shader availability, shader module names, recommended quality
tier, and whether reduced effects are forced.

QML-only source mode owns the current production visual path:

- Glow fields.
- Scanline, pixel-grid, and subpixel overlays.
- Phosphor trails for event-row persistence.
- Signal distortion with bounded intensity.
- Glass curvature.
- Ambient frame treatment.
- Event-reactive pulses for run start, provider health, decisions,
  iterations, stop, completion, and fault states.

Shader source modules are clean-room GLSL 440 files under
`src/apex_infinite_visual/shaders/` with provenance in
`src/apex_infinite_visual/shaders/PROVENANCE.md`. Compiled `.qsb` files are
ignored local build outputs unless a release explicitly promotes reviewed
compiled artifacts into package data and the QML render path.

## Graphical First Run And Doctor

`src/apex_infinite_visual/doctor.py` provides display-safe pass, warn, and
fail diagnostics for launch readiness. Doctor facts may be surfaced as
`doctor_started`, `doctor_check`, and `doctor_finished` events.

The current first-run surface is a banner plus doctor/dry-run guidance. A full
graphical shared-config write flow is still release work. That flow must:

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

The first-run flow must stay inside the same command shell; it must not become
a separate plain wizard that feels like another product.

## Failure States

The wrapper renders or reports these product-facing states:

| Condition | Surface |
|-----------|---------|
| PySide6 missing | Entrypoint prints `Visual wrapper unavailable` with install guidance. |
| Display backend unavailable | Entrypoint reports a display or Qt runtime unavailable state. |
| Missing base CLI module | QML failure state: `CLI missing`. |
| Invalid project path | QML failure state: `Project unavailable`. |
| Malformed JSONL | QML failure state: `Malformed event`. |
| Subprocess timeout | QML failure state: `Timed out`. |
| Subprocess stderr | QML failure state: `Subprocess stderr`. |
| Non-zero subprocess exit | QML failure state: `Process failed`. |
| Operator stop | QML state: `Stopped`. |

The wrapper keeps stderr separate from stdout JSONL. Stderr is summarized before
display. Event payload validation still excludes secrets, ANSI escapes,
Rich markup, frame glyphs, and visual token values.

## Smoke And Verification

Recommended source checks before release verification:

```bash
cd apex-infinite-cli
./.venv/bin/python -m pytest tests/test_visual_wrapper_spike.py \
  tests/test_visual_wrapper_productization.py -v
./.venv/bin/python -m py_compile \
  src/apex_infinite_visual/__init__.py \
  src/apex_infinite_visual/events.py \
  src/apex_infinite_visual/launcher.py \
  src/apex_infinite_visual/main.py \
  src/apex_infinite_visual/settings.py
./.venv/bin/pyside6-qmllint src/apex_infinite_visual/qml/Main.qml
QT_QPA_PLATFORM=offscreen ./.venv/bin/apex-infinite-visual \
  --dry-run --max-iterations 1 --auto-close-ms 300
```

If `pyside6-qmllint` is unavailable because optional wrapper dependencies are
not installed, record that exact environment blocker before release
verification. Do not move PySide6 into the base dependency set to make the
check pass.

## Packaging Path

The intended Linux binary path is:

1. Build and review the source visual mode.
2. Build an isolated AppDir using `scripts/build-appimage.sh`.
3. Inspect generated files, collected Qt plugins, bundled wheels, QML
   resources, and licenses.
4. Wrap the reviewed Linux output as
   `apex-infinite-visual-linux-x86_64.AppImage` only after license review.
5. Publish SHA256 checksums and source/dev install instructions with the
   binary artifact.

`pyside6-deploy` was evaluated as the first candidate. The current AppImage
script uses a venv-in-AppDir approach because it keeps bundled wheels
byte-auditable and keeps LGPL replacement/relink review straightforward.

Do not commit generated packaging outputs unless a later release session
explicitly scopes them.

## License And Release Gates

Before publishing a binary artifact:

- Confirm the selected Qt for Python license path: LGPLv3-compatible or
  commercial.
- Include required Qt/PySide6 notices.
- Confirm no GPL-only Qt modules are bundled.
- Confirm the AppImage does not block required library replacement or relink
  rights.
- Provide source availability or relink/replacement instructions required by
  the chosen license path.
- Publish SHA256 checksums for the final artifact.
- Keep the base dependency set independent of PySide6 and graphical display
  dependencies.

Experienced legal review is recommended when there is doubt about LGPLv3,
commercial Qt terms, generated bundle contents, or AppImage replacement rights.

## Clean-Room Verification

Tracked wrapper source, tests, docs, and release assets must not include copied
reference source code, QML, shaders, shader constants, generated shader blobs,
images, icons, fonts, profile data, resource manifests, build scripts,
terminal-emulator code, qmltermwidget, or QTermWidget material.

Use these checks during implementation and release verification:

```bash
git ls-files | grep '^EXAMPLE/' && exit 1 || true
LC_ALL=C git ls-files apex-infinite-cli | xargs -r grep -nP '[^\x00-\x7F]' || true
git diff --check
```

The local `EXAMPLE/` tree remains ignored reference material only. It is not a
runtime dependency and not a source for implementation details.

## Current Release Position

Source mode has focused checks for optional dependency isolation, event-stream
boundaries, clean-room scans, dependency audit evidence, visual state, profile
persistence, render capabilities, doctor diagnostics, and license-gate
documentation.

The current AppImage script uses the venv-in-AppDir packaging path. A binary
release must still verify generated bundle contents, AppImage behavior,
notices, checksums, dependency inventory, source/relink instructions, and
clean-room boundaries before publishing any artifact.
