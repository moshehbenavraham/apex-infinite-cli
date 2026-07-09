"""XDG-backed visual profile persistence for the Hyperterminal wrapper.

Profiles are wrapper-only presentation state. They never contain provider
secrets and never touch the shared CLI config file. Storage is versioned
JSON with atomic writes and corruption backups so a damaged file cannot
break startup.
"""

from __future__ import annotations

import json
import os
import tempfile
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from apex_infinite_visual.settings import (
    EFFECT_NAMES,
    THEME_PRESETS,
    WrapperSettings,
    WrapperSettingsError,
    build_settings,
    default_settings,
)

PROFILE_SCHEMA_VERSION = 1
PROFILE_FILE_NAME = "visual-profiles.json"
STATE_FILE_NAME = "visual-state.json"
MAX_PROFILE_NAME_LENGTH = 64

_SECRET_KEY_TOKENS = ("key", "secret", "token", "password", "credential")


class ProfileStoreError(ValueError):
    """Raised when profile persistence input or storage is invalid."""


@dataclass(frozen=True)
class VisualProfile:  # pylint: disable=too-many-instance-attributes
    """One versioned, validated visual profile."""

    name: str
    theme_name: str
    rendering_mode: str
    quality_tier: str
    effect_intensity: int
    font_family: str
    font_scale: float
    font_width: float
    line_spacing: float
    reduced_effects: bool
    plain_fallback: bool
    effects: dict[str, bool] = field(default_factory=dict)
    builtin: bool = False

    def to_settings(self) -> WrapperSettings:
        """Return validated wrapper settings for this profile."""
        return build_settings(
            theme_name=self.theme_name,
            effect_intensity=self.effect_intensity,
            font_family=self.font_family,
            font_scale=self.font_scale,
            reduced_effects=self.reduced_effects,
            plain_fallback=self.plain_fallback,
            rendering_mode=self.rendering_mode,
            quality_tier=self.quality_tier,
            font_width=self.font_width,
            line_spacing=self.line_spacing,
        )

    def to_payload(self) -> dict[str, Any]:
        """Return the JSON payload for export or storage."""
        payload = asdict(self)
        payload.pop("builtin", None)
        payload["version"] = PROFILE_SCHEMA_VERSION
        return payload


def profile_from_settings(
    name: str, settings: WrapperSettings, effects: dict[str, bool] | None = None
) -> VisualProfile:
    """Capture current wrapper settings as a named profile."""
    _validate_profile_name(name)
    effect_map = settings.effect_map()
    if effects is not None:
        _validate_effect_map(effects)
        effect_map = dict(effects)
    return VisualProfile(
        name=name,
        theme_name=settings.theme_name,
        rendering_mode=settings.rendering_mode,
        quality_tier=settings.quality_tier,
        effect_intensity=settings.effect_intensity,
        font_family=settings.font_family,
        font_scale=settings.font_scale,
        font_width=settings.font_width,
        line_spacing=settings.line_spacing,
        reduced_effects=settings.reduced_effects,
        plain_fallback=settings.plain_fallback,
        effects=effect_map,
    )


def builtin_profiles() -> dict[str, VisualProfile]:
    """Return the built-in profile set derived from theme presets."""
    profiles: dict[str, VisualProfile] = {}
    for theme_name in THEME_PRESETS:
        settings = default_settings(theme_name)
        profile = profile_from_settings(theme_name, settings)
        profiles[theme_name] = VisualProfile(**{**asdict(profile), "builtin": True})
    return profiles


def xdg_config_dir() -> Path:
    """Return the XDG config directory for apex-infinite."""
    base = os.environ.get("XDG_CONFIG_HOME") or os.path.expanduser("~/.config")
    return Path(base) / "apex-infinite"


def xdg_state_dir() -> Path:
    """Return the XDG state directory for apex-infinite."""
    base = os.environ.get("XDG_STATE_HOME") or os.path.expanduser("~/.local/state")
    return Path(base) / "apex-infinite"


def default_profile_path() -> Path:
    """Return the default profile storage path."""
    return xdg_config_dir() / PROFILE_FILE_NAME


def default_state_path() -> Path:
    """Return the default runtime window-state path."""
    return xdg_state_dir() / STATE_FILE_NAME


