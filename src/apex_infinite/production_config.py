"""Resolve production-launch config and project defaults for the shell wrapper."""

from __future__ import annotations

import argparse
import os
import sys
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

import yaml
from dotenv import load_dotenv

from apex_infinite.config_resolution import (
    ProjectResolutionError,
    resolve_config,
    resolve_project,
)


class ProductionSettingsError(ValueError):
    """Raised when production defaults cannot be resolved safely."""


@dataclass(frozen=True)
class ProductionSettings:
    """Resolved paths needed by the production shell launcher."""

    config_path: str
    project_path: str


def _load_config_mapping(config_path: str) -> Mapping[str, object]:
    """Read the selected YAML and load its dotenv precedence chain."""
    path = Path(config_path)
    try:
        config = yaml.safe_load(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise ProductionSettingsError(f"could not read config: {config_path}") from exc
    except yaml.YAMLError as exc:
        raise ProductionSettingsError(
            f"malformed config file {config_path}: {exc}"
        ) from exc
    if not isinstance(config, Mapping):
        raise ProductionSettingsError(
            f"malformed config file {config_path}: expected a YAML mapping"
        )

    # Match the base CLI: cwd dotenv values load first, and values beside the
    # selected config take precedence over them.
    load_dotenv(Path.cwd() / ".env")
    load_dotenv(path.parent / ".env", override=True)
    return config


def resolve_production_settings(
    explicit_project: str | None = None,
    explicit_config: str | None = None,
) -> ProductionSettings:
    """Resolve one config and noninteractive project for production launch."""
    resolved_config = resolve_config(explicit_config or None)
    if resolved_config is None:
        raise ProductionSettingsError(
            "no config.yaml found; run apex-infinite --setup or set CONFIG"
        )
    if not resolved_config.exists:
        raise ProductionSettingsError(
            f"config not found: {resolved_config.path} "
            "(run apex-infinite --setup or set CONFIG)"
        )

    config = _load_config_mapping(resolved_config.path)
    resolved_project = resolve_project(explicit_project, config, env=os.environ)
    if resolved_project is None:
        raise ProductionSettingsError(
            "project not configured; set APEX_PRODUCTION_PATH=/absolute/path "
            "or PROJECT=/absolute/path, set APEX_INFINITE_DEFAULT_PROJECT in "
            ".env, or set defaults.project in config.yaml"
        )

    for label, value in (
        ("config path", resolved_config.path),
        ("project path", resolved_project.path),
    ):
        if "\n" in value or "\r" in value:
            raise ProductionSettingsError(f"{label} must not contain newlines")

    return ProductionSettings(
        config_path=resolved_config.path,
        project_path=resolved_project.path,
    )


def main(argv: Sequence[str] | None = None) -> int:
    """Print resolved config and project paths on separate lines."""
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--project", default=None)
    parser.add_argument("--config", default=None)
    args = parser.parse_args(argv)
    try:
        settings = resolve_production_settings(args.project, args.config)
    except (ProductionSettingsError, ProjectResolutionError) as exc:
        print(f"Production launch error: {exc}", file=sys.stderr)
        return 2
    print(settings.config_path)
    print(settings.project_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
