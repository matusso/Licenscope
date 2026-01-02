from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from licenscope.core.models import LicenseRecord


class Notifier(ABC):
    name: str

    @abstractmethod
    def send(self, records: list[LicenseRecord], *, context: dict[str, Any]) -> None:
        """Send notifications for license records."""
