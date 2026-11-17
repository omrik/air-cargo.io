# Quickstart

Track your first air waybill in five minutes.

## 1. Get an API key

[Sign up](https://www.air-cargo.io/register), confirm your email, then open **API Keys** in the dashboard and create a key. It is shown once, so store it safely.

All examples use the base URL `https://www.air-cargo.io/api` and the header `Authorization: Bearer <api-key>`.

## 2. Add a shipment

```bash
curl -X POST https://www.air-cargo.io/api/shipments/ \
  -H "Authorization: Bearer $AIRTRACK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"awb": "176-12345675"}'
```

An AWB is 11 digits: a 3-digit airline prefix and an 8-digit serial. Dashes and spaces are accepted and the AWB is stored as `176-12345675`. The airline is detected from the prefix.

**Response** `201 Created` (shortened):

```json
{
  "id": "3e959642-6876-493f-9045-633bbadb0706",
  "awb": "176-12345675",
  "carrier_id": "5e2a777f-f34f-4bd4-ba49-e1d9ac7ead2d",
  "status": "booked",
  "origin": "",
  "destination": "",
  "tracking_events": [],
  "created_at": "2026-11-17T20:40:39.599642"
}
```

Adding an AWB you already track returns `409 Conflict` with the existing shipment's id.

## 3. Get tracking

Airtrack checks the airline on a schedule (see [update timing](/guide/tracking#update-timing)). To ask right away:

```bash
curl -X POST "https://www.air-cargo.io/api/tracking/?shipment_id=<shipment-id>" \
  -H "Authorization: Bearer $AIRTRACK_API_KEY"
```

This returns only the events that are new. To read the full history:

```bash
curl "https://www.air-cargo.io/api/tracking/<shipment-id>" \
  -H "Authorization: Bearer $AIRTRACK_API_KEY"
```

```json
{
  "events": [
    {
      "id": "058a5507-f675-4f15-aa15-a1114b5b6e01",
      "status": "in_transit",
      "iata_code": "DEP",
      "location": "DXB",
      "timestamp": "2026-11-17T19:38:00Z",
      "description": "Departed — flight has departed",
      "flight_number": "EK9881",
      "source": "carrier"
    }
  ],
  "total": 1,
  "page": 1,
  "limit": 50
}
```

## 4. Get pushed updates

Rather than polling, register a [webhook](/guide/webhooks) and Airtrack will POST each new milestone to you.

## Next steps

- [Tracking](/guide/tracking): statuses, IATA codes and update timing
- [Webhooks](/guide/webhooks): payload, signatures and retries
- [API reference](/api/openapi)
- [Python SDK](/sdks/python)
