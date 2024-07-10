import requests


ENDPOINT = "https://petstore.swagger.io/v2/pet/findByStatus?status=pending"


def test_check_endpoint():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200
    pass


