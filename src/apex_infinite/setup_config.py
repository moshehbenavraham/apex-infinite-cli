"""First-run setup support: build and write the shared CLI config.

The module stays free of terminal rendering and provider dependencies so
both the terminal CLI (``apex-infinite --setup``) and the visual wrapper's
graphical first-run flow can share it. Secrets are always referenced
through environment variable placeholders and never written into config.
Writes are atomic, keep a timestamped backup of any existing file, and use
conservative permissions.
"""

from __future__ import annotations

import os
import shlex
import time
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from apex_infinite.config_resolution import (
    SOURCE_CLI_FLAG,
    SOURCE_ENV,
    SOURCE_XDG,
    resolve_config,
    user_config_path,
)

SETUP_PROVIDERS = ("ollama", "openai", "grok")
REASONING_EFFORTS = ("minimal", "low", "medium", "high", "xhigh")
DEFAULT_EXEC_FLAGS = "--dangerously-bypass-approvals-and-sandbox"
DEFAULT_REASONING_EFFORT = "xhigh"

AUTONOMY_WARNING = (
    "Codex exec flags control how much autonomy the agent has. The default "
    "bypasses approval prompts and sandboxing so the workflow can run "
    "unattended; Codex will edit the target project directly. Start with "
    "--dry-run before any live run."
)

# Provider templates keep secrets as environment placeholders. The values
# mirror the packaged defaults in src/apex_infinite/config.yaml.
PROVIDER_TEMPLATES: dict[str, dict[str, str]] = {
    "ollama": {
        "base_url": "http://${OLLAMA_HOST}:${OLLAMA_PORT}/v1",
        "api_key": "${OLLAMA_API_KEY}",
        "model": "${OLLAMA_MODEL}",
    },
    "openai": {
        "base_url": "https://api.openai.com/v1",
        "api_key": "${OPENAI_API_KEY}",
        "model": "gpt-4o",
    },
    "grok": {
        "base_url": "https://api.x.ai/v1",
        "api_key": "${XAI_API_KEY}",
        "model": "grok-4-1-fast-reasoning",
    },
}

PROVIDER_KEY_ENV_VARS = {
    "ollama": "OLLAMA_API_KEY",
    "openai": "OPENAI_API_KEY",
    "grok": "XAI_API_KEY",
}


class SetupError(ValueError):
    """Raised when setup values fail validation."""


@dataclass(frozen=True)
class SetupValues:
    """Operator choices collected by interactive or scripted setup."""

    provider: str = "ollama"
    model: str = ""
    codex_binary: str = "codex"
    exec_flags: str = DEFAULT_EXEC_FLAGS
    model_reasoning_effort: str = DEFAULT_REASONING_EFFORT
    projects_dir: str = ""
    default_project: str = ""


@dataclass(frozen=True)
class SetupWriteResult:
    """Where setup wrote config and any preserved backup."""

    path: Path
    backup_path: Path | None = None
    warnings: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class SetupConfigTarget:
    """Resolved setup write target and the config source it satisfies."""

    path: Path
    source: str


def resolve_setup_config_target(
    explicit_path: str | None = None,
    env=None,
) -> SetupConfigTarget:
    """Return the config path setup should write.

    Explicit ``--config`` and ``APEX_INFINITE_CONFIG`` selections win config
    resolution even when missing, so setup must write those selected paths.
    Otherwise first-run setup creates the shared XDG config.
    """
    resolved = resolve_config(explicit_path or None, env=env)
    if resolved and resolved.source in {SOURCE_CLI_FLAG, SOURCE_ENV}:
        return SetupConfigTarget(path=Path(resolved.path), source=resolved.source)
    return SetupConfigTarget(path=user_config_path(env), source=SOURCE_XDG)


