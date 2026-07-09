# Apex Infinite CLI - UX Requirements Document

**Companion to**: [PRD.md](PRD.md)
**Created**: 2026-07-02
**Status**: Authoritative standalone UX source for the Apex Infinite CLI UI upgrade and Apex Infinite Hyperterminal design lane

This document is intended to survive deletion of the original research inputs.
It incorporates the relevant UX facts from the local retro-terminal reference
tree, the Apex Infinite CLI upgrade plan, the current CLI implementation, and
the current CLI docs. Future planning and implementation should use this file
and `PRD.md` as the durable product source of truth.

---

## 1. Design Brief

### Emotional Targets

Focused command, accountable momentum, reactive depth, Linux-native authority.

The interface should make a long autonomous development run feel controlled and
observable. The retro mood is a disciplined operator-console layer, not a toy
theme. Every visible element must help the operator understand state, risk,
current work, captured output, or the next handoff. The visual app should feel
like a production Linux command center, not a website, landing page, or generic
dashboard.

### Aesthetic Identity

- **Reference domain**: Mission-control terminal benches, service monitors,
  and late mainframe operator consoles.
- **Era / movement**: Late-1970s and early-1980s CRT computing interpreted
  through Swiss information hierarchy.
- **Material metaphor**: Phosphor text behind smoked glass inside a black metal
  instrument rack.

The visual source material established useful concepts: profile-driven terminal
moods, terminal frame composition, screen/effect/performance settings groups,
operator-oriented menus, persistent settings, viewport status overlays, and a
render pipeline split between source content, dynamic effects, static effects,
and frame treatment. Apex Infinite CLI must translate those ideas clean-room
into independent CLI tokens, labels, layouts, tests, docs, and optional wrapper
code. Do not copy reference source, QML, shader code, shader constants, compiled
shader blobs, colors, profile data, images, icons, fonts, resource manifests,
build scripts, or terminal-emulator code.

### Signature Moment

The screenshot-worthy moment is the Hyperterminal command surface during an
active run: the run command strip is armed, the mission state rail shows
provider/model/spec status, the event core receives a manager decision pulse,
the spec map shows phase/session progress, and the signal panel isolates any
stderr, timeout, malformed event, or provider fault without hiding the command
log.

### Micro-Narrative

Arrival -> Orientation -> Engagement -> Action -> Resolution

```text
Launch/config -> Boot panel or first-run setup -> Command surface
              -> Manager decision -> Prompt preview -> Codex execution
              -> Event core and signal panel -> Next command, pause,
                 completion, doctor action, or safety stop
```

The user should feel that the system is booting an autonomous instrument,
establishing context, acting visibly, recording its work, and handing off to the
next command without drama.

### Experience Principles

- Legibility beats novelty in every theme.
- Every visual element carries operational information.
- Terminal-first behavior remains scriptable, headless-safe, and plain-output
  compatible.
- Styled output never becomes stored workflow data.
- The first visual screen is the actual command surface, not a product tour.
- Rich visual effects are allowed by default when the machine supports them,
  but reduced-effects and plain modes must stay readable and intentional.
- Effects react to real workflow facts, not arbitrary decoration.
- Apex Infinite Hyperterminal is a companion display for the same workflow
  engine, not a fork of the CLI behavior.

---

## 2. Source Digest And Current Baseline

This section preserves the source-derived facts that would otherwise be lost if
the planning document and local example tree are removed.

### Product Context

Apex Infinite CLI is a Python CLI that repeatedly:

```text
read recent SQLite history -> summarize history -> ask manager LLM
                            -> route decision -> run codex exec
                            -> log result -> repeat
```

The loop stops when the manager emits `alldonebaby`, when the max iteration
limit is reached, when the operator quits from an emergency prompt, or when the
process is externally terminated.

### Current Implementation Baseline

The current implementation is a packaged Click application in
`src/apex_infinite/cli.py`, with rendering in `src/apex_infinite/ui.py`, event
streaming in `src/apex_infinite/events.py`, and the optional visual wrapper in
`src/apex_infinite_visual/`.

- Runtime dependencies already include Click, Rich, OpenAI Python SDK,
  python-dotenv, PyYAML, SQLite from the Python standard library, and Codex CLI.
- A global Rich `Console()` currently owns terminal output.
- `src/apex_infinite/config.yaml` defines provider, Codex, and UI settings.
- Supported provider names are `ollama`, `grok`, and `openai`.
- Codex settings include binary, exec flags, and model reasoning effort.
- Main CLI options today are `--path`, `--start`, `--ceo`, `--provider`,
  `--model`, `--config`, `--history`, `--max-iterations`, `--dry-run`,
  `--verbose`, `--theme`, `--plain`, `--ascii`, `--compact`,
  `--check-provider`, `--check-provider-chat`, `--skip-provider-check`,
  `--event-stream`, `--machine-output`, and `--version`.
- If `--path` is absent, the CLI lists directories under `~/projects/`, accepts
  a number or path, prompts for optional start command, and prompts for optional
  CEO instructions.
- The project path is expanded, checked for existence, normalized to one
  trailing slash, and used as the SQLite history key.
- The default max iteration limit is 50.
- Each Codex command has a 30-minute timeout.
- `execute_codex()` currently uses `subprocess.run(..., capture_output=True)`.
  It returns stdout, falls back to stderr when stdout is empty, wraps non-zero
  exits, reports timeout, reports missing binary, and reports generic
  exceptions.
- `--dry-run` prints the `codex exec` command that would be launched and returns
  a dry-run response without launching Codex.
- `--verbose` currently expands the visible agent response after execution.
- `--history` currently prints up to 50 rows through a Rich table.
- The SQLite DB lives at `~/.apex-infinite/history.db`, uses WAL mode, and
  stores one `history` table with `id`, `path`, `cc_response`,
  `ai_decision_output`, `ai_decision_reason`, `help_or_done_msg`, and
  `created_at`.
- The legacy `cc_response` column must stay intact for backward compatibility.
- The manager recognizes 14 Apex Spec commands for prompt generation:
  `initspec`, `createprd`, `createuxprd`, `plansession`, `implement`,
  `creview`, `validate`, `updateprd`, `audit`, `pipeline`, `infra`,
  `carryforward`, `documents`, and `phasebuild`.
- The normal autonomous manager loop is scoped to initialized projects and
  normally chooses post-initialization workflow commands.
- Known commands are converted to `Run the apex-spec skill command /<command>`.
  Unknown outputs are sent to Codex as raw instructions.
- Manager output is normalized by trimming whitespace, lowercasing for routing,
  and stripping a leading slash before command matching.
- `help` is an emergency operator pause, not normal workflow routing.
- `Ctrl+C` once requests a pause at the next loop boundary; a second interrupt
  can force quit.
- `notify-send` is used opportunistically for Linux desktop notifications, but
  terminal output remains authoritative.
- Current tests cover prompt routing, config, flags, renderer behavior, history
  display, environment fallbacks, subprocess display, provider preflight, event
  output, and optional wrapper behavior.

### Hyperterminal Design Lane

The production visual app is Apex Infinite Hyperterminal. This name describes
the visual mode only; command names remain `apex-infinite` and
`apex-infinite-visual` unless a later release explicitly renames them.

The final visual architecture is layered:

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

The visual wrapper must not own manager decisions, prompt building, Codex
execution, history logging, stop conditions, or safety behavior. It may own
presentation state, visual preferences, layout state, profile persistence, and
explicitly confirmed shared config writes.

The first viewport is the operator console. The primary zones are:

- **Run Command Strip**: Project path selector, start command selector,
  dry-run/live-run segmented control, max-iteration stepper, start, stop,
  resume, doctor, and autonomy summary.
- **Mission State Rail**: Run status, stage, iteration, provider, model, Codex
  binary, config source, event stream mode, and history DB status.
- **Spec Map**: `.spec_system/` status, phase/session identity, current
  command, task checklist progress, carry-forward warnings, and validation
  status when events provide them.
- **Event Core**: Virtualized structured event rows for startup, provider
  preflight, manager decision, command, response, pause, error, stop,
  completion, and summary states, with search, filter, pin, copy, and export.
- **Signal Panel**: Provider health, recent stderr summary, malformed event
  count, runtime duration, last machine event, and safe artifact links.
- **Visual Profile Drawer**: Theme family, rendering mode, quality tier, effect
  intensity, font family, font scale, font width, line spacing, reduced effects,
  plain fallback, save, duplicate, import, export, and reset.

