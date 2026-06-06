# Tracking

## Trigger a Tracking Refresh

Request Airtrack to scrape the carrier's tracking page for live updates:

```bash
curl -X POST "https://www.air-cargo.io/api/tracking/?shipment_id=<shipment-uuid>" \
  -H "Authorization: Bearer <token>"
```

This triggers the carrier adapter to visit the airline's public tracking page, parse the response, and create new tracking events. If the status changed, registered webhooks are fired.

## Get Tracking Events

Retrieve the full tracking history for a shipment:

```bash
curl "https://www.air-cargo.io/api/tracking/<shipment-uuid>" \
  -H "Authorization: Bearer <token>"
```

**Response:**

```json
[
  {
    "id": "uuid",
    "shipment_id": "uuid",
    "status": "BOOKED",
    "location": "IST",
    "timestamp": "2025-01-15T08:00:00Z",
    "description": "Shipment booked",
    "source": "carrier",
    "created_at": "2025-01-15T08:00:01Z"
  },
  {
    "id": "uuid",
    "shipment_id": "uuid",
    "status": "ACCEPTED",
    "location": "IST",
    "timestamp": "2025-01-15T10:00:00Z",
    "description": "Shipment accepted at origin warehouse",
    "source": "carrier",
    "created_at": "2025-01-15T10:00:02Z"
  }
]
```

## Available Statuses

| Status | Meaning |
|--------|---------|
| `BOOKED` | Shipment booked in carrier system |
| `ACCEPTED` | Cargo accepted at origin |
| `IN_TRANSIT` | En route to destination |
| `LANDED` | Arrived at destination airport |
| `DELIVERED` | Delivered to consignee |
| `EXCEPTION` | Delay, damage, or other issue |

## Webhook Integration

After triggering tracking, you can subscribe to status changes via webhooks. See the [Webhooks guide](/guide/webhooks) for details.
