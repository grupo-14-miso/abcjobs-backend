from unittest.mock import patch, MagicMock
import pytest
from google.cloud.datastore import Entity

from main import app
from src.utils.utils import get_candidates_ready

# Mock firebase_admin for tests
firebase_admin = MagicMock()

# Set up mock return values or behaviors as needed
firebase_admin.initialize_app.return_value = None
firebase_admin.db.reference.return_value.get.return_value = {
    'user1': {'name': 'John', 'type': 'Developer'},
    'user2': {'name': 'Alice', 'type': 'Designer'},
    'user3': {'name': 'John', 'type': 'Tester'},
}
user_update_data = {
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
# Mock the Flask client
@pytest.fixture
def client():
    with patch('main.firebase_admin', firebase_admin):
        with patch('google.auth.default', return_value=(None, None)):  # Mock GCP authentication
            with patch('google.cloud.datastore.Client', autospec=True):  # Mock Datastore Client
                with app.test_client() as client:
                    yield client

def test_ping(client):
    response_valid = client.get("/users-get/ping")
    assert response_valid.json == "Pong"

def test_user_profile(client):
    # Perform a GET request to /users-get/profiles
    response = client.get('/users-get/profiles')

    # Validate the response
    assert response.status_code == 200


def test_get_all_users(client):
    # Perform a GET request to /users
    response = client.get('/users-get?rol=Devops&soft_skills=Hablador&lenguajes_programacion=Ingles&tecnologias_herramientas=Python&idiomas=Español')

    # Validate the response
    assert response.status_code == 200
    assert isinstance(response.json, list)


def test_get_candidato_exception(client):
    # Perform a GET request to /users
    try:
        response = client.get('/users-get/123')
    except:
        # Validate the response
        assert True


def test_get_users_ready(client):
    # Perform get request to users ready
    response = client.get('/users-get/ready/5163227868561408')
    assert response.status_code == 200



def test_get_candidates_ready(client):
    # Mock the necessary functions
    candidates = [Entity()]
    assignments = [Entity()]
    results = get_candidates_ready(candidates, [], [], [])
    assert isinstance(results, list)