Proposed Python modules for the visual lane are `profile_store.py`,
`render_caps.py`, `visual_state.py`, `doctor.py`, and `assets.py`. Proposed QML
families are shell components, command-surface components, reusable controls,
and original Apex effect components.

### Planned UX Commitments

The UI upgrade must add a renderer/config/event boundary without changing the
workflow contract unless a session explicitly changes prompt behavior and
updates code, tests, README, and prompt-contract docs together.

New UI configuration requirements:

```yaml
ui:
  theme: "auto"
  effect_level: "low"
  ascii: false
  compact: false
  show_elapsed: true
  show_provider: true
  themes: {}
```

New or planned CLI overrides:

```bash
apex-infinite --theme crt-amber
apex-infinite --plain
apex-infinite --ascii
apex-infinite --compact
apex-infinite --event-stream /tmp/apex-infinite-events.jsonl
apex-infinite --event-stream - --machine-output
```

Configuration precedence:

```text
CLI flags -> environment constraints -> config.yaml -> built-in defaults
```

Resolution rules:

- Built-in default theme is `auto`.
- `auto` resolves to `crt-green` on capable interactive TTYs.
- `auto` resolves to `plain` for `NO_COLOR`, `TERM=dumb`, non-TTY output,
  redirected output, or a non-terminal Rich console path.
- `--plain` forces plain theme, color disabled, and effect level off.
- `NO_COLOR` behaves like plain mode unless the operator explicitly opts back
  into a theme.
- `--ascii` changes glyph selection only; it does not automatically disable
  color.
- `--compact` reduces vertical space but must not hide errors, manager reasons,
  command prompts, completion state, help, interrupts, or timeouts.
- Invalid `--theme`, `ui.theme`, and malformed `ui.themes` values fail fast
  with clear Click/config errors. Invalid user configuration must not silently
  fall back to `plain`.
- `--event-stream PATH` writes line-buffered JSONL events to a file without
  changing normal human output.
- `--machine-output` is the explicit human-rendering disable mode. It requires
  `--event-stream`, disables Rich/plain human rendering, disables terminal bell
  and desktop notifications, and makes stdout machine-readable only.
- `--event-stream -` is allowed only with `--machine-output`, so JSONL never
  mixes with Rich or plain human output.

Hyperterminal visual commitments:

- The visual app uses the CLI as the workflow engine and consumes registered
  events or an importable event API; it never scrapes Rich output, plain
  terminal text, SQLite history rows, ANSI captures, or terminal-control
  sequences.
- Wrapper-only visual settings are stored under
  `${XDG_CONFIG_HOME:-~/.config}/apex-infinite/visual-profiles.json`.
- Runtime window state can be stored under
  `${XDG_STATE_HOME:-~/.local/state}/apex-infinite/visual-state.json`.
- Visual profile schema includes version, name, theme name, rendering mode,
  quality tier, effect intensity, font family, font scale, font width, line
  spacing, reduced effects, plain fallback, effect toggles, and layout density.
- Profile operations include save current, duplicate, rename, delete custom,
  reset built-in, import JSON, export JSON, validate schema/version, reject
  non-ASCII names for now, and never write provider secrets.
- Quality tiers are Cinematic, Balanced, Battery, Low Effects, and Plain.
- Rendering modes are `modern-crisp`, `scanline`, `pixel-grid`, `subpixel`,
  and `cinematic`.
- First-run setup detects missing shared CLI config, presents provider choices,
  captures model and Codex binary, chooses a project, runs doctor, defaults to
  dry run, and requires explicit confirmation before writing shared CLI config.
- Desktop productization includes original icon, `.desktop` file, AppStream
  metadata, launcher actions, AppImage artifact, SHA256 checksum, dependency
  inventory, Qt/PySide6 notices, and clean-machine verification.
- `pyside6-deploy` was evaluated first for packaging. The current AppImage path
  uses a venv-in-AppDir bundle so the shipped PyPI wheels remain byte-auditable
  and the Qt/PySide6 LGPL replacement/relink path stays explicit.

### External Verification Facts

These facts were checked on 2026-07-02 and are captured here for durable
implementation planning.

- PySide6 is the official Qt for Python binding and is available under open
  source LGPLv3/GPL licensing or a commercial license.
- Qt recommends experienced legal review for LGPL compliance when there is any
  doubt; the wrapper must document LGPLv3/commercial obligations and avoid
  GPL-only Qt modules.
- PyQt remains excluded because GPL-incompatible distribution requires a
  commercial PyQt license.
- Qt for Python ships `pyside6-deploy`, a Nuitka-based deployment helper that
  produces a Linux `.bin` executable. The current release path instead wraps a
  reviewed venv-in-AppDir bundle into an AppImage unless a later release
  records a better packaging decision.
- Qt Quick `ShaderEffect` supports custom vertex and fragment shaders in QML,
  but effects may not render with unsupported scene graph backends such as the
  software backend. The wrapper must detect this and fall back to a beautiful
  low-effects scene instead of failing.
- AppImage is the selected first binary release format because it gives upstream
  control, one file, no root install, and no package-manager ceremony.
- pywebview is a lightweight native webview wrapper for HTML/CSS/JS desktop
  interfaces, while xterm.js is a browser terminal-emulation component. Together
  they are a backup only if a future requirement demands an interactive
  terminal emulator.

### Reference-Derived Visual Concepts

The local retro-terminal reference established the following reusable ideas.
They are requirements as concepts only, not implementation data.

- Profile families: amber CRT, green CRT, DOS-like high contrast, blue/cyan
  variants, old computer moods, minimal "boring" mode, and e-ink-like quiet
  mode. Apex Infinite CLI first ships `auto`, `crt-green`, `crt-amber`,
  `ibm-dos`, and `plain`. Hyperterminal adds Apex-owned profiles:
  `apex-reactor`, `operator-amber`, `blueprint-dos`, `whiteout-lab`,
  `blackbox`, and `incident-red`.
- Settings organization: general/profile settings, terminal/font settings,
  effects settings, advanced/performance settings, import/export/persistence,
  and small reusable controls.
- Terminal viewport concepts: source content, scroll position, selection,
  focus, paste/copy affordances, terminal size feedback, zoom/scaling, and
  stable status display.
- Effect categories: bloom, glow, burn-in trails, static/noise, jitter,
  flicker, scanlines/rasterization, horizontal sync, RGB shift, curvature,
  ambient light, frame size, frame color, and frame shine.
- Performance controls: effects FPS, texture quality, bloom quality, burn-in
  quality, and low-effects fallbacks.
- Render pipeline concepts: source terminal surface, optional bloom source,
  dynamic effect pass, static final pass, frame pass, frame buffer, and timing
  driver. Hyperterminal translates this into an independent QML scene graph
  with explicit event source, state compositor, effect buffer, postprocess
  pass, and presentation frame.
- Wrapper controls: theme selector, effect intensity, font/scaling, reduced
  effects, plain fallback, copy/log actions, settings import/export, fullscreen,
  and zoom.
- Packaging concepts: graphical wrapper dependencies and release artifacts must
  be documented separately from base CLI installation.

Clean-room limits:

- Rich may translate only mood, hierarchy, labels, simple separators, and
  settings vocabulary.
- The Linux wrapper ships as the Phase 02 Hyperterminal design lane. It should
  independently implement glow, scanlines, flicker, curvature, trails, frame
  treatment, quality tiers, and event-reactive effects after the event boundary
  is available.
- The base CLI must not require Qt, PySide6, PyQt, qmltermwidget,
  QTermWidget, a graphical display, an external terminal emulator, or the
  reference application.
- The selected wrapper path is PySide6 with Qt Quick/QML as an optional
  Linux-only extra. PyQt, qmltermwidget, QTermWidget, copied QML, copied
  shaders, generated reference shader blobs, copied assets, copied fonts,
  copied profile data, copied manifests, copied package metadata, copied build
  scripts, and copied terminal-emulator code are excluded.
- The first binary wrapper artifact is an x86_64 Linux AppImage named in the
  pattern `apex-infinite-visual-linux-x86_64.AppImage`, published with SHA256
  checksums, license notices, and a separate source/dev install path through
  the optional Python extra.

---

## 3. User Flows

### Flow 1: Interactive Project Selection And Startup

**Trigger**: Operator runs `apex-infinite` with no `--path`.
**Goal**: Choose a project and enter the autonomous loop with clear context.

```text
Launch -> Config resolution -> Project list or path prompt
      -> Optional start command -> Optional CEO instruction
      -> Boot panel -> Iteration 1
```

