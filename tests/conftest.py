import pytest
import requests

from config.config import ENDPOINT, ORDER_ENDPOINT, LOGIN_URL


@pytest.fixture
def new_order():
    '''
    Fixture to create a new order for a pet in the system.
    '''
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
    '''
    Fixture to delete a order for a pet in the system.
    '''
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
    '''
    Fixture to create a non existent pet in the system.
    '''
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
    '''
    Fixture to create a API Token for authorization.
    '''
    username = "test"
    password = "abc123"
    response = requests.get(LOGIN_URL, params={"username": username, "password": password})
    response.raise_for_status()
    # Predefined authorization token (example)
    return "YOUR_API_TOKEN"


@pytest.fixture
def create_order_url():
    '''
    Fixture to create a new order url for a pet in the system.
    '''
    return f"{ENDPOINT}/v2/store/order"


@pytest.fixture
def new_order_store():
    '''
    Fixture to create a new order for a pet in the system from order data.
    '''
    def create_order(order_data):
        response = requests.post(ORDER_ENDPOINT, json=order_data)
        assert response.status_code == 200, f"Failed to create order, status code: {response.status_code}"
        order = response.json()
        return order
    return create_order


@pytest.fixture
def base_user():
    '''
    Fixture to create a new user in the system.
    '''
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
    '''
    Fixture to create a new pet in the system.
    '''
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


created_users = []
"""
Global list to store usernames created during testing
"""


@pytest.fixture(autouse=True)
def cleanup_users():
    """
    Deletes all users created during testing.
    """
    yield
    while created_users: 
        username = created_users.pop()
        response = requests.delete(f"{ENDPOINT}/v2/user/{username}")
        if response.status_code == 200:
            print(f"Deleted user: {username}")
        else:
            print(f"User {username} not found or already deleted.")


created_pets = []
"""
Global list to store pets created during testing
"""


@pytest.fixture(autouse=True)
def cleanup_pets():
    """
    Deletes all pets created during testing.
    """
    yield
    while created_pets: 
        pet_id = created_pets.pop()
        response = requests.delete(f"{ENDPOINT}/v2/pet/{pet_id}")
        if response.status_code == 200:
            print(f"Deleted pet: {pet_id}")
        else:
            print(f"Pet {pet_id} not found or already deleted.")