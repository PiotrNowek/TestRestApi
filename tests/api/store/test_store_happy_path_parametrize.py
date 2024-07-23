import pytest
import requests


ENDPOINT = "https://petstore.swagger.io"
ORDER_ENDPOINT = f"{ENDPOINT}/v2/store/order"


def test_check_endpoint():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200


def test_returns_pet_inventories_by_status():
    return_pet_response = requests.get(ENDPOINT + "/v2/store/inventory")
    assert return_pet_response.status_code == 200


@pytest.fixture
def new_order():
    def create_order(order_data):
        response = requests.post(ORDER_ENDPOINT, json=order_data)
        assert response.status_code == 200, f"Failed to create order, status code: {response.status_code}"
        order = response.json()
        return order
    return create_order


@pytest.mark.parametrize("order_data", [
    {
        "id": 0,
        "petId": 0,
        "quantity": 1,
        "shipDate": "2024-07-16T19:20:30.45Z",
        "status": "placed",
        "complete": True
    },
    {
        "id": 10,
        "petId": 1,
        "quantity": 2,
        "shipDate": "2024-07-16T19:20:30.45Z",
        "status": "approved",
        "complete": True
    }
])

def test_create_order(new_order, order_data):
    order = new_order(order_data)
    assert order is not None
    assert order["status"] == order_data["status"]
    assert order and order_data["complete"] == True


@pytest.mark.parametrize("order_data", [
    {
        "id": 0,
        "petId": 0,
        "quantity": 1,
        "shipDate": "2024-07-16T19:20:30.45Z",
        "status": "placed",
        "complete": True
    },
    {
        "id": 10,
        "petId": 1,
        "quantity": 2,
        "shipDate": "2024-07-16T19:20:30.45Z",
        "status": "approved",
        "complete": True
    }
])

def test_get_order_by_id(new_order, order_data):
    order = new_order(order_data)
    response = requests.get(f"{ORDER_ENDPOINT}/{order['id']}")
    assert response.status_code == 200, f"Failed to get order, status code: {response.status_code}"
    valid_order = response.json()
    assert valid_order['id'] == order['id']
    assert valid_order['status'] == order['status']


@pytest.mark.parametrize("order_data", [
    {
        "id": 0,
        "petId": 0,
        "quantity": 1,
        "shipDate": "2024-07-16T19:20:30.45Z",
        "status": "placed",
        "complete": True
    },
    {
        "id": 10,
        "petId": 1,
        "quantity": 2,
        "shipDate": "2024-07-16T19:20:30.45Z",
        "status": "approved",
        "complete": True
    }
])

def test_delete_order(new_order, order_data):
    order = new_order(order_data)
    response = requests.delete(f"{ORDER_ENDPOINT}/{order['id']}")
    assert response.status_code == 200, f"Failed to delete order, status code: {response.status_code}"
    response = requests.get(f"{ORDER_ENDPOINT}/{order['id']}")
    assert response.status_code == 404, f"Expected status code 404, but got {response.status_code}"