**Happy path**: The user sees resolved provider, model, project path, max
iterations, dry-run state, UI mode, start command, and CEO instruction presence
before work begins.
**Error states**: Missing config, unknown provider, missing API key value,
invalid theme/config, invalid project selection, and nonexistent directory fail
before loop execution.

### Flow 2: Direct Or Resume Autonomous Run

**Trigger**: Operator runs with `--path`, optionally `--start` and `--ceo`.
**Goal**: Start or resume a target project without interactive prompts.

```text
CLI flags -> Config/UI resolver -> Path normalization -> Boot panel
          -> Fetch history -> Manager decision or start override
          -> Prompt preview -> Codex execution -> DB log
          -> Next iteration or stop
```

**Happy path**: The operator can confirm project identity and first action from
the boot panel and first iteration frame.
**Error states**: Invalid config, invalid path, invalid theme, missing Codex
binary, provider retry exhaustion, timeout, and non-zero Codex exit render with
severity labels and raw stored facts.

### Flow 3: Dry-Run Confidence Check

**Trigger**: Operator passes `--dry-run`.
**Goal**: Verify route, prompt, provider/model, config, UI mode, and exact
Codex command without launching Codex.

```text
Launch -> Config/UI resolver -> Boot panel -> Manager/start decision
      -> Prompt preview -> Dry-run command panel -> DB log
      -> Next iteration or safety stop
```

**Happy path**: Output clearly says no Codex subprocess was launched and shows
the command that would run.
**Error states**: Invalid config, invalid theme, and invalid project path fail
before the dry-run command panel appears.

### Flow 4: Known Command Routing

**Trigger**: Manager emits a known Apex Spec command or a slash-prefixed known
command.
**Goal**: Run the correct Codex prompt while preserving prompt-contract tests.

```text
Manager JSON/raw output -> Normalize -> Known command?
    yes -> Build skill command prompt -> Preview -> codex exec
    no  -> Send raw instruction -> Preview -> codex exec
```

**Happy path**: Known commands are labeled as workflow commands; custom outputs
are labeled as raw instructions.
**Error states**: Malformed manager JSON falls back to regex or raw output and
shows that fallback clearly without hiding the routed output.

### Flow 5: Monitor Long Codex Execution

**Trigger**: A non-dry-run iteration launches `codex exec`.
**Goal**: Keep the operator aware of active work while preserving captured
stdout/stderr semantics.

```text
Prompt dispatch -> Process start -> Elapsed status
                -> stdout success | stderr fallback | non-zero exit
                -> timeout | missing binary | generic exception
                -> Response panel -> DB log
```

**Happy path**: A live status line or equivalent shows command state, elapsed
time, timeout threshold, binary name, and current operation.
**Error states**: Timeout, non-zero exit, missing binary, generic exception,
and interrupted runs have text labels, plain fallbacks, and raw DB rows.

### Flow 6: Inspect History Ledger

**Trigger**: Operator passes `--history`, optionally with `--path` and
`--verbose`.
**Goal**: Review recent workflow state without horizontal scrolling.

```text
History flag -> Optional path filter -> Compact ledger
             -> Verbose row expansion when --verbose is present
```

**Happy path**: Default history uses ID, timestamp, project, manager output,
status/help marker, concise reason, and truncated response summary. Verbose
history expands reason and response detail.
**Error states**: Empty history, sparse legacy rows, long paths, long reasons,
and long responses remain readable at 80 columns.

### Flow 7: Emergency Help Or Operator Interrupt

**Trigger**: Manager emits `help`, or the operator presses `Ctrl+C` once.
**Goal**: Pause visibly without corrupting workflow state.

```text
Help/interrupt -> Alert block -> Optional desktop notification
               -> Operator input or quit -> Continue/log or stop
```

**Happy path**: The prompt states whether the system is waiting for input, why
it paused, and whether the response becomes CEO instructions.
**Error states**: A second `Ctrl+C` can still force quit. A normal pause and a
force quit are visibly different.

### Flow 8: Plain, ASCII, Compact, And Automation Output

**Trigger**: Operator passes `--plain`, `--ascii`, or `--compact`; environment
sets `NO_COLOR`; terminal is dumb, non-TTY, redirected, or test-injected.
**Goal**: Keep output deterministic and readable outside rich interactive
terminals.

```text
Environment/flags -> UI resolver -> Plain/ascii/compact renderer
                  -> Same semantic states -> Raw DB/events unchanged
```

**Happy path**: Logs contain plain text labels and no ANSI escapes, Rich markup,
box glyphs, or carriage-return-only live output.
**Error states**: Plain mode must still show errors, timeouts, help,
interrupts, manager reasons, prompt previews, DB log notices, and completion.

### Flow 9: Emit Lifecycle Events For Visual Surfaces

**Trigger**: Operator passes `--event-stream PATH`, or Hyperterminal launches
the CLI as a subprocess.
**Goal**: Provide raw machine-readable lifecycle facts without scraping human
output.

```text
CLI launch -> Event emitter open -> Lifecycle JSONL writes
          -> Human renderer remains separate
          -> Wrapper/test consumes events
```

**Happy path**: Events include startup, config/UI resolution, iteration
lifecycle, history summary, manager decision, prompt dispatch, subprocess
lifecycle, output summary, DB log, help, interrupt, completion, timeout, error,
and stop states.
**Error states**: `--event-stream -` is rejected unless `--machine-output` is
present. Event write failures are emitted as machine-readable errors in
machine-output mode and as visible human errors otherwise.

### Flow 10: Configure A Visual Theme

**Trigger**: Operator edits `config.yaml` or passes `--theme`, `--plain`,
`--ascii`, `--compact`, or Hyperterminal settings.
**Goal**: Select a readable presentation without changing workflow behavior.

```text
Config/flags -> Validate theme names and overrides
             -> Resolve environment constraints -> Render token set
             -> Same workflow engine and storage
```

**Happy path**: Built-in themes and valid custom overrides apply consistently
to boot, iteration, history, errors, and completion.
**Error states**: Invalid names or malformed override values fail fast with the
invalid field and accepted values.

### Flow 11: Operate Apex Infinite Hyperterminal

**Trigger**: Operator launches `apex-infinite-visual` from source install,
desktop launcher, or AppImage.
**Goal**: Run the same autonomous workflow through a full-window visual command
surface.

```text
Launch -> Resolve visual profile -> Detect render capabilities
      -> Command surface -> Start or resume -> Event adapter
      -> Visual state store -> Mission rail, spec map, event core,
         signal panel, and effects
```

**Happy path**: The first screen is usable. The operator can select project,
mode, command, max iterations, and doctor/start/stop/resume actions while the
event core and status panels update from registered lifecycle events.
**Error states**: Missing CLI, missing PySide6, malformed JSONL, missing Codex,
missing provider config, shader unsupported, software backend, non-zero exit,
and timeout show visible recovery states without crashing or scraping terminal
frames.

### Flow 12: Manage Visual Profiles

**Trigger**: Operator opens the visual profile drawer.
**Goal**: Persist, reuse, and exchange visual settings without touching secrets
or shared workflow behavior.

```text
Open drawer -> Change profile/rendering/quality/font/effects/layout
           -> Save, duplicate, import, export, reset, or delete
           -> Validate schema -> Atomic write or visible error
```

**Happy path**: Restarting the app restores the selected visual profile, custom
profiles can be exported/imported, and built-in profiles can be reset.
**Error states**: Corrupt JSON, unsupported schema version, non-ASCII profile
name, invalid quality tier, invalid rendering mode, and failed write preserve a
backup when possible and never modify provider secrets.

### Flow 13: Graphical First Run And Doctor

**Trigger**: A clean Linux user opens the visual app without complete shared CLI
config, or clicks Doctor.
**Goal**: Configure enough state to run safely and understand launch readiness.

```text
Detect missing config -> Provider/model/Codex/project steps
      -> Codex flag compatibility -> Doctor checks
      -> Pass/warn/fail summary -> Dry-run default
      -> Explicit config write confirmation
```

**Happy path**: The user can choose provider, model, Codex binary, project, run
doctor, see pass/warn/fail results, and start with dry run without editing
source files.
**Error states**: Missing provider key, missing Codex, incompatible flags,
invalid project, config write denial, and doctor failure remain actionable and
do not start live mode accidentally.

### Flow 14: Desktop Launch And AppImage Verification

**Trigger**: Operator launches from `.desktop` metadata, AppStream entry,
launcher action, or the AppImage.
**Goal**: Start the visual app from normal Linux desktop surfaces with
documented release evidence.

```text
Launcher/AppImage -> Runtime dependency check -> Command surface
                  -> Doctor or safe dry run -> Clean shutdown
```

