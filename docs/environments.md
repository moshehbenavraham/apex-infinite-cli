# Environments

## Runtime Environments

| Environment | URL Or Location | Purpose |
|-------------|-----------------|---------|
| Local CLI | Developer machine | Runs `apex-infinite` against an initialized Apex Spec project. |
| Local Ollama Docker | `http://127.0.0.1:11434` by default | Optional local OpenAI-compatible provider. |
| Hosted Grok provider | `https://api.x.ai/v1` | Optional hosted provider configured through `XAI_API_KEY`. |
| Hosted OpenAI provider | `https://api.openai.com/v1` | Optional hosted provider configured through `OPENAI_API_KEY`. |
| GitHub Actions quality job | `.github/workflows/quality.yml` | Installs `.[dev]`, then runs Black, Pylint, and mypy. |

No staging or production web service is defined in this repository.
`make production PROJECT=/absolute/path` is the strongest supported
production-like local operator profile: it gates live base-CLI execution on an
initialized project, shared config, terminal doctor, and provider chat check.
It does not deploy a service or change the source-shippable release position.

## Required Environment Variables

| Variable | Purpose | Secret |
|----------|---------|--------|
| `OLLAMA_HOST` | Host used for local Ollama provider URL expansion. | No |
| `OLLAMA_PORT` | Port used for local Ollama provider URL expansion. | No |
| `OLLAMA_API_KEY` | Placeholder key for OpenAI-compatible local Ollama calls. | Treat as secret if changed from local default. |
| `OLLAMA_MODEL` | Local Ollama model name. | No |
| `XAI_API_KEY` | Grok provider API key. | Yes |
| `OPENAI_API_KEY` | OpenAI provider API key. | Yes |
| `APEX_INFINITE_PROVIDER_CHECK_TIMEOUT` | Provider preflight timeout in seconds. | No |
| `APEX_INFINITE_LIVE_OLLAMA` | Opt-in flag for live Ollama tests. | No |
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
