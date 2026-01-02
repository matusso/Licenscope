from __future__ import annotations

from abc import ABC, abstractmethod
from urllib.request import Request


class AuthProvider(ABC):
    name: str

    @abstractmethod
    def apply(self, request: Request) -> Request:
        """Apply auth headers to an outgoing request."""