**Happy path**: Desktop launcher opens the app, AppImage does not depend on the
source checkout or repo `.venv`, checksum/notices are published, and safe dry
run is available when feasible.
**Error states**: Missing Qt plugin, missing provider config, missing Codex,
failed AppImage mount, and missing display/backend support produce a visual
failure state or documented CLI error, not an unexplained crash.

---

## 4. Screen Inventory

For this product, "screen" means a distinct terminal surface, output mode,
event surface, or Hyperterminal view.

| Screen | Entry/Route | Purpose | Key Components |
|--------|-------------|---------|----------------|
| Interactive Project Selection | `apex-infinite` with no `--path` | Select project, starting command, and CEO instruction | Project list, number/path prompt, validation error |
| Config Error Surface | Startup/config load | Fail before loop execution on invalid setup | Error label, invalid field, accepted values, source file |
| Boot Status Panel | Normal and dry-run startup | Establish operational context | Project, provider, model, config path, theme, max iterations, dry-run, start command |
| Iteration Frame | Main loop | Group one autonomous cycle | Iteration, operation, elapsed time, provider/model, project, dry-run |
| History Summary Notice | Iteration start | Show memory context preparation | Prior row count, summarizer status, retry label |
| Manager Decision Panel | After manager response | Separate manager choice from Codex output | Output command/instruction, reason, known/custom label, parse fallback label |
| Prompt Preview | Before Codex execution | Show what will be sent to Codex without flooding output | Truncated prompt, command class, custom instruction marker |
| Codex Execution Status | During subprocess | Show active process and elapsed time | Binary, timeout threshold, elapsed time, process state |
| Agent Response Panel | After subprocess | Summarize captured output | Truncated response, verbose expansion, stderr fallback, error state |
| DB Log Notice | End of iteration | Confirm durable history write | Project key, manager output, timestamp/status |
| Help Pause | `help` decision | Request external operator input | Alert label, reason, input prompt, notification note |
| Interrupt Pause | `Ctrl+C` once | Collect new CEO instruction after current step | Alert label, input prompt, quit option |
| Completion State | `alldonebaby` | End workflow visibly | Completion label, reason, iteration count, DB marker |
| Max Iteration Stop | Safety limit reached | Stop runaway loops safely | Warning, max count, next operator action hint |
| Timeout/Error State | Subprocess or provider failure | Make failure unmistakable | Severity label, raw reason, recovery hint |
| History Ledger | `--history` | Review recent interactions | Compact rows, optional path filter, verbose detail, empty state |
| Plain Output Mode | Auto or `--plain` | Serve logs, CI, non-TTY, dumb terminals | Line labels, no ANSI, no box glyphs, no live-only UI |
| ASCII Output Mode | `--ascii` | Avoid non-ASCII glyphs while allowing color if supported | ASCII separators, ASCII status markers |
| Compact Output Mode | `--compact` | Reduce vertical space without losing semantics | Short labels, fewer blank lines, no hidden critical states |
| Event Stream | `--event-stream PATH` | Machine-readable lifecycle boundary | JSONL events, raw payload facts, no markup |
| Hyperterminal Command Surface | `apex-infinite-visual` | Operate the visual Linux app from the first viewport | Run command strip, mission state rail, spec map, event core, signal panel, visual profile drawer |
| Run Command Strip | Hyperterminal main window | Start, stop, resume, dry-run/live-run, doctor, and command setup | Project selector, command selector, mode segmented control, max-iteration stepper, autonomy summary |
| Mission State Rail | Hyperterminal main window | Keep run state visible while events stream | Status, stage, iteration, provider, model, Codex binary, config source, event stream, history DB |
| Spec Map | Hyperterminal main window | Show Apex Spec project and workflow progress | `.spec_system/` status, phase/session, current command, task progress, validation/carry-forward warnings |
| Event Core | Hyperterminal main window | Render structured lifecycle rows | Virtualized log rows, search, filter, pin, copy, export, event classes |
| Signal Panel | Hyperterminal main window | Isolate health and faults | Provider health, stderr summary, malformed event count, duration, last event, safe artifact links |
| Visual Profile Drawer | Hyperterminal main window | Configure persisted visual-only preferences | Profile, rendering mode, quality tier, effects, font, layout, import/export/reset |
| Graphical First Run | Hyperterminal startup | Configure clean Linux setup before first dry run | Provider/model/Codex/project steps, doctor, dry-run default, config write confirmation |
| Graphical Doctor | Hyperterminal startup or toolbar | Diagnose launch readiness | Pass/warn/fail rows, Codex flags, provider checks, recovery actions |
| Desktop Launch Surface | `.desktop`, AppStream, AppImage | Start visual app from Linux desktop packaging | Launcher actions, AppImage runtime checks, notices, checksum expectations |
| Wrapper Failure Surface | Hyperterminal | Show subprocess, capability, or malformed-event failures | Missing CLI, missing PySide6, non-zero exit, timeout, malformed JSONL, shader fallback, reconnect guidance |

---

## 5. Navigation Structure

```text
apex-infinite
|-- Interactive startup
|   |-- Project selection
|   |-- Start command prompt
|   \-- CEO instruction prompt
|-- Direct run
|   |-- Boot status panel
|   |-- Iteration loop
|   |   |-- History summary
|   |   |-- Manager decision
|   |   |-- Prompt preview
|   |   |-- Codex execution
|   |   |-- Response panel
|   |   \-- DB log
|   |-- Help or interrupt pause
|   \-- Completion, timeout, error, or max-iteration stop
|-- Dry run
|   \-- Same semantic loop with no Codex subprocess launch
|-- History
|   \-- Compact ledger with optional verbose expansion
|-- Event stream
|   \-- JSONL side channel for wrappers/tests
\-- apex-infinite-visual
    |-- Graphical first run and doctor
    |-- Hyperterminal command surface
    |   |-- Run command strip
    |   |-- Mission state rail
    |   |-- Spec map
    |   |-- Event core
    |   |-- Signal panel
    |   \-- Visual profile drawer
    |-- Desktop launcher and AppImage entry points
    \-- Failure surface and fallback modes
```

**Navigation pattern**: CLI flags determine entry mode. Inside normal runs, the
only interactive navigation is startup selection and emergency help/interrupt
input.

**Deep linking**: Project history is scoped by normalized project path. Event
streams are addressed by file path. Hyperterminal views consume event names and
payloads, not Rich terminal frames.

**State ownership**: The CLI workflow engine owns manager decisions, prompt
building, Codex execution, history logging, stop conditions, and safety
behavior. Renderers and wrappers display this state but do not fork it.

---

## 6. Interaction Patterns

### Forms And Prompts

- Startup prompts are line-oriented and keyboard-first.
- Click/config validation happens before loop execution.
- Invalid values show one visible severity label, the field/value, and accepted
  values or environmental reason.
- Success feedback appears in the boot panel before the first manager decision.
- Help and interrupt prompts must clearly own input focus.

### Config And Theme Resolution

- A single resolver owns UI setting precedence.
- Theme validation is fail-fast for user errors.
- Environmental constraints choose plain defaults only when the user did not
  explicitly force a styled theme.
- Custom theme overrides are validated data, not executable style hooks.
- `--plain`, `--ascii`, and `--compact` are orthogonal where possible:
  plain disables color/effects, ascii changes glyphs, compact changes density.

### Visual Profile And Capability Resolution

- The visual app resolves profile, rendering mode, quality tier, reduced
  effects, plain fallback, and detected render capabilities before showing an
  effect-heavy scene.
- Capability detection chooses shader, QML-only, low-effects, or plain fallback
  without crashing unsupported graphics environments.
- Profile writes are explicit, versioned, atomic where possible, and preserve a
  backup before overwriting user data.
- Import/export validates schema and rejects secrets, unsupported versions, and
  non-ASCII names for now.
- Shared CLI config writes happen only through explicit first-run confirmation.

### Loading States

- LLM summarization shows the number of prior rows and retry state.
- Manager decision shows active decision state and retry state.
- Codex subprocess shows elapsed time, timeout threshold, process state, and
  binary name.
- Plain mode emits durable lines instead of relying on spinners, live-only
  refresh, or carriage-return animation.
- Wrapper mode may animate event arrivals, but active status remains pinned and
  readable.
- Hyperterminal event rows are virtualized so long runs do not shift primary
  controls or make the active status rail disappear.

### Notifications

- Terminal output is always the source of truth.
- Terminal bell and `notify-send` can support help, completion, interrupt, and
  safety-stop states.
