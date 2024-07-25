import pytest
import requests

from config.config import ENDPOINT


def test_check_endpoint():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200


def test_min_name_lenght():
    payload = {
        "id": 101,
        "category": {
            "id": 0,
            "name": "string"
        },
        "name": "a",
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
    response = requests.post(ENDPOINT + "/v2/pet", json=payload)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    assert response.json()["name"] == payload["name"], f"Expected name '{payload['name']}', but got '{response.json()['name']}'"


def test_max_name_lenght():
    long_name = "a" * 256
    payload = {
        "id": 56,
        "category": {
            "id": 0,
            "name": "string"
        },
        "name": long_name,
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
    response = requests.post(ENDPOINT + "/v2/pet", json=payload)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    assert response.json()["name"] == payload["name"], f"Expected name '{payload['name']}', but got '{response.json()['name']}'"


def test_create_pet_with_missing_required_fields():
    payload = {
    }
    response = requests.post(ENDPOINT + "/v2/pet", json=payload)
    assert response.status_code == 400, f"Expected status code 400, but got {response.status_code}"


def test_request_too_large():
    payload = {
        "id": 1,
        "name": "Janek",
        "photoUrls": ["http://" + "a" * 10000 + ".com"],  # Long URL
        "status": "available"
    }
    response = requests.post(ENDPOINT + "/v2/pet", json=payload)
    assert response.status_code == 413, f"Expected status code 413, but got {response.status_code}"
    assert "error" in response.json(), "Expected 'error' key in response"
    

def test_get_pet_with_invalid_status():
    payload = {
        "id": 1010,
        "category": {
            "id": 0,
            "name": "string"
        },
        "name": "a",
        "photoUrls": [
            "string"
        ],
        "tags": [
            {
                "id": 0,
                "name": "string"
            }
        ],
        "status": "invalid"
    }
    response = requests.get(ENDPOINT + "/v2/pet/findByStatus",json=payload)
    assert response.status_code == 400, f"Expected status code 400, but got {response.status_code}"
    assert "error" in response.json(), "Expected 'error' key in response"


def test_get_pet_with_empty_status():
    payload = {
        "id": 1011,
        "category": {
            "id": 0,
            "name": "string"
        },
        "name": "a",
        "photoUrls": [
            "string"
        ],
        "tags": [
            {
                "id": 0,
                "name": "string"
            }
        ],
        "status": ""
    }
    response = requests.get(ENDPOINT + "/v2/pet/findByStatus",json=payload)
    assert response.status_code == 400, f"Expected status code 400, but got {response.status_code}"
    assert "error" in response.json(), "Expected 'error' key in response"


def test_get_pet_with_missing_status():
    payload = {
        "id": 1012,
        "category": {
            "id": 0,
            "name": "string"
        },
        "name": "a",
        "photoUrls": [
            "string"
        ],
        "tags": [
            {
                "id": 0,
                "name": "string"
            }
        ],
    }
    response = requests.get(ENDPOINT + "/v2/pet/findByStatus",json=payload)
    assert response.status_code == 400, f"Expected status code 400, but got {response.status_code}"
    assert "error" in response.json(), "Expected 'error' key in response"
        