from unittest.mock import patch, MagicMock
import pytest
from main import app
from src.view.public_user_view import VistaLogIn

# Mock firebase_admin for tests
firebase_admin = MagicMock()
firebase_admin.initialize_app.return_value = None


@pytest.fixture
def client():
    with patch('main.firebase_admin', firebase_admin):
        with patch('google.auth.default', return_value=(None, None)):  # Mock GCP authentication
            with patch('google.cloud.datastore.Client', autospec=True):  # Mock Datastore Client
                with app.test_client() as client:
                    yield client


def test_ping(client):
    response_valid = client.get("/public/ping")
    assert response_valid.json == "Pong"


def test_register(client):
    data = {
        "username": "garayurbina",
        "email": "jose@bowser.com",
        "password": "chocoB0wser",
        "role": "Admin"
    }
    response = client.post("/public/register", json=data)
    # Validate the response
    assert response.status_code == 201


@patch('google.cloud.datastore.Client')
def test_login_not_found(mock_datastore_client, client):
    mock_user_results = [
        {'salt': 'some_salt', 'password_hash': 'some_hash', 'user_id': 'some_user_id', 'role': 'some_role',
         'first_name': 'John', 'last_name': 'Doe'}]
    mock_client_instance = MagicMock()
    mock_datastore_client.return_value = mock_client_instance

    # Mock the get method of datastore.Client
    mock_client_instance.query.return_value.fetch.return_value = mock_user_results
    data = {
        "username": "garayurbina",
        "password": "chocoB0wser"
    }
    response = client.post("/public/login", json=data)
    # Validate the response
    assert response.status_code == 404



def test_post_failed_400(client):
    # Mocking request.json
    mock_request_json = {'username': 'some_username', 'password': 'some_password'}

    # Creating an instance of the class
    your_instance = VistaLogIn()

    # Mocking the request object
    your_instance.request = MagicMock()
    your_instance.request.json = mock_request_json

    response, status_code = your_instance.post()

    # Assertions
    assert status_code == 400
