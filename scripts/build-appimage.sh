#!/usr/bin/env bash
# Build the Apex Infinite Hyperterminal AppImage.
#
# Clean-room packaging: everything bundled here is built from this
# repository and PyPI wheels. Nothing is copied from the reference-only
# EXAMPLE/ tree. Output artifacts land in build/appimage/dist and are not
# tracked by git.
#
# Requirements: python3.10+, appimagetool on PATH (or APPIMAGETOOL env),
# and network access for pip wheels on first run.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BUILD_ROOT="$REPO_ROOT/build/appimage"
APPDIR="$BUILD_ROOT/AppDir"
DIST_DIR="$BUILD_ROOT/dist"
VERSION="$(grep -m1 '^version' "$REPO_ROOT/pyproject.toml" | sed 's/.*"\(.*\)"/\1/')"
OUTPUT_NAME="apex-infinite-visual-linux-x86_64.AppImage"

APPIMAGETOOL="${APPIMAGETOOL:-appimagetool}"
if ! command -v "$APPIMAGETOOL" >/dev/null 2>&1; then
    echo "error: appimagetool not found; install it or set APPIMAGETOOL" >&2
    exit 1
fi

echo "==> Cleaning build root"
rm -rf "$BUILD_ROOT"
mkdir -p "$APPDIR/usr" "$DIST_DIR"

echo "==> Building wheel"
python3 -m venv "$BUILD_ROOT/buildenv"
"$BUILD_ROOT/buildenv/bin/pip" install --quiet --upgrade pip build
(cd "$REPO_ROOT" && "$BUILD_ROOT/buildenv/bin/python" -m build --wheel \
    --outdir "$BUILD_ROOT/wheels")

echo "==> Creating bundled runtime"
python3 -m venv "$APPDIR/usr/venv"
"$APPDIR/usr/venv/bin/pip" install --quiet --upgrade pip
"$APPDIR/usr/venv/bin/pip" install --quiet \
    "$(ls "$BUILD_ROOT"/wheels/apex_infinite_cli-*.whl)[visual]"

# Nuitka is a build-time tool from the visual extra; the shipped bundle
# runs from source wheels (see packaging/RELEASE-CHECKLIST.md decision
# record) and must not carry it.
echo "==> Removing build-only tools from the bundle"
"$APPDIR/usr/venv/bin/pip" uninstall --quiet -y Nuitka

echo "==> Writing dependency inventory"
"$APPDIR/usr/venv/bin/pip" freeze > "$DIST_DIR/dependency-inventory.txt"

echo "==> Installing desktop metadata"
ASSET_DIR="$REPO_ROOT/src/apex_infinite_visual/assets"
cp "$ASSET_DIR/apex-infinite-visual.desktop" "$APPDIR/"
cp "$ASSET_DIR/apex-infinite-visual.svg" "$APPDIR/apex-infinite-visual.svg"
mkdir -p "$APPDIR/usr/share/metainfo" \
    "$APPDIR/usr/share/applications" \
    "$APPDIR/usr/share/icons/hicolor/scalable/apps"
# AppStream requires the installed metainfo filename to match the
# component id (org.apexinfinite.Hyperterminal).
cp "$ASSET_DIR/apex-infinite-visual.appdata.xml" \
    "$APPDIR/usr/share/metainfo/org.apexinfinite.Hyperterminal.appdata.xml"
cp "$ASSET_DIR/apex-infinite-visual.desktop" "$APPDIR/usr/share/applications/"
cp "$ASSET_DIR/apex-infinite-visual.svg" \
    "$APPDIR/usr/share/icons/hicolor/scalable/apps/"

echo "==> Writing notices"
cp "$REPO_ROOT/LICENSE" "$APPDIR/LICENSE"
cp "$REPO_ROOT/packaging/NOTICES.md" "$APPDIR/NOTICES.md"

echo "==> Writing AppRun"
cat > "$APPDIR/AppRun" <<'APPRUN'
#!/usr/bin/env bash
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PATH="$HERE/usr/venv/bin:$PATH"
exec "$HERE/usr/venv/bin/apex-infinite-visual" "$@"
APPRUN
chmod +x "$APPDIR/AppRun"

echo "==> Building AppImage"
(cd "$BUILD_ROOT" && ARCH=x86_64 "$APPIMAGETOOL" "$APPDIR" \
    "$DIST_DIR/$OUTPUT_NAME")

echo "==> Writing checksum"
(cd "$DIST_DIR" && sha256sum "$OUTPUT_NAME" > "$OUTPUT_NAME.sha256")

echo
echo "AppImage: $DIST_DIR/$OUTPUT_NAME (version $VERSION)"
echo "Checksum: $DIST_DIR/$OUTPUT_NAME.sha256"
echo "Inventory: $DIST_DIR/dependency-inventory.txt"
echo
echo "Verify on a clean machine before release:"
echo "  ./$OUTPUT_NAME --dry-run --auto-close-ms 2000"
