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

VISUAL_OVERRIDE="${APEX_PRODUCTION_VISUAL:-}"
VISUAL_BIN="${VISUAL_OVERRIDE:-$ROOT/.venv/bin/apex-infinite-visual}"
VISUAL_BIN="$(expand_home "$VISUAL_BIN")"
if [[ "$VISUAL_BIN" == */* ]]; then
    if [[ ! -x "$VISUAL_BIN" ]]; then
        fail "visual executable not found: $VISUAL_BIN (install .[visual])"
    fi
else
    RESOLVED_VISUAL="$(command -v "$VISUAL_BIN" || true)"
    if [[ -z "$RESOLVED_VISUAL" ]]; then
        fail "visual executable not found on PATH: $VISUAL_BIN (install .[visual])"
    fi
    VISUAL_BIN="$RESOLVED_VISUAL"
fi
if [[ -z "$VISUAL_OVERRIDE" && -z "${DISPLAY:-}" && -z "${WAYLAND_DISPLAY:-}" ]]; then
    case "${QT_QPA_PLATFORM:-}" in
        offscreen|minimal) ;;
        *) fail "visual production requires DISPLAY or WAYLAND_DISPLAY" ;;
    esac
fi

PYTHON_BIN="$ROOT/.venv/bin/python"
if [[ ! -x "$PYTHON_BIN" ]]; then
    fail "production settings resolver not found: $PYTHON_BIN"
fi

PROJECT_SELECTION="${APEX_PRODUCTION_PATH:-${PROJECT:-}}"
CONFIG_SELECTION="${APEX_PRODUCTION_CONFIG:-${CONFIG:-${APEX_INFINITE_CONFIG:-}}}"
SETTINGS_ARGS=()
if [[ -n "$PROJECT_SELECTION" ]]; then
    SETTINGS_ARGS+=(--project "$PROJECT_SELECTION")
fi
if [[ -n "$CONFIG_SELECTION" ]]; then
    SETTINGS_ARGS+=(--config "$CONFIG_SELECTION")
fi

SETTINGS_OUTPUT=""
if ! SETTINGS_OUTPUT="$(
    "$PYTHON_BIN" \
        -m apex_infinite.production_config \
        "${SETTINGS_ARGS[@]}"
)"; then
    exit 2
fi
mapfile -t RESOLVED_SETTINGS <<< "$SETTINGS_OUTPUT"
if [[ "${#RESOLVED_SETTINGS[@]}" -ne 2 ]]; then
    fail "settings resolver returned an invalid response"
fi
CONFIG_PATH="${RESOLVED_SETTINGS[0]}"
PROJECT_PATH="${RESOLVED_SETTINGS[1]}"

CONFIG_PATH="$(expand_home "$CONFIG_PATH")"
if [[ "$CONFIG_PATH" != /* ]]; then
    fail "CONFIG must be an absolute path: $CONFIG_PATH"
fi
if [[ ! -f "$CONFIG_PATH" ]]; then
    fail "config not found: $CONFIG_PATH (run apex-infinite --setup or set CONFIG)"
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

RUN_STAMP="$(date -u +%Y%m%dT%H%M%SZ)-$$"
PREFLIGHT_LOG="$LOG_DIR_VALUE/preflight-$RUN_STAMP.jsonl"

printf 'Apex Infinite visual production-like local run\n'
printf '  Project: %s\n' "$PROJECT_PATH"
printf '  Config: %s\n' "$CONFIG_PATH"
printf '  Start: %s\n' "${START_COMMAND:-manager auto-selection}"
printf '  Max iterations: %s\n' "$MAX_ITERATIONS_VALUE"
printf '  Preflight events: %s\n' "$PREFLIGHT_LOG"
printf '  Run events directory: %s\n' "$LOG_DIR_VALUE"
printf 'Running readiness and provider chat checks...\n'

if ! "$CLI_BIN" \
    --config "$CONFIG_PATH" \
    --path "$PROJECT_PATH" \
    --doctor \
    --doctor-visual \
    --check-provider-chat \
    --event-stream "$PREFLIGHT_LOG"; then
    fail "readiness checks failed; the visual console was not started"
fi

VISUAL_ARGS=(
    --config "$CONFIG_PATH"
    --path "$PROJECT_PATH"
    --start-command "$START_COMMAND"
    --max-iterations "$MAX_ITERATIONS_VALUE"
    --launch-cli
    --require-initialized-project
    --run-log-dir "$LOG_DIR_VALUE"
    --no-restore-profile
    --theme "${APEX_VISUAL_THEME:-apex-reactor}"
    --rendering-mode "${APEX_VISUAL_RENDERING_MODE:-cinematic}"
    --quality-tier "${APEX_VISUAL_QUALITY_TIER:-balanced}"
    --effect-intensity "${APEX_VISUAL_EFFECT_INTENSITY:-85}"
)

printf 'Readiness checks passed. Opening the live visual console.\n'
printf 'Review the controls, then click Start to begin autonomous execution.\n'
exec "$VISUAL_BIN" "${VISUAL_ARGS[@]}"
