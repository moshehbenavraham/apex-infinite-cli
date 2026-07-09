#!/usr/bin/env bash
set -euo pipefail

umask 077

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

fail() {
    printf 'Production launch error: %s\n' "$1" >&2
    exit 2
}

expand_home() {
    local value="$1"
    if [[ "$value" == \~ ]]; then
        printf '%s\n' "$HOME"
    elif [[ "$value" == \~/* ]]; then
        printf '%s/%s\n' "$HOME" "${value:2}"
    else
        printf '%s\n' "$value"
    fi
}

if [[ -z "${HOME:-}" ]]; then
    fail "HOME must be set for config, history, and state storage."
fi

PROJECT_PATH="${APEX_PRODUCTION_PATH:-${PROJECT:-}}"
if [[ -z "$PROJECT_PATH" ]]; then
    fail "set PROJECT=/absolute/path/to/an/initialized-apex-spec-project"
fi
PROJECT_PATH="$(expand_home "$PROJECT_PATH")"
if [[ "$PROJECT_PATH" != /* ]]; then
    fail "PROJECT must be an absolute path: $PROJECT_PATH"
fi
if [[ ! -d "$PROJECT_PATH" ]]; then
    fail "PROJECT directory does not exist: $PROJECT_PATH"
fi
if [[ ! -d "$PROJECT_PATH/.spec_system" ]]; then
    fail "PROJECT is not initialized: missing $PROJECT_PATH/.spec_system"
fi

CONFIG_PATH="${APEX_PRODUCTION_CONFIG:-${CONFIG:-${APEX_INFINITE_CONFIG:-}}}"
if [[ -z "$CONFIG_PATH" ]]; then
    CONFIG_PATH="${XDG_CONFIG_HOME:-$HOME/.config}/apex-infinite/config.yaml"
fi
CONFIG_PATH="$(expand_home "$CONFIG_PATH")"
if [[ "$CONFIG_PATH" != /* ]]; then
    fail "CONFIG must be an absolute path: $CONFIG_PATH"
fi
if [[ ! -f "$CONFIG_PATH" ]]; then
    fail "config not found: $CONFIG_PATH (run apex-infinite --setup or set CONFIG)"
fi

MAX_ITERATIONS_VALUE="${APEX_PRODUCTION_MAX_ITERATIONS:-${MAX_ITERATIONS:-50}}"
if [[ ! "$MAX_ITERATIONS_VALUE" =~ ^[1-9][0-9]*$ ]]; then
    fail "MAX_ITERATIONS must be a positive integer: $MAX_ITERATIONS_VALUE"
fi

if [[ -n "${APEX_PRODUCTION_START_COMMAND+x}" ]]; then
    START_COMMAND="$APEX_PRODUCTION_START_COMMAND"
else
    START_COMMAND="${START:-}"
fi

LOG_DIR_VALUE="${APEX_PRODUCTION_LOG_DIR:-${LOG_DIR:-}}"
if [[ -z "$LOG_DIR_VALUE" ]]; then
    LOG_DIR_VALUE="${XDG_STATE_HOME:-$HOME/.local/state}/apex-infinite/logs"
fi
LOG_DIR_VALUE="$(expand_home "$LOG_DIR_VALUE")"
if [[ "$LOG_DIR_VALUE" != /* ]]; then
    fail "LOG_DIR must be an absolute path: $LOG_DIR_VALUE"
fi
mkdir -p "$LOG_DIR_VALUE"
if [[ ! -d "$LOG_DIR_VALUE" || ! -w "$LOG_DIR_VALUE" ]]; then
    fail "LOG_DIR is not writable: $LOG_DIR_VALUE"
fi

CLI_BIN="${APEX_PRODUCTION_CLI:-$ROOT/.venv/bin/apex-infinite}"
CLI_BIN="$(expand_home "$CLI_BIN")"
if [[ "$CLI_BIN" == */* ]]; then
    if [[ ! -x "$CLI_BIN" ]]; then
        fail "apex-infinite executable not found: $CLI_BIN"
    fi
else
    RESOLVED_CLI="$(command -v "$CLI_BIN" || true)"
    if [[ -z "$RESOLVED_CLI" ]]; then
        fail "apex-infinite executable not found on PATH: $CLI_BIN"
    fi
    CLI_BIN="$RESOLVED_CLI"
fi

RUN_STAMP="$(date -u +%Y%m%dT%H%M%SZ)-$$"
PREFLIGHT_LOG="$LOG_DIR_VALUE/preflight-$RUN_STAMP.jsonl"
RUN_LOG="$LOG_DIR_VALUE/run-$RUN_STAMP.jsonl"

printf 'Apex Infinite production-like local run\n'
printf '  Project: %s\n' "$PROJECT_PATH"
printf '  Config: %s\n' "$CONFIG_PATH"
printf '  Start: %s\n' "${START_COMMAND:-manager auto-selection}"
printf '  Max iterations: %s\n' "$MAX_ITERATIONS_VALUE"
printf '  Preflight events: %s\n' "$PREFLIGHT_LOG"
printf '  Run events: %s\n' "$RUN_LOG"
printf 'Running readiness and provider chat checks...\n'

if ! "$CLI_BIN" \
    --config "$CONFIG_PATH" \
    --path "$PROJECT_PATH" \
    --doctor \
    --check-provider-chat \
    --event-stream "$PREFLIGHT_LOG"; then
    fail "readiness checks failed; the live run was not started"
fi

LIVE_ARGS=(
    --config "$CONFIG_PATH"
    --path "$PROJECT_PATH"
    --max-iterations "$MAX_ITERATIONS_VALUE"
    --check-provider-chat
    --event-stream "$RUN_LOG"
)
if [[ -n "$START_COMMAND" ]]; then
    LIVE_ARGS+=(--start "$START_COMMAND")
fi

printf 'Readiness checks passed. Starting live autonomous execution.\n'
exec "$CLI_BIN" "${LIVE_ARGS[@]}"
