# Rate limiting

Requests are counted per account over a rolling minute. API keys and dashboard sessions of the same account share one count.

| Plan | Requests per minute |
|------|---------------------|
| Free | 30 |
| Starter | 120 |
| Pro | 300 |
| Enterprise | Custom |

Requests without a valid token are limited to 60 per minute per IP address.

## Headers

Every response carries:

```
X-RateLimit-Limit: 120
X-RateLimit-Remaining: 87
X-RateLimit-Reset: 1794948099
```

`X-RateLimit-Reset` is a Unix time in seconds.

## When you go over

The API answers `429 Too Many Requests`:

```json
{
  "detail": "Rate limit exceeded. Try again shortly.",
  "rate_limit": { "limit": 120, "remaining": 0, "reset": 1794948099 }
}
```

Wait until `reset`, then continue.

## Tips

- Use [webhooks](/guide/webhooks) instead of polling for changes.
- Add many AWBs with one `POST /api/shipments/batch` call (up to 100).
- Don't call `POST /api/tracking/` in a loop: Airtrack already checks on a schedule.
