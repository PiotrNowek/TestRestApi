import requests

from config.config import ENDPOINT


def test_check_endpoint():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200
    
def test_create_new_pet():
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
    create_pet_response = create_pet(payload)
    assert create_pet_response.status_code == 200
    data = create_pet_response.json()
    
    pet_id = data["id"]
    get_pet_by_id_response = get_pets_by_id(pet_id)
    assert get_pet_by_id_response.status_code == 200
    
    get_pet_by_id = get_pet_by_id_response.json()
    assert get_pet_by_id["id"] == pet_id
    assert get_pet_by_id["name"] == payload["name"]
    assert get_pet_by_id["status"] == payload["status"]

def test_update_pet():
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
    create_pet_response = create_pet(payload)
    assert create_pet_response.status_code == 200

    new_payload = {
        "id": 0,
        "category": {
            "id": 0,
            "name": "string"
        },
        "name": "cat",
        "photoUrls": [
            "string"
        ],
        "tags": [
            {
                "id": 0,
                "name": "string"
            }
        ],
        "status": "sold"
    }
    update_pet_response = update_pet(new_payload)
    assert update_pet_response.status_code == 200

    data = update_pet_response.json()
    pet_id = data["id"]
    get_pet_by_id_response = get_pets_by_id(pet_id)
    assert get_pet_by_id_response.status_code == 200
    get_pet_by_id = get_pet_by_id_response.json()
    assert get_pet_by_id["id"] == pet_id
    assert get_pet_by_id["name"] == new_payload["name"]
    assert get_pet_by_id["status"] == new_payload["status"]

def test_delete_pet():
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
    create_pet_response = create_pet(payload)
    assert create_pet_response.status_code == 200
    data = create_pet_response.json()
    pet_id = data["id"]

    delete_pet_by_id = delete_pet(pet_id)
    assert delete_pet_by_id.status_code == 200

    get_pet_by_id_response = get_pets_by_id(pet_id)
    assert get_pet_by_id_response.status_code == 404

def create_pet(payload):
    return requests.post(ENDPOINT + "/v2/pet", json=payload)

def get_pets_by_id(pet_id):
    return requests.get(ENDPOINT + f"/v2/pet/{pet_id}")

def update_pet(payload):
    return requests.put(ENDPOINT + "/v2/pet", json=payload)

def delete_pet(pet_id):
    return requests.delete(ENDPOINT + f"/v2/pet/{pet_id}")