- Notifications must never be the only place an important state appears.
- CI, non-TTY, `NO_COLOR`, `TERM=dumb`, and redirected output use plain text
  with no ANSI escapes or box glyphs.

### Error, Warning, And Empty States

- Every error has a severity label, failing subsystem, raw reason, and recovery
  direction when known.
- Empty history is a first-class state, not an empty table.
- Sparse legacy DB rows render with blank-safe cells.
- Non-zero subprocess exits show return code plus captured stdout/stderr
  semantics.
- Timeout text uses the configured timeout threshold.
- Invalid UI config fails before any misleading themed output appears.

### History Interaction

- Default history is compact and readable at 80 columns.
- `--verbose` expands reason and response detail in history mode; do not add
  `--history-verbose`.
- Long response summaries truncate with explicit counts.
- History display does not mutate the DB.
- History rows remain raw workflow facts, not renderer snapshots.

### Event Stream Interaction

- Events are opt-in.
- Events are line-buffered JSONL.
- Event payloads contain raw facts, not Rich markup, ANSI escapes, box glyphs,
  frame tokens, or reference-derived visual tokens.
- Human rendering and machine stdout JSONL are mutually exclusive.
- `--machine-output` is the only supported human-rendering disable mode. It
  requires `--event-stream`, disables terminal bell and desktop notifications,
  and guarantees stdout contains only JSONL events when `--event-stream -` is
  used.
- Event errors are visible in human output unless `--machine-output` is active,
  in which case they must be emitted as machine-readable event errors.

### Product Surface Boundaries

- Primary surfaces: boot panel, iteration frame, manager decision, prompt
  preview, execution status, response panel, history ledger, pause states,
  completion states, Hyperterminal command surface, run command strip, mission
  rail, spec map, event core, signal panel, profile drawer, graphical first
  run, doctor, and user-facing visual failure states.
- Developer/admin/debug surfaces: pytest output, renderer fixture recordings,
  raw event JSONL files, config validation traces, visual spike logs, and
  reference-clean-room audit notes.
- Excluded from primary UI: renderer internals, route ownership notes,
  frame/glyph diagnostics, visual test scaffolding labels, raw event dumps,
  shader reference details, copied profile metadata, arbitrary effect demos,
  package build internals, and implementation-only file paths.

---

## 7. Motion And Animation Strategy

### Philosophy

Motion communicates liveness, elapsed time, and event arrival. It must never
hide commands, errors, handoffs, or captured output.

### Base CLI

- Page load: output appears in stable sections: boot, iteration, decision,
  prompt, execution, result, log, next state.
- Scroll-driven animation: none.
- Live display: limited to status/progress while preserving captured output.
- Plain/compact/non-TTY: degrade to durable line-oriented messages.
- Error/help/interrupt/completion text is never animated over or replaced by
  transient spinners.

### Hyperterminal

- Event arrival may use subtle opacity or position changes.
- Active status remains pinned while the log scrolls.
- Theme and settings controls show immediate state changes.
- Effects may include independently implemented glow, scanlines, flicker,
  curvature, phosphor trails, bloom, procedural noise, chroma/subpixel edge
  treatment, jitter, sync distortion, ambient frame light, and frame treatment.
- Reduced effects keeps state visible through text, color, and simple layout
  changes rather than removing status feedback.
- Run start creates a short surface charge.
- Provider preflight success sends a low-intensity signal sweep.
- Provider preflight failure creates a visible red fault lock.
- New manager decisions pulse around the decision panel.
- New iterations add a soft persistence trail to the event core.
- Operator stop drains glow immediately and freezes final state.
- Successful completion performs a restrained completion sweep.
- Non-zero exit, stderr, malformed JSONL, and timeout use distinct error
  signatures.

### Delivery Stages

1. QML-only high design with structured shell, glow, scanlines, frame
   treatment, pulse, virtualized rows, profile persistence, quality tiers,
   reduced effects, plain fallback, and screenshot smoke checks.
2. Clean-room shader layer with original curvature, glass, bloom, procedural
   noise, chroma, persistence, jitter, sync distortion, capability probing, and
   automatic fallback.
3. Workflow-aware rendering with effect intensity bound to run state, severity,
   task progress, provider health, autonomy policy, config source, and doctor
   results.
4. Production hardening with offscreen smoke, software-backend fallback,
   desktop screenshots, pixel nonblank checks, no-overlap checks, memory checks,
   reduced/plain verification, and clean base install verification.

### Animation Constraints

- Target locked 60fps for live terminal updates and wrapper effects.
- Maximum 3 simultaneous animated elements per viewport region in the wrapper.
- Rich terminal animations must be disabled or simplified under `--plain`,
  `--compact`, `NO_COLOR`, `TERM=dumb`, non-TTY, redirected output, or a
  non-terminal console path.
- Do not use linear easing for wrapper motion; use gentle eased transitions.
- Test performance-sensitive interactions under constrained CPU assumptions.

---

## 8. Layout Philosophy

### Composition Approach

Dense and information-rich, with enough rhythm to separate phases of work. The
base CLI should feel like one instrument panel, not unrelated print statements.
The visual app should feel like a Linux-native command center: first viewport
as the real operating surface, not a product explanation or marketing hero.

### Visual Hierarchy

- Labels, borders, spacing, and color roles matter more than large text.
- Important states use concise uppercase labels only when they need immediate
  attention.
- Default mode may use one blank line between major sections.
- Compact mode removes decorative spacing while preserving semantic labels.
- Every iteration uses the same order so operators can scan by habit.

### Section Transitions

Use hard terminal section boundaries: boot, iteration, history, decision,
prompt, execution, result, log, next step. Rich themes may use faint repeated
ASCII-compatible separators for a low-fidelity scanline feel; plain and compact
modes use simple line labels.

### Framing Rules

- Do not nest UI cards or heavy panels inside panels.
- Avoid wide tables for primary history at 80 columns.
- Keep the current command and current failure visible without horizontal
  scrolling.
- Let wrapper frame treatment stay full-window and functional; do not put the
  primary terminal viewport inside decorative cards.
- The Hyperterminal command surface uses stable zones: run command strip,
  mission state rail, spec map, event core, signal panel, and profile drawer.
- Controls must not resize or shift when events arrive, errors occur, or
  profiles change.

---

## 9. Responsive Strategy

| Breakpoint | Target | Layout Approach |
|------------|--------|-----------------|
| `< 80 columns` | Narrow terminal/logs | Single-column labels, no wide tables, no hidden errors, truncate only with explicit counts |
| `80 columns` | Baseline terminal | Compact status strip, wrapped reason text, readable history ledger |
| `100 columns` | Comfortable terminal | Full iteration frame, concise panels, response summaries |
| `120+ columns` | Wide terminal | Wider response/history columns without extra decorative noise |
| `non-TTY/log` | CI, redirected output, dumb terminal | Plain line output, no color, no live rendering, no box glyphs |
| `Hyperterminal small window` | Visual app minimum | Command strip and event core remain primary; rails collapse before log readability is sacrificed |
| `Hyperterminal large window` | Visual app desktop | Mission rail, spec map, event core, signal panel, and profile drawer can be visible without nested cards |

**Approach**: Terminal-width adaptive, with plain-output fallbacks ahead of
visual polish.

**Touch targets**: Hyperterminal controls must be at least 44x44px. Base CLI
interactions remain keyboard-first.

---

## 10. Accessibility

**Target**: WCAG 2.1 AA intent for contrast and non-color semantics, adapted to
terminal constraints.

- Keyboard navigation: All base CLI interactions must be keyboard-accessible.
  Hyperterminal controls require normal tab order and visible focus.
- Screen reader: Plain mode should produce sequential, meaningful text without
  relying on Rich layout. Live statuses must also emit durable state changes.
- Color contrast: Styled themes must keep normal text, muted text, warnings,
  errors, success, and borders readable on common dark terminals.
- Color independence: Every status has a text label in addition to color.
- Focus management: Help and interrupt prompts must clearly own input focus.
- Reduced motion: `--plain`, `--compact`, `ui.effect_level: off`, `NO_COLOR`,
  `TERM=dumb`, non-TTY output, and redirected output remove live-only or
  decorative effects while preserving state changes.
- Non-ASCII: `--ascii` and plain mode must use code points 0-127 only.
- Width resilience: Text wraps or truncates with counts; it must not overlap,
  disappear, or require horizontal scrolling for critical states.
- Secrets: API keys and environment-derived secrets must not be printed,
  written to SQLite, or emitted in JSONL events.

---

## 11. Design System

### Color Architecture

