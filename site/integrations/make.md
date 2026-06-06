# Make (Integromat) Integration

Connect Airtrack to Make scenarios using webhook modules.

## Setup

1. In Make, create a new scenario and add a **Webhook** module
2. Click **Add** to generate a unique webhook URL
3. Register the URL with Airtrack:

```bash
curl -X POST https://www.air-cargo.io/api/webhooks/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://hook.make.com/your-unique-id",
    "events": ["status_change"]
  }'
```

4. Add modules after the webhook trigger to process the data

## Example Scenario

```
[Webhook] → [Filter: status == "EXCEPTION"]
          → [Email: Send notification to operations team]
          → [Slack: Post message in #alerts channel]
          → [Google Sheets: Log exception row]
```

## Webhook Payload

The webhook sends:

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

Use a **Text parser** module to extract the AWB and status, then map them to your downstream modules.
