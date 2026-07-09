"""Render capability detection and quality tier selection.

Detection is environment-driven and PySide6-free so it can run headlessly
before Qt is imported. The bridge publishes the resolved facts through the
registered ``wrapper_capabilities_resolved`` event payload shape.
"""

from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

from apex_infinite_visual.settings import (
    QUALITY_BALANCED,
    QUALITY_BATTERY,
    QUALITY_CINEMATIC,
    QUALITY_LOW_EFFECTS,
    QUALITY_PLAIN,
    QUALITY_TIERS,
)

BACKEND_HARDWARE = "hardware"
BACKEND_SOFTWARE = "software"

FORCE_TIER_ENV = "APEX_INFINITE_VISUAL_TIER"

_TIER_RANK = {tier: rank for rank, tier in enumerate(QUALITY_TIERS)}

SHADER_MODULE_NAMES = (
    "surface_postprocess",
    "glow_composite",
    "noise_field",
    "chroma_edge",
    "persistence_buffer",
    "signal_distortion",
)


class RenderCapsError(ValueError):
    """Raised when capability overrides are invalid."""


@dataclass(frozen=True)
class RenderCapabilities:  # pylint: disable=too-many-instance-attributes
    """Detected rendering environment facts."""

    platform: str
    backend: str
    offscreen: bool
    shaders_available: bool
    shader_modules: tuple[str, ...]
    recommended_tier: str
    reduced_effects_forced: bool
    forced_tier: str = ""


def default_shader_dir() -> Path:
    """Return the packaged directory for compiled shader artifacts."""
    return Path(__file__).resolve().parent / "shaders" / "compiled"


def available_shader_modules(shader_dir: Path | None = None) -> tuple[str, ...]:
    """Return shader modules with reviewed compiled artifacts present."""
    directory = shader_dir if shader_dir is not None else default_shader_dir()
    if not directory.is_dir():
        return ()
    present = []
    for module in SHADER_MODULE_NAMES:
        if (directory / f"{module}.frag.qsb").is_file():
            present.append(module)
    return tuple(present)


def detect_capabilities(
    env: Mapping[str, str] | None = None,
    shader_dir: Path | None = None,
) -> RenderCapabilities:
    """Detect backend, shader availability, and a recommended tier."""
    environ = dict(env) if env is not None else dict(os.environ)
    platform = environ.get("QT_QPA_PLATFORM", "").strip() or "default"
    offscreen = platform in {"offscreen", "minimal"}
    software = (
        offscreen
        or environ.get("QT_QUICK_BACKEND", "").strip() == "software"
        or environ.get("LIBGL_ALWAYS_SOFTWARE", "").strip() == "1"
    )
    backend = BACKEND_SOFTWARE if software else BACKEND_HARDWARE
    modules = available_shader_modules(shader_dir)
    shaders_available = bool(modules) and backend == BACKEND_HARDWARE

    if offscreen:
        recommended = QUALITY_LOW_EFFECTS
    elif software:
        recommended = QUALITY_BATTERY
    elif shaders_available:
        recommended = QUALITY_CINEMATIC
    else:
        recommended = QUALITY_BALANCED

    forced = environ.get(FORCE_TIER_ENV, "").strip()
    if forced:
        if forced not in QUALITY_TIERS:
            accepted = ", ".join(QUALITY_TIERS)
            raise RenderCapsError(f"{FORCE_TIER_ENV} must be one of: {accepted}")
        recommended = forced

    return RenderCapabilities(
        platform=platform,
        backend=backend,
        offscreen=offscreen,
        shaders_available=shaders_available,
        shader_modules=modules,
        recommended_tier=recommended,
        reduced_effects_forced=recommended in {QUALITY_LOW_EFFECTS, QUALITY_PLAIN},
        forced_tier=forced,
    )


def resolve_quality_tier(requested: str, caps: RenderCapabilities) -> str:
    """Clamp a requested tier to what the environment supports."""
    if requested not in _TIER_RANK:
        accepted = ", ".join(QUALITY_TIERS)
        raise RenderCapsError(f"quality tier must be one of: {accepted}")
    if caps.forced_tier:
        return caps.forced_tier
    if _TIER_RANK[requested] < _TIER_RANK[caps.recommended_tier]:
        return caps.recommended_tier
    return requested


def capabilities_payload(caps: RenderCapabilities) -> dict[str, object]:
    """Return an event-safe payload for wrapper_capabilities_resolved."""
    return {
        "platform": caps.platform,
        "backend": caps.backend,
        "offscreen": caps.offscreen,
        "shaders_available": caps.shaders_available,
        "shader_modules": list(caps.shader_modules),
        "quality_tier": caps.recommended_tier,
        "reduced_effects_forced": caps.reduced_effects_forced,
    }
