# Webhooks

Webhooks allow you to receive real-time notifications when shipment statuses change. Airtrack posts JSON payloads to your endpoint with HMAC signing for verification.

## Register a Webhook

```bash
curl -X POST https://www.air-cargo.io/api/webhooks/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://your-server.com/webhook",
    "events": ["status_change"]
  }'
```

A signing secret is auto-generated and returned in the response. Save it — you'll use it to verify payloads.

## Event Types

| Event | Description |
|-------|-------------|
| `status_change` | Shipment status updated |
| `tracking_update` | New tracking event added |
| `*` (empty array) | All events |

## Verify Payloads

Each webhook request includes a `X-Webhook-Signature` header — an HMAC-SHA256 of the raw body, signed with your webhook secret.

```python
import hashlib, hmac

def verify_webhook(payload: bytes, signature: str, secret: str) -> bool:
    expected = hmac.new(
        secret.encode(), payload, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)
```

## Payload Format

```json
{
  "event": "status_change",
  "shipment_id": "uuid",
  "awb": "235-12345678",
  "old_status": "BOOKED",
  "new_status": "IN_TRANSIT",
  "timestamp": "2025-01-15T12:00:00Z"
}
```

## Retry Policy

Airtrack retries failed deliveries up to 3 times with exponential backoff (1min, 5min, 30min). After all retries fail, the webhook is marked as degraded and visible in the dashboard.

## List Webhooks

```bash
curl https://www.air-cargo.io/api/webhooks/ \
  -H "Authorization: Bearer <token>"
```

## Delivery Logs

```bash
curl https://www.air-cargo.io/api/webhooks/<id>/logs \
  -H "Authorization: Bearer <token>"
```

## Delete a Webhook

```bash
curl -X DELETE https://www.air-cargo.io/api/webhooks/<id> \
  -H "Authorization: Bearer <token>"
```

## Best Practices

1. **Respond quickly** — Return 200 within 5 seconds
2. **Idempotent processing** — Use the event timestamp or shipment_id to deduplicate
3. **Verify signatures** — Always validate the `X-Webhook-Signature` header
4. **Graceful degradation** — If your endpoint fails, Airtrack retries with backoff
