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
        response_valid = client.get("/assignments/ping")
        assert response_valid.json == "Pong"


def test_get_assignments( client):
    # Perform a GET request to /assignments
    response = client.get('/assignments?status=tsts&type=hdhdh')

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

@patch('google.cloud.datastore.Client')
def test_questionnaire_view(mock_firestore_client, client):
    # Mock Firestore client
    firestore_client = mock_firestore_client.return_value
    mocked_entity = MagicMock()
    mocked_entity.get.return_value = [{"created_timestamp":"2023-10-19T02:16:49.503418","description":"What is the difference between a list and a tuple in Python?","answers":[{"a":"A list is mutable, while a tuple is immutable."},{"b":"A list can contain any type of data, while a tuple can only contain primitive data types."},{"c":"A list is used to store a collection of items, while a tuple is used to store a fixed-size collection of items."},{"d":"All of the above"}],"correct_answer":["a"],"selected_answer":["d"],"assignment_id":"5714489739575296"},{"created_timestamp":"2023-10-19T02:16:49.503418","description":"What is the difference between a list and a tuple in Python?","answers":[{"a":"A list is mutable, while a tuple is immutable."},{"b":"A list can contain any type of data, while a tuple can only contain primitive data types."},{"c":"A list is used to store a collection of items, while a tuple is used to store a fixed-size collection of items."},{"d":"All of the above"}],"correct_answer":["d"],"selected_answer":["d"],"assignment_id":"5714489739575296"}]
    firestore_client.get.return_value = mocked_entity

    # Perform the request to the endpoint
    response = client.post('/assignments/questionnaire/123')

    # Validate the response
    assert response.status_code == 201
    assert 'message' in response.json

@patch('google.cloud.datastore.Client')
def test_update_assignment_with_question(mock_firestore_client, client):

    # Mock Firestore client
    firestore_client = mock_firestore_client.return_value
    mocked_entity = MagicMock()
    mocked_entity.get.return_value = {
        "assignment_id": 123,
        "focus": "Java",
        "questions": [{
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
                "description": "What is the difference between a list and a tuple in Python?"
            }],
        "result": 22.22222222222222,
        "rol": "Developer",
        "status": "to_do",
        "type": "Technical"
    }

    firestore_client.get.return_value = mocked_entity

    data = {
        "assignment_id": "123",
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
        "description": "What is the difference between a list and a tuple in Python?",
        "created_timestamp": "2023-10-19T02:16:49.503418"
    }
    response = client.put('/assignments', json=data)
    # Validate the response
    assert response.status_code == 201
    assert 'message' in response.json
    print(response.json)


@pytest.fixture
def mock_datastore_client():
    with patch('google.cloud.datastore.Client') as mock_client:
        mock_instance = mock_client.return_value
        mock_instance.get.return_value = assignment_data_mock
        yield mock_instance


def test_assignment_template_candidate_post(client, mock_datastore_client):
    # Perform a POST request to /assignment_template_candidate

    response = client.post('/assignments/candidate/123/some_candidate_key')

    # Validate the response
    assert response.status_code == 200

def test_assignment_perfomance_test(client, mock_datastore_client):
    # Perform a POST request to /assignment_template_candidate

    response = client.get('assignments/company/5726177821982720')

    # Validate the response
    assert response.status_code == 200

def test_assignment_by_candidate_test(client, mock_datastore_client):
    # Perform a POST request to /assignment_template_candidate

    response = client.get('assignments/candidate/5705491514654720?status=finished')

    # Validate the response
    assert response.status_code == 200


