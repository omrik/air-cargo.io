# API Reference

The full OpenAPI 3.1 specification is auto-generated from the live API and synced every 24 hours.

- [View openapi.json](/air-cargo.io/api/openapi.json) (raw JSON)
- [Swagger UI](https://www.air-cargo.io/docs) (interactive docs)
- [ReDoc](https://www.air-cargo.io/redoc) (alternative viewer)

## Endpoints Overview

### Public (No Auth)

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/auth/register` | Create account |
| POST | `/api/auth/login` | Login, get JWT |
| GET | `/api/auth/verify` | Verify email |
| POST | `/api/auth/resend-verification` | Resend verification |
| GET | `/api/health` | Health check |

### Shipments

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/shipments/` | List shipments |
| POST | `/api/shipments/` | Create shipment |
| POST | `/api/shipments/batch` | Batch create shipments |
| GET | `/api/shipments/export` | Export as CSV/JSON |
| GET | `/api/shipments/stats` | Aggregate stats |
| GET | `/api/shipments/trends` | Daily trends |
| GET | `/api/shipments/{id}` | Get shipment |
| PATCH | `/api/shipments/{id}` | Update shipment |
| DELETE | `/api/shipments/{id}` | Delete shipment |

### Tracking

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/tracking/` | Trigger tracking refresh |
| GET | `/api/tracking/{id}` | Get tracking events |

### Webhooks

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/webhooks/` | List webhooks |
| POST | `/api/webhooks/` | Register webhook |
| PATCH | `/api/webhooks/{id}` | Toggle active/inactive |
| DELETE | `/api/webhooks/{id}` | Delete webhook |
| GET | `/api/webhooks/{id}/logs` | Delivery logs |

### Account

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/account/` | Get profile |
| PATCH | `/api/account/profile` | Update profile |
| POST | `/api/account/change-password` | Change password |
| POST | `/api/account/api-keys` | Create API key |
| GET | `/api/account/api-keys` | List API keys |
| DELETE | `/api/account/api-keys/{id}` | Revoke API key |

### Carriers

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/carriers/` | List carriers |

### Integrations

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/integrations/slack` | Get Slack status |
| PUT | `/api/integrations/slack` | Set Slack webhook |
| DELETE | `/api/integrations/slack` | Remove Slack |
| POST | `/api/integrations/slack/test` | Test notification |

### Billing

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/billing/plans` | List plans |
| POST | `/api/billing/create-checkout-session` | Create checkout |
| POST | `/api/billing/create-portal-session` | Customer portal |
| GET | `/api/billing/subscription` | Get subscription |

### Admin

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/admin/check` | Verify admin |
| GET | `/api/admin/users` | List users |
| GET | `/api/admin/users/{id}` | Get user |
| PATCH | `/api/admin/users/{id}` | Update user |
| GET | `/api/admin/stats` | Platform stats |
| GET | `/api/admin/scraping/stats` | Scrape stats |
| GET | `/api/admin/scraping/failed` | Failed scrapes |
| GET | `/api/admin/settings` | Get settings |
| PATCH | `/api/admin/settings` | Update settings |