- **Dominant surface (60%)**: Terminal background or wrapper viewport. Default
  interactive theme should feel dark, quiet, and high contrast.
- **Secondary surfaces (25%)**: Panels, iteration frames, response blocks, and
  history rows. Use low-contrast borders or muted color, not heavy decoration.
- **Accent (10%)**: Active command, current operation, elapsed time, selected
  theme, and focused prompt.
- **Signal colors (5%)**: Success, warning, error, timeout, help, interrupt,
  dry-run, completion, and invalid configuration.

Palette character: Synthetic, dark, restrained, and high-contrast. Use
independent token names and values. Do not copy reference profile colors.

### Built-In Theme Intents

| Theme | Intent | Primary Use |
|-------|--------|-------------|
| `auto` | Resolve to the right default for the terminal | First-run default |
| `crt-green` | Focused green-phosphor operator console | Capable interactive TTY default |
| `crt-amber` | Warm amber maintenance terminal | Operator preference |
| `ibm-dos` | Crisp DOS-like contrast with minimal effects | High-legibility retro mode |
| `plain` | Deterministic unstyled text | Logs, CI, non-TTY, dumb terminals |

### Hyperterminal Profile Intents

These profile names, colors, and constants are Apex-owned and must be
independently designed.

| Profile | Intent | Primary Use |
|---------|--------|-------------|
| `apex-reactor` | Deep black command surface with green-white active signal, red fault charge, and high bloom | Default cinematic Hyperterminal profile |
| `operator-amber` | Warm amber command surface with strong maintenance/warning emphasis and low blue content | Long operator sessions and low-light rooms |
| `blueprint-dos` | Blue-black base with precise cyan vector lines and crisp pixel-grid structure | Spec navigation, status maps, and screenshots |
| `whiteout-lab` | High-contrast light mode for bright rooms and documentation captures | Accessibility and presentation mode |
| `blackbox` | Minimal dark surface with restrained effects | Long unattended runs and low distraction |
| `incident-red` | Error investigation mode with stronger event classification and fault isolation | Debugging failures, timeouts, malformed events, and provider faults |

### Rendering Modes

| Mode | Intent |
|------|--------|
| `modern-crisp` | High-readability default when effects are disabled |
| `scanline` | Horizontal line treatment without copying reference formulas |
| `pixel-grid` | Cell-grid treatment for log rows and status modules |
| `subpixel` | Fine RGB-style edge treatment implemented from original Apex code |
| `cinematic` | Full postprocess pipeline with curvature, glow, persistence, ambient frame, jitter, and event-reactive pulse |

### Status Vocabulary

Use stable labels across themes and plain mode:

- `BOOT`
- `ITERATION`
- `HISTORY`
- `DECISION`
- `PROMPT`
- `EXECUTING`
- `DRY RUN`
- `RESPONSE`
- `LOGGED`
- `HELP`
- `INTERRUPT`
- `TIMEOUT`
- `ERROR`
- `COMPLETE`
- `STOP`

### Typography

- **Display font**: The user's terminal font in bold or high-emphasis style.
  Do not ship copied or bundled reference fonts in the base CLI.
- **Body font**: The user's terminal monospace font.
- **Monospace**: Primary typography for every base CLI surface.
- **Scale ratio**: Terminal emphasis scale: normal, dim, bold, panel title,
  alert title. Do not depend on viewport-width font scaling.
- **Minimum body size**: Controlled by terminal. Hyperterminal should default
  to a readable system monospace size and expose scaling controls.

### Spacing Scale

Terminal spacing uses rows and columns:

```text
0 rows: compact inline labels
1 row: default section separation
2 rows: major state transition
4 columns: nested detail indent
8 columns: table padding or status grouping when width allows
```

Hyperterminal spacing uses an 8px base scale:

```text
4, 8, 12, 16, 24, 32, 48, 64
```

### Elevation And Depth

Base CLI depth comes from ordering, borders, labels, and muted text. Do not
simulate physical depth with heavy boxes inside boxes. Hyperterminal may use
subtle glow, dark glass, and frame treatment, but text legibility remains the
priority.

### Texture And Atmosphere

Rich milestone:

- Low-fidelity scanline-like separators may use simple repeated characters.
- Disable decorative separators in `plain` and compact modes.
- Never write box glyphs, ANSI escapes, or Rich markup to SQLite history.

Hyperterminal:

- Effects may include independently implemented glow, scanlines, flicker,
  curvature, phosphor trail, and frame treatment.
- Do not use copied noise images, CRT images, shaders, constants, fonts, icons,
  profile data, or resource manifests.

---

## 12. Component Patterns

| Component | Used In | Behavior |
|-----------|---------|----------|
| UI Config Resolver | Startup | Resolves CLI flags, environment constraints, config, and defaults deterministically |
| Theme Token Set | Renderer, wrapper | Supplies color, severity, border, glyph, emphasis, and fallback tokens |
| Glyph Set | Renderer | Switches between styled, ASCII, compact, and plain symbols |
| Renderer Facade | All human output | Centralizes `Console` usage and supports injected test consoles |
| Boot Panel | Normal and dry-run startup | Shows provider, model, project, config, theme, max iterations, dry-run, start command |
| Status Strip | Iteration frame | Shows iteration, operation, elapsed time, provider/model, project, dry-run |
| Iteration Frame | Main loop | Groups one autonomous cycle with stable section order |
| History Summary Notice | Main loop | Shows prior record count and summarizer activity |
| Decision Panel | Manager output | Separates command/custom instruction and reason from agent output |
| Prompt Preview | Before Codex | Shows generated Codex prompt with truncation and command classification |
| Execution Status | Codex subprocess | Shows process state, elapsed time, timeout, and binary name |
| Response Panel | After Codex | Shows captured output summary, verbose expansion, and error labels |
| History Ledger | `--history` | Shows compact rows, path filter, verbose expansion, empty state |
| Alert Block | Help, interrupt, timeout, error | Uses text labels plus color/severity; impossible to miss in plain mode |
| DB Log Notice | End of iteration | Confirms history write without exposing debug internals |
| Event Emitter | Event stream | Writes raw JSONL facts and exposes importable API for tests/wrappers |
| Visual Event Adapter | Hyperterminal | Converts registered events into display-state updates without QML parsing raw JSONL |
| Visual State Store | Hyperterminal | Holds run health, stage, provider, model, iteration, current spec, task progress, errors, and artifacts |
| Profile Store | Hyperterminal | Persists versioned visual profiles under XDG config with import/export/reset and corruption handling |
| Render Capabilities Resolver | Hyperterminal | Detects graphics backend, shader support, software mode, and quality tier fallback |
| Doctor Adapter | Hyperterminal | Presents CLI doctor checks as pass/warn/fail visual rows |
| App Shell | Hyperterminal | Full-window command-center frame that owns stable responsive zones |
| Run Command Strip | Hyperterminal | Project/start command controls, dry-run/live-run mode, max iterations, start/stop/resume/doctor |
| Mission State Rail | Hyperterminal | Provider/model/stage/iteration/config/event/history state that stays visible during long runs |
| Spec Map | Hyperterminal | `.spec_system/`, phase/session, current command, task progress, and validation/carry-forward state |
| Event Core | Hyperterminal | Virtualized structured lifecycle log with typed rows, search, filter, pin, copy, and export |
| Signal Panel | Hyperterminal | Provider health, stderr summary, malformed event count, duration, last event, and safe artifacts |
| Visual Profile Drawer | Hyperterminal | Profile, rendering mode, quality, effects, font, layout, import/export/reset |
| QML Controls | Hyperterminal | Apex button, toggle, slider, segmented control, and status cell components |
| Effect Surface | Hyperterminal | QML-only and shader-backed glow, scanline, phosphor trail, curvature, distortion, and frame treatment |
| Wrapper Failure Surface | Hyperterminal | Shows malformed events, missing CLI, missing PySide6, subprocess exit, timeout, shader fallback, and recovery |

---

## 13. Event Model And Wrapper Boundary

### Event Stream Purpose

The event stream is the machine-readable interface for future renderers,
wrappers, tests, and diagnostics. It prevents wrappers from parsing Rich output
or terminal frames.

### Required Event Names

Use stable snake_case names:

- `startup_begin`
- `config_loaded`
- `ui_resolved`
- `project_resolved`
- `iteration_started`
- `history_fetched`
- `history_summarize_started`
- `history_summarize_finished`
- `manager_decision_started`
- `manager_decision_finished`
- `prompt_built`
- `codex_started`
- `codex_finished`
- `codex_timeout`
- `codex_error`
- `response_summarized`
- `db_log_started`
- `db_log_finished`
- `help_requested`
- `operator_interrupt_requested`
- `operator_input_received`
- `workflow_completed`
- `max_iterations_reached`
- `run_stopped`
- `event_stream_error`

