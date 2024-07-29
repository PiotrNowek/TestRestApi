import pytest
import requests

from config.config import ENDPOINT


# def test_check_endpoint():
#     response = requests.get(ENDPOINT)
#     assert response.status_code == 200, f"Failed to create order, status code: {response.status_code}"


def test_create_user_boundary():
    pass






def create_user(payload):
    return requests.post(f"{ENDPOINT}/v2/user", json=payload)


def get_username(username):
    return requests.get(f"{ENDPOINT}/v2/user/{username}")


def update_user(payload, username):
    return requests.put(f"{ENDPOINT}/v2/user/{username}", json=payload)


def delete_user(payload, username):
    return requests.delete(f"{ENDPOINT}/v2/user/{username}", json=payload)