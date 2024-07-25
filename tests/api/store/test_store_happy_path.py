import pytest
import requests

from config.config import ENDPOINT, ORDER_ENDPOINT


def test_check_endpoint():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200


def test_get_pet_list_by_status():
    response = requests.get(f"{ENDPOINT}/v2/store/inventory")
    assert response.status_code == 200, f"Failed to create list, status code: {response.status_code}"
    assert response.headers['Content-Type'] == 'application/json', f"Expected application/json but got {response.headers['Content-Type']}"
    try:
        response = response.json()
    except ValueError:
        assert False, "Response is not in JSON format"
    assert isinstance(response, dict), "Expected response to be a dictionary"

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


def test_create_order(new_order):
    assert new_order["id"] is not None
    assert new_order["status"] == "placed"
    assert new_order["complete"] == True


def test_get_order_by_id(new_order):
    response = requests.get(f"{ORDER_ENDPOINT}/{new_order['id']}")
    assert response.status_code == 200, f"Failed to find order, status code: {response.status_code}"
    order = response.json()
    assert order["id"] == new_order["id"]
    assert order["status"] == new_order["status"] 


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


def test_delete_order(delete_order):
    response = requests.delete(f"{ORDER_ENDPOINT}/{delete_order['id']}")
    assert response.status_code == 200, f"Failed to delete order, status code: {response.status_code}"  

    response = requests.get(f"{ORDER_ENDPOINT}/{delete_order['id']}")
    assert response.status_code == 404, f"Expected status code 404, but got {response.status_code}"