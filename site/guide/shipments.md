# Shipments

A shipment is one air waybill (AWB) you track.

## Create

```bash
curl -X POST https://www.air-cargo.io/api/shipments/ \
  -H "Authorization: Bearer <api-key>" \
  -H "Content-Type: application/json" \
  -d '{"awb": "176-12345675"}'
```

- The AWB must be 11 digits (3-digit prefix + 8-digit serial). `17612345675`, `176-12345675` and `176 12345675` are all stored as `176-12345675`. Anything else returns `422`.
- The airline is detected from the prefix.
- Optional fields you can send: `origin`, `destination`, `pieces`, `weight_kg`, `volume_cbm`, `flight_number`, `departure_date`, `arrival_date`. Airtrack fills these from the airline when it can.
- If you already track the AWB: `409 Conflict`, with `detail.shipment_id` pointing to the existing shipment.
- If your plan's shipment limit is reached: `403 Forbidden`.

## Create many

Up to 100 AWBs per request:

```bash
curl -X POST https://www.air-cargo.io/api/shipments/batch \
  -H "Authorization: Bearer <api-key>" \
  -H "Content-Type: application/json" \
  -d '{"awbs": ["176-12345675", "020-12345675", "not-an-awb"]}'
```

```json
{
  "created": [{ "id": "…", "awb": "020-12345675", "status": "booked" }],
  "skipped": ["176-12345675"],
  "invalid": ["not-an-awb"],
  "total_created": 1,
  "total_skipped": 1
}
```

`skipped` are AWBs you already track; `invalid` are entries that are not AWBs.

## List

```bash
curl "https://www.air-cargo.io/api/shipments/?page=1&limit=20&status=in_transit" \
  -H "Authorization: Bearer <api-key>"
```

| Parameter | Example | Meaning |
|-----------|---------|---------|
| `page` | `1` | Page number |
| `limit` | `20` | Per page, up to 100 |
| `awb` | `176` | Part of the AWB |
| `status` | `in_transit` | One of the [statuses](/guide/tracking#statuses) |
| `carrier_id` | `uuid` | From `GET /api/carriers/` |
| `origin` / `destination` | `TLV` | Airport code |
| `sort_by` | `created_at` | `awb`, `status`, `origin`, `destination` or `created_at` |
| `sort_order` | `desc` | `asc` or `desc` |

```json
{
  "data": [ { "id": "…", "awb": "176-12345675", "status": "in_transit" } ],
  "pagination": { "page": 1, "per_page": 20, "total": 150, "pages": 8 }
}
```

## Get one

`GET /api/shipments/{id}` returns the shipment with its `tracking_events`.

## Update

```bash
curl -X PATCH https://www.air-cargo.io/api/shipments/<id> \
  -H "Authorization: Bearer <api-key>" \
  -H "Content-Type: application/json" \
  -d '{"origin": "IST", "destination": "JFK", "pieces": 10, "weight_kg": 500.0}'
```

## Delete

`DELETE /api/shipments/{id}` stops tracking and removes the shipment and its events. Returns `204`.

## Export, stats, trends

```bash
curl "https://www.air-cargo.io/api/shipments/export?format=csv" -H "Authorization: Bearer <api-key>"   # or format=json
curl "https://www.air-cargo.io/api/shipments/stats" -H "Authorization: Bearer <api-key>"
curl "https://www.air-cargo.io/api/shipments/trends?days=30" -H "Authorization: Bearer <api-key>"
```

`stats` returns `{"total": 3, "by_status": {"booked": 1, "in_transit": 2, …}}`; `trends` returns `{"trends": [{"date": "2026-11-17", "count": 3}]}`.
