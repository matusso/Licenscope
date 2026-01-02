from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Iterable
from zoneinfo import ZoneInfo

_ORDINAL_RE = re.compile(r"(\\d{1,2})(st|nd|rd|th)")
_MULTISPACE_RE = re.compile(r"\\s+")

DEFAULT_FORMATS = (
    "%b %d %Y %H:%M:%S",
    "%b %d %Y %H:%M",
    "%B %d %Y %H:%M:%S",
    "%B %d %Y %H:%M",
    "%b %d, %Y %H:%M:%S",
    "%b %d, %Y %H:%M",
    "%B %d, %Y %H:%M:%S",
    "%B %d, %Y %H:%M",
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d",
)


def parse_datetime(
    value: object,
    *,
    formats: Iterable[str] | None = None,
    timezone_name: str | None = "UTC",
    timestamp_unit: str = "auto",
) -> datetime:
    if isinstance(value, datetime):
        dt = value
    elif isinstance(value, (int, float)):
        dt = _from_timestamp(float(value), unit=timestamp_unit)
    elif isinstance(value, str):
        dt = _parse_datetime_str(
            value,
            formats=formats,
            timestamp_unit=timestamp_unit,
        )
    else:
        raise ValueError(f"Unsupported datetime value: {type(value).__name__}")

    if dt.tzinfo is None and timezone_name:
        try:
            tzinfo = ZoneInfo(timezone_name)
        except Exception as exc:  # pragma: no cover - defensive for invalid zones
            raise ValueError(f"Unknown timezone: {timezone_name}") from exc
        dt = dt.replace(tzinfo=tzinfo)
    return dt


def _parse_datetime_str(
    value: str,
    *,
    formats: Iterable[str] | None,
    timestamp_unit: str,
) -> datetime:
    text = _normalize_datetime_text(value)
    if not text:
        raise ValueError("Datetime string is empty")
    if _looks_like_number(text):
        return _from_timestamp(float(text), unit=timestamp_unit)
    try:
        return datetime.fromisoformat(text)
    except ValueError:
        pass

    for fmt in formats or DEFAULT_FORMATS:
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            continue
    raise ValueError(f"Unsupported datetime format: {value}")


def _normalize_datetime_text(value: str) -> str:
    text = value.strip()
    if not text:
        return text
    text = text.replace(",", " ")
    text = _ORDINAL_RE.sub(r"\\1", text)
    text = _MULTISPACE_RE.sub(" ", text)
    return text


def _from_timestamp(value: float, *, unit: str) -> datetime:
    if unit == "auto":
        unit = "milliseconds" if value > 1_000_000_000_000 else "seconds"
    if unit == "milliseconds":
        value /= 1000.0
    elif unit != "seconds":
        raise ValueError(f"Unsupported timestamp unit: {unit}")
    return datetime.fromtimestamp(value, tz=timezone.utc)


def _looks_like_number(text: str) -> bool:
    if text.isdigit():
        return True
    if text.count(".") == 1:
        left, right = text.split(".", 1)
        return left.isdigit() and right.isdigit()
    return False
