# Zapier Integration

Connect Airtrack to 5,000+ apps via Zapier. *(Coming soon — currently in partner app review.)*

## Planned Triggers

| Trigger | Description |
|---------|-------------|
| **Status Changed** | Fires when a shipment status changes |
| **New Tracking Event** | Fires when a new tracking event is added |
| **Exception Detected** | Fires when a shipment hits an EXCEPTION status |

## Planned Actions

| Action | Description |
|--------|-------------|
| **Create Shipment** | Create a new shipment by AWB |
| **Get Shipment** | Look up a shipment by AWB or ID |
| **List Shipments** | Search shipments by status, carrier, or route |

## Manual Workaround

Until the Zapier app is live, use the **Webhooks by Zapier** trigger with your Airtrack webhook URL:

1. Create a new Zap with **Webhooks by Zapier** → **Catch Hook** trigger
2. Copy the webhook URL
3. Register it with Airtrack:

```bash
curl -X POST https://www.air-cargo.io/api/webhooks/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://hooks.zapier.com/...",
    "events": ["status_change"]
  }'
```

4. Test the webhook by triggering a tracking refresh
5. Map the shipment data to your desired action app (Gmail, Sheets, Slack, etc.)
