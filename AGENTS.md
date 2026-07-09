# AGENTS.md

## Scope

These instructions apply to the whole repository. This project is a Python
3.10+ package for `apex-infinite`, an autonomous Codex CLI workflow runner for
Apex Spec projects, plus an optional Linux PySide6/QML visual wrapper.

Treat `pyproject.toml` as canonical for package metadata, dependencies,
entry points, pytest, Black, Pylint, mypy, and coverage settings. The
`requirements*.txt` files are compatibility shims.

## Source Map

- `src/apex_infinite/`: base terminal CLI, config loading, provider preflight,
  Codex subprocess execution, SQLite history, event stream, logging, and Rich
  rendering.
- `src/apex_infinite_visual/`: optional visual wrapper. PySide6 imports must
  stay lazy and wrapper-only.
- `tests/`: pytest coverage for CLI options, prompts, subprocesses, event
  streams, renderer behavior, history, provider checks, and wrapper behavior.
- `docs/PRD.md`, `docs/CONVENTIONS.md`, `docs/ARCHITECTURE.md`,
  `docs/prompt-contract.md`, `docs/event-stream.md`, and
  `docs/visual-wrapper-boundary.md`: primary product and contract references.
- `EXAMPLE/`: ignored reference-only material. Do not read from it as a source
  dependency, copy from it, or make runtime behavior depend on it.

## Core Contracts

- Preserve the Apex Spec autonomous loop: summarize history, ask the manager
  LLM for a next action, normalize known commands, run `codex exec`, log to
  SQLite, and repeat until completion or a safety stop.
- Keep prompt routing stable unless the change explicitly targets prompts. If
  `MANAGER_SYSTEM_PROMPT`, `SUMMARIZER_SYSTEM_PROMPT`, command normalization,
  or `build_codex_prompt()` changes, update `src/apex_infinite/cli.py`,
  `tests/test_prompts.py`, `README.md`, and `docs/prompt-contract.md`
  together.
- Known Apex Spec commands route to exactly
  `Run the apex-spec skill command /<command>`. Unknown manager output passes
  through as raw Codex instructions.
- Preserve SQLite compatibility. History lives at
  `~/.apex-infinite/history.db`, uses WAL, and keeps the legacy `cc_response`
  column name.
- Store raw workflow facts only. Do not write Rich markup, ANSI escapes, frame
  glyphs, theme tokens, rendered labels, or truncation text to SQLite or event
  payloads.
- Keep `--event-stream -` guarded by `--machine-output`; stdout JSONL must not
  mix with human output.
- Keep base CLI dependencies terminal-only. Do not add Qt, PySide6, PyQt,
  pywebview, xterm.js, qmltermwidget, QTermWidget, copied terminal emulators,
  shaders, fonts, images, icons, or graphical startup checks to the base CLI
  path.
- Visual work must be clean-room: independently chosen code, QML, colors,
  settings, assets, effects, schemas, docs, tests, and packaging metadata.

## Development Commands

Use the repository virtualenv explicitly:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -e ".[dev,visual]"
```

Core verification:

```bash
.venv/bin/python -m pytest tests/ -v
.venv/bin/python -m black --check src tests
.venv/bin/python -m mypy
.venv/bin/python -m pylint src/apex_infinite src/apex_infinite_visual
```

Release or dependency checks may also require:

```bash
.venv/bin/python -m pip_audit
.venv/bin/python -m build --outdir /tmp/apex-infinite-cli-smoke-dist
```

Local Ollama helpers:

```bash
./scripts/ollama-docker.sh --chat
./scripts/check-ollama.sh --chat
make ollama-up
make ollama-down
```

Live Ollama tests are opt-in with `APEX_INFINITE_LIVE_OLLAMA=1`; normal tests
must use fixtures and monkeypatching instead of real LLM, Codex, or provider
calls.

## Code Style

- Keep authored files ASCII-only with Unix LF endings.
- Use Black formatting at 88 columns and the Pylint/mypy settings in
  `pyproject.toml`.
- Prefer small, testable helper boundaries over expanding
  `src/apex_infinite/cli.py` indefinitely.
- Keep imports grouped standard library, third-party, then local.
- Add focused tests for changed config parsing, Click options, renderer output,
  event payloads, subprocess behavior, history behavior, prompt routing, or
  visual wrapper state.
- Use `Console(record=True, width=...)` for renderer tests and `CliRunner` for
  CLI option tests.
- For event payloads, reject or suppress secrets, ANSI, Rich markup, frame
  glyphs, and visual token values.

## CLI And UI Rules

- UI config keys are `theme`, `effect_level`, `ascii`, `compact`,
  `show_elapsed`, `show_provider`, and `themes`.
- Built-in themes are `auto`, `crt-green`, `crt-amber`, `ibm-dos`, and
  `plain`.
- Resolve display settings in this order: CLI flags, environment constraints,
  config file, built-in defaults.
- `--plain` forces plain output and disables effects. `--ascii` changes glyphs
  only. `--compact` must not hide errors, manager reasons, prompts, output
  summaries, help pauses, completion, timeouts, or non-zero exits.
- Invalid config, invalid themes, malformed Codex flags, unsupported reasoning
  effort, missing Codex binary, and provider preflight failures should fail
  fast with clear operator-facing errors.

## Security And Data

- Never commit provider keys, `.env`, local history DBs, real event streams,
  customer data, or private project output.
- Provider prompts can include recent history, latest agent output, summaries,
  operator instructions, and project paths. Treat those as potentially
  sensitive.
- Keep generated smoke artifacts outside the repo unless they are intentional
  deterministic fixtures under `docs/transcripts/` or tests.
