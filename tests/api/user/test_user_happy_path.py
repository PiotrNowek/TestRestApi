import pytest
import requests

from config.config import ENDPOINT
from conftest import created_users


def test_check_endpoint():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"


@pytest.mark.parametrize("payload", [
    ([{
        "id": 0,
        "username": "user1",
        "firstName": "FirstName1",
        "lastName": "LastName1",
        "email": "user1@example.com",
        "password": "password1",
        "phone": "123456789",
        "userStatus": 0
    }]),
    ([{
        "id": 1,
        "username": "user2",
        "firstName": "FirstName2",
        "lastName": "LastName2",
        "email": "user2@example.com",
        "password": "password2",
        "phone": "987654321",
        "userStatus": 1
    }]),
    ([{
        "id": 2,
        "username": "user3",
        "firstName": "FirstName3",
        "lastName": "LastName3",
        "email": "user3@example.com",
        "password": "password3",
        "phone": "111222333",
        "userStatus": 2
    }])
])


def test_get_user_with_list(payload):
    """
    Test creating a list of users and verifying the response.
    """
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(f"{ENDPOINT}/v2/user/createWithList", json=payload, headers=headers)
    assert response.status_code == 200, f"Failed to create list, status code: {response.status_code}"
    assert response.headers['Content-Type'] == 'application/json', f"Expected application/json but got {response.headers['Content-Type']}"
    try:
        response = response.json()
    except ValueError:
        assert False, f"Response is not in JSON format"
    assert isinstance(response, dict), f"Expected response to be a dictionary"


@pytest.mark.parametrize("payload", [
    ({
        "id": 0,
        "username": "Johnny",
        "firstName": "FirstName1",
        "lastName": "LastName1",
        "email": "user1@example.com",
        "password": "password1",
        "phone": "123456789",
        "userStatus": 0
    }),
    ({
        "id": 0,
        "username": "Tommy",
        "firstName": "FirstName2",
        "lastName": "LastName2",
        "email": "user2@example.com",
        "password": "password2",
        "phone": "123452229",
        "userStatus": 0
    })
])


def test_create_new_user(payload):
    """
    Test creating a users and verifying the response.
    """
    response = create_user(payload)
    assert response.status_code == 200, f"Failed to create user, status code: {response.status_code}"
    username = payload["username"]
    created_users.append(username)

    response_username = get_username(username)
    assert response_username.status_code == 200, f"Failed to get username, status code: {response.status_code}"
    second_data = response_username.json()
    assert second_data["username"] == username, f"Expected {second_data ['username']} to be equal username"
    assert second_data["email"] == payload["email"], f"Expected email to be {payload['email']}, but got {second_data['email']}."
    assert second_data["phone"] == payload["phone"], f"Expected email to be {payload['phone']}, but got {second_data['phone']}."

    
def test_update_user(base_user):
    """
    Test creata a user, update a user and verifying the response.
    """
    response = create_user(base_user)
    assert response.status_code == 200, f"Failed to create user, status code: {response.status_code}"
    base_username = base_user["username"]
    created_users.append(base_username)

    payload = {
        "id": 0,
        "username": "Mike",
        "firstName": "Michale",
        "lastName": "Tyson",
        "email": "mike@example.com",
        "password": "strong password",
        "phone": "485624789",
        "userStatus": 0
    }
    username = payload["username"]
    update_response = update_user(payload, username)
    assert update_response.status_code == 200, f"Failed to update user, status code: {response.status_code}"

    response_username = get_username(username)
    assert response_username.status_code == 200, f"Failed to get username, status code: {response.status_code}"
    data = response_username.json()
    assert data["username"] == payload["username"], f"Expected username to be {payload['username']}, but got {data['username']}."
    assert data["lastName"] == payload["lastName"], f"Expected username to be {payload['lastName']}, but got {data['lastName']}."
    assert data["password"] == payload["password"], f"Expected username to be {payload['password']}, but got {data['password']}."


def test_delete_user(base_user):
    """
    Test creata a user, delete a user and verifying the response.
    """
    response = create_user(base_user)
    assert response.status_code == 200, f"Failed to create user, status code: {response.status_code}"
    username = base_user["username"]
    created_users.append(username)
    
    delete_response = delete_user(base_user, username)
    assert delete_response.status_code == 200, f"Failed to delete user, status code: {response.status_code}"

    response_username = get_username(username)
    assert response_username.status_code == 404, f"Expected status code 404, but got {response.status_code}"


def test_user_login_and_logout(base_user):
    """
    Test creates a user and checks the correct login and logout from the system
    """
    response = create_user(base_user)
    assert response.status_code == 200, f"Failed to create user, status code: {response.status_code}"
    username = base_user["username"]
    password = base_user["password"]
    created_users.append(username)

    login_response = requests.get(f"{ENDPOINT}/v2/user/login", params={"username": username, "password": password})
    assert login_response.status_code == 200, f"Failed to login, status code: {login_response.status_code}"   
    login_data = login_response.json()
    assert "message" in login_data, f"'message' key not found in the response data."
    assert "unknown" in login_data["type"], f"Expected message 'unknown', but got '{login_data['type']}'" 

    logout_response = requests.get(f"{ENDPOINT}/v2/user/logout")
    logout_response.status_code == 200, f"Failed to logout, status code: {login_response.status_code}" 
    logout_data = logout_response.json()
    assert "ok" in logout_data["message"], f"Unexpected logout message: {logout_data['message']}"

    
@pytest.mark.parametrize("payload", [
    ([{
        "id": 0,
        "username": "user1",
        "firstName": "FirstName1",
        "lastName": "LastName1",
        "email": "user1@example.com",
        "password": "password1",
        "phone": "123456789",
        "userStatus": 0
    }]),
    ([{
        "id": 1,
        "username": "user2",
        "firstName": "FirstName2",
        "lastName": "LastName2",
        "email": "user2@example.com",
        "password": "password2",
        "phone": "987654321",
        "userStatus": 1
    }]),
    ([{
        "id": 2,
        "username": "user3",
        "firstName": "FirstName3",
        "lastName": "LastName3",
        "email": "user3@example.com",
        "password": "password3",
        "phone": "111222333",
        "userStatus": 2
    }])
])


def test_get_user_with_array(payload):
    """
    Test creating a list of users and verifying the response.
    """
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(f"{ENDPOINT}/v2/user/createWithArray", json=payload, headers=headers)
    assert response.status_code == 200, f"Failed to create list, status code: {response.status_code}"
    assert response.headers['Content-Type'] == 'application/json', f"Expected application/json but got {response.headers['Content-Type']}"
    try:
        response = response.json()
    except ValueError:
        assert False, f"Response is not in JSON format"
    assert isinstance(response, dict), f"Expected response to be a dictionary"


def create_user(payload):
    return requests.post(f"{ENDPOINT}/v2/user", json=payload)


def get_username(username):
    return requests.get(f"{ENDPOINT}/v2/user/{username}")


def update_user(payload, username):
    return requests.put(f"{ENDPOINT}/v2/user/{username}", json=payload)


def delete_user(payload, username):
    return requests.delete(f"{ENDPOINT}/v2/user/{username}", json=payload)