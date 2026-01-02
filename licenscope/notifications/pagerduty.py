from __future__ import annotations

from typing import Any

from licenscope.core.models import LicenseRecord
from licenscope.notifications.base import Notifier
from licenscope.util.logging import get_logger


class PagerDutyNotifier(Notifier):
    name = "pagerduty"

    def __init__(self, routing_key: str) -> None:
        self._routing_key = routing_key
        self._logger = get_logger(self.__class__.__name__)

    def send(self, records: list[LicenseRecord], *, context: dict[str, Any]) -> None:
        self._logger.info(
            "PagerDuty would notify records={} routing_key_prefix={}",
            len(records),
            self._routing_key[:4],
        )