def validate_setup_values(values: SetupValues) -> list[str]:
    """Return operator-facing validation errors for setup values."""
    errors: list[str] = []
    if values.provider not in SETUP_PROVIDERS:
        errors.append(
            f"Unknown provider '{values.provider}'. "
            f"Choose one of: {', '.join(SETUP_PROVIDERS)}."
        )
    if values.model_reasoning_effort not in REASONING_EFFORTS:
        errors.append(
            f"Unsupported reasoning effort '{values.model_reasoning_effort}'. "
            f"Choose one of: {', '.join(REASONING_EFFORTS)}."
        )
    if not values.codex_binary.strip():
        errors.append("Codex binary must not be blank.")
    try:
        shlex.split(values.exec_flags)
    except ValueError as exc:
        errors.append(f"Malformed Codex exec flags: {exc}")
    if not _is_ascii(values.model):
        errors.append("Model name must be ASCII.")
    if values.projects_dir:
        projects_dir = Path(os.path.expanduser(values.projects_dir))
        if not projects_dir.is_dir():
            errors.append(f"Projects directory not found: {values.projects_dir}")
    if values.default_project:
        default_project = Path(os.path.expanduser(values.default_project))
        if not default_project.is_dir():
            errors.append(f"Default project not found: {values.default_project}")
    return errors


def setup_warnings(values: SetupValues, env=None) -> list[str]:
    """Return non-blocking reminders (missing secret env vars)."""
    environ = env if env is not None else os.environ
    warnings: list[str] = []
    if values.provider != "ollama":
        env_var = PROVIDER_KEY_ENV_VARS[values.provider]
        if not environ.get(env_var, "").strip():
            warnings.append(
                f"{env_var} is not set. Export it before a run; the config "
                "only stores the environment reference, never the key."
            )
    return warnings


def build_config_payload(values: SetupValues) -> dict:
    """Build the full shared-config mapping from setup values."""
    errors = validate_setup_values(values)
    if errors:
        raise SetupError("; ".join(errors))
    providers = {name: dict(template) for name, template in PROVIDER_TEMPLATES.items()}
    if values.model.strip():
        providers[values.provider]["model"] = values.model.strip()
    payload: dict = {
        "provider": values.provider,
        "codex": {
            "binary": values.codex_binary.strip(),
            "exec_flags": values.exec_flags,
            "model_reasoning_effort": values.model_reasoning_effort,
        },
        "ui": {
            "theme": "auto",
            "effect_level": "low",
            "ascii": False,
            "compact": False,
            "show_elapsed": True,
            "show_provider": True,
            "themes": {},
        },
        "providers": providers,
    }
    defaults: dict[str, str] = {}
    if values.projects_dir.strip():
        defaults["projects_dir"] = values.projects_dir.strip()
    if values.default_project.strip():
        defaults["project"] = values.default_project.strip()
    if defaults:
        payload["defaults"] = defaults
    return payload


def render_config_yaml(payload: dict) -> str:
    """Render a deterministic ASCII YAML document."""
    return yaml.safe_dump(
        payload,
        default_flow_style=False,
        sort_keys=False,
        allow_unicode=False,
    )


def write_shared_config(
    values: SetupValues,
    path: Path | None = None,
    env=None,
) -> SetupWriteResult:
    """Atomically write the shared config with backup and safe permissions."""
    target = Path(path) if path is not None else user_config_path(env)
    text = render_config_yaml(build_config_payload(values))

    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        target.parent.chmod(0o700)
    except OSError:
        pass

    backup_path: Path | None = None
    if target.exists():
        stamp = time.strftime("%Y%m%d%H%M%S", time.gmtime())
        backup_path = target.with_name(f"{target.name}.bak-{stamp}")
        backup_path.write_bytes(target.read_bytes())
        backup_path.chmod(0o600)

    tmp_path = target.with_name(f".{target.name}.tmp")
    tmp_path.write_text(text, encoding="ascii")
    tmp_path.chmod(0o600)
    os.replace(tmp_path, target)

    return SetupWriteResult(
        path=target,
        backup_path=backup_path,
        warnings=tuple(setup_warnings(values, env=env)),
    )


def _is_ascii(text: str) -> bool:
    try:
        text.encode("ascii")
    except UnicodeEncodeError:
        return False
    return True
