"""Visual profile persistence tests."""

import json

import pytest

from apex_infinite_visual.profile_store import (
    PROFILE_SCHEMA_VERSION,
    ProfileStore,
    ProfileStoreError,
    builtin_profiles,
    load_window_state,
    profile_from_settings,
    save_window_state,
)
from apex_infinite_visual.settings import (
    WRAPPER_THEME_NAMES,
    build_settings,
)


@pytest.fixture(name="store_path")
def store_path_fixture(tmp_path):
    """Return a temp profile file path."""
    return tmp_path / "visual-profiles.json"


def test_builtin_profiles_cover_every_theme_and_validate():
    profiles = builtin_profiles()

    assert set(profiles) == set(WRAPPER_THEME_NAMES)
    for profile in profiles.values():
        settings = profile.to_settings()
        assert settings.theme_name == profile.name
        assert profile.builtin is True


def test_save_and_reload_restores_custom_profile(store_path):
    store = ProfileStore(store_path)
    settings = build_settings(
        theme_name="apex-reactor",
        effect_intensity=80,
        quality_tier="cinematic",
        rendering_mode="cinematic",
    )
    store.save_current("night-ops", settings)

    reloaded = ProfileStore(store_path)
    profile = reloaded.get("night-ops")
    assert reloaded.last_profile == "night-ops"
    assert profile.theme_name == "apex-reactor"
    assert profile.quality_tier == "cinematic"
    assert profile.effect_intensity == 80
    assert reloaded.is_builtin("night-ops") is False


def test_saving_over_builtin_name_is_rejected(store_path):
    store = ProfileStore(store_path)

    with pytest.raises(ProfileStoreError, match="built-in"):
        store.save_current("plain", build_settings())


def test_duplicate_rename_delete_and_reset(store_path):
    store = ProfileStore(store_path)
    store.save_current("base", build_settings(theme_name="blackbox"))

    store.duplicate("base", "base-copy")
    assert store.get("base-copy").theme_name == "blackbox"

    store.rename("base-copy", "ops")
    assert "base-copy" not in store.profile_names()
    assert store.get("ops").theme_name == "blackbox"

    store.delete("ops")
    with pytest.raises(ProfileStoreError):
        store.get("ops")

    with pytest.raises(ProfileStoreError, match="custom"):
        store.delete("crt-green")

    reset = store.reset_builtin("crt-green")
    assert reset.builtin is True


def test_import_export_round_trip(store_path, tmp_path):
    store = ProfileStore(store_path)
    store.save_current(
        "exported", build_settings(theme_name="incident-red", effect_intensity=66)
    )
    export_path = tmp_path / "exported.json"
    store.export_profile("exported", export_path)

    payload = json.loads(export_path.read_text(encoding="ascii"))
    assert payload["version"] == PROFILE_SCHEMA_VERSION
    assert payload["theme_name"] == "incident-red"

    other = ProfileStore(tmp_path / "other.json")
    imported = other.import_profile(export_path, rename_to="imported")
    assert imported.effect_intensity == 66
    assert other.get("imported").theme_name == "incident-red"


def test_import_rejects_secret_fields_and_bad_schema(store_path, tmp_path):
    store = ProfileStore(store_path)
    bad = tmp_path / "bad.json"

    bad.write_text(json.dumps({"version": 99, "name": "x"}), encoding="ascii")
    with pytest.raises(ProfileStoreError, match="version"):
        store.import_profile(bad)

    profile = profile_from_settings("ok", build_settings()).to_payload()
    profile["api_key"] = "sk-not-a-real-key"
    bad.write_text(json.dumps(profile), encoding="ascii")
    with pytest.raises(ProfileStoreError, match="secret"):
        store.import_profile(bad)

    profile = profile_from_settings("ok", build_settings()).to_payload()
    profile["theme_name"] = "not-a-theme"
    bad.write_text(json.dumps(profile), encoding="ascii")
    with pytest.raises(ProfileStoreError, match="invalid profile values"):
        store.import_profile(bad)


def test_non_ascii_profile_names_are_rejected(store_path):
    store = ProfileStore(store_path)

    with pytest.raises(ProfileStoreError, match="ASCII"):
        store.save_current("caf\u00e9", build_settings())
    with pytest.raises(ProfileStoreError, match="path"):
        store.save_current("a/b", build_settings())


def test_corrupt_profile_file_is_backed_up_and_startup_survives(store_path):
    store_path.write_text("{not valid json", encoding="ascii")

    store = ProfileStore(store_path)

    assert store.load_error
    assert store.profile_names() == list(builtin_profiles())
    backup = store_path.with_suffix(store_path.suffix + ".corrupt")
    assert backup.exists()


def test_window_state_round_trip_and_corruption(tmp_path):
    state_path = tmp_path / "visual-state.json"
    save_window_state({"width": 1280, "height": 800}, state_path)

    assert load_window_state(state_path) == {"width": 1280, "height": 800}

    state_path.write_text("broken", encoding="ascii")
    assert load_window_state(state_path) == {}


def test_default_paths_honor_xdg_env(monkeypatch, tmp_path):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "cfg"))
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))

    from apex_infinite_visual import profile_store as module

    assert module.default_profile_path() == (
        tmp_path / "cfg" / "apex-infinite" / "visual-profiles.json"
    )
    assert module.default_state_path() == (
        tmp_path / "state" / "apex-infinite" / "visual-state.json"
    )
