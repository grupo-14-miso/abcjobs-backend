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



def test_ping(client):
        response_valid = client.get("/interviews/ping")
        assert response_valid.json == "Pong"
