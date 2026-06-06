# Python SDK

The official Python SDK for the air-cargo.io API. Works with Python 3.10+.

## Installation

```bash
pip install airack
```

## Quickstart

```python
from airack import Client

client = Client(api_key="your-api-key")

# Create a shipment
shipment = client.shipments.create("235-12345678")
print(shipment.awb, shipment.status)

# List shipments
shipments = client.shipments.list(status="IN_TRANSIT", limit=50)
for s in shipments.data:
    print(s.awb, s.status)

# Get tracking events
events = client.tracking.get(shipment.id)
for e in events:
    print(e.status, e.location, e.timestamp)

# Register a webhook
webhook = client.webhooks.create(
    url="https://my-server.com/webhook",
    events=["status_change"]
)
print(f"Signing secret: {webhook.secret}")
```

## API Reference

### Client

```python
client = Client(api_key="your-api-key")
# or
client = Client(jwt_token="your-jwt-token")
```

### Shipments

```python
client.shipments.create(awb: str) -> Shipment
client.shipments.create_batch(awbs: list[str]) -> list[Shipment]
client.shipments.list(page=1, limit=20, status=None, carrier_id=None,
                      awb=None, origin=None, destination=None,
                      sort_by="created_at", sort_order="desc") -> PaginatedResponse[Shipment]
client.shipments.get(id: str) -> Shipment
client.shipments.update(id: str, **fields) -> Shipment
client.shipments.delete(id: str) -> None
client.shipments.export(format="csv", **filters) -> bytes
client.shipments.stats() -> dict
client.shipments.trends(days=30) -> list[dict]
```

### Tracking

```python
client.tracking.trigger(shipment_id: str) -> list[TrackingEvent]
client.tracking.get(shipment_id: str) -> list[TrackingEvent]
```

### Webhooks

```python
client.webhooks.create(url: str, events: list[str] = None) -> Webhook
client.webhooks.list() -> list[Webhook]
client.webhooks.delete(id: str) -> None
client.webhooks.logs(id: str, page=1, limit=20) -> PaginatedResponse[WebhookLog]
```

### Account

```python
client.account.get() -> User
client.account.update_profile(name=None, email=None) -> User
client.account.change_password(current: str, new: str) -> None
client.account.create_api_key(name: str) -> ApiKey
client.account.list_api_keys() -> list[ApiKey]
client.account.revoke_api_key(id: str) -> None
```

### Carriers

```python
client.carriers.list() -> list[Carrier]
```

### Billing

```python
client.billing.plans() -> list[Plan]
client.billing.create_checkout(plan_id: str) -> str  # returns checkout URL
client.billing.create_portal() -> str  # returns portal URL
client.billing.subscription() -> Subscription
```

### Integrations

```python
client.integrations.slack_status() -> SlackConfig
client.integrations.slack_set(webhook_url: str) -> SlackConfig
client.integrations.slack_remove() -> None
client.integrations.slack_test() -> None
```

## Error Handling

```python
from airack import AirtrackError, RateLimitError, NotFoundError

try:
    client.shipments.get("invalid-id")
except NotFoundError:
    print("Shipment not found")
except RateLimitError:
    print("Rate limited — wait and retry")
except AirtrackError as e:
    print(f"API error: {e}")
```
