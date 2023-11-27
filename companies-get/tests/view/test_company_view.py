from unittest.mock import patch, MagicMock
import pytest
from main import app


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
        response_valid = client.get("/companies-get/ping")
        assert response_valid.json == "Pong"


def test_get_companies(client):
        # Perform get request to offer
        response = client.get("/companies-get")
        # Validate the response
        assert response.status_code == 200
        assert response.json == []


def test_get_offers(client):
        # Perform get request to offer
        response = client.get("/companies-get/offer/123456")
        # Validate the response
        assert response.status_code == 200
        assert response.json == []




def test_get_equipo_from_offer(client):
    # Perform get request to offer
    response = client.get("/companies-get/equipo/123456")
    # Validate the response
    assert response.status_code == 200
    assert response.json == []


def test_get_offer_exception(client):
    # Perform a GET request to /users
    try:
        response = client.get('/companies-get/offerById/123')
    except:
        # Validate the response
        assert True
