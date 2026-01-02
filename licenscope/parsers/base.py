from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from licenscope.core.models import LicenseRecord


class Parser(ABC):
    name: str

    @abstractmethod
    def parse(self, payload: str, *, context: dict[str, Any]) -> list[LicenseRecord]:
        """Parse payload text into license records."""
