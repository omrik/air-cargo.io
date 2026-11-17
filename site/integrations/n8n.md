# n8n

Run an n8n workflow whenever a shipment changes.

## Set up

1. In n8n, add a **Webhook** node with method `POST`, and copy its production URL.
2. Register it with Airtrack, choosing the events you want:

```bash
curl -X POST https://www.air-cargo.io/api/webhooks/ \
  -H "Authorization: Bearer <api-key>" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://your-n8n.example/webhook/airtrack", "events": ["shipment.exception", "shipment.delivered"]}'
```

3. Send a test with `POST /api/webhooks/{id}/test` and use it to map fields in the next nodes.

The fields are under `$json.body`, for example `$json.body.shipment.awb`, `$json.body.shipment.status`, `$json.body.event.iata_code` and `$json.body.event.location`. See the [payload](/guide/webhooks#payload).

## Example

```
[Webhook] → [IF shipment.status = exception] → [Send email to operations]
                                             → [Post to Slack]
```

## Template

Import [airtrack-n8n-workflow.json](/integrations/n8n-template.json): a webhook node, an exception check and an email alert. Set your SMTP credentials and recipient after importing.

For signature checks in n8n, compute the HMAC-SHA256 of the raw body in a **Crypto** node and compare it with the `X-Webhook-Signature` header.
