from datetime import datetime
from pydantic import BaseModel


class User(BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str
    plan: str
    active: bool
    email_verified: bool = True
    is_admin: bool = False
    created_at: datetime


class Shipment(BaseModel):
    id: str
    awb: str
    origin: str
    destination: str
    carrier_id: str | None = None
    carrier_name: str | None = None
    status: str
    pieces: int | None = None
    weight_kg: float | None = None
    volume_cbm: float | None = None
    flight_number: str | None = None
    created_at: datetime
    updated_at: datetime


class TrackingEvent(BaseModel):
    id: str
    shipment_id: str
    status: str
    location: str
    timestamp: datetime
    description: str
    source: str
    created_at: datetime


class Webhook(BaseModel):
    id: str
    url: str
    events: list
    active: bool
    secret: str | None = None
    created_at: datetime


class WebhookLog(BaseModel):
    id: str
    webhook_id: str
    event_type: str
    status_code: int | None = None
    success: bool
    created_at: datetime


class ApiKey(BaseModel):
    id: str
    name: str
    key: str | None = None
    last_used: datetime | None = None
    revoked: bool = False
    created_at: datetime


class Carrier(BaseModel):
    id: str
    code: str
    name: str
    iata_prefix: str | None = None
    active: bool
    created_at: datetime


class Pagination(BaseModel):
    page: int
    limit: int
    total: int
    pages: int


class PaginatedResponse(BaseModel):
    data: list
    pagination: Pagination


class Plan(BaseModel):
    id: str
    name: str
    price: int
    currency: str
    interval: str


class Subscription(BaseModel):
    plan: str
    status: str | None = None
    current_period_end: datetime | None = None
    cancel_at_period_end: bool = False
    on_trial: bool = False


class SlackConfig(BaseModel):
    connected: bool
    webhook_url: str | None = None
