import pytest
import requests

from config.config import ENDPOINT


# def test_check_endpoint():
#     response = requests.get(ENDPOINT)
#     assert response.status_code == 200


# @pytest.mark.parametrize("user_data, expected_status", [
#    ({"id": 0, "username": "Bambo", "lastName": "LastName1", "email": "user1@example.com", "password": "password1", "phone": "123456789", "userStatus": 0},400), #missing firstName, 200
#    ({"id": 0, "username": "Rambo", "firstName": "FirstName1", "lastName": "LastName1", "password": "password1", "phone": "123456789", "userStatus": 0},400), #missing email, 200
#    ({"id": -1, "username": "Mambo", "firstName": "FirstName1", "lastName": "LastName1", "email": "user1@example.com", "password": "password1", "phone": "123456789", "userStatus": 0},400), #negative id, 200
#    ({"id": "", "username": "Tambo", "firstName": "FirstName1", "lastName": "LastName1", "email": "user1@example.com", "password": "password1", "phone": "123456789", "userStatus": 0},400), # empty id, 200
#    ({"id": "invalid", "username": "Jambo", "firstName": "FirstName1", "lastName": "LastName1", "email": "user1@example.com", "password": "password1", "phone": "123456789", "userStatus": 0},400), #invalid id, 500 
# ])


# def test_create_user_with_invalid_params(user_data, expected_status):
#     response = create_user(user_data)
#     assert response.status_code == expected_status, f"Expected status code {expected_status} but got {response.status_code}" 


@pytest.mark.parametrize("username, expected_status", [
({"username": ""},400), 
({"username": "Bambo" * 100},400),
({},404)    
])


def test_get_user_by_id(username, expected_status):
    response = create_user(username)
    assert response.status_code == 200, f"Failed to create user, status code: {response.status_code}"

    get_user_response = get_username()
    assert get_user_response.status_code == expected_status, f"Expected status code {expected_status} but got {get_user_response.status_code}"







def get_username(username):
    return requests.get(f"{ENDPOINT}/v2/user/{username}")


def create_user(base_user):
    return requests.post(f"{ENDPOINT}/v2/user", json=base_user)


def update_user(payload, username):
    return requests.put(f"{ENDPOINT}/v2/user/{username}", json=payload)


def delete_user(payload, username):
    return requests.delete(f"{ENDPOINT}/v2/user/{username}", json=payload)