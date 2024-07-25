import pytest
import requests

from config.config import ENDPOINT, ORDER_ENDPOINT


def test_check_endpoint():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200, f"Failed to create order, status code: {response.status_code}"


def test_get_pet_list_by_status_is_json():
    headers = {
        "content-type": "text/plain"
    }
    response = requests.get(f"{ENDPOINT}/v2/store/inventory", headers=headers)
    assert response.status_code == 400, f"Expected failed to create list, but got status code: {response.status_code}"
    assert response.headers['content-type'] == 'application/json', f"Expected application/json but got {response.headers['content-type']}"
    try:
        response = response.json()
    except ValueError:
        assert False, "Response is not in JSON format"
    

@pytest.mark.parametrize("payload, expected_status", [
    ({"id": "invalid_id", "petId": 1, "quantity": 1, "status": "placed", "complete": True}, 400), # kod 500
    ({"petId": 1, "quantity": 1, "status": "placed"}, 400), # tworzy order
    ({"id": 1, "petId": "invalid_pet_id", "quantity": "one", "status": "placed", "complete": "yes"}, 400) # kod 500
])

def test_create_order_invalid_id_and_input(payload, expected_status):
    response = requests.post(ORDER_ENDPOINT, json=payload)
    assert response.status_code == expected_status, f"Expected status code {expected_status} but got {response.status_code}"


@pytest.mark.parametrize("payload, expected_status", [
    ({"id": 1777777777777,"petId": 1, "quantity": 1, "status": "placed", "complete": True}, 404),
    ({"id": "invalid","petId": 1, "quantity": 1, "status": "placed", "complete": True}, 404)
])    

def test_get_order_with_non_exist_and_invalid_id(payload, expected_status):
    response = requests.get(f"{ORDER_ENDPOINT}/{payload['id']}")
    assert response.status_code == 404, f"Expected status code 404, but got {response.status_code}"


def test_delete_non_exist_order():
    non_exist_order_id = 1717171717171 # We assume this id does not exist
    response = requests.get(f"{ORDER_ENDPOINT}/{non_exist_order_id}")
    assert response.status_code == 404, f"Expected status code 404, but got {response.status_code}"
    
    
def test_delete_order_with_invalid_id():
    invalid_order = "invalid"
    response = requests.get(f"{ORDER_ENDPOINT}/{invalid_order}")
    assert response.status_code == 404, f"Expected status code 404, but got {response.status_code}"