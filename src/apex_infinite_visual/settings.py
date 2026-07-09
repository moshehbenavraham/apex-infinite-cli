"""Validated settings for the optional visual wrapper."""

from __future__ import annotations

import math
from dataclasses import dataclass, replace
from typing import Any

THEME_CRT_GREEN = "crt-green"
THEME_CRT_AMBER = "crt-amber"
THEME_IBM_DOS = "ibm-dos"
THEME_PLAIN = "plain"
THEME_APEX_REACTOR = "apex-reactor"
THEME_OPERATOR_AMBER = "operator-amber"
THEME_BLUEPRINT_DOS = "blueprint-dos"
THEME_WHITEOUT_LAB = "whiteout-lab"
THEME_BLACKBOX = "blackbox"
THEME_INCIDENT_RED = "incident-red"

WRAPPER_THEME_NAMES = (
    THEME_CRT_GREEN,
    THEME_CRT_AMBER,
    THEME_IBM_DOS,
    THEME_PLAIN,
    THEME_APEX_REACTOR,
    THEME_OPERATOR_AMBER,
    THEME_BLUEPRINT_DOS,
    THEME_WHITEOUT_LAB,
    THEME_BLACKBOX,
    THEME_INCIDENT_RED,
)

RENDERING_MODE_MODERN = "modern-crisp"
RENDERING_MODE_SCANLINE = "scanline"
RENDERING_MODE_PIXEL_GRID = "pixel-grid"
RENDERING_MODE_SUBPIXEL = "subpixel"
RENDERING_MODE_CINEMATIC = "cinematic"

RENDERING_MODES = (
    RENDERING_MODE_MODERN,
    RENDERING_MODE_SCANLINE,
    RENDERING_MODE_PIXEL_GRID,
    RENDERING_MODE_SUBPIXEL,
    RENDERING_MODE_CINEMATIC,
)

QUALITY_CINEMATIC = "cinematic"
QUALITY_BALANCED = "balanced"
QUALITY_BATTERY = "battery"
QUALITY_LOW_EFFECTS = "low-effects"
QUALITY_PLAIN = "plain"

QUALITY_TIERS = (
    QUALITY_CINEMATIC,
    QUALITY_BALANCED,
    QUALITY_BATTERY,
    QUALITY_LOW_EFFECTS,
    QUALITY_PLAIN,
)

QUALITY_INTENSITY_CAP = {
    QUALITY_CINEMATIC: 100,
    QUALITY_BALANCED: 85,
    QUALITY_BATTERY: 45,
    QUALITY_LOW_EFFECTS: 20,
    QUALITY_PLAIN: 0,
}

QUALITY_EFFECT_FPS = {
    QUALITY_CINEMATIC: 60,
    QUALITY_BALANCED: 45,
    QUALITY_BATTERY: 24,
    QUALITY_LOW_EFFECTS: 12,
    QUALITY_PLAIN: 0,
}

EFFECT_NAMES = (
    "glow",
    "scanlines",
    "flicker",
    "curvature",
    "bloom",
    "persistence",
    "noise",
    "jitter",
    "sync",
    "chroma",
    "ambient_frame",
)

FONT_FAMILIES = (
    "monospace",
    "DejaVu Sans Mono",
    "Liberation Mono",
    "Noto Sans Mono",
)

EFFECT_INTENSITY_MIN = 0
EFFECT_INTENSITY_MAX = 100
FONT_SCALE_MIN = 0.8
FONT_SCALE_MAX = 1.4
FONT_WIDTH_MIN = 0.8
FONT_WIDTH_MAX = 1.25
LINE_SPACING_MIN = 0.9
LINE_SPACING_MAX = 1.6
DEFAULT_EFFECT_INTENSITY = 45
DEFAULT_FONT_FAMILY = "monospace"
DEFAULT_FONT_SCALE = 1.0
DEFAULT_FONT_WIDTH = 1.0
DEFAULT_LINE_SPACING = 1.0
DEFAULT_QUALITY_TIER = QUALITY_BALANCED


class WrapperSettingsError(ValueError):
    """Raised when visual wrapper settings are invalid."""


@dataclass(frozen=True)
class ThemePreset:  # pylint: disable=too-many-instance-attributes
    """Clean-room visual preset consumed by Python and QML."""

    name: str
    label: str
    background: str
    panel: str
    panel_alt: str
    cell: str
    border: str
    accent: str
    text: str
    muted: str
    warning: str
    error: str
    default_intensity: int
    default_rendering_mode: str = RENDERING_MODE_MODERN


