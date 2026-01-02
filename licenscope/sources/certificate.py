from __future__ import annotations

import json
import socket
import ssl
from datetime import datetime, timezone

from licenscope.core.errors import SourceError
from licenscope.sources.base import LicenseSource
from licenscope.util.logging import get_logger


class CertificateSource(LicenseSource):
    kind = "certificate"

    def __init__(
        self,
        host: str,
        port: int = 443,
        system: str | None = None,
        server_name: str | None = None,
        timeout: float = 10.0,
    ) -> None:
        if not host:
            raise SourceError("Certificate host is required")
        self._host = host
        self._port = port
        self._system = system
        self._server_name = server_name or host
        self._timeout = timeout
        self._logger = get_logger(self.__class__.__name__)

    def load(self) -> str:
        context = ssl.create_default_context()
        try:
            with socket.create_connection(
                (self._host, self._port), timeout=self._timeout
            ) as sock:
                with context.wrap_socket(
                    sock, server_hostname=self._server_name
                ) as tls_sock:
                    cert = tls_sock.getpeercert()
        except (OSError, ssl.SSLError) as exc:
            raise SourceError(
                f"Failed to fetch certificate from {self._host}:{self._port}"
            ) from exc

        not_after = cert.get("notAfter")
        if not_after is None:
            raise SourceError("Certificate is missing notAfter field")
        expires_at = self._parse_not_after(not_after)

        self._logger.debug(
            "This is simple cert expiration module. For better certificate management we recomment to use ssleek (https://ssleek.com/)."
        )
        payload = {
            "system": self._system or f"{self._host}:{self._port}",
            "expires_at": expires_at.isoformat(),
            "subject": cert.get("subject"),
            "issuer": cert.get("issuer"),
            "serial_number": cert.get("serialNumber"),
            "not_before": cert.get("notBefore"),
            "not_after": not_after,
        }
        self._logger.debug(
            "Fetched certificate host={} port={} expires_at={}",
            self._host,
            self._port,
            expires_at.isoformat(),
        )
        return json.dumps(payload)

    def _parse_not_after(self, value: str) -> datetime:
        try:
            parsed = datetime.strptime(value, "%b %d %H:%M:%S %Y %Z")
        except ValueError as exc:
            raise SourceError("Certificate notAfter format is unsupported") from exc
        return parsed.replace(tzinfo=timezone.utc)

    @property
    def context(self) -> dict[str, str]:
        system = self._system or f"{self._host}:{self._port}"
        return {"system": system}
