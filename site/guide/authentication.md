# Authentication

Every request uses the `Authorization: Bearer <token>` header. The token is either an API key or a login session token.

## API keys (for integrations)

Create keys in the dashboard under **API Keys**, or with the API:

```bash
curl -X POST https://www.air-cargo.io/api/account/api-keys \
  -H "Authorization: Bearer <api-key-or-session-token>" \
  -H "Content-Type: application/json" \
  -d '{"name": "erp-production"}'
```

The response contains `key` (48 characters). It is shown only once.

```bash
curl -H "Authorization: Bearer <api-key>" https://www.air-cargo.io/api/shipments/
```

- Keys do not expire; revoke one with `DELETE /api/account/api-keys/{id}`.
- Use a separate key per system so you can revoke one without affecting others.
- Requests are rate-limited by your plan; see [Rate limiting](/guide/rate-limiting).

## Session tokens

The dashboard logs in with email and password and receives a token valid for 24 hours. Use API keys for server-to-server work.

```bash
curl -X POST https://www.air-cargo.io/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "you@example.com", "password": "..."}'
```

The response's `access_token` is used in the same `Authorization: Bearer` header.

New accounts must confirm their email address before they can log in.
