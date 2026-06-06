# Errors

All API errors return a consistent JSON structure:

```json
{
  "detail": "Error description"
}
```

## HTTP Status Codes

| Code | Meaning |
|------|---------|
| 400 | Bad Request — invalid input |
| 401 | Unauthorized — missing or invalid token |
| 403 | Forbidden — insufficient permissions |
| 404 | Not Found — resource doesn't exist |
| 409 | Conflict — duplicate resource (e.g., duplicate AWB) |
| 429 | Too Many Requests — rate limit exceeded |
| 500 | Internal Server Error |

## Common Errors

### Invalid AWB Format

```json
{
  "detail": "Invalid AWB format. Expected format: XXX-XXXXXXXX"
}
```

AWB numbers use the format `CCC-NNNNNNNN` where `CCC` is a 3-digit IATA prefix and `NNNNNNNN` is an 8-digit serial number.

### Duplicate AWB

```json
{
  "detail": "Shipment with AWB 235-12345678 already exists"
}
```

### Rate Limited

```json
{
  "detail": "Rate limit exceeded. Try again in 18 seconds."
}
```

See [Rate Limiting](/guide/rate-limiting) for details.

## Error Handling Best Practices

1. **Check HTTP status code first**, then parse `detail`
2. **Retry with backoff** on 429 and 5xx errors
3. **Log `detail`** for debugging non-2xx responses
