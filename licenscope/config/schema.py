from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class LicenseSourceConfig:
    kind: str
    parser: str
    options: dict[str, Any] = field(default_factory=dict)
    parser_options: dict[str, Any] = field(default_factory=dict)
    auth: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class NotificationConfig:
    kind: str
    options: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class AppConfig:
    sources: list[LicenseSourceConfig]
    notifications: list[NotificationConfig]
    default_timezone: str = "UTC"
