# Tracking

## Statuses

Each shipment has one status. Each tracking event also has the status it moved the shipment to.

| Status | Meaning |
|--------|---------|
| `booked` | Booked with the airline |
| `accepted` | Received by the airline and prepared or manifested |
| `in_transit` | Departed, or landed at a transit airport |
| `landed` | Arrived at the destination airport |
| `delivered` | Handed to the consignee |
| `exception` | The airline reported a discrepancy |

A status only moves forward. An arrival at a transit airport keeps the shipment `in_transit` until it reaches its destination.

## IATA milestone codes

Events carry the airline's IATA Cargo-IMP status code in `iata_code`:

| Code | Description | Status |
|------|-------------|--------|
| `BKD` | Booked | `booked` |
| `FWB` | Electronic air waybill received | `accepted` |
| `FOH` | Freight on hand | `accepted` |
| `RCS` | Received from shipper | `accepted` |
| `RCT` | Received from another airline | `accepted` |
| `PRE` | Prepared for loading | `accepted` |
| `MAN` | Manifested on a flight | `accepted` |
| `CLD` | Loaded on a flight | `accepted` |
| `PDD` | Customs pre-declaration sent | `accepted` |
| `DEP` | Departed | `in_transit` |
| `TFD` | Transferred to another flight or airline | `in_transit` |
| `ARR` | Arrived | `landed` (`in_transit` at a transit airport) |
| `RCF` | Received from flight | `landed` |
| `AWR` | Arrival documents received | `landed` |
| `NFD` | Consignee notified | `landed` |
| `AWD` | Documents delivered to consignee | `landed` |
| `CRC` | Reported to customs | `landed` |
| `CCD` | Cleared by customs | `landed` |
| `CLC` | Cleared by customs | `landed` |
| `TRM` | To be transferred to another airline | `landed` |
| `DLV` | Delivered | `delivered` |
| `DIS` | Discrepancy | `exception` |
| `SOH` | Shipment on hold | `exception` |
| `OFF` | Offloaded from a flight | `exception` |

Which codes you receive depends on the airline: some publish every step, others only departures and arrivals. A code not in this table (for example `TPL`, a temperature log) is passed through as the airline sent it, and its event keeps the shipment's current status.

Events you add yourself without a code, and events from a few older airline sources that publish no codes, get the code that matches their status (`BKD`, `RCS`, `DEP`, `ARR`, `DLV` or `DIS`).

### Reading milestones

- **Delivery.** Only `DLV` means the goods were handed over, and only `DLV` sets a shipment to `delivered`. `NFD` (consignee notified) and `AWD` (documents delivered) come before it, while the goods still wait at the airport.
- **Actual times.** Use `DEP` for the actual departure and `ARR` for the actual arrival. `MAN`, `RCF` and the other codes have their own times.
- **Split lines.** An airline reports a split shipment as several events with the same code, airport and time and different `pieces`, for example `RCF` with 4 pieces and `RCF` with 5. These are separate events, not duplicates. Use `id` to tell events apart.
- **Sources.** One milestone is stored once. If both the airline's own tracking and the partner network report it, the second report is recognised as the same event and is not sent again.

## Refresh now

```bash
curl -X POST "https://www.air-cargo.io/api/tracking/?shipment_id=<shipment-id>" \
  -H "Authorization: Bearer <api-key>"
```

Returns a list of the events that are new (often empty). Webhooks fire for them as usual.

## Read the history

```bash
curl "https://www.air-cargo.io/api/tracking/<shipment-id>?page=1&limit=50" \
  -H "Authorization: Bearer <api-key>"
```

```json
{
  "events": [
    {
      "id": "058a5507-f675-4f15-aa15-a1114b5b6e01",
      "shipment_id": "3e959642-6876-493f-9045-633bbadb0706",
      "status": "in_transit",
      "iata_code": "DEP",
      "location": "TLV",
      "timestamp": "2026-11-17T19:38:00Z",
      "description": "Departed — flight has departed",
      "flight_number": "5C851",
      "pieces": 3,
      "weight_kg": 420.5,
      "source": "carrier",
      "created_at": "2026-11-17T19:40:12Z"
    }
  ],
  "total": 1,
  "page": 1,
  "limit": 50
}
```

- `timestamp` is when it happened, in UTC (converted from the airport's local time).
- `created_at` is when Airtrack recorded it.
- `location` is the IATA airport code.
- `source` is `carrier` (the airline's own tracking), `network` (our partner tracking network) or `manual` (added by you).

## Update timing

Airtrack asks airlines for updates on a schedule. Airlines don't push to us.

| Shipment | How often |
|----------|-----------|
| Booked, accepted, in transit | Every 30 minutes |
| Landed or exception, waiting for delivery | Every 3 hours, for up to 14 days |
| Delivered | No longer checked |
| Archived | Not checked; see [Archive](/guide/shipments#archive) |

For airlines tracked through the partner network, a shipment is asked at most every 2 hours (3 hours when there was no data, 6 hours once landed).

So a milestone usually reaches you within 30 minutes for airlines we connect to directly, and within 2–3 hours for the others. When a check finds something new, the webhook is sent within seconds. `POST /api/tracking/` asks right away; for partner-network airlines, at most once every 10 minutes per shipment.

## Add an event yourself

You can record an event Airtrack cannot see, for example a delivery confirmed by your own driver:

```bash
curl -X POST "https://www.air-cargo.io/api/tracking/?shipment_id=<shipment-id>" \
  -H "Authorization: Bearer <api-key>" \
  -H "Content-Type: application/json" \
  -d '{"status": "delivered", "iata_code": "DLV", "location": "JFK", "description": "Signed by J. Smith"}'
```

It is stored with `source: "manual"` and sent to your webhooks.
