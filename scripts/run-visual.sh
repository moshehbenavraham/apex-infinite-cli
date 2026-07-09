#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="${PYTHON:-python3}"
VENV_PYTHON="$ROOT/.venv/bin/python"
VISUAL_BIN="$ROOT/.venv/bin/apex-infinite-visual"
VISUAL_CONFIG="${APEX_VISUAL_CONFIG:-$ROOT/src/apex_infinite/config.yaml}"
VISUAL_PATH="${APEX_VISUAL_PATH:-$ROOT}"
VISUAL_START_COMMAND="${APEX_VISUAL_START_COMMAND:-implement}"
VISUAL_LAUNCH_CLI="${APEX_VISUAL_LAUNCH_CLI:-0}"
VISUAL_DRY_RUN="${APEX_VISUAL_DRY_RUN:-1}"

cd "$ROOT"

if [[ ! -x "$VENV_PYTHON" ]]; then
    echo "Creating .venv..."
    "$PYTHON_BIN" -m venv "$ROOT/.venv"
fi

if [[ ! -x "$VISUAL_BIN" ]] || ! "$VENV_PYTHON" -c "import PySide6" >/dev/null 2>&1; then
    echo "Installing visual dependencies..."
    "$VENV_PYTHON" -m pip install --upgrade pip
    "$VENV_PYTHON" -m pip install -e ".[dev,visual]"
fi

ARGS=(
    --config "$VISUAL_CONFIG"
    --path "$VISUAL_PATH"
    --start-command "$VISUAL_START_COMMAND"
    --max-iterations "${APEX_VISUAL_MAX_ITERATIONS:-1}"
    --no-restore-profile
    --theme "${APEX_VISUAL_THEME:-apex-reactor}"
    --rendering-mode "${APEX_VISUAL_RENDERING_MODE:-cinematic}"
    --quality-tier "${APEX_VISUAL_QUALITY_TIER:-balanced}"
    --effect-intensity "${APEX_VISUAL_EFFECT_INTENSITY:-85}"
)

if [[ "$VISUAL_LAUNCH_CLI" == "1" ]]; then
    ARGS+=(--launch-cli)
fi

if [[ "$VISUAL_DRY_RUN" != "0" ]]; then
    ARGS+=(--dry-run)
fi

exec "$VISUAL_BIN" "${ARGS[@]}" "$@"
