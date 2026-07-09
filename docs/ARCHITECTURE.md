# Architecture

## System Overview

Apex Infinite CLI is a Python command-line workflow runner for initialized Apex
Spec projects. The base package reads provider and Codex configuration, asks a
manager LLM for the next workflow action, runs `codex exec`, records local
SQLite history, and repeats until a completion or safety stop. The optional
visual wrapper is a separate PySide6/QML surface that consumes the base CLI
event boundary.

```text
Operator
  |
  v
apex-infinite Click command
  |
  +-- provider client for manager and summarizer calls
  +-- codex exec subprocess
  +-- SQLite history at ~/.apex-infinite/history.db
  +-- optional JSONL event stream
  |
  v
initialized Apex Spec project
```

## Components

| Component | Location | Tech | Purpose |
|-----------|----------|------|---------|
| Base CLI | `src/apex_infinite/cli.py` | Click, OpenAI SDK, subprocess, SQLite | Entry point, config loading, provider preflight, manager loop, Codex execution, and history storage. |
| Renderer | `src/apex_infinite/ui.py` | Rich | Styled, plain, ASCII, and compact terminal output from raw workflow facts. |
| Event stream | `src/apex_infinite/events.py` | JSONL | Validated lifecycle event writer for automation and wrappers. |
| Logging | `src/apex_infinite/logging_config.py` | Python logging | Local diagnostic logging and last-error file support. |
| Optional visual wrapper | `src/apex_infinite_visual/` | PySide6, Qt Quick/QML | Hyperterminal command surface that launches or replays the base CLI through the event boundary. |
| Visual state store | `src/apex_infinite_visual/visual_state.py` | Python | PySide6-free event-derived display state: run health, spec map, signal panel, typed rows, effect pulses. |
| Visual profiles | `src/apex_infinite_visual/profile_store.py` | JSON, XDG | Versioned visual profile persistence with atomic writes, backups, and import/export. |
| Render capabilities | `src/apex_infinite_visual/render_caps.py` | Python | Backend detection, shader artifact discovery, and quality tier clamping. |
| Visual doctor | `src/apex_infinite_visual/doctor.py` | Python | Display-safe pass/warn/fail launch diagnostics for the wrapper. |
| Shaders | `src/apex_infinite_visual/shaders/` | GLSL 440, qsb | Clean-room shader sources with provenance; compiled artifacts are untracked build outputs. |
| Desktop assets | `src/apex_infinite_visual/assets/` | SVG, desktop, AppStream | Original icon, launcher entry, and AppStream metadata for Linux packaging. |
| Ollama helpers | `scripts/`, `docker-compose.ollama.yml` | Bash, Docker Compose | Local Ollama deployment, model pull, provider checks, and compatibility aliases. |
| Tests | `tests/` | pytest | Prompt routing, config, UI, event stream, history, subprocess, provider preflight, and visual wrapper coverage. |

## Data And Dependencies

- **History**: `src/apex_infinite/cli.py` writes SQLite rows under
  `~/.apex-infinite/history.db` using the legacy `cc_response` column for
  compatibility.
- **Event stream**: `src/apex_infinite/events.py` writes line-buffered ASCII
  JSONL to a file or to stdout with `--machine-output`.
- **Provider traffic**: manager and summarizer prompts use the configured
  OpenAI-compatible provider from `src/apex_infinite/config.yaml`.
- **Codex subprocess**: real workflow execution goes through `codex exec` with
  validated configured flags and reasoning-effort tokens.
- **Base dependencies**: Python 3.10+, Click, OpenAI Python SDK,
  python-dotenv, PyYAML, Rich, structlog, and the standard-library SQLite and
  subprocess modules.
- **Optional wrapper dependencies**: PySide6 and Nuitka are isolated in the
  `visual` optional dependency extra.

## Interface Boundaries

- Human terminal output is not a machine interface. Wrappers and automation use
  JSONL events or importable event APIs.
- Renderer labels, Rich markup, ANSI escapes, frame glyphs, and theme tokens
  are display-only and must not be written to SQLite or event payloads.
- Prompt routing remains coupled to the documented manager and summarizer
  contracts in `docs/prompt-contract.md`.
- The visual wrapper must not copy terminal-emulator source, QML, shaders,
  images, icons, fonts, resource manifests, build scripts, or profile data from
  reference projects.

## Related Docs

- [Event stream contract](event-stream.md)
- [History DB reference](history-db.md)
- [Prompt contract](prompt-contract.md)
- [Visual wrapper boundary](visual-wrapper-boundary.md)
