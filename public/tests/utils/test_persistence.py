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
def test_create_user(client):
    # Perform a user persistence operation
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
    response = persist_new_candidate(data, None, None)

    # Validate the response
    assert response is not None

