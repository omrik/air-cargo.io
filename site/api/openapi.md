# API Reference

The complete reference is generated from the running API:

- **[Interactive reference](https://www.air-cargo.io/api/docs)**: try calls in the browser with your API key
- [ReDoc view](https://www.air-cargo.io/api/redoc)
- [openapi.json](https://www.air-cargo.io/api/openapi.json): OpenAPI 3.1, for code generators
- [Postman collection](/airtrack.postman_collection.json): import it and set `token` to your API key

Base URL: `https://www.air-cargo.io/api`. Authentication: `Authorization: Bearer <api-key>`.

## Endpoints

### Shipments

| Method | Path | Description |
|--------|------|-------------|
| POST | `/shipments/` | Track an AWB |
| POST | `/shipments/batch` | Track up to 100 AWBs |
| GET | `/shipments/` | List, filter and sort |
| GET | `/shipments/{id}` | One shipment with its events |
| PATCH | `/shipments/{id}` | Update details |
| DELETE | `/shipments/{id}` | Stop tracking |
| GET | `/shipments/export` | CSV or JSON export |
| GET | `/shipments/stats` | Counts by status |
| GET | `/shipments/trends` | Shipments added per day |

### Tracking

| Method | Path | Description |
|--------|------|-------------|
| POST | `/tracking/?shipment_id={id}` | Ask the airline now, or add your own event |
| GET | `/tracking/{shipment_id}` | Event history |

### Webhooks

| Method | Path | Description |
|--------|------|-------------|
| POST | `/webhooks/` | Register an endpoint |
| GET | `/webhooks/` | List, with delivery state |
| PATCH | `/webhooks/{id}` | Pause, or change URL or events |
| DELETE | `/webhooks/{id}` | Delete |
| POST | `/webhooks/{id}/test` | Send a signed sample |
| GET | `/webhooks/{id}/logs` | Recent deliveries |

### Account and reference data

| Method | Path | Description |
|--------|------|-------------|
| GET | `/account/` | Your plan, limits and usage |
| GET | `/account/api-keys` | List API keys |
| POST | `/account/api-keys` | Create an API key |
| DELETE | `/account/api-keys/{id}` | Revoke an API key |
| GET | `/carriers/` | Airlines and their AWB prefixes |
| GET | `/integrations/slack` | Slack notification settings |
| PUT | `/integrations/slack` | Connect a Slack incoming webhook |
| DELETE | `/integrations/slack` | Disconnect Slack |
| POST | `/integrations/slack/test` | Send a test Slack message |

Health check (no auth): `GET https://www.air-cargo.io/health`.
