from __future__ import annotations

from typing import Type

from licenscope.core.errors import ConfigError
from licenscope.parsers.base import Parser


class ParserRegistry:
    def __init__(self) -> None:
        self._parsers: dict[str, Type[Parser]] = {}

    def register(self, parser_cls: Type[Parser]) -> None:
        if not getattr(parser_cls, "name", ""):
            raise ConfigError("Parser is missing a name")
        self._parsers[parser_cls.name] = parser_cls

    def create(self, name: str, **kwargs) -> Parser:
        parser_cls = self._parsers.get(name)
        if parser_cls is None:
            raise ConfigError(f"Unknown parser: {name}")
        return parser_cls(**kwargs)
