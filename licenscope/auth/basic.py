from __future__ import annotations

import base64
from urllib.request import Request

from licenscope.auth.base import AuthProvider


class BasicAuth(AuthProvider):
    name = "basic"

    def __init__(self, username: str, password: str) -> None:
        self._username = username
        self._password = password

    def apply(self, request: Request) -> Request:
        credentials = f"{self._username}:{self._password}".encode("utf-8")
        encoded = base64.b64encode(credentials).decode("ascii")
        request.add_header("Authorization", f"Basic {encoded}")
        return request
