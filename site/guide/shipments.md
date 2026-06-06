# Shipments

## Create a Shipment

```bash
curl -X POST https://www.air-cargo.io/api/shipments/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"awb": "235-12345678"}'
```

The carrier is auto-detected from the IATA prefix (first 3 digits of the AWB).

## Batch Create

Create multiple shipments at once (up to 50 per request):

```bash
curl -X POST https://www.air-cargo.io/api/shipments/batch \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"awbs": ["235-12345678", "176-87654321", "020-11223344"]}'
```

## List Shipments

```bash
curl "https://www.air-cargo.io/api/shipments/?page=1&limit=20&status=IN_TRANSIT" \
  -H "Authorization: Bearer <token>"
```

**Parameters:**

| Param | Example | Description |
|-------|---------|-------------|
| `page` | `1` | Page number |
| `limit` | `20` | Per page (max 100) |
| `awb` | `235` | Partial AWB search |
| `status` | `BOOKED` | Exact match |
| `carrier_id` | `uuid` | Filter by carrier |
| `origin` | `IST` | Partial origin code |
| `destination` | `JFK` | Partial destination code |
| `sort_by` | `created_at` | Field to sort |
| `sort_order` | `desc` | asc or desc |

**Response:**

```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 150,
    "pages": 8
  }
}
```

## Get a Shipment

```bash
curl "https://www.air-cargo.io/api/shipments/<id>" \
  -H "Authorization: Bearer <token>"
```

## Update a Shipment

```bash
curl -X PATCH https://www.air-cargo.io/api/shipments/<id> \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "origin": "IST",
    "destination": "JFK",
    "pieces": 10,
    "weight_kg": 500.0,
    "flight_number": "TK1234"
  }'
```

## Delete a Shipment

```bash
curl -X DELETE https://www.air-cargo.io/api/shipments/<id> \
  -H "Authorization: Bearer <token>"
```

## Export Shipments

Download filtered results as CSV or JSON:

```bash
curl "https://www.air-cargo.io/api/shipments/export?format=csv" \
  -H "Authorization: Bearer <token>"
```

## Stats & Trends

```bash
# Aggregate stats
curl "https://www.air-cargo.io/api/shipments/stats" \
  -H "Authorization: Bearer <token>"

# Daily creation trends (last 30 days)
curl "https://www.air-cargo.io/api/shipments/trends?days=30" \
  -H "Authorization: Bearer <token>"
```
