import json
from typing import Any

import httpx

from .errors import AirtrackError, NotFoundError, RateLimitError, UnauthorizedError, ValidationError
from .models import (
    ApiKey,
    Carrier,
    PaginatedResponse,
    Plan,
    Shipment,
    SlackConfig,
    Subscription,
    TrackingEvent,
    User,
    Webhook,
    WebhookLog,
)

BASE_URL = "https://www.air-cargo.io/api"


class _ShipmentsResource:
    def __init__(self, client: "Client"):
        self._client = client

    def create(self, awb: str, **kwargs) -> Shipment:
        data = {"awb": awb, **kwargs}
        return Shipment(**self._client._post("/shipments/", json=data))

    def create_batch(self, awbs: list[str]) -> list[Shipment]:
        result = self._client._post("/shipments/batch", json={"awbs": awbs})
        return [Shipment(**s) for s in result.get("created", [])]

    def list(self, page: int = 1, limit: int = 20, **filters) -> PaginatedResponse:
        params = {"page": page, "limit": limit, **{k: v for k, v in filters.items() if v is not None}}
        result = self._client._get("/shipments/", params=params)
        return PaginatedResponse(**result)

    def get(self, id: str) -> Shipment:
        return Shipment(**self._client._get(f"/shipments/{id}"))

    def update(self, id: str, **fields) -> Shipment:
        return Shipment(**self._client._patch(f"/shipments/{id}", json=fields))

    def delete(self, id: str) -> None:
        self._client._delete(f"/shipments/{id}")

    def export(self, format: str = "csv", **filters) -> bytes:
        params = {"format": format, **filters}
        return self._client._request("GET", "/shipments/export", params=params)

    def stats(self) -> dict:
        return self._client._get("/shipments/stats")

    def trends(self, days: int = 30) -> list[dict]:
        return self._client._get("/shipments/trends", params={"days": days})


class _TrackingResource:
    def __init__(self, client: "Client"):
        self._client = client

    def trigger(self, shipment_id: str) -> list[TrackingEvent]:
        result = self._client._post("/tracking/", params={"shipment_id": shipment_id})
        return [TrackingEvent(**e) for e in result]

    def get(self, shipment_id: str) -> list[TrackingEvent]:
        result = self._client._get(f"/tracking/{shipment_id}")
        return [TrackingEvent(**e) for e in result]


class _WebhooksResource:
    def __init__(self, client: "Client"):
        self._client = client

    def create(self, url: str, events: list[str] | None = None) -> Webhook:
        return Webhook(**self._client._post("/webhooks/", json={"url": url, "events": events or []}))

    def list(self) -> list[Webhook]:
        return [Webhook(**w) for w in self._client._get("/webhooks/")]

    def update(self, id: str, active: bool) -> Webhook:
        return Webhook(**self._client._patch(f"/webhooks/{id}", json={"active": active}))

    def delete(self, id: str) -> None:
        self._client._delete(f"/webhooks/{id}")

    def logs(self, id: str, page: int = 1, limit: int = 20) -> list[WebhookLog]:
        result = self._client._get(f"/webhooks/{id}/logs", params={"page": page, "limit": limit})
        return [WebhookLog(**l) for l in result.get("data", [])]


class _AccountResource:
    def __init__(self, client: "Client"):
        self._client = client

    def get(self) -> User:
        return User(**self._client._get("/account/"))

    def update_profile(self, **fields) -> User:
        return User(**self._client._patch("/account/profile", json=fields))

    def change_password(self, current: str, new: str) -> None:
        self._client._post("/account/change-password", json={"current_password": current, "new_password": new})

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


class _BillingResource:
    def __init__(self, client: "Client"):
        self._client = client

    def plans(self) -> list[Plan]:
        return [Plan(**p) for p in self._client._get("/billing/plans")]

    def create_checkout(self, price_id: str, success_url: str, cancel_url: str) -> str:
        result = self._client._post("/billing/create-checkout-session", json={
            "price_id": price_id,
            "success_url": success_url,
            "cancel_url": cancel_url,
        })
        return result["url"]

    def create_portal(self, return_url: str) -> str:
        result = self._client._post("/billing/create-portal-session", json={"return_url": return_url})
        return result["url"]

    def subscription(self) -> Subscription | None:
        result = self._client._get("/billing/subscription")
        return Subscription(**result) if result else None


class _IntegrationsResource:
    def __init__(self, client: "Client"):
        self._client = client

    def slack_status(self) -> SlackConfig:
        return SlackConfig(**self._client._get("/integrations/slack"))

    def slack_set(self, webhook_url: str) -> SlackConfig:
        return SlackConfig(**self._client._put("/integrations/slack", json={"url": webhook_url}))

    def slack_remove(self) -> SlackConfig:
        return SlackConfig(**self._client._delete("/integrations/slack"))

    def slack_test(self) -> bool:
        result = self._client._post("/integrations/slack/test")
        return result["success"]


class Client:
    def __init__(self, api_key: str | None = None, jwt_token: str | None = None, base_url: str = BASE_URL):
        self.base_url = base_url.rstrip("/")
        self._token = api_key or jwt_token
        self._client = httpx.Client(base_url=self.base_url)

        self.shipments = _ShipmentsResource(self)
        self.tracking = _TrackingResource(self)
        self.webhooks = _WebhooksResource(self)
        self.account = _AccountResource(self)
        self.carriers = _CarriersResource(self)
        self.billing = _BillingResource(self)
        self.integrations = _IntegrationsResource(self)

    def _headers(self) -> dict:
        headers = {"Content-Type": "application/json"}
        if self._token:
            headers["Authorization"] = f"Bearer {self._token}"
        return headers

    def _request(self, method: str, path: str, **kwargs) -> Any:
        url = f"{self.base_url}{path}"
        headers = self._headers()
        if "headers" in kwargs:
            headers.update(kwargs.pop("headers"))

        response = self._client.request(method, url, headers=headers, **kwargs)

        if response.is_success:
            if response.status_code == 204:
                return None
            if "application/json" in response.headers.get("content-type", ""):
                return response.json()
            return response.content

        self._handle_error(response)

    def _get(self, path: str, **kwargs) -> Any:
        return self._request("GET", path, **kwargs)

    def _post(self, path: str, **kwargs) -> Any:
        return self._request("POST", path, **kwargs)

    def _put(self, path: str, **kwargs) -> Any:
        return self._request("PUT", path, **kwargs)

    def _patch(self, path: str, **kwargs) -> Any:
        return self._request("PATCH", path, **kwargs)

    def _delete(self, path: str, **kwargs) -> Any:
        return self._request("DELETE", path, **kwargs)

    def _handle_error(self, response: httpx.Response) -> None:
        status = response.status_code
        try:
            body = response.json()
            detail = body.get("detail", response.text)
        except (json.JSONDecodeError, AttributeError):
            detail = response.text

        if status == 401:
            raise UnauthorizedError(detail, status)
        elif status == 404:
            raise NotFoundError(detail, status)
        elif status == 429:
            raise RateLimitError(detail, status)
        elif status == 422:
            raise ValidationError(detail, status)
        else:
            raise AirtrackError(detail, status)

    def health(self) -> dict:
        response = self._client.get(f"{self.base_url}/../health")
        response.raise_for_status()
        return response.json()

    def close(self):
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
