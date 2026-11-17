# Zapier

There is no Airtrack app in Zapier yet. Use **Webhooks by Zapier**, which works the same way.

## Set up

1. Create a Zap with the trigger **Webhooks by Zapier → Catch Hook**, and copy its URL.
2. Register it with Airtrack:

```bash
curl -X POST https://www.air-cargo.io/api/webhooks/ \
  -H "Authorization: Bearer <api-key>" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://hooks.zapier.com/hooks/catch/...", "events": ["status_change"]}'
```

3. Send a test with `POST /api/webhooks/{id}/test`, then click **Test trigger** in Zapier to load the fields.
4. Add your action (Gmail, Google Sheets, Slack…) and map fields such as `shipment awb`, `shipment status` and `event location`.

See the [payload](/guide/webhooks#payload) for every field.
