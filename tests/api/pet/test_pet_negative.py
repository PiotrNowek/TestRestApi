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
    invalid_pet_id = 999999999
    response = requests.get(ENDPOINT + f"/v2/pet/{invalid_pet_id}")
    assert response.status_code == 404, f"Expected status code 404, but got {response.status_code}"


  








