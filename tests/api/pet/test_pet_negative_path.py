import pytest
import requests

from config.config import ENDPOINT


def test_check_endpoint():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"


def test_add_pet_with_missing_id():
    """
    Test checks if it is possible to add a pet with a missing id
    """
    payload = {
        "category": {
            "id": 0,
            "name": "string"
        },
        "name": "dog",
        "photoUrls": ["string"],
        "tags": [
            {
                "id": 0,
                "name": "string"
            }
        ],
        "status": "available"
    }
    response = requests.post(ENDPOINT + "/v2/pet", json=payload)
    assert response.status_code == 400, f"Expected status code 400, but got {response.status_code}"


def test_add_pet_with_invalid_id():
    """
    Test checks if it is possible to add a pet with an invalid id
    """
    payload = {
        "id": "invalid_id",  
        "category": {
            "id": 0,
            "name": "string"
        },
        "name": "dog",
        "photoUrls": ["string"],
        "tags": [
            {
                "id": 0,
                "name": "string"
            }
        ],
        "status": "available"
    }
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(ENDPOINT + "/v2/pet", json=payload, headers=headers)
    assert response.status_code == 400, f"Expected status code 400, but got {response.status_code}"


def test_add_pet_with_empty_id():
    """
    Test checks if it is possible to add a pet with an empty id
    """
    payload = {
        "id": "",  
        "category": {
            "id": 0,
            "name": "string"
        },
        "name": "dog",
        "photoUrls": ["string"],
        "tags": [
            {
                "id": 0,
                "name": "string"
            }
        ],
        "status": "available"
    }
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(ENDPOINT + "/v2/pet", json=payload, headers=headers)
    assert response.status_code == 400, f"Expected status code 400, but got {response.status_code}"    

    

def test_get_pet_by_invalid_id():
    """
    Test checks if it is possible to get a pet with a invalid id
    """
    invalid_pet_id = 9999999991 # We assume this ID does not exist
    response = requests.get(ENDPOINT + f"/v2/pet/{invalid_pet_id}")
    assert response.status_code == 404, f"Expected status code 404, but got {response.status_code}"
    response_data = response.json()
    assert "message" in response_data, "Expected 'message' to be in the response data"
    assert response_data["message"] == "Pet not found", f"Expected error message 'Pet not found', but got {response_data['message']}"
    assert response_data["type"] == "error", f"Expected type message 'error', but got {response_data['type']}"


def test_update_non_exist_pet(non_exist_pet):
    """
    Test checks if it is possible to update a non-existent pet
    """
    response = requests.put(ENDPOINT + "/v2/pet", json=non_exist_pet)
    assert response.status_code == 404, f"Expected status code 404, but got {response.status_code}"
    response_data = response.json()
    assert "message" in response_data, "Expected 'message' to be in response data"
    assert response_data["message"] == "Pet not found", f"Expected error message 'Pet not found', but got {response_data['message']}"
  

def test_delete_non_exist_pet():
    """
    Test checks if it is possible to delete a non-existent pet
    """
    non_exist_pet_id = 8888888 # We assume this ID does not exist
    response = requests.delete(ENDPOINT + f"/v2/pet/{non_exist_pet_id}")
    assert response.status_code == 404, f"Expected status code 404, but got {response.status_code}"
 

def test_invalid_Content_Type_header():
    """
    Test creating a new pet with invalid Content-Type header.
    """
    payload = {
        "id": 5050,  
        "category": {
            "id": 0,
            "name": "string"
        },
        "name": "dog",
        "photoUrls": ["string"],
        "tags": [
            {
                "id": 0,
                "name": "string"
            }
        ],
        "status": "available"
    }
    headers = {
        "Content-Type": "text/plain"
    }
    response = requests.post(ENDPOINT + "/v2/pet", json=payload, headers=headers)
    assert response.status_code == 415, f"Expected status code 415, but got {response.status_code}"
    


def test_missing_Content_Type_header():
    """
    Test creating a new pet without a Content-Type header.
    """
    payload = {
        "id": 50505,  
        "category": {
            "id": 0,
            "name": "string"
        },
        "name": "dog",
        "photoUrls": ["string"],
        "tags": [
            {
                "id": 0,
                "name": "string"
            }
        ],
        "status": "available"
    }
    headers = {
    }
    response = requests.post(ENDPOINT + "/v2/pet", json=payload, headers=headers)
    assert response.status_code == 415, f"Expected status code 415, but got {response.status_code}"


def test_empty_Content_Type_header():
    """
    Test creating a new pet with empty Content-Type header.
    """
    payload = {
        "id": 505050,  
        "category": {
            "id": 0,
            "name": "string"
        },
        "name": "dog",
        "photoUrls": ["string"],
        "tags": [
            {
                "id": 0,
                "name": "string"
            }
        ],
        "status": "available"
    }
    headers = {
        "Content-Type" : ""
    }
    response = requests.post(ENDPOINT + "/v2/pet", json=payload, headers=headers)
    assert response.status_code == 415, f"Expected status code 415, but got {response.status_code}"


def test_requesting_invalid_endpoint():
    """
    Test checks it is possible to send a request to a non-existent endpoint
    """
    payload = {
        "id": 10010,
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
    response = requests.get(ENDPOINT + "/v2/pet/invalid", json=payload)
    assert response.status_code == 404, f"Expected status code 404, but got {response.status_code}"