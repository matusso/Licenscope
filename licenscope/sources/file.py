from __future__ import annotations

from pathlib import Path

from licenscope.core.errors import SourceError
from licenscope.sources.base import LicenseSource


class FileSource(LicenseSource):
    kind = "file"

    def __init__(self, path: str, system: str | None = None) -> None:
        self._path = Path(path)
        self._system = system

    def load(self) -> str:
        if not self._path.exists():
            raise SourceError(f"File not found: {self._path}")
        return self._path.read_text()

    @property
    def context(self) -> dict[str, str]:
        context = {}
        if self._system:
            context["system"] = self._system
        return context