THEME_PRESETS: dict[str, ThemePreset] = {
    THEME_CRT_GREEN: ThemePreset(
        name=THEME_CRT_GREEN,
        label="Green CRT",
        background="#07100d",
        panel="#0b1b17",
        panel_alt="#10231d",
        cell="#111c19",
        border="#263c34",
        accent="#6ee7a8",
        text="#d8ffe7",
        muted="#8dbca2",
        warning="#f2c166",
        error="#ff6f6f",
        default_intensity=45,
        default_rendering_mode=RENDERING_MODE_SCANLINE,
    ),
    THEME_CRT_AMBER: ThemePreset(
        name=THEME_CRT_AMBER,
        label="Amber CRT",
        background="#120e08",
        panel="#1b160d",
        panel_alt="#241b0f",
        cell="#1d180e",
        border="#4a3720",
        accent="#f0a53a",
        text="#ffe2a8",
        muted="#c59a63",
        warning="#f2c166",
        error="#ff746d",
        default_intensity=40,
        default_rendering_mode=RENDERING_MODE_SCANLINE,
    ),
    THEME_IBM_DOS: ThemePreset(
        name=THEME_IBM_DOS,
        label="IBM DOS",
        background="#050914",
        panel="#07152a",
        panel_alt="#0c1f3a",
        cell="#0a172b",
        border="#27496f",
        accent="#62a8ff",
        text="#d9ecff",
        muted="#89a7c5",
        warning="#f2c166",
        error="#ff6f6f",
        default_intensity=30,
        default_rendering_mode=RENDERING_MODE_PIXEL_GRID,
    ),
    THEME_PLAIN: ThemePreset(
        name=THEME_PLAIN,
        label="Plain",
        background="#101419",
        panel="#182029",
        panel_alt="#1e2732",
        cell="#151b22",
        border="#303943",
        accent="#e6edf3",
        text="#e6edf3",
        muted="#8b949e",
        warning="#d8b45f",
        error="#ff6f6f",
        default_intensity=0,
        default_rendering_mode=RENDERING_MODE_MODERN,
    ),
    THEME_APEX_REACTOR: ThemePreset(
        name=THEME_APEX_REACTOR,
        label="Apex Reactor",
        background="#020604",
        panel="#04120b",
        panel_alt="#071a10",
        cell="#05140c",
        border="#14442b",
        accent="#4dffa6",
        text="#e7fff1",
        muted="#6fae8c",
        warning="#ffd166",
        error="#ff4d5e",
        default_intensity=70,
        default_rendering_mode=RENDERING_MODE_CINEMATIC,
    ),
    THEME_OPERATOR_AMBER: ThemePreset(
        name=THEME_OPERATOR_AMBER,
        label="Operator Amber",
        background="#140d02",
        panel="#1e1405",
        panel_alt="#281a08",
        cell="#211605",
        border="#5c4212",
        accent="#ffb52e",
        text="#ffe9c2",
        muted="#cfa168",
        warning="#ffd166",
        error="#ff6a55",
        default_intensity=55,
        default_rendering_mode=RENDERING_MODE_SCANLINE,
    ),
    THEME_BLUEPRINT_DOS: ThemePreset(
        name=THEME_BLUEPRINT_DOS,
        label="Blueprint DOS",
        background="#020817",
        panel="#061226",
        panel_alt="#0a1a33",
        cell="#081527",
        border="#1c4d7a",
        accent="#35d6ff",
        text="#dbf2ff",
        muted="#7fa9c9",
        warning="#ffd166",
        error="#ff5f6d",
        default_intensity=50,
        default_rendering_mode=RENDERING_MODE_PIXEL_GRID,
    ),
    THEME_WHITEOUT_LAB: ThemePreset(
        name=THEME_WHITEOUT_LAB,
        label="Whiteout Lab",
        background="#f4f6f5",
        panel="#ffffff",
        panel_alt="#eef1f0",
        cell="#f8faf9",
        border="#c3cbc7",
        accent="#0a7a4d",
        text="#14201a",
        muted="#5d6b64",
        warning="#a3641a",
        error="#b3222f",
        default_intensity=15,
        default_rendering_mode=RENDERING_MODE_MODERN,
    ),
    THEME_BLACKBOX: ThemePreset(
        name=THEME_BLACKBOX,
        label="Blackbox",
        background="#0a0b0d",
        panel="#101216",
        panel_alt="#14171c",
        cell="#0e1013",
        border="#23272e",
        accent="#9aa4b2",
        text="#dfe4ea",
        muted="#79818c",
        warning="#cfa75a",
        error="#e0606a",
        default_intensity=10,
        default_rendering_mode=RENDERING_MODE_MODERN,
    ),
    THEME_INCIDENT_RED: ThemePreset(
        name=THEME_INCIDENT_RED,
        label="Incident Red",
        background="#120406",
        panel="#1c080b",
        panel_alt="#260a0e",
        cell="#1f090c",
        border="#55151d",
        accent="#ff5964",
        text="#ffe1e4",
        muted="#bd7d84",
        warning="#ffb84d",
        error="#ff2e44",
        default_intensity=60,
        default_rendering_mode=RENDERING_MODE_SCANLINE,
    ),
}


