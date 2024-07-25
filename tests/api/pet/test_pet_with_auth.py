import pytest
import requests

from config.config import ENDPOINT, LOGIN_URL


@pytest.fixture
def auth_token():
    username = "test"
    password = "abc123"
    response = requests.get(LOGIN_URL, params={"username": username, "password": password})
    response.raise_for_status()
    # Predefined authorization token (example)
    return "YOUR_API_TOKEN"

def test_add_pet_authorized(auth_token):
    payload = {
        "id": 0,
        "category": {
            "id": 0,
            "name": "string"
        },
        "name": "dog",
        "photoUrls": [
            "string"
        ],
        "tags": [
            {
                "id": 0,
                "name": "string"
            }
        ],
        "status": "available"
    }

    # Authorization Token Request Headers
    headers = {
        "Content-Type": "application/json",
        "api_key": auth_token
    }
    response = requests.post(ENDPOINT + "/v2/pet", json=payload, headers=headers)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    data = response.json()
    assert data["name"] == payload["name"], f"Expected name {payload['name']}, but got {data['name']}"
    

   