from __future__ import annotations

from urllib.request import Request

from licenscope.auth import AUTH_PROVIDERS
from licenscope.core.errors import SourceError
from licenscope.sources.base import LicenseSource
from licenscope.util.http import HttpClient
from licenscope.util.logging import get_logger


class UrlSource(LicenseSource):
    kind = "url"

    def __init__(
        self,
        url: str,
        auth: dict[str, str] | None = None,
        system: str | None = None,
        method: str = "GET",
        headers: dict[str, str] | None = None,
        body: str | bytes | None = None,
    ) -> None:
        self._url = url
        self._auth = auth or {}
        self._system = system
        self._method = method.upper()
        self._headers = headers or {}
        self._body = body
        self._client = HttpClient()
        self._logger = get_logger(self.__class__.__name__)

    def load(self) -> str:
        data = None
        if self._body is not None:
            if self._method == "GET":
                raise SourceError("GET requests cannot have a body")
            data = (
                self._body.encode("utf-8")
                if isinstance(self._body, str)
                else self._body
            )
        request = Request(
            self._url, data=data, method=self._method, headers=self._headers
        )
        auth_type = self._auth.get("type")
        if auth_type:
            provider_cls = AUTH_PROVIDERS.get(auth_type)
            if provider_cls is None:
                raise SourceError(f"Unknown auth provider: {auth_type}")
            provider = provider_cls(
                **{k: v for k, v in self._auth.items() if k != "type"}
            )
            request = provider.apply(request)
        body_len = len(data) if data is not None else 0
        headers_to_log = {
            k: v
            for k, v in request.header_items()
            if k.lower() not in ("authorization", "x-xdr-auth-id")
        }
        self._logger.debug(
            "URL request method={} url={} system={} headers={} body_bytes={}",
            self._method,
            self._url,
            self._system or "unknown",
            headers_to_log,
            body_len,
        )
        return self._client.fetch(request)

    @property
    def context(self) -> dict[str, str]:
        context = {}
        if self._system:
            context["system"] = self._system
        return context
