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

def test_post_company(client):
    data = {
        "document_type":"NIT",
        "document_number":"2343255",
        "name":"CEMENTOS LECHOSA SAS",
        "phone_number":"3125553124",
        "country":"Colombia",
        "email":"cechosa.rrhh@cementos.com"
    }
    response = client.post('/companies', json=data)
    # Validate the response
    assert response.status_code == 201


def test_post_offer(client):
    data = {
        "company_id": "5726966351134720",
        "name":"CEMENTOS TI FASE 2",
        "description":"Transformación digital del área de ventas",
        "start_date":"2022-06-30",
        "end_date":"2024-06-30"
    }
    response = client.post('/companies/offer', json=data)
    # Validate the response
    assert response.status_code == 201
