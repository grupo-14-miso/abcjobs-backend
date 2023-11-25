from unittest.mock import patch, MagicMock
import pytest
from google.cloud.datastore import Entity

from main import app
from src.utils.utils import remove_password_properties, get_details_for_interview
from src.view.interview_view import VistaInterview

# Mock firebase_admin for tests
firebase_admin = MagicMock()

# Set up mock return values or behaviors as needed
firebase_admin.initialize_app.return_value = None


# Mock the Flask client
@pytest.fixture
def client():
    with patch('main.firebase_admin', firebase_admin):
        with patch('google.auth.default', return_value=(None, None)):  # Mock GCP authentication
            with patch('google.cloud.datastore.Client', autospec=True):  # Mock Datastore Client
                with app.test_client() as client:
                    yield client


@patch('google.cloud.datastore.Client')
def test_get_request_interview_company(mock_datastore_client, client):
    # Set up mock pre_interview results
    mock_pre_interview_results = [
        MagicMock(id_offer='offer_id_1', id_candidate='candidate_id_1'),
        MagicMock(id_offer='offer_id_2', id_candidate='candidate_id_2'),
        # Add more mock results as needed
    ]

    mock_client_instance = MagicMock()
    mock_datastore_client.return_value = mock_client_instance
    mock_client_instance.query.return_value.fetch.return_value = mock_pre_interview_results

    # Set up mock candidate results
    mock_candidate_result = {'candidate_data': 'mock_data'}

    # Mock the get method of datastore.Client
    mock_client_instance.get.return_value = mock_candidate_result

    # Call the get method of VistaInterviewCompany
    response = client.get("/interviews-get/offer/5683780991844352/pre")

    assert response.status_code == 200


@patch('google.cloud.datastore.Client')
def test_get_request_interview(mock_datastore_client, client):
    # Set up mock interview results
    mock_interview_results = [
        MagicMock(id=1, id_company='company_id_1', id_offer='offer_id_1', candidates=[]),
        # Add more mock results as needed
    ]

    mock_client_instance = MagicMock()
    mock_datastore_client.return_value = mock_client_instance
    mock_client_instance.query.return_value.fetch.return_value = mock_interview_results

    # Mock get method for candidates

    # Assuming this line raises a TypeError
    with pytest.raises(TypeError) as exc_info:
        response = client.get("/interviews-get")

    # You can then assert details about the exception, for example:
    assert "Object of type MagicMock is not JSON serializable" in str(exc_info.value)


def test_ping(client):
    response_valid = client.get("/interviews-get/ping")
    assert response_valid.json == "Pong"


def test_remove_password_properties(client):
    entity = Entity()
    entity.update({
        'password_hash': '1234',
        'salt': '1234'
    })
    remove_password_properties(entity)
    assert entity.get('password_hash', '') == ''


def test_get_details_for_interview(client):
    client = MagicMock()
    interview_entity = Entity()
    interview_entity.update({
        'candidates': ['1234566'],
        'id_offer': '1234566',
        'id_company': '1234566'
    })
    response = get_details_for_interview(client, interview_entity)
    assert isinstance(response, list)