---
layout: home

hero:
  name: Airtrack API
  text: Air cargo tracking by AWB
  tagline: Add an air waybill, get IATA milestones as they happen, and receive signed webhooks. One REST API, flat monthly pricing.
  actions:
    - theme: brand
      text: Quickstart
      link: /guide/quickstart
    - theme: alt
      text: Webhooks
      link: /guide/webhooks
    - theme: alt
      text: API Reference
      link: /api/openapi

features:
  - title: Simple REST API
    details: Create shipments by AWB, read tracking events, manage webhooks. JSON over HTTPS, API key auth.
  - title: IATA milestones
    details: Standard status codes (BKD, RCS, DEP, ARR, RCF, NFD, DLV, DIS…) with station, UTC time and flight, grouped into six simple statuses.
  - title: Signed webhooks with retries
    details: Every new milestone and status change is pushed to your endpoint, HMAC-SHA256 signed, retried after 1, 5 and 30 minutes.
  - title: Many airlines
    details: Direct connections to a growing list of airlines' own tracking, plus a partner network for the rest. Coverage and speed vary by airline.
  - title: Python SDK
    details: Typed client with a webhook signature helper. Installs from GitHub.
  - title: Flat pricing
    details: No per-shipment fees. Predictable monthly cost for high-volume forwarders.
---
