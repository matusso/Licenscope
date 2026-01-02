from __future__ import annotations

import tomllib
from pathlib import Path
from typing import Any

from licenscope.config.schema import AppConfig, LicenseSourceConfig, NotificationConfig
from licenscope.core.errors import ConfigError


def _require_list(value: Any, name: str) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        raise ConfigError(f"Expected '{name}' to be a list")
    return value


def load_config(path: str | Path) -> AppConfig:
    config_path = Path(path)
    if not config_path.exists():
        raise ConfigError(f"Config file not found: {config_path}")
    raw = tomllib.loads(config_path.read_text())
    sources_raw = _require_list(raw.get("sources", []), "sources")
    notifications_raw = _require_list(raw.get("notifications", []), "notifications")

    sources = [
        LicenseSourceConfig(
            kind=source.get("kind", ""),
            parser=source.get("parser", ""),
            options=source.get("options", {}),
            parser_options=source.get("parser_options", {}),
            auth=source.get("auth", {}),
        )
        for source in sources_raw
    ]
    notifications = [
        NotificationConfig(
            kind=notification.get("kind", ""),
            options=notification.get("options", {}),
        )
        for notification in notifications_raw
    ]

    return AppConfig(
        sources=sources,
        notifications=notifications,
        default_timezone=raw.get("default_timezone", "UTC"),
    )
