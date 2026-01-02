from __future__ import annotations

from typing import Any

from licenscope.config.schema import AppConfig
from licenscope.core.models import LicenseRecord
from licenscope.util.logging import get_logger
from licenscope.parsers.registry import ParserRegistry
from licenscope.sources import create_source
from licenscope.notifications.registry import NotificationRegistry


class LicenseChecker:
    def __init__(
        self,
        parser_registry: ParserRegistry,
        notification_registry: NotificationRegistry,
    ) -> None:
        self._parser_registry = parser_registry
        self._notification_registry = notification_registry
        self._logger = get_logger(self.__class__.__name__)

    def run(self, config: AppConfig) -> list[LicenseRecord]:
        records: list[LicenseRecord] = []
        failures = 0
        for source_config in config.sources:
            try:
                source = create_source(
                    source_config.kind,
                    **source_config.options,
                    auth=source_config.auth,
                )
                parser = self._parser_registry.create(
                    source_config.parser,
                    **source_config.parser_options,
                )
                payload = source.load()
                self._logger.debug("Loaded payload: {}", payload)
                parser_context = {
                    **source.context,
                    "default_timezone": config.default_timezone,
                }
                parsed = parser.parse(payload, context=parser_context)
                records.extend(parsed)
                self._logger.info(
                    "Processed source kind={} parser={} records={}",
                    source_config.kind,
                    source_config.parser,
                    len(parsed),
                )
                for record in parsed:
                    self._logger.info(
                        "Record system={} expires_at={} days_left={} expired={}",
                        record.system,
                        record.expires_at.isoformat(),
                        record.days_left,
                        record.is_expired,
                    )
            except Exception as exc:
                failures += 1
                self._logger.error(
                    "Failed processing source kind={} parser={}: {}",
                    source_config.kind,
                    source_config.parser,
                    exc,
                )

        self._notify(config, records)
        expired = sum(1 for record in records if record.is_expired)
        self._logger.info(
            "Finished processing: total_records={} expired={} failures={}",
            len(records),
            expired,
            failures,
        )
        return records

    def _notify(self, config: AppConfig, records: list[LicenseRecord]) -> None:
        context: dict[str, Any] = {
            "default_timezone": config.default_timezone,
        }
        for notification_config in config.notifications:
            try:
                notifier = self._notification_registry.create(
                    notification_config.kind, **notification_config.options
                )
                notifier.send(records, context=context)
                self._logger.info(
                    "Notification sent kind={} records={}",
                    notification_config.kind,
                    len(records),
                )
            except Exception as exc:
                self._logger.error(
                    "Failed notification kind={}: {}",
                    notification_config.kind,
                    exc,
                )
