# Webhooks

Airtrack sends a `POST` to your endpoint for every new tracking event, and again when a shipment's status changes. Each request is signed, and failed deliveries are retried.

## Register

```bash
curl -X POST https://www.air-cargo.io/api/webhooks/ \
  -H "Authorization: Bearer <api-key>" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://your-server.example/airtrack", "events": []}'
```

The response includes `secret`. It is shown only here, so store it: you need it to check signatures.

You can also create webhooks in the dashboard under **Webhooks**.

## Events

| Event | Sent when |
|-------|-----------|
| `tracking_update` | A new milestone was recorded. One delivery per milestone. |
| `status_change` | The shipment moved to a new status. Sent after the `tracking_update` deliveries that caused it. |
| `shipment.<status>` | A filter: only `status_change` deliveries to that status, e.g. `shipment.delivered` or `shipment.exception`. |

`"events": []` subscribes to everything.

## Payload

```json
{
  "id": "evt_8c1f5e0f3b2a4d0e9a6b7c2d1e0f9a8b",
  "type": "status_change",
  "api_version": "2026-11-17",
  "created_at": "2026-11-17T23:05:12Z",
  "shipment": {
    "id": "3e959642-6876-493f-9045-633bbadb0706",
    "awb": "700-12345675",
    "carrier": { "prefix": "700", "name": "Challenge Airlines IL" },
    "origin": "TLV",
    "destination": "LGG",
    "status": "landed",
    "previous_status": "in_transit",
    "flight_number": "5C851",
    "pieces": 3,
    "weight_kg": 420.5,
    "departure_date": "2026-11-17T19:38:00Z",
    "arrival_date": "2026-11-17T23:00:00Z"
  },
  "event": {
    "id": "4b0d5c7e-2f61-4a8e-9d3b-1c2e3f4a5b6c",
    "status": "landed",
    "iata_code": "ARR",
    "location": "LGG",
    "timestamp": "2026-11-17T23:00:00Z",
    "description": "Arrived — shipment arrived at destination",
    "flight_number": "5C851",
    "pieces": 3,
    "weight_kg": 420.5,
    "source": "carrier"
  }
}
```

- `type` is `tracking_update`, `status_change` or `test`.
- `shipment.previous_status` is the status before this batch of events. It is the same as `status` on a `tracking_update` that didn't change it.
- All times are UTC. Fields Airtrack doesn't know are `null`.
- New fields may be added; ignore ones you don't use.

### Headers

| Header | Value |
|--------|-------|
| `X-Webhook-Signature` | HMAC-SHA256 of the raw body, hex, keyed with your secret |
| `X-Airtrack-Event` | The `type` |
| `X-Airtrack-Delivery` | The payload `id` |
| `X-Airtrack-Attempt` | `1` for the first try, up to `4` |

## Verify the signature

Compute the HMAC over the raw request body, before parsing it:

```python
import hashlib, hmac

def verify(raw_body: bytes, signature: str, secret: str) -> bool:
    expected = hmac.new(secret.encode(), raw_body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)
```

```javascript
import crypto from "node:crypto";

function verify(rawBody, signature, secret) {
  const expected = crypto.createHmac("sha256", secret).update(rawBody).digest("hex");
  return signature.length === expected.length &&
    crypto.timingSafeEqual(Buffer.from(expected), Buffer.from(signature));
}
```

The Python SDK has this as `airtrack.verify_webhook`.

## Retries

Reply with any `2xx` status within 10 seconds. Anything else, or no answer, counts as a failure, and the same body is sent again after 1 minute, 5 minutes and 30 minutes (four attempts in all). Because a delivery can arrive more than once, use the payload `id` to skip duplicates.

In the webhook list, `state` shows how the latest delivery went:

| State | Meaning |
|-------|---------|
| `unused` | Nothing sent yet |
| `ok` | Last delivery succeeded |
| `retrying` | Last delivery failed and will be retried |
| `failing` | Last delivery failed all attempts |

## Send a test

```bash
curl -X POST https://www.air-cargo.io/api/webhooks/<id>/test \
  -H "Authorization: Bearer <api-key>"
```

This sends a signed sample (`"type": "test"`) right away and returns the result. Tests are not retried.

## Manage

```bash
# List, with state and last delivery
curl https://www.air-cargo.io/api/webhooks/ -H "Authorization: Bearer <api-key>"

# Pause, or change the URL or events
curl -X PATCH https://www.air-cargo.io/api/webhooks/<id> \
  -H "Authorization: Bearer <api-key>" -H "Content-Type: application/json" \
  -d '{"active": false}'

# Recent deliveries: status code, attempts, next retry, error
curl "https://www.air-cargo.io/api/webhooks/<id>/logs?limit=20" -H "Authorization: Bearer <api-key>"

# Delete
curl -X DELETE https://www.air-cargo.io/api/webhooks/<id> -H "Authorization: Bearer <api-key>"
```
