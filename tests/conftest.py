import pytest
import requests

from config.config import ENDPOINT, ORDER_ENDPOINT, LOGIN_URL


@pytest.fixture
def new_order():
    new_order = {
        "id": 0,
        "petId": 0,
        "quantity": 1,
        "shipDate": "2024-07-16T19:20:30.45Z",
        "status": "placed",
        "complete": True
    }
    response = requests.post(ORDER_ENDPOINT, json=new_order)
    assert response.status_code == 200, f"Failed to create order, status code: {response.status_code}"

    order = response.json()
    yield order

    delete_response = requests.delete(f"{ORDER_ENDPOINT}/{order['id']}")
    assert delete_response.status_code == 200, f"Failed to delete order, status code: {delete_response.status_code}"


@pytest.fixture
def delete_order():
    order = {
        "id": 0,
        "petId": 0,
        "quantity": 1,
        "shipDate": "2024-07-16T19:20:30.45Z",
        "status": "placed",
        "complete": True
    }
    response = requests.post(ORDER_ENDPOINT, json=order)
    assert response.status_code == 200, f"Failed to create order, status code: {response.status_code}"

    order = response.json()
    yield order


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


@pytest.fixture
def auth_token():
    username = "test"
    password = "abc123"
    response = requests.get(LOGIN_URL, params={"username": username, "password": password})
    response.raise_for_status()
    # Predefined authorization token (example)
    return "YOUR_API_TOKEN"


@pytest.fixture
def create_order_url():
    return f"{ENDPOINT}/v2/store/order"


@pytest.fixture
def new_order_store():
    def create_order(order_data):
        response = requests.post(ORDER_ENDPOINT, json=order_data)
        assert response.status_code == 200, f"Failed to create order, status code: {response.status_code}"
        order = response.json()
        return order
    return create_order


@pytest.fixture
def base_user():
    return {
        "id": 0,
        "username": "Rambo",
        "firstName": "FirstName1",
        "lastName": "LastName1",
        "email": "user1@example.com",
        "password": "password1",
        "phone": "123456789",
        "userStatus": 0
    }


@pytest.fixture
def base_pet():
    return {
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