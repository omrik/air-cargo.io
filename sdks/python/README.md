# Airtrack Python SDK

Official Python client for the [air-cargo.io](https://www.air-cargo.io) air cargo tracking API.

## Installation

```bash
pip install airack
```

## Quickstart

```python
from airack import Client

client = Client(api_key="your-api-key")

# Create a shipment
shipment = client.shipments.create("235-12345678")
print(f"Tracking {shipment.awb} — {shipment.status}")

# List shipments
for s in client.shipments.list(status="IN_TRANSIT"):
    print(s.awb, s.carrier_name)
```

## Documentation

Full documentation at [https://air-cargo.github.io/air-cargo.io](https://air-cargo.github.io/air-cargo.io)
