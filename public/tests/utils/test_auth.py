from src.utils.auth import get_entity_by_email
from src.utils.persistence import persist_new_candidate
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


def test_get_entity_by_email(client):
    response = get_entity_by_email('entity','email')
    assert response is None

