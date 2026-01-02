from __future__ import annotations

from urllib.request import Request, urlopen


class HttpClient:
    def fetch(self, request: Request) -> str:
        with urlopen(request, timeout=30) as response:
            return response.read().decode("utf-8")
