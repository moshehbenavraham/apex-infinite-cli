# Development Guide

## Required Tools

| Tool | Verified Source | Purpose |
|------|-----------------|---------|
| Python 3.10+ | `pyproject.toml` | Runtime and development interpreter. |
| Codex CLI | `README.md`, `src/apex_infinite/config.yaml` | Executes Apex Spec workflow commands through `codex exec`. |
| Docker Compose | `scripts/ollama-docker.sh` | Optional local Ollama service. |
| pytest | `pyproject.toml` | Test runner. |
| Black | `pyproject.toml` | Formatting check. |
| mypy | `pyproject.toml` | Type checking for `src`. |
| Pylint | `pyproject.toml`, `.github/workflows/quality.yml` | Linting. |
| pip-audit | `pyproject.toml` | Local dependency vulnerability audit. |

## Dev Scripts

| Command | Purpose |
|---------|---------|
| `python3 -m venv .venv` | Create the repository virtualenv. |
| `.venv/bin/python -m pip install -e ".[dev,visual]"` | Install base CLI, dev tools, and optional wrapper dependencies. |
| `.venv/bin/python -m pytest tests/ -v` | Run the full test suite. |
| `.venv/bin/python -m black --check src tests` | Check formatting. |
| `.venv/bin/python -m mypy` | Type-check `src` using `pyproject.toml`. |
| `.venv/bin/python -m pylint src tests` | Lint source and tests with project Pylint settings. |
| `.venv/bin/python -m pip_audit` | Run a local dependency audit. |
| `.venv/bin/python -m build --outdir /tmp/apex-infinite-cli-smoke-dist` | Build release artifacts outside the repo. |
| `./scripts/ollama-docker.sh --chat` | Start local Ollama, ensure the configured model exists, and run a chat check. |
| `./scripts/check-ollama.sh --chat` | Check the configured local Ollama provider. |
| `make production [PROJECT=/absolute/path]` | Gate and open the live visual production console; review it and click `Start`. Requires the existing `.[visual]` environment. |
| `make visual-real` | Open the unguarded one-iteration live visual development launcher; it may bootstrap missing visual dependencies. |
| `make ollama-up` | Compatibility target for `./scripts/ollama-docker.sh up`. |
| `make ollama-down` | Stop the local Ollama container without deleting model data. |

## Testing

Core local verification:

```bash
.venv/bin/python -m pytest tests/ -v
.venv/bin/python -m black --check src tests
.venv/bin/python -m mypy
.venv/bin/python -m pylint src tests
```

Release-oriented checks add dependency audit and package build:

```bash
.venv/bin/python -m pip_audit
.venv/bin/python -m build --outdir /tmp/apex-infinite-cli-smoke-dist
```

Live Ollama tests are opt-in through `APEX_INFINITE_LIVE_OLLAMA=1`. The normal
test suite uses fixtures and does not require a running local model.

## Source Layout

| Path | Purpose |
|------|---------|
| `src/apex_infinite/` | Base terminal CLI, renderer, events, config, and logging. |
| `src/apex_infinite_visual/` | Optional Linux visual wrapper source mode. |
| `tests/` | Unit and integration-style tests for CLI behavior. |
| `docs/` | Operator, architecture, event, history, wrapper, and troubleshooting docs. |
| `scripts/` | Guarded runtime, local Ollama, visual, and packaging helpers. |
| `.spec_system/` | Apex Spec workflow state, PRDs, session specs, and audits. |

## Development Notes

- Keep base CLI imports headless-safe; PySide6 belongs only in the optional
  visual wrapper path.
- Keep `scripts/run-visual.sh` a development convenience. The production target
  must use the preinstalled visual executable after its strict preflight and
  must not install or upgrade packages.
- Preserve the SQLite `cc_response` column for history compatibility.
- Update tests and docs together when changing prompt routing, event payloads,
  config parsing, renderer output, history behavior, or subprocess command
  construction.
