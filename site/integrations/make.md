# Make

Start a Make scenario whenever a shipment changes.

## Set up

1. In Make, create a scenario that starts with **Webhooks → Custom webhook**, and copy its URL.
2. Register it with Airtrack:

```bash
curl -X POST https://www.air-cargo.io/api/webhooks/ \
  -H "Authorization: Bearer <api-key>" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://hook.eu1.make.com/your-id", "events": ["status_change"]}'
```

3. Click **Redetermine data structure** in Make, then send a test: `POST /api/webhooks/{id}/test`. Make learns the fields from it.

## Example

```
[Custom webhook] → [Filter: shipment.status = exception]
                 → [Email the operations team]
                 → [Add a row to Google Sheets]
```

Useful fields: `shipment.awb`, `shipment.status`, `shipment.previous_status`, `event.iata_code`, `event.location`, `event.timestamp`. See the [payload](/guide/webhooks#payload).
