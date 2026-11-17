# Airtrack developer portal

Documentation, SDK and integration templates for the [Airtrack](https://www.air-cargo.io) air cargo tracking API.

**Docs: https://docs.air-cargo.io**

| Directory | Contents |
|-----------|----------|
| `site/` | [VitePress](https://vitepress.dev) documentation site, published to docs.air-cargo.io by GitHub Pages |
| `sdks/python/` | Python SDK |
| `integrations/` | n8n workflow template |
| `postman/` | Postman collection |

## Quickstart

```bash
# Create an API key in the dashboard at https://www.air-cargo.io, then:
curl -X POST https://www.air-cargo.io/api/shipments/ \
  -H "Authorization: Bearer $AIRTRACK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"awb": "176-12345675"}'
```

## Python SDK

```bash
pip install "git+https://github.com/omrik/air-cargo.io.git#subdirectory=sdks/python"
```

```python
from airtrack import Client

client = Client(api_key="your-api-key")
shipment = client.shipments.create("176-12345675")
for event in client.tracking.get(shipment.id):
    print(event.iata_code, event.location, event.timestamp)
```

## License

MIT
