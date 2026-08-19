from __future__ import annotations

import json
from typing import Any, Mapping, Protocol
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen


class VendorAdapterError(RuntimeError):
    pass


def validate_provider_base_url(base_url: str) -> str:
    """Return a normalized HTTPS base URL suitable for credential-bearing calls."""
    if not isinstance(base_url, str) or not base_url.strip():
        raise ValueError("provider base_url must be a non-empty HTTPS URL")
    normalized = base_url.strip().rstrip("/")
    parsed = urlsplit(normalized)
    if parsed.scheme.lower() != "https":
        raise ValueError("provider base_url must use HTTPS")
    if not parsed.hostname:
        raise ValueError("provider base_url must include a hostname")
    if parsed.username or parsed.password:
        raise ValueError("provider base_url must not contain embedded credentials")
    if parsed.query or parsed.fragment:
        raise ValueError("provider base_url must not contain query parameters or fragments")
    return normalized


class JsonHttpTransport(Protocol):
    def post_json(
        self,
        url: str,
        *,
        headers: Mapping[str, str],
        payload: Mapping[str, Any],
        timeout: float,
    ) -> Mapping[str, Any]: ...


class UrllibJsonTransport:
    """Small dependency-free HTTP transport used by the reference adapters."""

    def post_json(
        self,
        url: str,
        *,
        headers: Mapping[str, str],
        payload: Mapping[str, Any],
        timeout: float,
    ) -> Mapping[str, Any]:
        body = json.dumps(payload).encode("utf-8")
        request = Request(url, data=body, headers=dict(headers), method="POST")
        try:
            with urlopen(request, timeout=timeout) as response:
                data = json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            raise VendorAdapterError(f"provider HTTP error: {exc.code}") from exc
        except URLError as exc:
            raise VendorAdapterError("provider network request failed") from exc
        except json.JSONDecodeError as exc:
            raise VendorAdapterError("provider returned non-JSON HTTP response") from exc

        if not isinstance(data, Mapping):
            raise VendorAdapterError("provider HTTP response must be a JSON object")
        return data
