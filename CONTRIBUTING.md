# Contributing

## Scope

Keep changes focused on the Apex Infinite CLI repository. The package metadata,
dependencies, entry points, pytest configuration, mypy configuration, Black
configuration, and Pylint configuration live in `pyproject.toml`.

## Branch Conventions

This repository does not encode branch protection rules, CODEOWNERS, or a
required branch naming policy. Use a focused branch per change and follow the
hosting repository rules when they exist.

## Commit Style

Use short imperative commit subjects. The current history uses subjects such as
`Add quality workflow and logging diagnostics` and
`Complete phase01-session05-agent-config-semantics: align Codex config semantics`.

## Local Verification

Use the repository virtualenv explicitly:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -e ".[dev,visual]"
.venv/bin/python -m pytest tests/ -v
.venv/bin/python -m black --check src tests
.venv/bin/python -m mypy
.venv/bin/python -m pylint src tests
```

Run `.venv/bin/python -m pip_audit` before release or dependency changes.

## Pull Request Process

1. Explain what changed and why.
2. Include the commands you ran and their results.
3. Update docs or transcripts when commands, config, output, event payloads,
   history behavior, or wrapper behavior changes.
4. Keep generated smoke artifacts outside the repository unless a fixture is
   intentionally updated.

## Security And Privacy

Do not commit provider API keys, local history databases, event-stream files
from real runs, or customer data. The CLI can send recent history, latest agent
output, summaries, operator instructions, and project paths to the configured
LLM provider; avoid placing secrets or personal data in prompts or target
project output.
