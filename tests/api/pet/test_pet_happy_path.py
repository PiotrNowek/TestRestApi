import requests

from config.config import ENDPOINT


def test_check_endpoint():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    

def test_create_new_pet(base_pet):
    """
    Test creating a new pet and check is it correct.
    """
    create_pet_response = create_pet(base_pet)
    assert create_pet_response.status_code == 200, f"Failed to create pet, status code: {create_pet_response.status_code}"
    
    data = create_pet_response.json()
    pet_id = data["id"]
    get_pet_by_id_response = get_pets_by_id(pet_id)
    assert get_pet_by_id_response.status_code == 200, f"Failed to get pet by id, status code: {get_pet_by_id_response.status_code}"
    
    get_pet_by_id = get_pet_by_id_response.json()
    assert get_pet_by_id["id"] == pet_id, f"Expected {pet_id}, but got {get_pet_by_id['id']}."
    assert get_pet_by_id["name"] == base_pet["name"], f"Expected pet name {base_pet['name']}, but got {get_pet_by_id['name']}."
    assert get_pet_by_id["status"] == base_pet["status"], f"Expected pet status {base_pet['status']}, but got {get_pet_by_id['status']}."

    delete_pet_by_id = delete_pet(pet_id)
    assert delete_pet_by_id.status_code == 200, f"Failed to delete pet, status code: {delete_pet_by_id.status_code}"


def test_update_pet(base_pet):
    """
    Test creating a new pet, update a pet and check is it correct.
    """
    create_pet_response = create_pet(base_pet)
    assert create_pet_response.status_code == 200, f"Failed to create pet, status code: {create_pet_response.status_code}"

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
    assert update_pet_response.status_code == 200, f"Failed to update pet, status code: {update_pet_response.status_code}"

    data = update_pet_response.json()
    pet_id = data["id"]
    get_pet_by_id_response = get_pets_by_id(pet_id)
    assert get_pet_by_id_response.status_code == 200, f"Failed to get pet by id, status code: {get_pet_by_id_response.status_code}"

    get_pet_by_id = get_pet_by_id_response.json()
    assert get_pet_by_id["id"] == pet_id, f"Expected {pet_id}, but got {get_pet_by_id['id']}."
    assert get_pet_by_id["name"] == new_payload["name"], f"Expected pet name {new_payload['name']}, but got {get_pet_by_id['name']}."
    assert get_pet_by_id["status"] == new_payload["status"], f"Expected pet status {new_payload['status']}, but got {get_pet_by_id['status']}."

    delete_pet_by_id = delete_pet(pet_id)
    assert delete_pet_by_id.status_code == 200, f"Failed to delete pet, status code: {delete_pet_by_id.status_code}"


def test_delete_pet(base_pet):
    """
    Test creates a new pet and checks if it was deleted correctly
    """
    create_pet_response = create_pet(base_pet)
    assert create_pet_response.status_code == 200, f"Failed to create pet, status code: {create_pet_response.status_code}"

    data = create_pet_response.json()
    pet_id = data["id"]
    delete_pet_by_id = delete_pet(pet_id)
    assert delete_pet_by_id.status_code == 200, f"Failed to delete pet, status code: {delete_pet_by_id.status_code}"

    get_pet_by_id_response = get_pets_by_id(pet_id)
    assert get_pet_by_id_response.status_code == 404, "Expected status code 404, but got: {get_pet_by_id_response.status_code}"


def create_pet(payload):
    return requests.post(ENDPOINT + "/v2/pet", json=payload)


def get_pets_by_id(pet_id):
    return requests.get(ENDPOINT + f"/v2/pet/{pet_id}")


def update_pet(payload):
    return requests.put(ENDPOINT + "/v2/pet", json=payload)


def delete_pet(pet_id):
    return requests.delete(ENDPOINT + f"/v2/pet/{pet_id}")