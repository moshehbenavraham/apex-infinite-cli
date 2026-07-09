# Environments

## Runtime Environments

| Environment | URL Or Location | Purpose |
|-------------|-----------------|---------|
| Local CLI | Developer machine | Runs `apex-infinite` against an initialized Apex Spec project. |
| Local visual wrapper | Graphical Linux session | Runs `apex-infinite-visual`; `make production` uses it after guarded preflight. |
| Local Ollama Docker | `http://127.0.0.1:11434` by default | Optional local OpenAI-compatible provider. |
| Hosted Grok provider | `https://api.x.ai/v1` | Optional hosted provider configured through `XAI_API_KEY`. |
| Hosted OpenAI provider | `https://api.openai.com/v1` | Optional hosted provider configured through `OPENAI_API_KEY`. |
| GitHub Actions quality job | `.github/workflows/quality.yml` | Installs `.[dev]`, then runs Black, Pylint, and mypy. |

No staging or production web service is defined in this repository.
`make production` is the strongest supported production-like local operator
profile: it gates a live base-CLI run on an initialized project, resolved
config, terminal doctor, visual dependencies, and a provider chat check. It
then opens the visual wrapper in live mode and waits for the operator to click
`Start`. Supply `PROJECT` explicitly or configure a reusable environment,
`.env`, or YAML project default. The repository `.[visual]` environment and a
graphical Linux session must already be available. This does not deploy a
service or change the source-shippable release position.

## Runtime Environment Variables

| Variable | Purpose | Secret |
|----------|---------|--------|
| `OLLAMA_HOST` | Host used for local Ollama provider URL expansion. | No |
| `OLLAMA_PORT` | Port used for local Ollama provider URL expansion. | No |
| `OLLAMA_API_KEY` | Placeholder key for OpenAI-compatible local Ollama calls. | Treat as secret if changed from local default. |
| `OLLAMA_MODEL` | Local Ollama model name. | No |
| `XAI_API_KEY` | Grok provider API key. | Yes |
| `OPENAI_API_KEY` | OpenAI provider API key. | Yes |
| `APEX_INFINITE_DEFAULT_PROJECT` | Default project when no explicit path is supplied. | No |
| `APEX_INFINITE_PROVIDER_CHECK_TIMEOUT` | Provider preflight timeout in seconds. | No |
| `APEX_INFINITE_LIVE_OLLAMA` | Opt-in flag for live Ollama tests. | No |
| `APEX_VISUAL_THEME` | Visual theme used by development and production launchers. | No |
| `APEX_VISUAL_RENDERING_MODE` | Visual rendering mode used by development and production launchers. | No |
| `APEX_VISUAL_QUALITY_TIER` | Visual quality tier used by development and production launchers. | No |
| `APEX_VISUAL_EFFECT_INTENSITY` | Visual effect intensity used by development and production launchers. | No |
| `OLLAMA_DOCKER_PROJECT` | Docker Compose project name for local Ollama. | No |
| `OLLAMA_DOCKER_CONTAINER` | Local Ollama container name. | No |
| `OLLAMA_DOCKER_IMAGE` | Ollama Docker image tag. | No |
| `OLLAMA_DOCKER_VOLUME` | Docker volume for model data. | No |
| `OLLAMA_DOCKER_BIND_HOST` | Host interface for published Ollama port. | No |
| `OLLAMA_DOCKER_GPU` | `auto`, CPU, or GPU mode selection for local Ollama. | No |
| `OLLAMA_DOCKER_WAIT_SECONDS` | Startup wait time for local Ollama readiness. | No |
| `OLLAMA_DOCKER_PROGRESS` | Docker progress output mode. | No |
| `OLLAMA_KEEP_ALIVE` | Ollama model keep-alive setting. | No |
| `OLLAMA_CHAT_CHECK_TIMEOUT` | Timeout for chat-based local Ollama checks. | No |

`src/apex_infinite/config.yaml` expands provider values from environment
variables at runtime. The repository `.env.example` contains placeholders and
local defaults only; real hosted provider keys belong in `.env` or the shell
environment and must not be committed.

For production launches, an explicit `APEX_PRODUCTION_PATH` or `PROJECT` wins,
followed by `APEX_INFINITE_DEFAULT_PROJECT` from the environment or `.env`,
then config `defaults.project`. Config resolution falls through to packaged
defaults when no explicit selection or user config exists; an explicitly
selected missing `CONFIG` remains an error.

Production invokes the preinstalled visual executable directly, not
`scripts/run-visual.sh`. The guarded preflight log is created before the window
opens; the wrapper run log is created only after the operator clicks `Start`.

## Data Locations

| Path | Purpose |
|------|---------|
| `~/.apex-infinite/history.db` | Local SQLite history for manager decisions, reasons, agent responses, project paths, and state. |
| `logs/` | Local diagnostic logs when logging is configured. |
| `/tmp/apex-infinite-*` | Recommended location for release smoke event streams, history homes, and build artifacts. |

## Security Notes

The manager and summarizer can send recent history, latest agent output,
operator instructions, summaries, and project paths to the configured provider.
Do not put provider keys, secrets, personal data, or customer data in operator
instructions or target-project output.