@dataclass(frozen=True)
class WrapperSettings:  # pylint: disable=too-many-instance-attributes
    """Validated visual settings for the wrapper surface."""

    theme_name: str = THEME_CRT_GREEN
    effect_intensity: int = DEFAULT_EFFECT_INTENSITY
    font_family: str = DEFAULT_FONT_FAMILY
    font_scale: float = DEFAULT_FONT_SCALE
    reduced_effects: bool = False
    plain_fallback: bool = False
    rendering_mode: str = RENDERING_MODE_MODERN
    quality_tier: str = DEFAULT_QUALITY_TIER
    font_width: float = DEFAULT_FONT_WIDTH
    line_spacing: float = DEFAULT_LINE_SPACING

    def __post_init__(self) -> None:
        _validate_theme_name(self.theme_name)
        _validate_intensity(self.effect_intensity)
        _validate_font_family(self.font_family)
        _validate_bounded_number(
            "font scale", self.font_scale, FONT_SCALE_MIN, FONT_SCALE_MAX
        )
        _validate_rendering_mode(self.rendering_mode)
        _validate_quality_tier(self.quality_tier)
        _validate_bounded_number(
            "font width", self.font_width, FONT_WIDTH_MIN, FONT_WIDTH_MAX
        )
        _validate_bounded_number(
            "line spacing", self.line_spacing, LINE_SPACING_MIN, LINE_SPACING_MAX
        )

    @property
    def effective_theme_name(self) -> str:
        """Return the preset after applying the plain fallback."""
        if self.plain_fallback or self.theme_name == THEME_PLAIN:
            return THEME_PLAIN
        return self.theme_name

    @property
    def preset(self) -> ThemePreset:
        """Return the effective visual preset."""
        return THEME_PRESETS[self.effective_theme_name]

    @property
    def effective_quality_tier(self) -> str:
        """Return the quality tier after reduced and plain fallbacks."""
        if self.plain_fallback or self.effective_theme_name == THEME_PLAIN:
            return QUALITY_PLAIN
        if self.reduced_effects:
            return QUALITY_LOW_EFFECTS
        return self.quality_tier

    @property
    def effective_rendering_mode(self) -> str:
        """Return the rendering mode after fallbacks."""
        if self.effective_quality_tier in {QUALITY_PLAIN, QUALITY_LOW_EFFECTS}:
            return RENDERING_MODE_MODERN
        return self.rendering_mode

    @property
    def effective_intensity(self) -> int:
        """Return the bounded effect intensity after fallbacks."""
        if self.reduced_effects or self.effective_theme_name == THEME_PLAIN:
            return 0
        return min(self.effect_intensity, QUALITY_INTENSITY_CAP[self.quality_tier])

    @property
    def effects_available(self) -> bool:
        """Return whether optional visual effects may run."""
        return self.effective_intensity > 0

    @property
    def effect_opacity(self) -> float:
        """Return a normalized opacity multiplier for QML effects."""
        return round(self.effective_intensity / EFFECT_INTENSITY_MAX, 2)

    @property
    def effect_fps(self) -> int:
        """Return the frame pacing budget for animated effects."""
        return QUALITY_EFFECT_FPS[self.effective_quality_tier]

    def effect_enabled(  # pylint: disable=too-many-return-statements
        self, name: str
    ) -> bool:
        """Return the default enabled state for an optional effect."""
        if not self.effects_available:
            return False
        intensity = self.effective_intensity
        tier = self.effective_quality_tier
        mode = self.effective_rendering_mode
        rich_tier = tier in {QUALITY_CINEMATIC, QUALITY_BALANCED}
        if name in {"glow", "curvature"}:
            return True
        if name == "scanlines":
            return mode in {RENDERING_MODE_SCANLINE, RENDERING_MODE_CINEMATIC} or (
                mode
                in {
                    RENDERING_MODE_PIXEL_GRID,
                    RENDERING_MODE_SUBPIXEL,
                }
            )
        if name == "flicker":
            return intensity >= 65
        if name in {"bloom", "persistence"}:
            return rich_tier and intensity >= 40
        if name in {"noise", "jitter", "sync", "chroma"}:
            return mode == RENDERING_MODE_CINEMATIC and rich_tier and intensity >= 55
        if name == "ambient_frame":
            return tier == QUALITY_CINEMATIC or intensity >= 50
        return False

    def effect_map(self) -> dict[str, bool]:
        """Return the enabled state of every optional effect."""
        return {name: self.effect_enabled(name) for name in EFFECT_NAMES}

    def updated(self, **changes: Any) -> "WrapperSettings":
        """Return a validated copy with selected fields changed."""
        return replace(self, **changes)

    def color_map(self) -> dict[str, str]:
        """Return QML-facing colors for the effective preset."""
        preset = self.preset
        return {
            "background": preset.background,
            "panel": preset.panel,
            "panel_alt": preset.panel_alt,
            "cell": preset.cell,
            "border": preset.border,
            "accent": preset.accent,
            "text": preset.text,
            "muted": preset.muted,
            "warning": preset.warning,
            "error": preset.error,
        }


