# Swaggernauts - Conquering APIs with Postman and Pytest

## About the Project

Welcome to an epic adventure through the galaxy of APIs! Our mission: to test the universe of Swagger using the cosmic tools of Postman and Pytest.

## Goal

When Star Wars meets Postman and Pytest, there's no room for errors. We're creating intergalactic tests that will make APIs run faster than the Millennium Falcon!

## Features

- **Postman**: Our star pilot for sending and receiving messages from the API.
- **Pytest**: The Force that makes our tests as strong and reliable as Master Yoda.

## How to Run

1. **Clone the repository** - Load your spaceship with the code.
2. **Launch Postman** - Fire up the engines and start exploring the API.
3. **Unleash Pytest** - May the testing Force be with you!

## Test Structure

Our tests are organized in a way that ensures clarity and ease of use. Here's a breakdown of the structure:

- **`tests/api/`**: This is where our finest Jedi test cases are trained in the art of endpoint combat. For example, tests for the `pet` endpoint are in `tests/api/pet/` and tests for the `user` endpoint are in `tests/api/user/`. May your tests be as precise as a lightsaber strike!

- **`tests/config/`**: In this secret hangar of the Death Star, we store maps and coordinates of intergalactic endpoints. Remember, young Padawan, here you will find everything you need for your tests to travel safely through the vast expanses of code! 🌌

- **`/TestRestApi.postman_collection.json`**: Welcome to the Postman Galactic Collections, where each request is like a starship ready for a hyperspace jump! Here you’ll find our meticulously crafted blueprints for interstellar communication with the API universe.

## Example Tests

### Postman Test Example (in a Postman collection):

```json
{
	"info": {
		"_postman_id": "61159455-ffa9-4580-bc18-07c102bf890e",
		"name": "TestRestApi",
		"schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
		"_exporter_id": "36686341"
	},
	"item": [
		{
					"name": "Add pet",
					"event": [
						{
							"listen": "test",
							"script": {
								"exec": [
									"// Validate that the response code should be 200\r",
									"pm.test(\"Status code is 200\", function () {\r",
									"    pm.response.to.have.status(200);\r",
									"});\r",
									"\r",
									"const schema = {\r",
									"    \"id\": 0,\r",
									"  \"category\": {\r",
									"    \"id\": 0,\r",
									"    \"name\": \"string\"\r",
									"  },\r",
									"  \"name\": \"doggie\",\r",
									"  \"photoUrls\": [\r",
									"    \"string\"\r",
									"  ],\r",
									"  \"tags\": [\r",
									"    {\r",
									"      \"id\": 0,\r",
									"      \"name\": \"string\"\r",
									"    }\r",
									"  ],\r",
									"  \"status\": \"available\"\r",
									"}\r",
									"\r",
									"if (pm.response.code === 200){\r",
									"\t\t pm.test('Schema is valid', () => {\r",
									"     const response = pm.response.json();\r",
									"     pm.expect(response).to.have.jsonSchema(schema);\r",
									"     })\r",
									"\t}"
								],
								"type": "text/javascript",
								"packages": {}
							}
						}
					],
					"request": {
						"method": "POST",
						"header": [],
						"body": {
							"mode": "raw",
							"raw": "{\r\n  \"id\": 0,\r\n  \"category\": {\r\n    \"id\": 0,\r\n    \"name\": \"string\"\r\n  },\r\n  \"name\": \"doggie\",\r\n  \"photoUrls\": [\r\n    \"string\"\r\n  ],\r\n  \"tags\": [\r\n    {\r\n      \"id\": 0,\r\n      \"name\": \"string\"\r\n    }\r\n  ],\r\n  \"status\": \"available\"\r\n}",
							"options": {
								"raw": {
									"language": "json"
								}
							}
						},
						"url": {
							"raw": "https://petstore.swagger.io/v2/pet",
							"protocol": "https",
							"host": [
								"petstore",
								"swagger",
								"io"
							],
							"path": [
								"v2",
								"pet"
							]
						}
					},
					"response": []
				},
```

### Pytest Test Example (in `tests/api/user/test_user_happy_path.py`)

```python
def test_user_login_and_logout(base_user):
    """
    Test creates a user and checks the correct login and logout from the system
    """
    response = create_user(base_user)
    assert response.status_code == 200, f"Failed to create user, status code: {response.status_code}"
    username = base_user["username"]
    password = base_user["password"]

    login_response = requests.get(f"{ENDPOINT}/v2/user/login", params={"username": username, "password": password})
    assert login_response.status_code == 200, f"Failed to login, status code: {login_response.status_code}"   
    login_data = login_response.json()
    assert "message" in login_data, f"'message' key not found in the response data."
    assert "unknown" in login_data["type"], f"Expected message 'unknown', but got '{login_data['type']}'" 

    logout_response = requests.get(f"{ENDPOINT}/v2/user/logout")
    assert logout_response.status_code == 200, f"Failed to logout, status code: {login_response.status_code}" 
    logout_data = logout_response.json()
    assert "ok" in logout_data["message"], f"Unexpected logout message: {logout_data['message']}"

    delete_response = delete_user(base_user, username)
    assert delete_response.status_code == 200, f"Failed to delete user, status code: {response.status_code}"
```

## How to Contribute

- **Fork the repository** - Become a new recruit in our galactic mission.
- **Create pull requests** - Add your innovative tests and strengthen our forces!

## About the Author

I'm a budding programmer embarking on this interstellar journey of API testing. With a passion for learning and a drive to master the art of coding, I'm excited to contribute to the galaxy of Swaggernauts. Together, we'll explore the farthest reaches of the API universe and ensure that no bug escapes our vigilant watch.

## License

This code is as free as the Millennium Falcon in hyperspace. Use it, modify it, and share it to make the world of APIs a safer place!

**"Remember, every tested endpoint is a step closer to Jedi mastery in API testing!"**

Enjoy your project! 🚀
