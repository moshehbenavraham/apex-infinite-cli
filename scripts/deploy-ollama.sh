#!/usr/bin/env bash
# Compatibility wrapper. Prefer scripts/ollama-docker.sh for new usage.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

exec "${SCRIPT_DIR}/ollama-docker.sh" "$@"
