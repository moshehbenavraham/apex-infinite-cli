# Onboarding

## Prerequisites

- [ ] Python 3.10 or newer.
- [ ] Codex CLI installed and available as `codex`, or configured through
      `codex.binary`.
- [ ] A configured LLM provider: local Ollama, Grok, or OpenAI.
- [ ] Provider secrets exported through `.env` or the shell environment.
- [ ] Docker with Docker Compose if using the local Ollama helper scripts.
- [ ] PySide6/Qt Quick only when running the optional visual wrapper.

## Setup Steps

1. Create and activate the repository virtualenv through explicit paths:

   ```bash
   python3 -m venv .venv
   .venv/bin/python -m pip install --upgrade pip
   .venv/bin/python -m pip install -e ".[dev,visual]"
   ```

2. Create local provider environment settings:

   ```bash
   cp .env.example .env
   ```

3. Edit `.env` for hosted provider keys or local Ollama values. Do not commit
   real keys.

4. For local Ollama, start the Docker service and check chat completion:

   ```bash
   ./scripts/ollama-docker.sh --chat
   ```

5. Verify CLI configuration and provider availability:

   ```bash
   .venv/bin/apex-infinite --check-provider
   ```

6. Dry-run an initialized Apex Spec project before real execution:

   ```bash
   .venv/bin/apex-infinite --path /path/to/apex-spec-project --start plansession --dry-run
   ```

## Verify Setup

- [ ] `.venv/bin/apex-infinite --help`
- [ ] `.venv/bin/apex-infinite --check-provider`
- [ ] `.venv/bin/python -m pytest tests/ -v`
- [ ] `.venv/bin/python -m black --check src tests`
- [ ] `.venv/bin/python -m mypy`
- [ ] `.venv/bin/python -m pylint src tests`

## First Real Run

After dry-run output shows the expected target path, provider, model, Codex
binary, flags, and reasoning effort, start the autonomous loop:

```bash
.venv/bin/apex-infinite --path /path/to/apex-spec-project --start plansession
```

Use `--plain --ascii --compact` for log-oriented shells or CI-style captures.
