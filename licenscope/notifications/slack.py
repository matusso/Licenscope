from __future__ import annotations

from typing import Any

from licenscope.core.models import LicenseRecord
from licenscope.notifications.base import Notifier
from licenscope.util.logging import get_logger

from slack_sdk.webhook import WebhookClient


class SlackNotifier(Notifier):
    name = "slack"

    def __init__(self, webhook_url: str) -> None:
        self._webhook_url = webhook_url
        self._logger = get_logger(self.__class__.__name__)

    def send(self, records: list[LicenseRecord], *, context: dict[str, Any]) -> None:
        message = f"[Licenscope] notify {len(records)} licenses about to expire"
        self._logger.info("Sending Slack notification records={}", len(records))

        blocks = []
        for record in records:
            blocks.append(
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": (
                            f"*{record.system}* - License expiring on "
                            f"*{record.expires_at.isoformat()}*"
                        ),
                    },
                }
            )

        webhook = WebhookClient(self._webhook_url, timeout=10)
        response = webhook.send(
            text=message,
            blocks=blocks,
        )
        assert response.status_code == 200
        assert response.body == "ok"
        self._logger.info(
            "Slack notification delivered status={}", response.status_code
        )