### Candidate Event Additions For Hyperterminal

Add these only when a visual surface needs the fact and tests define the file
stream plus stdout-machine-output behavior:

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

### Payload Rules

- Include timestamp, project path key, iteration number when applicable,
  operation name, severity when applicable, and concise raw facts.
- Do not include API keys, secrets, Rich markup, ANSI escapes, box glyphs,
  renderer tokens, reference-derived visual constants, or human-only frames.
- Keep event payloads JSON-serializable with primitive values and simple
  objects.
- Flush line-buffered writes so wrapper state stays current.
- Preserve event order in dry-run tests.
- Keep event versioning explicit if payload shape changes.
- When `--machine-output` is active, stdout is reserved for JSONL only. Human
  renderer output, terminal bells, and desktop notifications are disabled.

### Wrapper Contract

The Phase 02 Hyperterminal visual app:

- Launches or observes the Python CLI as the workflow engine.
- Consumes JSONL events or an importable event emitter API.
- Keeps raw JSONL parsing in Python adapter/state code; QML consumes display
  state, models, and invokable actions.
- Ships with PySide6 and Qt Quick/QML as an optional Linux-only extra.
- Renders a read-only event core, operational panels, and a full-window command
  surface composed from lifecycle events.
- Implements independently designed glow, scanlines, curvature, flicker,
  phosphor trails, ambient frame light, and status-panel choreography.
- Does not embed a pseudo-terminal or terminal-emulator viewport in the selected
  path. It should use native QML models/views for logs and event panels.
- Does not scrape Rich frames.
- Does not depend on the reference terminal application.
- Does not use PyQt, qmltermwidget, QTermWidget, copied QML, copied shaders,
  copied generated shader blobs, copied assets, copied fonts, copied profile
  data, copied manifests, copied build scripts, copied package metadata, or
  copied terminal-emulator code.
- Keeps graphical dependencies optional and Linux-scoped.
- Documents PySide6 LGPLv3/commercial obligations and packaging requirements.
- Stores visual profiles and runtime visual state in XDG locations and never
  writes provider secrets.
- Ships as a real Linux app with desktop metadata, AppStream metadata, launcher
  actions, AppImage, checksum, notices, and clean-machine verification.
- Uses pywebview plus xterm.js only as a backup if a future accepted
  requirement needs a fully interactive terminal emulator, PTY behavior,
  curses-like applications, or raw ANSI fidelity.

### Wrapper Release Artifact

The first binary visual-wrapper release artifact is a single x86_64 Linux
AppImage:

```text
apex-infinite-visual-linux-x86_64.AppImage
```

Release requirements:

- Build the wrapper as a PySide6/QML application, using `pyside6-deploy` or an
  equivalent reproducible Python desktop build pipeline as the inner executable
  step.
- Wrap the Linux executable and required runtime files into an AppImage.
- Publish SHA256 checksums, license notices, and a short compatibility note.
- Keep source/developer installation available as an optional Python extra, for
  example `.[visual]`, but do not treat that as the first user-facing binary
  artifact.
- Defer `.deb`, `.rpm`, Flatpak, and Snap packages until the AppImage has real
  operator feedback or distribution-specific demand.

---

## 14. Implementation Coverage Matrix

This matrix captures the completed CLI UX scope plus the Phase 02
Hyperterminal scope without making final session stubs authoritative.
`phasebuild` owns final session files and counts.

| Coverage Area | UX Deliverables | Verification |
|---------------|-----------------|--------------|
| UI architecture and theme tokens | Renderer boundary, injected `Console`, UI resolver, token model, built-in themes, custom override validation | Prompt tests unchanged, config/Click tests, no styled DB rows |
| CRT-inspired operator console | Boot panel, iteration frame, status strip, manager/prompt/response/log surfaces, help/completion/error render states | 80/100/120 column checks, plain/ascii/compact checks |
| Live execution and history | Elapsed subprocess status, preserved capture semantics, compact history ledger, verbose history expansion | Fake subprocess tests for success, stderr-only, non-zero, timeout, dry-run, missing binary |
| Documentation and samples | README/runbook/history/prompt-contract/troubleshooting updates, ASCII transcripts or asciinema casts, clean-room note | Docs describe implemented flags, fallback modes, event stream, no-copy boundary |
| Event stream boundary | `--event-stream PATH`, `--machine-output`, guarded stdout JSONL mode, importable emitter API, raw event payloads | Dry-run event order tests, no markup/ANSI/reference tokens |
| Visual state foundation | Python visual state model, event adapter, run health, provider/model/config/Codex/spec/task/error/artifact state | Unit tests from JSONL fixtures, QML does not parse raw JSONL |
| Profile persistence | XDG profile store, versioned schema, import/export, reset, migration stubs, corruption handling | Profile schema tests, atomic write/backup tests, invalid profile tests, no secrets |
| App shell redesign | Full-window command surface, reusable QML shell/controls, run strip, mission rail, spec map, event core, signal panel, drawer | QML lint, no overlap checks, minimum-size checks, readable event rows |
| QML high-design effects | Glow, scanlines, frame treatment, pulse, persistence, quality tiers, reduced/plain enforcement | Offscreen smoke, desktop screenshots, pixel nonblank, reduced/plain checks |
| CLI event expansion | Registered doctor/config/Codex/autonomy/spec/task/artifact/duration/capability events | File-stream and stdout-machine-output event tests, secret/markup/ANSI exclusion |
| Graphical doctor and first run | Provider/model/Codex/project setup, doctor pass/warn/fail summaries, dry-run default, explicit config write | Clean user flow tests, missing provider/Codex/project checks, no accidental live mode |
| Clean-room shader pipeline | Original shaders, capability detection, shader fallback, provenance for generated outputs | Shader source review, generated artifact review, software-backend fallback, performance tiers |
| Desktop and AppImage release | Original icon, `.desktop`, AppStream, launcher actions, AppImage, checksum, notices, dependency inventory | AppImage clean-machine launch, visual extra source install, license inventory review |
| Terminal CLI polish | Rich theme/status hierarchy polish, autonomy summary, compact progress/diagnostics | Plain output, redirected output, `--event-stream - --machine-output`, and regression tests |
| Release verification | Compatibility, docs, clean-room audit, smoke run, fallback behavior, source encoding | Full applicable test suite, `git diff --check`, ASCII/LF checks, no tracked `EXAMPLE/`, no copied reference material |

---

## 15. UX Acceptance Checklist

- The default interactive run presents a cohesive operator-console experience.
- The first visible surface identifies project, provider, model, config/theme,
  max iterations, dry-run state, and first command when available.
- Every iteration has stable sections in the same order.
- Manager decisions are visually distinct from Codex output.
- Prompt preview is visible but truncated safely.
- Operators can tell whether Codex is running and how long it has been running.
- Timeout, non-zero exit, missing binary, provider retry failure, help,
  interrupt, completion, and max-iteration stop are impossible to miss.
- `--dry-run` clearly shows that Codex was not launched.
- `--history` is readable at 80 columns without horizontal scrolling.
- `--verbose` expands normal execution output and history detail.
- `--plain` emits deterministic unstyled text.
- `--ascii` avoids non-ASCII glyphs.
- `--compact` reduces density without hiding critical information.
- `NO_COLOR`, `TERM=dumb`, non-TTY, redirected output, and non-terminal console
  paths choose plain output by default.
- Explicit `--theme` can override environmental color defaults only where
  documented.
- Invalid theme values fail fast with clear error text.
- SQLite history rows contain raw workflow facts only.
- JSONL events contain raw workflow facts only.
- API keys and secrets are never printed, stored, or emitted.
- Existing history DBs remain readable without migration.
- Prompt contract behavior remains unchanged unless code, tests, README, and
  prompt-contract docs change together.
- The base CLI remains usable without Qt, PySide6, PyQt, qmltermwidget,
  QTermWidget, a graphical display, or an external terminal emulator.
- Apex Infinite Hyperterminal opens as the usable visual command surface on the
  first screen, not a landing page or demo dashboard.
- The visual app consumes registered events through a Python adapter/state
  layer; QML does not parse raw JSONL and no visual surface scrapes Rich output.
- The command surface includes run command strip, mission state rail, spec map,
  event core, signal panel, and visual profile drawer.
