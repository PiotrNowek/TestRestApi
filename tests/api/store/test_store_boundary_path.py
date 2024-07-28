import pytest
import requests

from config.config import ENDPOINT


def test_check_endpoint():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200, f"Failed to create order, status code: {response.status_code}"


@pytest.mark.parametrize("url, expected_status", [
    (f"{ENDPOINT}/v2/store/order/", 405)
])

def test_delete_order_with_no_id(url, expected_status):
    response = requests.delete(url)
    assert response.status_code == expected_status, f"Expected status code {expected_status} but got {response.status_code}"


@pytest.mark.parametrize("order_id, expected_status", [
    (-1, 404)
])

def test_delete_negative_id(order_id, expected_status):
    response = requests.delete(f"{ENDPOINT}/v2/store/order/{order_id}")
    assert response.status_code == expected_status, f"Expected status code {expected_status} but got {response.status_code}"


@pytest.mark.parametrize("payload, expected_status", [
    ({"id": 1, "petId": 1, "quantity": 1, "shipDate": 1, "status": "placed", "complete": True}, 400),
    ({"id": 1, "petId": 1, "quantity": 1, "shipDate": "2024-07-18T09:10:32.000Z", "status": "placed"*100, "complete": True}, 400),
    ({"id": 1, "petId": 1, "quantity": -1, "shipDate": "2024-07-18T09:10:32.000Z", "status": "placed", "complete": True}, 400)
]) # 3 testy kod 200

def test_create_boundary_order(create_order_url, payload, expected_status):
    response = requests.post(create_order_url, json=payload)
    assert response.status_code == expected_status, f"Expected status code {expected_status} but got {response.status_code}"


@pytest.mark.parametrize("order_id, expected_status", [
    ("a" * 128, 404),
    ("@#$%^&*", 404),
    ("", 405)
])

def test_get_order_by_boundary_id(create_order_url, order_id, expected_status):
    response = requests.get(f"{create_order_url}/{order_id}")
    assert response.status_code == expected_status, f"Expected status code {expected_status} but got {response.status_code}" 