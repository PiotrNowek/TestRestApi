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