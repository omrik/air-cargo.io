# Authentication

Airtrack supports two authentication methods. Both use the `Authorization: Bearer` header.

## API Keys (Recommended for Machines)

Generate API keys from the dashboard under **API Keys**.

```bash
curl -H "Authorization: Bearer <api-key>" https://www.air-cargo.io/api/shipments/
```

- 48-character tokens
- Can be revoked individually
- Rate-limited per plan tier
- Best for scripts, integrations, and automated systems

## JWT Tokens (User Sessions)

JWT tokens are returned on login or registration and expire after 24 hours.

```bash
# Login
curl -X POST https://www.air-cargo.io/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "your-password"}'

# Response includes access_token
curl -H "Authorization: Bearer <jwt-token>" https://www.air-cargo.io/api/account/
```

JWT tokens are best for browser-based applications and user-facing tools.

## Rate Limits

Authentication method doesn't affect rate limits — they're based on your plan tier.

| Plan | Rate Limit |
|------|-----------|
| Free | 10 req/min |
| Starter | 60 req/min |
| Pro | 300 req/min |
| Enterprise | Custom |
