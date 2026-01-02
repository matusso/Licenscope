from __future__ import annotations

from urllib.request import Request

from licenscope.auth.base import AuthProvider


class TokenAuth(AuthProvider):
    name = "token"

    def __init__(self, token: str, scheme: str = "Bearer") -> None:
        self._token = token
        self._scheme = scheme

    def apply(self, request: Request) -> Request:
        request.add_header("Authorization", f"{self._scheme} {self._token}")
        return request
