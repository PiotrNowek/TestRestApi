import pytest
import requests

from config.config import ENDPOINT


def test_check_endpoint():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"


@pytest.mark.parametrize("user_data, expected_status",[
    ({},400), # empty user
    ({"id": 0, "username": 115, "lastName": "LastName1", "email": "user1@example.com", "password": "password1", "phone": "123456789", "userStatus": 0}, 400), # integer in username
    ({"id": 0, "username": "", "lastName": "", "email": "", "password": "", "phone": "", "userStatus": 0}, 400) # missing values
]) # bug - create all users


def test_create_user_with_boundary_params(user_data, expected_status):
    """
    The test checks the creation of users with boundary parameters.
    """
    response = create_user(user_data)
    assert response.status_code == expected_status, f"Expected status code 400, but got {response.status_code}"

    username = user_data["username"]
    delete_response = delete_user(username)
    assert delete_response.status_code == 200, f"Failed to delete user, status code: {delete_response.status_code}"


def test_update_user_with_boundary_param(base_user):
    """
    The test checks the update of user with boundary parameters.
    """
    response = create_user(base_user)
    assert response.status_code == 200, f"Failed to create user, status code: {response.status_code}"

    payload = {
        "id": 0,
        "username": 122,
        "firstName": "Michael",
        "lastName": "Tor",
        "email": "mike@example.com",
        "password": "password",
        "phone": "485624789",
        "userStatus": 0
    } #bug - updated user with integer username
    username = payload["username"]
    update_response = update_user(payload, username)
    assert update_response.status_code == 400, f"Expected status code 400, but got {response.status_code}"

    delete_response = delete_user(username)
    assert delete_response.status_code == 200, f"Failed to delete user, status code: {delete_response.status_code}"
    

@pytest.mark.parametrize("payload", [
    ({
        "id": 0,
        "username": 122,
        "firstName": "Michael",
        "lastName": "Tor",
        "email": "mike@example.com",
        "password": "password",
        "phone": "485624789",
        "userStatus": 0
    }),
    ({
        "id": 0,
        "username": "a",
        "firstName": "Michael",
        "lastName": "Tor",
        "email": "mike@example.com",
        "password": "password",
        "phone": "485624789",
        "userStatus": 0
    })
])


def test_delete_user_with_boundary_param(payload):
    """
    The test checks the delete of user with boundary parameters.
    """
    response = create_user(payload)
    assert response.status_code == 200, f"Failed to create user, status code: {response.status_code}"

    username = payload["username"]
    delete_response = delete_user(username)
    assert delete_response.status_code == 200, f"Failed to delete user, status code: {delete_response.status_code}"
   
    get_user_response = get_username(username)
    assert get_user_response.status_code == 404, f"Expected status code 404, but got {get_user_response.status_code}"


def test_login_with_max_length_username_and_password():
    """
    The test checks the login of user with boundary parameters.
    """
    max_length_username = "a" * 255
    max_length_password = "b" * 255
    base_user = {
        "username": max_length_username,
        "password": max_length_password,
        "email": "testuser@example.com",
        "firstName": "Test",
        "lastName": "User"
    }

    create_response = create_user(base_user)
    assert create_response.status_code == 200, f"Failed to create user, status code: {create_response.status_code}"

    login_response = requests.get(f"{ENDPOINT}/v2/user/login", params={"username": base_user["username"], "password": base_user["password"]})
    assert login_response.status_code == 200, f"Failed to login, status code: {login_response.status_code}"
    login_data = login_response.json()
    assert "message" in login_data, f"'message' key not found in the response data."
    

def create_user(base_user):
    return requests.post(f"{ENDPOINT}/v2/user", json=base_user)


def get_username(username):
    return requests.get(f"{ENDPOINT}/v2/user/{username}")


def update_user(payload, username):
    return requests.put(f"{ENDPOINT}/v2/user/{username}", json=payload)


def delete_user(username):
    return requests.delete(f"{ENDPOINT}/v2/user/{username}")