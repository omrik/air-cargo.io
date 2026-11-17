# Errors

Errors return a JSON body with `detail`. It is usually a message:

```json
{ "detail": "Shipment not found" }
```

For some errors it is an object or a list with more information (see below).

## Status codes

| Code | Meaning |
|------|---------|
| 400 | Bad request, for example an empty or oversized batch |
| 401 | Missing or invalid API key or token |
| 403 | Not allowed, for example the plan's shipment limit is reached |
| 404 | Not found, or not yours |
| 409 | You already track this AWB |
| 422 | Invalid input |
| 429 | Rate limit exceeded |
| 5xx | Our fault. Retry with backoff. |

## Examples

**409: AWB already tracked**

```json
{
  "detail": {
    "message": "You already track AWB 176-12345675.",
    "shipment_id": "3e959642-6876-493f-9045-633bbadb0706"
  }
}
```

**422: invalid AWB**

```json
{
  "detail": "Invalid AWB number. Use 11 digits: a 3-digit airline prefix and an 8-digit serial, e.g. 235-12345675."
}
```

**422: malformed request body.** Here `detail` is a list of field errors:

```json
{
  "detail": [
    { "type": "missing", "loc": ["body", "awb"], "msg": "Field required" }
  ]
}
```

**403: plan limit**

```json
{ "detail": "Shipment limit reached (50). Upgrade your plan to add more." }
```

**429:** see [Rate limiting](/guide/rate-limiting).