- Visual profiles, rendering modes, quality tiers, effect intensity, font
  controls, reduced effects, and plain fallback persist across launches.
- Event-reactive effects respond to real workflow states such as run start,
  provider preflight, manager decision, iteration progress, stop, completion,
  timeout, stderr, and malformed events.
- Low-effects and plain modes are intentionally designed and verified, not
  broken versions of high-effects mode.
- Graphical first run can configure provider, model, Codex binary, project,
  doctor, and dry-run default without editing source files.
- The first visual-wrapper binary release artifact is an x86_64 Linux AppImage
  with checksum and license notices.
- The selected wrapper does not require a terminal-emulator viewport.
- Desktop launcher and AppImage work on a clean supported Linux machine.
- No reference source, QML, shader, generated shader blob, image, icon, font,
  profile data, resource manifest, package metadata, terminal-widget code, or
  build script is copied into the product.
- All authored files stay ASCII-only with Unix LF line endings.

---

## 16. Anti-Patterns To Avoid

- Do not copy reference source, QML, shader code, shader constants, generated
  shader blobs, profile JSON, literal colors, images, icons, fonts, resource
  manifests, package metadata, terminal emulator code, or build scripts.
- Do not make the Hyperterminal first screen a landing page, marketing hero,
  explanatory dashboard, or decorative demo shell.
- Do not animate arbitrary decoration. Visual effects must respond to workflow
  facts or explicit user profile choices.
- Do not put raw JSONL parsing or workflow decision logic in QML.
- Do not make the base CLI require Qt, PySide6, PyQt, qmltermwidget,
  QTermWidget, a graphical display, or an external terminal emulator.
- Do not make operators run Apex Infinite CLI inside another terminal emulator
  to get the upgraded experience.
- Do not let styling alter manager prompts, command normalization, path
  normalization, timeout behavior, DB schema compatibility, or autonomous
  `Next command:` handoffs.
- Do not store styled output, ANSI escapes, Rich markup, frame glyphs, or
  visual tokens in SQLite rows or JSONL events.
- Do not hide errors, timeouts, help pauses, interrupts, non-zero exits, or
  completion states in compact or styled output.
- Do not use wide history tables that require horizontal scrolling at
  80 columns.
- Do not turn primary operator surfaces into debug dashboards. Renderer tests,
  raw event payloads, and frame diagnostics belong in developer surfaces.
- Do not use decorative effects that make text harder to read.
- Do not commit generated packaging output unless a release session explicitly
  scopes it.
- Do not add brittle full-frame snapshot tests where semantic renderer tests
  would be more stable.
- Do not ship binary screenshots in source docs; use ASCII transcripts or
  deterministic asciinema casts when documentation needs examples.

---

## 17. Assumptions And Conflict Resolutions

### Working Assumptions

- Apex Infinite CLI remains terminal-first and operator-facing at the base
  package layer, while Phase 02 adds a Linux visual product lane. Evidence:
  `PRD.md`, the CLI README, operator runbook, architecture docs, current
  implementation, and visual-wrapper docs all keep the Python CLI as workflow
  engine. It is safe to proceed because graphical dependencies stay isolated in
  the optional visual package path.
- The first Phase 02 visual milestone should stabilize state, profiles, and
  QML-only high design before custom shaders. Evidence: the PRD, architecture
  docs, and visual-wrapper productization docs order visual state, profile
  persistence, shell redesign, and QML effects before shader promotion. It is
  safe because shader complexity is gated behind a working command surface and
  fallback model.
- `auto` should resolve to `crt-green` only for capable interactive terminals
  and to `plain` for constrained output. Evidence: the product PRD,
  conventions, and settings implementation require this fallback model. It is
  safe because invalid user theme configuration still fails fast.
- The reference terminal project informs UX vocabulary but not implementation
  data. Evidence: the reference material is GPL-family and the product PRD
  forbids copying source, QML, shaders, generated shader blobs, assets, fonts,
  profile data, manifests, package metadata, build scripts, and terminal-widget
  code. It is safe because the PRD records clean-room translation boundaries as
  explicit product requirements.
- Operational telemetry is part of the product only when it helps the operator.
  Status strip, elapsed time, timeout, provider/model, manager decision, prompt
  preview, DB log confirmation, and history ledger are primary surfaces because
  the product is an autonomous workflow runner. Renderer internals and raw event
  payload dumps remain developer/debug surfaces.
- The local `EXAMPLE/cool-retro-term/` tree is conceptual source material
  only. It is safe to use independently translated concepts because this UX PRD
  and the wrapper boundary docs record forbidden translations and clean-room
  gates instead of copying implementation data.
- This UX PRD must be self-contained with respect to source example trees and
  archived planning notes. It is safe because this file embeds the relevant
  current behavior, visual concepts, no-copy boundaries, configuration rules,
  event requirements, wrapper direction, acceptance checks, and resolved
  decisions.
- Hyperterminal should optimize for a custom event-composed scene rather than a
  terminal-emulator viewport. Evidence: the current CLI product needs lifecycle
  facts, logs, status, and captured responses rather than an interactive shell;
  the reference's strongest visual ideas come from source/effects/frame
  composition; Qt Quick supports custom shader effects; and xterm.js is
  specifically useful when browser-based terminal emulation is a product
  requirement. It is safe because pywebview plus xterm.js remains a documented
  backup for a future interactive-terminal requirement.

### Conflict Resolutions

- The completed product history contains Phase 00 and Phase 01, while Phase 02
  defines the Hyperterminal visual lane. The chosen interpretation is to
  preserve completed phase records and keep Phase 02 as the planned
  Hyperterminal scope.
- The visual source is a full graphical terminal emulator with tabs, menus,
  settings dialogs, shader passes, copied assets, and external submodules,
  while Apex Infinite CLI is a Python workflow manager. The chosen
  interpretation is clean-room visual translation: Rich gets status hierarchy,
  framing, profile-like themes, and low-fidelity separators; Hyperterminal gets
  event-driven visual effects without depending on the reference app,
  qmltermwidget, or QTermWidget.
- Older UX source material described the visual wrapper as optional future
  productization. The chosen interpretation is Phase 02 Hyperterminal with
  base CLI dependency isolation and explicit release gates.
- `NO_COLOR` normally means no color, while explicit `--theme` can opt back
  into styled output under the documented UI configuration rules. The chosen
  interpretation is that environmental constraints set safe defaults, while
  explicit operator choices can override them when documented and tested.
- `--event-stream -` is useful for machine pipelines but unsafe if human output
  also goes to stdout. The chosen interpretation is to require
  `--machine-output`, which disables human rendering and reserves stdout for
  JSONL.
- The visual source ships AppImage as its Linux release path and also contains
  distro-package examples, while Qt for Python deployment produces a Linux
  executable rather than a complete distro package. The chosen interpretation is
  to ship the first Apex Infinite visual-wrapper binary as an AppImage wrapping
  the Linux executable, with distro packages deferred until demand is proven.

---

## 18. Resolved UX Decisions

Open UX Decisions: none.

1. **Human-rendering disable mode**: Use `--machine-output`.
   `--machine-output` requires `--event-stream`, disables Rich/plain human
   rendering, disables terminal bell and desktop notifications, and guarantees
   stdout is JSONL-only when paired with `--event-stream -`.
2. **Hyperterminal productization**: Ship the PySide6/Qt Quick/QML wrapper as
   the Phase 02 Apex Infinite Hyperterminal visual lane. The visual app uses the
   Python CLI as workflow engine, keeps graphical dependencies optional and
   Linux-scoped, and treats QML-only design, shaders, packaging, and clean-room
   release evidence as verification gates.
3. **First wrapper release artifact**: Publish an x86_64 Linux AppImage named
   `apex-infinite-visual-linux-x86_64.AppImage`, with SHA256 checksums, license
   notices, and a source/developer install path through the optional Python
   extra. Defer `.deb`, `.rpm`, Flatpak, and Snap packages until the AppImage
   has operator feedback or distribution-specific demand.
4. **Terminal-emulator viewport**: Do not require a terminal-emulator viewport
   for the selected wrapper architecture. The wrapper should render lifecycle
   events and captured output through native QML models/views inside a
   full-window Hyperterminal command surface. Evaluate pywebview plus xterm.js only if a
   future accepted requirement needs an interactive shell, PTY behavior,
   curses-like applications, or raw ANSI terminal fidelity.
5. **Visual lane name**: Use `Apex Infinite Hyperterminal` as the visual mode
   name only. Keep `apex-infinite` and `apex-infinite-visual` as command names
   unless a later release explicitly changes them.
