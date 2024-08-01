import pytest
import requests

from config.config import ENDPOINT, LOGIN_URL
from conftest import created_pets


def test_add_pet_authorized(auth_token):
    """
    Test creating a new pet with authorization token
    """
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
    pet_id = payload["id"]
    created_pets.append(pet_id)
    assert data["name"] == payload["name"], f"Expected name {payload['name']}, but got {data['name']}"
    

   