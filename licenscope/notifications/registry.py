from __future__ import annotations

from typing import Type

from licenscope.core.errors import ConfigError
from licenscope.notifications.base import Notifier


class NotificationRegistry:
    def __init__(self) -> None:
        self._notifiers: dict[str, Type[Notifier]] = {}

    def register(self, notifier_cls: Type[Notifier]) -> None:
        if not getattr(notifier_cls, "name", ""):
            raise ConfigError("Notifier is missing a name")
        self._notifiers[notifier_cls.name] = notifier_cls

    def create(self, name: str, **kwargs) -> Notifier:
        notifier_cls = self._notifiers.get(name)
        if notifier_cls is None:
            raise ConfigError(f"Unknown notifier: {name}")
        return notifier_cls(**kwargs)
