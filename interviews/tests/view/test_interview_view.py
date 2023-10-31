from unittest.mock import patch, MagicMock, Mock
import pytest
from main import app

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
def test_request_pre_onterview(mock_datastore_client, client ):

        mock_client_instance = Mock()
        mock_datastore_client.return_value = mock_client_instance
        mock_client_instance.put.return_value = None  # You can customize the return value if needed

        # Prepare test data
        test_data = {
            'id_company': 'company_id',
            'id_offer': 'offer_id',
            'id_candidate': 'candidate_id'
        }

        response = client.post("/interviews/pre-candidate", json=test_data)
        assert response.status_code == 200



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
    response = client.get("/interviews/offer/5683780991844352/pre")

    assert response.status_code == 200


@patch('google.cloud.datastore.Client')
def test_post_request_interview(mock_datastore_client, client):
    mock_client_instance = Mock()
    mock_datastore_client.return_value = mock_client_instance
    mock_client_instance.put.return_value = None  # You can customize the return value if needed

    # Prepare test data
    test_data = {
        'id_company': 'company_id',
        'id_offer': 'offer_id',
        'candidates': ['candidate_id_1', 'candidate_id_2'],
        'link': 'http://example.com',
        'date': '21/04/2023 14:00',
        'description': 'Entrevista miso',
    }

    # Set up mock pre_interview results
    mock_pre_interview_results = [
        MagicMock(id_offer='offer_id_1', id_candidate='candidate_id_1'),
        MagicMock(id_offer='offer_id_2', id_candidate='candidate_id_2'),
        # Add more mock results as needed
    ]

    mock_client_instance.query.return_value.fetch.return_value = mock_pre_interview_results


    response = client.post("/interview", json=test_data)

    # Assertions
    assert response.status_code == 200

def test_ping(client):
        response_valid = client.get("/interviews/ping")
        assert response_valid.json == "Pong"
