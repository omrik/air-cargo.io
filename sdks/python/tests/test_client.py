from airack import Client


def test_client_initialization():
    client = Client(api_key="test-key")
    assert client._token == "test-key"
    assert client.base_url == "https://www.air-cargo.io/api"
    client.close()


def test_client_auth_header():
    client = Client(api_key="test-key")
    headers = client._headers()
    assert headers["Authorization"] == "Bearer test-key"
    client.close()


def test_client_jwt():
    client = Client(jwt_token="jwt-token")
    headers = client._headers()
    assert headers["Authorization"] == "Bearer jwt-token"
    client.close()
