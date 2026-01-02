from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class LicenseSource(ABC):
    kind: str

    @abstractmethod
    def load(self) -> str:
        """Load raw payload for parsing."""

    @property
    def context(self) -> dict[str, Any]:
        return {}
