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
    response = requests.post(ENDPOINT + "/v2/pet", json=payload)
    data = response.json()
    print(data)
    
