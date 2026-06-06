# Rate Limiting

Rate limits are applied per API key (or per JWT session) and depend on your plan.

## Limits by Plan

| Plan | Rate Limit | Burst |
|------|-----------|-------|
| Free | 10 requests/min | 10 |
| Starter | 60 requests/min | 60 |
| Pro | 300 requests/min | 300 |
| Enterprise | Custom | Custom |

## Headers

Every response includes rate limit headers:

```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 42
X-RateLimit-Reset: 1705320000
```

## Handling Rate Limits

When you exceed your limit, the API returns `429 Too Many Requests`:

```json
{
  "detail": "Rate limit exceeded. Try again in 18 seconds."
}
```

## Best Practices

1. **Cache responses** — Avoid duplicate API calls for the same shipment within short time windows
2. **Batch operations** — Use the batch AWB create endpoint instead of individual calls
3. **Use webhooks** — Instead of polling, subscribe to status changes
4. **Respect Retry-After** — If you get a 429, wait for the time specified in the response before retrying
