#!/usr/bin/env bash
# Compile Apex-owned shader sources to Qt 6 .qsb artifacts.
#
# Artifacts land in src/apex_infinite_visual/shaders/compiled/ and are
# intentionally untracked: regenerate and review them before any release
# that bundles shader effects. See shaders/PROVENANCE.md.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SHADER_DIR="$REPO_ROOT/src/apex_infinite_visual/shaders"
OUT_DIR="$SHADER_DIR/compiled"

QSB_BIN="${QSB:-}"
if [[ -z "$QSB_BIN" ]]; then
    if [[ -x "$REPO_ROOT/.venv/bin/pyside6-qsb" ]]; then
        QSB_BIN="$REPO_ROOT/.venv/bin/pyside6-qsb"
    elif command -v pyside6-qsb >/dev/null 2>&1; then
        QSB_BIN="pyside6-qsb"
    elif command -v qsb >/dev/null 2>&1; then
        QSB_BIN="qsb"
    else
        echo "error: no qsb tool found (install the visual extra or Qt tools)" >&2
        exit 1
    fi
fi

mkdir -p "$OUT_DIR"

shopt -s nullglob
compiled=0
for source in "$SHADER_DIR"/*.frag "$SHADER_DIR"/*.vert; do
    name="$(basename "$source")"
    target="$OUT_DIR/$name.qsb"
    echo "qsb: $name -> compiled/$name.qsb"
    "$QSB_BIN" --glsl "100 es,120,150" --hlsl 50 --msl 12 -o "$target" "$source"
    compiled=$((compiled + 1))
done

if [[ "$compiled" -eq 0 ]]; then
    echo "error: no shader sources found in $SHADER_DIR" >&2
    exit 1
fi

echo "Compiled $compiled shader artifact(s) into $OUT_DIR"
echo "Review artifacts before bundling them in a release."
