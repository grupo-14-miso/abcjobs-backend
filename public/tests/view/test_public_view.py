from unittest.mock import patch, MagicMock
import pytest
from main import app
from src.utils.utils import hash_new_password
from src.view.public_user_view import VistaLogIn

# Mock firebase_admin for tests
firebase_admin = MagicMock()
firebase_admin.initialize_app.return_value = None
salt, pw_hash = hash_new_password('chocoB0wser')


@pytest.fixture
def client():
    with patch('main.firebase_admin', firebase_admin):
        with patch('google.auth.default', return_value=(None, None)):  # Mock GCP authentication
            with patch('google.cloud.datastore.Client', autospec=True):  # Mock Datastore Client
                with patch('src.utils.auth.get_entity_by_email',
                           return_value={'salt': salt, 'password_hash': pw_hash, 'first_name': '1', 'last_name': '2',
                                         'name': '3', 'Nombre': '1', 'apellido': '2'}):
                    with app.test_client() as client:
                        yield client


def test_ping(client):
    response_valid = client.get("/public/ping")
    assert response_valid.json == "Pong"


def test_register(client):
    data = {
        "username": "garayurbina",
        "email": "jose@bowser.com",
        "password": "chocoB0wser",
        "role": "Admin"
    }
    response = client.post("/public/register", json=data)
    # Validate the response
    assert response.status_code == 201


def test_register_candidate(client):
    data = {
        "email": "josegaray@gmail.com",
        "password": "joselusigaray",
        "role": "Candidate",
        "Nombre": "Jose",
        "apellido": "Garay",
        "segundo_nombre": "Luis",
        "segundo_apellido": "Garay",
        "tipo_documento": "CC",
        "documento": "3143145315",
        "fecha_nacimiento": "01-12-1994",
        "genero": "masuculino",
        "nacionalidad": "nacionalidad",
        "estado_civil": "soltero",
        "telefono": "273635363",
        "pais_nacimiento": "Colombia",
        "pais_residencia": "Colombia",
        "ciudad_nacimiento": "Bucaramanga",
        "rol": [
            "Architect",
            "Devops"
        ],
        "lenguajes_programacion": [
            "java",
            "nodjs",
            "typescript"
        ],
        "tecnologias_herramientas": [
            "slack",
            "intellij",
            "linux"
        ],
        "soft_skill": [
            "comunicador",
            "lider",
            "puntual",
            "mejor"
        ],
        "ciudad_residencia": "Ibague",
        "educacion": [
            {
                "nivel_academico": "",
                "institucion": "",
                "titulo_obtenido": "",
                "fecha_inicio": "",
                "fecha_fin": "",
                "rol": "Architect",
                "lenguajes_programacion": [
                    "java",
                    "nodjs",
                    "typescript"
                ],
                "tecnologias_herramientas": [
                    "slack",
                    "intellij",
                    "linux"
                ]
            }
        ],
        "experiencia": [
            {
                "empresa": "",
                "pais": "",
                "ciudad": "",
                "cargo": "",
                "rol": "",
                "fecha_inicio": "",
                "fecha_fin": ""
            }
        ],
        "idiomas": [
            {
                "idioma": "ingles",
                "nivel_conversacion": 20,
                "nivel_lectura": 20,
                "nivel_escritura": 20,
                "nativo": "si",
                "fecha_certificacion": ""
            },
            {
                "idioma": "spanish",
                "nivel_conversacion": 20,
                "nivel_lectura": 20,
                "nivel_escritura": 20,
                "nativo": "si",
                "fecha_certificacion": ""
            }
        ]
    }
    response = client.post("/public/register", json=data)
    # Validate the response
    assert response.status_code == 201


def test_register_company(client):
    data = {
        "email": "comercial@gansoscorp.com",
        "password": "gansosCorp",
        "role": "Company",
        "document_type": "NIT",
        "document_number": "2342352352",
        "name": "GANSOS CORPORATION",
        "phone_number": "3147654721",
        "country": "Colombia"
    }
    response = client.post("/public/register", json=data)
    # Validate the response
    assert response.status_code == 201


@patch('google.cloud.datastore.Client')
def test_login_bad_request(mock_datastore_client, client):
    mock_user_results = [
        {'salt': 'some_salt', 'password_hash': 'some_hash', 'user_id': 'some_user_id', 'role': 'some_role',
         'first_name': 'John', 'last_name': 'Doe'}]
    mock_client_instance = MagicMock()
    mock_datastore_client.return_value = mock_client_instance

    # Mock the get method of datastore.Client
    mock_client_instance.query.return_value.fetch.return_value = mock_user_results
    data = {
        "username": "garayurbina",
        "password": "chocoB0wser"
    }
    response = client.post("/public/login", json=data)
    # Validate the response
    assert response.status_code == 400


def test_post_failed_400(client):
    # Mocking request.json
    mock_request_json = {'username': 'some_username', 'password': 'some_password'}

    # Creating an instance of the class
    your_instance = VistaLogIn()

    # Mocking the request object
    your_instance.request = MagicMock()
    your_instance.request.json = mock_request_json

    response, status_code = your_instance.post()

    # Assertions
    assert status_code == 400


def test_login_admin_user(client):
    data = {
        "email": "jose@bowser.com",
        "password": "chocoB0wser",
        "role": "Admin"
    }
    response = client.post("/public/login", json=data)
    # Validate the response
    assert response.status_code == 200


def test_login_candidate(client):
    data = {
        "email": "jose@bowser.com",
        "password": "chocoB0wser",
        "role": "Candidate"
    }
    response = client.post("/public/login", json=data)
    # Validate the response
    assert response.status_code == 200


def test_login_company(client):
    data = {
        "email": "jose@bowser.com",
        "password": "chocoB0wser",
        "role": "Company"
    }
    response = client.post("/public/login", json=data)
    # Validate the response
    assert response.status_code == 200
