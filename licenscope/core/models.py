from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class LicenseRecord:
    system: str
    expires_at: datetime
    meta: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.expires_at.tzinfo is None:
            object.__setattr__(
                self, "expires_at", self.expires_at.replace(tzinfo=timezone.utc)
            )

    @property
    def is_expired(self) -> bool:
        return self.expires_at <= datetime.now(timezone.utc)

    @property
    def days_left(self) -> int:
        delta = self.expires_at - datetime.now(timezone.utc)
        return max(0, delta.days)
