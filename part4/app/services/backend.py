"""Client wrapper for the Part 3 backend API."""

from __future__ import annotations

import json
from dataclasses import dataclass
from urllib import error, parse, request
from typing import Any


@dataclass
class BackendResponse:
    """Normalized backend response payload."""

    status_code: int
    payload: Any | None = None
    text: str = ""


class BackendClientError(RuntimeError):
    """Raised when the backend request cannot be completed."""


class BackendClient:
    """Minimal HTTP client for the Part 3 REST API."""

    def __init__(self, base_url: str, timeout: float = 10.0) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def request(
        self,
        method: str,
        path: str,
        *,
        token: str | None = None,
        json: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> BackendResponse:
        """Send an HTTP request and normalize the response."""
        url = f"{self.base_url}/{path.lstrip('/')}"
        if params:
            url = f"{url}?{parse.urlencode(params, doseq=True)}"

        headers = {"Accept": "application/json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"

        body: bytes | None = None
        if json is not None:
            headers["Content-Type"] = "application/json"
            body = json_module_dumps(json).encode("utf-8")

        http_request = request.Request(
            url=url,
            data=body,
            headers=headers,
            method=method.upper(),
        )

        try:
            with request.urlopen(http_request, timeout=self.timeout) as response:
                return self._build_response(response.status, response.headers, response.read())
        except error.HTTPError as exc:
            return self._build_response(exc.code, exc.headers, exc.read())
        except error.URLError as exc:
            raise BackendClientError(f"Failed to reach backend at {self.base_url}") from exc

    @staticmethod
    def _build_response(status_code: int, headers, body: bytes) -> BackendResponse:
        payload: Any | None = None
        text = body.decode("utf-8").strip()
        content_type = headers.get("Content-Type", "")
        if body and "application/json" in content_type.lower():
            try:
                payload = json.loads(text)
            except ValueError:
                payload = None

        return BackendResponse(status_code=status_code, payload=payload, text=text)


def json_module_dumps(payload: dict[str, Any]) -> str:
    """Serialize JSON using compact separators."""
    return json.dumps(payload, separators=(",", ":"))


__all__ = ["BackendClient", "BackendClientError", "BackendResponse"]
