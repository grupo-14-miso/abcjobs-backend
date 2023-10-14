import pytest
from unittest.mock import MagicMock

@pytest.fixture
def app():
    # You can create a placeholder for the app or modify as needed
    app_mock = MagicMock()
    return app_mock

@pytest.fixture()
def client(app):
    return app.test_client()