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
        response_valid = client.get("/assignments/ping")
        assert response_valid.json == "Pong"


def test_get_assignments( client):
    # Perform a GET request to /assignments
    response = client.get('/assignments')

    # Validate the response
    assert response.status_code == 200
    assert response.json == []

def test_assignments_with_firebase_mock(client):
    # Set up mock return values or behaviors for Datastore Client

    # Perform a POST request to /assignments
    data = {'rol': 'Developer', 'type': 'Test', 'focus': 'Programming', 'questions': []}
    response = client.post('/assignments', json=data)

    # Validate the response
    assert response.status_code == 201
    assert 'message' in response.json
    assert 'assignment_id' in response.json

@patch('google.cloud.pubsub_v1.PublisherClient', autospec=True, return_value=pubsub_client)
@patch('google.auth.default', return_value=(None, None))
@patch('src.main.firebase_admin', firebase_admin)
def test_assignments_with_pubsub_mock(mock_firebase_admin, mock_auth_default, mock_pubsub_client, client):
    # Set up mock return values or behaviors for Datastore Client

    # Perform a POST request to /assignments
    data =  {
                "answers": [
                    {
                        "a": "A list is mutable, while a tuple is immutable."
                    },
                    {
                        "b": "A list can contain any type of data, while a tuple can only contain primitive data types."
                    },
                    {
                        "c": "A list is used to store a collection of items, while a tuple is used to store a fixed-size collection of items."
                    },
                    {
                        "d": "All of the above"
                    }
                ],
                "correct_answer": [
                    "d"
                ],
                "selected_answer": [
                    "d"
                ],
                "description": "What is the difference between a list and a tuple in Python?"
            } 
    response = client.post('/assignments/123', json=data)

    # Validate the response
    assert response.status_code == 201
    assert 'message' in response.json
    print(response.json)