class ProfileStore:
    """Versioned profile persistence with atomic writes and backups."""

    def __init__(self, path: Path | None = None):
        self.path = Path(path) if path is not None else default_profile_path()
        self._builtins = builtin_profiles()
        self._custom: dict[str, VisualProfile] = {}
        self._last_profile = ""
        self.load_error = ""
        self._load()

    @property
    def last_profile(self) -> str:
        """Return the profile selected on last save, if any."""
        return self._last_profile

    def profile_names(self) -> list[str]:
        """Return built-in names first, then custom names sorted."""
        return list(self._builtins) + sorted(self._custom)

    def get(self, name: str) -> VisualProfile:
        """Return one profile by name."""
        if name in self._custom:
            return self._custom[name]
        if name in self._builtins:
            return self._builtins[name]
        raise ProfileStoreError(f"unknown profile: {name}")

    def is_builtin(self, name: str) -> bool:
        """Return whether a name refers to a built-in profile."""
        return name in self._builtins and name not in self._custom

    def save_current(
        self,
        name: str,
        settings: WrapperSettings,
        set_last: bool = True,
        effects: dict[str, bool] | None = None,
    ) -> VisualProfile:
        """Save wrapper settings as a custom profile."""
        _validate_profile_name(name)
        if name in self._builtins:
            raise ProfileStoreError(
                f"profile {name!r} is built-in; choose a different name"
            )
        profile = profile_from_settings(name, settings, effects=effects)
        self._custom[name] = profile
        if set_last:
            self._last_profile = name
        self._persist()
        return profile

    def set_last_profile(self, name: str) -> None:
        """Persist the profile to restore on next launch."""
        self.get(name)
        self._last_profile = name
        self._persist()

    def duplicate(self, source: str, target: str) -> VisualProfile:
        """Copy an existing profile to a new custom name."""
        _validate_profile_name(target)
        if target in self._builtins or target in self._custom:
            raise ProfileStoreError(f"profile {target!r} already exists")
        origin = self.get(source)
        copy = VisualProfile(**{**asdict(origin), "name": target, "builtin": False})
        self._custom[target] = copy
        self._persist()
        return copy

    def rename(self, source: str, target: str) -> VisualProfile:
        """Rename a custom profile."""
        if source not in self._custom:
            raise ProfileStoreError(f"only custom profiles can be renamed: {source}")
        copy = self.duplicate(source, target)
        del self._custom[source]
        if self._last_profile == source:
            self._last_profile = target
        self._persist()
        return copy

    def delete(self, name: str) -> None:
        """Delete a custom profile."""
        if name not in self._custom:
            raise ProfileStoreError(f"only custom profiles can be deleted: {name}")
        del self._custom[name]
        if self._last_profile == name:
            self._last_profile = ""
        self._persist()

    def reset_builtin(self, name: str) -> VisualProfile:
        """Drop any custom override shadowing a built-in profile."""
        if name not in self._builtins:
            raise ProfileStoreError(f"unknown built-in profile: {name}")
        if name in self._custom:
            del self._custom[name]
            self._persist()
        return self._builtins[name]

    def export_profile(self, name: str, path: Path) -> Path:
        """Write one profile as validated JSON."""
        profile = self.get(name)
        payload = json.dumps(
            profile.to_payload(), ensure_ascii=True, sort_keys=True, indent=2
        )
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(payload + "\n", encoding="ascii")
        return target

    def import_profile(self, path: Path, rename_to: str | None = None) -> VisualProfile:
        """Import one profile JSON file after schema validation."""
        source = Path(path)
        try:
            raw = json.loads(source.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ProfileStoreError(f"profile import failed: {exc}") from exc
        profile = _profile_from_payload(raw, rename_to=rename_to)
        if profile.name in self._builtins:
            raise ProfileStoreError(
                f"imported profile name {profile.name!r} shadows a built-in profile"
            )
        self._custom[profile.name] = profile
        self._persist()
        return profile

    def _load(self) -> None:
        if not self.path.exists():
            return
        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
            if not isinstance(raw, dict):
                raise ProfileStoreError("profile file must contain a JSON object")
            version = raw.get("version")
            if version != PROFILE_SCHEMA_VERSION:
                raise ProfileStoreError(
                    f"unsupported profile schema version: {version!r}"
                )
            profiles = raw.get("profiles")
            if not isinstance(profiles, list):
                raise ProfileStoreError("profile file must contain a profiles list")
            for entry in profiles:
                profile = _profile_from_payload(entry)
                if profile.name not in self._builtins:
                    self._custom[profile.name] = profile
            last = raw.get("last_profile")
            if isinstance(last, str) and (
                last in self._custom or last in self._builtins
            ):
                self._last_profile = last
        except (OSError, json.JSONDecodeError, ProfileStoreError) as exc:
            self.load_error = str(exc)
            self._backup_corrupt_file()

    def _backup_corrupt_file(self) -> None:
        try:
            backup = self.path.with_suffix(self.path.suffix + ".corrupt")
            os.replace(self.path, backup)
        except OSError:
            pass

    def _persist(self) -> None:
        payload = {
            "version": PROFILE_SCHEMA_VERSION,
            "last_profile": self._last_profile,
            "profiles": [
                self._custom[name].to_payload() for name in sorted(self._custom)
            ],
        }
        _atomic_write_json(self.path, payload)


def load_window_state(path: Path | None = None) -> dict[str, Any]:
    """Load persisted runtime window state, tolerating corruption."""
    state_path = Path(path) if path is not None else default_state_path()
    if not state_path.exists():
        return {}
    try:
        raw = json.loads(state_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return raw if isinstance(raw, dict) else {}


def save_window_state(state: dict[str, Any], path: Path | None = None) -> Path:
    """Persist runtime window state under XDG state."""
    state_path = Path(path) if path is not None else default_state_path()
    _atomic_write_json(state_path, dict(state))
    return state_path


def _atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, ensure_ascii=True, sort_keys=True, indent=2) + "\n"
    handle, temp_name = tempfile.mkstemp(
        dir=str(path.parent), prefix=path.name, suffix=".tmp"
    )
    try:
        with os.fdopen(handle, "w", encoding="ascii") as stream:
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp_name, path)
    except OSError as exc:
        try:
            os.unlink(temp_name)
        except OSError:
            pass
        raise ProfileStoreError(f"failed to write profile file: {exc}") from exc


