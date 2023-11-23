from unittest.mock import patch, MagicMock
import pytest
from src.main import app

# Mock firebase_admin for tests
firebase_admin = MagicMock()

# Set up mock return values or behaviors as needed
firebase_admin.initialize_app.return_value = None
firebase_admin.db.reference.return_value.get.return_value = [
        {
                "assignment_id": 5352686694170624,
                "focus": "Java"
        },
        {
                "assignment_id": 5352686694170624,
                "focus": "Java"
        }
]

assignment_data_mock = {
    'candidate': 'mocked_candidate_key',
    'other_data': 'mocked_other_data'
}

# Mock the Pub/Sub client
pubsub_client = MagicMock()

@pytest.fixture
def mock_pubsub_client():
    return MagicMock()

# Mock the Flask client
@pytest.fixture
def client():
    with patch('src.main.firebase_admin', firebase_admin):
        with patch('google.auth.default', return_value=(None, None)):  # Mock GCP authentication
            with patch('google.cloud.datastore.Client', autospec=True):  # Mock Datastore Client
                    with app.test_client() as client:
                        yield client



def test_ping(client):
        response_valid = client.get("/assignments-get/ping")
        assert response_valid.json == "Pong"


def test_get_assignments( client):
    # Perform a GET request to /assignments
    response = client.get('/assignments-get?status=tsts&type=hdhdh')

    # Validate the response
    assert response.status_code == 200
    assert response.json == []



@pytest.fixture
def mock_datastore_client():
    with patch('google.cloud.datastore.Client') as mock_client:
        mock_instance = mock_client.return_value
        mock_instance.get.return_value = assignment_data_mock
        yield mock_instance


def test_assignment_perfomance_test(client, mock_datastore_client):
    # Perform a POST request to /assignment_template_candidate

    response = client.get('assignments-get/company/5726177821982720')

    # Validate the response
    assert response.status_code == 200

def test_assignment_by_candidate_test(client, mock_datastore_client):
    # Perform a POST request to /assignment_template_candidate

    response = client.get('assignments-get/candidate/5705491514654720?status=finished')

    # Validate the response
    assert response.status_code == 200


