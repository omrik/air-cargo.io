# Slack

Post every new tracking event for your shipments to a Slack channel.

## Connect

1. Create an [incoming webhook](https://api.slack.com/messaging/webhooks) in Slack and copy its URL (`https://hooks.slack.com/services/…`).
2. Add it in the dashboard under **Integrations**, or with the API:

```bash
curl -X PUT https://www.air-cargo.io/api/integrations/slack \
  -H "Authorization: Bearer <api-key>" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://hooks.slack.com/services/..."}'
```

## Test

```bash
curl -X POST https://www.air-cargo.io/api/integrations/slack/test \
  -H "Authorization: Bearer <api-key>"
```

## Disconnect

```bash
curl -X DELETE https://www.air-cargo.io/api/integrations/slack \
  -H "Authorization: Bearer <api-key>"
```

## What is posted

One message per new tracking event, with the AWB, status, airport, description and time (UTC).
