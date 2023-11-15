from unittest.mock import patch, MagicMock
import pytest
from main import app

# Mock firebase_admin for tests
firebase_admin = MagicMock()

# Set up mock return values or behaviors as needed
firebase_admin.initialize_app.return_value = None
firebase_admin.db.reference.return_value.get.return_value = {
    'user1': {'name': 'John', 'type': 'Developer'},
    'user2': {'name': 'Alice', 'type': 'Designer'},
    'user3': {'name': 'John', 'type': 'Tester'},
}

# Mock the Flask client
@pytest.fixture
def client():
    with patch('main.firebase_admin', firebase_admin):
        with patch('google.auth.default', return_value=(None, None)):  # Mock GCP authentication
            with patch('google.cloud.datastore.Client', autospec=True):  # Mock Datastore Client
                with app.test_client() as client:
                    yield client

def test_ping(client):
    response_valid = client.get("/users/ping")
    assert response_valid.json == "Pong"

def test_user_profile(client):
    # Perform a GET request to /users/profiles
    response = client.get('/users/profiles')

    # Validate the response
    assert response.status_code == 200
    

def test_create_profile(client):
    # Perform a POST request to /users/profiles
    data = {'name': 'NewUser', 'type': 'NewType'}
    response = client.post('/users/profiles', json=data)

    # Validate the response
    assert response.status_code == 201
    assert 'message' in response.json
    assert 'profile_id' in response.json

def test_create_user(client):
    # Perform a POST request to /users
    data = {
        "id_candidato": "correlation_id",
        "email": "email",
        "password": "password",
        "Nombre": "nombre",
        "apellido": "apellido",
        "segundo_nombre": "segundo_nombre",
        "segundo_apellido": "segundo_apellido",
        "tipo_documento": "documento",
        "documento": "documento",
        "fecha_nacimiento": "01-12-1994",
        "genero": "masculino|femenino|otro",
        "nacionalidad": "nacionalidad",
        "estado_civil": "soltero|casado|",
        "telefono": "273635363",
        "pais_nacimiento": "ecuador",
        "pais_residencia": "Colombia",
        "ciudad_nacimiento": "Guayaquil",
        "lenguajes_programacion": ["", "", ""],
        "tecnologias_herramientas": ["", "", ""],
        "ciudad_residencia": "Ibague",
        "educacion": [
            {
                "nivel_academico": "",
                "institucion": "",
                "titulo_obtenido": "",
                "fecha_inicio": "",
                "fecha_fin": "",
                "rol": "",
                "lenguajes_programacion": ["", "", ""],
                "tecnologias_herramientas": ["", "", ""]
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
                "idioma": "",
                "nivel_conversacion": 20,
                "nivel_lectura": 20,
                "nivel_escritura": 20,
                "nativo": "si",
                "fecha_certificacion": ""
            }
        ]
    }
    response = client.post('/users', json=data)

    # Validate the response
    assert response.status_code == 201
    assert 'message' in response.json
    assert 'profile_id' in response.json

def test_get_all_users(client):
    # Perform a GET request to /users
    response = client.get('/users')

    # Validate the response
    assert response.status_code == 200
    assert isinstance(response.json, list)