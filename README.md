# air-cargo.io

Developer portal for the [Airtrack](https://www.air-cargo.io) air cargo tracking API.

**Track shipments across 80+ airlines** — DHL, Emirates, Turkish Cargo, Qatar Airways, Lufthansa, and more.

## What's Here

| Directory | Contents |
|-----------|----------|
| `site/` | [VitePress](https://vitepress.dev) documentation site — guides, API reference, SDK docs |
| `sdks/python/` | Official [Python SDK](https://pypi.org/project/airtrack/) — `pip install airack` |
| `integrations/` | Integration templates (Slack, n8n, Zapier, Make) |
| `postman/` | Ready-to-import [Postman collection](postman/airtrack.postman_collection.json) |
| `.github/workflows/` | CI/CD: deploy docs to GitHub Pages, sync OpenAPI spec daily |

## Quickstart

```bash
# 1. Get an API key from https://www.air-cargo.io

# 2. Create a shipment
curl -X POST https://www.air-cargo.io/api/shipments/ \
  -H "Authorization: Bearer <your-api-key>" \
  -H "Content-Type: application/json" \
  -d '{"awb": "235-12345678"}'

# 3. Trigger tracking
curl -X POST "https://www.air-cargo.io/api/tracking/?shipment_id=<id>" \
  -H "Authorization: Bearer <your-api-key>"
```

## Python SDK

```bash
pip install airack
```

```python
from airack import Client

client = Client(api_key="your-api-key")
shipment = client.shipments.create("235-12345678")
print(shipment.status)
```

## Documentation

Full docs at **https://air-cargo.github.io/air-cargo.io**

## License

MIT
