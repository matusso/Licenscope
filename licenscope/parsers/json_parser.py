from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from typing import Any

from licenscope.core.errors import ParserError
from licenscope.core.models import LicenseRecord
from licenscope.parsers.base import Parser


_ORDINAL_RE = re.compile(r"(\d+)(st|nd|rd|th)", re.IGNORECASE)


def _strip_ordinals(value: str) -> str:
    return _ORDINAL_RE.sub(r"\1", value)


def _resolve_path(payload: Any, key: str) -> Any:
    path = key.lstrip(".")
    if not path:
        return payload
    current = payload
    for part in path.split("."):
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            raise ParserError(f"Path not found in payload: {key}")
    return current


def _parse_datetime(
    value: Any, date_formats: list[str], timestamp_unit: str
) -> datetime:
    if isinstance(value, (int, float)):
        if timestamp_unit == "milliseconds":
            seconds = float(value) / 1000.0
        elif timestamp_unit == "seconds":
            seconds = float(value)
        else:
            seconds = float(value) / 1000.0 if float(value) > 10**11 else float(value)
        return datetime.fromtimestamp(seconds, tz=timezone.utc)

    if not isinstance(value, str):
        raise ParserError("expires_at must be a string or timestamp")

    cleaned = _strip_ordinals(value)
    if date_formats:
        for fmt in date_formats:
            try:
                parsed = datetime.strptime(cleaned, fmt)
                if parsed.tzinfo is None:
                    return parsed.replace(tzinfo=timezone.utc)
                return parsed
            except ValueError:
                continue
        raise ParserError("No matching date format")

    try:
        parsed = datetime.fromisoformat(cleaned)
    except ValueError as exc:
        raise ParserError(
            "expires_at must be ISO format or match date_formats"
        ) from exc

    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


class JsonParser(Parser):
    name = "json"

    def __init__(
        self,
        key: str,
        date_formats: list[str] | None = None,
        timestamp_unit: str = "auto",
    ) -> None:
        self._key = key
        self._date_formats = date_formats or []
        self._timestamp_unit = timestamp_unit

    def parse(self, payload: str, *, context: dict[str, Any]) -> list[LicenseRecord]:
        try:
            data = json.loads(payload)
        except json.JSONDecodeError as exc:
            raise ParserError("Payload is not valid JSON") from exc

        resolved = _resolve_path(data, self._key)
        items = resolved if isinstance(resolved, list) else [resolved]

        records: list[LicenseRecord] = []
        for item in items:
            if isinstance(item, dict):
                expires_value = item.get("expires_at")
                if expires_value is None:
                    raise ParserError("Missing expires_at field in JSON object")
                system = item.get("system", context.get("system", "unknown"))
                meta = {
                    k: v for k, v in item.items() if k not in {"system", "expires_at"}
                }
            else:
                expires_value = item
                system = context.get("system", "unknown")
                meta = {}

            expires_at = _parse_datetime(
                expires_value, self._date_formats, self._timestamp_unit
            )
            records.append(
                LicenseRecord(system=system, expires_at=expires_at, meta=meta)
            )

        return records
