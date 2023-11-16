import pytest
from main import app as main_app

@pytest.fixture
def app():
    # You can create a placeholder for the app or modify as needed
    app_mock = main_app
    return app_mock

@pytest.fixture()
def client(app):
    return app.test_client()