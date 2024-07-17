import pytest
import requests


ENDPOINT = "https://petstore.swagger.io"


def test_check_endpoint():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200


def test_add_pet_with_missing_id():
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
    assert response.status_code == 404, f"Expected status code 404, but got {response.status_code}"


def test_add_pet_with_invalid_id():
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
    assert response.status_code == 404, f"Expected status code 404, but got {response.status_code}"


def test_add_pet_with_empty_id():
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
    assert response.status_code == 404, f"Expected status code 404, but got {response.status_code}"    

    

def test_get_pet_by_invalid_id():
    invalid_pet_id = 9999999991 # We assume this ID does not exist
    response = requests.get(ENDPOINT + f"/v2/pet/{invalid_pet_id}")
    assert response.status_code == 404, f"Expected status code 404, but got {response.status_code}"
    response_data = response.json()
    assert "message" in response_data, "Expected 'message' to be in the response data"
    assert response_data["message"] == "Pet not found", f"Expected error message 'Pet not found', but got {response_data['message']}"
    assert response_data["type"] == "error", f"Expected type message 'error', but got {response_data['type']}"


@pytest.fixture
def non_exist_pet():
    return {
        "id" : 999999999, # We assume this ID does not exist
        "category" : {
            "id" : 0,
            "name" : "string"
        },
        "name" : "Ghost",
        "photoUrls" : [
            "string"
        ],
        "tags" : [
            {
                "id" : 0,
                "name" : "string"
            }
        ],
        "status" : "available"
    }


def test_update_nonexist_pet(non_exist_pet):
    response = requests.put(ENDPOINT + "/v2/pet", json=non_exist_pet)
    assert response.status_code == 404, f"Expected status code 404, but got {response.status_code}"
    response_data = response.json()
    assert "message" in response_data, "Expected 'message' to be in response data"
    assert response_data["message"] == "Pet not found", f"Expected error message 'Pet not found', but got {response_data['message']}"
  

def test_delete_nonexist_pet():
    non_exist_pet_id = 8888888 # We assume this ID does not exist
    response = requests.delete(ENDPOINT + f"/v2/pet/{non_exist_pet_id}")
    assert response.status_code == 404, f"Expected status code 404, but got {response.status_code}"
 





