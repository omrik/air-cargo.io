"""Response models. Unknown fields are kept, so new API fields never break the SDK."""
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class _Model(BaseModel):
    model_config = ConfigDict(extra="allow")


class User(_Model):
    id: str
    email: str
    first_name: str
    last_name: str
    plan: str
    active: bool
    email_verified: bool = True
    shipment_limit: int = 0
    shipment_count: int = 0
    api_call_count: int = 0
    trial_end: datetime | None = None
    created_at: datetime


class TrackingEvent(_Model):
    id: str
    shipment_id: str
    status: str
    iata_code: str = ""
    location: str = ""
    timestamp: datetime
    description: str = ""
    source: str
    flight_number: str | None = None
    pieces: int | None = None
    weight_kg: float | None = None
    created_at: datetime


class Shipment(_Model):
    id: str
    awb: str
    origin: str = ""
    destination: str = ""
    carrier_id: str | None = None
    status: str
    pieces: int | None = None
    weight_kg: float | None = None
    volume_cbm: float | None = None
    flight_number: str | None = None
    departure_date: datetime | None = None
    arrival_date: datetime | None = None
    created_at: datetime
    updated_at: datetime
    tracking_events: list[TrackingEvent] = []


class BatchResult(_Model):
    created: list[Shipment]
    skipped: list[str]
    invalid: list[str] = []
    total_created: int
    total_skipped: int


class Pagination(_Model):
    page: int
    per_page: int
    total: int
    pages: int


class ShipmentPage(_Model):
    data: list[Shipment]
    pagination: Pagination

    def __iter__(self):  # type: ignore[override]
        return iter(self.data)


class TrackingPage(_Model):
    events: list[TrackingEvent]
    total: int
    page: int
    limit: int

    def __iter__(self):  # type: ignore[override]
        return iter(self.events)


class Webhook(_Model):
    id: str
    url: str
    events: list[str]
    active: bool
    secret: str | None = None
    state: str = "unused"
    last_delivery: dict | None = None
    created_at: datetime


class WebhookDelivery(_Model):
    id: str
    event_id: str | None = None
    event_type: str | None = None
    shipment_id: str
    url: str
    status_code: int | None = None
    success: bool
    attempts: int | None = None
    next_attempt_at: datetime | None = None
    error_message: str | None = None
    created_at: datetime


class ApiKey(_Model):
    id: str
    name: str
    key: str | None = None
    last_used: datetime | None = None
    revoked: bool = False
    created_at: datetime


class Carrier(_Model):
    id: str
    code: str
    name: str
    iata_prefix: str | None = None
    active: bool
    created_at: datetime
