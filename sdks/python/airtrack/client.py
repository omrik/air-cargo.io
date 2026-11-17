from __future__ import annotations

import hashlib
import hmac
import json
from typing import Any

import httpx

from .errors import (
    AirtrackError,
    ConflictError,
    ForbiddenError,
    NotFoundError,
    RateLimitError,
    UnauthorizedError,
    ValidationError,
)
from .models import (
    ApiKey,
    BatchResult,
    Carrier,
    Shipment,
    ShipmentPage,
    TrackingEvent,
    TrackingPage,
    User,
    Webhook,
    WebhookDelivery,
)

BASE_URL = "https://www.air-cargo.io/api"


def verify_webhook(raw_body: bytes, signature: str, secret: str) -> bool:
    """Check the X-Webhook-Signature header of a delivery. Pass the body bytes exactly as received."""
    expected = hmac.new(secret.encode(), raw_body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature or "")


class _ShipmentsResource:
    def __init__(self, client: "Client"):
        self._client = client

    def create(self, awb: str, **fields) -> Shipment:
        """Start tracking an AWB. Raises ConflictError if you already track it."""
        return Shipment(**self._client._post("/shipments/", json={"awb": awb, **fields}))

    def create_batch(self, awbs: list[str]) -> BatchResult:
        """Up to 100 AWBs. Already-tracked ones are skipped, malformed ones listed as invalid."""
        return BatchResult(**self._client._post("/shipments/batch", json={"awbs": awbs}))

    def list(self, page: int = 1, limit: int = 20, **filters) -> ShipmentPage:
        """Filters: awb, status, carrier_id, origin, destination, sort_by, sort_order."""
        params = {"page": page, "limit": limit, **{k: v for k, v in filters.items() if v is not None}}
        return ShipmentPage(**self._client._get("/shipments/", params=params))

    def get(self, id: str) -> Shipment:
        return Shipment(**self._client._get(f"/shipments/{id}"))

    def update(self, id: str, **fields) -> Shipment:
        return Shipment(**self._client._patch(f"/shipments/{id}", json=fields))

    def delete(self, id: str) -> None:
        self._client._delete(f"/shipments/{id}")

    def export(self, format: str = "csv", **filters) -> bytes | list:
        return self._client._get("/shipments/export", params={"format": format, **filters})

    def stats(self) -> dict:
        return self._client._get("/shipments/stats")

    def trends(self, days: int = 30) -> list[dict]:
        return self._client._get("/shipments/trends", params={"days": days})["trends"]


class _TrackingResource:
    def __init__(self, client: "Client"):
        self._client = client

    def refresh(self, shipment_id: str) -> list[TrackingEvent]:
        """Ask the carrier now. Returns only the events that are new."""
        result = self._client._post("/tracking/", params={"shipment_id": shipment_id})
        return [TrackingEvent(**e) for e in result]

    trigger = refresh  # older name

    def get(self, shipment_id: str, page: int = 1, limit: int = 50) -> TrackingPage:
        result = self._client._get(f"/tracking/{shipment_id}", params={"page": page, "limit": limit})
        return TrackingPage(**result)


class _WebhooksResource:
    def __init__(self, client: "Client"):
        self._client = client

    def create(self, url: str, events: list[str] | None = None) -> Webhook:
        """events: tracking_update, status_change, shipment.<status>; empty for all. Keep the returned secret."""
        return Webhook(**self._client._post("/webhooks/", json={"url": url, "events": events or []}))

    def list(self) -> list[Webhook]:
        return [Webhook(**w) for w in self._client._get("/webhooks/")]

    def update(self, id: str, *, active: bool | None = None, url: str | None = None,
               events: list[str] | None = None) -> Webhook:
        body = {k: v for k, v in {"active": active, "url": url, "events": events}.items() if v is not None}
        return Webhook(**self._client._patch(f"/webhooks/{id}", json=body))

    def delete(self, id: str) -> None:
        self._client._delete(f"/webhooks/{id}")

    def test(self, id: str) -> WebhookDelivery:
        """Send a signed sample delivery to the endpoint now."""
        return WebhookDelivery(**self._client._post(f"/webhooks/{id}/test"))

    def logs(self, id: str, limit: int = 20) -> list[WebhookDelivery]:
        return [WebhookDelivery(**d) for d in self._client._get(f"/webhooks/{id}/logs", params={"limit": limit})]


class _AccountResource:
    def __init__(self, client: "Client"):
        self._client = client

    def get(self) -> User:
        return User(**self._client._get("/account/"))

    def create_api_key(self, name: str = "default") -> ApiKey:
        return ApiKey(**self._client._post("/account/api-keys", json={"name": name}))

    def list_api_keys(self) -> list[ApiKey]:
        return [ApiKey(**k) for k in self._client._get("/account/api-keys")]

    def revoke_api_key(self, id: str) -> None:
        self._client._delete(f"/account/api-keys/{id}")


class _CarriersResource:
    def __init__(self, client: "Client"):
        self._client = client

    def list(self) -> list[Carrier]:
        return [Carrier(**c) for c in self._client._get("/carriers/")]


class Client:
    def __init__(self, api_key: str | None = None, jwt_token: str | None = None, base_url: str = BASE_URL,
                 http_client: httpx.Client | None = None, timeout: float = 30.0):
        self.base_url = base_url.rstrip("/")
        self._token = api_key or jwt_token
        self._client = http_client or httpx.Client(timeout=timeout)

        self.shipments = _ShipmentsResource(self)
        self.tracking = _TrackingResource(self)
        self.webhooks = _WebhooksResource(self)
        self.account = _AccountResource(self)
        self.carriers = _CarriersResource(self)

    def _headers(self) -> dict:
        headers = {"Content-Type": "application/json", "User-Agent": "airtrack-python/0.2.0"}
        if self._token:
            headers["Authorization"] = f"Bearer {self._token}"
        return headers

    def _request(self, method: str, path: str, **kwargs) -> Any:
        response = self._client.request(method, f"{self.base_url}{path}", headers=self._headers(), **kwargs)
        if response.is_success:
            if response.status_code == 204:
                return None
            if "application/json" in response.headers.get("content-type", ""):
                return response.json()
            return response.content
        self._raise(response)

    def _get(self, path: str, **kwargs) -> Any:
        return self._request("GET", path, **kwargs)

    def _post(self, path: str, **kwargs) -> Any:
        return self._request("POST", path, **kwargs)

    def _patch(self, path: str, **kwargs) -> Any:
        return self._request("PATCH", path, **kwargs)

    def _delete(self, path: str, **kwargs) -> Any:
        return self._request("DELETE", path, **kwargs)

    @staticmethod
    def _raise(response: httpx.Response) -> None:
        status = response.status_code
        try:
            detail = response.json().get("detail", response.text)
        except (json.JSONDecodeError, AttributeError):
            detail = response.text
        message = detail.get("message", str(detail)) if isinstance(detail, dict) else str(detail)
        error = {
            401: UnauthorizedError, 403: ForbiddenError, 404: NotFoundError,
            409: ConflictError, 422: ValidationError, 429: RateLimitError,
        }.get(status, AirtrackError)
        raise error(message, status, detail)

    def close(self):
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
