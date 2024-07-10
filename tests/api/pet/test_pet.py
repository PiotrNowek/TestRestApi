import requests


ENDPOINT = "https://petstore.swagger.io"


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
    data = create_pet_response.json()
    
    pet_id = data["id"]
    get_pet_by_id_response = function_get_pet_by_id(pet_id)
    
    get_pet_by_id = get_pet_by_id_response.json()
    assert get_pet_by_id["id"] == pet_id
    assert get_pet_by_id["name"] == payload["name"]
    assert get_pet_by_id["status"] == payload["status"]

def create_pet(payload):
    return requests.post(ENDPOINT + "/v2/pet", json=payload)

def function_get_pet_by_id(pet_id):
    return requests.get(ENDPOINT + f"/v2/pet/{pet_id}")