# Slack Integration

Send shipment status updates directly to your Slack channels.

## Setup

1. Create an [Incoming Webhook](https://api.slack.com/messaging/webhooks) in your Slack workspace
2. Copy the webhook URL (`https://hooks.slack.com/services/...`)
3. Configure it via the Airtrack API:

```bash
curl -X PUT https://www.air-cargo.io/api/integrations/slack \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"webhook_url": "https://hooks.slack.com/services/..."}'
```

## Test

```bash
curl -X POST https://www.air-cargo.io/api/integrations/slack/test \
  -H "Authorization: Bearer <token>"
```

## Disable

```bash
curl -X DELETE https://www.air-cargo.io/api/integrations/slack \
  -H "Authorization: Bearer <token>"
```

## Notification Triggers

Slack notifications are automatically sent when:
- A shipment status changes
- A tracking event is created
- An exception is detected

The Slack message includes the AWB number, new status, location, and a link to the shipment dashboard.
