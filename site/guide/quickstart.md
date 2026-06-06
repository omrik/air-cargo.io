# Quickstart

Track your first air cargo shipment in 5 minutes.

## 1. Get an API Key

[Sign up](https://www.air-cargo.io/register) for a free account. Navigate to **API Keys** and generate a new key. Save it — you'll only see it once.

## 2. Create a Shipment

Create a shipment by AWB number:

```bash
curl -X POST https://www.air-cargo.io/api/shipments/ \
  -H "Authorization: Bearer <your-api-key>" \
  -H "Content-Type: application/json" \
  -d '{"awb": "235-12345678"}'
```

The carrier is auto-detected from the AWB prefix (first 3 digits).

**Response:**
```json
{
  "id": "uuid-here",
  "awb": "235-12345678",
  "carrier_id": "uuid",
  "carrier_name": "Turkish Cargo",
  "status": "BOOKED",
  "origin": null,
  "destination": null,
  "created_at": "2025-01-15T10:30:00Z"
}
```

## 3. Trigger Tracking

Request a live tracking refresh:

```bash
curl -X POST "https://www.air-cargo.io/api/tracking/?shipment_id=<shipment-id>" \
  -H "Authorization: Bearer <your-api-key>"
```

Airtrack will scrape the carrier's tracking page and return any new events.

## 4. View Tracking Events

Get the full tracking history:

```bash
curl "https://www.air-cargo.io/api/tracking/<shipment-id>" \
  -H "Authorization: Bearer <your-api-key>"
```

**Response:**
```json
[
  {
    "status": "BOOKED",
    "location": "IST",
    "timestamp": "2025-01-15T08:00:00Z",
    "description": "Shipment booked",
    "source": "carrier"
  }
]
```

## Next Steps

- Read the [Authentication guide](/guide/authentication) for JWT and API key details
- Browse the full [API reference](/api/openapi)
- Try the [Python SDK](/sdks/python) for programmatic access
- Set up [webhooks](/guide/webhooks) for real-time updates
