from __future__ import annotations

import re
from typing import Any

from licenscope.core.errors import ParserError
from licenscope.core.models import LicenseRecord
from licenscope.parsers.base import Parser
from licenscope.util.datetime import parse_datetime


class RegexParser(Parser):
    name = "regex"

    def __init__(
        self,
        pattern: str,
        flags: int = 0,
        date_formats: list[str] | None = None,
        timestamp_unit: str = "auto",
    ) -> None:
        if not pattern:
            raise ParserError("Regex pattern is required")
        self._regex = re.compile(pattern, flags)
        self._date_formats = date_formats
        self._timestamp_unit = timestamp_unit

    def parse(self, payload: str, *, context: dict[str, Any]) -> list[LicenseRecord]:
        records = []
        for match in self._regex.finditer(payload):
            groupdict = match.groupdict()
            expires_value = groupdict.get("expires_at")
            if not expires_value:
                raise ParserError("Regex must define an expires_at named group")
            try:
                expires_at = parse_datetime(
                    expires_value,
                    formats=self._date_formats,
                    timezone_name=context.get("default_timezone", "UTC"),
                    timestamp_unit=self._timestamp_unit,
                )
            except ValueError as exc:
                raise ParserError(
                    "expires_at must be a supported datetime format"
                ) from exc
            system = groupdict.get("system", context.get("system", "unknown"))
            meta = {
                key.removeprefix("meta_"): value
                for key, value in groupdict.items()
                if key.startswith("meta_")
            }
            records.append(
                LicenseRecord(system=system, expires_at=expires_at, meta=meta)
            )
        return records
