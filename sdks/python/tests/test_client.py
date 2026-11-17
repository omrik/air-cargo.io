import hashlib
import hmac
import json

import httpx
import pytest

from airtrack import Client, ConflictError, NotFoundError, verify_webhook


def make_client(handler) -> Client:
    return Client(api_key="test-key", base_url="https://api.test/api",
                  http_client=httpx.Client(transport=httpx.MockTransport(handler)))


SHIPMENT = {"id": "s1", "awb": "176-12345675", "origin": "", "destination": "", "status": "booked",
            "created_at": "2026-11-17T10:00:00Z", "updated_at": "2026-11-17T10:00:00Z"}


def test_sends_bearer_key_and_parses_shipment():
    seen = {}

    def handler(request):
        seen["auth"] = request.headers["Authorization"]
        seen["body"] = json.loads(request.content)
        return httpx.Response(201, json=SHIPMENT)

    s = make_client(handler).shipments.create("176-12345675")
    assert seen == {"auth": "Bearer test-key", "body": {"awb": "176-12345675"}}
    assert s.awb == "176-12345675"


def test_conflict_carries_existing_shipment_id():
    def handler(request):
        return httpx.Response(409, json={"detail": {"message": "You already track AWB 176-12345675.",
                                                    "shipment_id": "s1"}})

    with pytest.raises(ConflictError) as err:
        make_client(handler).shipments.create("176-12345675")
    assert err.value.status_code == 409
    assert err.value.detail["shipment_id"] == "s1"
    assert "already track" in str(err.value)


def test_not_found():
    with pytest.raises(NotFoundError):
        make_client(lambda r: httpx.Response(404, json={"detail": "Shipment not found"})).shipments.get("x")


def test_tracking_page_is_iterable():
    event = {"id": "e1", "shipment_id": "s1", "status": "in_transit", "iata_code": "DEP", "location": "TLV",
             "timestamp": "2026-11-17T19:38:00Z", "description": "Departed", "source": "carrier",
             "created_at": "2026-11-17T19:40:00Z"}
    page = make_client(lambda r: httpx.Response(200, json={"events": [event], "total": 1, "page": 1, "limit": 50})
                       ).tracking.get("s1")
    assert [e.iata_code for e in page] == ["DEP"]


def test_verify_webhook():
    body = b'{"id":"evt_1","type":"tracking_update"}'
    sig = hmac.new(b"secret", body, hashlib.sha256).hexdigest()
    assert verify_webhook(body, sig, "secret")
    assert not verify_webhook(body + b" ", sig, "secret")
    assert not verify_webhook(body, "", "secret")
