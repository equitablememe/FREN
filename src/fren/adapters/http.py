from __future__ import annotations

import json
from typing import Any, Mapping, Protocol
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class VendorAdapterError(RuntimeError):
    pass


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
