"""Original packaged asset paths for the Hyperterminal wrapper.

Every asset here is Apex-owned with documented provenance. Nothing in this
package may reference or depend on the reference-only ``EXAMPLE/`` tree.
"""

from __future__ import annotations

from pathlib import Path

ASSET_DIR = Path(__file__).resolve().parent

ICON_NAME = "apex-infinite-visual.svg"
DESKTOP_NAME = "apex-infinite-visual.desktop"
APPSTREAM_NAME = "apex-infinite-visual.appdata.xml"


class AssetError(RuntimeError):
    """Raised when a packaged asset is missing."""


def asset_path(name: str) -> Path:
    """Return the path of one packaged asset, verifying it exists."""
    path = ASSET_DIR / name
    if not path.is_file():
        raise AssetError(f"packaged asset missing: {name}")
    return path


def icon_path() -> Path:
    """Return the original application icon path."""
    return asset_path(ICON_NAME)


def desktop_entry_path() -> Path:
    """Return the .desktop launcher entry path."""
    return asset_path(DESKTOP_NAME)


def appstream_path() -> Path:
    """Return the AppStream metadata path."""
    return asset_path(APPSTREAM_NAME)
