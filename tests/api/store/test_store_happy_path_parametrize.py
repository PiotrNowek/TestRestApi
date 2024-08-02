import pytest
import requests

from config.config import ENDPOINT, ORDER_ENDPOINT
from conftest import created_orders


def test_check_endpoint():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"


def test_get_pet_list_by_status():
    """
    Test get pet list and checks if the list is in json format
    """
    response = requests.get(f"{ENDPOINT}/v2/store/inventory")
    assert response.status_code == 200, f"Failed to create list, status code: {response.status_code}"
    assert response.headers['Content-Type'] == 'application/json', f"Expected application/json but got {response.headers['Content-Type']}"
    try:
        response = response.json()
    except ValueError:
        assert False, f"Response is not in JSON format"
    assert isinstance(response, dict), f"Expected response to be a dictionary"


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

def test_create_order(new_order_store, order_data):
    """
    Test creates an order and checks if it is correct
    """
    order_id = order_data["id"]
    created_orders.append(order_id)
    order = new_order_store(order_data)
    assert order is not None, f"Expected order to be initialized, but it is None"
    assert order["status"] == order_data["status"], f"Expected order status to be {order_data['status']}, but got {order['status']}"
    assert order and order_data["complete"] == True, f"Expected the order to exist and 'complete' status to be True, but it was not."


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

def test_get_order_by_id(new_order_store, order_data):
    """
    Test checks the correct getting of the order by id
    """
    order = new_order_store(order_data)
    response = requests.get(f"{ORDER_ENDPOINT}/{order['id']}")
    assert response.status_code == 200, f"Failed to get order, status code: {response.status_code}"
    valid_order = response.json()
    assert valid_order['id'] == order['id'], f"Expected order ID to be {valid_order['id']}, but got {order['id']}"
    assert valid_order['status'] == order['status'], f"Expected order status to be {valid_order['status']}, but got {order['status']}"


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

def test_delete_order(new_order_store, order_data):
    """
    Test checks the correct deletion of the order
    """
    order = new_order_store(order_data)
    response = requests.delete(f"{ORDER_ENDPOINT}/{order['id']}")
    assert response.status_code == 200, f"Failed to delete order, status code: {response.status_code}"
    response = requests.get(f"{ORDER_ENDPOINT}/{order['id']}")
    assert response.status_code == 404, f"Expected status code 404, but got {response.status_code}"