def default_settings(theme_name: str = THEME_CRT_GREEN) -> WrapperSettings:
    """Build settings with the selected theme preset defaults."""
    _validate_theme_name(theme_name)
    preset = THEME_PRESETS[theme_name]
    return WrapperSettings(
        theme_name=theme_name,
        effect_intensity=preset.default_intensity,
        rendering_mode=preset.default_rendering_mode,
        plain_fallback=theme_name == THEME_PLAIN,
    )


def build_settings(  # pylint: disable=too-many-arguments
    *,
    theme_name: str = THEME_CRT_GREEN,
    effect_intensity: int | None = None,
    font_family: str = DEFAULT_FONT_FAMILY,
    font_scale: float = DEFAULT_FONT_SCALE,
    reduced_effects: bool = False,
    plain_fallback: bool = False,
    rendering_mode: str | None = None,
    quality_tier: str = DEFAULT_QUALITY_TIER,
    font_width: float = DEFAULT_FONT_WIDTH,
    line_spacing: float = DEFAULT_LINE_SPACING,
) -> WrapperSettings:
    """Build validated settings from CLI or bridge inputs."""
    _validate_theme_name(theme_name)
    preset = THEME_PRESETS[theme_name]
    return WrapperSettings(
        theme_name=theme_name,
        effect_intensity=(
            preset.default_intensity
            if effect_intensity is None
            else int(effect_intensity)
        ),
        font_family=font_family,
        font_scale=float(font_scale),
        reduced_effects=bool(reduced_effects),
        plain_fallback=bool(plain_fallback or theme_name == THEME_PLAIN),
        rendering_mode=(
            preset.default_rendering_mode if rendering_mode is None else rendering_mode
        ),
        quality_tier=quality_tier,
        font_width=float(font_width),
        line_spacing=float(line_spacing),
    )


def _validate_theme_name(value: str) -> None:
    if value not in THEME_PRESETS:
        accepted = ", ".join(WRAPPER_THEME_NAMES)
        raise WrapperSettingsError(f"theme must be one of: {accepted}")


def _validate_rendering_mode(value: str) -> None:
    if value not in RENDERING_MODES:
        accepted = ", ".join(RENDERING_MODES)
        raise WrapperSettingsError(f"rendering mode must be one of: {accepted}")


def _validate_quality_tier(value: str) -> None:
    if value not in QUALITY_TIERS:
        accepted = ", ".join(QUALITY_TIERS)
        raise WrapperSettingsError(f"quality tier must be one of: {accepted}")


def _validate_intensity(value: int) -> None:
    if isinstance(value, bool) or not isinstance(value, int):
        raise WrapperSettingsError("effect intensity must be an integer")
    if value < EFFECT_INTENSITY_MIN or value > EFFECT_INTENSITY_MAX:
        raise WrapperSettingsError("effect intensity must be between 0 and 100")


def _validate_font_family(value: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise WrapperSettingsError("font family must be non-empty text")
    try:
        value.encode("ascii")
    except UnicodeEncodeError as exc:
        raise WrapperSettingsError("font family must be ASCII text") from exc


def _validate_bounded_number(
    label: str, value: float, minimum: float, maximum: float
) -> None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise WrapperSettingsError(f"{label} must be a number")
    if not math.isfinite(float(value)):
        raise WrapperSettingsError(f"{label} must be finite")
    if value < minimum or value > maximum:
        raise WrapperSettingsError(f"{label} must be between {minimum} and {maximum}")
