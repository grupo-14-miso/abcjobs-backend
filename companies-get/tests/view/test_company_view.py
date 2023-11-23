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
        response_valid = client.get("/companies/ping")
        assert response_valid.json == "Pong"


def test_get_companies(client):
        # Perform get request to offer
        response = client.get("/companies")
        # Validate the response
        assert response.status_code == 200
        assert response.json == []


def test_get_offers(client):
        # Perform get request to offer
        response = client.get("/companies/offer/123456")
        # Validate the response
        assert response.status_code == 200
        assert response.json == []




def test_get_equipo_from_offer(client):
    # Perform get request to offer
    response = client.get("/companies/equipo/123456")
    # Validate the response
    assert response.status_code == 200
    assert response.json == []
