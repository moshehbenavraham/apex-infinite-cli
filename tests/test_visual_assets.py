"""Packaged asset and clean-room guard tests."""

import subprocess
from pathlib import Path

import pytest

from apex_infinite_visual.assets import (
    AssetError,
    appstream_path,
    asset_path,
    desktop_entry_path,
    icon_path,
)

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_icon_is_original_svg():
    path = icon_path()
    text = path.read_text(encoding="utf-8")

    assert path.suffix == ".svg"
    assert "<svg" in text
    assert "Original artwork" in text


def test_desktop_entry_declares_launcher_actions():
    text = desktop_entry_path().read_text(encoding="utf-8")

    assert "[Desktop Entry]" in text
    assert "Exec=apex-infinite-visual" in text
    assert "[Desktop Action Doctor]" in text
    assert "[Desktop Action DryRun]" in text
    assert "Icon=apex-infinite-visual" in text


def test_appstream_metadata_has_required_fields():
    text = appstream_path().read_text(encoding="utf-8")

    assert '<component type="desktop-application">' in text
    assert "<project_license>MIT</project_license>" in text
    assert "<launchable" in text
    assert "<releases>" in text


def test_missing_asset_raises_clear_error():
    with pytest.raises(AssetError, match="missing"):
        asset_path("does-not-exist.png")


def test_no_example_tree_files_are_tracked():
    tracked = subprocess.run(
        ["git", "ls-files"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.splitlines()

    assert not [path for path in tracked if path.startswith("EXAMPLE/")]


def test_no_generated_shader_blobs_are_tracked():
    tracked = subprocess.run(
        ["git", "ls-files"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.splitlines()

    assert not [path for path in tracked if path.endswith(".qsb")]


def test_shader_sources_document_provenance():
    shader_dir = REPO_ROOT / "src" / "apex_infinite_visual" / "shaders"
    sources = sorted(shader_dir.glob("*.frag"))

    assert len(sources) == 6
    for source in sources:
        assert "PROVENANCE.md" in source.read_text(encoding="ascii")
    assert (shader_dir / "PROVENANCE.md").is_file()


def test_notices_cover_pyside_lgpl_path():
    notices = (REPO_ROOT / "packaging" / "NOTICES.md").read_text(encoding="utf-8")

    assert "PySide6" in notices
    assert "LGPL" in notices
    assert "Clean-Room" in notices
