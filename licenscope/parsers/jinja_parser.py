from __future__ import annotations

import json
from typing import Any

from licenscope.core.errors import ParserError
from licenscope.core.models import LicenseRecord
from licenscope.parsers.base import Parser
from licenscope.util.datetime import parse_datetime


class JinjaParser(Parser):
    name = "jinja"

    def __init__(
        self,
        template: str,
        date_formats: list[str] | None = None,
        timestamp_unit: str = "auto",
    ) -> None:
        self._template = template
        self._date_formats = date_formats
        self._timestamp_unit = timestamp_unit

    def parse(self, payload: str, *, context: dict[str, Any]) -> list[LicenseRecord]:
        try:
            from jinja2 import Environment
        except ImportError as exc:
            raise ParserError("jinja2 is required for the jinja parser") from exc

        env = Environment(autoescape=False)
        tmpl = env.from_string(self._template)
        rendered = tmpl.render(payload=payload, **context)
        try:
            data = json.loads(rendered)
        except json.JSONDecodeError as exc:
            raise ParserError("Jinja template must render valid JSON") from exc

        if isinstance(data, dict):
            data = [data]
        if not isinstance(data, list):
            raise ParserError("Jinja output must be a JSON object or list")

        records = []
        for item in data:
            try:
                expires_at = parse_datetime(
                    item["expires_at"],
                    formats=self._date_formats,
                    timezone_name=context.get("default_timezone", "UTC"),
                    timestamp_unit=self._timestamp_unit,
                )
            except (KeyError, ValueError) as exc:
                raise ParserError("Missing or invalid expires_at field") from exc
            records.append(
                LicenseRecord(
                    system=item.get("system", "unknown"),
                    expires_at=expires_at,
                    meta={
                        k: v
                        for k, v in item.items()
                        if k not in {"system", "expires_at"}
                    },
                )
            )
        return records
