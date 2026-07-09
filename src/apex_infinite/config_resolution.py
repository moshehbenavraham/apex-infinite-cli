"""Shared config-file resolution for the CLI, setup, doctor, and wrapper.

This module is intentionally dependency-free (standard library only) so the
optional visual wrapper can import it without pulling terminal rendering or
provider dependencies. The precedence chain is a release contract:

1. Explicit ``--config`` flag value.
2. ``APEX_INFINITE_CONFIG`` environment variable.
3. XDG user config: ``${XDG_CONFIG_HOME:-~/.config}/apex-infinite/config.yaml``.
4. Local ``./config.yaml`` in the working directory.
5. Source-root ``config.yaml`` for checkout development.
6. Packaged defaults shipped inside ``apex_infinite``.

Explicit flag and environment selections are returned even when the file is
missing so config loading fails fast with a clear operator-facing error
instead of silently falling through to another file.
"""

from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

CONFIG_ENV_VAR = "APEX_INFINITE_CONFIG"
CONFIG_DIR_NAME = "apex-infinite"
CONFIG_FILE_NAME = "config.yaml"

SOURCE_CLI_FLAG = "cli-flag"
SOURCE_ENV = "env"
SOURCE_XDG = "xdg"
SOURCE_CWD = "cwd"
SOURCE_SOURCE_ROOT = "source-root"
SOURCE_PACKAGED = "packaged"

SOURCE_CATEGORIES = (
    SOURCE_CLI_FLAG,
    SOURCE_ENV,
    SOURCE_XDG,
    SOURCE_CWD,
    SOURCE_SOURCE_ROOT,
    SOURCE_PACKAGED,
)

# Sources that mean the operator has real user-owned configuration. The
# packaged default keeps the CLI usable but still counts as "first run" for
# setup and first-run detection.
USER_OWNED_SOURCES = frozenset(
    {SOURCE_CLI_FLAG, SOURCE_ENV, SOURCE_XDG, SOURCE_CWD, SOURCE_SOURCE_ROOT}
)


@dataclass(frozen=True)
class ResolvedConfig:
    """One resolved config path and the precedence category that chose it."""

    path: str
    source: str

    @property
    def exists(self) -> bool:
        """Return whether the resolved file currently exists."""
        return Path(self.path).is_file()


def xdg_config_home(env: Mapping[str, str] | None = None) -> Path:
    """Return the XDG config base honoring ``XDG_CONFIG_HOME`` when set."""
    environ = env if env is not None else os.environ
    base = environ.get("XDG_CONFIG_HOME", "").strip()
    if base:
        return Path(base).expanduser()
    return Path.home() / ".config"


def user_config_path(env: Mapping[str, str] | None = None) -> Path:
    """Return the XDG shared CLI config path."""
    return xdg_config_home(env) / CONFIG_DIR_NAME / CONFIG_FILE_NAME


def packaged_config_path() -> Path:
    """Return the packaged default config shipped inside the base package."""
    return Path(__file__).resolve().parent / CONFIG_FILE_NAME


def source_root_config_path() -> Path | None:
    """Return the checkout-root config when running from a source tree."""
    source_root = Path(__file__).resolve().parents[2]
    if (source_root / "pyproject.toml").exists():
        return source_root / CONFIG_FILE_NAME
    return None


def resolve_config(
    explicit_path: str | None = None,
    env: Mapping[str, str] | None = None,
    cwd: Path | None = None,
) -> ResolvedConfig | None:
    """Resolve the active config file through the shared precedence chain."""
    environ = env if env is not None else os.environ
    working_dir = cwd if cwd is not None else Path.cwd()

    if explicit_path:
        return ResolvedConfig(
            path=str(Path(explicit_path).expanduser()), source=SOURCE_CLI_FLAG
        )

    env_path = environ.get(CONFIG_ENV_VAR, "").strip()
    if env_path:
        return ResolvedConfig(path=str(Path(env_path).expanduser()), source=SOURCE_ENV)

    candidates = (
        (user_config_path(environ), SOURCE_XDG),
        (working_dir / CONFIG_FILE_NAME, SOURCE_CWD),
        (source_root_config_path(), SOURCE_SOURCE_ROOT),
        (packaged_config_path(), SOURCE_PACKAGED),
    )
    for candidate, source in candidates:
        if candidate is not None and candidate.is_file():
            return ResolvedConfig(path=str(candidate), source=source)
    return None


def first_run_needed(
    explicit_path: str | None = None,
    env: Mapping[str, str] | None = None,
    cwd: Path | None = None,
) -> bool:
    """Return whether no user-owned shared config exists yet."""
    resolved = resolve_config(explicit_path, env=env, cwd=cwd)
    if resolved is None:
        return True
    if resolved.source not in USER_OWNED_SOURCES:
        return True
    return not resolved.exists
