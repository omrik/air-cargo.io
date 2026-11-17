# Airtrack Python SDK

Python client for the [Airtrack](https://www.air-cargo.io) air cargo tracking API.

## Installation

```bash
pip install "git+https://github.com/omrik/air-cargo.io.git#subdirectory=sdks/python"
```

The package is not on PyPI yet.

## Quickstart

```python
from airtrack import Client, ConflictError

client = Client(api_key="your-api-key")

try:
    shipment = client.shipments.create("176-12345675")
except ConflictError as e:
    shipment = client.shipments.get(e.detail["shipment_id"])  # already tracked

for event in client.tracking.get(shipment.id):
    print(event.timestamp, event.iata_code, event.location, event.description)
```

## Documentation

https://docs.air-cargo.io/sdks/python
