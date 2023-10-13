import json
from unittest.mock import patch, MagicMock
import pytest
from users import app


# Mock firebase_admin for tests
firebase_admin = MagicMock()

# Set up mock return values or behaviors as needed
firebase_admin.initialize_app.return_value = None
firebase_admin.db.reference.return_value.get.return_value = {
    'user1': {'name': 'John', 'type': 'Developer'},
    'user2': {'name': 'Alice', 'type': 'Designer'},
    'user3': {'name': 'John', 'type': 'Tester'},
}

# Use the mock in the tests
with patch('src.view.user_view.firebase_admin', firebase_admin):
    def test_ping(client):
        response_valid = client.get("/users/ping")
        assert response_valid.json == "Pong"

    def test_user_profile(client):
        # Mock the Firebase Admin query results
        query_results = {
            'user1': {'name': 'John', 'type': 'Developer'},
            'user2': {'name': 'Alice', 'type': 'Designer'},
            'user3': {'name': 'John', 'type': 'Tester'},
        }

        # Set the return value for the get method
        firebase_admin.db.reference.return_value.get.return_value = query_results

        # Perform a GET request to /users/profiles
        response = client.get('/users/profiles')

        # Validate the response
        assert response.status_code == 200
        expected_response = [
            [{'name': 'John', 'type': 'Developer'}, {'name': 'Alice', 'type': 'Designer'}, {'name': 'John', 'type': 'Tester'}]
        ]
        assert json.loads(response.data) == expected_response

    def test_create_profile(client):
        # Perform a POST request to /users/profiles
        data = {'name': 'NewUser', 'type': 'NewType'}
        response = client.post('/users/profiles', json=data)

        # Validate the response
        assert response.status_code == 201
        assert 'message' in response.json
        assert 'profile_id' in response.json

    def test_ping(client):
        response_valid = client.get("/users/ping")
        assert response_valid.json == "Pong"