def _profile_from_payload(payload: Any, rename_to: str | None = None) -> VisualProfile:
    if not isinstance(payload, dict):
        raise ProfileStoreError("profile entry must be a JSON object")
    version = payload.get("version", PROFILE_SCHEMA_VERSION)
    if version != PROFILE_SCHEMA_VERSION:
        raise ProfileStoreError(f"unsupported profile version: {version!r}")
    _reject_secret_keys(payload)
    name = rename_to if rename_to is not None else payload.get("name")
    if not isinstance(name, str):
        raise ProfileStoreError("profile name must be text")
    _validate_profile_name(name)
    effects = payload.get("effects", {})
    if not isinstance(effects, dict):
        raise ProfileStoreError("profile effects must map known effects to booleans")
    _validate_effect_map(effects)
    try:
        settings = build_settings(
            theme_name=_expect_str(payload, "theme_name"),
            effect_intensity=_expect_int(payload, "effect_intensity"),
            font_family=_expect_str(payload, "font_family"),
            font_scale=_expect_number(payload, "font_scale"),
            reduced_effects=bool(payload.get("reduced_effects", False)),
            plain_fallback=bool(payload.get("plain_fallback", False)),
            rendering_mode=_expect_str(payload, "rendering_mode"),
            quality_tier=_expect_str(payload, "quality_tier"),
            font_width=_expect_number(payload, "font_width"),
            line_spacing=_expect_number(payload, "line_spacing"),
        )
    except WrapperSettingsError as exc:
        raise ProfileStoreError(f"invalid profile values: {exc}") from exc
    profile = profile_from_settings(name, settings)
    if effects:
        profile = VisualProfile(**{**asdict(profile), "effects": dict(effects)})
    return profile


def _validate_effect_map(effects: dict[str, bool]) -> None:
    if not all(
        key in EFFECT_NAMES and isinstance(value, bool)
        for key, value in effects.items()
    ):
        raise ProfileStoreError("profile effects must map known effects to booleans")


def _reject_secret_keys(payload: dict[str, Any]) -> None:
    for key in payload:
        lowered = str(key).lower()
        if any(token in lowered for token in _SECRET_KEY_TOKENS):
            raise ProfileStoreError(f"profile field {key!r} looks secret-like")


def _expect_str(payload: dict[str, Any], key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str):
        raise ProfileStoreError(f"profile field {key!r} must be text")
    return value


def _expect_int(payload: dict[str, Any], key: str) -> int:
    value = payload.get(key)
    if isinstance(value, bool) or not isinstance(value, int):
        raise ProfileStoreError(f"profile field {key!r} must be an integer")
    return value


def _expect_number(payload: dict[str, Any], key: str) -> float:
    value = payload.get(key)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ProfileStoreError(f"profile field {key!r} must be a number")
    return float(value)


def _validate_profile_name(name: str) -> None:
    if not isinstance(name, str) or not name.strip():
        raise ProfileStoreError("profile name must be non-empty text")
    if len(name) > MAX_PROFILE_NAME_LENGTH:
        raise ProfileStoreError("profile name is too long")
    try:
        name.encode("ascii")
    except UnicodeEncodeError as exc:
        raise ProfileStoreError("profile name must be ASCII text") from exc
    if any(ch in name for ch in "/\\\n\r\t"):
        raise ProfileStoreError("profile name must not contain path separators")
