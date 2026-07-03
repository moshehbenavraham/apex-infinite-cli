#!/usr/bin/env bash
# Start project-local Ollama Docker service and pull the configured model.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLI_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

ACTION="up"
CHAT_CHECK=0
GPU_OVERRIDE=""
MODEL_OVERRIDE=""
PULL_MODEL=1

usage() {
    cat <<'EOF'
Usage: deploy-ollama.sh [action] [options]

Actions:
  up        Start Ollama and pull OLLAMA_MODEL (default)
  pull      Pull OLLAMA_MODEL into the running container
  status    Show container and model status
  logs      Show recent Ollama container logs
  down      Stop the Ollama container without deleting model data
  restart   Restart Ollama and pull OLLAMA_MODEL

Options:
  --model MODEL       Override OLLAMA_MODEL for this run
  --gpu              Force Docker GPU mode
  --cpu              Force CPU-only Docker mode
  --no-pull          Start container without pulling OLLAMA_MODEL
  --chat             Run scripts/check-ollama.sh --chat after deploy
  -h, --help         Show this help

Environment:
  Reads .env.example first, then .env if present. Relevant variables:
  OLLAMA_HOST, OLLAMA_PORT, OLLAMA_MODEL, OLLAMA_DOCKER_*, OLLAMA_KEEP_ALIVE.
EOF
}

die() {
    printf 'deploy-ollama.sh: %s\n' "$*" >&2
    exit 1
}

load_env_file() {
    local env_file="$1"
    if [[ -f "$env_file" ]]; then
        set -a
        # shellcheck disable=SC1090
        . "$env_file"
        set +a
    fi
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        up | pull | status | logs | down | restart)
            ACTION="$1"
            shift
            ;;
        --model)
            MODEL_OVERRIDE="${2:?missing value for --model}"
            shift 2
            ;;
        --gpu)
            GPU_OVERRIDE="1"
            shift
            ;;
        --cpu)
            GPU_OVERRIDE="0"
            shift
            ;;
        --no-pull)
            PULL_MODEL=0
            shift
            ;;
        --chat)
            CHAT_CHECK=1
            shift
            ;;
        -h | --help)
            usage
            exit 0
            ;;
        *)
            die "unknown option or action: $1"
            ;;
    esac
done

load_env_file "${CLI_DIR}/.env.example"
load_env_file "${CLI_DIR}/.env"

if [[ -n "$MODEL_OVERRIDE" ]]; then
    OLLAMA_MODEL="$MODEL_OVERRIDE"
    export OLLAMA_MODEL
fi

OLLAMA_HOST="${OLLAMA_HOST:-localhost}"
OLLAMA_PORT="${OLLAMA_PORT:-11434}"
OLLAMA_MODEL="${OLLAMA_MODEL:-qwen2.5-coder:7b-instruct-q4_K_M}"
OLLAMA_DOCKER_CONTAINER="${OLLAMA_DOCKER_CONTAINER:-apex-infinite-ollama}"
OLLAMA_DOCKER_WAIT_SECONDS="${OLLAMA_DOCKER_WAIT_SECONDS:-180}"
OLLAMA_DOCKER_GPU="${GPU_OVERRIDE:-${OLLAMA_DOCKER_GPU:-auto}}"

export OLLAMA_HOST OLLAMA_PORT OLLAMA_MODEL
export OLLAMA_DOCKER_CONTAINER OLLAMA_DOCKER_WAIT_SECONDS OLLAMA_DOCKER_GPU

command -v docker >/dev/null 2>&1 || die "docker is not installed or not on PATH"
docker compose version >/dev/null 2>&1 || die "docker compose is not available"

has_nvidia_runtime() {
    docker info --format '{{json .Runtimes}}' 2>/dev/null | grep -q '"nvidia"'
}

use_gpu_compose() {
    case "${OLLAMA_DOCKER_GPU,,}" in
        1 | true | yes | on | all | gpu)
            has_nvidia_runtime || die "GPU mode requested, but Docker NVIDIA runtime was not found"
            return 0
            ;;
        0 | false | no | off | cpu)
            return 1
            ;;
        auto)
            has_nvidia_runtime
            return
            ;;
        *)
            die "invalid OLLAMA_DOCKER_GPU value: ${OLLAMA_DOCKER_GPU}"
            ;;
    esac
}

compose_args() {
    printf '%s\0' compose -f "${CLI_DIR}/docker-compose.ollama.yml"
    if use_gpu_compose; then
        printf '%s\0' -f "${CLI_DIR}/docker-compose.ollama.gpu.yml"
    fi
}

docker_compose() {
    local args=()
    while IFS= read -r -d '' item; do
        args+=("$item")
    done < <(compose_args)
    docker "${args[@]}" "$@"
}

client_base_url() {
    local host="$OLLAMA_HOST"
    host="${host#http://}"
    host="${host#https://}"
    host="${host%%/*}"
    if [[ "$host" == *:* ]]; then
        printf 'http://%s' "$host"
    else
        printf 'http://%s:%s' "$host" "$OLLAMA_PORT"
    fi
}

wait_for_ollama() {
    local base_url deadline
    base_url="$(client_base_url)"
    deadline=$((SECONDS + OLLAMA_DOCKER_WAIT_SECONDS))

    printf 'Waiting for Ollama at %s ...\n' "$base_url"
    while (( SECONDS < deadline )); do
        if command -v curl >/dev/null 2>&1; then
            if curl -fsS "${base_url}/api/tags" >/dev/null 2>&1; then
                printf 'Ollama API is ready.\n'
                return 0
            fi
        elif docker_compose exec -T ollama ollama list >/dev/null 2>&1; then
            printf 'Ollama container is ready.\n'
            return 0
        fi
        sleep 2
    done

    die "Ollama did not become ready within ${OLLAMA_DOCKER_WAIT_SECONDS}s"
}

pull_model() {
    [[ -n "$OLLAMA_MODEL" ]] || die "OLLAMA_MODEL is empty"
    printf 'Pulling Ollama model: %s\n' "$OLLAMA_MODEL"
    docker_compose exec -T ollama ollama pull "$OLLAMA_MODEL"
}

show_status() {
    docker_compose ps
    printf '\nConfigured model: %s\n' "$OLLAMA_MODEL"
    printf 'Client URL: %s\n\n' "$(client_base_url)"
    if docker_compose ps --status running --services | grep -qx 'ollama'; then
        docker_compose exec -T ollama ollama list
    fi
}

cd "$CLI_DIR"

case "$ACTION" in
    up)
        docker_compose up -d
        wait_for_ollama
        if [[ "$PULL_MODEL" == "1" ]]; then
            pull_model
        fi
        show_status
        ;;
    pull)
        docker_compose up -d
        wait_for_ollama
        pull_model
        show_status
        ;;
    status)
        show_status
        ;;
    logs)
        docker_compose logs --tail=200 ollama
        ;;
    down)
        docker_compose down
        ;;
    restart)
        docker_compose up -d --force-recreate
        wait_for_ollama
        if [[ "$PULL_MODEL" == "1" ]]; then
            pull_model
        fi
        show_status
        ;;
esac

if [[ "$CHAT_CHECK" == "1" && "$ACTION" != "down" && "$ACTION" != "logs" ]]; then
    "${SCRIPT_DIR}/check-ollama.sh" --chat
fi
