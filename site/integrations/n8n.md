# n8n Integration

Connect Airtrack to n8n workflows using webhook nodes.

## Setup

1. In n8n, add a **Webhook** node
2. Set the webhook URL where Airtrack can send events
3. Register the URL with Airtrack:

```bash
curl -X POST https://www.air-cargo.io/api/webhooks/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://your-n8n-instance/webhook/airtrack",
    "events": ["status_change"]
  }'
```

4. Add any node after the Webhook trigger to process the shipment update (send email, update spreadsheet, etc.)

## Example Workflow

```
[Webhook] → [IF status == EXCEPTION] → [Send Email Alert]
                                     → [Slack Message]
                                     → [Update Google Sheet]
```

## AWB Format Check (Function Node)

```javascript
const awb = $json.body.awb;
const pattern = /^\d{3}-\d{8}$/;
if (!pattern.test(awb)) {
  throw new Error(`Invalid AWB: ${awb}`);
}
return { awb, status: $json.body.new_status };
```

## Download

Download the ready-to-import n8n workflow template:

- [airtrack-n8n-workflow.json](/air-cargo.io/integrations/n8n-template.json)
