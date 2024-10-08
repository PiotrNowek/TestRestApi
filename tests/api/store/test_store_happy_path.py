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


def test_create_order(new_order):
    """
    Test creates an order and checks if it is correct
    """
    order_id = new_order["id"]
    created_orders.append(order_id)
    assert new_order["id"] is not None, f"Expected order to be initialized, but it is None"
    assert new_order["status"] == "placed", f"Expected status to be 'placed', but got {new_order['status']}"
    assert new_order["complete"] == True, f"Expected the order to exist and 'complete' status to be True, but it was not."


def test_get_order_by_id(new_order):
    """
    Test checks the correct getting of the order by id
    """
    response = requests.get(f"{ORDER_ENDPOINT}/{new_order['id']}")
    assert response.status_code == 200, f"Failed to find order, status code: {response.status_code}"
    order = response.json()
    assert order["id"] == new_order["id"], f"Expected order ID to be {new_order['id']}, but got {order['id']}"
    assert order["status"] == new_order["status"], f"Expected order status to be {new_order['status']}, but got {order['status']}"


def test_delete_order(delete_order):
    """
    Test checks the correct deletion of the order
    """
    response = requests.delete(f"{ORDER_ENDPOINT}/{delete_order['id']}")
    assert response.status_code == 200, f"Failed to delete order, status code: {response.status_code}"  

    response = requests.get(f"{ORDER_ENDPOINT}/{delete_order['id']}")
    assert response.status_code == 404, f"Expected status code 404, but got {response.status_code}"