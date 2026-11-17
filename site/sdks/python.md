# Python SDK

A typed Python client for the Airtrack API, with a helper to verify webhook signatures.

## Install

```bash
pip install "git+https://github.com/omrik/air-cargo.io.git#subdirectory=sdks/python"
```

Requires Python 3.10+. The package is not on PyPI yet.

## Quickstart

```python
from airtrack import Client, ConflictError

client = Client(api_key="your-api-key")

try:
    shipment = client.shipments.create("176-12345675")
except ConflictError as e:
    # already tracked: e.detail holds the existing shipment's id
    shipment = client.shipments.get(e.detail["shipment_id"])

new_events = client.tracking.refresh(shipment.id)   # ask the airline now

for event in client.tracking.get(shipment.id):     # full history
    print(event.timestamp, event.iata_code, event.location, event.description)
```

## Shipments

```python
client.shipments.create("176-12345675", origin="TLV", destination="JFK")
result = client.shipments.create_batch(["176-12345675", "020-12345675"])  # up to 100
result.created, result.skipped, result.invalid

page = client.shipments.list(status="in_transit", limit=50)
for s in page:
    print(s.awb, s.status)
page.pagination.total

client.shipments.get(shipment_id)
client.shipments.update(shipment_id, pieces=10, weight_kg=500.0)
client.shipments.delete(shipment_id)

client.shipments.export("csv")     # bytes; "json" gives a list
client.shipments.stats()           # {"total": …, "by_status": {…}}
client.shipments.trends(days=30)   # [{"date": …, "count": …}]
```

## Tracking

```python
client.tracking.refresh(shipment_id)            # list of new events
client.tracking.get(shipment_id, page=1, limit=50)  # iterate for events; .total for the count
```

## Webhooks

```python
hook = client.webhooks.create("https://your-server.example/airtrack", events=["tracking_update"])
hook.secret                 # store this; it is only returned here

client.webhooks.test(hook.id)                    # sends a signed sample now
client.webhooks.update(hook.id, active=False)    # or url=…, events=[…]
client.webhooks.list()                           # with .state: ok / retrying / failing
client.webhooks.logs(hook.id)
client.webhooks.delete(hook.id)
```

Verify deliveries in your endpoint, using the raw body:

```python
from airtrack import verify_webhook

# Flask example
@app.post("/airtrack")
def airtrack_webhook():
    if not verify_webhook(request.get_data(), request.headers.get("X-Webhook-Signature", ""), SECRET):
        abort(401)
    payload = request.get_json()
    if already_processed(payload["id"]):
        return "", 200
    ...
    return "", 200
```

## Account

```python
client.account.get()          # plan, limits, usage
key = client.account.create_api_key("erp-production")
key.key                       # shown once
client.account.list_api_keys()
client.account.revoke_api_key(key.id)
client.carriers.list()
```

## Errors

| Exception | HTTP |
|-----------|------|
| `UnauthorizedError` | 401 |
| `ForbiddenError` | 403, e.g. plan limit reached |
| `NotFoundError` | 404 |
| `ConflictError` | 409, AWB already tracked; `.detail["shipment_id"]` |
| `ValidationError` | 422 |
| `RateLimitError` | 429 |
| `AirtrackError` | anything else; base class of all of them |

Every error has `.status_code` and `.detail` (the API's full `detail`).

## Options

```python
Client(api_key="…", timeout=30.0)
Client(api_key="…", base_url="https://www.air-cargo.io/api")
Client(api_key="…", http_client=my_httpx_client)   # proxies, custom retries
```
