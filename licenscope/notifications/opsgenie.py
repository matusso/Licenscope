from __future__ import annotations

from typing import Any

from licenscope.core.models import LicenseRecord
from licenscope.notifications.base import Notifier
from licenscope.util.logging import get_logger


class OpsgenieNotifier(Notifier):
    name = "opsgenie"

    def __init__(self, api_key: str) -> None:
        self._api_key = api_key
        self._logger = get_logger(self.__class__.__name__)

    def send(self, records: list[LicenseRecord], *, context: dict[str, Any]) -> None:
        self._logger.info(
            "Opsgenie would notify records={} api_key_prefix={}",
            len(records),
            self._api_key[:4],
        )
