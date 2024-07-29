import pytest
import requests

from config.config import ENDPOINT


def test_check_endpoint():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200


@pytest.mark.parametrize("user_data, expected_status", [
   ({"id": 0, "username": "Bambo", "lastName": "LastName1", "email": "user1@example.com", "password": "password1", "phone": "123456789", "userStatus": 0},400), #missing firstName, 200
   ({"id": 0, "username": "Rambo", "firstName": "FirstName1", "lastName": "LastName1", "password": "password1", "phone": "123456789", "userStatus": 0},400), #missing email, 200
   ({"id": -1, "username": "Mambo", "firstName": "FirstName1", "lastName": "LastName1", "email": "user1@example.com", "password": "password1", "phone": "123456789", "userStatus": 0},400), #negative id, 200
   ({"id": "", "username": "Tambo", "firstName": "FirstName1", "lastName": "LastName1", "email": "user1@example.com", "password": "password1", "phone": "123456789", "userStatus": 0},400), # empty id, 200
   ({"id": "invalid", "username": "Jambo", "firstName": "FirstName1", "lastName": "LastName1", "email": "user1@example.com", "password": "password1", "phone": "123456789", "userStatus": 0},400), #invalid id, 500 
])


def test_create_user_with_invalid_params(user_data, expected_status):
    response = create_user(user_data)
    assert response.status_code == expected_status, f"Expected status code {expected_status} but got {response.status_code}" 

    username = user_data["username"]
    delete_response = delete_user(username)
    assert delete_response.status_code == 200, f"Failed to delete user, status code: {delete_response.status_code}"


@pytest.mark.parametrize("username, expected_status", [
({"username": ""},404), 
({"username": "Bambo" * 100},404),
({},404)    
])


def test_get_user_by_id(username, expected_status):
    get_user_response = get_username(username)
    assert get_user_response.status_code == expected_status, f"Expected status code {expected_status} but got {get_user_response.status_code}"
    

@pytest.mark.parametrize("username, expected_status",[
    ({"username": "Rambo" * 100}, 400),
    ({"username": ""}, 400)
])


def test_update_user(base_user, username, expected_status):
    response = create_user(base_user)
    assert response.status_code == 200, f"Failed to create user, status code: {response.status_code}"

    update_response = update_user(username, expected_status)
    assert update_response == expected_status, f"Expected status code {expected_status} but got {update_response.status_code}"

    delete_response = delete_user(username)
    assert delete_response.status_code == 200, f"Failed to delete user, status code: {delete_response.status_code}"


@pytest.mark.parametrize("username",[
    ({"username": "Rambo" * 100}),
    ({"username": ""})
])


def test_delete_user(username):
    response = delete_user(username)
    assert response.status_code == 404, f"Expected status code 404, but got {response.status_code}"


@pytest.mark.parametrize("username, password, expected_status", [
    ("nonexistent_user", "password1", 400),  
    ("user1", "wrong_password", 400),  
    ("", "password1", 400),  
    ("user1", "", 400),  
]) #bug - logs all cases

def test_login_user_negative(username, password, expected_status):
    response = requests.get(f"{ENDPOINT}/v2/user/login", params={"username": username, "password": password})
    assert response.status_code == expected_status, f"Expected status code {expected_status}, but got {response.status_code}"
    

def get_username(username):
    return requests.get(f"{ENDPOINT}/v2/user/{username}")


def create_user(base_user):
    return requests.post(f"{ENDPOINT}/v2/user", json=base_user)


def update_user(payload, username):
    return requests.put(f"{ENDPOINT}/v2/user/{username}", json=payload)


def delete_user(username):
    return requests.delete(f"{ENDPOINT}/v2/user/{username}")